# African Queen Lite — Wiring Diagram & Hardware Guide

## ESP32 Pin Assignment

```
ESP32 DevKit V1 — Pin Mapping
================================

INPUTS:
  GPIO 4  ← Mode+ button (handlebar, pullup to 3.3V)
  GPIO 5  ← Mode- button (handlebar, pullup to 3.3V)
  GPIO 18 ← Ignition pulse coil (interrupt, optocoupler input)
  GPIO 19 ← Oil pressure switch (LOW = pressure OK)
  GPIO 34 ← ADC: Thermistor (NTC 10kΩ voltage divider)
  GPIO 35 ← ADC: Battery voltage divider

OUTPUTS:
  GPIO 25 → PWM: Exhaust valve servo
  GPIO 26 → PWM: Airbox flap servo
  GPIO 27 → CDI map select (LOW = Map A, HIGH = Map B)
  GPIO 32 → WS2812 RGB LED data

I2C (OLED):
  GPIO 21 → SDA (OLED SSD1306)
  GPIO 22 → SCL (OLED SSD1306)

POWER:
  VIN ← 5V (from 7805 regulator, input from motorcycle battery)
  3V3 ← Internal regulator (for sensors, OLED)
```

## Power Supply Circuit

```
Motorcycle Battery (12V, stator-charged)
    │
    ├── 1N5408 Reverse Polarity Protection Diode
    │
    ├── SMAJ28A TVS Diode (28V clamp)
    │
    ├── 470µF Electrolytic Cap (bulk filtering)
    │
    ├── 100nF Ceramic Cap (HF decoupling)
    │
    ├── 7805 Voltage Regulator → 5V/1A
    │       │
    │       └── ESP32 VIN (5V input)
    │
    └── Voltage Divider (for ADC battery monitoring)
            R1 = 100kΩ (to battery+)
            R2 = 33kΩ (to GND)
            Junction → GPIO 35
```

## Thermistor Circuit (Cylinder Head Temperature)

```
3.3V ─── 10kΩ pull-up ───┬─── NTC 10kΩ (in cylinder head) ─── GND
                          │
                          └─── GPIO 34 (ADC)
```

NTC 10kΩ (B=3950) typical for engine temperature sensing.
Use waterproof probe (e.g., DS18B20-compatible housing or brass M6 thread).

## Oil Pressure Switch

```
GPIO 19 ─── Pull-up 10kΩ ─── 3.3V
    │
    └─── Oil pressure switch ─── GND
         (Switch closes to GND when pressure OK)
         NX650: Green/Blue wire from oil pressure sender
```

## Ignition Pulse Input (RPM)

```
Pulse Generator Coil (NX650 left crankcase cover)
    │
    ├── 4N35 Optocoupler (isolation)
    │       Anode → 1kΩ → Pulse coil +
    │       Cathode → Pulse coil -
    │       Collector → GPIO 18 (pull-up 10kΩ to 3.3V)
    │       Emitter → GND
    │
    └── Or: LM393 comparator with hysteresis
```

## Servo Connections

```
Exhaust Valve Servo (MG996R or custom gearmotor):
    VCC → 5V (separate supply if >1A)
    GND → GND (common)
    Signal → GPIO 25 (PWM 50Hz)

Airbox Flap Servo:
    VCC → 5V
    GND → GND (common)
    Signal → GPIO 26 (PWM 50Hz)

NOTE: Do NOT power servos from ESP32 3.3V/5V regulator!
Use separate BEC or direct from 7805 with adequate capacitor bank.
```

## OLED Display Connection

```
SSD1306 1.3" OLED (I²C):
    VCC → 3.3V
    GND → GND
    SDA → GPIO 21
    SCL → GPIO 22
```

## WS2812 LED

```
WS2812 RGB LED:
    VCC → 5V
    GND → GND
    DIN → GPIO 32 (via 470Ω series resistor)
    1000µF cap across VCC/GND (WS2812 protection)
```

## Handlebar Switch Wiring

```
Mode+ Button (Cyclops Adventure Switch):
    Pin 1 → 3.3V (via internal pull-up on GPIO 4)
    Pin 2 → GPIO 4 (active LOW)
    IP68 rated, rubber boot

Mode- Button (Cyclops Adventure Switch):
    Pin 1 → 3.3V (via internal pull-up on GPIO 5)
    Pin 2 → GPIO 5 (active LOW)
    IP68 rated, rubber boot

All wiring through Deutsch DT connectors (IP67).
Route along handlebar inside braided sleeving.
```

## 3D-Printed Enclosure Notes

- **Material:** PETG or ABS (heat resistant to 80°C+)
- **IP Rating:** Target IP67 with gasket (silicone or neoprene O-ring)
- **Mount:** Handlebar clamp mount (22mm or 1" bar)
- **Cable exits:** Bottom-facing, with drip loops
- **Ventilation:** Small breather hole with Gore-Tex patch for pressure equalization
- **Display window:** 1mm polycarbonate cover, anti-glare coating
- **LED window:** Small clear window for WS2812

## CDI Map Select Integration

```
ESP32 GPIO 27 (CDI_MAP_SELECT)
    │
    ├── LOW (0V) → Ignitech Map A (base timing / eco)
    └── HIGH (3.3V) → Ignitech Map B (advanced timing / sport)

Connect to Ignitech DC-CDI-P2 "Map Select" input.
If Ignitech is NOT installed, this output is unused (no-op).
```