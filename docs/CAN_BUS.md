# Volvo V50 CAN Bus Protocol Reference

## CAN Bus Overview

The V50 uses **two CAN buses** connected through the CEM gateway:

### High-Speed CAN (Powertrain Bus)
- **Speed**: 500 kbit/s
- **Protocol**: ISO 15765-4 / SAE J2284
- **Connector**: OBD-II pins 6 (CAN-H) and 14 (CAN-L)
- **Location**: Twisted pair, white/green wires

### Low-Speed CAN (Body/Comfort Bus)
- **Speed**: 125 kbit/s
- **Protocol**: ISO 11519-2 (Volvo-specific)
- **Connector**: Not on OBD-II (gatewayed through CEM)
- **Location**: Separate twisted pair

## Known CAN Message IDs (V50 / P1 Platform)

⚠️ These are community-documented IDs, not from official VIDA. Always verify!

### Engine / Powertrain (High-Speed CAN)

| CAN ID | Direction | Description | Data Bytes |
|--------|-----------|-------------|------------|
| 0x0C0 | ECM → CEM | Engine RPM | Byte 0-1: RPM (÷ 4) |
| 0x0C8 | ECM → CEM | Engine coolant temperature | Byte 0: temp (°C - 40) |
| 0x0D0 | ECM → CEM | Throttle position | Byte 0: position % |
| 0x0D8 | ECM → CEM | Engine load / MAF | Byte 0-1: load value |
| 0x0E0 | ECM → CEM | Vehicle speed | Byte 0-1: speed (÷ 100 km/h) |
| 0x0F0 | ECM → CEM | Fuel level | Byte 1: fuel level % |
| 0x100 | ECM → CEM | Intake air temperature | Byte 0: temp (°C - 40) |
| 0x108 | ECM → CEM | Oil pressure / temperature | Byte 0: oil temp |
| 0x1A0 | TCM → CEM | Gear position indicator | Byte 0: gear (P=0,R=1,N=2,D=3,4,5) |
| 0x1A8 | TCM → CEM | Transmission temperature | Byte 0: temp (°C - 40) |

### Climate Control (High-Speed CAN)

| CAN ID | Direction | Description | Data Bytes |
|--------|-----------|-------------|------------|
| 0x200 | ACC → CEM | Climate panel button press | Byte 0: button ID |
| 0x208 | ACC → CEM | Temperature setpoint (driver) | Byte 0: temp (°C × 2) |
| 0x210 | ACC → CEM | Temperature setpoint (passenger) | Byte 0: temp (°C × 2) |
| 0x218 | ACC → CEM | Fan speed request | Byte 0: speed level (0-15) |
| 0x220 | ACC → CEM | Air distribution request | Byte 0: mode (0=auto, 1=face, 2=feet, 3=defrost) |
| 0x228 | ACC → CEM | A/C compressor request | Byte 0: 0=off, 1=on |
| 0x230 | CEM → DIM | Interior temperature | Byte 0: temp (°C × 2) |
| 0x238 | CEM → DIM | Exterior temperature | Byte 0: temp (°C - 40) |
| 0x240 | ACC → CEM | Recirculation request | Byte 0: 0=fresh, 1=recirc |
| 0x280 | CEM → ACC | Blend door position feedback | Byte 0: position % |

### Dashboard / DIM (High-Speed CAN)

| CAN ID | Direction | Description | Data Bytes |
|--------|-----------|-------------|------------|
| 0x300 | CEM → DIM | RPM for tachometer | Byte 0-1: RPM ÷ 4 |
| 0x308 | CEM → DIM | Speedometer value | Byte 0-1: speed ÷ 100 |
| 0x310 | CEM → DIM | Fuel gauge value | Byte 0: level % |
| 0x318 | CEM → DIM | Coolant temperature gauge | Byte 0: position % |
| 0x320 | CEM → DIM | Warning lights bitmap | Byte 0-3: bitmap |
| 0x328 | CEM → DIM | Odometer value | Byte 0-3: km |
| 0x340 | DIM → CEM | Trip computer button press | Byte 0: button ID |

### Body / Comfort (Low-Speed CAN via CEM gateway)

| CAN ID | Direction | Description |
|--------|-----------|-------------|
| 0x400 | SWM → CEM | Steering wheel button |
| 0x410 | DDM → CEM | Driver door status |
| 0x418 | PDM → CEM | Passenger door status |
| 0x420 | CEM → DIM | Exterior lighting status |
| 0x430 | CEM → SWM | Cruise control data |
| 0x500 | IAM → CEM | Audio system status |
| 0x510 | CEM → IAM | Audio commands |

## OBD-II Access

### Standard OBD-II PIDs (ISO 15031)

| PID | Description | Formula |
|-----|-------------|---------|
| 0x0C | Engine RPM | (A × 256 + B) ÷ 4 |
| 0x0D | Vehicle Speed | A km/h |
| 0x05 | Coolant Temperature | A - 40 °C |
| 0x0F | Intake Air Temperature | A - 40 °C |
| 0x2F | Fuel Tank Level | (A ÷ 255) × 100 % |
| 0x04 | Engine Load | (A ÷ 255) × 100 % |
| 0x10 | MAF | (A × 256 + B) ÷ 100 g/s |
| 0x11 | Throttle Position | (A ÷ 255) × 100 % |

### Volvo-Specific OBD Mode 22 (Proprietary)

⚠️ Community-documented, not official. Verify with VIDA/DICE.

| PID | Description | Notes |
|-----|-------------|-------|
| 0x220104 | Oil temperature | Needs verification |
| 0x220105 | Boost pressure (turbo models) | 2.4L NA may not have |
| 0x22010C | Transmission fluid temp | From TCM |
| 0x2201| ACC cabin temp sensor | From ACC module |

## CAN Sniffing Setup

### Hardware Required
1. **CAN bus interface**: PiCAN2 Duo (dual CAN) or USBtin
2. **Raspberry Pi** 4/5 with CAN HAT
3. **DB9-to-OBD2 adapter** for OBD port access
4. **Wiring tap** for low-speed CAN ( splice into white/blue CAN wires behind CEM)

### Software Stack
```bash
# Enable CAN on Raspberry Pi
sudo ip link set can0 up type can bitrate 500000
sudo ip link set can1 up type can bitrate 125000

# Sniff all messages
candump can0
candump can1

# Log to file with timestamps
candump -l can0
```

### Python CAN Example
```python
import can
bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)
for msg in bus:
    print(f"ID: 0x{msg.arbitration_id:03X} Data: {msg.data.hex()} DLC: {msg.dlc}")
```