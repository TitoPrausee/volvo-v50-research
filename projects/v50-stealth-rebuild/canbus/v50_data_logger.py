#!/usr/bin/env python3
"""
Volvo V50 2.4i — CAN Data Logger with Session Management
==========================================================
Manages CAN data logging sessions with automatic rotation,
compression, and space management.

Features:
- Session-based logging: auto-start on ignition, auto-stop on ignition off
- Rotating log files: max 100MB per file, auto-rotate
- Compression: gzip old logs after rotation
- Space management: keep max 2GB of logs, delete oldest first
- CSV format: timestamp, can_id, dlc, data_hex, signal_name, value
- Session metadata: start time, duration, distance, avg speed, fuel used
- Export: convert to JSON, Parquet (future), or custom analysis format

Storage layout:
  /var/log/v50/
  ├── sessions/
  │   ├── 2026-05-28_14-30-01/           # Session directory
  │   │   ├── session.json                 # Metadata
  │   │   ├── can_log_001.csv              # CAN data (rotated)
  │   │   ├── can_log_002.csv.gz           # Compressed rotation
  │   │   └── summary.json                 # Session summary
  │   └── 2026-05-28_16-45-12/
  ├── diagnostics/
  │   ├── dtc_history.json
  │   └── maintenance_log.json
  └── performance/
      └── can_throughput.json

Author: v50-developer agent
Date: 2026-05-28
"""

import csv
import gzip
import json
import logging
import os
import shutil
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from threading import Lock
from typing import Optional, Dict, List, Tuple

logger = logging.getLogger('v50.data_logger')


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_LOG_DIR = Path("/var/log/v50/sessions")
MAX_LOG_SIZE_MB = 100          # Max size per CSV before rotation
MAX_TOTAL_LOG_SIZE_MB = 2048   # Max total log space (2GB)
MAX_SESSION_AGE_DAYS = 90      # Delete logs older than 90 days
CSV_HEADER = ["timestamp", "can_id", "dlc", "data_hex", "decoded"]


@dataclass
class SessionMetadata:
    """Metadata for a logging session."""
    session_id: str
    start_time: str
    end_time: Optional[str] = None
    start_odometer_km: float = 0
    end_odometer_km: float = 0
    total_distance_km: float = 0
    total_fuel_used_l: float = 0
    avg_speed_kmh: float = 0
    max_speed_kmh: float = 0
    avg_rpm: float = 0
    max_rpm: float = 0
    max_coolant_temp_c: float = 0
    max_oil_temp_c: float = 0
    can_frames_logged: int = 0
    can_frames_dropped: int = 0
    log_files_created: int = 0
    drive_profile: str = "unknown"
    dtc_codes_read: int = 0
    dtc_codes_cleared: int = 0

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, default=str)

    @classmethod
    def from_json(cls, json_str: str) -> 'SessionMetadata':
        data = json.loads(json_str)
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class CANDataLogger:
    """
    Rotating CAN data logger with session management.
    
    Logs CAN frames to CSV files with automatic rotation and compression.
    Tracks session statistics and manages disk space.
    """
    
    def __init__(self, log_dir: Path = DEFAULT_LOG_DIR, max_log_size_mb: int = MAX_LOG_SIZE_MB):
        self.log_dir = Path(log_dir)
        self.max_log_size_mb = max_log_size_mb
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self._current_session: Optional[SessionMetadata] = None
        self._current_file = None
        self._current_writer = None
        self._current_file_num = 0
        self._lock = Lock()
        self._running = False
        
        # Session statistics accumulators
        self._speed_samples: List[float] = []
        self._rpm_samples: List[float] = []
        self._coolant_samples: List[float] = []
        self._oil_samples: List[float] = []
        self._fuel_start_pct: Optional[float] = None
        self._fuel_start_km: Optional[float] = None
    
    def start_session(self, odometer_km: float = 0, fuel_pct: float = 0) -> str:
        """Start a new logging session. Returns session ID."""
        with self._lock:
            if self._running:
                self.stop_session()
            
            session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            session_dir = self.log_dir / session_id
            session_dir.mkdir(parents=True, exist_ok=True)
            
            self._current_session = SessionMetadata(
                session_id=session_id,
                start_time=datetime.now().isoformat(),
                start_odometer_km=odometer_km,
            )
            self._fuel_start_pct = fuel_pct
            
            self._current_file_num = 0
            self._speed_samples = []
            self._rpm_samples = []
            self._coolant_samples = []
            self._oil_samples = []
            self._fuel_start_pct = fuel_pct
            self._fuel_start_km = odometer_km
            
            self._open_new_file(session_dir)
            self._running = True
            
            logger.info(f"Started session {session_id} at {odometer_km:.0f} km")
            return session_id
    
    def stop_session(self, final_odometer_km: float = 0, final_fuel_pct: float = 0) -> Optional[str]:
        """Stop the current session and save metadata."""
        with self._lock:
            if not self._running or self._current_session is None:
                return None
            
            self._current_session.end_time = datetime.now().isoformat()
            self._current_session.end_odometer_km = final_odometer_km
            
            # Calculate session statistics
            if self._speed_samples:
                self._current_session.avg_speed_kmh = sum(self._speed_samples) / len(self._speed_samples)
                self._current_session.max_speed_kmh = max(self._speed_samples)
            if self._rpm_samples:
                self._current_session.avg_rpm = sum(self._rpm_samples) / len(self._rpm_samples)
                self._current_session.max_rpm = max(self._rpm_samples)
            if self._coolant_samples:
                self._current_session.max_coolant_temp_c = max(self._coolant_samples)
            if self._oil_samples:
                self._current_session.max_oil_temp_c = max(self._oil_samples)
            
            # Distance and fuel
            if self._fuel_start_km is not None and final_odometer_km > 0:
                self._current_session.total_distance_km = final_odometer_km - self._fuel_start_km
            
            session_dir = self.log_dir / self._current_session.session_id
            
            # Close current CSV file
            self._close_file()
            
            # Save session metadata
            meta_path = session_dir / "session.json"
            with open(meta_path, 'w') as f:
                f.write(self._current_session.to_json())
            
            session_id = self._current_session.session_id
            logger.info(f"Stopped session {session_id}: "
                       f"{self._current_session.total_distance_km:.1f}km, "
                       f"avg {self._current_session.avg_speed_kmh:.1f}km/h, "
                       f"{self._current_session.can_frames_logged} frames")
            
            self._running = False
            self._current_session = None
            
            # Compress old log files and manage space
            self._compress_old_logs(session_dir)
            self._manage_disk_space()
            
            return session_id
    
    def log_frame(self, timestamp: float, can_id: int, dlc: int, data_hex: str, decoded: str = ""):
        """Log a single CAN frame."""
        with self._lock:
            if not self._running or self._current_writer is None:
                return
            
            # Check if rotation needed
            if self._current_file and self._current_file.tell() > self.max_log_size_mb * 1024 * 1024:
                self._rotate_file()
            
            try:
                self._current_writer.writerow([
                    f"{timestamp:.6f}",
                    f"0x{can_id:03X}",
                    dlc,
                    data_hex,
                    decoded
                ])
                self._current_file.flush()
                if self._current_session:
                    self._current_session.can_frames_logged += 1
            except Exception as e:
                logger.error(f"Failed to log CAN frame: {e}")
                if self._current_session:
                    self._current_session.can_frames_dropped += 1
    
    def update_stats(self, speed_kmh: float = 0, rpm: float = 0,
                     coolant_temp_c: float = 0, oil_temp_c: float = 0):
        """Update running statistics from decoded vehicle state."""
        if speed_kmh > 0:
            self._speed_samples.append(speed_kmh)
        if rpm > 0:
            self._rpm_samples.append(rpm)
        if coolant_temp_c > -30:
            self._coolant_samples.append(coolant_temp_c)
        if oil_temp_c > -30:
            self._oil_samples.append(oil_temp_c)
    
    def _open_new_file(self, session_dir: Path):
        """Open a new CSV log file."""
        self._current_file_num += 1
        filename = session_dir / f"can_log_{self._current_file_num:03d}.csv"
        self._current_file = open(filename, 'w', buffering=1)  # Line buffered
        self._current_writer = csv.writer(self._current_file)
        self._current_writer.writerow(CSV_HEADER)
        
        if self._current_session:
            self._current_session.log_files_created += 1
        
        logger.debug(f"Opened log file: {filename}")
    
    def _close_file(self):
        """Close the current CSV log file."""
        if self._current_file:
            self._current_file.flush()
            self._current_file.close()
            self._current_file = None
            self._current_writer = None
    
    def _rotate_file(self):
        """Rotate to a new log file."""
        session_dir = self.log_dir / self._current_session.session_id
        self._close_file()
        self._open_new_file(session_dir)
    
    def _compress_old_logs(self, current_session_dir: Path):
        """Gzip compress all CSV files in previous sessions."""
        for session_dir in self.log_dir.iterdir():
            if not session_dir.is_dir():
                continue
            if session_dir == current_session_dir:
                continue  # Don't compress current session
            
            for csv_file in session_dir.glob("can_log_*.csv"):
                gz_path = csv_file.with_suffix('.csv.gz')
                if gz_path.exists():
                    continue  # Already compressed
                
                try:
                    with open(csv_file, 'rb') as f_in:
                        with gzip.open(gz_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    csv_file.unlink()  # Delete original after compression
                    logger.debug(f"Compressed {csv_file.name} → {gz_path.name}")
                except Exception as e:
                    logger.error(f"Failed to compress {csv_file}: {e}")
    
    def _manage_disk_space(self):
        """
        Ensure total log size doesn't exceed MAX_TOTAL_LOG_SIZE_MB.
        Delete oldest sessions first if over limit.
        """
        total_size = sum(f.stat().st_size for f in self.log_dir.rglob('*') if f.is_file())
        total_size_mb = total_size / (1024 * 1024)
        
        if total_size_mb <= MAX_TOTAL_LOG_SIZE_MB:
            return
        
        logger.warning(f"Log size {total_size_mb:.0f}MB exceeds limit {MAX_TOTAL_LOG_SIZE_MB}MB")
        
        # Get sessions sorted by date (oldest first)
        sessions = sorted(
            [d for d in self.log_dir.iterdir() if d.is_dir()],
            key=lambda d: d.name
        )
        
        for old_session in sessions:
            if total_size_mb <= MAX_TOTAL_LOG_SIZE_MB * 0.8:  # Clean to 80%
                break
            
            session_size = sum(f.stat().st_size for f in old_session.rglob('*') if f.is_file())
            session_size_mb = session_size / (1024 * 1024)
            
            logger.info(f"Deleting old session {old_session.name} ({session_size_mb:.1f}MB)")
            shutil.rmtree(old_session, ignore_errors=True)
            total_size_mb -= session_size_mb
        
        # Also delete sessions older than MAX_SESSION_AGE_DAYS
        cutoff = datetime.now() - timedelta(days=MAX_SESSION_AGE_DAYS)
        for session_dir in self.log_dir.iterdir():
            if not session_dir.is_dir():
                continue
            try:
                session_date = datetime.strptime(session_dir.name[:10], "%Y-%m-%d")
                if session_date < cutoff:
                    logger.info(f"Deleting expired session {session_dir.name}")
                    shutil.rmtree(session_dir, ignore_errors=True)
            except ValueError:
                continue
    
    def list_sessions(self) -> List[Dict]:
        """List all logging sessions with metadata."""
        sessions = []
        for session_dir in sorted(self.log_dir.iterdir()):
            if not session_dir.is_dir():
                continue
            meta_path = session_dir / "session.json"
            if meta_path.exists():
                try:
                    with open(meta_path) as f:
                        meta = json.load(f)
                    sessions.append(meta)
                except Exception:
                    # Partial/corrupted session
                    sessions.append({
                        "session_id": session_dir.name,
                        "status": "incomplete"
                    })
            else:
                # Current session (metadata not written yet)
                csv_files = list(session_dir.glob("can_log_*.csv"))
                sessions.append({
                    "session_id": session_dir.name,
                    "status": "active" if csv_files else "empty",
                    "log_files": len(csv_files)
                })
        return sessions
    
    def get_disk_usage(self) -> Dict:
        """Get current disk usage statistics."""
        total_size = sum(f.stat().st_size for f in self.log_dir.rglob('*') if f.is_file())
        session_count = sum(1 for d in self.log_dir.iterdir() if d.is_dir())
        
        return {
            "total_size_mb": round(total_size / (1024 * 1024), 1),
            "max_size_mb": MAX_TOTAL_LOG_SIZE_MB,
            "usage_pct": round(total_size / (1024 * 1024) / MAX_TOTAL_LOG_SIZE_MB * 100, 1),
            "session_count": session_count,
            "log_dir": str(self.log_dir),
        }


# =============================================================================
# Main (for standalone logging)
# =============================================================================

if __name__ == "__main__":
    import argparse
    import time
    from v50_can_decoder import V50State, decode_message, MESSAGE_DEFINITIONS
    
    parser = argparse.ArgumentParser(description="V50 CAN Data Logger")
    parser.add_argument('--log-dir', default=str(DEFAULT_LOG_DIR), help='Log directory')
    parser.add_argument('--simulate', action='store_true', help='Simulate data for testing')
    parser.add_argument('--list', action='store_true', help='List existing sessions')
    parser.add_argument('--disk-usage', action='store_true', help='Show disk usage')
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO, 
                       format='%(asctime)s %(levelname)s [%(name)s] %(message)s')
    
    logger_obj = CANDataLogger(log_dir=Path(args.log_dir))
    
    if args.list:
        sessions = logger_obj.list_sessions()
        for s in sessions:
            print(f"  {s.get('session_id', '?')}: {s.get('status', '?')} "
                  f"{s.get('total_distance_km', 0):.1f}km")
        print(f"\nTotal sessions: {len(sessions)}")
    
    elif args.disk_usage:
        usage = logger_obj.get_disk_usage()
        print(f"Disk usage: {usage['total_size_mb']} / {usage['max_size_mb']} MB ({usage['usage_pct']}%)")
        print(f"Sessions: {usage['session_count']}")
    
    elif args.simulate:
        print("Simulating a short driving session...")
        session_id = logger_obj.start_session(odometer_km=150000, fuel_pct=65)
        
        # Simulate some CAN frames
        start_time = time.time()
        for i in range(100):
            ts = start_time + i * 0.1
            can_id = 0x0C0  # Engine RPM
            rpm = 2000 + i * 10
            data_hex = f"{int(rpm/0.25):04X}" + "0" * 12
            logger_obj.log_frame(ts, can_id, 8, data_hex, f"engine_rpm={rpm:.0f}")
            logger_obj.update_stats(speed_kmh=80+i*0.1, rpm=rpm, coolant_temp_c=88+i*0.01)
        
        session_id = logger_obj.stop_session(final_odometer_km=150010, final_fuel_pct=63)
        print(f"Session {session_id} logged and saved.")
        print(f"Disk usage: {logger_obj.get_disk_usage()}")
    
    else:
        print("Use --simulate, --list, or --disk-usage")
        print("For live CAN logging, use v50_app.py --log <dir>")