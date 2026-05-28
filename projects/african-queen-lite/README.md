# 🏍️ African Queen Lite — Build Project

## Vision
**Leichtere, sportlichere Africa Twin auf Honda NX650 Dominator Basis**

- Basis: Honda NX650 Dominator (161kg trocken, 44PS/32kW)
- Inspiration: African Queen (getunte Honda Africa Twin)
- Zielgewicht: ~170-175kg fahrfertig (vs. Africa Twin CRF1000L = 232kg)
- **Leistung: MAX 49PS** — KEIN Leistungstuning als Ziel! 44PS OEM reichen. Auspuff+Filter nur für Sound/Optik, PS=Bonus
- Charakter: Sportlich + geländetauglich + kurvenfreundlich + tourentauglich
- Optik: Abgerundeter Adventure-Look wie African Queen, aber puristischer

## Team (Cron-Agenten)
Siehe Cron-Jobs: `aql-*` Präfix

## Budget: 5.000€ HARD CAP — So viel erreichen wie möglich, kein Cent verschwenden!

| Phase | Fokus | Budget | Priorität |
|-------|-------|--------|----------|
| 1 | Motorlauf & Sicherheit (MUSS) | €470-800 | 🔴 Kritisch |
| 2 | Fahrwerk Sport+Gelände | €800-1.200 | 🔴 Kritisch |
| 3 | Africa Twin Look + Sound | €800-1.000 | 🟡 Wichtig |
| 4 | Touring-Komfort | €300-600 | 🟢 Nice-to-have |
| 5 | Reserve | €200-500 | 🔵 Puffer |
| **Total** | | **€5.000 MAX** | |

## Budget-Stand (Preis-Jäger Run #3 — 2026-05-28)

|| Phase | Geplant (€) | Budget (€) | Reserve (€) | Status |
|-------|------------|-----------|------------|--------|
| 1: Zuverlässigkeit | 429 | 800 | +371 (46%) | ✅ Stark |
| 2: Fahrwerk | 892 | 1.200 | +308 (26%) | ✅ Gut |
| 3: Africa Twin Look | 688 | 1.000 | +312 (31%) | ✅ Gut |
| 4: Touring-Komfort | 187 | 800 | +613 (77%) | ✅ Sehr gut |
| 5: Reserve | — | 500 | +500 | 🔵 Puffer |
| **Total** | **2.196** | **4.300** | **+2.104** | ✅ |

> **Ergebnis:** Option A (Optimal) kostet €2.196 + €500 Reserve = €2.696. Unter dem €5.000 Hard Cap mit **€2.304 Reserve** (46%).
> 
> 🆕 **Run #3 Verbesserung:** €68 günstiger als Run #2! (€2.264 → €2.196)
> - Venhill SS Bremsleitung statt HEL: **-€15** (gleiche Qualität!)
> - YSS Z-366 Mono Shock WRS Italy: **-€52.50** (gleiche YSS Qualität!)
> - Diverse Preis-Korrekturen: **-€0.50**

### Budget-Guard: KEINE Phase überschritten ✅
- Phase 1: €429 / €800 → **€371 Reserve** (46%) — 🆕 Venhill statt HEL spart €15!
- Phase 2: €892 / €1.200 → **€308 Reserve** (26%) — 🆕 YSS Z-366 WRS Italy spart €52!
- Phase 3: €688 / €1.000 → **€312 Reserve** (31%) — unverändert
- Phase 4: €187 / €800 → **€613 Reserve** (77%) — unverändert

### DB-Verifizierung (2026-05-28 — Preis-Jäger Run #3)
- **187 NX650-fitment Teile** in DB (inkl. alle Alternativen + Bundle/Kits)
- **DB SUM(price_avg) alle NX650:** ~€13.200 (nicht AQL-Budget — enthält Alternativen!)
- **34 Teile in Option A Build-Plan:** €2.196
- **54 NX650 Known Issues:** 5 critical (Stator, Regler, +Verbinder), 4 high (Verkabelung, CDI)
- **4 DB-Preise aktualisiert (Run #3):** YSS Z-366 min/max/avg, Venhill SS Line, EBC FA185HH, All Balls Carb Kit
- **1 neues Teil (Run #3):** Venhill SS Brake Line Front NX650 (ID 450)
- **🆕 Run #3 Key Finds:** Venhill statt HEL = €15 sparen, YSS WRS Italy = €52 sparen

### Neue NX650-Ersatzteile in DB (nicht im Build-Budget)
Folgenden Teile wurden von Research-Agenten hinzugefügt — wichtig als Referenz für Wartung, aber **NICHT** im AQL-Build-Budget enthalten:

| ID | Teil | € (avg) | Typ | Relevanz |
|----|------|---------|-----|----------|
| 313 | Zylinderkopfdichtung | 38 | Engine | Wartungs-Ersatz |
| 314 | Steuerkette OEM | 65 | Engine | Falls APE MCCT nicht reicht |
| 318 | APE MCCT | 79 | Engine | Empfohlen bei Kettengeräuschen |
| 319 | Komplette Dichtungs-Set Athena | 89 | Engine | Komplett-Überholung |
| 322 | Neutral-Schalter | 14 | Elektrik | Bekanntes Problem |
| 323 | Regler-Verbinder-Kit | 8 | Elektrik | Verbrennt oft! |
| 329 | Kraftstoffhahn | 55 | Fuel | Leckt häufig |

## Gewichtsbilanz

| Position | OEM (kg) | Nach Bau (kg) | Δ |
|----------|----------|---------------|---|
| Basis NX650 | 161 | 161 | 0 |
| Batterie LiFePO4 | 3.2 | 1.2 | -2.0 |
| Auspuff SS+Leo Vince | 8.0 | 5.0 | -3.0 |
| LED Scheinwerfer | 2.5 | 1.5 | -1.0 |
| LED Blinker+Rücklicht | 1.0 | 0.3 | -0.7 |
| Gabel+Emulatoren | — | +0.5 | +0.5 |
| YSS Mono Shock | 5.5 | 4.2 | -1.3 |
| Kette 520 VX3 | 1.8 | 1.5 | -0.3 |
| Heckträger Alu | 0 | +1.5 | +1.5 |
| Windschild | 0 | +0.4 | +0.4 |
| Handguards | 0 | +0.3 | +0.3 |
| **Total** | **~183** | **~175.4** | **-5.6** |

> **Fahrfertig:** ~170-171kg (mit Benzin, Öl, Kühlflüssigkeit)
> **Ziel 175-180kg:** ✅ ERREICHT — sogar ~5kg darunter!

## Kompatibilitäts-Checks ✅

| Teil | Kompatibel mit NX650? | Quelle |
|------|---------------------|--------|
| RM Stator 200W + FH020AA | ✅ Bekanntes NX650-Upgrade | RM Stator, Forum |
| YSS Z-366-330TRL-06 | ✅ NX650 Mono-Shock (Bracket nötig) | YSS-Katalog |
| Race Tech FEGV S4101 | ✅ 41mm konventionelle Gabel | Race Tech |
| Leo Vince SBK Slip-on | ✅ ECE R92, NX650 fitment | Leo Vince |
| Delkevic SS Header | ✅ Direkt-Bolt-on NX650 | Delkevic |
| DID 520VX3 + JT 15/44 | ✅ NX650 Kette+Ritzel | DID/Motea |
| UNI NU-4050 | ✅ NX650 Luftfilter | UNI |
| All Balls 22-1022 | ✅ VE82M Vergaser-Rebuild-Kit | All Balls |
| EBC FA185HH | ✅ NX650 Bremsbeläge vorne+hinten | EBC |
| HEL Performance SS Line | ✅ NX650 Front Bremsschlauch | HEL |
| Koso RX-22 7" LED | ✅ 7" H4, passt NX650 Bucket | Koso |
| LiFePO4 YTZ10F | ✅ NX650 Batterie-Größe | JMT |

## Performance-Teile: KEINE ✅

Folgende Teile wurden NICHT in den Build-Plan aufgenommen:
- ❌ Big Bore Kit (680/710cc) — KEINE Leistungssteigerung
- ❌ Aftermarket CDI — OEM reicht, 44PS sind genug *(Ignitech DC-CDI-P2 = OE-Ersatz mit 3 Maps, kein Leistungstuning)*
- ❌ FMF PowerCore 4 — Offroad-only, illegal auf Straße
- ❌ K&N Filter Charger Kit — UNI NU-4050 reicht für Adventure
- ❌ Leistungs-Auspuff — Leo Vince = Sound+Optik, KEin PS-Tuning

## Projektstruktur

```
african-queen-lite/
├── README.md              ← This file
├── TEAM_REQUESTS.md       ← Team communication hub
├── WEIGHT_BALANCE.md      ← Weight tracking
├── BUDGET_OPTIMIZATION.md ← Budget details & 3 build options
├── MOTOR_RELIABILITY_DRIVE.md ← Engine reliability research
├── STYLING_SOUND.md       ← Styling & sound specialization
├── dashboard/             ← ESP32 Ride-Mode Controller (PlatformIO)
│   ├── platformio.ini     ← Board config, libraries
│   ├── src/
│   │   ├── main.cpp       ← Main program, mode switching, display loop
│   │   ├── modes.h        ← 6 ride modes with parameter sets
│   │   ├── cdi_controller.h   ← Ignition timing control (3-map: A/B/C via GPIO27+GPIO33)
│   │   ├── exhaust_valve.h    ← Servo PWM for exhaust valve
│   │   ├── airbox.h           ← Servo PWM for airbox resonance flap
│   │   ├── sensors.h          ← RPM, temp, voltage, oil pressure sensing
│   │   ├── display.h          ← SSD1306 OLED 128x64 rendering (sunlight-optimized v2.1)
│   │   ├── bluetooth.h        ← NimBLE service for smartphone logging
│   │   └── led_indicator.h    ← WS2812 RGB LED mode indicator
│   ├── hardware/
│   │   ├── WIRING.md       ← Pin mappings, circuits, enclosure notes
│   │   ├── wiring_diagram.py ← SVG+ASCII wiring diagram generator (v2.1)
│   │   └── parts_checker.py ← Parts compatibility checker against DB (v2.1)
│   └── RESEARCH.md          ← Research findings (MCU, servo, CDI, StVZO)
└── tracker/                ← Build tracker web app (Python/Flask)
    ├── app.py              ← Dashboard server (port 5050)
    └── requirements.txt
```

## Ride-Mode Controller v2.1 — 6 Modi

| Mode | Zündung | Valve | Airbox | CDI Map | LED | Charakter |
|------|---------|-------|--------|---------|-----|-----------|
| STRASSE | 0° | 50% | 50% | A | 🟢 Grün | Ausgewogen, moderater Sound |
| STADT | -2° | 20% | 30% | A | 🔵 Blau | Leise, spritsparend |
| GELÄNDE | +2° | 100% | 100% | B | 🔴 Rot | Aggressiv, volle Leistung |
| SPORT | +3° | 100% | 100% | B | 🟠 Orange | Scharf, sportlich |
| COMFORT | -1° | 40% | 40% | A | 🟣 Lila | Sanft, cruisen |
| SOUND | +1° | 100% | 80% | C | 🔵 Türkis | Best Sound, nicht max Leistung |

## Hardware

- **MCU:** ESP32 DevKit (WiFi + BLE, 34 GPIO, 240MHz dual-core)
- **Display:** SSD1306 1.3" OLED (128×64, I²C) — sunlight-optimized firmware v2.1
- **LED:** WS2812 RGB (1 LED, Modus-Farbe)
- **Servos:** MG996R (Prototyp) → **DRV8833+AS5600** motor driver (v2.1, compile-time selectable)
- **CDI:** Ignitech DC-CDI-P2 (3-Map: A/B/C via GPIO27+GPIO33, EC-type approved)
- **Switches:** 2× Cyclops Adventure Switch (Mode+/Mode-), IP68
- **Gehäuse:** 3D-gedruckt PETG, IP67 mit Dichtung, Lenker-Halterung

### v2.1 Key Changes
- **3-Map CDI:** GPIO27 (Map A/B) + GPIO33 (Map B/C) → 3 ignition curves via Ignitech DC-CDI-P2
- **DRV8833+AS5600:** Closed-loop motor driver for exhaust/airbox valves (replaces unreliable RC servos)
- **Sunlight display:** 2x font for temp/voltage, inverted display mode, high-contrast layout
- **Engine runtime fix:** `update_runtime()` with millis()-based minute tracking
- **Wiring diagram generator:** Python SVG+ASCII generator in `hardware/wiring_diagram.py`
- **Parts compatibility checker:** Validates components against `vehicle_database.db`

## DB
Alle Daten in: `research/vehicle_database.db`
- Variant ID: 5 (NX650 Dominator RFVC)
- 143 NX650-fitment Teile in DB
- 54 NX650 Known Issues (5 critical)
- Build Guide #8: African Queen Lite Styling (active)