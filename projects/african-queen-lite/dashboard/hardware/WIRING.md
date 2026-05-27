# African Queen Lite — Wiring Diagram & Hardware Guide v2.0

## ESP32 Pin Assignment (Updated for v2.0)

```
ESP32 DevKit V1 — Pin Mapping v2.0
====================================

INPUTS:
  GPIO 4  ← Mode+ button (handlebar, pullup to 3.3V)
  GPIO 5  ← Mode- button (handlebar, pullup to 3.3V)
  GPIO 0  ← Encoder push button (BOOT pin, internal pullup)
  GPIO 16 ← Encoder A (CLK, interrupt)
  GPIO 17 ← Encoder B (DT)
  GPIO 18 ← Ignition pulse coil (interrupt, optocoupler input)
  GPIO 19 ← Oil pressure switch (LOW = pressure OK)
  GPIO 34 ← ADC: Thermistor (NTC 10kΩ voltage divider)
  GPIO 35 ← ADC: Battery voltage divider
  GPIO 36 ← ADC: Stator/regulator voltage divider (NEW v2.0)

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
    ├── Voltage Divider #1 (for ADC battery monitoring)
    │       R1 = 100kΩ (to battery+)
    │       R2 = 33kΩ (to GND)
    │       Junction → GPIO 35
    │
    └── Voltage Divider #2 (for ADC stator monitoring) [NEW v2.0]
            R1 = 100kΩ (to regulator output+, after key switch)
            R2 = 33kΩ (to GND)
            Junction → GPIO 36
```

## Thermistor Circuit (Cylinder Head Temperature)

```
3.3V ─── 10kΩ pull-up ───┬─── NTC 10kΩ (in cylinder head) ─── GND
                          │
                          └─── GPIO 34 (ADC)
```

### Thermistor placement
- **Location**: Bolt the NTC sensor to one of the cylinder head fins (use thermal paste)
- **Alternative**: Replace the OEM temperature sending unit (if NX650 has one)
- **Wire**: Use high-temperature silicone wire (≥200°C rated) for the sensor leads
- **Heatshield**: Wrap wires in fiberglass sleeving near exhaust

## Stator Voltage Sensing Circuit (NEW v2.0)

```
Regulator/Rectifier Output (12V+ when running)
    │
    ├── R1 = 100kΩ (1/4W, to regulator output+)
    │
    ├── C1 = 100nF Ceramic Cap (to GND, HF filtering)
    │
    ├── R2 = 33kΩ (to GND)
    │
    └─── Junction → GPIO 36 (ADC)

Purpose: Monitor charging system health.
- At 3000+ RPM, voltage should be 13.0V-14.8V
- Below 12.5V at cruise RPM → stator failing
- Above 15.5V → regulator/rectifier failing
```

## Rotary Encoder Wiring (NEW v2.0)

```
KY-040 Rotary Encoder:
    CLK  → GPIO 16 (with 10kΩ pullup to 3.3V)
    DT   → GPIO 17 (with 10kΩ pullup to 3.3V)
    SW   → GPIO 0  (with internal pullup)
    +    → 3.3V
    GND  → GND

Recommended encoder: KY-040 with custom knob
- Waterproof: Add silicone sealant around shaft
- Alternative: Apem 5620 series (IP67, motorcycle-rated)
- Knob: Large knurled aluminum, easy to grip with gloves
```

## Ignition Pulse Pickup Circuit

```
NX650 Pulse Generator Coil (output: ~0.5-5V AC pulse)
    │
    ├── 10kΩ current limiting resistor
    │
    ├── PC817 Optocoupler (isolate ESP32 from ignition)
    │       Anode → through 10kΩ resistor
    │       Cathode → GND (motorcycle side)
    │       Collector → GPIO 18 (with 10kΩ pullup to 3.3V)
    │       Emitter → GND (ESP32 side)
    │
    └── 100nF cap (noise filtering)
```

## Exhaust Valve Servo Wiring

### Production (Recommended): DRV8833 + Gearmotor + AS5600

```
ESP32 GPIO 25 (PWM) → DRV8833 IN1
ESP32 GPIO 26 (PWM) → DRV8833 IN2 (airbox flap alternative)

DRV8833 Motor Driver:
    IN1 = GPIO 25 (PWM exhaust valve)
    IN2 = GPIO 26 (PWM airbox flap, if using same driver)
    VCC = 3.3V (logic)
    VM  = 12V (motor power from battery through fuse)
    GND = GND
    OUT1/OUT2 → Exhaust valve gearmotor
    OUT3/OUT4 → Airbox flap gearmotor

AS5600 Magnetic Encoder (I²C, exhaust valve position feedback):
    VDD = 3.3V
    SDA = GPIO 21 (shared I²C bus with OLED)
    SCL = GPIO 22 (shared I²C bus with OLED)
    GND = GND
```

### Prototype (Testing Only): Standard RC Servo

```
ESP32 GPIO 25 → Exhaust valve servo signal (Orange wire)
ESP32 GPIO 26 → Airbox flap servo signal (Orange wire)

Servo Power:
    Red wire   → 5V (from 7805 regulator)
    Brown wire → GND
    Orange wire → GPIO 25/26 (PWM signal)

⚠️ WARNING: RC servos (SG90/MG996R) are NOT suitable for production!
    - Heat damage at exhaust proximity (>80°C)
    - Vibration-induced failure
    - No position feedback for fault detection
    Use gearmotor + DRV8833 + AS5600 for production.
```

## CDI Map Select Wiring

```
ESP32 GPIO 27 → CDI Map Select Line

Ignitech DC-CDI-P2:
    Map Select Pin → GPIO 27 (through 1kΩ resistor)
    LOW = Map A (base/retarded timing)
    HIGH = Map B (advanced timing)

If no programmable CDI available:
    GPIO 27 → LED indicator only (shows recommended timing)
    Actual timing change must be done manually via CDI software
```

## WS2812 LED Indicator Wiring

```
ESP32 GPIO 32 → WS2812 LED Data (through 470Ω resistor)
WS2812 LED:
    VCC → 5V (from 7805 regulator)
    GND → GND
    DIN → GPIO 32 (through 470Ω series resistor)
    DOUT → (next LED, if chaining)

Mounting: 3D-printed bracket on handlebar, IP67 sealed
Shows: Green=Stadt, Blue=Strasse, Red=Gelände, Orange=Sport,
       Violet=Comfort, Cyan=Sound, Flashing Red=Alert
```

## Complete System Wiring Summary

```
┌─────────────────────────────────────────────────────────┐
│                    ESP32 DevKit V1                       │
│                                                         │
│  GPIO 0  ← Encoder SW (internal pullup)               │
│  GPIO 4  ← Mode+ Button (pullup)                      │
│  GPIO 5  ← Mode- Button (pullup)                      │
│  GPIO 16 ← Encoder A (pullup)                          │
│  GPIO 17 ← Encoder B (pullup)                          │
│  GPIO 18 ← Ignition Pulse (optocoupler)                │
│  GPIO 19 ← Oil Pressure Switch (pullup)               │
│  GPIO 21 → I²C SDA (OLED + AS5600)                    │
│  GPIO 22 → I²C SCL (OLED + AS5600)                    │
│  GPIO 25 → Exhaust Valve Servo PWM                     │
│  GPIO 26 → Airbox Flap Servo PWM                       │
│  GPIO 27 → CDI Map Select                              │
│  GPIO 32 → WS2812 LED Data                              │
│  GPIO 34 ← ADC Thermistor                               │
│  GPIO 35 ← ADC Battery Voltage                          │
│  GPIO 36 ← ADC Stator Voltage                           │
│                                                         │
│  VIN ← 5V (7805 regulator)                              │
│  3V3 ← Internal regulator                               │
│  GND ← Common ground                                    │
└─────────────────────────────────────────────────────────┘

Power budget:
    ESP32 + WiFi/BT:  ~80 mA @ 3.3V  = 0.26W
    OLED SSD1306:     ~20 mA @ 3.3V   = 0.07W
    WS2812 LED:       ~60 mA @ 5V     = 0.30W
    Servos (2):       ~500 mA @ 5V    = 2.50W (peak, moving)
    DRV8833 logic:    ~10 mA @ 3.3V   = 0.03W
    ────────────────────────────────────────
    Total average:    ~200 mA @ 12V    = 2.4W
    Peak (servos):    ~700 mA @ 12V    = 8.4W
    
    NX650 Stator output: ~180W @ 5000 RPM (15A @ 12V)
    Headlight: ~55W (H4 bulb)
    Available: ~120W — MORE than enough for controller
```

## 3D-Printed Enclosure

```
Design Requirements:
    - IP67 waterproof (gasket + silicone seal)
    - Handlebar mount (22mm clamp, rubber-damped)
    - Sunlight-readable OLED position (angled ~15°)
    - Encoder protrudes through top (sealed shaft)
    - Cable glands for all external connections
    - Internal mounting for ESP32 + DRV8833
    
Material: PETG or ABS (heat resistant, not PLA!)
Wall Thickness: 3mm minimum
Print Settings: 0.2mm layers, 40% infill, 3 perimeters
```

## Fuses & Protection

```
Circuit            Fuse Rating    Wire Gauge
─────────────────  ───────────   ──────────
Main 12V input     5A            18 AWG
Servo power        3A            20 AWG
ESP32 5V supply    500mA        22 AWG (polyfuse on 7805)
Sensor inputs      —             24 AWG (signal level)
OLED I²C           —             26 AWG

All fuses: automotive blade fuses (water-resistant housings)
All external connections: Deutsch DT or Superseal connectors (IP67)
```