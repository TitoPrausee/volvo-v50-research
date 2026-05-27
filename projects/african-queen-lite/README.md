# 🏍️ African Queen Lite — Build Project

## Vision
**Leichtere, sportlichere Africa Twin auf Honda NX650 Dominator Basis**

- Basis: Honda NX650 Dominator (161kg trocken, 44PS/32kW)
- Inspiration: African Queen (getunte Honda Africa Twin)
- Zielgewicht: ~175-180kg voll ausgerüstet (vs. Africa Twin CRF1000L = 232kg)
- **Leistung: MAX 49 PS** — KEIN Leistungstuning als Ziel! 44PS OEM reichen. Wenn Auspuff+Filter für Sound/Optik zufällig 2-3 PS mehr bringen, ist das Sahnehaube — aber kein Extra-Aufwand für PS
- Charakter: Sportlich + geländetauglich + kurvenfreundlich + tourentauglich
- Optik: Abgerundeter Adventure-Look wie African Queen, aber puristischer

## Team (Cron-Agenten)
Siehe Cron-Jobs: `aql-*` Präfix

## Budget: 5.000€ HARD CAP — So viel erreichen wie möglich, kein Cent verschwenden!

|| Phase | Fokus | Budget | Priorität ||
||-------|-------|--------|----------- ||
|| 1 | Motorlauf & Sicherheit (MUSS) | €500-800 | 🔴 Kritisch | Zuverlässigkeit, KEINE Leistungssteigerung ||
|| 2 | Fahrwerk Sport+Gelände | €800-1.200 | 🔴 Kritisch | Das wichtigste für Kurven+Schotter ||
|| 3 | Africa Twin Look + Sound | €800-1.200 | 🟡 Wichtig | LED, Sitzbank, Heck, Windschild, **Auspuff + Luftfilter** ||
|| 4 | Touring-Komfort | €300-600 | 🟢 Nice-to-have | Heizgriffe, USB, Träger ||
|| 5 | Reserve | €200-500 | 🔵 Puffer | Unvorhergesehenes ||
|| **Total** | | **€5.000 MAX** | ||

**Prinzip**: Jeder Euro muss Leistung bringen. Lieber weniger Teile von guter Qualität als mehr Teile von schlechter.

## Gewichtsbilanz
|| Position | OEM (kg) | Nach Bau (kg) | Δ ||
||----------|----------|---------------|---||
|| Basis NX650 | 161 | 161 | 0 ||
|| Batterie LiFePO4 | -3.2 | -1.2 | -2.0 ||
|| Auspuff Collector-Box | +8 | +5 (SS) | -3.0 ||
|| LED Scheinwerfer | -2.5 | -1.5 | -1.0 ||
|| LED Blinker+Rücklicht | -1.0 | -0.3 | -0.7 ||
|| Gabel+Emulatoren | +0.5 | +0.5 | 0 ||
|| YSS Federbein | +5.5 | +4.2 | -1.3 ||
|| Heckträger Alu | 0 | +1.5 | +1.5 ||
|| **Ziel gesamt** | **~175** | | ||

## Projektstruktur

```
african-queen-lite/
├── README.md              ← This file
├── TEAM_REQUESTS.md       ← Team communication hub
├── WEIGHT_BALANCE.md      ← Weight tracking
├── dashboard/             ← ESP32 Ride-Mode Controller (PlatformIO)
│   ├── platformio.ini     ← Board config, libraries
│   ├── src/
│   │   ├── main.cpp       ← Main program, mode switching, display loop
│   │   ├── modes.h        ← 6 ride modes with parameter sets
│   │   ├── cdi_controller.h   ← Ignition timing control (Map A/B select)
│   │   ├── exhaust_valve.h    ← Servo PWM for exhaust valve
│   │   ├── airbox.h           ← Servo PWM for airbox resonance flap
│   │   ├── sensors.h          ← RPM, temp, voltage, oil pressure sensing
│   │   ├── display.h          ← SSD1306 OLED 128x64 rendering
│   │   ├── bluetooth.h        ← NimBLE service for smartphone logging
│   │   └── led_indicator.h    ← WS2812 RGB LED mode indicator
│   ├── hardware/
│   │   └── WIRING.md       ← Pin mappings, circuits, enclosure notes
│   └── RESEARCH.md          ← Research findings (MCU, servo, CDI, StVZO)
└── tracker/                ← Build tracker web app (Python/Flask)
    ├── app.py              ← Dashboard server (port 5050)
    └── requirements.txt
```

## Ride-Mode Controller — 6 Modi

| Mode | Zündung | Valve | Airbox | LED | Charakter |
|------|---------|-------|--------|-----|-----------|
| STRASSE | 0° | 50% | 50% | 🟢 Grün | Ausgewogen, moderater Sound |
| STADT | -2° | 20% | 30% | 🔵 Blau | Leise, spritsparend |
| GELÄNDE | +2° | 100% | 100% | 🔴 Rot | Aggressiv, volle Leistung |
| SPORT | +3° | 100% | 100% | 🟠 Orange | Scharf, sportlich |
| COMFORT | -1° | 40% | 40% | 🟣 Lila | Sanft, cruisen |
| SOUND | +1° | 100% | 80% | 🔵 Türkis | Best Sound, nicht max Leistung |

## Hardware

- **MCU:** ESP32 DevKit (WiFi + BLE, 34 GPIO, 240MHz dual-core)
- **Display:** SSD1306 1.3" OLED (128×64, I²C) — sonnenlichtlesbar
- **LED:** WS2812 RGB (1 LED, Modus-Farbe)
- **Servos:** MG996R (Prototyp) → später Pololu 37D Gearmotor + AS5600
- **CDI:** Ignitech DC-CDI-P2 (Map A/B via GPIO)
- **Switches:** 2× Cyclops Adventure Switch (Mode+/Mode-), IP68
- **Gehäuse:** 3D-gedruckt PETG, IP67 mit Dichtung, Lenker-Halterung

## DB
Alle Daten in: `research/vehicle_database.db`
- Variant ID: 5 (NX650 Dominator RFVC)
- Build Guide: "African Queen Lite"