# 🏍️ African Queen Lite — Projekt-Status & ESP32 Ride-Mode Controller

**Honda NX650 Dominator RFVC** — Zuverlässigkeit + Fahrwerk + Optik + Touring (44PS OEM, KEIN Performance-Tuning)

## Projekt-Status (Chefingenieur Run #6 — 2026-05-28)

|| Metric | Wert |
|--------|------|
| **Budget Hard Cap** | €5.000 |
| **Option A Best-Price** | €2.128 |
| **Option A + Reserve** | €2.628 |
| **Freie Reserve** | €2.372 (47%) |
| **Gewicht Ziel** | 175-180 kg fahrfertig |
| **Gewicht Ist (Option A)** | ~171 kg fahrfertig ✅ |
| **DB Teile (NX650)** | 117+ |
| **Kompatibilität** | 15/15 Hauptteile ✅ |
| **Performance-Teile** | 0 (7 gestrichen) ✅ |

### Budget-Guard Status (Run #6 — 2026-05-28)

|| Phase | Geplant | Budget | Reserve | Status |
|-------|---------|--------|---------|--------|
| 1: Zuverlässigkeit | €393 | €800 | +€407 (51%) | ✅ |
| 2: Fahrwerk | €880 | €1.200 | +€320 (27%) | ✅ |
| 3: Africa Twin Look | €655 | €1.000 | +€345 (35%) | ✅ |
| 4: Touring-Komfort | €187 | €800 | +€613 (77%) | ✅ |
| 5: Reserve | — | €500 | +€500 | 🔵 |

### Styling+Sound Update (Run #6 — 2026-05-28)

- Leo Vince M15051: **FC-Moto auf €289-309 gesenkt** (war €360!)
- Delkevic SS Header: **€165-189** (Delkevic EU Direct)
- Koso RX-22 LED: **€84-94** (Carpimoto.it bester EU-Preis)
- Neuartige UK-Optionen (Black Widow, Fuel Exhaust) = KEIN ABE
- TÜV Phase 3 geschätzt: €90-250
- Bundle-Empfehlung: FC-Moto Sammelbestellung (6 Teile, 1x Versand)
- LED-Umbau: Flasher-Relay MUSS getauscht werden (M8/M10 Thread)

### ⚠️ Kompatibilitäts-Hinweise
1. YSS Z-366 Mono: Bracket muss geschweißt werden (€65 extra)
2. DID 520VX3: 520 pitch ersetzt OEM 525 — Sprockets MUSS 520 sein
3. FH020AA Regler: Adapter-Verkabelung nötig (Connector-Kit €8)
4. Stator-Connector: MUSS gelötet werden (kein Stecker!)
5. JMT YTZ10F: Geringe Batteriebox-Modifikation nötig

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
| **OTA Update** | `ota_update.h` | WiFi-basiertes Firmware-Update (Encoder beim Boot) |

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
│   ├── config_mode.h        # v2.2: Konfigurations-Menü
│   └── ota_update.h          # v2.2: OTA WiFi Firmware Update
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
- **Aktuelle Option-A**: EUR2.128 (28 Teile)