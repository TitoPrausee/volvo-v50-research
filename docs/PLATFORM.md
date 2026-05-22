# Volvo P1 Platform Architecture

## Overview

The **P1 platform** (internally Ford C1) was co-developed by Volvo, Ford, and Mazda. It underpins:

- **Volvo**: S40 (2004–2012), V50 (2004–2012), C30 (2006–2013), C70 (2006–2013)
- **Ford**: Focus Mk2 (2004–2011), Kuga (2008–2012)
- **Mazda**: Mazda 3 BK (2003–2008), Mazda 5 (2005–2010)

## Key Architecture Details

### Electronic Architecture

The P1 platform uses a **distributed electronic architecture** with multiple control modules communicating over CAN bus:

```
                    ┌──────────────┐
                    │   CEM (Central│
                    │  Electronic   │
                    │   Module)     │
                    │  ↕ High-Speed │
                    │    CAN 500kbps│
                    └──────┬───────┘
                           │
        ┌──────────┬───────┼────────┬──────────┐
        │          │       │        │          │
   ┌────▼───┐ ┌───▼──┐ ┌──▼───┐ ┌──▼───┐ ┌───▼────┐
   │  ECM   │ │  TCM │ │  DIM │ │  ACC  │ │  DEM   │
   │(Engine)│ │(Trans│ │(Dash │ │(Climate│ │(AWD/  │
   │        │ │ miss.)│ │ Inst)│ │ Ctrl) │ │ Haldex)│
   └────────┘ └──────┘ └──────┘ └──────┘ └────────┘
        │
   ┌────▼───┐ ┌───────┐ ┌────────┐
   │  SRS   │ │  ABS  │ │  SUM   │
   │(Airbag)│ │(Brake)│ │(Suspens│
   └────────┘ └───────┘ └────────┘

   Low-Speed CAN (125 kbps):
   CEM ←→ Doors (DDM/PDM) ←→ Seats (PSM) ←→ Steering (SWM)
   CEM ←→ Audio (IAM/AUH) ←→ Nav (RTI) ←→ Phone (PHM)
```

### CAN Bus Layout

| Bus | Speed | Modules | Purpose |
|-----|-------|---------|---------|
| **High-Speed CAN** | 500 kbit/s | CEM, ECM, TCM, DIM, ACC, ABS, SRS, DEM, BCM | Powertrain, safety, climate |
| **Low-Speed CAN** | 125 kbit/s | CEM, DDM, PDM, SWM, PSM, IAM, RTI | Body, comfort, infotainment |

- **CEM** (Central Electronic Module) is the gateway between both buses
- CEM handles message translation between high-speed and low-speed CAN
- Located under the dashboard on the driver's side

### Module Communication

| From | To | Bus | Function |
|------|----|-----|----------|
| ECM | CEM | High | Engine RPM, temp, load, fuel |
| TCM | CEM | High | Gear position, mode, torque request |
| ACC | CEM | High | Climate requests, temperature data |
| DIM | CEM | High | Display data, warnings, gauges |
| ABS | CEM | High | Wheel speed, brake pressure |
| CEM | DIM | High | Instrument cluster data |
| CEM | IAM | Low | Audio commands |
| SWM | CEM | Low | Steering wheel button presses |

## Wiring Architecture

- **Fuse box**: Located under the dashboard (driver's side) and in the engine compartment
- **Ground points**: Multiple — body, engine, transmission
- **Power distribution**: CEM distributes switched power to modules
- **Signal wires**: Twisted pair for CAN, single wire for LIN

## Shared Components with Ford Focus Mk2

Many modules are shared or mechanically similar:
- ABS/ESP module (Ford/Continental TEVES)
- ECM (Bosch/Denso variants)
- Power steering (TRW/Eaton)
- Some sensor types (MAP, MAF, CKP, CMP)

⚠️ **However**, Volvo-specific modules (CEM, DIM, ACC, RTI) have different firmware and CAN message formats than Ford equivalents.