#!/usr/bin/env python3
"""
Volvo V50 2.4i — Dashboard Performance Monitor
================================================
Tracks FPS (frames per second), CAN bus throughput, and system resources.
Displays an overlay on the dashboard for development/debugging.

Performance targets:
- Dashboard render: ≥20 FPS (smooth gauges)
- CAN decode: ≥1000 frames/s (lightweight)
- CAN throughput: 500 kbps bus = ~5000 frames/s max
- Memory: <128MB for entire dashboard process
- CPU: <30% single core at steady state

Author: v50-developer agent
Date: 2026-05-28
"""

import logging
import os
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Optional, Deque

logger = logging.getLogger('v50.perf_monitor')


@dataclass
class PerformanceStats:
    """Snapshot of performance metrics."""
    timestamp: float = 0
    
    # Dashboard rendering
    fps: float = 0
    frame_time_ms: float = 0
    fps_min: float = 0
    fps_max: float = 0
    
    # CAN bus
    can_frames_per_sec: float = 0
    can_decode_time_ms: float = 0
    can_known_pct: float = 0  # % of frames with known CAN IDs
    
    # System resources
    cpu_pct: float = 0
    memory_mb: float = 0
    cpu_temp_c: float = 0
    
    # Uptime
    uptime_s: float = 0
    total_frames: int = 0
    total_dropped: int = 0


class PerformanceMonitor:
    """
    Lightweight performance monitor for the V50 dashboard.
    
    Tracks:
    - Render FPS using frame time tracking
    - CAN bus throughput and decode times
    - System CPU and memory usage
    - Pi CPU temperature
    
    Can display as a HUD overlay on the dashboard.
    """
    
    # FPS tracking
    FPS_WINDOW = 60  # Average over last 60 frames
    SLOW_FRAME_MS = 50  # >50ms = slow frame warning
    
    def __init__(self, enabled: bool = True, overlay: bool = True):
        self.enabled = enabled
        self.overlay = overlay
        
        # Frame timing
        self._frame_times: Deque[float] = deque(maxlen=self.FPS_WINDOW)
        self._last_frame_time: float = 0
        
        # CAN performance
        self._can_frame_times: Deque[float] = deque(maxlen=1000)
        self._can_decode_times: Deque[float] = deque(maxlen=1000)
        self._can_known_count: int = 0
        self._can_unknown_count: int = 0
        self._can_last_count_time: float = time.time()
        self._can_last_count: int = 0
        
        # Counters
        self._total_frames: int = 0
        self._total_dropped: int = 0
        self._start_time: float = time.time()
        
        # Stats cache
        self._last_stats: Optional[PerformanceStats] = None
        self._stats_update_interval: float = 0.5  # Update stats every 500ms
        self._last_stats_time: float = 0
    
    def frame_start(self):
        """Mark the start of a dashboard frame render."""
        if not self.enabled:
            return
        now = time.time()
        if self._last_frame_time > 0:
            frame_time = now - self._last_frame_time
            self._frame_times.append(frame_time)
            if frame_time > self.SLOW_FRAME_MS / 1000:
                logger.debug(f"Slow frame: {frame_time*1000:.1f}ms")
        self._last_frame_time = now
        self._total_frames += 1
    
    def frame_end(self):
        """Mark the end of a dashboard frame render."""
        pass  # FPS is measured between frame starts
    
    def can_frame_decoded(self, can_id: int, known: bool, decode_time_ms: float = 0):
        """Track a CAN frame decode."""
        if not self.enabled:
            return
        self._can_decode_times.append(decode_time_ms)
        self._can_frame_times.append(time.time())
        if known:
            self._can_known_count += 1
        else:
            self._can_unknown_count += 1
    
    def frame_dropped(self):
        """Track a dropped frame."""
        self._total_dropped += 1
    
    def get_stats(self) -> PerformanceStats:
        """Get current performance statistics."""
        now = time.time()
        
        # FPS calculation
        fps = 0
        frame_time_ms = 0
        fps_min = 0
        fps_max = 0
        
        if self._frame_times:
            avg_frame_time = sum(self._frame_times) / len(self._frame_times)
            fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
            frame_time_ms = avg_frame_time * 1000
            all_fps = [1.0 / t for t in self._frame_times if t > 0]
            fps_min = min(all_fps) if all_fps else 0
            fps_max = max(all_fps) if all_fps else 0
        
        # CAN throughput
        can_fps = 0
        can_decode_ms = 0
        can_known_pct = 0
        
        # Calculate frames per second over last second
        one_sec_ago = now - 1.0
        recent_can = [t for t in self._can_frame_times if t > one_sec_ago]
        can_fps = len(recent_can)
        
        if self._can_decode_times:
            can_decode_ms = sum(self._can_decode_times) / len(self._can_decode_times)
        
        total_can = self._can_known_count + self._can_unknown_count
        if total_can > 0:
            can_known_pct = self._can_known_count / total_can * 100
        
        # System resources
        cpu_pct = self._read_cpu_usage()
        memory_mb = self._read_memory_usage()
        cpu_temp = self._read_cpu_temp()
        
        stats = PerformanceStats(
            timestamp=now,
            fps=round(fps, 1),
            frame_time_ms=round(frame_time_ms, 1),
            fps_min=round(fps_min, 1),
            fps_max=round(fps_max, 1),
            can_frames_per_sec=round(can_fps, 0),
            can_decode_time_ms=round(can_decode_ms, 3),
            can_known_pct=round(can_known_pct, 1),
            cpu_pct=round(cpu_pct, 1),
            memory_mb=round(memory_mb, 1),
            cpu_temp_c=round(cpu_temp, 1),
            uptime_s=round(now - self._start_time, 0),
            total_frames=self._total_frames,
            total_dropped=self._total_dropped,
        )
        
        self._last_stats = stats
        return stats
    
    def get_overlay_text(self) -> str:
        """Get performance stats as a compact overlay string."""
        stats = self.get_stats()
        lines = [
            f"FPS: {stats.fps:.0f} ({stats.fps_min:.0f}-{stats.fps_max:.0f})",
            f"CAN: {stats.can_frames_per_sec:.0f} f/s ({stats.can_known_pct:.0f}% known)",
            f"CPU: {stats.cpu_pct:.0f}% | MEM: {stats.memory_mb:.0f}MB | {stats.cpu_temp_c:.0f}°C",
            f"Frames: {stats.total_frames} ({stats.total_dropped} dropped) | Up: {stats.uptime_s:.0f}s",
        ]
        return "\n".join(lines)
    
    def get_overlay_compact(self) -> str:
        """Get very compact performance overlay (single line)."""
        stats = self.get_stats()
        return (f"FPS:{stats.fps:.0f} CAN:{stats.can_frames_per_sec:.0f} "
                f"CPU:{stats.cpu_pct:.0f}% MEM:{stats.memory_mb:.0f}MB "
                f"T:{stats.cpu_temp_c:.0f}°C")
    
    # =========================================================================
    # System resource readers
    # =========================================================================
    
    def _read_cpu_usage(self) -> float:
        """Read CPU usage percentage (Linux)."""
        try:
            # Read from /proc/stat
            with open('/proc/stat', 'r') as f:
                line = f.readline()
            values = [int(v) for v in line.split()[1:8]]
            total = sum(values)
            idle = values[3]
            
            # Simple approximation
            if total > 0:
                return (1 - idle / total) * 100
        except Exception:
            pass
        return 0
    
    def _read_memory_usage(self) -> float:
        """Read process memory usage in MB (Linux)."""
        try:
            with open('/proc/self/status', 'r') as f:
                for line in f:
                    if line.startswith('VmRSS:'):
                        return int(line.split()[1]) / 1024  # KB to MB
        except Exception:
            pass
        return 0
    
    def _read_cpu_temp(self) -> float:
        """Read Pi CPU temperature."""
        temp_paths = [
            '/sys/class/thermal/thermal_zone0/temp',  # Pi
            '/sys/class/hwmon/hwmon0/temp1_input',     # Generic Linux
        ]
        for path in temp_paths:
            try:
                with open(path, 'r') as f:
                    temp = float(f.read().strip())
                if temp > 1000:  # millidegrees
                    temp = temp / 1000
                return temp
            except Exception:
                continue
        return 0


# =============================================================================
# PyQt5 Performance Overlay Widget
# =============================================================================

def create_perf_overlay(parent=None, monitor: PerformanceMonitor = None):
    """Create a PyQt5 QLabel overlay for the dashboard.
    
    Returns None if PyQt5 is not available.
    """
    try:
        from PyQt5.QtWidgets import QLabel
        from PyQt5.QtCore import QTimer, Qt
        from PyQt5.QtGui import QFont, QColor
    except ImportError:
        return None
    
    if monitor is None:
        monitor = PerformanceMonitor()
    
    class PerfOverlay(QLabel):
        def __init__(self, parent, perf_monitor):
            super().__init__(parent)
            self.perf = perf_monitor
            self.setFont(QFont("Monospace", 9))
            self.setStyleSheet("""
                QLabel {
                    background-color: rgba(0, 0, 0, 180);
                    color: #00FF00;
                    padding: 4px;
                    border-radius: 4px;
                }
            """)
            self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            self.setFixedSize(320, 64)
            self.move(5, 5)  # Top-left corner
            
            # Update timer
            self._timer = QTimer()
            self._timer.timeout.connect(self._update_text)
            self._timer.start(500)  # Update every 500ms
        
        def _update_text(self):
            self.setText(self.perf.get_overlay_compact())
    
    return PerfOverlay(parent, monitor)


if __name__ == "__main__":
    import time
    
    print("V50 Performance Monitor — Simulated Load Test")
    print("=" * 50)
    
    monitor = PerformanceMonitor()
    
    # Simulate dashboard rendering at ~30 FPS
    start = time.time()
    for i in range(300):  # 10 seconds at 30fps
        monitor.frame_start()
        time.sleep(0.033)  # ~30fps
        
        # Simulate CAN frames
        for can_id in range(20):
            monitor.can_frame_decoded(can_id, known=(can_id < 15), decode_time_ms=0.05)
        
        if i % 30 == 0:
            stats = monitor.get_stats()
            print(f"  {stats.uptime_s:.0f}s | FPS: {stats.fps:.1f} | "
                  f"CAN: {stats.can_frames_per_sec:.0f} f/s | "
                  f"Known: {stats.can_known_pct:.1f}% | "
                  f"CPU: {stats.cpu_pct:.0f}% | MEM: {stats.memory_mb:.0f}MB")
    
    print("\nFinal stats:")
    stats = monitor.get_stats()
    print(f"  Total frames: {stats.total_frames}")
    print(f"  Average FPS: {stats.fps:.1f} (min={stats.fps_min:.1f}, max={stats.fps_max:.1f})")
    print(f"  CAN throughput: {stats.can_frames_per_sec:.0f} f/s")
    print(f"  CAN known IDs: {stats.can_known_pct:.1f}%")
    print(f"  Uptime: {stats.uptime_s:.0f}s")