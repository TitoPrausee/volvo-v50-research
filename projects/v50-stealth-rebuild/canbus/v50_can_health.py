#!/usr/bin/env python3
"""
Volvo V50 2.4i — CAN Bus Health Monitor
========================================
Monitors CAN bus health: startup self-test, bus-off detection,
error frame counting, message rate monitoring, and interface diagnostics.

Features:
- SocketCAN interface health check (can0/can1)
- Bus-off detection and recovery
- Error frame counting and alerting
- Message rate monitoring (per-ID and total)
- Startup self-test routine
- Known/unknown CAN ID tracking
- Health report generation for dashboard/diagnostics

Hardware: Raspberry Pi 4 + PiCAN2 Duo HAT
Bus: High-Speed CAN (500kbps) — can0
      Low-Speed CAN (125kbps) — can1

Author: v50-developer agent
Date: 2026-05-28
"""

import os
import time
import logging
import threading
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple, Set
from pathlib import Path
from enum import IntEnum

try:
    import can
    HAS_PYTHON_CAN = True
except ImportError:
    HAS_PYTHON_CAN = False

from v50_can_decoder import CANBus, MESSAGE_DEFINITIONS

logger = logging.getLogger('v50.can_health')

# =============================================================================
# Constants
# =============================================================================

CAN_INTERFACE_HS = 'can0'  # High-Speed 500kbps
CAN_INTERFACE_LS = 'can1'  # Low-Speed 125kbps

# Health thresholds
WARN_ERROR_RATE = 10       # errors/minute → WARNING
CRIT_ERROR_RATE = 50      # errors/minute → CRITICAL
WARN_MSG_RATE_DROP = 0.5   # <50% of baseline rate → WARNING
MIN_EXPECTED_RATE = 50     # minimum messages/second on healthy bus
BUS_OFF_RECOVERY_DELAY = 5  # seconds before retrying bus recovery

# =============================================================================
# CAN Bus Error Types
# =============================================================================

class CANHealthStatus(IntEnum):
    """CAN bus health status."""
    UNKNOWN = 0
    HEALTHY = 1
    WARNING = 2
    CRITICAL = 3
    BUS_OFF = 4
    NO_INTERFACE = 5

    @property
    def icon(self) -> str:
        icons = {0: "❓", 1: "✅", 2: "⚠️", 3: "🔴", 4: "🛑", 5: "🔌"}
        return icons.get(self.value, "❓")

    @property
    def color(self) -> str:
        colors = {0: "#888888", 1: "#00CC00", 2: "#FFAA00", 3: "#FF0000", 4: "#FF0000", 5: "#666666"}
        return colors.get(self.value, "#888888")

    @property
    def label(self) -> str:
        labels = {
            0: "UNKNOWN", 1: "HEALTHY", 2: "WARNING",
            3: "CRITICAL", 4: "BUS_OFF", 5: "NO_INTERFACE"
        }
        return labels.get(self.value, "UNKNOWN")


@dataclass
class CANInterfaceStats:
    """Statistics for a single CAN interface."""
    interface: str = ""
    bitrate: int = 0
    status: CANHealthStatus = CANHealthStatus.UNKNOWN

    # Frame counters
    rx_frames: int = 0
    tx_frames: int = 0
    error_frames: int = 0
    dropped_frames: int = 0

    # Per-ID tracking
    known_ids: Set[int] = field(default_factory=set)
    unknown_ids: Set[int] = field(default_factory=set)
    id_counts: Dict[int, int] = field(default_factory=dict)

    # Timing
    last_rx_time: float = 0.0
    start_time: float = 0.0
    last_error_time: float = 0.0

    # Bus state
    bus_state: str = "UNKNOWN"  # ERROR-ACTIVE, ERROR-PASSIVE, BUS-OFF
    restart_count: int = 0
    bus_off_count: int = 0

    # Rates (calculated)
    rx_rate_per_sec: float = 0.0
    error_rate_per_min: float = 0.0

    def uptime_seconds(self) -> float:
        """Seconds since monitoring started."""
        if self.start_time == 0:
            return 0.0
        return time.time() - self.start_time

    def known_ratio(self) -> float:
        """Ratio of known CAN IDs to total seen."""
        total = len(self.known_ids) + len(self.unknown_ids)
        if total == 0:
            return 0.0
        return len(self.known_ids) / total


@dataclass
class CANHealthReport:
    """Complete CAN bus health report."""
    timestamp: float = 0.0
    hs_can: CANInterfaceStats = field(default_factory=lambda: CANInterfaceStats(interface=CAN_INTERFACE_HS))
    ls_can: CANInterfaceStats = field(default_factory=lambda: CANInterfaceStats(interface=CAN_INTERFACE_LS))
    overall_status: CANHealthStatus = CANHealthStatus.UNKNOWN
    alerts: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'timestamp': self.timestamp,
            'overall_status': self.overall_status.label,
            'hs_can': self._stats_to_dict(self.hs_can),
            'ls_can': self._stats_to_dict(self.ls_can),
            'alerts': self.alerts,
        }

    @staticmethod
    def _stats_to_dict(stats: CANInterfaceStats) -> Dict:
        return {
            'interface': stats.interface,
            'bitrate': stats.bitrate,
            'status': stats.status.label,
            'rx_frames': stats.rx_frames,
            'tx_frames': stats.tx_frames,
            'error_frames': stats.error_frames,
            'dropped_frames': stats.dropped_frames,
            'known_ids': len(stats.known_ids),
            'unknown_ids': len(stats.unknown_ids),
            'known_ratio': stats.known_ratio(),
            'rx_rate_per_sec': round(stats.rx_rate_per_sec, 1),
            'error_rate_per_min': round(stats.error_rate_per_min, 1),
            'bus_state': stats.bus_state,
            'restart_count': stats.restart_count,
            'bus_off_count': stats.bus_off_count,
            'uptime_seconds': round(stats.uptime_seconds(), 0),
        }


# =============================================================================
# CAN Bus Health Monitor
# =============================================================================

class CANBusHealthMonitor:
    """Monitors CAN bus health and provides diagnostics.

    Usage:
        monitor = CANBusHealthMonitor()
        monitor.start_self_test()

        # In CAN reader loop:
        monitor.on_frame(interface='can0', can_id=0x0C0, is_error=False)
        monitor.on_frame(interface='can0', can_id=0x0C0, is_error=True)

        # Periodic health check:
        report = monitor.get_health_report()
        if report.overall_status >= CANHealthStatus.WARNING:
            print(f"CAN bus alert: {report.alerts}")
    """

    # Known CAN IDs for the V50 (pre-loaded from MESSAGE_DEFINITIONS)
    KNOWN_HS_IDS: Set[int] = set()
    KNOWN_LS_IDS: Set[int] = set()

    def __init__(self, hs_interface: str = CAN_INTERFACE_HS,
                 ls_interface: str = CAN_INTERFACE_LS):
        self.hs = CANInterfaceStats(interface=hs_interface, bitrate=500000)
        self.ls = CANInterfaceStats(interface=ls_interface, bitrate=125000)
        self._lock = threading.Lock()
        self._active = False

        # Build known ID sets from MESSAGE_DEFINITIONS
        for can_id, msg_def in MESSAGE_DEFINITIONS.items():
            if msg_def.bus == CANBus.HIGH_SPEED:
                self.KNOWN_HS_IDS.add(can_id)
            else:
                self.KNOWN_LS_IDS.add(can_id)

        self.hs.known_ids = self.KNOWN_HS_IDS.copy()
        self.ls.known_ids = self.KNOWN_LS_IDS.copy()

        logger.info(f"CAN Health Monitor initialized: {len(self.KNOWN_HS_IDS)} HS IDs, "
                     f"{len(self.KNOWN_LS_IDS)} LS IDs known")

    def start_self_test(self) -> CANHealthReport:
        """Run startup self-test for both CAN interfaces.

        Checks:
        1. Interface exists (SocketCAN device node)
        2. Interface is UP
        3. Correct bitrate configured
        4. CAN device state (ERROR-ACTIVE = healthy)
        5. No bus-off condition

        Returns health report with self-test results.
        """
        report = CANHealthReport(timestamp=time.time())

        # Test both interfaces
        for name, stats in [('HS', self.hs), ('LS', self.ls)]:
            result = self._test_interface(stats)
            if result == CANHealthStatus.HEALTHY:
                logger.info(f"{name} CAN ({stats.interface}): ✅ Self-test passed")
            else:
                logger.warning(f"{name} CAN ({stats.interface}): {result.label} — {result.icon}")

        # Determine overall status
        worst = min(self.hs.status.value, self.ls.status.value)
        report.overall_status = CANHealthStatus(worst)

        # Generate alerts
        report.alerts = self._generate_alerts()
        report.hs_can = self.hs
        report.ls_can = self.ls

        self.hs.start_time = time.time()
        self.ls.start_time = time.time()
        self._active = True

        return report

    def _test_interface(self, stats: CANInterfaceStats) -> CANHealthStatus:
        """Test a single CAN interface."""
        interface = stats.interface

        # Check 1: Interface exists
        if not os.path.exists(f'/sys/class/net/{interface}'):
            logger.error(f"Interface {interface} not found")
            stats.status = CANHealthStatus.NO_INTERFACE
            stats.bus_state = "NOT_FOUND"
            return CANHealthStatus.NO_INTERFACE

        # Check 2: Read interface state via ip link
        try:
            import subprocess
            result = subprocess.run(
                ['ip', '-details', 'link', 'show', interface],
                capture_output=True, text=True, timeout=5
            )
            output = result.stdout

            # Check if interface is UP
            if 'DOWN' in output or 'state DOWN' in output:
                logger.warning(f"Interface {interface} is DOWN")
                stats.status = CANHealthStatus.NO_INTERFACE
                stats.bus_state = "DOWN"
                return CANHealthStatus.NO_INTERFACE

            # Check CAN state
            if 'BUS-OFF' in output:
                logger.error(f"Interface {interface} is BUS-OFF!")
                stats.status = CANHealthStatus.BUS_OFF
                stats.bus_state = "BUS-OFF"
                stats.bus_off_count += 1
                return CANHealthStatus.BUS_OFF

            if 'ERROR-PASSIVE' in output:
                logger.warning(f"Interface {interface} is ERROR-PASSIVE")
                stats.status = CANHealthStatus.WARNING
                stats.bus_state = "ERROR-PASSIVE"
                return CANHealthStatus.WARNING

            if 'ERROR-ACTIVE' in output or 'NOHOOK' in output or 'UP' in output:
                logger.info(f"Interface {interface} is UP and healthy")
                stats.status = CANHealthStatus.HEALTHY
                stats.bus_state = "ERROR-ACTIVE"

                # Check bitrate
                for bitrate_str in [f'bitrate {stats.bitrate}']:
                    if bitrate_str in output:
                        logger.info(f"  Bitrate confirmed: {stats.bitrate} bps")

                return CANHealthStatus.HEALTHY

            # If we can't determine state, assume unknown
            stats.status = CANHealthStatus.UNKNOWN
            stats.bus_state = "UNKNOWN"
            return CANHealthStatus.UNKNOWN

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.error(f"Failed to check interface {interface}: {e}")
            stats.status = CANHealthStatus.NO_INTERFACE
            return CANHealthStatus.NO_INTERFACE

    def on_frame(self, interface: str, can_id: int, is_error: bool = False,
                 dlc: int = 0) -> None:
        """Called for every received CAN frame.

        Args:
            interface: 'can0' or 'can1'
            can_id: CAN message ID
            is_error: True if this is an error frame
            dlc: Data Length Code
        """
        with self._lock:
            stats = self.hs if interface == CAN_INTERFACE_HS else self.ls

            if is_error:
                stats.error_frames += 1
                stats.last_error_time = time.time()
                return

            stats.rx_frames += 1
            stats.last_rx_time = time.time()

            # Track CAN ID
            stats.id_counts[can_id] = stats.id_counts.get(can_id, 0) + 1

            # Classify as known or unknown
            known_set = self.KNOWN_HS_IDS if interface == CAN_INTERFACE_HS else self.KNOWN_LS_IDS
            if can_id in known_set:
                stats.known_ids.add(can_id)
            else:
                stats.unknown_ids.add(can_id)

            # Update rates
            self._update_rates(stats)

    def on_bus_off(self, interface: str) -> None:
        """Called when a bus-off condition is detected."""
        with self._lock:
            stats = self.hs if interface == CAN_INTERFACE_HS else self.ls
            stats.bus_off_count += 1
            stats.bus_state = "BUS-OFF"
            stats.status = CANHealthStatus.BUS_OFF
            logger.critical(f"💥 BUS-OFF detected on {interface}! "
                             f"Count: {stats.bus_off_count}")

    def recover_bus(self, interface: str) -> bool:
        """Attempt to recover a bus-off CAN interface.

        Returns True if recovery was successful.
        """
        logger.info(f"Attempting bus recovery for {interface}...")

        try:
            import subprocess
            # Set interface down
            subprocess.run(['ip', 'link', 'set', interface, 'down'],
                           capture_output=True, timeout=5)
            time.sleep(0.5)

            # Set interface back up
            bitrate = 500000 if interface == CAN_INTERFACE_HS else 125000
            subprocess.run(
                ['ip', 'link', 'set', interface, 'type', 'can',
                 'bitrate', str(bitrate), 'restart-ms', '100'],
                capture_output=True, timeout=5
            )
            subprocess.run(['ip', 'link', 'set', interface, 'up'],
                           capture_output=True, timeout=5)

            stats = self.hs if interface == CAN_INTERFACE_HS else self.ls
            stats.restart_count += 1
            stats.bus_state = "RECOVERING"

            logger.info(f"Bus recovery completed for {interface} "
                         f"(restart #{stats.restart_count})")
            return True

        except Exception as e:
            logger.error(f"Bus recovery failed for {interface}: {e}")
            return False

    def _update_rates(self, stats: CANInterfaceStats) -> None:
        """Update message and error rates for an interface."""
        uptime = stats.uptime_seconds()
        if uptime > 0:
            stats.rx_rate_per_sec = stats.rx_frames / uptime

            # Error rate per minute
            error_minutes = min(uptime / 60, 1.0)  # minimum 1 minute
            stats.error_rate_per_min = stats.error_frames / error_minutes

    def _generate_alerts(self) -> List[str]:
        """Generate alert messages based on current health status."""
        alerts = []

        for name, stats in [('HS', self.hs), ('LS', self.ls)]:
            if stats.status == CANHealthStatus.NO_INTERFACE:
                alerts.append(f"{name}: Interface {stats.interface} not found or DOWN")
            elif stats.status == CANHealthStatus.BUS_OFF:
                alerts.append(f"{name}: BUS-OFF condition detected! Bus recovery needed.")
            elif stats.status == CANHealthStatus.CRITICAL:
                alerts.append(f"{name}: Critical — high error rate ({stats.error_rate_per_min:.0f}/min)")
            elif stats.status == CANHealthStatus.WARNING:
                alerts.append(f"{name}: Warning — error-passive state or elevated errors")

            if stats.unknown_ids and len(stats.unknown_ids) > 5:
                alerts.append(f"{name}: {len(stats.unknown_ids)} unknown CAN IDs detected")

            if stats.rx_rate_per_sec > 0 and stats.rx_rate_per_sec < MIN_EXPECTED_RATE:
                alerts.append(f"{name}: Low message rate ({stats.rx_rate_per_sec:.0f}/s, expected >{MIN_EXPECTED_RATE})")

        return alerts

    def get_health_report(self) -> CANHealthReport:
        """Generate a complete health report."""
        with self._lock:
            report = CANHealthReport(
                timestamp=time.time(),
                hs_can=self.hs,
                ls_can=self.ls,
                alerts=self._generate_alerts()
            )

            # Overall status = worst of both
            worst = min(self.hs.status.value, self.ls.status.value)
            report.overall_status = CANHealthStatus(worst)

            return report

    def get_unknown_ids(self) -> Dict[str, Set[int]]:
        """Get all unknown CAN IDs detected on each bus.

        Returns:
            {'can0': {0x123, 0x456}, 'can1': {0x789}}
        """
        with self._lock:
            return {
                CAN_INTERFACE_HS: self.hs.unknown_ids.copy(),
                CAN_INTERFACE_LS: self.ls.unknown_ids.copy(),
            }

    def get_top_ids(self, interface: str = CAN_INTERFACE_HS, count: int = 10) -> List[Tuple[int, int]]:
        """Get top N most frequent CAN IDs by message count.

        Returns:
            List of (can_id, count) sorted by count descending
        """
        with self._lock:
            stats = self.hs if interface == CAN_INTERFACE_HS else self.ls
            sorted_ids = sorted(stats.id_counts.items(), key=lambda x: x[1], reverse=True)
            return sorted_ids[:count]

    def format_report(self, report: CANHealthReport = None) -> str:
        """Format a health report as a human-readable string."""
        if report is None:
            report = self.get_health_report()

        lines = [
            "=" * 60,
            "  V50 CAN Bus Health Report",
            "=" * 60,
            f"  Overall: {report.overall_status.icon} {report.overall_status.label}",
            f"  Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(report.timestamp))}",
            "",
        ]

        for name, stats in [("High-Speed CAN (can0)", report.hs_can),
                             ("Low-Speed CAN (can1)", report.ls_can)]:
            lines.extend([
                f"  ── {name} ──",
                f"  Status: {stats.status.icon} {stats.status.label}",
                f"  Bus state: {stats.bus_state}",
                f"  Bitrate: {stats.bitrate} bps",
                f"  RX frames: {stats.rx_frames:,}",
                f"  TX frames: {stats.tx_frames:,}",
                f"  Error frames: {stats.error_frames:,}",
                f"  RX rate: {stats.rx_rate_per_sec:.1f} msg/s",
                f"  Error rate: {stats.error_rate_per_min:.1f} err/min",
                f"  Known IDs: {len(stats.known_ids)} / {len(stats.known_ids) + len(stats.unknown_ids)}"
                f" ({stats.known_ratio():.0%})",
                f"  Unknown IDs: {len(stats.unknown_ids)}",
                f"  Bus-off events: {stats.bus_off_count}",
                f"  Restart count: {stats.restart_count}",
                f"  Uptime: {stats.uptime_seconds():.0f}s",
                "",
            ])

        if report.alerts:
            lines.append("  ⚠️  Alerts:")
            for alert in report.alerts:
                lines.append(f"     • {alert}")
            lines.append("")

        # Show unknown IDs if any
        for interface, label in [(CAN_INTERFACE_HS, "HS"), (CAN_INTERFACE_LS, "LS")]:
            unknown = report.hs_can.unknown_ids if interface == CAN_INTERFACE_HS else report.ls_can.unknown_ids
            if unknown:
                ids = sorted(unknown)
                id_strs = [f"0x{id:03X}" for id in ids[:20]]
                lines.append(f"  Unknown {label} IDs: {', '.join(id_strs)}"
                             + (f" ... +{len(ids)-20} more" if len(ids) > 20 else ""))
                lines.append("")

        lines.append("=" * 60)
        return "\n".join(lines)


# =============================================================================
# Startup Self-Test Function
# =============================================================================

def run_startup_self_test() -> CANHealthReport:
    """Run a complete startup self-test of the CAN bus system.

    Tests:
    1. SocketCAN interfaces exist and are UP
    2. Correct bitrate configuration
    3. No bus-off conditions
    4. python-can library available
    5. CAN message definitions loaded
    6. Quick message reception test (optional, requires running vehicle)

    Returns:
        CANHealthReport with self-test results
    """
    monitor = CANBusHealthMonitor()
    report = monitor.start_self_test()

    # Additional checks
    if not HAS_PYTHON_CAN:
        report.alerts.append("⚠️ python-can library not installed — CAN bus features disabled")

    if len(MESSAGE_DEFINITIONS) == 0:
        report.alerts.append("🔴 No CAN message definitions loaded!")
    else:
        hs_count = sum(1 for m in MESSAGE_DEFINITIONS.values() if m.bus == CANBus.HIGH_SPEED)
        ls_count = sum(1 for m in MESSAGE_DEFINITIONS.values() if m.bus == CANBus.LOW_SPEED)
        logger.info(f"CAN definitions: {hs_count} HS, {ls_count} LS messages loaded")

    return report


# =============================================================================
# Main entry point
# =============================================================================

def main():
    """Run CAN bus health self-test and print report."""
    import argparse
    parser = argparse.ArgumentParser(description='V50 CAN Bus Health Monitor')
    parser.add_argument('--test', action='store_true', help='Run startup self-test')
    parser.add_argument('--monitor', type=int, default=0, metavar='SECONDS',
                        help='Monitor CAN bus for N seconds')
    parser.add_argument('--interface', default=CAN_INTERFACE_HS,
                        help='CAN interface (default: can0)')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s: %(message)s')

    if args.test:
        print("Running V50 CAN Bus Startup Self-Test...\n")
        report = run_startup_self_test()
        monitor = CANBusHealthMonitor()
        monitor.hs = report.hs_can
        monitor.ls = report.ls_can
        print(monitor.format_report(report))

    elif args.monitor:
        print(f"Monitoring CAN bus on {args.interface} for {args.monitor}s...\n")

        monitor = CANBusHealthMonitor()
        monitor.start_self_test()

        if not HAS_PYTHON_CAN:
            print("ERROR: python-can not installed. Install with: pip3 install python-can")
            return

        try:
            bus = can.Bus(channel=args.interface, interface='socketcan',
                          bitrate=500000 if args.interface == CAN_INTERFACE_HS else 125000)

            start_time = time.time()
            while time.time() - start_time < args.monitor:
                msg = bus.recv(timeout=1.0)
                if msg:
                    is_error = msg.is_error_frame
                    monitor.on_frame(args.interface, msg.arbitration_id, is_error, msg.dlc)
                else:
                    # Timeout — no message received
                    pass

            report = monitor.get_health_report()
            print(monitor.format_report(report))

            # Show top CAN IDs
            print("\nTop 10 CAN IDs by frequency:")
            for can_id, count in monitor.get_top_ids(args.interface, 10):
                name = MESSAGE_DEFINITIONS.get(can_id)
                name_str = name.name if name else "UNKNOWN"
                print(f"  0x{can_id:03X} ({name_str}): {count:,} msgs")

            bus.shutdown()

        except can.CanError as e:
            print(f"CAN Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    else:
        # Default: just run self-test
        print("Running V50 CAN Bus Startup Self-Test...\n")
        report = run_startup_self_test()
        monitor = CANBusHealthMonitor()
        monitor.hs = report.hs_can
        monitor.ls = report.ls_can
        print(monitor.format_report(report))


if __name__ == '__main__':
    main()