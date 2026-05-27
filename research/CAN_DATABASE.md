# Volvo V50 CAN Bus — Master Database

> Consolidated from all sources. Cross-referenced and deduplicated.  
> Last updated: 2026-05-27

## ⚠️ Verification Legend

| Status | Meaning |
|--------|---------|
| ⚠️ UNVERIFIED-community | From community docs, not confirmed by CAN dump |
| ⚠️ UNVERIFIED-model | From AI model training knowledge, NOT verified |
| ⚠️ CONTRADICTS | Conflicts with another source — needs resolution |
| ✅ VERIFIED | Confirmed by actual CAN dump or official VIDA |

## High-Speed CAN Bus (500 kbps) — Powertrain

| CAN ID | Direction | Description | Byte Layout | Status | Source |
|--------|-----------|-------------|-------------|--------|--------|
| 0x0C0 | ECM → CEM | Engine RPM | Byte 0-1: RPM ÷ 4 | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x316 | ECM → ? | Engine RPM | 16-bit, rpm*4 | ⚠️ CONTRADICTS 0x0C0 | test_glm51.txt |
| 0x0C8 | ECM → CEM | Coolant Temperature | Byte 0: temp (°C - 40) | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x3B0 | ? → ? | Coolant Temperature | — | ⚠️ CONTRADICTS 0x0C8 | test_glm51.txt |
| 0x0D0 | ECM → CEM | Throttle Position | Byte 0: position % | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x3F0 | ? → ? | Throttle Position | — | ⚠️ CONTRADICTS 0x0D0 | test_glm51.txt |
| 0x0D8 | ECM → CEM | Engine Load / MAF | Byte 0-1: load value | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x3E0 | ? → ? | Engine Load | — | ⚠️ CONTRADICTS 0x0D8 | test_glm51.txt |
| 0x0E0 | ECM → CEM | Vehicle Speed | Byte 0-1: speed ÷ 100 km/h | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x360 | ? → ? | Vehicle Speed | km/h | ⚠️ CONTRADICTS 0x0E0 | test_glm51.txt |
| 0x0F0 | ECM → CEM | Fuel Level | Byte 1: fuel level % | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x320 | ? → ? | Fuel Level | 0-100% | ⚠️ CONTRADICTS 0x0F0 | test_glm51.txt |
| 0x100 | ECM → CEM | Intake Air Temperature | Byte 0: temp (°C - 40) | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x108 | ECM → CEM | Oil Pressure/Temperature | Byte 0: oil temp | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x1A0 | TCM → CEM | Gear Position | Byte 0: P=0,R=1,N=2,D=3,4,5 | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x1A8 | TCM → CEM | Transmission Temperature | Byte 0: temp (°C - 40) | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x330 | ? → ? | Fuel Consumption Instantaneous | — | ⚠️ UNVERIFIED-model | test_glm51.txt |
| 0x3D0 | ? → ? | Accelerator Pedal Position | — | ⚠️ UNVERIFIED-model | test_glm51.txt |

### ABS / Brakes (High-Speed CAN)

| CAN ID | Direction | Description | Byte Layout | Status | Source |
|--------|-----------|-------------|-------------|--------|--------|
| 0x1A0 | ABS → ? | Wheel Speed FL | — | ⚠️ UNVERIFIED-model | test_glm51.txt |
| 0x1A1 | ABS → ? | Wheel Speed FR | — | ⚠️ UNVERIFIED-model | test_glm51.txt |
| 0x1A2 | ABS → ? | Wheel Speed RL | — | ⚠️ UNVERIFIED-model | test_glm51.txt |
| 0x1A3 | ABS → ? | Wheel Speed RR | — | ⚠️ UNVERIFIED-model | test_glm51.txt |
| 0x1B0 | ABS → ? | Brake Pedal/Pressure | — | ⚠️ UNVERIFIED-model | test_glm51.txt |
| 0x100 | ? → ? | Steering Angle Sensor | — | ⚠️ UNVERIFIED-model | test_glm51.txt |

## Climate Control (High-Speed CAN)

| CAN ID | Direction | Description | Byte Layout | Status | Source |
|--------|-----------|-------------|-------------|--------|--------|
| 0x200 | ACC → CEM | Climate Panel Button | Byte 0: button ID | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x200 | ? → ? | HVAC Blower Speed | — | ⚠️ CONTRADICTS (different meaning) | test_glm51.txt |
| 0x204 | ? → ? | Air Distribution/Recirc | — | ⚠️ UNVERIFIED-model | test_glm51.txt |
| 0x208 | ACC → CEM | Temperature Setpoint Driver | Byte 0: temp (°C × 2) | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x208 | ? → ? | AC Compressor Status | — | ⚠️ CONTRADICTS (different meaning) | test_glm51.txt |
| 0x210 | ACC → CEM | Temperature Setpoint Passenger | Byte 0: temp (°C × 2) | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x218 | ACC → CEM | Fan Speed Request | Byte 0: speed level (0-15) | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x220 | ACC → CEM | Air Distribution | Byte 0: mode (0=auto,1=face,2=feet,3=defrost) | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x228 | ACC → CEM | A/C Compressor Request | Byte 0: 0=off, 1=on | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x230 | CEM → DIM | Interior Temperature | Byte 0: temp (°C × 2) | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x238 | CEM → DIM | Exterior Temperature | Byte 0: temp (°C - 40) | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x240 | ACC → CEM | Recirculation Request | Byte 0: 0=fresh, 1=recirc | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x280 | CEM → ACC | Blend Door Position Feedback | Byte 0: position % | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x220 | ? → ? | Ambient/Outside Air Temp | — | ⚠️ CONTRADICTS 0x238 | test_glm51.txt |
| 0x240 | ? → ? | Interior Temperature HVAC | — | ⚠️ CONTRADICTS 0x230 | test_glm51.txt |

## Dashboard / DIM (High-Speed CAN)

| CAN ID | Direction | Description | Byte Layout | Status | Source |
|--------|-----------|-------------|-------------|--------|--------|
| 0x300 | CEM → DIM | RPM for Tachometer | Byte 0-1: RPM ÷ 4 | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x308 | CEM → DIM | Speedometer Value | Byte 0-1: speed ÷ 100 | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x310 | CEM → DIM | Fuel Gauge Value | Byte 0: level % | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x318 | CEM → DIM | Coolant Temp Gauge | Byte 0: position % | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x320 | CEM → DIM | Warning Lights Bitmap | Byte 0-3: bitmap | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x328 | CEM → DIM | Odometer Value | Byte 0-3: km | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x340 | DIM → CEM | Trip Computer Button | Byte 0: button ID | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x300 | ? → ? | Odometer/Trip Data | — | ⚠️ CONTRADICTS 0x328 (different meaning for same ID) | test_glm51.txt |
| 0x310 | ? → ? | Turn Signal Status | — | ⚠️ CONTRADICTS 0x310 (different meaning) | test_glm51.txt |
| 0x340 | ? → ? | Warning Lights/MIL Status | — | ⚠️ CONTRADICTS 0x320 (different meaning) | test_glm51.txt |

## Body / Comfort (Low-Speed CAN via CEM Gateway)

| CAN ID | Direction | Description | Byte Layout | Status | Source |
|--------|-----------|-------------|-------------|--------|--------|
| 0x400 | SWM → CEM | Steering Wheel Button | — | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x260 | ? → ? | Steering Wheel Buttons | — | ⚠️ CONTRADICTS 0x400 | test_glm51.txt |
| 0x264 | ? → ? | Audio Volume/Mute | — | ⚠️ UNVERIFIED-model | test_glm51.txt |
| 0x410 | DDM → CEM | Driver Door Status | — | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x418 | PDM → CEM | Passenger Door Status | — | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x280 | ? → ? | Door Status/Lock | — | ⚠️ CONTRADICTS 0x410/0x418 | test_glm51.txt |
| 0x420 | CEM → DIM | Exterior Lighting Status | — | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x2E0 | ? → ? | Light Switch Status | — | ⚠️ UNVERIFIED-model | test_glm51.txt |
| 0x430 | CEM → SWM | Cruise Control Data | — | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x500 | IAM → CEM | Audio System Status | — | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x510 | CEM → IAM | Audio Commands | — | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x2C0 | ? → ? | Wiper Status/Speed | — | ⚠️ UNVERIFIED-model | test_glm51.txt |

## OBD-II Standard PIDs (ISO 15031)

| PID | Description | Formula | Status | Source |
|-----|-------------|---------|--------|--------|
| 0x0C | Engine RPM | (A × 256 + B) ÷ 4 | ✅ VERIFIED (standard) | CAN_BUS.md |
| 0x0D | Vehicle Speed | A km/h | ✅ VERIFIED (standard) | CAN_BUS.md |
| 0x05 | Coolant Temperature | A - 40 °C | ✅ VERIFIED (standard) | CAN_BUS.md |
| 0x0F | Intake Air Temperature | A - 40 °C | ✅ VERIFIED (standard) | CAN_BUS.md |
| 0x2F | Fuel Tank Level | (A ÷ 255) × 100 % | ✅ VERIFIED (standard) | CAN_BUS.md |
| 0x04 | Engine Load | (A ÷ 255) × 100 % | ✅ VERIFIED (standard) | CAN_BUS.md |
| 0x10 | MAF | (A × 256 + B) ÷ 100 g/s | ✅ VERIFIED (standard) | CAN_BUS.md |
| 0x11 | Throttle Position | (A ÷ 255) × 100 % | ✅ VERIFIED (standard) | CAN_BUS.md |

## Volvo Proprietary OBD Mode 22 PIDs

| PID | Description | Notes | Status | Source |
|-----|-------------|-------|--------|--------|
| 0x220104 | Oil Temperature | Needs verification | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x220105 | Boost Pressure (turbo) | 2.4L NA may not have | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x22010C | Transmission Fluid Temp | From TCM | ⚠️ UNVERIFIED-community | CAN_BUS.md |
| 0x2201__ | ACC Cabin Temp Sensor | From ACC module | ⚠️ UNVERIFIED-community | CAN_BUS.md |

## Key Contradictions to Resolve

| CAN ID | Doc A Says | Doc B Says | Resolution Needed |
|--------|-----------|------------|-------------------|
| 0x0C0 vs 0x316 | RPM | RPM | Need real CAN dump — may be different model years |
| 0x0E0 vs 0x360 | Vehicle Speed | Vehicle Speed | Same — model year dependent? |
| 0x200 | Climate button | HVAC blower speed | Completely different meanings! |
| 0x208 | Temp setpoint driver | AC compressor status | Completely different meanings! |
| 0x220 | Air distribution | Ambient temp | Completely different meanings! |
| 0x280 | Blend door position | Door status | Completely different meanings! |
| 0x300 | RPM for tach | Odometer data | Different meanings on same ID |
| 0x310 | Fuel gauge | Turn signal status | Different meanings on same ID |

### Likely Explanation
The P1 platform likely uses **different CAN IDs for different model years** (pre-2008 vs post-2008 facelift). Some IDs may also be **Ford C1 shared IDs** vs Volvo-specific IDs. Real CAN dumps from the specific V50 model year are essential.