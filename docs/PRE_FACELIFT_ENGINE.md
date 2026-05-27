# Volvo V50 Pre-Facelift (2004-2007) — Model Year Reference

> Focus: MY2004-MY2007 V50 before the 2008 facelift  
> These model years likely use the 0x0xx CAN ID range documented in our original CAN_BUS.md  
> Last updated: 2026-05-27

## Model Year Overview

### 2004 (Introductory Year)
- **Launch**: Spring 2004 as 2005 model year in most markets
- **Engines**: 2.4i (B5244S, 140hp), 2.5T (B5254T3, 220hp), D5 (D5244T, 163hp)
- **Transmissions**: 5-speed auto (AW55-51) or 5/6-speed manual (M56/M66)
- **Electronics**: Early CEM revision, Bosch ME9.1 ECU
- **Known Issues**: Early CEM failures, DIM pixel fade, AW55-51 valve body problems

### 2005-2006
- **Engine additions**: 1.6 (B4164S, 100hp) in some markets, 2.0D (D4204T, 136hp)
- **Transmissions**: Same options
- **Minor updates**: Software updates to ECU/TCM, improved CEM relays
- **Known Issues**: CEM relay solder joint cracks, DIM capacitor leaks, S40/V50 door lock actuator failures

### 2007 (Last Pre-Facelift Year)
- **Engines**: Same lineup, some markets got 2.0F (flex-fuel)
- **This is the transition year** — some late 2007 models got pre-facelift interior changes
- **ECU**: Some 2007 models transitioned from Bosch ME9 to Denso
- **CEM**: Revised part numbers (31268840 appeared)

## Engine Variants (2004-2007)

| Code | Displacement | Cylinders | Power | Torque | Years | Notes |
|------|-------------|-----------|-------|--------|-------|-------|
| B5244S | 2.4L | I5 NA | 103 kW (140 hp) | 220 Nm | 2004-2007 | Most common, NA |
| B5254T3 | 2.5L | I5 Turbo | 162 kW (220 hp) | 320 Nm | 2004-2007 | T5 variant |
| D5244T | 2.4L | I5 Diesel | 120 kW (163 hp) | 340 Nm | 2004-2007 | Common diesel |
| D4204T | 2.0L | I4 Diesel | 100 kW (136 hp) | 320 Nm | 2005-2007 | PSA/Ford diesel |
| B4164S | 1.6L | I4 NA | 74 kW (100 hp) | 145 Nm | 2005-2007 | Budget markets only |
| B4204S3 | 2.0L | I4 NA | 107 kW (145 hp) | 185 Nm | 2005-2007 | Some European markets |

## Transmission Options (2004-2007)

| Transmission | Code | Gears | Torque Rating | Years | Notes |
|-------------|------|-------|--------------|-------|-------|
| AW55-51SN | ASIN | 5-speed auto | 320 Nm | 2004-2007 | Common, valve body issues |
| M56 | — | 5-speed manual | 280 Nm | 2004-2006 | Reliable, cable shift |
| M66 | — | 6-speed manual | 400 Nm | 2004-2007 | T5 and D5 models |

### AW55-51 Known Issues (Pre-Facelift)
- **Valve body wear**: Harsh shifts, flare between 2-3, 3-4
- **Solenoid failures**: Shift solenoid A/B, TCC solenoid
- **Fluid type**: Toyota T-IV (NOT Dexron VI) — using wrong fluid causes shift problems
- **Recommended**: Fluid change every 60,000 km, valve body rebuild at ~150,000 km
- **TCM on CAN bus**: Sends gear position ID 0x1A0, temp ID 0x1A8

## ECU Variants (2004-2007)

### Pre-Facelift ECU Types
| Year | Engine | ECU Type | Part Number Range | Notes |
|------|--------|---------|------------------|-------|
| 2004-2006 | B5244S | Bosch ME9.1 | 30647xxx | Early ME9, more CAN IDs in 0x0xx range |
| 2006-2007 | B5244S | Denso (transition) | 30735xxx | Some late models switched ECU |
| 2004-2007 | B5254T3 (T5) | Bosch ME9.1 | 30647xxx | Turbo variant, boost PID 0x220105 |
| 2004-2007 | D5244T | Denso | 30647xxx | Diesel always Denso |

### ⚠️ KEY INSIGHT: ECU and CAN ID Relationship
- **Bosch ME9.1 (early models)**: Likely uses CAN IDs in the **0x0C0-0x1A8 range** (as in our CAN_BUS.md)
- **Denso (later models / diesel)**: Likely uses CAN IDs in the **0x300+ range** (as in model knowledge)
- **This explains the contradictions in our CAN database!**
- **Pre-facelift 2.4i (our B5244S)** with Bosch ME9.1 almost certainly uses the 0x0xx range

## CEM Variants (2004-2007)

### Pre-Facelift CEM
| Part Number | Description | Years | Notes |
|------------|-------------|-------|-------|
| 30647356 | CEM-Low, early | 2004-2005 | Fewer features, fewer connectors |
| 30647546 | CEM-High, early | 2004-2006 | More options (sunroof, premium audio) |
| 30735804 | CEM-High, revised | 2006-2007 | Updated relays, improved connectors |
| 31268840 | CEM, late pre-facelift | 2007-2008 | Transition part, may differ internally |

### Known Pre-Facelift CEM Issues
- **Relay solder cracks**: CEM internally has soldered micro-relays that develop cracks over time
  - Symptoms: Intermittent wipers, no A/C, random warning lights, no start
  - Fix: Resolder CEM board or replace CEM
  - **Warning**: Replacement CEM MUST be programmed with VIDA for the specific VIN
- **Immobilizer**: Stored in CEM + ECM pair — cannot swap either module without VIDA reprogramming
- **Key programming**: Up to 3 remote keys can be programmed per CEM

### Pre-Facelift CEM Connectors (Likely 38/52/22/16/10 Layout)
Based on early CEM documentation, pre-facelift CEM connectors appear to be:
- **A (38-pin, Black)**: Power, ignition, high-speed CAN
- **B (52-pin, Gray)**: Low-speed CAN, lighting, wipers, accessories
- **C (22-pin, Blue)**: Door modules, LIN bus, seats
- **D (16-pin, Green)**: Immobilizer, key recognition
- **E (10-pin, Red)**: Battery direct power

**This matches our original CAN_BUS.md connector documentation.**

⚠️ The 54/26/40/20/16 layout from model knowledge may be the **facelift (2008+)** CEM revision.

## DIM Variants (2004-2007)

### Pre-Facelift Instrument Clusters
- **Mono DIN**: Basic orange LCD, trip computer, basic warnings
- **Mono TFT**: Red/orange dot-matrix display (mid-level trims)
- Both use VID29xx or X27.589 stepper motors for gauges
- No color TFT in pre-facelift V50 (that's facelift only)

### Pre-Facelift DIM CAN IDs (Likely)
Based on the ECU analysis, pre-facelift V50 should use:
- 0x300: RPM → DIM tachometer
- 0x308: Speed → DIM speedometer
- 0x310: Fuel → DIM fuel gauge
- 0x318: Temp → DIM temp gauge
- 0x320: Warning lights → DIM
- 0x328: Odometer → DIM
- 0x340: Trip computer buttons → CEM

## 2008 Facelift — Key Changes

| Aspect | Pre-Facelift (2004-2007) | Facelift (2008-2012) |
|--------|--------------------------|----------------------|
| Front design | Rounded grille, large headlights | Sharper grille, thinner headlights |
| Interior | Center stack "floating" console redesigned | Updated materials, new HVAC controls |
| CEM | 38/52/22/16/10 connectors (likely) | Updated connectors (possibly 54/26/40/20/16) |
| ECU | Bosch ME9.1 (2.4i/2.5T), Denso (diesel) | Transition to Denso for more models |
| CAN IDs | 0x0xx range (likely) | Possibly shifted to 0x3xx range |
| DIM | Mono DIN or Mono TFT | Mono TFT or Color TFT (late) |
| TCM | AW55-51SN (5-speed only) | Some got Geartronic updates |
| DRL | Not standard | DRL became standard (EU regulation) |

## Important Notes for 2004-2007 V50 (B5244S)

1. **Your car likely uses the 0x0C0-0x1A8 CAN ID range** (Bosch ME9.1 ECU)
2. **The 0x300+ CAN IDs in our database may be facelift/diesel variants**
3. **CEM connector layout is likely A38/B52/C22/D16/E10** (pre-facelift)
4. **AW55-51 transmission needs fluid changes every 60k km** — use Toyota T-IV only
5. **DIM pixel fade is common** — a custom LCD dashboard eliminates this problem entirely
6. **CEM relay solder cracks** are the #1 electrical issue — if you're already behind the dash for the Pi, resolder the CEM board as preventive maintenance

## Verification Plan for Pre-Facelift V50

To confirm the CAN IDs, you need:
1. **CAN dump from key-on to engine running** (capture all IDs on high-speed bus)
2. **Log all unique CAN IDs** during idle and driving
3. **Correlate IDs with known events** (press A/C button → look for new/changed IDs)
4. **Compare your CAN dump against both ID ranges** (0x0xx and 0x3xx)
5. **This will definitively resolve which range your model year uses**