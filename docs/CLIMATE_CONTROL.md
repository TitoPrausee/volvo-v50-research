# Climate Control — ACC Module Integration

## Goal: Custom Digital Climate Display & Control

Build a replacement display for the Volvo V50 ACC (Automatic Climate Control) that can:
1. **Display** current temperatures (cabin, exterior, evaporator, setpoints)
2. **Control** HVAC settings (temp, fan speed, air distribution, A/C, recirculation)
3. **Integrate** with a larger infotainment/CarPlay system

## ACC Architecture

```
┌──────────────────────────────────────────────────┐
│                  ACC Module                        │
│  (Behind climate panel, on high-speed CAN)        │
│                                                    │
│  Inputs:                      Outputs:             │
│  - Rotation dials (temp L/R)  - Blend door motors │
│  - Button presses             - Fan speed PWM       │
│  - Auto/Off/Econ buttons      - A/C compressor     │
│  - Cabin temp sensor NTC      - Recirculation flap │ │
│  - Exterior temp sensor NTC   - Air distribution   │
│  - Sun sensor photodiode       - Seat heaters       │
│  - Evaporator temp NTC        - Heated windshield  │
│                                                    │
│  CAN: 0x200–0x280 (climate messages)               │
└──────────────────────────────────────────────────┘
```

## Reading Climate Data via CAN

### Temperature Display

| CAN ID | Data | Formula | Description |
|--------|------|---------|-------------|
| 0x208 | Byte 0 | value ÷ 2 | Driver setpoint (°C) |
| 0x210 | Byte 0 | value ÷ 2 | Passenger setpoint (°C) |
| 0x230 | Byte 0 | value ÷ 2 | Cabin temperature (°C) |
| 0x238 | Byte 0 | value + 40 | 40 → 0°C, 88 → 48°C | Exterior temperature |
| 0x200 | Byte 1 | — | Current mode (0-15) |
| 0x218 | Byte 0 | — | Fan speed level (0-15, 0=off, 15=max) |
| 0x228 | Byte 0 | — | A/C compressor: 0=off, 1=on |
| 0x240 | Byte 0 | — | Recirculation: 0=fresh, 1=recirc |
| 0x220 | Byte 0 | — | Distribution: 0=auto, 1=face, 2=feet, 3=bi-level, 4=defrost |

### Temperature Sensor Reading (NTC)

The cabin and exterior sensors are **NTC thermistors** (10kΩ @ 25°C):

| Resistance | Approx. Temp |
|-----------|--------------|
| 100kΩ | -20°C |
| 47kΩ | -10°C |
| 23kΩ | 0°C |
| 10kΩ | 25°C (reference) |
| 5kΩ | 40°C |
| 2.5kΩ | 60°C |
| 1.3kΩ | 80°C |

**Formula**: `T = 1 / (1/T₀ + (1/B) × ln(R/R₀))` where T₀=298.15K, R₀=10kΩ, B≈3435

## Controlling Climate via CAN

### Sending Climate Commands

⚠️ **Critical**: The ACC module expects specific message timing and formats. Incorrect messages can cause DTCs (Diagnostic Trouble Codes).

| CAN ID | Byte 0 | Purpose | Notes |
|--------|--------|---------|-------|
| 0x208 | temp×2 | Set driver temp | Range: 0x30 (16°C) to 0x50 (32°C) |
| 0x210 | temp×2 | Set passenger temp | Same range |
| 0x218 | level | Set fan speed | 0x00=off, 0x01-0x0F=speed 1-15 |
| 0x220 | mode | Set air distribution | 0=auto, 1=face, 2=feet, 3=bi, 4=defrost |
| 0x228 | state | A/C compressor | 0x00=off, 0x01=on |
| 0x240 | state | Recirculation | 0x00=fresh, 0x01=recirc |
| 0x200 | btn | Button press | See button ID table below |

### Button IDs (CAN ID 0x200)
| Byte | Button |
|------|--------|
| 0x01 | Auto |
| 0x02 | A/C on/off |
| 0x03 | Recirculation |
| 0x04 | Fan up |
| 0x05 | Fan down |
| 0x06 | Temp driver up |
| 0x07 | Temp driver down |
| 0x08 | Temp passenger up |
| 0x09 | Temp passenger down |
| 0x0A | Air distribution face |
| 0x0B | Air distribution feet |
| 0x0C | Air distribution defrost |
| 0x0D | Heated rear window |
| 0x0E | Heated windshield |
| 0x0F | Econ mode |
| 0x10 | Off |

### Recommended Approach for Custom Control

1. **Read-only first**: Sniff CAN bus for 1-2 weeks, document all messages
2. **Playback testing**: Replay captured messages to verify control
3. **Gradual override**: Start with temperature display only, then add control
4. **Safety**: Always maintain ability to fall back to original ACC panel

## Raspberry Pi Climate Display

### Hardware List
| Component | Purpose | Est. Cost |
|-----------|---------|------------|
| Raspberry Pi 4/5 | Main controller | €40-80 |
| PiCAN2 Duo HAT | Dual CAN interface | €35 |
| 7" IPS HDMI LCD | Display touch panel | €30-50 |
| 5V 3A Step-down | Car 12V → 5V | €8 |
| OBD2 to DB9 adapter | CAN access | €5 |
| DS3231 RTC | Time keeping (car has no GPS time) | €3 |
| **Total** | | **€120-180** |

### Software Architecture
```
┌─────────────────────────────────────────────────┐
│                Qt/QML Dashboard                  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│  │Climate  │ │ Engine  │ │  Audio  │           │
│  │Display  │ │ Gauges  │ │ Control │           │
│  └────┬────┘ └────┬────┘ └────┬────┘           │
│       │            │           │                  │
│  ┌────▼────────────▼───────────▼────┐           │
│  │        CAN Message Bus           │           │
│  │    (python-can + SQLite)         │           │
│  └────────────┬──────────────────────┘           │
│               │                                   │
│  ┌────────────▼──────────────────────┐           │
│  │   SocketCAN (Linux kernel)        │           │
│  │   can0: High-speed (500kbps)      │           │
│  │   can1: Low-speed (125kbps)       │           │
│  └────────────────────────────────────┘           │
│               │                                   │
│          PiCAN2 Duo HAT                          │
│               │                                   │
│          ┌────┴─────┐                             │
│          │  Volvo    │                             │
│          │  V50 CAN  │                             │
│          └──────────┘                              │
└─────────────────────────────────────────────────┘
```