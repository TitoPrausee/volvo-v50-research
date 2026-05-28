# African Queen Lite — Ride-Mode Controller Research v2.3

## 1. ESP32 vs Arduino vs Teensy — Motorcycle Controller

| Feature | ESP32-WROOM-32 | ESP32-S3 | Arduino Mega 2560 | Teensy 4.0 |
|---------|---------------|----------|-------------------|-------------|
| **GPIO** | 34 usable | 45 usable | 54 (5V only) | 40 (3.3V) |
| **PWM** | 16 hardware LEDC | 8 LEDC | 15 (8-bit) | 12 (16-bit timers) |
| **WiFi/BT** | WiFi + BLE built-in | WiFi + BLE 5.0 | None | None (add-on) |
| **CPU** | 240 MHz dual-core | 240 MHz dual-core | 16 MHz | 600 MHz Cortex-M7 |
| **AI Acceleration** | No | Yes (vector) | No | No |
| **Power** | ~80 mA (WiFi on) | ~100 mA (WiFi on) | ~50 mA | ~100 mA |
| **Deep Sleep** | ~10 µA | ~10 µA | N/A (no sleep) | ~30 µA (hibernate) |
| **Temp Range** | -40°C to +85°C | -40°C to +105°C | -40°C to +85°C | -40°C to +105°C |
| **Flash** | 4MB (OTA partition) | 8-16MB (OTA) | 4KB EEPROM only | 2MB flash |
| **Price** | ~€5-8 | ~€8-12 | ~€15 | ~€25 |

**Decision: Stick with ESP32-WROOM-32** — S3 would be nice for the AI acceleration but overkill. The WROOM-32 is proven, well-documented, has enough GPIOs for all sensor+output needs, dual-core for BLE + real-time control, and is cheapest. v2.2 adds deep sleep (~10µA) which solves the parasitic draw concern.

**Motorcycle-specific protections required:**
- **Power conditioning:** TVS diode (SMAJ28A), 470µF + 100nF caps, reverse polarity protection (1N5408), 7805 → 3.3V LDO or Mean Well RSD-30G-3.3
- **Conformal coating:** MG Chemicals 422B for vibration/moisture resistance
- **Anti-vibration mount:** Rubber grommets (McMaster 9485K52) or 3M VHB tape

## 2. Exhaust Valve Systems

### Yamaha EXUP & Honda HES
- EXUP: DC brushed motor with integrated pot feedback, 50Hz PWM, 0.5°-90° rotation
- Honda HES: Similar principle, brushed DC motor + position pot
- **NX650 has NO factory exhaust valve** — must be retrofitted

### DIY Exhaust Valve — v2.2 Recommendation
**Do NOT use standard RC servos (SG90/MG996R)** — too fragile for heat/vibration.

**Production option:** 12V brushed gearmotor + DRV8833 H-bridge + AS5600 magnetic angle sensor
- Pololu 37Dx52L 13.5:1 gearmotor (~€25)
- DRV8833 dual H-bridge (~€3)
- AS5600 magnetic encoder (I²C, non-contact, vibration-resistant) (~€5)
- Total: ~€35 per axis

**v2.2 improvement — Auto-RPM curves:**
Instead of a fixed valve % position per mode, exhaust and airbox positions now follow RPM-based curves. Each mode has 5 interpolation points mapping RPM → valve position. This gives:
- **STADT**: Valve mostly closed, slight opening above 5000 RPM for scavenging
- **GELÄNDE**: Wide open above 2500 RPM for maximum flow
- **SPORT**: Early aggressive opening for power delivery
- **SOUND**: RPM-tuned for maximum acoustic effect (deep crescendo)

**3D-printable butterfly valve options:**
- Custom butterfly valve can be 3D-printed in stainless steel (Shapeways) or machined from aluminum
- Shaft: M6 or 5mm stainless steel rod
- Butterfly plate: 35-40mm diameter for NX650 exhaust (~38mm ID)
- Housing: needs to be machined or welded into exhaust

## 3. Programmable CDI for NX650 RFVC

### Options
| CDI | Type | Programmable | Price | Notes |
|-----|------|-------------|-------|-------|
| **Ignitech DC-CDI-P2** | DC-CDI | Yes (2 maps, USB programmable) | ~€120 | **Best option!** Dual map via analog input |
| **Ignitech DC-CDI-P4** | DC-CDI | Yes (4 maps, Bluetooth, Android app) | ~€180 | Premium: 4 maps, Bluetooth config |
| **Vape/Pamco** | AC-CDI | No (fixed curve) | ~€80 | Not programmable, avoid |
| **DIY Arduino CDI** | Custom | Yes (fully programmable) | ~€40 | Requires: high-voltage coil driver, careful timing |

### v2.2 CDI Integration (3-Map)
The v2.2 firmware uses **GPIO27 (CDI_MAP_A)** + **GPIO33 (CDI_MAP_B)** for 3-map control:
- Map A (eco/retarded): A=LOW, B=HIGH → STRASSE, STADT, COMFORT
- Map B (advanced/sport): A=HIGH, B=LOW → GELÄNDE, SPORT
- Map C (fallback/standard): A=HIGH, B=HIGH → SOUND mode, emergency fallback

### StVZO Legal Notes
- **Programmierbare Zündung:** Generally legal if the ignition timing stays within the manufacturer's specified range. The Ignitech allows programming within safe limits. **No TÜV approval needed for ignition timing changes within spec** if using a certified CDI.
- **Exhaust Valve Modification:** Installing an exhaust valve system is legal if the exhaust stays within noise limits (§ 49 StVZO). A butterfly valve is considered an "Abgasreinigungsanlage" and may need TÜV if it significantly changes exhaust characteristics.
- **Custom Display on Handlebar:**Legal under § 22 StVZO (Anbaugeräte) — display must not obstruct controls or vision. The SSD1306 128x64 OLED is small enough to be mounted on the handlebar clamp (same position as OEM tachometer).
- **Practical recommendation:** Mount display on existing tachometer bracket or handlebar clamp. No TÜV needed for small display if it doesn't obstruct instruments.

## 4. Handlebar Switches — Waterproof Options

| Product | IP Rating | Price | Notes |
|---------|-----------|-------|-------|
| **Apem 5620 series** | IP67 | ~€25 | Motorcycle-rated, momentary, tactile feedback |
| **Bürkert 3010** | IP69K | ~€35 | Industrial, overkill for motorcycle |
| **Sealed tactile button (eBay)** | IP67 | ~€3 | Cheap, waterproof, small button head |
| **Honda OEM handlebar switch** | IP67 | ~€15 (used) | From any Honda bike, 2-wire, plug and play |
| **Koso RX-2N handlebar switch** | IP65 | ~€30 | LED backlit, multi-function |

**v2.2 recommendation:** Use **KY-040 rotary encoder** for mode switching (already implemented) with a **large knurled aluminum knob** (easy to grip with gloves). Add silicone sealant around the shaft. Button inputs via sealed tactile switches (IP67) for Mode+ and Mode-.

### Encoder Integration
- KY-040 encoder + custom aluminum knob: best UX while riding
- Waterproofing: silicone potting compound on the encoder base
- Mount on left handlebar (left thumb can rotate while right hand stays on throttle)
- Mode switching: twist forward = next mode, twist backward = previous mode
- Long press (3 sec) = enter config mode

## 5. OLED vs TFT — Sunlight Readability

| Display | Type | Size | Readable in Sun? | Price | Power |
|---------|------|------|-----------------|-------|-------|
| **SSD1306 OLED** (128x64) | OLED I2C | 0.96" | Moderate (needs inverted mode) | ~€3 | ~20mA |
| **SSD1306 OLED** (128x64) | OLED I2C | 1.3" | Better than 0.96" | ~€5 | ~25mA |
| **SSD1351 TFT** (128x128) | TFT SPI | 1.5" | Poor (backlit) | ~€4 | ~40mA |
| **IL91874 e-Ink** | E-Ink SPI | 2.13" | **Excellent** | ~€8 | ~5mA |
| **Newhaven OLED** (256x64) | OLED I2C | 2.4" | **Good** | ~€20 | ~60mA |
| **Reflective TFT** (transflective) | TFT | 2.4" | **Good** | ~€15 | ~35mA |

**v2.2 strategy (already implemented):**
- SSD1306 128x64 with **inverted display mode** (white background, black text) for sunlight
- Auto-detect sunlight from thermistor proximity (bright display area gets hot)
- Manual sunlight cycle via long encoder press: AUTO → NORMAL → INVERTED
- **Future upgrade:** 2.13" e-ink display for perfect sunlight readability (slow refresh OK for mode info)

## 6. AS5600 Magnetic Encoder — Motorcycle Considerations

The AS5600 is an **excellent choice** for exhaust valve position:
- **Non-contact:** No mechanical wear from vibration
- **I²C interface:** Simple 2-wire connection
- **12-bit resolution:** 0.088° — more than enough for butterfly valve
- **Programmable zero position:** No mechanical alignment needed
- **Price:** ~€5 per sensor

**Potential issues:**
1. **Heat:** AS5600 rated to -40°C to +85°C. Near the exhaust, temperatures can exceed 85°C. **Solution:** Mount the magnet on the valve shaft outside the exhaust, sensor 2-5mm from magnet, with heat shield.
2. **Vibration:** Non-contact magnetic sensing is inherently vibration-resistant. The magnet is glued to the shaft (use high-temp epoxy like JB Weld).
3. **EMI:** I²C lines can pick up ignition noise. **Solution:** Use shielded twisted pair for SDA/SCL, with 100nF bypass caps at the sensor.

**Magnet specification:** diametrically magnetized neodymium disc, 6mm diameter × 2.5mm thick (standard AS5600 magnet).

## 7. LiFePO4 Battery Monitoring — 4S 12V

The v2.2 firmware already tracks:
- Battery voltage via ADC (GPIO35 + voltage divider)
- LiFePO4 SOC from voltage curves:
  - >13.6V = 75%+ (charge OK)
  - 13.2-13.6V = 50-75% (normal)
  - 12.8-13.2V = 25-50% (moderate)
  - 12.0-12.8V = 10-25% (low)
  - <12.0V = critical (charge ASAP)

**Dedicated fuel gauge ICs are unnecessary** for this application — the ESP32 ADC + voltage divider is sufficient because:
1. LiFePO4 has a flat discharge curve (voltage-based SOC is reasonable)
2. We also monitor stator charging voltage, so we see charge state
3. We estimate fuel consumption per mode (mL/100km), giving double redundancy

### Recommended LiFePO4 for NX650
- **4S LiFePO4 12.8V 6Ah** (~€80-120) — saves 2kg vs lead-acid
- Cold cranking: 300A+ (more than enough for NX650's kickstart/electric start)
- Drop-in replacement for YTX7L-BS (NX650 OEM battery)

## 8. v2.2 Component Price List (New/Changed)

|| Component | Qty | Price | Notes |
||-----------|-----|-------|-------|
| ESP32-WROOM-32 DevKit | 1 | €6 | Main controller |
| SSD1306 OLED 128x64 I2C | 1 | €3 | Display (0.96") |
| KY-040 Rotary Encoder | 1 | €2 | Mode switching |
| WS2812B RGB LED (single) | 1 | €1 | Mode indicator |
| DRV8833 H-bridge | 1 | €3 | Exhaust valve motor driver |
| Pololu 37Dx52L gearmotor | 1 | €25 | Exhaust valve actuator |
| AS5600 magnetic encoder | 2 | €10 | Position feedback (exhaust + airbox) |
| Neodymium magnet 6x2.5mm | 2 | €2 | For AS5600 |
| Ignitech DC-CDI-P2 | 1 | €120 | Programmable CDI (2-map) |
| NTC 10kΩ thermistor | 1 | €2 | Cylinder head temp |
| Oil pressure switch | 1 | €5 | Engine protection |
| 7805 voltage regulator | 1 | €1 | 12V→5V |
| SMAJ28A TVS diode | 1 | €0.5 | Overvoltage protection |
| Capacitors + resistors | — | €3 | Voltage dividers, filtering |
| 3D printed case (PETG) | 1 | €15 | IP67 handlebar mount |
| Sealed buttons (IP67) | 2 | €6 | Mode+ and Mode- |
| **Total** | | **~€205** | |

### v2.2 Additions:
- OTA WiFi update module (no hardware cost — uses ESP32 built-in WiFi)
- Gear estimator (software only — no new hardware)
- Fuel estimator (software only — uses existing ADC)
- Deep sleep (software only — ESP32 built-in)

## 9. Stator Health Monitoring — Critical for NX650

The NX650 stator is a **known weak point**. Common failure modes:
1. **Stator coil insulation breakdown** → shorted turns → reduced output
2. **Regulator/rectifier failure** → overcharging → battery boil
3. **Stator connector melting** → poor contact → intermittent charging

**v2.2 detection strategy:**
- Monitor stator output voltage at regulator (GPIO36 + voltage divider)
- At 3000+ RPM, healthy charging: 13.0V-14.8V
- Below 12.5V at cruise RPM: **stator failing** (yellow warning)
- Below 12.0V: **stator critical** (red warning, reduced electrical load)
- Above 15.5V: **regulator failing** (red warning, stop riding)

**Preventive actions:**
1. Replace OEM stator connector with a better one (bullet connectors or Deutsch DT)
2. Replace OEM regulator/rectifier with a MOSFET type (Shindengen SH775 or FH020AA)
3. Monitor regularly via BLE data logging

## 10. OTA WiFi Update — ESP32 Firmware Upload v2.2

The v2.2 firmware includes an OTA (Over-The-Air) update capability:

### How it works:
- **Activation:** Hold encoder button during ESP32 boot → enters OTA mode
- **WiFi AP:** ESP32 creates "AQL-OTA" network (password: aql2026)
- **Web Interface:** http://192.168.4.1 — upload .bin firmware file
- **Security:** Only activates on boot with encoder held — cannot be triggered while riding
- **Power:** ESP32 AP mode draws ~80mA — acceptable for short update sessions

### Build & Upload process:
```
# Build firmware
cd projects/african-queen-lite/dashboard
pio run -e esp32dev

# The .bin file is at:
# .pio/build/esp32dev/firmware.bin

# OTA upload: hold encoder, power on, connect to AQL-OTA WiFi, upload .bin
```

### Recovery:
- If OTA fails, flash via USB: `pio run -t upload`
- Deep sleep wake: ignition pulse or MODE_UP button wakes ESP32
- Factory reset: hold both buttons during boot

## 11. Display UX — v2.2 Layout

SSD1306 128x64 OLED (4 auto-cycling pages):

**Page 0 (RIDE):**
- Line 1: Mode name (3 chars) + Gear indicator + RPM (big)
- Line 2: Temperature + Voltage
- Line 3: Valve % + Airbox %
- Line 4: Oil pressure + CDI map
- Line 5: Throttle curve + Fuel remaining (L)
- Bottom: Fuel bar [=====.........]

**Page 1 (HEALTH):** Stator status, battery SOC, runtime
**Page 2 (MAINT):** Maintenance items with overdue warnings
**Page 3 (TRIP):** Odometer, trip, peak temp, stator/battery summary

---

## 5. StVZO Legal Research — Custom Ignition & Exhaust on NX650

### Programmable CDI — Legal Status
- **StVZO §55a**: Zündzeitpunkt may only be changed with type-approved parts
- **In practice**: Programmable CDI is legal IF it doesn't exceed the manufacturer's original timing range
- The NX650 RFVC has a single ignition map — adding 3 maps is a gray area
- **Recommendation**: Map C (standard) = OEM-equivalent timing. Maps A and B should stay within ±3° of specification
- **Key risk**: TÜV inspection will check exhaust emissions and noise — not ignition timing specifically

### Exhaust Valve — Legal Status
- **StVZO §49**: Abgasanlagen must be type-approved (EG-Betriebserlaubnis)
- A custom exhaust valve in a modified exhaust system requires:
  - EG-Betriebserlaubnis for the complete exhaust system
  - Or: Einzelabnahme (individual approval) via TÜV
- **Sound mode**: In STADT mode (valve closed), the bike must still meet the 80dB(A) limit at 5m
- **Exhaust valve retrofit**: Legal if the valve is part of a type-approved exhaust system (Akrapovič, Yoshimura with EXUP)
- **DIY exhaust valve**: Requires Einzelabnahme — feasible but requires documentation

### Display on Handlebar — Legal Status
- **StVZO §23**: Instruments and displays are allowed if they don't obstruct the rider's view
- OLED/TFT displays are legal — many factory bikes have them (Ducati, KTM, BMW)
- The display must not show video or entertainment content while riding
- Our display shows only vehicle data — fully legal

### LED Indicator — Legal Status
- **StVZO §51**: Light fixtures must be type-approved
- A single WS2812 LED for mode indication is legal as a supplementary indicator
- Must not be confused with turn signals or other required lights
- Colors: Avoid flashing red/blue (emergency vehicle) — our mode colors are fine

### Lenker-Schalter (Handlebar Switches) — Options
Weatherproof handlebar switches rated for motorcycle use:
1. **HealTech QR Quickshifter buttons** — waterproof, OEM-quality (~€25)
2. **Domino MX095** — 22mm bar mount, IP67, used on rally bikes (~€15)
3. **Trail Tech 2-button switch** — ATV/motorcycle rated, IP68 (~€20)
4. **Custom 3D-printed housing with sealed microswitches** — best for our encoder mount (~€10-15)

### OLED vs TFT bei Sonnenlicht
- **SSD1306 OLED (128x64)**: Good contrast, readable in shade, washes out in direct sun. Current draw: ~10mA
- **SSD1306 with inverted mode**: White-on-black becomes black-on-white — much better in direct sunlight
- **IPS TFT (ST7789, 1.3")**: Excellent in sunlight, faster refresh, but higher power (~30-50mA)
- **Transflective LCD (NOA1 style)**: Best in sunlight, nearly zero power in daylight, but monochrome
- **Decision**: SSD1306 with v2.1 sunlight inversion mode is ADEQUATE for motorcycle use
  - The inverted mode (v2.1) makes it readable in direct sun
  - Low power draw preserves battery
  - For v2.3: Consider adding an auto-brightness sensor (LDR on GPIO) for future TFT upgrade

---

## 6. v2.3 Development Notes

### Speed Input Module (NEW)
- GPS NMEA on Serial2 (GPIO14/GPIO15) — primary speed source
- Wheel hall sensor on GPIO39 (input-only pin) — secondary source
- Fallback to RPM-based estimation when no GPS/sensor
- Priority: GPS > Wheel > RPM estimate
- EMA filter (α=0.3) for GPS speed smoothing

### Smooth Mode Transitions (NEW)
- ModeTransition class interpolates servo positions over 1.5s
- easeInOutCubic curve for natural servo feel
- CDI map changes are still instant (engine safety)
- LED changes instant (visual feedback)

### Dedicated Airbox RPM Curves (IMPROVED)
- Airbox resonance is different from exhaust backpressure
- STADT mode: airbox mostly closed (quiet intake), exhaust partially open (scavenging)
- SOUND mode: both wide open for maximum acoustic output
- Airbox has narrower effective RPM band — different curve shape than exhaust

### Rev Limiter Soft-Cut (NEW)
- 3-stage progressive limiter per mode:
  1. Soft-cut: timing retard begins (gradual power reduction)
  2. Hard-cut: full retard + cylinder dropout (strong limit)
  3. Hard-limit: absolute no-spark cutoff (safety)
- STADT/COMFORT: earlier limiter for fuel economy (6800 RPM)
- GELÄNDE/SPORT: higher limiter for power (7600 RPM)
- Soft-cut timing retard applied via CDI map offset

### Pin Assignment Changes (v2.3)
- GPIO 14: GPS UART2 TX (was DRV8833 AIN2 in production mode — now shared)
- GPIO 15: GPS UART2 RX (was unused)
- GPIO 39: Wheel speed hall sensor (was unused — input-only pin)
- Note: GPS and DRV8833 share GPIO14. When in production motor mode, GPS must use alternative pins or be disabled via compile flag
