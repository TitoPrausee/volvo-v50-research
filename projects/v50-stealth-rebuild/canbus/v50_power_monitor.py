#!/usr/bin/env python3
"""
Volvo V50 2.4i — Raspberry Pi Power Monitor & Safe Shutdown
============================================================
Ensures the Raspberry Pi shuts down safely when the car's ignition is turned off.

Two detection methods:
1. CAN Bus activity monitor (software) — watches for CAN bus silence
2. GPIO voltage monitor (hardware) — watches ignition voltage via voltage divider

CRITICAL: Without this, the Pi will corrupt its SD card when power is cut!

Installation:
    # Run as systemd service for auto-start on boot:
    sudo cp v50_power_monitor.service /etc/systemd/system/
    sudo systemctl enable v50_power_monitor
    sudo systemctl start v50_power_monitor

Author: v50-developer agent
Date: 2026-05-28
"""

import argparse
import logging
import subprocess
import time
import signal
import os
from pathlib import Path
from typing import Optional

logger = logging.getLogger('v50.power_monitor')


# =============================================================================
# Configuration
# =============================================================================

# CAN bus activity detection (software method)
CAN_INTERFACE = 'can0'
CAN_IDLE_TIMEOUT = 300        # 5 minutes of no CAN activity = ignition off
CAN_CHECK_INTERVAL = 10       # Check every 10 seconds
CAN_RX_PACKETS_MIN = 5       # Minimum RX packets to consider "active"

# GPIO ignition detection (hardware method)
# Connect ignition+ (Klemme 15) through voltage divider to GPIO:
#   12V ── R1(33kΩ) ──┬── R2(10kΩ) ── GND
#                      │
#                    GPIO17 (Pin 11)
# When ignition ON: GPIO reads HIGH (~3.1V)
# When ignition OFF: GPIO reads LOW (~0V)
GPIO_IGNITION_PIN = 17
GPIO_DEBOUNCE_TIME = 2.0      # Seconds to confirm ignition state change
SHUTDOWN_DELAY = 30            # Seconds between detection and shutdown

# Pre-shutdown actions
PRE_SHUTDOWN_SCRIPT = None     # Optional: path to script before shutdown
LOG_FILE = Path('/opt/data/home/vehicle-database/projects/v50-stealth-rebuild/logs/power_monitor.log')


# =============================================================================
# CAN Bus Activity Monitor (Software Method)
# =============================================================================

class CANActivityMonitor:
    """Monitor CAN bus activity to detect ignition on/off.
    
    When the V50 ignition is turned off, the CAN bus goes silent.
    When ignition is on, there are continuous CAN messages (100+ per second).
    
    This method requires NO additional hardware — just the PiCAN2 HAT.
    """
    
    def __init__(self, interface: str = CAN_INTERFACE,
                 idle_timeout: int = CAN_IDLE_TIMEOUT,
                 check_interval: int = CAN_CHECK_INTERVAL):
        self.interface = interface
        self.idle_timeout = idle_timeout
        self.check_interval = check_interval
        self.last_rx_packets = 0
        self.last_activity_time = time.time()
        self.ignition_on = True  # Assume on at start
        self.running = False
    
    def _get_rx_packets(self) -> int:
        """Read RX packet count from CAN interface statistics."""
        try:
            result = subprocess.run(
                ['ip', '-s', 'link', 'show', self.interface],
                capture_output=True, text=True, timeout=5
            )
            # Parse output: "RX: bytes  packets  errors  dropped overrun mcast"
            lines = result.stdout.split('\n')
            for i, line in enumerate(lines):
                if 'RX:' in line and 'bytes' not in line:
                    # Next line has the actual numbers
                    if i + 1 < len(lines):
                        parts = lines[i + 1].split()
                        if len(parts) >= 2:
                            return int(parts[1])
            return 0
        except Exception as e:
            logger.warning(f"Failed to read CAN stats: {e}")
            return 0
    
    def _get_bus_state(self) -> str:
        """Get CAN interface state (UP/DOWN/ERROR)."""
        try:
            result = subprocess.run(
                ['ip', 'link', 'show', self.interface],
                capture_output=True, text=True, timeout=5
            )
            if 'UP' in result.stdout:
                return 'UP'
            elif 'DOWN' in result.stdout:
                return 'DOWN'
            return 'UNKNOWN'
        except:
            return 'ERROR'
    
    def check_activity(self) -> bool:
        """Check if CAN bus is active (ignition likely on).
        
        Returns True if ignition appears to be on.
        """
        current_rx = self._get_rx_packets()
        delta = current_rx - self.last_rx_packets
        self.last_rx_packets = current_rx
        
        if delta > CAN_RX_PACKETS_MIN:
            # CAN bus is active — ignition is on
            self.last_activity_time = time.time()
            if not self.ignition_on:
                logger.info(f"CAN bus activity detected — ignition ON (delta={delta} packets)")
                self.ignition_on = True
        else:
            # No CAN activity
            idle_seconds = time.time() - self.last_activity_time
            if self.ignition_on and idle_seconds > self.idle_timeout:
                logger.info(f"CAN bus idle for {idle_seconds:.0f}s — ignition likely OFF")
                self.ignition_on = False
        
        return self.ignition_on
    
    def run(self, on_shutdown=None):
        """Run the activity monitor loop.
        
        Args:
            on_shutdown: Called when shutdown is detected. If it returns
                        True, proceed with shutdown. If False, cancel.
        """
        self.running = True
        logger.info(f"CAN activity monitor started (interface={self.interface}, "
                    f"timeout={self.idle_timeout}s, interval={self.check_interval}s)")
        
        while self.running:
            try:
                ignition_on = self.check_activity()
                
                if not ignition_on:
                    logger.info("Ignition OFF detected — initiating shutdown sequence")
                    if on_shutdown is None or on_shutdown():
                        self._do_shutdown()
                        break
                
                time.sleep(self.check_interval)
            except KeyboardInterrupt:
                logger.info("Monitor interrupted")
                break
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                time.sleep(30)
        
        self.running = False
    
    def _do_shutdown(self):
        """Execute the shutdown sequence."""
        logger.info("=== SHUTDOWN SEQUENCE ===")
        
        # Run pre-shutdown script
        if PRE_SHUTDOWN_SCRIPT and Path(PRE_SHUTDOWN_SCRIPT).exists():
            logger.info(f"Running pre-shutdown script: {PRE_SHUTDOWN_SCRIPT}")
            try:
                subprocess.run(['python3', PRE_SHUTDOWN_SCRIPT], timeout=30)
            except Exception as e:
                logger.error(f"Pre-shutdown script failed: {e}")
        
        # Delay for final writes
        logger.info(f"Waiting {SHUTDOWN_DELAY}s before shutdown...")
        time.sleep(SHUTDOWN_DELAY)
        
        # Shutdown
        logger.info("Shutting down NOW")
        try:
            subprocess.run(['sudo', 'shutdown', '-h', 'now'], timeout=10)
        except Exception as e:
            logger.error(f"Shutdown command failed: {e}")
            # Fallback: force poweroff
            try:
                subprocess.run(['sudo', 'poweroff', '-f'], timeout=5)
            except:
                pass
    
    def stop(self):
        """Stop the monitor."""
        self.running = False


# =============================================================================
# GPIO Ignition Monitor (Hardware Method)
# =============================================================================

class GPIOIgnitionMonitor:
    """Monitor ignition state via GPIO pin with voltage divider.
    
    More reliable than CAN activity monitoring, but requires additional wiring:
    
    Wiring diagram:
        Ignition+ (Klemme 15, ~12V switched)
            │
            ├── R1: 33kΩ 1/4W
            ├─── GPIO17 (Pin 11, 3.3V max!)
            │
            ├── R2: 10kΩ 1/4W
            └─── GND
        
        Voltage at GPIO: Vgpio = 12V × R2/(R1+R2) = 12×10/43 ≈ 2.79V → HIGH
        When ignition OFF: 0V → LOW
    
    Safe: Voltage divider ensures GPIO never sees >3.3V even at 14.4V alternator voltage
    (14.4 × 10/43 ≈ 3.35V — add 3.3V Zener diode for extra safety)
    """
    
    def __init__(self, gpio_pin: int = GPIO_IGNITION_PIN,
                 debounce: float = GPIO_DEBOUNCE_TIME):
        self.gpio_pin = gpio_pin
        self.debounce = debounce
        self.ignition_on = False
        self.running = False
        self._gpio_available = False
        
        try:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            self._gpio_available = True
            logger.info(f"GPIO ignition monitor on pin {self.gpio_pin}")
        except ImportError:
            logger.warning("RPi.GPIO not available — GPIO monitoring disabled")
            logger.warning("Install: pip3 install RPi.GPIO")
        except Exception as e:
            logger.warning(f"GPIO setup failed: {e}")
    
    def read_ignition(self) -> bool:
        """Read current ignition state from GPIO."""
        if not self._gpio_available:
            return False
        
        return self.GPIO.input(self.gpio_pin) == self.GPIO.HIGH
    
    def run(self, on_shutdown=None):
        """Run the GPIO monitor loop."""
        if not self._gpio_available:
            logger.error("GPIO not available — cannot run hardware monitor")
            return
        
        self.running = True
        self.ignition_on = self.read_ignition()
        logger.info(f"GPIO monitor started — initial state: ignition={'ON' if self.ignition_on else 'OFF'}")
        
        low_start = None
        
        while self.running:
            try:
                current = self.read_ignition()
                
                if current:
                    # Ignition is ON
                    if not self.ignition_on:
                        logger.info("Ignition transition: OFF → ON")
                    self.ignition_on = True
                    low_start = None
                else:
                    # Ignition is OFF (or voltage dropped)
                    if self.ignition_on:
                        if low_start is None:
                            low_start = time.time()
                            logger.info("Ignition voltage LOW — debouncing...")
                        
                        # Confirm LOW for debounce period
                        if time.time() - low_start > self.debounce:
                            logger.info(f"Ignition confirmed OFF after {self.debounce}s debounce")
                            self.ignition_on = False
                            
                            if on_shutdown is None or on_shutdown():
                                self._do_shutdown()
                                break
                
                time.sleep(0.5)  # Check every 500ms
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"GPIO monitor error: {e}")
                time.sleep(5)
        
        self.running = False
        self._cleanup()
    
    def _do_shutdown(self):
        """Execute shutdown sequence (same as CANActivityMonitor)."""
        logger.info("=== GPIO SHUTDOWN SEQUENCE ===")
        
        if PRE_SHUTDOWN_SCRIPT and Path(PRE_SHUTDOWN_SCRIPT).exists():
            logger.info(f"Running pre-shutdown script: {PRE_SHUTDOWN_SCRIPT}")
            try:
                subprocess.run(['python3', PRE_SHUTDOWN_SCRIPT], timeout=30)
            except Exception as e:
                logger.error(f"Pre-shutdown script failed: {e}")
        
        logger.info(f"Waiting {SHUTDOWN_DELAY}s before shutdown...")
        time.sleep(SHUTDOWN_DELAY)
        
        logger.info("Shutting down NOW")
        try:
            subprocess.run(['sudo', 'shutdown', '-h', 'now'], timeout=10)
        except Exception as e:
            logger.error(f"Shutdown failed: {e}")
    
    def _cleanup(self):
        """Clean up GPIO."""
        if self._gpio_available:
            try:
                self.GPIO.cleanup(self.gpio_pin)
            except:
                pass
    
    def stop(self):
        """Stop the monitor."""
        self.running = False


# =============================================================================
# Combined Monitor (Recommended — uses both methods)
# =============================================================================

class CombinedPowerMonitor:
    """Uses both CAN activity AND GPIO to detect ignition state.
    
    Logic:
    - If GPIO available: GPIO is primary, CAN is backup
    - If GPIO unavailable: CAN activity only (software method)
    - Shutdown only when BOTH methods agree ignition is off,
      or when the primary method is confident.
    
    This is the recommended monitor for production use.
    """
    
    def __init__(self, can_interface: str = CAN_INTERFACE,
                 can_idle_timeout: int = CAN_IDLE_TIMEOUT,
                 gpio_pin: int = GPIO_IGNITION_PIN):
        self.can_monitor = CANActivityMonitor(can_interface, can_idle_timeout)
        self.gpio_monitor = GPIOIgnitionMonitor(gpio_pin)
        self.running = False
        self.ignition_on = True
        
        self.has_gpio = self.gpio_monitor._gpio_available
    
    def run(self, on_shutdown=None):
        """Run combined power monitoring."""
        self.running = True
        logger.info(f"Combined power monitor started "
                    f"(CAN={self.can_monitor.interface}, GPIO={'yes' if self.has_gpio else 'no'})")
        
        while self.running:
            try:
                can_ignition = self.can_monitor.check_activity()
                gpio_ignition = self.gpio_monitor.read_ignition() if self.has_gpio else None
                
                if self.has_gpio:
                    # GPIO is primary
                    if gpio_ignition is False and not can_ignition:
                        # Both agree: ignition is off
                        logger.info("GPIO + CAN both confirm ignition OFF")
                        self.ignition_on = False
                        if on_shutdown is None or on_shutdown():
                            self._shutdown()
                            break
                    elif gpio_ignition is False and can_ignition:
                        # GPIO says off but CAN still active — wait
                        logger.warning("GPIO=OFF but CAN=active — waiting for confirmation")
                    else:
                        self.ignition_on = True
                else:
                    # CAN only (software method)
                    if not can_ignition:
                        self.ignition_on = False
                        if on_shutdown is None or on_shutdown():
                            self._shutdown()
                            break
                
                time.sleep(self.can_monitor.check_interval)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                time.sleep(30)
        
        self.running = False
        self.stop()
    
    def _shutdown(self):
        """Execute shutdown."""
        logger.info("=== COMBINED SHUTDOWN SEQUENCE ===")
        
        # Log final stats
        logger.info(f"CAN monitor last RX: {self.can_monitor.last_rx_packets} packets")
        
        # Same shutdown procedure
        if PRE_SHUTDOWN_SCRIPT and Path(PRE_SHUTDOWN_SCRIPT).exists():
            try:
                subprocess.run(['python3', PRE_SHUTDOWN_SCRIPT], timeout=30)
            except:
                pass
        
        logger.info(f"Shutdown in {SHUTDOWN_DELAY}s...")
        time.sleep(SHUTDOWN_DELAY)
        
        try:
            subprocess.run(['sudo', 'shutdown', '-h', 'now'], timeout=10)
        except:
            try:
                subprocess.run(['sudo', 'poweroff', '-f'], timeout=5)
            except:
                pass
    
    def stop(self):
        """Stop all monitors."""
        self.running = False
        self.can_monitor.stop()
        self.gpio_monitor.stop()


# =============================================================================
# Systemd Service File Generator
# =============================================================================

SERVICE_FILE = """[Unit]
Description=V50 CAN Power Monitor — Safe Pi Shutdown
After=network.target bluetooth.target

[Service]
Type=simple
User=pi
WorkingDirectory=/opt/data/home/vehicle-database/projects/v50-stealth-rebuild/canbus
ExecStart=/usr/bin/python3 /opt/data/home/vehicle-database/projects/v50-stealth-rebuild/canbus/v50_power_monitor.py --combined
Restart=on-failure
RestartSec=30
StandardOutput=journal
StandardError=journal

# Ensure clean shutdown — give 45s for shutdown sequence
TimeoutStopSec=45

[Install]
WantedBy=multi-user.target
"""


def generate_service_file(output_path: str = None):
    """Generate the systemd service file for auto-start."""
    if output_path is None:
        output_path = str(Path(__file__).parent / 'v50_power_monitor.service')
    
    with open(output_path, 'w') as f:
        f.write(SERVICE_FILE)
    
    print(f"Service file written to: {output_path}")
    print("Install with:")
    print("  sudo cp v50_power_monitor.service /etc/systemd/system/")
    print("  sudo systemctl daemon-reload")
    print("  sudo systemctl enable v50_power_monitor")
    print("  sudo systemctl start v50_power_monitor")


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='V50 Power Monitor — Safe Raspberry Pi Shutdown')
    parser.add_argument('--can', action='store_true',
                       help='Use CAN bus activity detection only (software)')
    parser.add_argument('--gpio', action='store_true',
                       help='Use GPIO ignition detection only (hardware)')
    parser.add_argument('--combined', action='store_true',
                       help='Use both CAN and GPIO (recommended)')
    parser.add_argument('--service', action='store_true',
                       help='Generate systemd service file')
    parser.add_argument('--timeout', type=int, default=CAN_IDLE_TIMEOUT,
                       help=f'CAN idle timeout in seconds (default: {CAN_IDLE_TIMEOUT})')
    parser.add_argument('--gpio-pin', type=int, default=GPIO_IGNITION_PIN,
                       help=f'GPIO pin for ignition detection (default: {GPIO_IGNITION_PIN})')
    parser.add_argument('--dry-run', action='store_true',
                       help="Don't actually shutdown (for testing)")
    parser.add_argument('--verbose', '-v', action='store_true')
    
    args = parser.parse_args()
    
    level = logging.DEBUG if args.verbose else logging.INFO
    log_dir = LOG_FILE.parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(str(LOG_FILE))
        ]
    )
    
    if args.service:
        generate_service_file()
        return 0
    
    # Select monitor type
    if args.combined:
        monitor = CombinedPowerMonitor(
            can_idle_timeout=args.timeout,
            gpio_pin=args.gpio_pin
        )
    elif args.gpio:
        monitor = GPIOIgnitionMonitor(gpio_pin=args.gpio_pin)
    else:
        # Default: CAN activity (software method, no extra hardware needed)
        monitor = CANActivityMonitor(idle_timeout=args.timeout)
    
    # Dry run: just log, don't actually shutdown
    def dry_run_shutdown_check():
        logger.info("[DRY RUN] Would shutdown now — skipping actual shutdown")
        return False  # Cancel shutdown
    
    on_shutdown = dry_run_shutdown_check if args.dry_run else None
    
    logger.info(f"V50 Power Monitor starting (dry_run={args.dry_run})")
    
    try:
        if isinstance(monitor, CombinedPowerMonitor):
            monitor.run(on_shutdown=on_shutdown)
        elif isinstance(monitor, CANActivityMonitor):
            monitor.run(on_shutdown=on_shutdown)
        else:
            monitor.run(on_shutdown=on_shutdown)
    except KeyboardInterrupt:
        logger.info("Power monitor interrupted")
    
    # Cleanup
    if isinstance(monitor, CombinedPowerMonitor):
        monitor.stop()
    elif isinstance(monitor, CANActivityMonitor):
        monitor.stop()
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
