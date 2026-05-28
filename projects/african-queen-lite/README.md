# 🏍️ African Queen Lite — ESP32 Ride-Mode Controller

**Honda NX650 Dominator RFVC** — LangLeben durch Software

## Version: v2.2

### Was ist das?
Ein ESP32-basierter Ride-Mode Controller der WÄHREND DER FAHRT zwischen 6 Modi wechselt:
1. **STRASSE** — Ausgewogen, moderater Sound
2. **STADT** — Leise, spritsparend, sanfte Gasannahme
3. **GELÄNDE** — Aggressiv, volle Leistung, Drehzahl-hoch-halten
4. **SPORT** — Scharfer Zündzeitpunkt, offener Auspuff
5. **COMFORT** — Weich, leise, cruisen
6. **SOUND** — Optimiert für besten Sound (nicht Leistung!)

### Was steuert der Controller?
- **Zündzeitpunkt**: 3-Map CDI (Ignitech DC-CDI-P2) über GPIO27+GPIO33
- **Exhaust Valve**: DRV8833+AS5600 oder RC Servo — position folgt RPM-Kurve
- **Airbox-Klappe**: gleiche Aktorik wie Exhaust
- **LED-Anzeige**: WS2812 RGB (farblich pro Mode)
- **Display**: SSD1306 OLED 128x64 (4 Seiten auto-cycling)
- **Bluetooth**: NimBLE für Smartphone-Logging

### v2.2 Neue Features
| Feature | Datei | Beschreibung |
|---------|-------|-------------|
| **Auto-RPM Valve** | `auto_rpm_valve.h` | Auspuffklappe folgt RPM-Kurve pro Mode |
| **Fuel Estimator** | `fuel_estimator.h` | mL/100km pro Mode, Reichweite, Reserve-Warnung |
| **Gear Estimator** | `gear_estimator.h` | Gang-Erkennung aus RPM/Speed |
| **Deep Sleep** | `sleep_manager.h` | 5 Min Motor aus → 10µA (Wake an Taste/Zündung) |
| **Config Mode** | `config_mode.h` | Long-Press Encoder → Einstellungen |

### Verzeichnisstruktur
```
dashboard/
├── platformio.ini           # PlatformIO Build-Konfiguration
├── RESEARCH.md              # Hardware-Research (ESP32, CDI, Servos, ...)
├── src/
│   ├── main.cpp             # Hauprogramm v2.2
│   ├── modes.h              # Mode-Definitionen + Parameter
│   ├── cdi_controller.h     # 3-Map CDI-Steuerung
│   ├── exhaust_valve.h      # Auspuff-Klappen-Servo
│   ├── airbox.h             # Airbox-Klappen-Servo
│   ├── sensors.h            # RPM, Temperatur, Spannung, Öl
│   ├── display.h            # SSD1306 OLED (4 Seiten)
│   ├── longevity.h          # Stator, Batterie, Wartung
│   ├── bluetooth.h          # NimBLE GATT Service
│   ├── led_indicator.h      # WS2812 RGB LED
│   ├── encoder.h            # KY-040 Rotary Encoder
│   ├── auto_rpm_valve.h     # v2.2: RPM-basierte Ventil-Steuerung
│   ├── fuel_estimator.h     # v2.2: Verbrauchsschätzung
│   ├── gear_estimator.h     # v2.2: Gang-Erkennung
│   ├── sleep_manager.h      # v2.2: Deep Sleep
│   └── config_mode.h        # v2.2: Konfigurations-Menü
└── hardware/
    ├── WIRING.md             # Schaltplan & Pin-Belegung
    ├── wiring_diagram.py     # SVG/ASCII Generator
    ├── wiring_diagram.svg    # Dunkles SVG Schaltplan
    └── wiring_diagram.txt    # ASCII Schaltplan

tracker/
├── app.py                    # Flask Web-Dashboard v2.2
├── requirements.txt          # flask>=3.0
└── parts_checker.py          # Teile-Kompatibilitäts-Checker
```

### Bauen und Hochladen
```bash
cd dashboard
pio run -t upload          # Build und Flash an ESP32
pio device monitor         # Serial Monitor (115200 baud)
```

### Dashboard starten
```bash
cd tracker
pip install flask
python3 app.py
# → http://localhost:5050
```

### Budget
- **Motorrad-Build**: EUR5.000 Hart-Cap
- **ESP32 Controller**: ~EUR205 (separat)
- **Aktuelle Option-A**: EUR2.264 (28 Teile)