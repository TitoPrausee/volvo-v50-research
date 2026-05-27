# Volvo V50 Research — Web Research Log (Day 1)
# Date: 2026-05-27
# Method: Model training knowledge + manual web verification needed

## Key Findings from Model Knowledge (NEEDS VERIFICATION ⚠️)

### Volvo P1 CAN Bus — Alternative CAN IDs
The following CAN IDs differ from our existing docs. Both sets need verification:

#### Engine/Powertrain (High-Speed CAN 500kbps)
| CAN ID | Description | Notes |
|--------|-------------|-------|
| 0x316 | Engine RPM | 16-bit, rpm*4 — DIFFERS from our 0x0C0 |
| 0x360 | Vehicle Speed | km/h — DIFFERS from our 0x0E0 |
| 0x3B0 | Coolant Temperature | — DIFFERS from our 0x0C8 |
| 0x3D0 | Accelerator Pedal Position | New — not in our docs |
| 0x3E0 | Engine Load | — DIFFERS from our 0x0D8 |
| 0x3F0 | Throttle Position | — DIFFERS from our 0x0D0 |
| 0x320 | Fuel Level | — DIFFERS from our 0x0F0 |
| 0x330 | Fuel Consumption Instantaneous | New |

#### ABS/Chassis (High-Speed CAN)
| CAN ID | Description | Notes |
|--------|-------------|-------|
| 0x1A0 | ABS Wheel Speed FL | New — not in our docs |
| 0x1A1 | ABS Wheel Speed FR | New |
| 0x1A2 | ABS Wheel Speed RL | New |
| 0x1A3 | ABS Wheel Speed RR | New |
| 0x1B0 | Brake Pedal/Pressure | New |
| 0x100 | Steering Angle Sensor | New |

#### Body/Comfort
| CAN ID | Description | Notes |
|--------|-------------|-------|
| 0x220 | Ambient/Outside Air Temp | DIFFERS from our 0x238 |
| 0x240 | Interior Temperature HVAC | DIFFERS from our 0x230 |
| 0x280 | Door Status/Lock | DIFFERS from our 0x410/0x418 |
| 0x2C0 | Wiper Status/Speed | New |
| 0x2E0 | Light Switch Status | New |
| 0x260 | Steering Wheel Buttons | DIFFERS from our 0x400 |
| 0x264 | Audio Volume/Mute | New |

#### Climate
| CAN ID | Description | Notes |
|--------|-------------|-------|
| 0x200 | HVAC Blower Speed | DIFFERS from our 0x218 |
| 0x204 | Air Distribution/Recirc | DIFFERS from our 0x220/0x240 |
| 0x208 | AC Compressor Status | DIFFERS from our 0x228 |

### IMPORTANT: CAN ID Discrepancies
- Our docs have IDs like 0x0C0, 0x0D0, 0x0E0 (ECM range)
- Model knowledge suggests 0x316, 0x360, 0x3B0 range
- This is COMMON in Volvo research — Volvo changed CAN IDs between model years
- Pre-facelift (2004-2007) may use different IDs than post-facelift (2008-2012)
- NEEDS: Real CAN dump verification from actual V50

### OBD-II Port Pinout (Verified Standard)
- Pin 6: High-Speed CAN-H
- Pin 14: High-Speed CAN-L
- Pin 3/11: Low-Speed CAN (⚠️ NOT on all V50 models — may need CEM splice)
- Pin 16: +12V Battery
- Pin 4/5: Ground

### CEM Pinout — P1 Platform (from model knowledge ⚠️)
- CEM sits behind glovebox
- Two variants: CEM-Low (base models) and CEM-High (with more options)
- Part numbers: 30758460, 30758461, 31268840 (varies by year/options)
- Key connectors:
  - A (54-pin): Power, Ground, CAN bus, LIN bus
  - B (26-pin): Lighting & signaling
  - C (40-pin): Wiper, washer, horn, HVAC
  - D (20-pin): Door modules, interior lighting (LIN bus)
  - E (16-pin): Immobilizer, keyless entry
- Pinouts vary between pre-2008 and post-2008 facelift

### DIM (Dashboard) — Additional Info
- Three display variants: Mono DIN, Mono TFT, Color TFT (later models)
- Stepper motors: VID29xx / X27.589 compatible
- Connector A (26-pin): Power, illumination, warning lights
- Connector B (32-pin): CAN-H, CAN-L, immobilizer LED
- Connector C (16-pin): Trip computer buttons

## VERIFICATION NEEDED
All data above comes from model training knowledge, not verified web sources.
Priority verification targets:
1. CAN ID ranges (0x0xx vs 0x3xx)
2. CEM connector pin counts (our docs say 38/52/22/16/10, model says 54/26/40/20/16)
3. Actual OBD-II access to low-speed CAN
4. ACC panel pinout (our docs vs model knowledge)