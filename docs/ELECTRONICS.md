# Volvo V50 Electronic Modules Reference

## Module Overview

| Module | Code | Bus | Location | Function |
|--------|------|-----|----------|----------|
| **CEM** | Central Electronic Module | High+Low CAN | Under dash, driver side | Gateway, body control |
| **ECM** | Engine Control Module | High CAN | Engine bay, firewall | Engine management |
| **TCM** | Transmission Control Module | High CAN | Under battery tray | Gearbox control |
| **DIM** | Driver Information Module | High CAN | Behind instrument cluster | Gauges, display, warnings |
| **ACC** | Automatic Climate Control | High CAN | Behind climate panel | Temperature, fan, distribution |
| **ABS** | Anti-lock Brake System | High CAN | Under hood, near strut | Brakes, stability |
| **SRS** | Supplemental Restraint System | High CAN | Under center console | Airbags |
| **DEM** | Differential Electronic Module | High CAN | Rear, near Haldex | AWD coupling |
| **DDM** | Driver Door Module | Low CAN | Driver door | Window, mirror, lock |
| **PDM** | Passenger Door Module | Low CAN | Passenger door | Window, mirror, lock |
| **SWM** | Steering Wheel Module | Low CAN | Behind steering wheel | Buttons, cruise |
| **IAM** | Integrated Audio Module | Low CAN | In dashboard | Radio, amplifier |
| **RTI** | Road Traffic Information | Low CAN | In dashboard | Navigation |
| **PSM** | Power Seat Module | Low CAN | Under seats | Memory seats |
| **SUM** | Suspension Module | High CAN | Near rear axle | 4C suspension |

## CEM (Central Electronic Module) — Detailed

The CEM is the **most important module** — it's the CAN gateway and body controller.

### V50 CEM Variants
- **Part numbers**: 30647356, 30647546, 30735804 (varies by year/options)
- **Software**: Must be programmed with VIDA for specific VIN
- **Immobilizer**: CEM stores immobilizer data — swapping requires VIDA reprogramming

### CEM Connectors
| Connector | Pins | Color | Function |
|-----------|------|-------|----------|
| A | 38 | Black | High-speed CAN, power, ignition |
| B | 52 | Gray | Low-speed CAN, lighting, wipers |
| C | 22 | Blue | Door modules, seats |
| D | 16 | Green | Immobilizer, key recognition |
| E | 10 | Red | Battery power (always-on) |

### CEM as CAN Gateway
The CEM translates between the two CAN buses:
- Messages from high-speed → low-speed: CEM strips proprietary headers
- Messages from low-speed → high-speed: CEM adds module addressing
- **To intercept ALL messages**: Must tap both buses or use OBD port (high-speed only)

### Key CEM Functions for Dashboard Project
- **Ignition status**: CAN message when key turns
- **Door status**: All 5 doors + hood + trunk
- **Light status**: Headlights, DRL, turn signals, fog
- **Wiper status**: Speed, interval, wash
- **Alarm status**: Locked/unlocked, trigger

## ECM (Engine Control Module) — B5244S

### ECU Details
- **Type**: Bosch ME9.1 or Denso (varies by year)
- **Part number**: Varies by market (EU/US)
- **Immobilizer**: Paired with CEM — cannot swap without reprogramming

### Sensors (B5244S)
| Sensor | Type | Location | Signal |
|--------|------|----------|--------|
| CKP | Inductive | Near crank pulley | Crank position |
| CMP | Hall | Cam cover | Cam position |
| MAF | Hot-wire | Air filter → throttle | Air mass |
| MAP | Piezo | Intake manifold | Boost/vacuum |
| ECT | NTC | Thermostat housing | Coolant temp |
| IAT | NTC | Intake manifold | Intake air temp |
| O2 upstream | Wideband | Exhaust manifold | Lambda |
| O2 downstream | Switching | After catalyst | Cat efficiency |
| Knock | Piezo | Block, cylinder 2-3 | Detonation |
| TP | Potentiometer | Throttle body | Throttle angle |
| APP | Dual pot | Accelerator pedal | Driver demand |

## ACC (Automatic Climate Control) — Detailed

### Module Variants
- **Manual (ECC)**: Rotary dials, no display → simpler CAN
- **Automatic (ACC)**: Digital display, auto mode → full CAN integration

### ACC Panel Pinout (Auto climate version)
| Pin | Wire Color | Function |
|-----|-----------|----------|
| 1 | Red/White | +12V ignition |
| 2 | Black | Ground |
| 3 | White/Blue | CAN-H (high-speed) |
| 4 | Blue | CAN-L (high-speed) |
| 5 | Yellow | K-line (diagnostics) |
| 6-8 | — | Unused/reserved |
| 9 | Green | Illumination (+) |
| 10 | Brown | Illumination (-) |

### Temperature Sensors (ACC)
| Sensor | Type | Location | Range |
|--------|------|----------|-------|
| Cabin temp | NTC 10kΩ | Behind glove box | -40°C to +85°C |
| Exterior temp | NTC 10kΩ | Behind front bumper, left | -40°C to +85°C |
| Evaporator temp | NTC 5kΩ | HVAC housing | -40°C to +30°C |
| Sun sensor | Photodiode | Top of dashboard | 0-1500 W/m² |
| Blend door L | Potentiometer | HVAC box, left | 0-100% |
| Blend door R | Potentiometer | HVAC box, right | 0-100% |
| Footwell temp | NTC 10kΩ | Under dash, left/right | -20°C to +60°C |

### ACC CAN Messages for Custom Integration
- All climate controls are on **High-Speed CAN** — accessible via OBD
- Temperature setpoints: CAN IDs 0x208/0x210
- Fan speed: CAN ID 0x218
- Mode selection: CAN ID 0x220
- For a custom display: Read these CAN IDs and display current settings

## DIM (Driver Information Module) — Detailed

### Display Types
- **Mono DIN**: Basic orange LCD, trip computer
- **Mono TFT**: Red/orange dot-matrix, more info
- **Color TFT** (later models): Color display with navigation

### DIM Connectors
| Connector | Pins | Function |
|-----------|------|----------|
| A | 26 | Power, illumination, warning lights |
| B | 32 | CAN-H, CAN-L, immobilizer LED |
| C | 16 | Trip computer buttons |

### Gauge Motor Type
- **Stepper motors**: VID29xx or similar (X27.589 compatible)
- Each gauge has its own stepper motor controlled by DIM via CAN
- **Speedometer**: CAN ID 0x308
- **Tachometer**: CAN ID 0x300
- **Fuel**: CAN ID 0x310
- **Temperature**: CAN ID 0x318

### For Custom Dashboard Project
1. Use a **Raspberry Pi with CAN HAT** to read all CAN IDs above
2. Display via HDMI LCD panel (7" or 10.1")
3. Use PyQt/GTK or custom OpenGL for gauge rendering
4. CAN data is available via OBD port — no need to remove original cluster initially