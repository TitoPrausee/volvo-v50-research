# 🖥️ Custom Tacho — ESP32 TFT Speedometer für Honda NX650 Dominator

## Vision
**Vollständiger Ersatz des OEM-Kombiinstruments durch einen Custom-Tacho mit 3.5" TFT-Display, gesteuert vom selben ESP32 der bereits den Ride-Mode-Controller betreibt.**

OEM-Tacho zeigt nur: Geschwindigkeit, Drehzahl (analog), Tank, Öldruck-Warnleuchte.
Custom-Tacho zeigt: Speed, RPM, Gang, Tankinhalt in %, Öldruck, Temperatur, Spannung, Ride-Mode, Trip A/B, Uhrzeit, GPS-Position.

## Warum Custom-Tacho?
- **NX650 OEM-Tacho** ist rein mechanisch: Tachowelle vom Vorderrad, analoger Drehzahlmesser
- **Keine Elektronik** außer einer Öldruck-Warnleuchte und Tank-Füllstand
- **CDI-Zündung** = Pulse Generator Coil liefert RPM-Signal (das gleiche Signal das der ESP32 schon auswertet)
- **Kein CAN-Bus** — alle Signale sind analog/digital, kein Reverse-Engineering nötig
- **Volle Freiheit** bei Design, Alarmen, Datenlogging

---

## Architektur

```
┌──────────────────────────────────────────────────────┐
│                   ESP32 DevKit V1                      │
│                                                        │
│  Pulse Gen ──GPIO18──┐                                │
│  Hall Speed ──GPIO39─┤                                │
│  Thermistor──GPIO34──┤                                │
│  Volt-Div───GPIO35───┤──► sensors.h → Mode Switching │
│  Oil Press──GPIO19────┤                                │
│  Neutral────GPIO36────┘                                │
│                                                        │
│  ┌─────────────┐  ┌──────────┐  ┌─────────────┐     │
│  │ CDI Map Sel │  │ Servo    │  │ BLE NimBLE   │     │
│  │ GPIO27      │  │ PWM      │  │ UART2        │     │
│  └─────────────┘  └──────────┘  └─────────────┘     │
│                                                        │
│  ┌──────────────────────────────────────────────┐     │
│  │        3.5" ILI9488 TFT (480×320 SPI)        │     │
│  │  ┌──────┐┌──────┐┌──────┐┌──────┐┌────────┐ │     │
│  │  │ RPM  ││ SPEED││ GEAR ││ TEMP ││ FUEL   │ │     │
│  │  │      ││  km/h││  N   ││  °C  ││  ████  │ │     │
│  │  └──────┘└──────┘└──────┘└──────┘└────────┘ │     │
│  │  ┌──────┐┌──────┐┌────────┐┌──────────────┐│     │
│  │  │ VBAT ││ MODE ││  OIL ▼ ││  TRIP  A:    ││     │
│  │  │ 12.8V││🟢STR ││  PRESS  ││  247.3 km    ││     │
│  │  └──────┘└──────┘└────────┘└──────────────┘│     │
│  └──────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────┘
```

---

## Signale & Sensoren

### Eingangssignale (NX650-spezifisch)

| Signal | Quelle | GPIO | Typ | Beschreibung |
|--------|--------|------|-----|-------------|
| **RPM** | Pulse Generator Coil | GPIO18 | Interrupt | CDI-Pulsspule, 1 Puls/Kolbenhub (RFVC single-cylinder) = RPM × 1 |
| **Speed** | Hall-Sensor VR | GPIO39 | Interrupt | Magnete am Vorderrad (4-8 Pulse/Umdrehung) |
| **Temperatur** | NTC Thermistor | GPIO34 | ADC | Zylinderkopf (10kΩ NTC, Beta 3950) |
| **Batteriespannung** | Spannungsteiler | GPIO35 | ADC | 100kΩ/10kΩ Teiler, Vmax≈16V |
| **Öldruck** | Öldruckschalter | GPIO19 | Digital | LOW=Öldruck OK, HIGH=WARNUNG |
| **Neutral** | Neutral-Schalter | GPIO36 | Digital | LOW=Neutral eingelegt |
| **Tankinhalt** | Tankgeber (variabel) | GPIO4* | ADC | OEM-Widerstandsgeber, 10-180Ω |
| **Gang** | abgeleitet | — | Berechnet | Speed/RPM-Verhältnis → Gang-Erkennung |

*GPIO für Tankgeber = ADC1_PIN, muss noch festgelegt werden (GPIO4 oder GPIO13)

### Ausgangssignale

| Signal | Ziel | GPIO | Typ |
|--------|------|------|-----|
| TFT-Data | ILI9488 Display | GPIO23 MOSI | SPI |
| TFT-CLK | ILI9488 Display | GPIO18 SCLK | SPI (shared mit Pulse Gen — **KONFLIKT!**) |
| TFT-DC | ILI9488 Display | GPIO21 | Digital |
| TFT-CS | ILI9488 Display | GPIO5 | Digital |
| TFT-RST | ILI9488 Display | GPIO22 | Digital |
| TFT-BL | Backlight PWM | GPIO15 | PWM |
| LED-Data | WS2812 RGB | GPIO32 | Bit-bang |

---

## ⚠️ GPIO-Konflikt Resolution

**Problem:** Ride-Mode-Controller und TFT-Display teilen sich den ESP32, aber die Pin-Belegung hat Konflikte:
- GPIO18 = SCLK (SPI/TFT) **UND** Pulse Generator (RPM) ← **KONFLIKT!**
- GPIO21/22 = I²C (OLED) **UND** TFT-DC/RST ← **KONFLIKT!**

**Lösung:**
1. **RPM-Signal** auf **GPIO13** (ADC2, unterstützt Interrupts) statt GPIO18 → SCLK bleibt auf GPIO18
2. **OLED wird ersetzt durch TFT** → I²C-Pins (GPIO21/22) werden zu TFT-DC/RST
3. **I²C Brauchbar für Tankgeber** →(GPIO21 = SDA für I²C Expander falls nötig, oder als reiner Digital-Pin)

### Neue Pin-Belegung (Custom-Tacho + Ride-Mode)

| Funktion | GPIO | Bemerkung |
|----------|------|-----------|
| **TFT-MOSI** | GPIO23 | SPI Data |
| **TFT-SCLK** | GPIO18 | SPI Clock |
| **TFT-DC** | GPIO21 | Data/Command |
| **TFT-CS** | GPIO5 | Chip Select |
| **TFT-RST** | GPIO22 | Reset |
| **TFT-BL** | GPIO15 | Backlight PWM |
| **RPM (Pulse Gen)** | GPIO13 | Interrupt-fähig ✅ |
| **Hall Speed** | GPIO39 | VP, Interrupt |
| **Thermistor** | GPIO34 | ADC1 |
| **Voltage** | GPIO35 | ADC1 |
| **Öldruck** | GPIO19 | Digital Input |
| **Neutral** | GPIO36 | VP, Digital Input |
| **Tankgeber** | GPIO4 | ADC1 (oder I²C Expander) |
| **Exhaust Valve** | GPIO25 | PWM |
| **Airbox Flap** | GPIO26 | PWM |
| **CDI Map Select** | GPIO27 | Digital Out |
| **LED WS2812** | GPIO32 | Bit-bang |
| **BLE TX** | GPIO17 | UART2 |
| **BLE RX** | GPIO16 | UART2 |
| **Mode+** | GPIO14 | Button |
| **Mode-** | GPIO27* | Button (*shared mit CDI? → auf GPIO33 verschieben*) |

→ **GPIO27** = CDI Map Select (Output) **UND** Mode- (Input) ← **KONFLIKT!**
→ Mode- auf **GPIO33** verschieben (nur Input, funktioniert)

### Finale Pin-Tabelle

| Funktion | GPIO | Typ | Modus |
|----------|------|-----|-------|
| TFT-MOSI | 23 | SPI MOSI | Output |
| TFT-SCLK | 18 | SPI SCLK | Output |
| TFT-DC | 21 | Digital | Output |
| TFT-CS | 5 | Digital | Output |
| TFT-RST | 22 | Digital | Output |
| TFT-BL | 15 | PWM | Output |
| RPM Pulse | 13 | Interrupt | Input PULLUP |
| Hall Speed | 39 | Interrupt | Input PULLUP |
| Thermistor | 34 | ADC1 | Input |
| Voltage | 35 | ADC1 | Input |
| Öldruck | 19 | Digital | Input PULLUP |
| Neutral | 36 | Input only | Input PULLUP |
| Tankgeber | 4 | ADC1 | Input |
| Exhaust Valve | 25 | PWM | Output |
| Airbox Flap | 26 | PWM | Output |
| CDI Map Select | 27 | Digital | Output |
| LED WS2812 | 32 | Bit-bang | Output |
| BLE TX | 17 | UART2 TX | Output |
| BLE RX | 16 | UART2 RX | Input |
| Mode+/Shift+ | 14 | Digital | Input PULLUP |
| Mode-/Shift- | 33 | Digital | Input PULLUP |

---

## Display-Layouts

### Modus 1: Fahrmodus (Standard)

```
┌─────────────────────────────────────────┐
│  ┌───────────────┐   ┌───────────────┐  │
│  │    7,500      │   │     127       │  │
│  │    RPM ▮▮▮▮▮  │   │    km/h       │  │
│  └───────────────┘   └───────────────┘  │
│  ┌─────┐┌─────┐┌─────┐┌──────────────┐  │
│  │ 3rd ││ 12.8││ 78°C││ 🟢 STRASSE   │  │
│  │GEAR ││ VOLT││TEMP ││   MODE       │  │
│  └─────┘└─────┘└─────┘└──────────────┘  │
│  ┌─────┐┌──────────────┐┌────────────┐  │
│  │ ████││ ▼ OIL OK    ││ TRIP:247.3 │  │
│  │FUEL ││              ││ ODO:45,230 │  │
│  └─────┘└──────────────┘└────────────┘  │
│  12:45 │ GPS: 50.92°N 11.58°E │ SAT:8  │
└─────────────────────────────────────────┘
```

### Modus 2: Performance (Sport/Gelände)

```
┌─────────────────────────────────────────┐
│  ┌─────────────────────────────────────┐│
│  │        7,500  ████████████           ││
│  │         RPM   SHIFT ▲▲▲             ││
│  └─────────────────────────────────────┘│
│  ┌──────────────┐┌───────────────────┐ │
│  │    127 km/h  ││  G3 │12.8V│78°C  │ │
│  └──────────────┘└───────────────────┘ │
│  ┌──────────────┐┌───────────────────┐ │
│  │ FUEL ██████  ││ 🔴 GELÄNDE        │ │
│  └──────────────┘└───────────────────┘ │
│  LAP: 01:23.4 │ TRIP:47.2 │ BEST:01:19│
└─────────────────────────────────────────┘
```

### Modus 3: Diagnostic (Setup/Warning)

```
┌─────────────────────────────────────────┐
│  ┏━━ DIAGNOSTIC ━━━━━━━━━━━━━━━━━━━┓  │
│  ┃ Battery:  12.84V  ████░░  82%   ┃  │
│  ┃ Stator:   13.8V @2000rpm        ┃  │
│  ┃ Oil:      ✅ OK  2.1 bar        ┃  │
│  ┃ Temp:     78°C  ████░░  normal  ┃  │
│  ┃ Fuel:     78%  ████████░░░      ┃  │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
│  RPM Signal: ✅  7500 rpm            │
│  Speed:      ✅  127 km/h            │
│  GPS: 50.9234°N 11.5812°E  SAT:8    │
│  Mode: STRASSE  Uptime: 2h 34m      │
│  ▶ Hold both buttons for 3s: RESET  │
└─────────────────────────────────────────┘
```

---

## Speed-Berechnung

Die NX650 hat **keinen elektrischen Speedsensor** am Vorderrad — nur eine mechanische Tachowelle.

### Option A: Hall-Sensor am Vorderrad (Empfohlen)
- **Sensor:** Universal Hall-Sensor (z.B. KUS SL07 oder generic 3-Pin)
- **Magnete:** 4-8 Neodym-Magnete an Bremsscheibe/Radnabe befestigen
- **Formel:** `Speed = (Pulse_Count / Magnet_Count) × Radumfang × 3.6 × Zeitfaktor`
- **NX650 Bereifung:** 100/90-19 → Umfang ≈ 2.16m (berechnet: 622mm Felgendurchmesser + 90mm = 712mm, × π ≈ 2.237m)
- **Kalibrierung:** Gegen GPS abgleichen (Factor einstellbar)

### Option B: GPS-basiert
- **Modul:** GPS-NEO-6M oder NEO-M8N (UART, $10-15)
- **Vorteil:** Plug & Play, keine Mechanik
- **Nachteil:** Verzögerung ~1s, kein Signal in Tunneln, höherer Stromverbrauch
- **Kombi:** GPS als Referenz + Hall-Sensor als Primär, GPS für Odometer

### Option C: Tachowelle → Signalgeber
- **Mechanisch:** Tachowelle ab, Adapter mit Hall-Sensor zwischengesetzt
- **Nachteil:** Komplex, mechanisch fehleranfällig, teuer (Spezialanfertigung)

**→ Empfehlung: Option A (Hall-Sensor) + GPS als Backup/Odometer**

---

## RPM-Berechnung

Die NX650 Pulse Generator Coil liefert **1 Puls pro Kolbenhub**:
- **4-Takt Einzylinder:** 1 Puls alle 2 Kurbelwellenumdrehungen
- **Formel:** `RPM = (60 × Pulse_Count) / Zeitfenster_Sekunden / 2`
- **Alternativ (Interrupt):** `RPM = 60.000.000 / (Zeit_zwischen_Pulsen_µs × 2)`
- Die CDI liest dasselbe Signal — **keine Beeinträchtigung** weil hochohmiger Eingang

---

## Gang-Erkennung

Die NX650 hat **keinen Ganganzeige-Sensor**. Gang wird berechnet:

```cpp
// Übersetzungen NX650 (5-Gang)
constexpr float GEAR_RATIOS[] = {
    0,      // Neutral (not used)
    2.769,  // 1st gear
    1.824,  // 2nd gear
    1.357,  // 3rd gear
    1.074,  // 4th gear
    0.885,  // 5th gear
};
constexpr float PRIMARY_RATIO = 2.733;   // Primary reduction
constexpr float FINAL_RATIO = 45.0 / 15.0; // Final drive (45T/15T)
constexpr float TIRE_CIRC = 2.237;  // meters (100/90-19)

// Speed/RPM → Gear
float speed_mps = speed_kmh / 3.6;
float expected_rpm_per_gear[6];
for (int g = 1; g <= 5; g++) {
    expected_rpm_per_gear[g] = speed_mps / (TIRE_CIRC / (PRIMARY_RATIO * GEAR_RATIOS[g] * FINAL_RATIO)) * 60;
}
int current_gear = find_closest_gear(actual_rpm, expected_rpm_per_gear);
```

---

## Tankinhalt-Messung

OEM-Tankgeber der NX650 (Widerstandsgeber):
- **~10Ω = Voll** (180km Reichweite)
- **~180Ω = Leer** (Reserve)
- **Tankgröße:** 16 Liter (NX650) inkl. 3.5L Reserve
- **ADC-Messung:** Spannungsteiler mit Festwiderstand, ADC-Wert → Widerstand → Füllstand

```cpp
// Tank-Geber Kalibrierung
constexpr float FUEL_EMPTY_OHM = 180.0;  // Ω
constexpr float FUEL_FULL_OHM  = 10.0;   // Ω
constexpr float FUEL_TANK_LITERS = 16.0;  // Liter
constexpr float FUEL_RESERVE_LITERS = 3.5; // Liter (unter ¼ Tank)

float fuel_percent = mapfloat(fuel_ohm, FUEL_EMPTY_OHM, FUEL_FULL_OHM, 0.0, 100.0);
float fuel_liters = fuel_percent * FUEL_TANK_LITERS / 100.0;
```

---

## Hardware-Komponenten

| Komponente | Modell | Preis (€) | Quelle |
|------------|--------|-----------|--------|
| **MCU** | ESP32 DevKit V1 | ~8 | AliExpress |
| **Display** | 3.5" ILI9488 TFT 480×320 SPI | ~12 | AliExpress |
| **Display-Treiber** | TFT_eSPI Library | FOSS | GitHub |
| **Hall-Sensor** | KUS SL07 Universal Speed | ~8 | Amazon/eBay |
| **Neodym-Magnete** | 8× N35 6×3mm | ~3 | Amazon |
| **GPS-Modul** | NEO-M8N (UART) | ~10 | AliExpress |
| **Gehäuse** | 3D-gedruckt PETG+CF | ~15 | Selbst |
| **Kabelbaum** | Hitachi-Stecker+Silikonkabel | ~12 | eBay |
| **Stromversorgung** | 5V 3A Step-Down (LM2596) | ~4 | AliExpress |
| **Total** | | **~72** | |

---

## Software-Architektur

### PlattformIO Projektstruktur

```
custom-tacho/
├── platformio.ini
├── src/
│   ├── main.cpp              # Hauptloop, Mode-Switching, Display-Update
│   ├── tacho_display.h       # TFT-Rendering, Layouts, Farben
│   ├── tacho_display.cpp
│   ├── speed_sensor.h        # Hall-Sensor Interrupt → Speed
│   ├── speed_sensor.cpp
│   ├── rpm_sensor.h           # Pulse Generator → RPM
│   ├── rpm_sensor.cpp
│   ├── gear_detector.h        # Speed/RPM → Gang
│   ├── gear_detector.cpp
│   ├── fuel_gauge.h           # ADC → Tankinhalt
│   ├── fuel_gauge.cpp
│   ├── temp_sensor.h          # NTC → °C Zylinderkopf
│   ├── temp_sensor.cpp
│   ├── gps_handler.h          # NEO-M8N → Position, Odometer
│   ├── gps_handler.cpp
│   ├── trip_meter.h           # Trip A/B, Odometer
│   ├── trip_meter.cpp
│   ├── modes.h                # Ride-Mode-Parameter (aus bestehendem Projekt)
│   ├── cdi_controller.h       # CDI Map Select
│   ├── exhaust_valve.h        # Servo PWM
│   ├── airbox.h               # Airbox Flap
│   ├── sensors.h              # Zentrale Sensor-Verwaltung
│   ├── display.h              # OLED-Display (kleine Info-Anzeige)
│   ├── bluetooth.h            # NimBLE Logging
│   ├── led_indicator.h         # WS2812 Mode-LED + Shift-Light
│   ├── shift_light.h          # RPM-basiertes Shift-Light
│   └── constants.h            # Pins, Kalibrierung, Grenzwerte
├── hardware/
│   ├── WIRING.md              # Pin-Belegung, Schaltpläne
│   ├── HOUSING.md             # 3D-Druck Gehäuse
│   └── CALIBRATION.md         # Abgleich Speed, RPM, Tank
└── RESEARCH.md                # Display-Treiber, Sensor-Recherche
```

### PlattformIO.ini

```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
lib_deps =
    bodmer/TFT_eSPI@^2.5
    paulstoffregen/ESP32TimerInterrupt@^1.5
    h2zero/NimBLE-Arduino@^1.4
    mikalhart/TinyGPSPlus@^1.0
monitor_speed = 115200
build_flags =
    -DUSER_SETUP_LOADED=1
    -DILI9488_DRIVER=1
    -DTFT_WIDTH=480
    -DTFT_HEIGHT=320
    -DTFT_MOSI=23
    -DTFT_SCLK=18
    -DTFT_CS=5
    -DTFT_DC=21
    -DTFT_RST=22
    -DTFT_BL=15
    -DSPI_FREQUENCY=40000000
    -DSPI_READ_FREQUENCY=20000000
```

---

## Display-Modes

| Display-Mode | Trigger | Zeigt | Priorität |
|-------------|---------|-------|-----------|
| **FAHREN** | Standard | RPM, Speed, Gear, Temp, Volt, Mode, Fuel | Normal |
| **PERFORMANCE** | Mode=GELÄNDE/SPORT | RPM-Balken, Speed, Shift-Light, Lap-Timer | Sportlich |
| **DIAGNOSE** | Mode+ & Mode- 5s halten | Sensors, Stator-V, GPS, Uptime | Setup |
| **WARNING** | Auto (Temp>115, V<11.5, Öldruck) | Großes Warncenter, blinkend | Höchste |

---

## Integration mit Ride-Mode-Controller

Der Custom-Tacho **ersetzt** das SSD1306 OLED im bestehenden Ride-Mode-Controller:
- ~~SSD1306 128×64 I²C~~ → **ILI9488 480×320 SPI**
- Selber ESP32, selbe Mode-Logik, erweiterte Display-Ausgabe
- Neuer `tacho_display.h/cpp` kapselt TFT-spezifisches Rendering
- `display.h` (OLED) wird beibehalten als **Fallback/Failsafe-Display**
- Mode-Schaltung, CDI-Steuerung, Valve-Steuerung bleiben identisch

### Neue Module (zusätzlich zu bestehendem Ride-Mode-Controller)

1. **speed_sensor.h/cpp** — Hall-Speed-Interrupt
2. **gear_detector.h/cpp** — Speed/RPM → Gang
3. **fuel_gauge.h/cpp** — Tankgeber ADC → %
4. **gps_handler.h/cpp** — NEO-M8N → Position, Odo
5. **trip_meter.h/cpp** — Trip A/B, Gesamtkm
6. **tacho_display.h/cpp** — TFT-Rendering (ersetzt OLED falls TFT aktiv)
7. **shift_light.h** — WS2812 Ring als Shift-Indikator

---

## Offene Fragen / TODOs

- [ ] TFT-Display Auswahl bestätigen: ILI9488 vs. ILI9341 (2.8") — Preis/Größe-Tradeoff
- [ ] Hall-Sensor-Mounting am Vorderrad: Adapter zeichnen (3D-Druck)
- [ ] GPS-Antenne-Position: Unter Sitzbank? Lenker?
- [ ] Tankgeber-Kalibrierung: Leerlauf-Messung bei vollem/leerem Tank
- [ ] TFT-Beleuchtung: PWM-Dimmerung für Nachtfahrt
- [ ] Wasserfestigkeit: IP67-Gehäuse, Display-Seal
- [ ] Nightmode: Display wechselt zu invertierten Farben bei Dämmerung (LDR oder Zeitgesteuert)
- [ ] Software: TFT_eSPI User_Setup.h für ILI9488 konfigurieren

---

## Referenz

- NX650 Pulse Generator: 220-260 Ohm Pickup Coil, 1 Puls/Revolution (4-Takt = 2 Drehungen pro Puls)
- NX650 Übersetzungen: 1.=2.769, 2.=1.824, 3.=1.357, 4.=1.074, 5.=0.885
- NX650 Primärübersetzung: 2.733 (63/23)
- NX650 Sekundärübersetzung: 45/15 = 3.0 (Standard), 44/16 = 2.75 (Adventure)
- Reifenumfang 100/90-19: ≈ 2.237m (zu kalibrieren gegen GPS)