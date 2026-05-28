# African Queen Lite — Wiring Diagram & Hardware Guide v2.2

## ESP32 Pin Assignment (Updated for v2.2)

```
ESP32 DevKit V1 — Pin Mapping v2.2
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
  GPIO 36 ← ADC: Stator/regulator voltage divider

OUTPUTS:
  GPIO 25 → PWM: Exhaust valve servo
  GPIO 26 → PWM: Airbox flap servo
  GPIO 27 → CDI map select A (active LOW)
  GPIO 33 → CDI map select B (active LOW)
  GPIO 32 → WS2812 RGB LED data

DRIVER OUTPUTS (DRV8833 production mode):
  GPIO 14 → DRV8833 AIN1 (Exhaust valve motor)
  GPIO 13 → DRV8833 AIN2 (Exhaust valve motor)
  GPIO 23 → DRV8833 BIN1 (Airbox flap motor)
  GPIO 2  → DRV8833 BIN2 (Airbox flap motor)

I2C (shared bus):
  GPIO 21 → SDA (OLED SSD1306 + AS5600 exhaust @ 0x36 + AS5600 airbox @ 0x37)
  GPIO 22 → SCL (OLED SSD1306 + AS5600 encoders)

POWER:
  VIN ← 5V (from 7805 regulator, input from motorcycle battery)
  3V3 ← Internal regulator (for sensors, OLED)
```

## Power Supply Circuit

```
Motorcycle Battery (12V LiFePO4 4S, stator-charged)
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
    └── Voltage Divider #2 (for ADC stator monitoring)
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

## Stator Voltage Sensing Circuit

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
- Below 12.5V at cruise RPM → stator failing (yellow warning)
- Below 12.0V → stator critical (red warning)
- Above 15.5V → regulator/rectifier failing (red warning)
```

## Rotary Encoder Wiring

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
- Long press (3 sec) → Config Mode (v2.2 NEW)
```

## CDI 3-Map Control (Ignitech DC-CDI-P2)

```
ESP32 GPIO 27 ─────── CDI Map A (active LOW = Map A selected)
ESP32 GPIO 33 ─────── CDI Map B (active LOW = Map B selected)

CDI Map Selection:
  Map A (eco/retarded)  : GPIO27=LOW,  GPIO33=HIGH  → STRASSE, STADT, COMFORT
  Map B (advanced/sport) : GPIO27=HIGH, GPIO33=LOW   → GELÄNDE, SPORT
  Map C (fallback/standard): GPIO27=HIGH, GPIO33=HIGH → SOUND, Emergency
```

## Deep Sleep Wake Circuit (v2.2 NEW)

```
ESP32 Deep Sleep (5 min engine off → ~10µA):

Wake Sources:
  EXT0: GPIO 4 (Mode+ button) → wake on LOW (button press)
  EXT1: GPIO 18 (Ignition pulse) → wake on HIGH (engine start)

Behavior:
  1. Engine off for >5 minutes → save state → deep sleep
  2. Press Mode+ OR start engine → wake → full reboot → restore mode
  3. Display shows "WAKE:" + reason on startup
  4. All peripherals re-initialized on wake
```

## DRV8833 Dual H-Bridge (Production Mode)

```
DRV8833 Motor Driver:
    VCC   ← 5V (from 7805 regulator)
    GND   ← GND
    AIN1  ← GPIO 14 (ESP32 PWM)
    AIN2  ← GPIO 13 (ESP32 PWM)
    BIN1  ← GPIO 23 (ESP32 PWM)
    BIN2  ← GPIO 2  (ESP32 PWM)
    A01/A02 → Exhaust valve gearmotor
    B01/B02 → Airbox flap gearmotor
    SLEEP   ← HIGH (always enabled)

AS5600 Magnetic Encoders (position feedback):
    Exhaust valve: I2C address 0x36 (shared SDA/SCL with OLED)
    Airbox flap:  I2C address 0x37 (shared SDA/SCL with OLED)
    
    Each AS5600 needs:
    - Neodymium magnet (6mm x 2.5mm diametric) glued to valve shaft
    - Sensor mounted 2-5mm from magnet (non-contact!)
    - Heat shield near exhaust (aluminum foil + fiberglass sleeve)
```

## v2.2 New Feature Wiring Summary

| Feature | HW Needed | Wiring |
|---------|-----------|--------|
| Auto-RPM Valve | None (software) | Uses existing servos+AS5600 |  
| Fuel Estimation | None (software) | Uses existing battery voltage ADC |
| Gear Detection | None (software) | Uses existing RPM + speed estimation |
| Deep Sleep | None extra | Uses existing GPIO4 (wake) + GPIO18 (wake) |
| Config Mode | None (software) | Uses existing encoder long-press |
| OTA Update | WiFi antenna | ESP32 built-in — no extra wiring |