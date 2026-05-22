# Connectors & Pinouts Reference

## Under-Dashboard Connectors (Driver Side)

### CEM (Central Electronic Module) — Under Dashboard

#### Connector A (38-pin, Black) — High-Speed CAN + Power
| Pin | Wire Color | Function | Notes |
|-----|-----------|----------|-------|
| 1 | Red | +12V battery (always) | 30A fuse |
| 2 | Red | +12V battery (always) | 30A fuse |
| 3 | Red/Yellow | +12V ignition (position II) | Switched |
| 4 | Black | Ground | Chassis |
| 5 | Black | Ground | Chassis |
| 6 | — | — | — |
| 7 | White/Blue | CAN-H high-speed | 500kbps |
| 8 | Blue | CAN-L high-speed | 500kbps |
| 9 | Yellow | K-line (diagnostics) | OBD-II pin 7 |
| 10-15 | — | Power outputs | Various |
| 16 | Purple | Ignition sense | Key position |
| 17 | Green | Vehicle speed | From ABS |
| 18-20 | — | — | — |
| 21 | Orange | A/C compressor relay | Switched ground |
| 22-38 | — | Various outputs | Lights, wipers, etc. |

#### Connector B (52-pin, Gray) — Low-Speed CAN + Body

| Pin | Wire Color | Function | Notes |
|-----|-----------|----------|-------|
| 1 | White/Violet | CAN-L low-speed | 125kbps |
| 2 | White/Green | CAN-H low-speed | 125kbps |
| 3 | Green/Yellow | Fuel level | From tank sender |
| 4 | — | — | — |
| 5 | Brown/White | Trunk release | Ground to activate |
| 6 | Blue/White | Door lock driver | Pulse ground |
| 7 | Blue/Red | Door lock passenger | Pulse ground |
| 8 | Black/White | Window up driver | Ground to activate |
| 9 | Black/Red | Window down driver | Ground to activate |
| 10-15 | — | Door modules, mirrors | — |
| 16 | Purple/Yellow | SRS warning | — |
| 17-25 | — | Light outputs, indicators | — |
| 26-30 | — | Wiper controls | — |
| 31-52 | — | Power, ground, misc | — |

### OBD-II Diagnostic Port (Under Dash, Driver Side)

| Pin | Function | Wire Color |
|-----|----------|------------|
| 1 | — | Not used (Volvo specific) |
| 2 | J1850 PWM | Not used |
| 3 | — | Not used |
| 4 | Chassis Ground | Black |
| 5 | Signal Ground | Black/Brown |
| 6 | CAN-H (high-speed) | White/Blue |
| 7 | K-Line (ISO 9141) | Yellow |
| 8 | — | Not used |
| 9 | — | Not used |
| 10 | J1850 PWM | Not used |
| 11 | — | Not used |
| 12 | — | Not used |
| 13 | — | Not used |
| 14 | CAN-L (high-speed) | Blue |
| 15 | L-Line (ISO 9141) | Not used |
| 16 | +12V battery | Red |
| 2-20 | — | Not used |

**Key access**: Pins 6 (CAN-H) and 14 (CAN-L) give you direct access to the High-Speed CAN bus.

## ACC (Climate Control) Panel Connector

### Auto Climate Version (ECC) — 10-pin connector

| Pin | Wire Color | Function | Signal |
|-----|-----------|----------|--------|
| 1 | Red/White | +12V ignition | Switched power |
| 2 | Black | Ground | Chassis |
| 3 | White/Blue | CAN-H | High-speed CAN |
| 4 | Blue | CAN-L | High-speed CAN |
| 5 | Yellow | K-line | Diagnostics |
| 6 | — | — | — |
| 7 | — | — | — |
| 8 | — | — | — |
| 9 | Green | Illumination (+) | Dash dimmer |
| 10 | Brown | Illumination (-) | Ground |

### Temperature Sensor Connectors

| Sensor | Connector | Pins | Wire Colors | Location |
|--------|-----------|------|-------------|----------|
| Cabin temp | 2-pin | 2 | Brown/White, Brown | Behind glove box |
| Exterior temp | 2-pin | 2 | Blue/White, Blue | Behind front bumper, left |
| Evaporator temp | 2-pin | 2 | Grey/White, Grey | HVAC housing, top |
| Sun sensor | 3-pin | 3 | Red, Black, Green | Top of dashboard |

## Radio/Audio Connectors

### IAM (Integrated Audio Module) — Behind climate panel

| Connector | Pins | Color | Function |
|-----------|------|-------|----------|
| A | 20 | Black | Power, CAN, speaker outputs L |
| B | 20 | Brown | Speaker outputs R |
| C | 16 | Gray | Antenna, aux, phone |
| D | 8 | Blue | CD changer (if equipped) |
| E | 10 | Green | Amplifier (if Premium Sound) |

### Speaker Wire Colors (Behind IAM)

| Speaker | + Wire | - Wire | Polarity |
|---------|--------|--------|----------|
| Front left tweeter | Orange/White | Orange/White stripe | Standard |
| Front left mid | Green/White | Green/White stripe | Standard |
| Front right tweeter | Orange/Black | Orange/Black stripe | Standard |
| Front right mid | Green/Black | Green/Black stripe | Standard |
| Rear left | Blue/White | Blue/White stripe | Standard |
| Rear right | Blue/Black | Blue/Black stripe | Standard |

⚠️ **Stripe = negative/ground** on Volvo wiring harnesses.

## Key Fob & Immobilizer

### Key Recognition (CEM pin D connector)

| Pin | Function |
|-----|----------|
| D1 | Antenna ring (+) |
| D2 | Antenna ring (-) |
| D3 | Transponder signal |
| D4 | Key ID data |
| D5 | Ground |
| D6 | +5V reference |

⚠️ **Do NOT modify immobilizer wiring!** CEM and key are paired. Losing synchronization = car won't start.