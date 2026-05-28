# 🏍️ African Queen Lite — Projekt-Status & ESP32 Ride-Mode Controller

**Honda NX650 Dominator RFVC** — Zuverlässigkeit + Fahrwerk + Optik + Touring (44PS OEM, KEIN Performance-Tuning)

## Projekt-Status (Chefingenieur Run #7 — 2026-05-28)

| Metric | Wert |
|--------|------|
| **Budget Hard Cap** | €5.000 |
| **Option A Best-Price** | €2.128 |
| **Option A + Reserve** | €2.628 |
| **Freie Reserve** | €2.372 (47%) |
| **Gewicht Ziel** | 175-180 kg fahrfertig |
| **Gewicht Ist (Option A)** | ~171 kg fahrfertig ✅ |
| **DB Teile (NX650)** | 199 |
| **DB Total** | 668 Teile, 415 Quellen |
| **Kompatibilität** | 15/15 Hauptteile ✅ |
| **Performance-Teile** | 0 (15 gestrichen) ✅ |
| **NX650 Known Issues** | 65 (5 critical, 7 high) |

### Budget-Guard Status (Run #7 — 2026-05-28)

| Phase | Geplant | Budget | Reserve | Status |
|-------|---------|--------|---------|--------|
| 1: Zuverlässigkeit | €393 | €800 | +€407 (51%) | ✅ |
| 2: Fahrwerk | €880 | €1.200 | +€320 (27%) | ✅ |
| 3: Africa Twin Look | €655 | €1.000 | +€345 (35%) | ✅ |
| 4: Touring-Komfort | €187 | €800 | +€613 (77%) | ✅ |
| 5: Reserve | — | €500 | +€500 | 🔵 |

### 🆕 Run #7 Neue Erkenntnisse

#### 1. Neue NX650 Teile in DB (seit Run #6)
| ID | Teil | Preis | Gewicht | Kategorie | Relevanz |
|----|------|-------|---------|-----------|----------|
| 723 | Mosko Moto R80 Luggage System | €340 avg | 3.500g | exterior | ⚠️ Über Budget für Phase 4 |
| 722 | Koso RX-22N 7" LED (DOT/ECE) | €109 avg | 800g | exterior | ✅ Alternative zu RX-22 |
| 721 | Stator 3-Pin Weatherpack Upgrade | €9 avg | 20g | electrical | ✅ Besser als OEM-Stecker |
| 720 | Viton Fuel Hose Kit 3mm | €7 avg | 50g | fuel_system | ✅ Phase 1 Ethanol-Schutz |
| 719 | Pilot Jet #40 (Upgrade #38) | €5 avg | 5g | fuel_system | 🟡 Optional, kein Power-Tuning |
| 705 | Exhaust Gasket Muffler Joint | €5 avg | ?g | exhaust | ✅ Phase 3 Zubehör |
| 704 | Exhaust Gasket Header-Cylinder | €6 avg | ?g | exhaust | ✅ Phase 3 Zubehör |
| 702 | Deutsch DT Connector Kit | €22 avg | 120g | electrical | ✅ Alternative zu Weatherpack |
| 639 | Cylinder Head (cracked replacement) | €350 avg | 8.000g | engine | ❌ Notfall-Ersatz |

#### 2. Stator-Connector Upgrade: Weatherpack vs Deutsch DT
- **Weatherpack 3-Pin (ID 721):** €9 avg, 20g — wasserdicht, einfach
- **Deutsch DT Kit (ID 702):** €22 avg, 120g — IP67, Goldkontakte, professioneller
- **Empfehlung:** **Weatherpack** für Budget-Build (€9 vs €22), **Deutsch DT** für maximale Zuverlässigkeit
- Beide sind VAST besser als geschmolzener OEM-Stecker!

#### 3. Koso RX-22N vs RX-22: Neue Option
- **Koso RX-22** (Original): €108 avg, 1.000g, H4 LED + DRL Ring
- **Koso RX-22N** (Neu, ID 722): €109 avg, 800g, DOT/ECE approved
- **Unterschied:** RX-22N hat **200g weniger** und **DOT/ECE Zulassung** → besser für TÜV!
- **Preis:** Praktisch identisch (~€1 Unterschied)
- **Empfehlung:** RX-22N bevorzugen für TÜV-Eintragung

#### 4. Pilot Jet #40 — KEIN Performance-Tuning
- Pilot Jet #40 (statt #38 OEM) ist eine常见的 Vergaser-Abstimmung mit SS Header + Filter
- **Kategorie: Wartung/Tuning**, KEIN Leistungszuwachs — entspricht OEM-Abstimmung mit freierem Auspuff
- Preis: €5 → negligible, Teil der Phase 1 Vergaser-Wartung

#### 5. Mosko Moto R80 vs Budget Panniers
- **Mosko Moto R80:** €340, 3.500g — Premium-System
- **Budget Soft Pannier Set** (Phase 4): €40, ~1.200g
- **Empfehlung:** Budget Panniers für dieses Projekt. Mosko R80 = +€300 und +2.300g → überschreitet Phase 4 Budget massiv
- **Notiz:** Mosko R80 als OPTIONALE Upgrade-Möglichkeit für später dokumentiert

### ⚠️ Kompatibilitäts-Hinweise (aktualisiert Run #7)
1. YSS Z-366 Mono: Bracket muss geschweißt werden (€65 extra)
2. DID 520VX3: 520 pitch ersetzt OEM 525 — Sprockets MUSS 520 sein
3. FH020AA Regler: Adapter-Verkabelung nötig (Connector-Kit €8)
4. Stator-Connector: MUSS gelötet werden (kein Stecker!) oder Weatherpack/Deutsch DT Upgrade
5. JMT YTZ10F: Geringe Batteriebox-Modifikation nötig
6. **Koso RX-22N:** DOT/ECE Version des RX-22 — bevorzugen für TÜV
7. **Exhaust Gaskets:** Dichtungen für Header+Muffler Joint sind Pflicht bei SS Header Umbau (€11 total)

### Budget-Guard Status (Run #6 — Referenz)

| Phase | Geplant | Budget | Reserve | Status |
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
│   └── ota_update.h         # v2.2: OTA WiFi Firmware Update
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
- **Aktuelle Option-A**: EUR2.128 (28+ Teile)