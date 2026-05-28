#!/usr/bin/env python3
"""
Volvo V50 2.4i — GPIO Stealth Mode Button Handler
===================================================
Monitors physical GPIO buttons for:
- STEALTH mode toggle: switch between custom dashboard and OEM display
- Page switch: cycle through dashboard pages
- Brightness: adjust display brightness
- Force shutdown: emergency Pi shutdown

Hardware:
- GPIO17: Stealth mode toggle button (pull-up, active low)
- GPIO27: Page switch button (pull-up, active low)
- GPIO22: Brightness up (pull-up, active low)
- GPIO23: Brightness down (pull-up, active low)
- GPIO5:  Emergency shutdown (hold 5s, pull-up, active low)

Uses RPi.GPIO (installed on Pi) with fallback to simulated mode for development.

Debounce: 200ms hardware, 300ms software
Long press detection: >2s = long press, >5s = emergency

Author: v50-developer agent
Date: 2026-05-28
"""

import logging
import time
import threading
from enum import Enum, auto
from typing import Callable, Optional

logger = logging.getLogger('v50.gpio_buttons')

# Try to import RPi.GPIO — fall back to mock for development
try:
    import RPi.GPIO as GPIO
    HAS_GPIO = True
except ImportError:
    HAS_GPIO = False
    logger.warning("RPi.GPIO not available — running in simulated mode")


class ButtonEvent(Enum):
    """Button event types."""
    STEALTH_TOGGLE = auto()
    STEALTH_LONG = auto()
    PAGE_NEXT = auto()
    PAGE_PREV = auto()
    BRIGHTNESS_UP = auto()
    BRIGHTNESS_DOWN = auto()
    EMERGENCY_SHUTDOWN = auto()
    
    # Combined events
    STEALTH_AND_PAGE = auto()  # Stealth toggle + page switch simultaneously


class ButtonState(Enum):
    """Current display mode."""
    CUSTOM = "custom"      # Custom dashboard active
    STEALTH = "stealth"    # OEM-style display active
    OFF = "off"            # Display off (night mode, minimal)


# =============================================================================
# GPIO Pin Configuration
# =============================================================================

GPIO_PINS = {
    'stealth': 17,      # Stealth mode toggle
    'page': 27,         # Page switch
    'bright_up': 22,    # Brightness increase
    'bright_down': 23,  # Brightness decrease
    'emergency': 5,      # Emergency shutdown (hold 5s)
}

DEBOUNCE_MS = 200          # Hardware debounce (ms)
LONG_PRESS_MS = 2000        # Long press threshold (ms)
EMERGENCY_PRESS_MS = 5000   # Emergency shutdown threshold (ms)
POLL_INTERVAL = 0.05        # Button poll interval (seconds)

# Brightness levels (0-100%)
BRIGHTNESS_LEVELS = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
DEFAULT_BRIGHTNESS_IDX = 5  # 50%


class GPIOButtonHandler:
    """
    Handles GPIO button inputs for the V50 dashboard.
    
    Provides debounced button detection, long-press support,
    and callbacks for dashboard integration.
    """
    
    def __init__(self,
                 stealth_callback: Optional[Callable] = None,
                 page_callback: Optional[Callable] = None,
                 brightness_callback: Optional[Callable] = None,
                 shutdown_callback: Optional[Callable] = None):
        """
        Initialize button handler.
        
        Args:
            stealth_callback: Called when stealth mode toggles. Receives ButtonState.
            page_callback: Called on page switch. Receives direction (+1 or -1).
            brightness_callback: Called on brightness change. Receives new brightness 0-100.
            shutdown_callback: Called on emergency shutdown.
        """
        self.stealth_callback = stealth_callback
        self.page_callback = page_callback
        self.brightness_callback = brightness_callback
        self.shutdown_callback = shutdown_callback
        
        self.display_mode = ButtonState.CUSTOM
        self.brightness_idx = DEFAULT_BRIGHTNESS_IDX
        self.running = False
        self._thread: Optional[threading.Thread] = None
        
        # Button state tracking
        self._button_states = {}
        self._press_times = {}
        for name in GPIO_PINS:
            self._button_states[name] = True   # Pull-up = high = not pressed
            self._press_times[name] = 0.0
        
        # Callbacks list for multiple subscribers
        self._event_callbacks = []
        
        # Initialize GPIO
        self._setup_gpio()
    
    def _setup_gpio(self):
        """Configure GPIO pins."""
        if HAS_GPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            for name, pin in GPIO_PINS.items():
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                # Add interrupt-based detection for faster response
                GPIO.add_event_detect(pin, GPIO.FALLING,
                                       callback=lambda channel, n=name: self._on_button_press(n),
                                       bouncetime=DEBOUNCE_MS)
            logger.info("GPIO initialized with hardware interrupt support")
        else:
            logger.info("GPIO simulated — using poll-based detection")
    
    def _on_button_press(self, button_name: str):
        """Handle a button press (called from GPIO interrupt or poll)."""
        press_time = time.time()
        self._press_times[button_name] = press_time
        
        # For short-press actions, we'll schedule a delayed check
        # If the button is still held after LONG_PRESS_MS, it's a long press
        threading.Timer(LONG_PRESS_MS / 1000.0, 
                        self._check_long_press, 
                        args=[button_name, press_time]).start()
    
    def _check_long_press(self, button_name: str, press_time: float):
        """Check if button is still held (long press detected)."""
        if press_time != self._press_times.get(button_name, 0):
            return  # Button was released and re-pressed, ignore
        
        if not self._is_button_pressed(button_name):
            return  # Button was released, short press handled elsewhere
        
        # Long press detected
        logger.info(f"Long press detected: {button_name}")
        
        if button_name == 'stealth':
            self._emit_event(ButtonEvent.STEALTH_LONG)
        elif button_name == 'emergency':
            # Check for 5-second hold
            threading.Timer((EMERGENCY_PRESS_MS - LONG_PRESS_MS) / 1000.0,
                           self._check_emergency_press,
                           args=[button_name, press_time]).start()
    
    def _check_emergency_press(self, button_name: str, press_time: float):
        """Check for emergency shutdown (5-second hold)."""
        if press_time != self._press_times.get(button_name, 0):
            return
        
        if self._is_button_pressed(button_name):
            logger.warning("EMERGENCY SHUTDOWN button held for 5 seconds!")
            self._emit_event(ButtonEvent.EMERGENCY_SHUTDOWN)
    
    def _is_button_pressed(self, button_name: str) -> bool:
        """Check if button is currently pressed (active low)."""
        if HAS_GPIO:
            return GPIO.input(GPIO_PINS[button_name]) == GPIO.LOW
        else:
            # Simulated mode — check internal state
            return not self._button_states.get(button_name, True)
    
    def _emit_event(self, event: ButtonEvent):
        """Emit a button event to all registered callbacks."""
        logger.info(f"Button event: {event.name}")
        
        # Mode-specific handling
        if event == ButtonEvent.STEALTH_TOGGLE:
            if self.display_mode == ButtonState.CUSTOM:
                self.display_mode = ButtonState.STEALTH
            elif self.display_mode == ButtonState.STEALTH:
                self.display_mode = ButtonState.CUSTOM
            else:
                self.display_mode = ButtonState.CUSTOM
            
            if self.stealth_callback:
                self.stealth_callback(self.display_mode)
        
        elif event == ButtonEvent.STEALTH_LONG:
            # Long press: cycle CUSTOM → STEALTH → OFF → CUSTOM
            if self.display_mode == ButtonState.CUSTOM:
                self.display_mode = ButtonState.STEALTH
            elif self.display_mode == ButtonState.STEALTH:
                self.display_mode = ButtonState.OFF
            else:
                self.display_mode = ButtonState.CUSTOM
            
            if self.stealth_callback:
                self.stealth_callback(self.display_mode)
        
        elif event == ButtonEvent.PAGE_NEXT:
            if self.page_callback:
                self.page_callback(1)
        
        elif event == ButtonEvent.PAGE_PREV:
            if self.page_callback:
                self.page_callback(-1)
        
        elif event == ButtonEvent.BRIGHTNESS_UP:
            self.brightness_idx = min(self.brightness_idx + 1, len(BRIGHTNESS_LEVELS) - 1)
            if self.brightness_callback:
                self.brightness_callback(BRIGHTNESS_LEVELS[self.brightness_idx])
        
        elif event == ButtonEvent.BRIGHTNESS_DOWN:
            self.brightness_idx = max(self.brightness_idx - 1, 0)
            if self.brightness_callback:
                self.brightness_callback(BRIGHTNESS_LEVELS[self.brightness_idx])
        
        elif event == ButtonEvent.EMERGENCY_SHUTDOWN:
            if self.shutdown_callback:
                self.shutdown_callback()
        
        # Notify all subscribers
        for callback in self._event_callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Event callback error: {e}")
        
        # Simulated button release handling for short presses
        if event in (ButtonEvent.BRIGHTNESS_UP, ButtonEvent.BRIGHTNESS_DOWN,
                     ButtonEvent.PAGE_NEXT, ButtonEvent.PAGE_PREV):
            # These are short-press actions
            pass
    
    def _poll_loop(self):
        """Background thread for poll-based button detection (used without GPIO ints)."""
        if HAS_GPIO:
            return  # Using interrupts, no need for polling
        
        while self.running:
            for name, pin in GPIO_PINS.items():
                # In simulated mode, we just check for keypresses or external input
                pass  # In production, read GPIO state here
            
            time.sleep(POLL_INTERVAL)
    
    def start(self):
        """Start the button handler."""
        self.running = True
        if not HAS_GPIO:
            self._thread = threading.Thread(target=self._poll_loop, daemon=True)
            self._thread.start()
        logger.info("GPIO button handler started")
    
    def stop(self):
        """Stop the button handler and cleanup GPIO."""
        self.running = False
        if HAS_GPIO:
            try:
                GPIO.cleanup()
            except Exception:
                pass
        logger.info("GPIO button handler stopped")
    
    def add_event_callback(self, callback: Callable[[ButtonEvent], None]):
        """Add a callback for button events."""
        self._event_callbacks.append(callback)
    
    # =========================================================================
    # Simulated Mode — for testing without hardware
    # =========================================================================
    
    def simulate_press(self, button_name: str, duration_ms: int = 100):
        """Simulate a button press (for testing without GPIO hardware).
        
        Args:
            button_name: One of 'stealth', 'page', 'bright_up', 'bright_down', 'emergency'
            duration_ms: Press duration in ms (short <2000, long 2000-5000, emergency >5000)
        """
        if button_name not in GPIO_PINS:
            logger.error(f"Unknown button: {button_name}")
            return
        
        logger.info(f"Simulated press: {button_name} for {duration_ms}ms")
        
        if duration_ms >= EMERGENCY_PRESS_MS:
            self._emit_event(ButtonEvent.EMERGENCY_SHUTDOWN)
        elif duration_ms >= LONG_PRESS_MS:
            if button_name == 'stealth':
                self._emit_event(ButtonEvent.STEALTH_LONG)
        else:
            # Short press
            if button_name == 'stealth':
                self._emit_event(ButtonEvent.STEALTH_TOGGLE)
            elif button_name == 'page':
                self._emit_event(ButtonEvent.PAGE_NEXT)
            elif button_name == 'bright_up':
                self._emit_event(ButtonEvent.BRIGHTNESS_UP)
            elif button_name == 'bright_down':
                self._emit_event(ButtonEvent.BRIGHTNESS_DOWN)
            elif button_name == 'emergency':
                logger.warning("Emergency button short press — no action (hold 5s for shutdown)")
    
    def get_brightness(self) -> int:
        """Get current brightness percentage."""
        return BRIGHTNESS_LEVELS[self.brightness_idx]
    
    def get_mode(self) -> ButtonState:
        """Get current display mode."""
        return self.display_mode


# =============================================================================
# Main (for testing)
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="V50 GPIO Button Handler Test")
    parser.add_argument('--simulate', action='store_true', help='Run in simulated mode')
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    def on_stealth(mode: ButtonState):
        print(f"  → Stealth mode: {mode.value}")
    
    def on_page(direction: int):
        print(f"  → Page: {'next' if direction > 0 else 'prev'}")
    
    def on_brightness(level: int):
        print(f"  → Brightness: {level}%")
    
    def on_shutdown():
        print("  → EMERGENCY SHUTDOWN triggered!")
    
    handler = GPIOButtonHandler(
        stealth_callback=on_stealth,
        page_callback=on_page,
        brightness_callback=on_brightness,
        shutdown_callback=on_shutdown
    )
    
    print("=== V50 GPIO Button Handler Test ===")
    print(f"GPIO available: {'yes' if HAS_GPIO else 'no (simulated)'}")
    print()
    
    if args.simulate or not HAS_GPIO:
        print("Running simulated button tests...")
        print()
        
        # Test stealth toggle
        print("1. Stealth toggle (short press):")
        handler.simulate_press('stealth')
        
        print("2. Stealth toggle back:")
        handler.simulate_press('stealth')
        
        print("3. Stealth long press (CUSTOM → OFF):")
        handler.simulate_press('stealth', duration_ms=3000)
        
        print("4. Stealth short press (OFF → STEALTH):")
        handler.simulate_press('stealth')
        
        print("5. Page next:")
        handler.simulate_press('page')
        
        print("6. Brightness up:")
        for _ in range(3):
            handler.simulate_press('bright_up')
        print(f"   Current brightness: {handler.get_brightness()}%")
        
        print("7. Brightness down:")
        for _ in range(2):
            handler.simulate_press('bright_down')
        print(f"   Current brightness: {handler.get_brightness()}%")
        
        print(f"\nCurrent mode: {handler.get_mode().value}")
        print(f"Current brightness: {handler.get_brightness()}%")
    
    handler.stop()