# Volvo V50 Dashboard — Wiring Guide

> **Revision**: 1.0 — May 2026
> **PiCAN2 Duo** installation on Raspberry Pi 5 for Volvo V50 CAN bus reading

---

## 1. PiCAN2 Duo GPIO Pinout (Raspberry Pi 5)

The PiCAN2 Duo uses **SPI interface** to communicate with both MCP2515 CAN controllers. Below is the GPIO mapping:

### Header: J8 (40-pin GPIO)

```
┌─────────────────────────────────────────────┐
│  ·  3.3V  (1)  (2)  5V ·                    │
│  ·  GPIO2  (3)  (4)  5V ·                    │
│  ·  GPIO3  (5)  (6)  GND·──── GND           │
│  ·  GPIO4  (7)  (8)  GPIO14·── (UART TX)    │
│  ·  GND    (9)  (10) GPIO15·── (UART RX)    │
│  ·  GPIO17 (11) (12) GPIO18·── (PCM_CLK)    │
│  ·  GPIO27 (13) (14) GND ·                   │
│  ·  GPIO22 (15) (16) GPIO23·                 │
│  ·  3.3V   (17) (18) GPIO24·                 │
│  ·  GPIO10 (19) (20) GND ·    ──── SPI0_MOSI │
│  ·  GPIO9  (21) (22) GPIO25·   ──── SPI0_MISO│
│  ·  GPIO11 (23) (24) GPIO8 ·   ──── SPI0_SCLK│
│  ·  GND    (25) (26) GPIO7 ·    ──── SPI0_CE1│
│  ·  GPIO0  (27) (28) GPIO1·    ──── ID_SD    │
│  ·  GPIO5  (29) (30) GND ·    ──── ID_SC    │
│  ·  GPIO6  (31) (32) GPIO12·                 │
│  ·  GPIO13 (33) (34) GND ·                   │
│  ·  GPIO19 (35) (36) GPIO16·                 │
│  ·  GPIO26 (37) (38) GPIO20·                 │
│  ·  GND    (39) (40) GPIO21·                 │
└─────────────────────────────────────────────┘
```

### PiCAN2 Duo Signal Mapping

| Pi Pin# | Pi GPIO | PiCAN2 Function | Notes |
|---------|---------|----------------|-------|
| 19 | GPIO10 (MOSI) | SPI0_MOSI | To MCP2515 SI pins |
| 21 | GPIO9 (MISO) | SPI0_MISO | To MCP2515 SO pins |
| 23 | GPIO11 (SCLK) | SPI0_SCLK | To MCP2515 SCK pins |
| 24 | GPIO8 (CE0) | SPI0_CE0 → **INT_CAN0** | Chip select CAN0 (high-speed) |
| 26 | GPIO7 (CE1) | SPI0_CE1 → **INT_CAN1** | Chip select CAN1 (low-speed) |
| 22 | GPIO25 | **INT_CAN0** | Interrupt from CAN0 controller |
| 13 | GPIO27 | **INT_CAN1** | Interrupt from CAN1 controller |
| 1 | 3.3V | 3.3V supply | Power for MCP2515 |
| 2,4 | 5V | 5V supply | Power for MCP2551 transceivers |
| 6,9,14,20,25,30,34,39 | GND | GND | Common ground |

### CAN Channel Assignment

| Channel | Chip Select | Bus | Bitrate | Volvo Bus |
|---------|------------|-----|---------|-----------|
| **CAN0** | CE0 (GPIO8) | SPI0 | 500 kbit/s | High-speed CAN (engine, drivetrain) |
| **CAN1** | CE1 (GPIO7) | SPI0 | 125 kbit/s | Low-speed CAN (body, comfort) |

### Jumper Settings on PiCAN2 Duo

| Jumper | Label | Setting | Effect |
|--------|-------|---------|--------|
| JP1 | 120R CAN0 | **ON** (fitted) | Enables 120Ω termination for CAN0 |
| JP2 | 120R CAN1 | **ON** (fitted) | Enables 120Ω termination for CAN1 |
| JP3 | PWR | DEFAULT | Selects power source (GPIO 5V) |

> **When to enable termination**: If the Pi is at one end of a CAN bus segment. On the OBD-II port, the bus already has termination in the vehicle. **For CAN0 (OBD-II)** the termination is already in the car's modules — leave JP1 OFF. **For CAN1 (splice into CEM)** the bus is short enough that you may need JP2 ON if the splice is far from the CEM.

---

## 2. OBD-II Connector Wiring (High-Speed CAN)

The V50's OBD-II diagnostic port gives direct access to the **high-speed CAN bus** (engine, transmission, ABS, DIM, ACC).

### OBD-II Port (Female, under dash — driver side)

```
 ┌───\   /───┐
 │ 4  1  5   │
 │  6        │
 │ 7         │
 │ 8         │
 │ 14        │
 │ 15    16  │
 └───────────┘
```

| OBD-II Pin | Signal | Wire Color (V50) | Connect To |
|------------|--------|-------------------|------------|
| 6 | **CAN-H** (high-speed) | White/Blue | PiCAN2 CAN0-H screw terminal |
| 14 | **CAN-L** (high-speed) | Blue | PiCAN2 CAN0-L screw terminal |
| 4 | Chassis Ground | Black | PiCAN2 GND (or common GND point) |
| 5 | Signal Ground | Black/Brown | PiCAN2 GND |
| 16 | +12V Battery (always) | Red | Buck converter input (for power) |
| 7 | K-Line (ISO 9141) | Yellow | Not used (diagnostics only) |

### Wiring the OBD2-to-DB9 Cable

If using the OBD2-to-DB9 cable:

```
OBD2 (male)          DB9 (female)          PiCAN2 Terminal
─────────────        ───────────────        ───────────────
Pin 6 (CAN-H)   ───  Pin 2 (DB9)      ───  CAN0-H
Pin 14 (CAN-L)  ───  Pin 7 (DB9)      ───  CAN0-L
Pin 4 (GND)     ───  Pin 3 (DB9)      ───  GND
Pin 5 (GND)     ───  Pin 5 (DB9)      ───  GND (bridge to pin 4)

If your cable doesn't have DB9, you can cut the end and use screw terminals:
┌─ OBD2 ──┐         ┌─ Screw Terminal ─┐
│ Pin 6   ├─────────┤ CAN0-H           │
│ Pin 14  ├─────────┤ CAN0-L           │
│ Pin 4+5 ├─────────┤ GND              │
└─────────┘         └──────────────────┘
```

---

## 3. Low-Speed CAN Wiring (CEM Splice)

The low-speed CAN bus (125 kbit/s) must be accessed at the CEM (Central Electronic Module).

### CEM Location

The CEM is located **under the dashboard on the driver's side**, above the footwell, behind a plastic cover. It's a black metal box with multiple connectors.

### CEM Connector B (Gray, 52-pin) — Low-Speed CAN

```
Connector B (52-pin, Gray)
┌──────────────────────────────────────────────────┐
│  (1)  (2)  (3)  (4)  (5)  (6)  (7)  (8)  (9)  │
│  (10) (11) (12) (13) (14) (15) (16) (17) (18)  │
│  ...                                            │
│  (44) (45) (46) (47) (48) (49) (50) (51) (52)  │
└──────────────────────────────────────────────────┘
```

| CEM-B Pin | Signal | Wire Color | Connect To |
|-----------|--------|------------|------------|
| 1 | **CAN-L** (low-speed) | White/Violet | PiCAN2 CAN1-L |
| 2 | **CAN-H** (low-speed) | White/Green | PiCAN2 CAN1-H |

**Splicing method**: Use T-tap connectors or solder splices. Do NOT cut the original wires — the CEM and other modules need the bus intact.

```
   ┌──── CEM ────┐
   │  B1 ────────┼── White/Violet ──┬── CAN1-L (PiCAN2)
   │  B2 ────────┼── White/Green  ──┬── CAN1-H (PiCAN2)
   └─────────────┘                 │
                                    └── Terminate 120Ω if end of bus
```

---

## 4. Power Supply Wiring

### System Architecture

```
 ┌──────────────┐
 │  Car Battery │ 12V
 │   12V (Pin 16│
 │   OBD-II or  │
 │   CEM A Pin1)│
 └──────┬───────┘
        │
        ├── [5A Fuse] ──┐
        │               │
        │         ┌─────▼──────┐      ┌──────────────────┐
        │         │  3-Way     │      │  Ignition Sense   │
        │         │  Terminal  │      │  (CEM A Pin 3)    │
        │         │  Block     │      │  Red/Yellow       │
        │         └──┬──┬──┬──┘      └────────┬─────────┘
        │            │  │  │                   │
        │            │  │  └─── GPIO (optional │ sense pin)
        │            │  │                      │
  ┌─────▼─────┐      │  └────── 12V fan (if used)
  │ Buck Conv │      │
  │ 12V → 5V  │◄─────┘
  │ D24V50F5  │
  └─────┬─────┘
        │ 5V
        │
   ┌────┴────┐
   │ 2200µF  │ ← Electrolytic capacitor (crank protection)
   │  16V    │
   └────┬────┘
        │ 5V
        │
  ┌─────┴──────┐
  │ 100nF      │ ← Ceramic capacitor (noise suppression)
  │ Ceramic    │
  └─────┬──────┘
        │ 5V
        │
   ┌────┴──────────────────────┐
   │                           │
   │  ┌───────────┐    ┌───────┴───────┐
   │  │ Pi 5 (5V) │    │ Display (5V)  │
   │  │ GPIO 2/4  │    │ Power input   │
   │  └───────────┘    └───────────────┘
   │
   └────── GND ── Chassis ground point
```

### Step-by-Step Power Wiring

#### Step 1: Prepare the 12V Supply
- Tap **+12V switched** from:
  - **CEM Connector A, Pin 3** (Red/Yellow wire) — best option, only live with ignition
  - **OBD-II Pin 16** (always-on) — use only if you want the Pi to stay on after parking
- Tap **Ground** from:
  - **CEM Connector A, Pin 4 or 5** (Black wire)
  - Or any chassis ground bolt near the CEM

#### Step 2: Add Inline Fuse
- Install a **5A mini blade fuse** on the +12V wire as close to the tap point as possible (within 15cm).
- Fuse holder → [5A fuse] → wire continues to buck converter.

#### Step 3: Wire the Buck Converter
```
Buck Converter D24V50F5:
┌─────────────────────────────────────┐
│  VIN (IN+) ──── +12V (from fuse)   │
│  GND (IN-) ──── Ground             │
│  VOUT (OUT+) ── +5V output         │
│  GND (OUT-) ── Ground (common)     │
│                                     │
│  Adjust: Potentiometer (if LM2596)  │
│  → Set to exactly 5.0V with meter  │
└─────────────────────────────────────┘
```

**If using LM2596**: Adjust the potentiometer with a multimeter to output **exactly 5.0V** before connecting to the Pi. Turn clockwise to increase voltage.

#### Step 4: Add Crank Protection Capacitors

These capacitors keep the Pi running during the voltage dip (~6-8V for ~300ms) when the starter motor engages.

```
5V rail ────┬──────┬──────┬──────► Pi 5V
            │      │      │
           [ ]    [ ]     │
           ║      ║       │
          2200µF  100nF   │
          16V     50V     │
           │      │       │
GND ───────┴──────┴───────┴──────► Pi GND
```

- **2200µF electrolytic**: Observe polarity! The stripe side (negative) goes to GND.
- **100nF ceramic**: No polarity, place as close to Pi power pins as possible.

#### Step 5: Connect to Raspberry Pi 5

The Pi 5 can be powered through:
1. **GPIO Pins 2/4 (5V) and Pin 6 (GND)** — preferred for this project
2. **USB-C PD port** (accepts 5V on non-PD chargers)

```
Option A: GPIO Power (Recommended, keep USB-C free for data)
┌────────────┐
│ Pi 5 GPIO  │
│            │
│ Pin 2 (5V) ├────── +5V from buck
│ Pin 4 (5V) ├────── +5V from buck (redundant)
│ Pin 6 (GND)├────── GND
│ Pin 14(GND)├────── GND (redundant)
└────────────┘

WARNING: Do NOT connect both GPIO and USB-C power simultaneously!
```

#### Step 6: Connect Display Power

The 7" Waveshare display has its own power input:

```
Display Power Options:
┌───────────────────────────────────────┐
│ Option 1: Direct from buck (best)     │
│  +5V ──── Display 5V input           │
│  GND ──── Display GND                │
│                                        │
│ Option 2: From Pi GPIO (limited)      │
│  Pi Pin 2/4 ──── Display 5V input    │
│  (Pi must supply extra 500mA)         │
└───────────────────────────────────────┘
```

**Recommendation**: Option 1 — run a separate 5V line from the buck converter directly to the display. The Pi's 5V rail (via GPIO) is limited by the polyfuse.

---

## 5. Display Wiring (HDMI + Touch)

### HDMI Connection

```
Pi 5 HDMI0 (micro-HDMI) ── micro-HDMI-to-HDMI cable ── Waveshare 7" HDMI IN

Cable: Standard micro-HDMI (male) to HDMI (male)
Length: 30-50cm (keep short to reduce cable clutter)
```

### Touch USB Connection

The Waveshare capacitive touch uses USB for the touch controller:

```
Pi 5 USB 2.0 (blue port) ── USB-A-to-micro-USB cable ── Display touch input (micro-USB)

Note: Use one of the Pi 5 USB 3.0 ports (blue) for touch.
The USB 2.0 ports are fine but slower.
```

### Display Backlight Control (Optional)

GPIO can control the display backlight for auto-dimming:

```
GPIO 18 (PWM0) ── NPN transistor (2N2222) ── Display backlight PWM input

Simpler alternative: Wire backlight to +5V constant (always on).
```

---

## 6. Step-by-Step Installation Guide

### Phase 1: Bench Assembly (Before Car Installation)

1. **Prepare the Pi 5**
   - Install Raspberry Pi OS (64-bit Bookworm) on microSD or NVMe SSD
   - Enable SPI: `sudo raspi-config nonint do_spi 0`
   - Install CAN utilities: `sudo apt install can-utils python3-can python3-pip`
   - Update firmware: `sudo apt update && sudo apt full-upgrade -y`

2. **Assemble the PiCAN2 Duo**
   - Install the supplied standoffs on the Pi 5
   - Align the PiCAN2 Duo HAT with the GPIO header
   - Press firmly — ensure all pins are seated
   - Set jumpers:
     - JP3 (PWR): DEFAULT (uses GPIO 5V)
     - JP1 (120R CAN0): OFF (car already has termination on high-speed bus)
     - JP2 (120R CAN1): ON if splicing far from CEM, OFF otherwise
   - Verify the HAT sits level — no gap between HAT and Pi

3. **Prepare the Buck Converter**
   - Set output voltage to **5.0V** with multimeter before car installation
   - Solder input wires (12V+ and GND) — use red for +, black for -
   - Solder output wires (5V+ and GND) — use yellow for +, black for -
   - Solder the 2200µF capacitor across the output (+ to 5V, - to GND)
   - Solder the 100nF capacitor across the output (parallel to electrolytic)
   - Install heat shrink over solder joints

4. **Prepare the OBD2 Cable**
   - If using OBD2-to-DB9: verify continuity between OBD pins and DB9 pins
   - If using cut OBD2 extension: strip, tin wires, label each (CAN-H, CAN-L, GND, +12V)
   - Attach to screw terminals on PiCAN2:
     - CAN-H → CAN0-H
     - CAN-L → CAN0-L
     - GND → GND

5. **Bench Test**
   - Power the buck converter with a 12V bench supply or car battery
   - Measure 5V output — should read 4.95-5.05V
   - Connect Pi 5 + PiCAN2 + display
   - Boot the Pi and verify it powers on
   - Run: `dmesg | grep spi` — should show SPI enabled
   - Run: `dmesg | grep mcp251x` — should show both CAN controllers detected
   - Test CAN: `sudo ip link set can0 type can bitrate 500000 && sudo ip link set can0 up && candump can0`

### Phase 2: Car Installation

6. **Disconnect the Car Battery**
   - Remove the negative terminal first
   - Wait 5 minutes for capacitors to discharge
   - ⚠️ Important: Airbag systems store energy — wait the full 5 minutes

7. **Access the CEM (Low-Speed CAN Tap)**
   - Remove the driver's side under-dash panel (T25 Torx screws)
   - Locate the CEM — metal box above the footwell
   - Identify Connector B (Gray, 52-pin) — low-speed CAN
   - Use T-tap connectors on pins B1 (White/Violet, CAN-L) and B2 (White/Green, CAN-H)
   - Run twisted pair wires to the PiCAN2 CAN1 terminals

8. **Access the OBD-II Port (High-Speed CAN)**
   - The OBD-II port is located under the dash, left of center
   - Plug in the OBD2-to-DB9 cable (or tap permanently)
   - For permanent install: use T-taps on pins 6 and 14
   - Route wire to PiCAN2 CAN0 terminals

9. **Mount the Buck Converter**
   - Choose a location with airflow (avoid heat buildup)
   - Common locations: behind the radio cavity, or on the transmission tunnel
   - Mount with double-sided tape or zip ties
   - Connect 12V+ (switched) from CEM A Pin 3 via 5A fuse
   - Connect GND to chassis ground bolt (sand paint off for good contact)

10. **Route the Power Wiring**
    - Run +5V and GND from buck converter to Pi 5
    - Keep wire runs short (<50cm) to minimize voltage drop
    - Use 1.5mm² wire for 12V input, 0.75mm² for 5V output
    - Secure wiring with zip ties away from moving pedals

11. **Install the Display**
    - Mount the 3D-printed bezel in the dashboard (replaces radio/climate panel area)
    - Insert the 7" display into the bezel
    - Connect HDMI cable from Pi 5 to display
    - Connect touch USB cable from Pi 5 to display
    - Connect display 5V power from buck converter
    - Route cables behind the dashboard

12. **Mount the Pi + PiCAN2**
    - Mount on the back of the display assembly or inside the glove box area
    - Use a protective case to prevent shorts against metal dashboard structure
    - Ensure ventilation — the Pi 5 runs hot under load

13. **Connect Grounds**
    - Establish a single star ground point (central ground bolt)
    - Connect: buck converter GND, Pi GND, CAN GND, display GND all to same point
    - Clean the ground point with sandpaper for good electrical contact

14. **Final Connections & Testing**
    - Verify all connections before reconnecting the battery
    - Check for loose wires, exposed conductors, potential shorts
    - Reconnect battery (positive first, then negative)
    - Do NOT turn ignition on yet

15. **Power-On Test**
    - Turn ignition to position I (accessory)
    - Verify Pi boots (wait 30 seconds)
    - Check display comes on with correct resolution
    - Run CAN test: `candump can0` — should see CAN messages
    - Run CAN1 test: `sudo ip link set can1 type can bitrate 125000 && sudo ip link set can1 up && candump can1`
    - If no data on CAN0: check OBD connection, termination, wiring polarity
    - If no data on CAN1: check CEM splice, jumper settings

16. **Engine Start Test**
    - Start the engine
    - Monitor Pi voltage — should stay above 4.75V during crank
    - Verify CAN data continues during startup
    - If Pi resets during crank: increase capacitor (try 3300µF or 4700µF)
    - Test all gauge displays for accuracy vs. stock cluster

### Phase 3: Software Configuration

17. **Configure CAN Interfaces (Persistent)**
    ```bash
    sudo sh -c "echo 'socketcan' >> /etc/modules"
    sudo sh -c "echo 'can_dev' >> /etc/modules"
    
    # Create /etc/network/interfaces.d/can0
    cat > /etc/network/interfaces.d/can0 << 'EOF'
    iface can0 inet manual
        pre-up ip link set can0 type can bitrate 500000
        up ip link set can0 up
        down ip link set can0 down
    EOF
    
    # Create /etc/network/interfaces.d/can1
    cat > /etc/network/interfaces.d/can1 << 'EOF'
    iface can1 inet manual
        pre-up ip link set can1 type can bitrate 125000
        up ip link set can1 up
        down ip link set can1 down
    EOF
    ```

18. **Install Dashboard Software**
    - Clone/install your dashboard application (custom Python/GTK/Web)
    - Set up auto-start via systemd service
    - Configure touch calibration if needed
    - Test all CAN decoders (RPM, speed, temp, etc.)

---

## 7. Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Pi reboots on engine start | Insufficient capacitance | Add 4700µF capacitor |
| No CAN data on can0 | OBD-II not connected or wrong pins | Check pins 6/14 polarity, verify OBD cable |
| No CAN data on can1 | CEM splice not making contact | Check T-tap connection, try soldering |
| CAN errors (bus off) | Wrong bitrate or termination | Verify bus is 500k (can0) / 125k (can1) |
| Display no signal | HDMI cable loose or wrong resolution | Check cable, set `hdmi_mode=16` in config.txt |
| Display flickering | Power supply inadequate | Measure 5V under load, upgrade buck converter |
| Touch not working | USB cable not connected | Try different USB port, check USB VID/PID |
| Pi overheating | No ventilation in dashboard | Add heatsink + fan on Pi 5 GPIO 14/15 |
| Intermittent CAN data | Loose wire or bad ground | Check all screw terminals, clean ground point |

---

## 8. Pin Reference Cards (Quick Reference)

### PiCAN2 → CAN Bus

```
┌──────────────────────────────────────────┐
│  PiCAN2 Duo Screw Terminals              │
│                                          │
│  CAN0-H ──── OBD Pin 6 (White/Blue)     │
│  CAN0-L ──── OBD Pin 14 (Blue)          │
│  CAN1-H ──── CEM B2 (White/Green)       │
│  CAN1-L ──── CEM B1 (White/Violet)      │
│  GND    ──── Chassis Ground             │
└──────────────────────────────────────────┘
```

### Power Distribution

```
┌──────────────────────────────────────────┐
│  +12V (switched)                         │
│    ├─ CEM A Pin 3 (Red/Yellow)          │
│    └─ [5A Fuse] ─► Buck Converter       │
│                                          │
│  Buck Converter D24V50F5                 │
│    ├─ VIN+  ── +12V (fused)             │
│    ├─ VIN-  ── GND                       │
│    ├─ VOUT+ ── 5V (+ capacitor bank)    │
│    └─ VOUT- ── GND                       │
│                                          │
│  5V Distribution                         │
│    ├─ Pi 5 GPIO Pin 2 (+5V)             │
│    ├─ Display 5V input                  │
│    └─ PiCAN2 (via GPIO, already routed)  │
└──────────────────────────────────────────┘
```

### OBD-II Pin (Volvo V50)

```
┌─────┬────┬──────────────┬──────────────┐
│ Pin │ Fn │ Wire Color   │ Connection   │
├─────┼────┼──────────────┼──────────────┤
│  4  │GND │ Black        │ GND          │
│  5  │GND │ Black/Brown  │ GND          │
│  6  │CANH│ White/Blue   │ CAN0-H       │
│ 14  │CANL│ Blue         │ CAN0-L       │
│ 16  │+12V│ Red          │ Buck VIN+    │
│  7  │K-Ln│ Yellow       │ Not used     │
└─────┴────┴──────────────┴──────────────┘
```

---

## ⚠️ Safety Notes

1. **Always disconnect the battery** before working on vehicle wiring.
2. **Use fuses** on all power connections — a short on an unfused wire can cause a fire.
3. **Keep wires away from moving parts** — pedals, steering column, seat rails.
4. **Do NOT cut CAN bus wires** — use T-taps or solder splices to tap into existing wiring.
5. **Verify polarity twice** — reversing CAN-H and CAN-L will produce no data (no damage).
6. **Reversing 12V and GND** will destroy the buck converter and Pi instantly.
7. **Ground loops cause CAN errors** — use a single star ground point, not chassis ground for signals.
8. **Test at every step** — don't install everything and hope it works. Test each subsystem first on the bench.
