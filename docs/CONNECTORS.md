# Volvo V50 P1 Platform — Connector & Pinout Reference

> Cross-referenced from multiple sources. ALL pinout data needs VIDA verification.  
> Last updated: 2026-05-27

## CEM (Central Electronic Module) — P1 Platform

### Location
Behind glovebox, driver's side under dashboard

### Variants
- **CEM-Low**: Base models (fewer options, fewer connectors)
- **CEM-High**: Models with more features (sunroof, premium audio, etc.)
- Part numbers: 30647356, 30647546, 30735804, 30758460, 30758461, 31268840

### Connector Overview — Source A (existing docs)

| Connector | Pins | Color | Function |
|-----------|------|-------|----------|
| A | 38 | Black | High-speed CAN, power, ignition |
| B | 52 | Gray | Low-speed CAN, lighting, wipers |
| C | 22 | Blue | Door modules, seats |
| D | 16 | Green | Immobilizer, key recognition |
| E | 10 | Red | Battery power (always-on) |

### Connector Overview — Source B (model knowledge)

| Connector | Pins | Function |
|-----------|------|----------|
| A | 54 | Power, Ground, LIN bus, CAN bus |
| B | 26 | Lighting & signaling |
| C | 40 | Wiper, washer, horn, HVAC |
| D | 20 | Door modules, interior lighting (LIN bus) |
| E | 16 | Immobilizer, keyless entry |

### ⚠️ DISCREPANCY
Pin counts differ significantly between sources. Likely explanation:
- Pre-2008 (early V50) uses different CEM revision with different connector layout
- CEM-Low vs CEM-High have different pin counts
- Some sources count connector + sub-connectors differently

**Resolution needed: Physical inspection of actual CEM in the car**

### CEM Connector A — Power & CAN (estimated)

| Pin | Function | Wire Color (typical) | Signal Type |
|-----|----------|---------------------|-------------|
| A1 | +12V Battery (terminal 30) | Red/White | Power (always-on) |
| A2 | +12V Ignition (terminal 15) | Yellow | Power (switched) |
| A3-A6 | Ground (terminal 31) | Brown/Black | Ground |
| A7 | High-Speed CAN-H | White | CAN |
| A8 | High-Speed CAN-L | Blue/White | CAN |
| A9 | Low-Speed CAN-H (body bus) | White/Green | CAN |
| A10 | Low-Speed CAN-L (body bus) | Blue | CAN |
| A11 | LIN Bus 1 | Violet | LIN |
| A12 | LIN Bus 2 | Violet/Yellow | LIN |

### CEM Connector D — Door Modules & LIN

| Pin | Function | Signal Type |
|-----|----------|-------------|
| D1-D4 | LIN to DDM/PDM | LIN |
| D5-D6 | Interior lighting (dome/courtesy) | Power |
| D7-D8 | Sunroof control (if equipped) | Power |

### CEM Connector E — Immobilizer & Keyless

| Pin | Function | Signal Type |
|-----|----------|-------------|
| E1-E2 | Immobilizer antenna ring | RF |
| E3-E4 | Keyless entry receiver | RF |
| E5 | Siren control | Digital |
| E6 | Hood switch (alarm) | Digital |

## OBD-II Port Pinout — P1 Platform

```
     ┌──────────────────────┐
     │  1  2  3  4  5  6  7  8  │
     │  9 10 11 12 13 14 15 16  │
     └──────────────────────┘

  Pin 1:  — (manufacturer specific)
  Pin 2:  J1850 Bus+ (not used on Volvo CAN)
  Pin 3:  ⚠️ Low-Speed CAN-H (not on all models)
  Pin 4:  Chassis Ground
  Pin 5:  Signal Ground
  Pin 6:  High-Speed CAN-H ✅
  Pin 7:  K-Line (ISO 9141, diagnostics)
  Pin 8:  — (manufacturer specific)
  Pin 9:  — (manufacturer specific)
  Pin 10: — (manufacturer specific)
  Pin 11: ⚠️ Low-Speed CAN-L (not on all models)
  Pin 12: — (manufacturer specific)
  Pin 13: — (manufacturer specific)
  Pin 14: High-Speed CAN-L ✅
  Pin 15: L-Line (ISO 9141)
  Pin 16: +12V Battery (always on)
```

### CAN Voltage Verification
```
Key OFF:  CAN-H ≈ 2.5V  |  CAN-L ≈ 2.5V  (recessive)
Key ON:   CAN-H ≈ 3.5V  |  CAN-L ≈ 1.5V  (dominant, active)
```

## ACC (Automatic Climate Control) — Connector

### ACC Panel Pinout (Auto climate version)

| Pin | Wire Color | Function | Signal Type |
|-----|-----------|----------|-------------|
| 1 | Red/White | +12V ignition | Power |
| 2 | Black | Ground | Ground |
| 3 | White/Blue | CAN-H (high-speed) | CAN |
| 4 | Blue | CAN-L (high-speed) | CAN |
| 5 | Yellow | K-Line (diagnostics) | K-Line |
| 6-8 | — | Unused/reserved | — |
| 9 | Green | Illumination (+) | Power |
| 10 | Brown | Illumination (-) | Ground |

### ACC Temperature Sensors

| Sensor | Type | Location | Resistance | Range |
|--------|------|----------|------------|-------|
| Cabin temp | NTC 10kΩ | Behind glove box | 10kΩ @ 25°C | -40°C to +85°C |
| Exterior temp | NTC 10kΩ | Behind front bumper, left | 10kΩ @ 25°C | -40°C to +85°C |
| Evaporator | NTC 5kΩ | HVAC housing | 5kΩ @ 25°C | -40°C to +30°C |
| Sun sensor | Photodiode | Top of dashboard | — | 0-1500 W/m² |
| Blend door L | Potentiometer | HVAC box, left | — | 0-100% |
| Blend door R | Potentiometer | HVAC box, right | — | 0-100% |
| Footwell temp | NTC 10kΩ | Under dash L/R | 10kΩ @ 25°C | -20°C to +60°C |

## DIM (Driver Information Module) — Connectors

### Display Variants
- **Mono DIN**: Basic orange LCD, trip computer
- **Mono TFT**: Red/orange dot-matrix, more info
- **Color TFT**: Color display, navigation (later models only)

### DIM Connectors

| Connector | Pins | Function |
|-----------|------|----------|
| A | 26 | Power, illumination, warning lights |
| B | 32 | CAN-H, CAN-L, immobilizer LED |
| C | 16 | Trip computer buttons |

### Gauge Stepper Motors
- Type: VID29xx / X27.589 compatible
- Each gauge has its own stepper motor
- Controlled by DIM via CAN bus (not directly by stepper driver)
- Speedo: CAN 0x308, Tacho: CAN 0x300, Fuel: CAN 0x310, Temp: CAN 0x318

## ECM (Engine Control Module) — B5244S

### ECU Type
- **Bosch ME9.1** (early models) or **Denso** (later models)
- Paired with CEM — cannot swap without VIDA reprogramming
- Immobilizer data stored in both CEM and ECM

### Primary Sensors

| Sensor | Type | Location | Signal |
|--------|------|----------|--------|
| CKP | Inductive | Near crank pulley | Crank position/rpm |
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

## Fuse Box — V50 (Under Dash, Driver's Side)

⚠️ Requires VIDA verification for specific fuse assignments. General layout:

| Fuse # | Amp | Circuit (typical P1) |
|--------|-----|---------------------|
| F1 | 15A | CEM power (terminal 30) |
| F2 | 10A | CEM ignition (terminal 15) |
| F3 | 5A | DIM power |
| F4 | 10A | ECM power |
| F5 | 15A | ACC / Climate control |
| F6 | 20A | Blower motor |
| F7 | 15A | Audio system (IAM) |
| F8 | 10A | OBD diagnostic |
| — | — | (Varies by model/options) |

## NTC Thermistor Reference Table

For 10kΩ NTC sensors (cabin, exterior, evaporator):

| Temp (°C) | Resistance (Ω) |
|-----------|---------------|
| -20 | 96,400 |
| -10 | 55,300 |
| 0 | 32,600 |
| 10 | 19,900 |
| 20 | 12,500 |
| 25 | 10,000 |
| 30 | 8,060 |
| 40 | 5,330 |
| 50 | 3,600 |
| 60 | 2,490 |
| 80 | 1,260 |
| 100 | 680 |