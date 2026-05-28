#!/usr/bin/env python3
"""
Volvo V50 2.4i — CAN-Bus Application Controller
=================================================
Central orchestrator that ties together all CAN-bus subsystems:
- CAN decoder (v50_can_decoder.py)
- DTC reader (v50_dtc_reader.py)
- Drive profile (v50_drive_profile.py)
- Power monitor (v50_power_monitor.py)
- BLE server (v50_ble_server.py)
- Dashboard (v50_dashboard.py)

Manages the CAN bus listener loop, dispatches messages to subsystems,
handles graceful startup/shutdown, and provides a status console.

Usage:
    # Full system (requires PiCAN2 hardware)
    python3 v50_app.py --full

    # CAN bus sniffer only
    python3 v50_app.py --sniff

    # Diagnostics (DTC read, live data)
    python3 v50_app.py --diagnostics

    # Data logging only
    python3 v50_app.py --log /path/to/session

Author: v50-developer agent
Date: 2026-05-28
"""

import argparse
import json
import logging
import os
import signal
import sys
import threading
import time
from pathlib import Path
from typing import Optional

# Add canbus dir to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from v50_can_decoder import (
    V50State, CANBus, MESSAGE_DEFINITIONS,
    decode_message, list_known_messages, get_gear_name
)

try:
    from v50_dtc_reader import V50DTCReader, V50MaintenanceTracker, V50DataLogger
    HAS_DTC = True
except ImportError:
    HAS_DTC = False

try:
    from v50_drive_profile import DriveProfileAnalyzer, FuelEconomyTracker
    HAS_DRIVE_PROFILE = True
except ImportError:
    HAS_DRIVE_PROFILE = False

try:
    from v50_power_monitor import PowerMonitor
    HAS_POWER_MONITOR = True
except ImportError:
    HAS_POWER_MONITOR = False

try:
    from v50_can_health import CANBusHealthMonitor
    HAS_CAN_HEALTH = True
except ImportError:
    HAS_CAN_HEALTH = False

try:
    from v50_ble_server import BLEDataServer
    HAS_BLE = True
except ImportError:
    HAS_BLE = False

try:
    import can
    HAS_PYTHON_CAN = True
except ImportError:
    HAS_PYTHON_CAN = False

logger = logging.getLogger('v50.app')


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_CAN_INTERFACE = 'can0'
DEFAULT_CAN_BITRATE = 500000  # High-speed CAN
DEFAULT_LOG_LEVEL = 'INFO'
DEFAULT_SAMPLE_RATE = 0.05  # 50ms = 20Hz


# =============================================================================
# CAN Bus Listener
# =============================================================================

class V50CANBusApp:
    """Central CAN-bus application controller.
    
    Manages:
    - CAN bus connection and message reception
    - State tracking (V50State)
    - Drive profile analysis
    - Maintenance tracking
    - Data logging (SQLite + CSV)
    - Power management (safe shutdown)
    - BLE smartphone data server
    
    This is the main entry point for the V50 CAN-bus system on the Pi.
    """
    
    def __init__(self, interface: str = DEFAULT_CAN_INTERFACE,
                 bitrate: int = DEFAULT_CAN_BITRATE,
                 log_dir: str = None,
                 sample_rate: float = DEFAULT_SAMPLE_RATE,
                 ble_enabled: bool = False,
                 dashboard_enabled: bool = False,
                 power_monitor_enabled: bool = True):
        """Initialize the V50 CAN bus application.
        
        Args:
            interface: CAN interface (default: can0)
            bitrate: CAN bitrate (default: 500000 for high-speed)
            log_dir: Directory for data logs (default: /var/log/v50can)
            sample_rate: Sample rate in seconds (default: 0.05 = 20Hz)
            ble_enabled: Enable BLE smartphone server
            dashboard_enabled: Enable PyQt5 dashboard
            power_monitor_enabled: Enable safe shutdown on ignition off
        """
        self.interface = interface
        self.bitrate = bitrate
        self.sample_rate = sample_rate
        
        # Core state
        self.state = V50State()
        self.bus: Optional[can.Bus] = None
        self.running = False
        
        # Subsystems
        self.drive_profile = DriveProfileAnalyzer() if HAS_DRIVE_PROFILE else None
        self.fuel_tracker = FuelEconomyTracker() if HAS_DRIVE_PROFILE else None
        self.maintenance = V50MaintenanceTracker() if HAS_DTC else None
        self.dtc_reader = V50DTCReader(interface=interface) if HAS_DTC else None
        self.data_logger = V50DataLogger(log_dir=log_dir) if HAS_DTC else None
        self.health_monitor: Optional[CANBusHealthMonitor] = None
        self.ble_server: Optional[BLEDataServer] = None
        self.power_monitor: Optional[PowerMonitor] = None
        
        self.ble_enabled = ble_enabled
        self.dashboard_enabled = dashboard_enabled
        self.power_monitor_enabled = power_monitor_enabled
        
        # Stats
        self._msg_count = 0
        self._unknown_msg_count = 0
        self._start_time = 0
        
        # Thread control
        self._threads = []
        self._stop_event = threading.Event()
    
    def setup(self) -> bool:
        """Initialize CAN bus and all subsystems.
        
        Returns:
            True if successful
        """
        if not HAS_PYTHON_CAN:
            logger.error("python-can not installed. Install with: pip install python-can")
            return False
        
        # Setup CAN bus
        try:
            self.bus = can.Bus(
                interface=self.interface,
                bustype='socketcan',
                bitrate=self.bitrate
            )
            logger.info(f"CAN bus connected: {self.interface} @ {self.bitrate}bps")
        except can.CanError as e:
            logger.error(f"Failed to connect to CAN bus: {e}")
            logger.info(f"Make sure {self.interface} is configured:")
            logger.info(f"  sudo ip link set {self.interface} type can bitrate {self.bitrate}")
            logger.info(f"  sudo ip link set {self.interface} up")
            return False
        
        # Setup data logger
        if self.data_logger:
            try:
                self.data_logger.start()
                logger.info("Data logger started")
            except Exception as e:
                logger.warning(f"Data logger failed: {e}")
        
        # Setup BLE server
        if self.ble_enabled and HAS_BLE:
            try:
                self.ble_server = BLEDataServer()
                ble_thread = threading.Thread(target=self.ble_server.start, daemon=True)
                ble_thread.start()
                self._threads.append(ble_thread)
                logger.info("BLE server started")
            except Exception as e:
                logger.warning(f"BLE server failed: {e}")
                self.ble_server = None
        
        # Setup power monitor
        if self.power_monitor_enabled and HAS_POWER_MONITOR:
            try:
                self.power_monitor = PowerMonitor(can_interface=self.interface)
                pm_thread = threading.Thread(target=self.power_monitor.monitor, daemon=True)
                pm_thread.start()
                self._threads.append(pm_thread)
                logger.info("Power monitor started")
            except Exception as e:
                logger.warning(f"Power monitor failed: {e}")
                self.power_monitor = None
        
        # Setup CAN health monitor
        if HAS_CAN_HEALTH:
            try:
                self.health_monitor = CANBusHealthMonitor(
                    hs_interface=self.interface,
                    ls_interface='can1'
                )
                health_report = self.health_monitor.start_self_test()
                logger.info(f"CAN health self-test: {health_report.overall_status.label}")
                if health_report.alerts:
                    for alert in health_report.alerts:
                        logger.warning(f"  CAN alert: {alert}")
            except Exception as e:
                logger.warning(f"CAN health monitor failed: {e}")
                self.health_monitor = None
        
        self._start_time = time.time()
        self.running = True
        return True
    
    def run(self):
        """Main CAN bus listener loop.
        
        Reads CAN messages, decodes them, updates state, and dispatches
        to all subsystems.
        """
        if not self.bus:
            logger.error("CAN bus not initialized — call setup() first")
            return
        
        logger.info("V50 CAN bus listener started — Ctrl+C to stop")
        
        # Register signal handlers for graceful shutdown
        original_sigint = signal.getsignal(signal.SIGINT)
        original_sigterm = signal.getsignal(signal.SIGTERM)
        
        def _shutdown_handler(signum, frame):
            logger.info(f"Received signal {signum} — shutting down...")
            self.stop()
            # Restore original handlers and re-raise
            signal.signal(signal.SIGINT, original_sigint)
            signal.signal(signal.SIGTERM, original_sigterm)
            raise KeyboardInterrupt()
        
        signal.signal(signal.SIGINT, _shutdown_handler)
        signal.signal(signal.SIGTERM, _shutdown_handler)
        
        try:
            while self.running and not self._stop_event.is_set():
                try:
                    msg = self.bus.recv(timeout=0.1)
                    if msg is None:
                        continue
                    
                    self._process_message(msg)
                    
                except can.CanError as e:
                    logger.warning(f"CAN error: {e}")
                    time.sleep(0.01)
                except Exception as e:
                    logger.error(f"Message processing error: {e}", exc_info=True)
                    time.sleep(0.01)
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
    
    def _process_message(self, msg: can.Message):
        """Process a single CAN message.
        
        Decodes the message, updates state, and dispatches to subsystems.
        """
        can_id = msg.arbitration_id
        data = msg.data
        timestamp = msg.timestamp
        is_error = msg.is_error_frame
        
        # Update health monitor
        if self.health_monitor:
            intf = 'can0' if self.interface == 'can0' else self.interface
            self.health_monitor.on_frame(intf, can_id, is_error, msg.dlc)
        
        self._msg_count += 1
        
        # Check if we know this message
        if can_id not in MESSAGE_DEFINITIONS:
            self._unknown_msg_count += 1
            # Log unknown messages at debug level (can be noisy)
            if self._unknown_msg_count <= 10 or self._unknown_msg_count % 1000 == 0:
                logger.debug(f"Unknown CAN ID: 0x{can_id:03X} data={data.hex()}")
            return
        
        # Decode and update state
        self.state.update(can_id, data, timestamp)
        
        # Update drive profile
        if self.drive_profile:
            self.drive_profile.update(self.state)
        
        # Update fuel tracker
        if self.fuel_tracker and self.state.rpm > 0:
            self.fuel_tracker.update(self.state.rpm, self.state.maf_g_per_s, self.state.speed_kmh)
        
        # Log data
        if self.data_logger and self._msg_count % max(1, int(self.sample_rate / 0.05)) == 0:
            self.data_logger.log_state(self.state)
        
        # Send to BLE clients
        if self.ble_server:
            try:
                self.ble_server.broadcast_state(self.state)
            except Exception:
                pass
    
    def stop(self):
        """Stop all subsystems and disconnect from CAN bus."""
        logger.info("Shutting down V50 CAN bus application...")
        self.running = False
        self._stop_event.set()
        
        # Stop data logger
        if self.data_logger:
            try:
                self.data_logger.stop()
            except Exception as e:
                logger.warning(f"Data logger stop error: {e}")
        
        # Stop BLE server
        if self.ble_server:
            try:
                self.ble_server.stop()
            except Exception as e:
                logger.warning(f"BLE server stop error: {e}")
        
        # Disconnect CAN bus
        if self.bus:
            try:
                self.bus.shutdown()
            except Exception as e:
                logger.warning(f"CAN bus shutdown error: {e}")
        
        # Update maintenance with current odometer
        if self.maintenance and self.state.odometer_km > 0:
            self.maintenance.update_odometer(self.state.odometer_km)
        
        uptime = time.time() - self._start_time if self._start_time else 0
        logger.info(f"Shutdown complete — {self._msg_count} messages processed in {uptime:.0f}s")
        logger.info(f"  Unknown messages: {self._unknown_msg_count}")
    
    def status(self) -> str:
        """Return a formatted status string."""
        uptime = time.time() - self._start_time if self._start_time else 0
        lines = [
            "=" * 60,
            "  V50 CAN-Bus Application Status",
            "=" * 60,
            f"  Interface:      {self.interface} @ {self.bitrate}bps",
            f"  Uptime:         {uptime:.0f}s",
            f"  Messages:       {self._msg_count}",
            f"  Unknown msgs:    {self._unknown_msg_count}",
            f"  Known IDs:      {len(MESSAGE_DEFINITIONS)}",
            f"  Drive Profile:  {'✓' if self.drive_profile else '✗'}",
            f"  Fuel Tracker:   {'✓' if self.fuel_tracker else '✗'}",
            f"  DTC Reader:     {'✓' if self.dtc_reader else '✗'}",
            f"  Data Logger:    {'✓' if self.data_logger else '✗'}",
            f"  BLE Server:     {'✓' if self.ble_server else '✗'}",
            f"  Power Monitor:  {'✓' if self.power_monitor else '✗'}",
            f"  Health Monitor: {'✓' if self.health_monitor else '✗'}",
            "=" * 60,
            "",
            self.state.summary(),
        ]
        
        if self.drive_profile:
            lines.append(str(self.drive_profile))
        
        if self.fuel_tracker:
            lines.append(str(self.fuel_tracker))
        
        if self.health_monitor:
            lines.append("")
            lines.append(self.health_monitor.format_report())
        
        return "\n".join(lines)


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="V50 CAN-Bus Application Controller",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  --full          Run full system (CAN listener + all subsystems)
  --sniff         CAN bus sniffer mode (print decoded messages)
  --diagnostics   Read DTCs and live data
  --status        Print current system status
  --list          List all known CAN messages
  --log           Data logging only (no dashboard)
        """
    )
    
    parser.add_argument("--full", action="store_true", help="Run full CAN bus system")
    parser.add_argument("--sniff", action="store_true", help="CAN bus sniffer mode")
    parser.add_argument("--diagnostics", action="store_true", help="Read DTCs and live data")
    parser.add_argument("--status", action="store_true", help="Print system status")
    parser.add_argument("--list", action="store_true", help="List all known CAN messages")
    parser.add_argument("--log", action="store_true", help="Data logging only")
    parser.add_argument("--interface", type=str, default=DEFAULT_CAN_INTERFACE, help="CAN interface")
    parser.add_argument("--bitrate", type=int, default=DEFAULT_CAN_BITRATE, help="CAN bitrate")
    parser.add_argument("--log-dir", type=str, default="/var/log/v50can", help="Log directory")
    parser.add_argument("--ble", action="store_true", help="Enable BLE server")
    parser.add_argument("--no-power-monitor", action="store_true", help="Disable power monitor")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # List known messages
    if args.list:
        print(list_known_messages())
        print(f"\nTotal: {len(MESSAGE_DEFINITIONS)} known CAN messages")
        return
    
    # Diagnostics (DTC reader)
    if args.diagnostics:
        if not HAS_DTC:
            print("ERROR: DTC reader module not available")
            return
        
        reader = V50DTCReader(interface=args.interface)
        if reader.connect():
            try:
                # Read VIN
                vin = reader.read_vin()
                print(f"VIN: {vin or 'NOT AVAILABLE'}")
                
                # Read stored and pending DTCs
                all_dtcs = reader.read_all_dtcs()
                print(f"\nStored DTCs ({len(all_dtcs['stored'])} found):")
                print(V50DTCReader.format_dtcs(all_dtcs['stored']))
                print(f"\nPending DTCs ({len(all_dtcs['pending'])} found):")
                print(V50DTCReader.format_dtcs(all_dtcs['pending']))
                
                # Read live data
                print("\nLive Data:")
                live = reader.read_live_data()
                for name, value in live.items():
                    print(f"  {name}: {value:.1f}")
                
            finally:
                reader.disconnect()
        else:
            print(f"Cannot connect to {args.interface}")
        return
    
    # Status mode — show maintenance status
    if args.status:
        if HAS_DTC:
            tracker = V50MaintenanceTracker()
            print(tracker.format_status())
        else:
            print("Maintenance tracker not available")
        return
    
    # Sniffer mode
    if args.sniff:
        from v50_can_sniffer import main as sniffer_main
        sys.argv = ['v50_can_sniffer.py', '--monitor', '--interface', args.interface]
        sniffer_main()
        return
    
    # Full mode or log mode
    if args.full or args.log:
        app = V50CANBusApp(
            interface=args.interface,
            bitrate=args.bitrate,
            log_dir=args.log_dir,
            ble_enabled=args.ble,
            power_monitor_enabled=not args.no_power_monitor,
        )
        
        if app.setup():
            try:
                app.run()
            finally:
                app.stop()
        else:
            print("Failed to initialize — check CAN interface and PiCAN2 setup")
            return 1
    
    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()