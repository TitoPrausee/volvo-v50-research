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
| 1 | Motorlauf & Sicherheit (MUSS) | €500-800 | 🔴 Kritisch |
| 2 | Fahrwerk Sport+Gelände | €800-1.200 | 🔴 Kritisch |
| 3 | Africa Twin Look + Sound | €800-1.000 | 🟡 Wichtig |
| 4 | Touring-Komfort | €300-600 | 🟢 Nice-to-have |
| 5 | Reserve | €200-500 | 🔵 Puffer |
| **Total** | | **€5.000 MAX** | |

## Budget-Stand (Chefingenieur 2026-05-28 — DB-Verifizierung + Preis-Jäger Run #2)

| Phase | Geplant (€) | Budget (€) | Reserve (€) | Status |
|-------|------------|-----------|------------|--------|
| 1: Zuverlässigkeit | 445 | 800 | +355 (44%) | ✅ Stark |
| 2: Fahrwerk | 944 | 1.200 | +256 (21%) | ✅ OK |
| 3: Africa Twin Look | 688 | 1.000 | +312 (31%) | ✅ Gut |
| 4: Touring-Komfort | 187 | 800 | +613 (77%) | ✅ Sehr gut |
| 5: Reserve | — | 500 | +500 | 🔵 Puffer |
| **Total** | **2.264** | **4.300** | **+2.036** | ✅ |

> **Ergebnis:** Option A (Optimal) kostet €2.264 + €500 Reserve = €2.764. Unter dem €5.000 Hard Cap mit **€2.236 Reserve** (45%).
> 
> ⚠️ Phase 1 um €19 gestiegen: Regler-Verbinder-Kit + Stator-Connector (€17) hinzugefügt — BEKANNTES NX650-Sicherheitsproblem!

### Budget-Guard: KEINE Phase überschritten ✅
- Phase 1: €445 / €800 → **€355 Reserve** (44%) — +€17 Regler-Verbinder+Stator-Connector
- Phase 2: €944 / €1.200 → **€256 Reserve** (21%) — Mitas E-07+ Dakar teurer
- Phase 3: €688 / €1.000 → **€312 Reserve** (31%)
- Phase 4: €187 / €800 → **€613 Reserve** (77%)

### DB-Verifizierung (2026-05-28 — Preis-Jäger Run #2)
- **143 NX650-fitment Teile** in DB (inkl. alle Alternativen + neue Bundle/Kits)
- **DB SUM(price_avg) alle NX650:** €12.657 (nicht AQL-Budget — enthält Alternativen!)
- **28 Teile in Option A Build-Plan:** €2.264
- **54 NX650 Known Issues:** 5 critical (Stator, Regler, +Verbinder), 4 high (Verkabelung, CDI)
- **Neu hinzugefügte NX650-Teile (IDs 303-346):** 44 Teile — Dichtungen, OEM-Ersatzteile, Motorinternas, Bundle-Deals, Connector-Kits
- **7 Preise aktualisiert:** Stator €95, Regler €55, EBC FA185HH €20, Koso RX-22 €99.90, Mitas E-07+ Dakar €89.90/€109
- **6 neue Teile (Run #2):** Bundle-Deals (Ketten-Set, Mitas Set, RT Fork Kit), Schweißarbeiten, Regler-Verbinder-Kit, Stator-Connector

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
- ❌ Aftermarket CDI — OEM reicht, 44PS sind genug
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
- 137 NX650-fitment Teile in DB
- 54 NX650 Known Issues (4 critical)
- Build Guide #8: African Queen Lite Styling (active)