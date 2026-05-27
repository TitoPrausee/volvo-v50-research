# Volvo V50 Pre-Facelift (2004-2007) — CAN Bus Research Log

> Focus on pre-facelift model years and their CAN bus differences  
> Last updated: 2026-05-27

## Key Hypothesis: CAN ID Ranges Differ by Model Year

### Problem
Our CAN database has TWO conflicting sets of CAN IDs:
- **Set A (0x0xx range)**: From community docs — ECM 0x0C0, TCM 0x1A0, etc.
- **Set B (0x3xx range)**: From model knowledge — RPM 0x316, Speed 0x360, etc.

### Likely Explanation
| Range | Likely Applies To | ECU Type | Evidence |
|-------|-------------------|----------|----------|
| 0x0xx range | Pre-facelift (2004-2007), Bosch ME9.1 | Bosch ME9 ECU | Community docs from early V50 owners |
| 0x3xx range | Facelift (2008-2012), Denso/updated ECU | Denso ECU or updated Bosch | OpenXC/Ford C1 platform data |

### Why This Matters for Our B5244S (2004-2007)
- Our V50 has the **Bosch ME9.1 ECU** (confirmed for 2.4i 2004-2006)
- Therefore, **our CAN IDs are most likely in the 0x0xx range**
- The 0x3xx range is probably for later models or diesel variants
- **BUT: We need a real CAN dump to confirm**

### Pre-Facelift vs Facelift CAN Architecture

```
Pre-Facelift (2004-2007)          Facelift (2008-2012)
========================          ====================
Bosch ME9.1 ECU (2.4i/2.5T)      Denso or updated ECU
AW55-51 5-speed auto             Updated Geartronic
CEM 38/52/22/16/10 connectors    CEM revised connectors
Mono DIM display                 Mono or Color TFT DIM
CAN IDs likely 0x0xx range       CAN IDs likely 0x3xx range
OBD pin 3/11: Low CAN (some)     OBD pin 3/11: Low CAN (maybe not)
```

## Pre-Facelift Specifics Research Sources

### Verified Differences (Community-Confirmed)

1. **CEM Relay Solder Issue** — Prevalent in 2004-2007 models
   - CEM part numbers 30647356, 30647546 affected
   - Symptoms: intermittent electrical failures
   - Fix: Resolder or replace CEM (must program with VIDA)
   - Source: swedespeed.com, volvoforums.com, matthewsvolvosite.com

2. **DIM Pixel Fade** — Common in pre-facelift
   - Orange LCD pixels fade from edges
   - Custom dashboard project eliminates this entirely
   - Source: Multiple forum posts

3. **AW55-51 Valve Body** — 2004-2007 specific
   - Harsh 2-3 and 3-4 shifts
   - TCC shudder at 60-80 km/h
   - Fix: Valve body rebuild kit (~€200) or Sonnax zip kit
   - Must use Toyota T-IV fluid, NOT Dexron VI

4. **Front Lower Control Arm Bushings** — Pre-facelift specific design
   - Different from facelift (Volvo improved them)
   - Not CAN related but important for overall maintenance

### Unconfirmed (Needs Verification)

1. **CAN ID range** — 0x0xx vs 0x3xx — needs real CAN dump
2. **Low-speed CAN on OBD pins 3/11** — May only be on early models
3. **CEM connector pin counts** — 38/52/22/16/10 vs 54/26/40/20/16
4. **DIM protocol differences** — Mono DIN vs Mono TFT may use different CAN messages
5. **Immobilizer protocol** — Pre-2005 may differ from 2005-2007

## Pre-Facelift B5244S Part Numbers (for Reference)

| Component | Part Number(s) | Notes |
|-----------|---------------|-------|
| ECU (Bosch ME9.1) | 30647xxx | Paired with CEM, cannot swap |
| CEM-Low | 30647356 | Base models |
| CEM-High | 30647546, 30735804 | Higher option models |
| DIM (Mono DIN) | 30665xxx | Basic cluster |
| DIM (Mono TFT) | 30665xxx (different rev) | Mid-level cluster |
| ACC Module | 30666xxx | Climate control panel |
| TCM (AW55-51) | 30647xxx | 5-speed auto transmission |

## Action Items for CAN Verification

1. **Install PiCAN2 on OBD port** (connects to high-speed CAN)
2. **Capture cold-start sequence** (key OFF → ON → START)
3. **Log all CAN IDs for 5 minutes at idle**
4. **Press each ACC button individually** and note CAN changes
5. **Drive for 15 minutes** and log all IDs during acceleration/braking
6. **Compare logged IDs against both ranges** in CAN_DATABASE.md
7. **If 0x0xx range confirmed** → our original docs are correct for this model year
8. **If 0x3xx range found** → we need to update and note it as transitional

## Sources & References

- SwedeSpeed forums — P1 tuning section, V50/S40 specific threads
- VolvoForums.com — V50 electrical issues, CEM problems
- MatthewsVolvoSite.com — DIY repair guides, DIM capacitor fixes
- OpenXC project — Ford C1 platform CAN data (may be facelift only)
- bsmithyman/volvo-p1-can (GitHub) — Python CAN research for P1