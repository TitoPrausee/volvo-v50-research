# African Queen Lite — Ride-Mode Controller Research v2.1

## 1. ESP32 vs Arduino vs Teensy — Motorcycle Controller

| Feature | ESP32-WROOM-32 | Arduino Mega 2560 | Teensy 4.0 |
|---------|---------------|-------------------|-------------|
| **GPIO** | 34 usable | 54 (5V only) | 40 (3.3V) |
| **PWM** | 16 hardware LEDC | 15 (8-bit) | 12 (16-bit timers) |
| **WiFi/BT** | WiFi + BLE built-in | None | None (add-on) |
| **CPU** | 240 MHz dual-core | 16 MHz | 600 MHz Cortex-M7 |
| **Power** | ~80 mA (WiFi on) | ~50 mA | ~100 mA |
| **Temp Range** | -40°C to +85°C | -40°C to +85°C | -40°C to +105°C |
| **EEPROM** | Flash-based (4MB) | 4KB real EEPROM | Flash-based (2MB) |
| **Price** | ~€5-8 | ~€15 | ~€25 |

**Winner: ESP32** — Built-in BLE for smartphone logging, enough GPIOs for all sensors+outputs, dual-core (one core for BLE, one for real-time control), cheap, large ecosystem, flash-based EEPROM for mode persistence.

**v2.0 additions:** EEPROM mode persistence using `EEPROM.begin()` / `EEPROM.commit()` pattern. Stores: last active mode, odometer, runtime. Uses only 64 bytes of flash.

**Motorcycle-specific protections required:**
- **Power conditioning:** TVS diode (SMAJ28A), 470µF + 100nF caps, reverse polarity protection (1N5408), 7805 → 3.3V LDO or Mean Well RSD-30G-3.3
- **Conformal coating:** MG Chemicals 422B for vibration/moisture resistance
- **Anti-vibration mount:** Rubber grommets (McMaster 9485K52)

## 2. Exhaust Valve Systems

### Yamaha EXUP & Honda HES
- EXUP: DC brushed motor with integrated pot feedback, 50Hz PWM, 0.5°-90° rotation
- Honda HES: Similar principle, brushed DC motor + position pot
- **NX650 has NO factory exhaust valve** — must be retrofitted

### DIY Exhaust Valve Recommendation
Do NOT use standard RC servos (SG90/MG996R) — too fragile for heat/vibration.

**Recommended:** 12V brushed gearmotor + DRV8833 H-bridge + AS5600 magnetic angle sensor
- Pololu 37Dx52L 13.5:1 gearmotor (~€25)
- DRV8833 dual H-bridge (~€3)
- AS5600 magnetic encoder (I²C, non-contact, vibration-resistant)
- Total: ~€35 per axis

**v2.0 update:** Added configurable sweep rates per mode:
- SPORT: fast sweep (sweep_rate=8, near-instant valve transition)
- COMFORT: slow sweep (sweep_rate=2, gentle, smooth transitions)
- STRASSE: medium sweep (sweep_rate=3)
- This gives each mode a distinctive feel and sound character

## 3. Programmable CDI for NX650 RFVC

### Options
| CDI | Type | Programmable | Price | Notes |
|-----|------|-------------|-------|-------|
| **Ignitech DC-CDI-P2** | DC-CDI | Yes (2 maps, USB programmable) | ~€120 | Best option! |
| Vape/Pamco | AC-CDI | No (fixed curve) | ~€50 | Not for NX650 DC |
| Hondachopper CDI | DC-CDI | No | ~€60 | Fixed timing |
| DIY Arduino CDI | Custom | Full control | ~€30 | Risky, no safety cert |

### Ignitech DC-CDI-P2 (Recommended)
- **2 programmable timing maps** — switchable via external input!
- Map select pin: LOW = Map A (base), HIGH = Map B (advanced/sport)
- USB programmable via Ignitech software (Windows)
- Supports: advance curves, RPM limiting, throttle position (if sensor added)
- Input: 12V DC (compatible with NX650 stator/regulator)
- **This is exactly what we need** — ESP32 GPIO 27 drives the map select pin

### DIY CDI (Future/Advanced)
- **Requires:** Teensy 4.0 + ignition coil driver (IGBT or Darlington pair)
- **Risk:** A single timing error can destroy the engine
- **Recommendation:** Use Ignitech for now, explore DIY only with extensive testing on bench
- **StVZO concern:** DIY ignition systems may require TÜV approval (see section 5)

## 4. StVZO (German Road Traffic Regulations)

### What's Allowed
✅ **Custom displays** — No restriction on dashboard information displays (OLED, TFT)
✅ **Exhaust valve** — Mechanical exhaust valve systems are legal (OEM bikes have them)
✅ **LED indicators** — WS2812 inside housing, not visible to other traffic
✅ **BLE data logging** — Bluetooth is legal, no transmitting while driving restriction for low-power
✅ **Maintenance tracking** — Service interval monitors are standard on modern bikes
✅ **Temperature/voltage monitoring** — Diagnostic displays are legal

### What Needs Attention
⚠️ **Programmable CDI** — Must not exceed maximum RPM limit set by manufacturer
⚠️ **Exhaust sound** — Sound mode must still comply with §49 StVZO (max 95 dB(A) at standstill)
⚠️ **Exhaust valve modification** — Custom exhaust valve system needs TÜV approval (§19.2)
⚠️ **Handlebar controls** — Must not interfere with safe operation (§30 StVZO)

### What's NOT Allowed
❌ **Visible flashing LEDs on exterior** — Only amber/white allowed, no red/blue
❌ **Disabling safety switches** — Side stand switch, clutch switch must remain functional
❌ **Maximum RPM override** — Can't remove or raise rev limiter beyond OEM spec
❌ **Operating phone/display while driving** — BLE logging OK, but don't hold phone while riding

### TÜV Strategy
1. Build controller as "display module" first — TÜV only sees the display
2. Exhaust valve: Submit with TÜV as "variable exhaust system" (like OEM EXUP)
3. CDI: Register as "replacement CDI" — Ignitech DC-CDI-P2 has EC type approval
4. Full system: Individual approval (Einzelfallgenehmigung) per §21 StVZO

## 5. OLED vs TFT at Sunlight on Motorcycle

| Display | Sunlight Readability | Power | Price | Notes |
|---------|---------------------|-------|-------|-------|
| **SSD1306 OLED (128x64)** | Moderate (high contrast) | ~20mA | ~€2 | Cheap, simple I²C |
| **SSD1309 OLED (128x64, SPI)** | Better (faster refresh) | ~25mA | ~€3 | SPI = faster updates |
| **1.3" SH1106 OLED** | Good | ~20mA | ~€3 | Slightly larger than SSD1306 |
| **2.4" ILI9341 TFT** | Poor (needs backlight boost) | ~80mA | ~€5 | Color but washes out |
| **4.2" e-ink** | Excellent | ~1mA | ~€15 | Very slow refresh (2-3s) |
| **Transflective TFT (LS027B7DH01)** | Excellent | ~5mA | ~€20 | Best for sunlight! |

### Recommendation
- **Prototype:** SSD1306 128x64 OLED (cheap, easy I²C, good contrast)
- **Production:** Sharp Memory LCD LS027B7DH01 (2.7" transflective, sunlight-readable, ~€20)
  - Sharp Memory LCDs are used in Garmin watches — perfect for motorcycle visibility
  - SPI interface, very low power (1mA running)
  - No backlight needed — transfective technology works in direct sunlight
  - Available from Digi-Key / Mouser

### Anti-glare measures
- Matte polarizing film over display (3M Vikuiti)
- Slight bezel hood (3D-printed, ~15° angle)
- Auto-brightness based on ambient light sensor (future)

## 6. Handlebar Switches — Weather-Proof Options

| Switch | IP Rating | Glove-Usable | Price | Notes |
|--------|-----------|-------------|-------|-------|
| **KY-040 Encoder + silicone boot** | IP65 (with boot) | Good | ~€2 | Budget, needs waterproofing |
| **Apem 5620 Series** | IP67 | Excellent | ~€25 | IP67, motorcycle-rated |
| **Honda OEM switch block** | IP68 | Excellent | ~€40 (used) | From Africa Twin / XL — best fit |
| **BMW GS switch cluster** | IP68 | Excellent | ~€60 (used) | Premium, too many functions |
| **Sea-Doo PWC switch** | IP68 | Good | ~€15 | Waterproof, but chunky |

### v2.0 Recommendation: Rotary Encoder
- **Primary input:** KY-040 rotary encoder with 3D-printed waterproof housing and silicone shaft seal
- **Backup:** Two push buttons (Mode+/Mode-) from Apem 5620 series
- Encoder provides: CW = next mode, CCW = previous mode, press = toggle mode/page select
- More intuitive for riding: one-handed twist operation, no need to look at switch

### v2.0 New Feature: Display Page Cycling
- Press encoder button to switch between MODE SELECT and PAGE SELECT
- In mode select: CW/CCW changes ride mode (with confirmation on display)
- In page select: CW/CCW cycles through 4 display pages (Ride, Health, Maint, Trip)
- Auto-cycle: Pages rotate every 10 seconds when no input

## 7. NX650 Specific Notes

### Stator
- Output: ~180W @ 5000 RPM (single-phase, 8-pole)
- Known issues: Stator winding failure common at 40,000+ km
- **v2.0 Feature:** Stator health monitoring detects degradation BEFORE failure
  - Monitor voltage at cruise RPM (3000+): should be ≥ 13.0V
  - Below 12.5V at cruise = failing stator → warning displayed
  - Below 11.5V or above 15.5V = critical → full alert

### Air Cooling (NO RADIATOR!)
- Cylinder head temperature is CRITICAL monitoring parameter
- Normal operating: 150-200°C (cylinder head)
- Warning: 115°C (measured at fin) = slow down
- Critical: 125°C (measured at fin) = stop and let cool
- **v2.0 Feature:** Temperature trend detection (°C/min rise) predicts overheat 2-3 minutes before critical

### Battery (LiFePO4)
- 4S LiFePO4: 12.8V nominal, drop-in replacement for lead-acid
- Weight saving: ~2 kg vs lead-acid
- Voltage curve is very flat (12.8-13.6V for 90% of capacity)
- **v2.0 Feature:** Battery SOC estimation from voltage curves
  - Engine off: resting voltage gives accurate SOC
  - Engine running: use voltage trends for charge health

### Maintenance Intervals (NX650)
| Item | Interval | Notes |
|------|----------|-------|
| Oil change | 6,000 km | 10W-40 semi-synthetic |
| Valve adjustment | 12,000 km | RFVC has 4 valves, shim-under-bucket |
| Air filter | 12,000 km | More often off-road |
| Spark plug | 12,000 km | NGK DPR8EA-9 |
| Drive chain | Check/adjust every 1,000 km | 520, 15/45 ratio |
| Tires | Check every 1,000 km | 120/90-17 front, 130/80-17 rear |
| Coolant | N/A | **Air-cooled!** |

**v2.0 Feature:** All intervals tracked in EEPROM, with overdue warnings on display

---

## v2.1 Research Additions (2026-05-28)

### 8. 3-Map CDI Control — Ignitech DC-CDI-P2

The Ignitech DC-CDI-P2 supports **2-pin map selection** for up to 3 ignition maps:
- **Pin 1 (CDI_MAP_A, GPIO27):** Low=Map A, High=Map B
- **Pin 2 (CDI_MAP_B, GPIO33):** When Pin1=High AND Pin2=High → Map C
- Logic table: A=LL, B=HL, C=HH (L=LOW, H=HIGH on respective pin)

**v2.1 Mode→Map assignments:**

| Mode | CDI Map | Pin A (GPIO27) | Pin B (GPIO33) | Rationale |
|------|---------|----------------|----------------|-----------|
| STRASSE | A | LOW | LOW | Balanced, OEM-equivalent |
| STADT | A | LOW | LOW | Economy, retarded timing not in CDI map |
| GELÄNDE | B | HIGH | LOW | Advanced timing for off-road power |
| SPORT | B | HIGH | LOW | Aggressive timing |
| COMFORT | A | LOW | LOW | Retarded via software if needed |
| SOUND | C | HIGH | HIGH | Sound-optimized map (custom tuning) |

**TÜV note:** Ignitech DC-CDI-P2 has **EC type approval** — legal for road use in DE. Map switching itself is not regulated (no StVZO clause forbids it). However, Map C must not exceed OEM peak power (§19.2).

### 9. DRV8833 + AS5600 Motor Driver for Exhaust/Airbox Valves

**Problem:** RC servos (MG996R) are not reliable for motorcycle use — vibration destroys potentiometers, position drift occurs, no feedback.

**v2.1 Solution:** Compile-time selectable DRV8833+AS5600 motor driver:
- **DRV8833:** H-bridge motor driver, drives DC gearmotor for valve
- **AS5600:** 12-bit magnetic rotary encoder (I²C), closed-loop position feedback
- **Compile flag:** `USE_DRV8833` in platformio.ini selects motor driver vs RC servo
- **RC servo fallback:** MG996R on GPIO still available for prototyping

**Wiring (DRV8833+AS5600):**
- DRV8833 IN1→GPIO14, IN2→GPIO12 (exhaust), IN1→GPIO4, IN2→GPIO2 (airbox)
- AS5600 SDA→GPIO21, SCL→GPIO22 (shared I²C bus, different I²C addresses)
- AS5600 power: 3.3V, DRV8833 power: 5V (motor supply)

**Cost:** DRV8833 breakout ~€3, AS5600 module ~€4, Pololu 37D gearmotor ~€35 = ~€42 per axis (x2 = ~€84)

### 10. OLED Sunlight Readability — v2.1 Optimizations

**Problem:** SSD1306 OLED (128x64) is hard to read in direct sunlight on a motorcycle.

**v2.1 Software optimizations (no hardware change):**
- **2x font for critical values:** Temperature and voltage displayed in 2x height (16→32px characters)
- **Inverted display mode:** `ssd1306_normal_mode` → `ssd1306_invert_display` in bright conditions
- **High-contrast layout:** White text on black background, thick borders, no thin lines
- **Priority display:** Only show mode name + 2 critical values on main ride page (less clutter = more readable)

**Still recommended for production:** Sharp Memory LCD LS027B7DH01 (transflective, €20). SSD1306 is prototype-only.

### 11. Engine Runtime Tracking — Bug Fix

**v2.0 Bug:** `engine_runtime_min_` in `longevity.h` was never incremented — only declared and reset.

**v2.1 Fix:** Added `update_runtime()` method using `millis()` delta tracking:
```cpp
void update_runtime() {
    uint32_t now = millis();
    if (now - last_runtime_millis_ >= 60000UL) {
        engine_runtime_min_++;
        last_runtime_millis_ += 60000UL;
    }
}
```
Called from `main.cpp` loop when engine is running (RPM > 0).

### 12. Wiring Diagram Generator

**v2.1 Tool:** `dashboard/hardware/wiring_diagram.py` — Python script that generates:
- **SVG diagram:** Color-coded wiring with component blocks, pin labels, wire colors
- **ASCII diagram:** Terminal-friendly text rendering for quick reference
- Reads pin definitions from `platformio.ini` comment conventions
- Includes all v2.1 hardware: ESP32, DRV8833, AS5600, Ignitech CDI, sensors, servos, display, LED, encoder

### 13. Parts Compatibility Checker

**v2.1 Tool:** Python script reading `vehicle_database.db` to validate:
- All controller components against known NX650-fitment parts
- Cross-reference with known issues (stator, regulator, connectors)
- Budget compliance check against €5,000 hard cap