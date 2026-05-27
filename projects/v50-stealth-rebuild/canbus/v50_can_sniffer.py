#!/usr/bin/env python3
"""
Volvo V50 2.4i CAN-Bus Sniffer, Logger & Diagnostics
======================================================
Live CAN bus monitoring with CSV logging, session recording,
DTC (Diagnostic Trouble Code) reading, and maintenance tracking.

Hardware: Raspberry Pi 4 + PiCAN2 Duo HAT
Bus: High-Speed CAN (500kbps) via OBD2 port
Requires: python-can, can-utils (for socketcan setup)

Usage:
    # Live monitor (requires PiCAN2 hardware)
    python3 v50_can_sniffer.py --monitor

    # Log to CSV file
    python3 v50_can_sniffer.py --log /path/to/session.csv

    # Read and clear DTCs
    python3 v50_can_sniffer.py --dtc

    # Maintenance tracker
    python3 v50_can_sniffer.py --maintenance

    # Replay a recorded session
    python3 v50_can_sniffer.py --replay /path/to/session.csv

Author: v50-developer agent
Date: 2026-05-27
"""

import argparse
import csv
import json
import logging
import os
import signal
import sys
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Dict, List

# Import the decoder
from v50_can_decoder import (
    V50State, CANBus, MESSAGE_DEFINITIONS,
    decode_message, extract_signal, list_known_messages,
    get_gear_name, calculate_fuel_consumption,
    OBD2_STANDARD_PIDS, VOLVO_PROPRIETARY_PIDS
)

logger = logging.getLogger('v50.sniffer')

# =============================================================================
# Configuration
# =============================================================================

CAN_INTERFACE = 'can0'
CAN_BITRATE_HS = 500000   # High-speed CAN
CAN_BITRATE_LS = 125000   # Low-speed CAN
LOG_DIR = Path('/opt/data/home/vehicle-database/projects/v50-stealth-rebuild/logs')
MAINTENANCE_FILE = Path('/opt/data/home/vehicle-database/projects/v50-stealth-rebuild/hardware/maintenance.json')

# Startup delay for CAN interface (seconds)
CAN_STARTUP_DELAY = 2.0

# Logger intervals
CONSOLE_UPDATE_INTERVAL = 0.5   # 2 FPS for console display
CSV_LOG_INTERVAL = 0.1          # 10 Hz logging
STALE_THRESHOLD = 5.0           # Mark data stale after 5 seconds


# =============================================================================
# CAN Bus Interface Setup
# =============================================================================

def setup_can_interface(interface: str = CAN_INTERFACE, bitrate: int = CAN_BITRATE_HS):
    """Configure the CAN interface using ip/link commands.
    
    Requires: can-utils, python-can
    The PiCAN2 Duo HAT creates /dev/spidev0.0 and uses socketcan.
    """
    import subprocess
    
    logger.info(f"Setting up {interface} at {bitrate}bps...")
    
    # Bring down interface first
    subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'], 
                   capture_output=True, timeout=5)
    
    # Configure CAN with bitrate
    result = subprocess.run(
        ['sudo', 'ip', 'link', 'set', interface, 'up', 
         'type', 'can', 'bitrate', str(bitrate)],
        capture_output=True, timeout=10
    )
    
    if result.returncode != 0:
        logger.error(f"Failed to setup CAN: {result.stderr.decode()}")
        logger.info("Try: sudo modprobe can && sudo modprobe can_raw && sudo modprobe mcp251x")
        logger.info("Also check /boot/config.txt for PiCAN2 overlay:")
        logger.info("  dtparam=spi=on")
        logger.info("  dtoverlay=mcp251x-can0,oscillator=16000000,interrupt=25")
        return False
    
    logger.info(f"CAN interface {interface} UP at {bitrate}bps")
    time.sleep(CAN_STARTUP_DELAY)
    return True


def create_can_bus(interface: str = CAN_INTERFACE, bitrate: int = CAN_BITRATE_HS):
    """Create a python-can Bus object for the V50."""
    try:
        import can
        bus = can.Bus(interface='socketcan', channel=interface, bitrate=bitrate)
        logger.info(f"python-can Bus created on {interface}")
        return bus
    except Exception as e:
        logger.error(f"Failed to create CAN bus: {e}")
        logger.info("Installation: pip install python-can")
        logger.info("Also requires: sudo apt install can-utils")
        return None


# =============================================================================
# CSV Logger
# =============================================================================

@dataclass
class CANLogEntry:
    """A single CAN message log entry."""
    timestamp: float
    can_id: int
    bus: str  # 'HS' or 'LS'
    dlc: int
    data_hex: str
    decoded: Optional[Dict[str, float]] = None


class CANLogger:
    """Logs CAN messages to CSV with rotation and compression."""
    
    def __init__(self, log_dir: Path, max_size_mb: int = 100):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.current_file = None
        self.current_size = 0
        self.entry_count = 0
        self._open_new_file()
    
    def _open_new_file(self):
        """Open a new log file with timestamp-based name."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.log_dir / f"v50_can_{timestamp}.csv"
        self.current_file = open(filename, 'w', newline='', buffering=1)
        self.current_size = 0
        self.entry_count = 0
        
        # Write CSV header
        writer = csv.writer(self.current_file)
        writer.writerow([
            'timestamp', 'can_id_hex', 'can_id_dec', 'bus', 'dlc', 
            'data_hex', 'message_name', 'decoded_signals'
        ])
        logger.info(f"Logging to: {filename}")
    
    def log(self, entry: CANLogEntry):
        """Write a CAN log entry to CSV."""
        msg_def = MESSAGE_DEFINITIONS.get(entry.can_id)
        msg_name = msg_def.name if msg_def else "UNKNOWN"
        bus_name = "HS" if (msg_def and msg_def.bus == CANBus.HIGH_SPEED) else "LS"
        
        decoded_str = ""
        if entry.decoded:
            decoded_str = json.dumps(entry.decoded)
        
        row = [
            f"{entry.timestamp:.6f}",
            f"0x{entry.can_id:03X}",
            entry.can_id,
            bus_name,
            entry.dlc,
            entry.data_hex,
            msg_name,
            decoded_str
        ]
        
        writer = csv.writer(self.current_file)
        writer.writerow(row)
        self.entry_count += 1
        
        # Check rotation
        self.current_size += sum(len(str(f)) for f in row) + len(row)
        if self.current_size > self.max_size_bytes:
            self.current_file.close()
            self._open_new_file()
    
    def close(self):
        """Close the current log file."""
        if self.current_file:
            logger.info(f"Closed log file. {self.entry_count} entries written.")
            self.current_file.close()


# =============================================================================
# Session Recorder
# =============================================================================

class SessionRecorder:
    """Records complete driving sessions for later replay and analysis."""
    
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.entries: List[CANLogEntry] = []
        self.start_time = None
    
    def start(self):
        """Start a new recording session."""
        self.entries = []
        self.start_time = time.time()
        logger.info("Recording session started")
    
    def record(self, can_id: int, data: bytes, bus: str = 'HS'):
        """Record a CAN message."""
        entry = CANLogEntry(
            timestamp=time.time(),
            can_id=can_id,
            bus=bus,
            dlc=len(data),
            data_hex=data.hex(),
            decoded=decode_message(can_id, data)
        )
        self.entries.append(entry)
    
    def stop(self) -> Path:
        """Stop recording and save to file."""
        if not self.entries:
            logger.warning("No entries to save")
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.log_dir / f"v50_session_{timestamp}.csv"
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'can_id_hex', 'can_id_dec', 'bus', 'dlc', 
                           'data_hex', 'message_name', 'decoded_signals'])
            
            for entry in self.entries:
                msg_def = MESSAGE_DEFINITIONS.get(entry.can_id)
                msg_name = msg_def.name if msg_def else "UNKNOWN"
                decoded_str = json.dumps(entry.decoded) if entry.decoded else ""
                
                writer.writerow([
                    f"{entry.timestamp - self.entries[0].timestamp:.6f}",
                    f"0x{entry.can_id:03X}",
                    entry.can_id,
                    entry.bus,
                    entry.dlc,
                    entry.data_hex,
                    msg_name,
                    decoded_str
                ])
        
        logger.info(f"Session saved: {filename} ({len(self.entries)} entries)")
        return filename
    
    def replay(self, filename: Path, state: V50State, speed: float = 1.0, 
               callback=None) -> Dict[str, int]:
        """Replay a recorded session from CSV file.
        
        Args:
            filename: Path to session CSV
            state: V50State object to update
            speed: Replay speed (1.0 = real time, 2.0 = double speed)
            callback: Optional function(state, entry) called per message
        """
        stats = {"messages": 0, "decoded": 0, "unknown": 0}
        
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            prev_time = None
            
            for row in reader:
                # Parse entry
                rel_time = float(row['timestamp'])
                can_id = int(row['can_id_dec'])
                data = bytes.fromhex(row['data_hex'])
                
                # Wait for real-time replay
                if prev_time is not None and speed > 0:
                    delay = (rel_time - prev_time) / speed
                    if delay > 0:
                        time.sleep(min(delay, 0.1))  # Cap sleep to avoid long waits
                
                prev_time = rel_time
                
                # Update state
                state.update(can_id, data)
                stats["messages"] += 1
                
                if can_id in MESSAGE_DEFINITIONS:
                    stats["decoded"] += 1
                else:
                    stats["unknown"] += 1
                
                if callback:
                    callback(state, row)
        
        return stats


# =============================================================================
# DTC Reader (OBD2 Diagnostics)
# =============================================================================

class DTCReader:
    """Reads and clears Diagnostic Trouble Codes from the V50 via OBD2.
    
    Uses ISO 15765-4 (CAN-based OBD2) on the high-speed bus.
    This replaces the need for VIDA/DICE for basic fault code reading.
    """
    
    # OBD2 mode bytes
    MODE_CURRENT = 0x01       # Current data
    MODE_FREEZE = 0x02        # Freeze frame data
    MODE_DTC = 0x03           # Request DTCs
    MODE_CLEAR = 0x04         # Clear DTCs
    MODE_O2_MONITOR = 0x05    # O2 sensor monitoring
    MODE_ONBOARD = 0x06       # On-board monitoring
    MODE_PENDING = 0x07       # Pending DTCs
    MODE_PERM_DTC = 0x0A      # Permanent DTCs
    
    # V50 specific: OBD2 request CAN IDs
    OBD2_REQUEST_ID = 0x7E0   # ECM request ID
    OBD2_RESPONSE_ID = 0x7E8  # ECM response ID
    TCM_REQUEST_ID = 0x7E1   # TCM request ID
    TCM_RESPONSE_ID = 0x7E9  # TCM response ID
    
    def __init__(self, bus=None):
        self.bus = bus
        self.dtcs: List[Dict] = []
    
    def _send_request(self, can_id: int, data: List[int]) -> Optional[bytes]:
        """Send an OBD2 request and wait for response."""
        try:
            import can
            msg = can.Message(arbitration_id=can_id, data=data[:8], is_extended_id=False)
            self.bus.send(msg)
            
            # Wait for response (timeout 2 seconds)
            start = time.time()
            while time.time() - start < 2.0:
                response = self.bus.recv(timeout=0.5)
                if response and response.arbitration_id in [self.OBD2_RESPONSE_ID, self.TCM_RESPONSE_ID]:
                    return response.data
            return None
        except Exception as e:
            logger.error(f"OBD2 request failed: {e}")
            return None
    
    def read_current_data(self, pid: int) -> Optional[float]:
        """Read current data for a standard OBD2 PID."""
        response = self._send_request(self.OBD2_REQUEST_ID, [self.MODE_CURRENT, pid])
        if response and len(response) >= 3 and response[0] == self.MODE_CURRENT + 0x40:
            # Parse PID response
            pid_resp = response[1]
            if pid_resp == pid:
                return response  # Return raw bytes for parsing
        return None
    
    def read_dtcs(self) -> List[Dict]:
        """Read stored Diagnostic Trouble Codes.
        
        Returns list of DTC dicts with keys:
            code: e.g., "P0171"
            description: human-readable description
            status: stored/pending/permanent
        """
        results = []
        
        # Read stored DTCs (Mode 03)
        response = self._send_request(self.OBD2_REQUEST_ID, [self.MODE_DTC])
        if response:
            dtcs = self._parse_dtc_response(response, "stored")
            results.extend(dtcs)
        
        # Read pending DTCs (Mode 07)
        response = self._send_request(self.OBD2_REQUEST_ID, [self.MODE_PENDING])
        if response:
            dtcs = self._parse_dtc_response(response, "pending")
            results.extend(dtcs)
        
        # Read permanent DTCs (Mode 0A)
        response = self._send_request(self.OBD2_REQUEST_ID, [self.MODE_PERM_DTC])
        if response:
            dtcs = self._parse_dtc_response(response, "permanent")
            results.extend(dtcs)
        
        self.dtcs = results
        return results
    
    def clear_dtcs(self) -> bool:
        """Clear all stored DTCs and reset the MIL.
        
        WARNING: This clears the Check Engine Light and all stored codes.
        Only do this after recording the codes!
        """
        response = self._send_request(self.OBD2_REQUEST_ID, [self.MODE_CLEAR])
        return response is not None
    
    def _parse_dtc_response(self, data: bytes, status: str) -> List[Dict]:
        """Parse DTC response bytes into human-readable codes."""
        dtcs = []
        
        if len(data) < 3 or data[0] not in [0x43, 0x47, 0x4A]:
            return dtcs
        
        # Number of DTCs is in the first byte after the response mode
        # Each DTC is 2 bytes: A B → CCDD where CC=type, DD=code
        i = 2  # Skip mode response + count byte
        while i + 1 < len(data):
            byte_a = data[i]
            byte_b = data[i + 1]
            
            # Decode DTC type (first 2 bits of byte A)
            type_char = {0: 'P', 1: 'C', 2: 'B', 3: 'U'}.get((byte_a >> 6) & 0x03, '?')
            
            # Decode code number
            code_num = ((byte_a & 0x3F) << 8) | byte_b
            code_str = f"{type_char}{code_num:04d}"
            
            description = self._lookup_dtc_description(code_str)
            
            dtcs.append({
                "code": code_str,
                "description": description,
                "status": status
            })
            i += 2
        
        return dtcs
    
    @staticmethod
    def _lookup_dtc_description(code: str) -> str:
        """Common V50 / Volvo DTC descriptions.
        
        This is a subset of common codes. For a complete database,
        use a DTC lookup service or the VIDA DTC database.
        """
        DTC_LOOKUP = {
            "P0171": "System too lean (Bank 1) — common on B5244S, vacuum leak or MAF",
            "P0172": "System too rich (Bank 1)",
            "P0174": "System too lean (Bank 2)",
            "P0175": "System too rich (Bank 2)",
            "P0300": "Random misfire detected",
            "P0301": "Cylinder 1 misfire detected",
            "P0302": "Cylinder 2 misfire detected",
            "P0303": "Cylinder 3 misfire detected",
            "P0304": "Cylinder 4 misfire detected",
            "P0305": "Cylinder 5 misfire detected — B5244S specific!",
            "P0420": "Catalyst system efficiency below threshold (Bank 1)",
            "P0442": "EVAP small leak detected",
            "P0456": "EVAP very small leak detected",
            "P0500": "Vehicle speed sensor malfunction",
            "P0700": "Transmission control system malfunction — AW55-51",
            "P0715": "Transmission fluid temp sensor — AW55-51 specific",
            "P0750": "Shift solenoid A malfunction",
            "P0755": "Shift solenoid B malfunction",
            "P1288": "ETM (Electronic Throttle Module) — common V50 issue!",
            "P2100": "Throttle actuator control system — ETM related",
            "P2135": "Throttle position sensor correlation — ETM related",
            "P2187": "Fuel adaptation too lean at idle — vacuum leak",
            "P2188": "Fuel adaptation too rich at idle",
            "P0128": "Coolant thermostat — thermostat stuck open",
            "P0116": "Coolant temp sensor range/performance",
            "P0117": "Coolant temp sensor circuit low",
            "P0118": "Coolant temp sensor circuit high",
            "B0001": "Airbag warning lamp circuit — common V50 issue",
            "B0003": "Airbag crash sensor",
            "C0000": "ABS system — check brake fluid level",
            "C0035": "Left front wheel speed sensor — ABS",
            "C0040": "Right front wheel speed sensor — ABS",
            "U0001": "High-Speed CAN bus communication error",
            "U0073": "CAN bus A (high-speed) off — serious bus error",
            "U0100": "Lost communication with ECM — check CAN wiring",
            "U0140": "Lost communication with BCM (CEM) — common CAN issue",
        }
        return DTC_LOOKUP.get(code, f"Unknown DTC — look up in VIDA")


# =============================================================================
# Maintenance Tracker
# =============================================================================

class MaintenanceTracker:
    """Track maintenance intervals based on odometer readings from CAN bus.
    
    Stores maintenance events in JSON file with km-based countdowns.
    """
    
    DEFAULT_INTERVALS = {
        "oil_change": {"interval_km": 15000, "interval_months": 12, "last_km": 0, "last_date": ""},
        "oil_filter": {"interval_km": 15000, "interval_months": 12, "last_km": 0, "last_date": ""},
        "air_filter": {"interval_km": 30000, "interval_months": 24, "last_km": 0, "last_date": ""},
        "cabin_filter": {"interval_km": 30000, "interval_months": 24, "last_km": 0, "last_date": ""},
        "brake_fluid": {"interval_km": 60000, "interval_months": 24, "last_km": 0, "last_date": ""},
        "spark_plugs": {"interval_km": 60000, "interval_months": 48, "last_km": 0, "last_date": ""},
        "timing_belt": {"interval_km": 120000, "interval_months": 120, "last_km": 0, "last_date": ""},
        "coolant": {"interval_km": 60000, "interval_months": 36, "last_km": 0, "last_date": ""},
        "transmission_fluid": {"interval_km": 60000, "interval_months": 48, "last_km": 0, "last_date": ""},
        "brake_pads_front": {"interval_km": 40000, "interval_months": 36, "last_km": 0, "last_date": ""},
        "brake_pads_rear": {"interval_km": 50000, "interval_months": 36, "last_km": 0, "last_date": ""},
        "tire_rotation": {"interval_km": 10000, "interval_months": 12, "last_km": 0, "last_date": ""},
    }
    
    def __init__(self, filepath: Path = MAINTENANCE_FILE):
        self.filepath = filepath
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()
    
    def _load(self) -> Dict:
        """Load maintenance data from JSON file."""
        if self.filepath.exists():
            with open(self.filepath, 'r') as f:
                return json.load(f)
        return {
            "current_odometer_km": 0,
            "intervals": self.DEFAULT_INTERVALS.copy(),
            "notes": []
        }
    
    def _save(self):
        """Save maintenance data to JSON file."""
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def update_odometer(self, km: float):
        """Update current odometer reading."""
        self.data["current_odometer_km"] = km
        self._save()
    
    def record_service(self, item: str, km: float = None, date: str = None):
        """Record a maintenance service event."""
        if item not in self.data["intervals"]:
            raise ValueError(f"Unknown maintenance item: {item}")
        
        if km is None:
            km = self.data["current_odometer_km"]
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        self.data["intervals"][item]["last_km"] = km
        self.data["intervals"][item]["last_date"] = date
        self._save()
        
        logger.info(f"Recorded {item} at {km:.0f} km on {date}")
    
    def get_status(self) -> List[Dict]:
        """Get maintenance status for all items.
        
        Returns list of dicts with keys: item, last_km, km_remaining, months_remaining, status
        """
        current_km = self.data["current_odometer_km"]
        results = []
        
        for item, config in self.data["intervals"].items():
            km_remaining = config["interval_km"] - (current_km - config["last_km"])
            
            # Calculate months remaining
            if config["last_date"]:
                last_date = datetime.strptime(config["last_date"], '%Y-%m-%d')
                months_elapsed = (datetime.now() - last_date).days / 30.44
                months_remaining = config["interval_months"] - months_elapsed
            else:
                months_remaining = None
            
            # Determine status
            if km_remaining <= 0 or (months_remaining is not None and months_remaining <= 0):
                status = "🔴 OVERDUE"
            elif km_remaining <= config["interval_km"] * 0.1:
                status = "🟡 DUE SOON"
            else:
                status = "✅ OK"
            
            results.append({
                "item": item,
                "interval_km": config["interval_km"],
                "last_km": config["last_km"],
                "km_remaining": km_remaining,
                "months_remaining": months_remaining,
                "status": status
            })
        
        return sorted(results, key=lambda x: x["km_remaining"])
    
    def print_status(self):
        """Print a formatted maintenance status report."""
        status = self.get_status()
        current_km = self.data["current_odometer_km"]
        
        print(f"\n{'='*60}")
        print(f"V50 Maintenance Status — Odometer: {current_km:,.0f} km")
        print(f"{'='*60}")
        print(f"{'Item':<25} {'Interval':<10} {'Last Km':<10} {'Remaining':<12} {'Status'}")
        print(f"{'-'*25} {'-'*10} {'-'*10} {'-'*12} {'-'*10}")
        
        for s in status:
            km_rem = f"{s['km_remaining']:,.0f} km"
            print(f"{s['item']:<25} {s['interval_km']:<10} {s['last_km']:<10} {km_rem:<12} {s['status']}")
        
        print(f"{'='*60}\n")


# =============================================================================
# CAN Bus Sniffer (Unknown Message Detector)
# =============================================================================

class CANSniffer:
    """Monitors CAN bus for unknown/unexpected messages.
    
    Tracks all CAN IDs seen and flags any that aren't in MESSAGE_DEFINITIONS.
    Useful for discovering new V50 P1 CAN messages.
    """
    
    def __init__(self):
        self.known_ids = set(MESSAGE_DEFINITIONS.keys())
        self.seen_ids: Dict[int, int] = {}  # can_id -> count
        self.unknown_ids: Dict[int, List[bytes]] = {}  # can_id -> [data_samples]
        self.start_time = time.time()
    
    def process(self, can_id: int, data: bytes):
        """Process a CAN message for sniffing."""
        # Track message count
        if can_id not in self.seen_ids:
            self.seen_ids[can_id] = 0
        self.seen_ids[can_id] += 1
        
        # Flag unknown messages
        if can_id not in self.known_ids:
            if can_id not in self.unknown_ids:
                self.unknown_ids[can_id] = []
            # Keep up to 10 samples per unknown ID
            if len(self.unknown_ids[can_id]) < 10:
                self.unknown_ids[can_id].append(data)
    
    def report(self) -> str:
        """Generate a sniffer report."""
        duration = time.time() - self.start_time
        lines = [
            f"\n=== CAN Bus Sniffer Report ({duration:.0f}s) ===",
            f"Total unique CAN IDs seen: {len(self.seen_ids)}",
            f"Known IDs: {len([k for k in self.seen_ids if k in self.known_ids])}",
            f"Unknown IDs: {len(self.unknown_ids)}",
            f"Total messages: {sum(self.seen_ids.values())}",
        ]
        
        # Message frequency
        lines.append("\n--- Message Frequency (sorted by count) ---")
        for can_id, count in sorted(self.seen_ids.items(), key=lambda x: -x[1]):
            is_known = "✓" if can_id in self.known_ids else "?"
            name = MESSAGE_DEFINITIONS[can_id].name if can_id in MESSAGE_DEFINITIONS else "UNKNOWN"
            rate = count / duration if duration > 0 else 0
            lines.append(f"  0x{can_id:03X} | {is_known} | {name:<25} | {count:>6} msgs | {rate:>6.1f} Hz")
        
        # Unknown messages detail
        if self.unknown_ids:
            lines.append("\n--- UNKNOWN Messages (need investigation!) ---")
            for can_id, samples in sorted(self.unknown_ids.items()):
                lines.append(f"  0x{can_id:03X}: {len(samples)} samples, count={self.seen_ids[can_id]}")
                for i, sample in enumerate(samples[:5]):
                    lines.append(f"    sample {i+1}: {sample.hex()}")
        
        return "\n".join(lines)


# =============================================================================
# Live Monitor (Console Display)
# =============================================================================

class LiveMonitor:
    """Real-time console display of V50 CAN bus data.
    
    Shows dashboard-style output with RPM, speed, temperatures,
    fuel, warnings, and more. Updates at 2 FPS.
    """
    
    def __init__(self, state: V50State, sniffer: CANSniffer = None):
        self.state = state
        self.sniffer = sniffer
        self.running = False
        self.message_count = 0
        self.last_display = 0
    
    def update(self, can_id: int, data: bytes):
        """Process an incoming CAN message."""
        self.state.update(can_id, data)
        self.message_count += 1
        if self.sniffer:
            self.sniffer.process(can_id, data)
    
    def render(self) -> str:
        """Render the dashboard display."""
        s = self.state
        
        # Staleness indicators
        rpm_stale = s.get_staleness(0x0C0) is not None and s.get_staleness(0x0C0) > STALE_THRESHOLD
        speed_stale = s.get_staleness(0x0E0) is not None and s.get_staleness(0x0E0) > STALE_THRESHOLD
        
        rpm_warning = " ⚠️ STALE" if rpm_stale else ""
        speed_warning = " ⚠️ STALE" if speed_stale else ""
        
        # RPM bar (0-7000, normalized to 50 chars)
        rpm_bar_len = 50
        rpm_pct = min(s.rpm / 7000, 1.0)
        rpm_bar = "█" * int(rpm_pct * rpm_bar_len) + "░" * (rpm_bar_len - int(rpm_pct * rpm_bar_len))
        
        # Fuel bar
        fuel_pct = s.fuel_level_pct / 100
        fuel_bar = "█" * int(fuel_pct * 20) + "░" * (20 - int(fuel_pct * 20))
        
        # Temp bar (cold=0, 60°C=middle, 120°C=max)
        temp_pct = max(0, min(1, (s.coolant_temp_c - 0) / 120))
        temp_bar = "█" * int(temp_pct * 30) + "░" * (30 - int(temp_pct * 30))
        
        # Warnings
        warnings = []
        if s.check_engine: warnings.append("⚠️ CHECK ENGINE")
        if s.oil_warning: warnings.append("🔴 OIL PRESSURE")
        if s.battery_warning: warnings.append("⚠️ BATTERY")
        if s.temp_warning: warnings.append("🌡️ HIGH TEMP")
        if s.oil_temp_c > 120: warnings.append("🌡️ OIL TEMP HIGH")
        if s.coolant_temp_c > 105: warnings.append("🌡️ COOLANT HIGH")
        warning_str = " | ".join(warnings) if warnings else "✅ No warnings"
        
        # Gear display
        gear_str = get_gear_name(s.gear)
        
        lines = [
            f"\n{'='*65}",
            f"  🚗 Volvo V50 2.4i — CAN Dashboard — CAN msgs: {self.message_count}",
            f"{'='*65}",
            f"",
            f"  🔧 RPM: {s.rpm:>7.0f} {rpm_warning}",
            f"  [{rpm_bar}] {s.rpm:.0f}/7000",
            f"",
            f"  🏎️  Speed: {s.speed_kmh:>6.1f} km/h{speed_warning}",
            f"  🌡️  Coolant: {s.coolant_temp_c:>5.0f}°C [{temp_bar}]",
            f"  🛢️  Oil: {s.oil_temp_c:>5.0f}°C | Intake: {s.intake_air_temp_c:>5.0f}°C",
            f"  ⛽  Fuel: [{fuel_bar}] {s.fuel_level_pct:>5.1f}%",
            f"  ⚙️  Gear: {gear_str} | Trans: {s.trans_temp_c:>5.0f}°C",
            f"  📊  Throttle: {s.throttle_pct:>5.1f}% | Load: {s.engine_load_pct:>5.1f}% | MAF: {s.maf_g_per_s:>5.1f} g/s",
            f"",
            f"  🌡️  Interior: {s.interior_temp_c:>5.0f}°C | Exterior: {s.exterior_temp_c:>5.0f}°C",
            f"  ❄️  A/C: {'ON' if s.ac_active else 'OFF'} | Fan: {s.fan_speed} | Recirc: {'ON' if s.recirc_active else 'OFF'}",
            f"  🚪  Doors: Driver={'OPEN' if s.driver_door_open else 'closed'} {'LOCKED' if s.driver_door_locked else 'unlocked'}",
            f"",
            f"  {warning_str}",
            f"{'='*65}",
        ]
        
        return "\n".join(lines)


# =============================================================================
# Main Entry Point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='V50 CAN Bus Sniffer & Diagnostics')
    parser.add_argument('--monitor', action='store_true', help='Live console monitor')
    parser.add_argument('--log', type=str, help='Log to CSV file (path)')
    parser.add_argument('--replay', type=str, help='Replay a recorded session')
    parser.add_argument('--dtc', action='store_true', help='Read Diagnostic Trouble Codes')
    parser.add_argument('--clear-dtc', action='store_true', help='Clear all DTCs (CAUTION!)')
    parser.add_argument('--maintenance', action='store_true', help='Show maintenance status')
    parser.add_argument('--record-service', type=str, help='Record service: item_name')
    parser.add_argument('--sniff', action='store_true', help='Sniff for unknown CAN messages')
    parser.add_argument('--interface', type=str, default='can0', help='CAN interface')
    parser.add_argument('--bitrate', type=int, default=500000, help='CAN bitrate')
    parser.add_argument('--list-messages', action='store_true', help='List all known CAN messages')
    parser.add_argument('--simulate', action='store_true', help='Run with simulated CAN data (for testing)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    
    # List messages and exit
    if args.list_messages:
        print(list_known_messages())
        return 0
    
    # Maintenance tracker
    if args.maintenance:
        tracker = MaintenanceTracker()
        tracker.print_status()
        return 0
    
    # Record service
    if args.record_service:
        tracker = MaintenanceTracker()
        tracker.record_service(args.record_service)
        tracker.print_status()
        return 0
    
    # DTC reading requires CAN bus
    if args.dtc or args.clear_dtc:
        if not setup_can_interface(args.interface, args.bitrate):
            return 1
        bus = create_can_bus(args.interface, args.bitrate)
        if not bus:
            return 1
        
        dtc_reader = DTCReader(bus)
        
        if args.clear_dtc:
            print("⚠️  CLEAR ALL DTCs — are you sure? (y/N)")
            if input().lower() == 'y':
                if dtc_reader.clear_dtcs():
                    print("✅ All DTCs cleared successfully")
                else:
                    print("❌ Failed to clear DTCs")
            else:
                print("Cancelled.")
        
        dtcs = dtc_reader.read_dtcs()
        if dtcs:
            print(f"\n{'='*60}")
            print(f"  V50 Diagnostic Trouble Codes — {len(dtcs)} found")
            print(f"{'='*60}")
            for dtc in dtcs:
                status_icon = {"stored": "🔵", "pending": "🟡", "permanent": "🔴"}.get(dtc["status"], "?")
                print(f"  {status_icon} {dtc['code']} [{dtc['status'].upper()}] — {dtc['description']}")
            print(f"{'='*60}\n")
        else:
            print("✅ No DTCs found — system clean!")
        
        bus.shutdown()
        return 0
    
    # Replay mode
    if args.replay:
        replay_file = Path(args.replay)
        if not replay_file.exists():
            print(f"Error: Replay file not found: {replay_file}")
            return 1
        
        state = V50State()
        recorder = SessionRecorder(LOG_DIR)
        
        print(f"Replaying: {replay_file}")
        stats = recorder.replay(replay_file, state, speed=10.0, callback=lambda s, r: None)
        print(f"Replay complete: {stats['messages']} messages, {stats['decoded']} decoded, {stats['unknown']} unknown")
        print(state.summary())
        return 0
    
    # Simulate mode (for testing without hardware)
    if args.simulate:
        state = V50State()
        monitor = LiveMonitor(state)
        
        print("Simulating V50 CAN data... (Ctrl+C to stop)")
        try:
            import random
            t = 0
            while True:
                # Simulate realistic V50 data
                rpm = int(800 + 4000 * (0.5 + 0.5 * abs((t * 0.1) % 2 - 1)))
                speed = int(80 * abs((t * 0.05) % 2 - 1))
                temp = int(85 + 10 * (0.5 + 0.5 * abs((t * 0.01) % 2)))
                fuel = 65
                load = int(rpm / 70)
                
                # Create simulated CAN frames
                rpm_data = int(rpm / 0.25).to_bytes(2, 'little') + b'\x00' * 6
                speed_data = int(speed / 0.01).to_bytes(2, 'little') + b'\x00' * 6
                temp_data = bytes([temp + 40]) + b'\x00' * 7
                fuel_data = bytes([int(fuel / 0.390625)]) + b'\x00' * 7
                load_data = bytes([int(load / 0.390625)]) + b'\x00' * 7
                gear_data = bytes([3]) + b'\x00' * 7  # D gear
                ext_temp_data = bytes([18 + 40]) + b'\x00' * 7  # 18°C outside
                int_temp_data = bytes([22 + 40]) + b'\x00' * 7  # 22°C inside
                odo_data = int(142500).to_bytes(4, 'little') + b'\x00' * 4
                
                monitor.update(0x0C0, rpm_data)
                monitor.update(0x0E0, speed_data)
                monitor.update(0x0C8, temp_data)
                monitor.update(0x0F0, fuel_data)
                monitor.update(0x0D8, load_data)
                monitor.update(0x1A0, gear_data)
                monitor.update(0x238, ext_temp_data)
                monitor.update(0x230, int_temp_data)
                monitor.update(0x328, odo_data)
                
                print(monitor.render())
                time.sleep(0.5)
                t += 1
        
        except KeyboardInterrupt:
            print("\nSimulation stopped.")
        return 0
    
    # Live monitor / log mode — requires CAN hardware
    if args.monitor or args.log or args.sniff:
        if not setup_can_interface(args.interface, args.bitrate):
            return 1
        bus = create_can_bus(args.interface, args.bitrate)
        if not bus:
            return 1
        
        state = V50State()
        monitor = LiveMonitor(state)
        sniffer = CANSniffer() if args.sniff else None
        logger_obj = CANLogger(LOG_DIR) if args.log else None
        
        print("V50 CAN Bus Monitor — Press Ctrl+C to stop")
        
        try:
            import can
            while True:
                msg = bus.recv(timeout=1.0)
                if msg:
                    can_id = msg.arbitration_id
                    data = msg.data
                    
                    monitor.update(can_id, data)
                    if sniffer:
                        sniffer.process(can_id, data)
                    if logger_obj:
                        logger_obj.log(CANLogEntry(
                            timestamp=time.time(),
                            can_id=can_id,
                            bus='HS',
                            dlc=len(data),
                            data_hex=data.hex(),
                            decoded=decode_message(can_id, data)
                        ))
                    
                    # Update console display at configured rate
                    if time.time() - monitor.last_display > CONSOLE_UPDATE_INTERVAL:
                        if args.monitor:
                            print(monitor.render())
                        monitor.last_display = time.time()
        
        except KeyboardInterrupt:
            print("\n\nStopping CAN monitor...")
        finally:
            if logger_obj:
                logger_obj.close()
            if sniffer:
                print(sniffer.report())
            bus.shutdown()
        
        return 0
    
    # Default: show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())