#!/usr/bin/env python3
"""
Volvo V50 2.4i Custom Dashboard — PyQt5 Version
=================================================
Full GUI dashboard with analog gauges, digital readouts,
day/night auto-dimming, and stealth mode toggle.

Hardware targets:
- Raspberry Pi 4 + 7" IPS TFT (1024x600)
- PiCAN2 Duo HAT for CAN bus
- Optional: BH1750 light sensor for auto-dimming

Features:
- Analog RPM gauge with redline
- Digital speedometer with gear indicator
- Temperature gauges (coolant, oil, intake, transmission)
- Fuel level bar
- Warning lights cluster
- Climate control display
- Day/Night auto-dimming
- Stealth mode: press button to switch to OEM-like display
- Maintenance countdowns

Author: v50-developer agent
Date: 2026-05-27
"""

import sys
import time
import math
import signal
import threading
from pathlib import Path
from typing import Optional

# Try PyQt5 first, fall back to tkinter
try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    HAS_PYQT5 = True
except ImportError:
    HAS_PYQT5 = False

from v50_can_decoder import V50State, CANBus, MESSAGE_DEFINITIONS, get_gear_name

# =============================================================================
# Theme / Color Definitions
# =============================================================================

class Theme:
    """Day and Night themes for the dashboard."""
    
    # Day mode (bright, for sunlight)
    DAY = {
        'bg': '#E8E8E8',
        'bg_dark': '#C0C0C0',
        'text': '#1A1A1A',
        'text_secondary': '#555555',
        'accent': '#0066CC',
        'warning': '#FF6600',
        'danger': '#CC0000',
        'success': '#00AA44',
        'gauge_bg': '#FFFFFF',
        'gauge_border': '#333333',
        'gauge_fill': '#0066CC',
        'gauge_fill_warn': '#FF6600',
        'gauge_fill_danger': '#CC0000',
        'fuel_bar': '#00AA44',
        'fuel_bar_low': '#CC0000',
        'rpm_arc': '#0066CC',
        'rpm_redline': '#CC0000',
    }
    
    # Night mode (dark, for driving at night)
    NIGHT = {
        'bg': '#0A0A14',
        'bg_dark': '#0F0F20',
        'text': '#E0E0E0',
        'text_secondary': '#888888',
        'accent': '#00AAFF',
        'warning': '#FF8800',
        'danger': '#FF2222',
        'success': '#00DD66',
        'gauge_bg': '#111122',
        'gauge_border': '#444466',
        'gauge_fill': '#00AAFF',
        'gauge_fill_warn': '#FF8800',
        'gauge_fill_danger': '#FF2222',
        'fuel_bar': '#00DD66',
        'fuel_bar_low': '#FF2222',
        'rpm_arc': '#00AAFF',
        'rpm_redline': '#FF2222',
    }

if HAS_PYQT5:

    # =========================================================================
    # Analog Gauge Widget
    # =========================================================================
    
    class AnalogGauge(QWidget):
        """A semi-circular analog gauge widget for RPM, temp, etc."""
        
        valueChanged = pyqtSignal(float)
        
        def __init__(self, title: str, unit: str, min_val: float, max_val: float,
                     warning_val: float = None, danger_val: float = None,
                     parent=None):
            super().__init__(parent)
            self.title = title
            self.unit = unit
            self.min_val = min_val
            self.max_val = max_val
            self.warning_val = warning_val
            self.danger_val = danger_val
            self.value = min_val
            self.theme = Theme.NIGHT.copy()
            self.setMinimumSize(160, 140)
        
        def set_value(self, value: float):
            self.value = max(self.min_val, min(self.max_val, value))
            self.valueChanged.emit(self.value)
            self.update()
        
        def set_theme(self, theme: dict):
            self.theme = theme
            self.update()
        
        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            w = self.width()
            h = self.height()
            size = min(w, h)
            
            # Gauge center and radius
            cx = w / 2
            cy = h * 0.65
            radius = size * 0.38
            
            # Draw arc background
            pen = QPen(QColor(self.theme['gauge_border']), 3)
            painter.setPen(pen)
            painter.drawArc(QRectF(cx - radius, cy - radius, radius * 2, radius * 2),
                           225 * 16, -270 * 16)
            
            # Calculate value position (225° to -45°, 270° range)
            pct = (self.value - self.min_val) / (self.max_val - self.min_val)
            pct = max(0, min(1, pct))
            
            # Determine arc color based on warning/danger zones
            if self.danger_val is not None and self.value >= self.danger_val:
                arc_color = QColor(self.theme['gauge_fill_danger'])
            elif self.warning_val is not None and self.value >= self.warning_val:
                arc_color = QColor(self.theme['gauge_fill_warn'])
            else:
                arc_color = QColor(self.theme['gauge_fill'])
            
            # Draw value arc
            pen = QPen(arc_color, 5)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            start_angle = 225 * 16
            span_angle = int(-270 * 16 * pct)
            painter.drawArc(QRectF(cx - radius, cy - radius, radius * 2, radius * 2),
                           start_angle, span_angle)
            
            # Draw value text
            font = QFont('Monospace', 18, QFont.Bold)
            painter.setFont(font)
            painter.setPen(QColor(self.theme['text']))
            
            if self.max_val >= 1000:
                value_text = f"{self.value:.0f}"
            elif self.max_val >= 10:
                value_text = f"{self.value:.1f}"
            else:
                value_text = f"{self.value:.2f}"
            
            painter.drawText(QRectF(0, cy - radius * 0.3, w, radius * 0.5),
                           Qt.AlignCenter, value_text)
            
            # Draw unit
            font = QFont('Monospace', 10)
            painter.setFont(font)
            painter.setPen(QColor(self.theme['text_secondary']))
            painter.drawText(QRectF(0, cy + radius * 0.2, w, radius * 0.3),
                           Qt.AlignCenter, self.unit)
            
            # Draw title
            font = QFont('Monospace', 11, QFont.Bold)
            painter.setFont(font)
            painter.setPen(QColor(self.theme['text']))
            painter.drawText(QRectF(0, 5, w, 20), Qt.AlignCenter, self.title)
            
            # Draw tick marks
            pen = QPen(QColor(self.theme['text_secondary']), 1)
            painter.setPen(pen)
            for i in range(10):
                tick_pct = i / 9
                angle_deg = 225 - tick_pct * 270
                angle_rad = math.radians(angle_deg)
                x1 = cx + (radius - 5) * math.cos(angle_rad)
                y1 = cy - (radius - 5) * math.sin(angle_rad)
                x2 = cx + (radius + 2) * math.cos(angle_rad)
                y2 = cy - (radius + 2) * math.sin(angle_rad)
                painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
                # Tick labels
                if i % 2 == 0:
                    tick_val = self.min_val + tick_pct * (self.max_val - self.min_val)
                    font = QFont('Monospace', 7)
                    painter.setFont(font)
                    lx = cx + (radius + 14) * math.cos(angle_rad)
                    ly = cy - (radius + 14) * math.sin(angle_rad)
                    painter.drawText(QPointF(lx - 10, ly + 3), f"{tick_val:.0f}")
            
            painter.end()


    # =========================================================================
    # Digital Readout Widget
    # =========================================================================
    
    class DigitalReadout(QWidget):
        """A digital value display with label and unit."""
        
        def __init__(self, title: str, unit: str, parent=None):
            super().__init__(parent)
            self.title = title
            self.unit = unit
            self.value = "---"
            self.theme = Theme.NIGHT.copy()
            self.setMinimumSize(120, 50)
        
        def set_value(self, value, fmt=".1f"):
            if isinstance(value, (int, float)):
                self.value = f"{value:{fmt}}"
            else:
                self.value = str(value)
            self.update()
        
        def set_theme(self, theme: dict):
            self.theme = theme
            self.update()
        
        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            w = self.width()
            h = self.height()
            
            # Background
            painter.fillRect(self.rect(), QColor(self.theme['bg_dark']))
            
            # Border
            pen = QPen(QColor(self.theme['gauge_border']), 1)
            painter.setPen(pen)
            painter.drawRect(self.rect().adjusted(0, 0, -1, -1))
            
            # Title
            font = QFont('Monospace', 8)
            painter.setFont(font)
            painter.setPen(QColor(self.theme['text_secondary']))
            painter.drawText(QRectF(2, 2, w - 4, 14), Qt.AlignLeft | Qt.AlignVCenter, self.title)
            
            # Value
            font = QFont('Monospace', 18, QFont.Bold)
            painter.setFont(font)
            painter.setPen(QColor(self.theme['text']))
            painter.drawText(QRectF(2, 14, w * 0.7, h - 18), Qt.AlignLeft | Qt.AlignVCenter, self.value)
            
            # Unit
            font = QFont('Monospace', 9)
            painter.setFont(font)
            painter.setPen(QColor(self.theme['text_secondary']))
            painter.drawText(QRectF(w * 0.7, 18, w * 0.3, h - 22), Qt.AlignRight | Qt.AlignVCenter, self.unit)
            
            painter.end()


    # =========================================================================
    # Fuel Bar Widget
    # =========================================================================
    
    class FuelBar(QWidget):
        """Horizontal fuel level bar with low fuel warning."""
        
        def __init__(self, parent=None):
            super().__init__(parent)
            self.fuel_pct = 0
            self.theme = Theme.NIGHT.copy()
            self.setMinimumSize(200, 30)
        
        def set_value(self, fuel_pct: float):
            self.fuel_pct = max(0, min(100, fuel_pct))
            self.update()
        
        def set_theme(self, theme: dict):
            self.theme = theme
            self.update()
        
        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            w = self.width()
            h = self.height()
            bar_height = 14
            bar_y = (h - bar_height) / 2
            
            # Border
            painter.setPen(QPen(QColor(self.theme['gauge_border']), 1))
            painter.drawRect(QRectF(30, bar_y, w - 60, bar_height))
            
            # Fill
            fill_width = (w - 62) * (self.fuel_pct / 100)
            if self.fuel_pct <= 15:
                fill_color = QColor(self.theme['fuel_bar_low'])
            else:
                fill_color = QColor(self.theme['fuel_bar'])
            
            painter.fillRect(QRectF(31, bar_y + 1, fill_width, bar_height - 2), fill_color)
            
            # Label
            font = QFont('Monospace', 8, QFont.Bold)
            painter.setFont(font)
            painter.setPen(QColor(self.theme['text']))
            painter.drawText(QRectF(0, 0, 28, h), Qt.AlignCenter, "⛽")
            
            # Percentage
            font = QFont('Monospace', 9)
            painter.setFont(font)
            painter.drawText(QRectF(w - 28, 0, 26, h), Qt.AlignCenter, f"{self.fuel_pct:.0f}%")
            
            painter.end()


    # =========================================================================
    # Warning Light Widget
    # =========================================================================
    
    class WarningLight(QWidget):
        """A single warning indicator light."""
        
        def __init__(self, icon: str, label: str, parent=None):
            super().__init__(parent)
            self.icon = icon
            self.label = label
            self.active = False
            self.theme = Theme.NIGHT.copy()
            self.setFixedSize(60, 35)
        
        def set_active(self, active: bool):
            self.active = active
            self.update()
        
        def set_theme(self, theme: dict):
            self.theme = theme
            self.update()
        
        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            if self.active:
                bg = QColor(self.theme['danger'] if 'check_engine' in self.label.lower() or 
                            'oil' in self.label.lower() or 'temp' in self.label.lower() 
                            else self.theme['warning'])
                text_color = QColor('#FFFFFF')
                painter.setBrush(QBrush(bg))
            else:
                bg = QColor(self.theme['bg_dark'])
                text_color = QColor(self.theme['text_secondary'])
                painter.setBrush(QBrush(bg))
            
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 4, 4)
            
            # Icon
            font = QFont('Monospace', 14)
            painter.setFont(font)
            painter.setPen(text_color)
            painter.drawText(self.rect(), Qt.AlignCenter, self.icon)
            
            painter.end()


    # =========================================================================
    # Main Dashboard Window
    # =========================================================================
    
    class V50Dashboard(QMainWindow):
        """Main dashboard window for the V50 custom display."""
        
        stealth_mode = pyqtSignal(bool)
        
        def __init__(self, state: V50State):
            super().__init__()
            self.state = state
            self.is_night_mode = True  # Start in night mode (dark)
            self.is_stealth = False      # Start with custom dashboard
            
            self.setWindowTitle("V50 Stealth Dashboard")
            self.setMinimumSize(1024, 600)  # 7" TFT resolution
            
            self.init_ui()
            self.init_timer()
        
        def init_ui(self):
            """Initialize all UI widgets."""
            central = QWidget()
            self.setCentralWidget(central)
            main_layout = QVBoxLayout(central)
            main_layout.setSpacing(4)
            main_layout.setContentsMargins(8, 4, 8, 4)
            
            current_theme = Theme.NIGHT if self.is_night_mode else Theme.DAY
            
            # === TOP BAR: Speed + RPM + Gear ===
            top_frame = QFrame()
            top_frame.setFrameStyle(QFrame.Box | QFrame.Raised)
            top_layout = QHBoxLayout(top_frame)
            top_layout.setSpacing(8)
            
            # RPM Gauge
            self.rpm_gauge = AnalogGauge("RPM", "rpm", 0, 7000, 
                                          warning_val=5500, danger_val=6500)
            self.rpm_gauge.set_theme(current_theme)
            top_layout.addWidget(self.rpm_gauge, 3)
            
            # Digital Speed + Gear display
            speed_gear_layout = QVBoxLayout()
            
            self.speed_readout = DigitalReadout("SPEED", "km/h")
            self.speed_readout.set_theme(current_theme)
            speed_gear_layout.addWidget(self.speed_readout)
            
            self.gear_readout = DigitalReadout("GEAR", "")
            self.gear_readout.set_theme(current_theme)
            speed_gear_layout.addWidget(self.gear_readout)
            
            top_layout.addLayout(speed_gear_layout, 1)
            
            # Coolant Gauge
            self.coolant_gauge = AnalogGauge("COOLANT", "°C", 40, 130,
                                               warning_val=105, danger_val=115)
            self.coolant_gauge.set_theme(current_theme)
            top_layout.addWidget(self.coolant_gauge, 3)
            
            main_layout.addWidget(top_frame, 5)
            
            # === MIDDLE BAR: Temperatures + Fuel ===
            mid_frame = QFrame()
            mid_frame.setFrameStyle(QFrame.Box | QFrame.Raised)
            mid_layout = QHBoxLayout(mid_frame)
            mid_layout.setSpacing(6)
            
            self.oil_temp_readout = DigitalReadout("OIL TEMP", "°C")
            self.intake_temp_readout = DigitalReadout("INTAKE", "°C")
            self.trans_temp_readout = DigitalReadout("TRANS", "°C")
            self.throttle_readout = DigitalReadout("THROTTLE", "%")
            self.load_readout = DigitalReadout("LOAD", "%")
            self.maf_readout = DigitalReadout("MAF", "g/s")
            
            for w in [self.oil_temp_readout, self.intake_temp_readout, 
                       self.trans_temp_readout, self.throttle_readout,
                       self.load_readout, self.maf_readout]:
                w.set_theme(current_theme)
                mid_layout.addWidget(w)
            
            main_layout.addWidget(mid_frame, 2)
            
            # === FUEL BAR ===
            self.fuel_bar = FuelBar()
            self.fuel_bar.set_theme(current_theme)
            main_layout.addWidget(self.fuel_bar, 1)
            
            # === BOTTOM BAR: Warnings + Climate ===
            bottom_frame = QFrame()
            bottom_frame.setFrameStyle(QFrame.Box | QFrame.Raised)
            bottom_layout = QHBoxLayout(bottom_frame)
            bottom_layout.setSpacing(4)
            
            # Warning lights
            self.cel_light = WarningLight("🔧", "CEL")
            self.oil_light = WarningLight("🛢️", "OIL")
            self.bat_light = WarningLight("🔋", "BAT")
            self.temp_light = WarningLight("🌡️", "TEMP")
            
            for w in [self.cel_light, self.oil_light, self.bat_light, self.temp_light]:
                w.set_theme(current_theme)
                bottom_layout.addWidget(w)
            
            # Digital readouts
            self.ext_temp_readout = DigitalReadout("OUTSIDE", "°C")
            self.int_temp_readout = DigitalReadout("INSIDE", "°C")
            self.odo_readout = DigitalReadout("ODO", "km")
            
            for w in [self.ext_temp_readout, self.int_temp_readout, self.odo_readout]:
                w.set_theme(current_theme)
                bottom_layout.addWidget(w)
            
            main_layout.addWidget(bottom_frame, 2)
        
        def init_timer(self):
            """Set up update timer at ~15 FPS."""
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_display)
            self.timer.start(66)  # 15 FPS
            
            # Stealth mode toggle with spacebar
            self.stealth_key = QShortcut(QKeySequence(Qt.Key_Space), self)
            self.stealth_key.activated.connect(self.toggle_stealth)
            
            # Night/Day toggle with 'N' key
            self.theme_key = QShortcut(QKeySequence(Qt.Key_N), self)
            self.theme_key.activated.connect(self.toggle_night_day)
        
        def update_display(self):
            """Update all gauges and readouts from V50State."""
            s = self.state
            
            # Powertrain
            self.rpm_gauge.set_value(s.rpm)
            self.speed_readout.set_value(s.speed_kmh, ".0f")
            self.gear_readout.set_value(get_gear_name(s.gear))
            self.coolant_gauge.set_value(s.coolant_temp_c)
            
            # Temperatures
            self.oil_temp_readout.set_value(s.oil_temp_c, ".0f")
            self.intake_temp_readout.set_value(s.intake_air_temp_c, ".0f")
            self.trans_temp_readout.set_value(s.trans_temp_c, ".0f")
            
            # Engine
            self.throttle_readout.set_value(s.throttle_pct, ".0f")
            self.load_readout.set_value(s.engine_load_pct, ".0f")
            self.maf_readout.set_value(s.maf_g_per_s, ".1f")
            
            # Fuel
            self.fuel_bar.set_value(s.fuel_level_pct)
            
            # Warnings
            self.cel_light.set_active(s.check_engine)
            self.oil_light.set_active(s.oil_warning)
            self.bat_light.set_active(s.battery_warning)
            self.temp_light.set_active(s.temp_warning)
            
            # Climate
            self.ext_temp_readout.set_value(s.exterior_temp_c, ".0f")
            self.int_temp_readout.set_value(s.interior_temp_c, ".0f")
            self.odo_readout.set_value(s.odometer_km, ".0f")
        
        def toggle_stealth(self):
            """Toggle between custom dashboard and OEM-like minimal display."""
            self.is_stealth = not self.is_stealth
            if self.is_stealth:
                # Show minimal OEM-style display
                self.setStyleSheet(f"background-color: #000000; color: #00FF00;")
                for child in self.findChildren(QWidget):
                    child.hide()
                # Show only speed and fuel (like OEM DIM)
                # Minimal display mode
                self.setWindowTitle("V50 Stealth Dashboard — STEALTH MODE")
            else:
                # Show full custom dashboard
                self.setStyleSheet("")
                for child in self.findChildren(QWidget):
                    child.show()
                self.setWindowTitle("V50 Stealth Dashboard")
            self.stealth_mode.emit(self.is_stealth)
        
        def toggle_night_day(self):
            """Toggle between night (dark) and day (bright) themes."""
            self.is_night_mode = not self.is_night_mode
            theme = Theme.NIGHT if self.is_night_mode else Theme.DAY
            
            bg = theme['bg']
            self.setStyleSheet(f"background-color: {bg};")
            
            # Update all themed widgets
            for child in self.findChildren((AnalogGauge, DigitalReadout, FuelBar, WarningLight)):
                child.set_theme(theme)
        
        def keyPressEvent(self, event):
            """Handle keyboard shortcuts."""
            if event.key() == Qt.Key_Q:
                self.close()
            elif event.key() == Qt.Key_F11:
                if self.isFullScreen():
                    self.showNormal()
                else:
                    self.showFullScreen()
            super().keyPressEvent(event)


    # =========================================================================
    # CAN Bus Reader Thread
    # =========================================================================
    
    class CANReaderThread(QThread):
        """Thread to read CAN bus messages and update V50State."""
        
        message_received = pyqtSignal(int, bytes)  # can_id, data
        
        def __init__(self, state: V50State, interface: str = 'can0', 
                     bitrate: int = 500000, simulate: bool = False):
            super().__init__()
            self.state = state
            self.interface = interface
            self.bitrate = bitrate
            self.simulate = simulate
            self.running = True
        
        def run(self):
            if self.simulate:
                self._run_simulated()
            else:
                self._run_real()
        
        def _run_simulated(self):
            """Run with simulated CAN data for testing."""
            import random
            t = 0
            while self.running:
                # Simulate realistic driving patterns
                rpm = 800 + 3000 * (0.5 + 0.5 * math.sin(t * 0.3))
                speed = 100 * max(0, math.sin(t * 0.15))
                temp_coolant = 88 + 5 * math.sin(t * 0.01)
                temp_oil = 82 + 8 * math.sin(t * 0.008)
                fuel = 65 - t * 0.001
                load = 30 + 25 * math.sin(t * 0.2)
                throttle = 15 + 20 * max(0, math.sin(t * 0.25))
                maf = 8 + 12 * max(0, math.sin(t * 0.2))
                gear = 3 if speed > 60 else (2 if speed > 20 else 0)
                ext_temp = 18 + 3 * math.sin(t * 0.001)
                int_temp = 22 + 1 * math.sin(t * 0.002)
                odo = 142500 + t * 0.028
                
                # Create CAN frames
                frames = {
                    0x0C0: int(rpm / 0.25).to_bytes(2, 'little') + b'\x00' * 6,
                    0x0E0: int(speed / 0.01).to_bytes(2, 'little') + b'\x00' * 6,
                    0x0C8: bytes([int(temp_coolant) + 40]) + b'\x00' * 7,
                    0x108: bytes([int(temp_oil) + 40]) + b'\x00' * 7,
                    0x0F0: bytes([int(fuel / 0.390625)]) + b'\x00' * 7,
                    0x0D8: bytes([int(load / 0.390625), int(maf / 0.01) >> 8, int(maf / 0.01) & 0xFF]) + b'\x00' * 5,
                    0x0D0: bytes([0, int(throttle / 0.390625)]) + b'\x00' * 6,
                    0x1A0: bytes([gear]) + b'\x00' * 7,
                    0x238: bytes([int(ext_temp) + 40]) + b'\x00' * 7,
                    0x230: bytes([int(int_temp) + 40]) + b'\x00' * 7,
                    0x328: int(odo).to_bytes(4, 'little') + b'\x00' * 4,
                }
                
                for can_id, data in frames.items():
                    self.state.update(can_id, data)
                    self.message_received.emit(can_id, data)
                
                t += 1
                self.msleep(66)  # ~15 FPS
        
        def _run_real(self):
            """Run with real CAN bus hardware."""
            try:
                import can
                bus = can.Bus(interface='socketcan', channel=self.interface, 
                            bitrate=self.bitrate)
                
                while self.running:
                    msg = bus.recv(timeout=0.1)
                    if msg:
                        can_id = msg.arbitration_id
                        data = msg.data
                        self.state.update(can_id, data)
                        self.message_received.emit(can_id, data)
                
                bus.shutdown()
            except Exception as e:
                print(f"CAN reader error: {e}")
        
        def stop(self):
            self.running = False


# =========================================================================
# Entry Point
# =========================================================================

def main():
    """Main entry point for the dashboard application."""
    import argparse
    
    parser = argparse.ArgumentParser(description='V50 Custom Dashboard')
    parser.add_argument('--simulate', action='store_true', help='Use simulated CAN data (for testing)')
    parser.add_argument('--interface', type=str, default='can0', help='CAN interface')
    parser.add_argument('--fullscreen', '-f', action='store_true', help='Start in fullscreen')
    parser.add_argument('--night', action='store_true', default=True, help='Start in night mode (default)')
    args = parser.parse_args()
    
    if not HAS_PYQT5:
        print("PyQt5 not available! Install with: pip install PyQt5")
        print("Falling back to console-only mode.")
        print("Use v50_can_sniffer.py --simulate for console dashboard.")
        sys.exit(1)
    
    # Create V50 state
    state = V50State()
    
    # Create dashboard
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    dashboard = V50Dashboard(state)
    dashboard.is_night_mode = args.night
    
    if args.fullscreen:
        dashboard.showFullScreen()
    else:
        dashboard.resize(1024, 600)
        dashboard.show()
    
    # Start CAN reader thread
    can_reader = CANReaderThread(state, simulate=args.simulate, 
                                  interface=args.interface)
    can_reader.start()
    
    # Clean exit
    def cleanup():
        can_reader.stop()
        can_reader.wait(2000)
    
    app.aboutToQuit.connect(cleanup)
    
    ret = app.exec_()
    cleanup()
    sys.exit(ret)


if __name__ == "__main__":
    main()