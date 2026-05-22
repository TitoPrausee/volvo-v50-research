# Raspberry Pi Integration Guide

## Hardware Setup

### Recommended: Raspberry Pi 5 + PiCAN2 Duo

| Component | Specification | Purpose |
|-----------|--------------|---------|
| Raspberry Pi 5 | 4GB or 8GB | Main computer |
| PiCAN2 Duo | Dual CAN HAT | Both high+low speed CAN |
| 7" IPS LCD | 1024×600, HDMI | Dashboard display |
| 5V 3A Buck Converter | 12V → 5V, 3A | Power supply from car |
| DS3231 RTC | I2C real-time clock | Time keeping (car has no GPS) |
| USB GPS (optional) | U-blox 7/8 | Navigation data |
| Bluetooth dongle (optional) | CSR 8510 | OBD2 adapter, CarPlay audio |

### Power Supply Design

```
Car Battery (12V) ──┬── Ignition +12V (switched)
                     │
              ┌──────▼──────┐
              │  Buck Conv.  │
              │  12V → 5V    │
              │  3A output   │
              └──────┬──────┘
                     │ 5V 3A
              ┌──────▼──────┐
              │  Raspberry   │
              │  Pi 5        │
              │  + PiCAN2    │
              │  + SSD       │
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │  7" LCD      │
              │  Display     │
              └──────────────┘

IMPORTANT: Add a 2000µF capacitor across 5V to handle
           crank voltage dips during engine start!
```

### CAN Bus Wiring

```
PiCAN2 Duo HAT:
┌─────────────────┐
│  CAN0 (High)     │── OBD-II Pin 6 (CAN-H) ── Twisted pair
│  CAN0 (Low)      │── OBD-II Pin 14 (CAN-L) ── Twisted pair
│                  │
│  CAN1 (High)     │── CEM splice (White/Violet)
│  CAN1 (Low)      │── CEM splice (White/Green)
│                  │
│  GND             │── Chassis ground
│  +5V             │── From Pi GPIO
└─────────────────┘

DO NOT mix high-speed and low-speed CAN wires!
Use 120Ω termination resistors on each bus.
```

## Software Setup

### 1. OS and Base Configuration

```bash
# Raspberry Pi OS 64-bit (Bookworm)
sudo apt update && sudo apt upgrade -y
sudo apt install -y can-utils python3-can python3-pip sqlite3

# Enable CAN kernel modules
sudo sh -c "echo 'socketcan' >> /etc/modules"
sudo sh -c "echo 'can_dev' >> /etc/modules"

# For PiCAN2 Duo: Enable SPI
sudo raspi-config nonint do_spi 0
```

### 2. CAN Interface Setup

```bash
# Create CAN startup script
cat > /etc/network/interfaces.d/can0 << 'EOF'
iface can0 inet manual
    pre-up ip link set can0 type can bitrate 500000
    up ip link set can0 up
    down ip link set can0 down
EOF

cat > /etc/network/interfaces.d/can1 << 'EOF'
iface can1 inet manual
    pre-up ip link set can1 type can bitrate 125000
    up ip link set can1 up
    down ip link set can1 down
EOF
```

### 3. Python CAN Library

```python
# volvo_can.py — Volvo V50 CAN message decoder
import can
import time
import sqlite3
from datetime import datetime

DB_PATH = "/opt/volvo/data/can_log.db"

# CAN message decoders for V50
DECODERS = {
    0x0C0: {"name": "Engine RPM", "bytes": 2, "decode": lambda d: (d[0]*256+d[1])/4, "unit": "rpm"},
    0x0C8: {"name": "Coolant Temp", "bytes": 1, "decode": lambda d: d[0]-40, "unit": "°C"},
    0x0D0: {"name": "Throttle Pos", "bytes": 1, "decode": lambda d: d[0]/2.55, "unit": "%"},
    0x0E0: {"name": "Vehicle Speed", "bytes": 2, "decode": lambda d: (d[0]*256+d[1])/100, "unit": "km/h"},
    0x208: {"name": "Temp Set Driver", "bytes": 1, "decode": lambda d: d[0]/2, "unit": "°C"},
    0x210: {"name": "Temp Set Passenger", "bytes": 1, "decode": lambda d: d[0]/2, "unit": "°C"},
    0x218: {"name": "Fan Speed", "bytes": 1, "decode": lambda d: d[0], "unit": "level"},
    0x228: {"name": "A/C Compressor", "bytes": 1, "decode": lambda d: "ON" if d[0] else "OFF", "unit": ""},
    0x230: {"name": "Cabin Temp", "bytes": 1, "decode": lambda d: d[0]/2, "unit": "°C"},
    0x238: {"name": "Exterior Temp", "bytes": 1, "decode": lambda d: d[0]-40, "unit": "°C"},
    0x300: {"name": "Tachometer", "bytes": 2, "decode": lambda d: (d[0]*256+d[1])/4, "unit": "rpm"},
    0x308: {"name": "Speedometer", "bytes": 2, "decode": lambda d: (d[0]*256+d[1])/100, "unit": "km/h"},
    0x320: {"name": "Warning Lights", "bytes": 4, "decode": lambda d: f"0x{d[0]:02x}{d[1]:02x}{d[2]:02x}{d[3]:02x}", "unit": "bitmap"},
}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS can_messages (
        timestamp REAL, can_id INTEGER, name TEXT, value TEXT, unit TEXT
    )""")
    conn.commit()
    return conn

def main():
    conn = init_db()
    bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)
    print("Listening on CAN0 (high-speed 500kbps)...")
    
    while True:
        msg = bus.recv(timeout=1)
        if msg and msg.arbitration_id in DECODERS:
            decoder = DECODERS[msg.arbitration_id]
            try:
                value = decoder["decode"](msg.data)
                timestamp = time.time()
                print(f"[{datetime.now():%H:%M:%S}] {decoder['name']}: {value} {decoder['unit']}")
                conn.execute("INSERT INTO can_messages VALUES (?,?,?,?,?)",
                    (timestamp, msg.arbitration_id, decoder["name"], str(value), decoder["unit"]))
                conn.commit()
            except Exception as e:
                pass
                
if __name__ == "__main__":
    main()
```

### 4. Auto-Start on Boot

```bash
# /etc/systemd/system/volvo-can.service
cat > /etc/systemd/system/volvo-can.service << 'EOF'
[Unit]
Description=Volvo V50 CAN Bus Monitor
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/usr/bin/python3 /opt/volvo/volvo_can.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable volvo-can
sudo systemctl start volvo-can
```