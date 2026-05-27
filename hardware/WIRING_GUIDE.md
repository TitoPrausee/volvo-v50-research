# Volvo V50 — Wiring & Installation Guide

> RPi 5 + PiCAN2 Duo integration for custom dashboard  
> Last updated: 2026-05-27

## PiCAN2 Duo GPIO Pinout (RPi 5)

| Function | GPIO | BCM | Physical Pin |
|----------|------|-----|-------------|
| SPI MOSI | GPIO10 | SPI0_MOSI | Pin 19 |
| SPI MISO | GPIO9 | SPI0_MISO | Pin 21 |
| SPI SCK | GPIO11 | SPI0_SCK | Pin 23 |
| SPI CE0 | GPIO8 | SPI0_CE0 | Pin 24 |
| SPI CE1 | GPIO7 | SPI0_CE1 | Pin 26 |
| CAN0 INT | GPIO25 | — | Pin 22 |
| CAN1 INT | GPIO24 | — | Pin 18 |
| CAN0 TX | MCP2551 | SPI via MCP2515 | — |
| CAN1 TX | MCP2551 | SPI via MCP2515 | — |

### Enable SPI on Pi 5
```bash
# /boot/firmware/config.txt (Pi 5 uses /boot/firmware/)
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25
dtoverlay=mcp2515-can1,oscillator=16000000,interrupt=24
```

### Bring up CAN interfaces
```bash
sudo ip link set can0 up type can bitrate 500000
sudo ip link set can1 up type can bitrate 125000
```

## OBD-II Connector Wiring

### Standard OBD2 Port (Female, Car Side)

| Pin | Wire Color (typically) | Function | Connect To |
|-----|----------------------|----------|------------|
| 6 | White | High-Speed CAN-H | PiCAN2 CAN0-H |
| 14 | Blue/White | High-Speed CAN-L | PiCAN2 CAN0-L |
| 3 | — | Low-Speed CAN-H (⚠️ not on all models) | PiCAN2 CAN1-H |
| 11 | — | Low-Speed CAN-L (⚠️ not on all models) | PiCAN2 CAN1-L |
| 16 | Red | +12V Battery (always on) | Buck converter input |
| 4 | Black | Chassis Ground | Ground bus |
| 5 | Black | Signal Ground | Ground bus |
| 7 | — | K-Line (ISO 9141) | Not used for CAN |
| 15 | — | L-Line (ISO 9141) | Not used for CAN |

### ⚠️ Critical Note
Low-Speed CAN (pins 3/11) is **NOT available on all V50 models** from the OBD port. On many P1 cars, low-speed CAN is only accessible behind the CEM or by splicing into the body wiring harness. **Verify with a multimeter before connecting!**

## Power Supply Wiring

### 12V → 5V Buck Converter Circuit

```
Car Battery (+12V) ───────┬──── Fuse (5A) ──── Schottky Diode ────┬──── 470µF ──── Buck IN
                           │                                      │     25V          │
Car Ground ───────────────┼────────────────────────────────────────┼─────────────────Buck GND
                           │                                      │
Ignition (15) ────────────┘                                      ┌─┴─┐
                                                                  │Rel│ ← NC to Pi
                                                                  │ay │   (auto on/off)
                                                                  └─┬─┘
                                                                    │
Buck OUT ─────────────────────────────────────────────────── 220µF ─┴─ Pi 5 (5V, 3A+)

IMPORTANT:
- Schottky diode (1N5822): Reverse polarity protection
- 470µF input cap: Smooths engine crank voltage drops
- 220µF output cap: Reduces ripple for Pi stability
- Relay coil: Connected to ignition (terminal 15) so Pi powers on with key
- Add a 5-10 second delay circuit (RC timer) for Pi shutdown on key-off
```

### Crank Protection
During engine start, car voltage can drop to 8-9V and spike to 14.4V. The buck converter must handle:
- Input range: 6-24V (use LM2596HV or similar automotive-grade)
- Sustained output: 5.1V at 3A minimum (Pi 5 peak draw)
- Add a supercapacitor (0.47F 5.5V) across the 5V rail for brownout protection

## Display Wiring

### 7" HDMI Display (1024×600)

| Pi 5 Pin | Display Pin | Function |
|----------|-------------|----------|
| HDMI Out | HDMI In | Video signal |
| USB-A 5V | Display USB | Touch screen (if touch model) |
| GPIO 5V | Display 5V | Backlight power (if separate) |

### Display Power Options
1. **From Pi USB**: Simple, but may cause brownouts at high brightness
2. **Separate buck converter**: Better, dedicated 5V/2A for display
3. **From display controller**: Some displays have built-in 12V→5V buck

## CAN Bus Physical Installation

### Step 1: OBD2 Port Connection (High-Speed CAN)
1. Locate OBD2 port under driver's side dashboard (left of steering wheel)
2. Insert OBD2-to-DB9 adapter
3. Connect DB9 to PiCAN2 CAN0 port
4. Verify CAN-H (pin 6) and CAN-L (pin 14) with multimeter:
   - Key OFF: CAN-H ≈ 2.5V, CAN-L ≈ 2.5V
   - Key ON: CAN-H ≈ 3.5V, CAN-L ≈ 1.5V (when active)

### Step 2: Low-Speed CAN Tap (if needed)
1. Remove driver's side lower dash panel (2 T25 Torx screws)
2. Locate CEM behind glovebox
3. Find white/blue twisted pair (CAN body bus)
4. Use a "Y-tap" connector — do NOT cut the original wires
5. Connect to PiCAN2 CAN1 port
6. Add 120Ω termination resistor at PiCAN2 end

### Step 3: CAN Termination
- PiCAN2 Duo has built-in 120Ω termination jumpers
- Enable both (CAN0 and CAN1) if you're at the end of the bus
- If CAN works intermittently, check termination
- High-Speed CAN: 120Ω between pins 6 and 14 (OBD) = correct termination
- Low-Speed CAN: 120Ω between CAN-H and CAN-L at the tap point

## Software Setup (RPi 5)

```bash
# Install OS
sudo raspi-config  # Enable SPI, disable serial console

# Install CAN tools
sudo apt update && sudo apt install -y can-utils python3-can

# Enable CAN interfaces (add to /etc/rc.local)
sudo ip link set can0 up type can bitrate 500000 restart-ms 100
sudo ip link set can1 up type can bitrate 125000 restart-ms 100

# Test CAN
candump can0  # Should show traffic when key is ON

# Install Python CAN
pip3 install python-can cantools

# Dashboard software (choose one)
# Option A: Custom PyQt dashboard
pip3 install PyQt5 pyqtgraph

# Option B: OpenAuto / Crankshaft (CarPlay)
git clone https://github.com/openauto/openauto.git
```

## Startup/Shutdown Sequence

### Auto-Start on Ignition
```python
# /opt/volvo/dashboard/watchdog.py
import RPi.GPIO as GPIO
import subprocess, time, os

IGNITION_PIN = 17  # GPIO 17 connected to ignition-sensing relay

GPIO.setmode(GPIO.BCM)
GPIO.setup(IGNITION_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def wait_for_ignition():
    """Wait for ignition to turn on"""
    while GPIO.input(IGNITION_PIN) == 0:
        time.sleep(0.5)
    return True

def graceful_shutdown():
    """Shut down Pi after ignition off"""
    time.sleep(10)  # Grace period
    if GPIO.input(IGNITION_PIN) == 0:  # Still off?
        subprocess.run(["sudo", "shutdown", "-h", "now"])

if __name__ == "__main__":
    while True:
        if wait_for_ignition():
            subprocess.Popen(["python3", "/opt/volvo/dashboard/main.py"])
        graceful_shutdown()
```

## ⚠️ Safety Warnings

1. **NEVER** connect 12V directly to Pi GPIO pins
2. **ALWAYS** use a fuse on the 12V supply (5A blade fuse)
3. **Double-check** CAN-H and CAN-L with a multimeter before powering on
4. **Do NOT** cut CAN bus wires — use Y-tap connectors
5. **Secure** all wiring away from moving parts (pedals, steering column)
6. **Test** on bench before installing in car
7. **Ground** all equipment to the same point (star ground)