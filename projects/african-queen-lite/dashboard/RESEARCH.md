# African Queen Lite — Ride-Mode Controller Research

## 1. ESP32 vs Arduino vs Teensy — Motorcycle Controller

| Feature | ESP32-WROOM-32 | Arduino Mega 2560 | Teensy 4.0 |
|---------|---------------|-------------------|-------------|
| **GPIO** | 34 usable | 54 (5V only) | 40 (3.3V) |
| **PWM** | 16 hardware LEDC | 15 (8-bit) | 12 (16-bit timers) |
| **WiFi/BT** | WiFi + BLE built-in | None | None (add-on) |
| **CPU** | 240 MHz dual-core | 16 MHz | 600 MHz Cortex-M7 |
| **Power** | ~80 mA (WiFi on) | ~50 mA | ~100 mA |
| **Temp Range** | -40°C to +85°C | -40°C to +85°C | -40°C to +105°C |
| **Price** | ~€5-8 | ~€15 | ~€25 |

**Winner: ESP32** — Built-in BLE for smartphone logging, enough GPIOs for all sensors+outputs, dual-core (one core for BLE, one for real-time control), cheap, large ecosystem.

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
- AS5600 magnetic encoder (I²C, non-contact, vibration-resistant) (~€3)
- PID position control via ESP32

Initial build uses standard RC servo (MG996R) for prototyping, upgrade to gearmotor later.

## 3. Programmable CDI for NX650 RFVC

### Options
| Unit | Price | Adjustable | Notes |
|------|-------|-----------|-------|
| **Ignitech DC-CDI-P2** | ~€150 | Timing curve via PC | Best option — proven, adjustable |
| VAPE / Spark Moto | ~€100 | Limited | Kickstart-oriented |
| MicroSquirt ECU | ~€300+ | Full EFI | Overkill for NX650 |

### ESP32 + CDI Integration
**ESP32 does NOT generate spark directly.** Instead:
1. Buy Ignitech DC-CDI-P2 with two pre-programmed timing maps (Map A: base, Map B: advanced)
2. ESP32 switches between maps via a single GPIO pin (LOW = Map A, HIGH = Map B)
3. Each ride mode selects Map A or Map B accordingly

**Future DIY CDI:** Would require Teensy 4.0 (better interrupt latency) + Quadspark ignition coil driver. Not recommended for v1.

## 4. StVZO (German Road Regulations)

| Modification | Legal? | Requirements |
|-------------|--------|-------------|
| Programmable CDI | ⚠️ Gray area | Must stay within OEM emissions specs; may need Einzelbetriebserlaubnis |
| Exhaust valve | ⚠️ Gray area | Counts as exhaust modification; needs TÜV if affects noise/emissions |
| Auxiliary display | ✅ Generally OK | Must not obstruct view or distract; keep stock instruments |
| Handlebar switches | ✅ OK | Must be securely mounted; no sharp edges |
| LED indicators | ✅ With ABE | Need ABE or TÜV approval |

**Recommendation:** Keep stock CDI initially. Add ride-mode controller as auxiliary system. Exhaust valve only for track/off-road use unless TÜV approved.

## 5. Handlebar Switches

| Product | Type | IP Rating | Price | Notes |
|---------|------|-----------|-------|-------|
| **Cyclops Adventure Switch** | Push button | IP68 | ~€25 | Best for mode up/down |
| **Touratech Switch Pod** | 2-button + hold | IP67 | ~€40 | OEM adventure quality |
| **Trail Tech Waterproof** | 2-3 button, illuminated | IP67 | ~€30-50 | Off-road proven |
| **Hella 957110301** | 19mm panel mount | IP69K | ~€20 | Very robust |

**Recommended:** 2x Cyclops Adventure Switch (Mode+/Mode-) + 1x Touratech Switch Pod (confirm/action). Use Deutsch DT connectors for wiring.

## 6. Display — OLED vs TFT

| Feature | 1.3" OLED (SSD1306) | 2.4" TFT (ILI9341) |
|---------|---------------------|---------------------|
| Resolution | 128×64 | 320×240 |
| Sunlight | ✅ Excellent (emissive) | ❌ Poor (needs shade) |
| Power | ~20-30 mA | ~80-120 mA |
| Contrast | Infinite (true black) | ~1000:1 |
| Size | Small (info only) | Large (menus, graphs) |

**Decision: 1.3" OLED (SSD1306)** for ride-mode display — superior sunlight readability, low power, simple text+icons sufficient for core info. Optional: 2.4" TFT with sunshade for extended data.

## Summary of Actionable Recommendations

1. **Controller:** ESP32 DevKit + power conditioning (TVS, caps, LDO)
2. **Exhaust Valve:** Phase 1: MG996R servo (prototype) → Phase 2: Pololu gearmotor + AS5600
3. **CDI:** Buy Ignitech DC-CDI-P2, ESP32 selects Map A/B via GPIO
4. **StVZO:** Keep as auxiliary system, exhaust valve track-only initially
5. **Switches:** 2× Cyclops Adventure Switch, Deutsch DT connectors
6. **Display:** 1.3" SSD1306 OLED (I²C)
7. **LED:** 1× WS2812 RGB LED for mode color indicator