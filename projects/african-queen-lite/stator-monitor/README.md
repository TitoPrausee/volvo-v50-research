# 🔋 Stator-Monitor & Öldruck-Warnsystem — African Queen Lite

## Warum?
Die NX650 Dominator hat **zwei bekannte Schwachstellen** die zu Motorschäden führen:
1. **Stator (Lichtmaschine)**: Bekannt dafür durchzubrennen → Batterie entlädt → Zündung fällt aus → Motor stirbt
2. **Öldruck**: Kein Öldruck = Motorschaden innerhalb von Sekunden. OEM hat nur eine Warnleuchte (die man nicht sieht bei Sonne)

Beides **lebensrettende** Systeme für eine Adventure-Maschine die in der Pampa stehen kann.

---

## Stator-Monitoring

### Das Problem
- NX650 hat einen **6V/180W Einphasen-Stator** (bei einigen Modellen) oder 12V/200W mit aftermarket RM Stator
- Der Regler/Gleichrichter ist oft schwach → Überspannung zerstört Batterie und Elektronik
- Wenn der Stator stirbt → Batterie wird nicht geladen → Motor stirbt nach 30-60 Min
- **Symptomloser Tod** — man merkt es erst wenn die Zündung ausfällt

### Messung

| Parameter | Methode | GPIO | Formel |
|-----------|---------|------|--------|
| **Ladespannung** | Spannungsteiler an Batterie | GPIO35 | `V_batt = ADC × 16.0 × 3.3 / 4095` |
| **Stator-AC** | Dioden-Gleichrichter + Teiler | GPIO4 (ADC1) | AC-Spitze messen |
| **Ladestrom** | Shunt-Widerstand (0.01Ω) | GPIO36 | `(V_shunt / 0.01) × Verstärkung` |

### Spannungsgrenzen

```cpp
// Stator/ Charging Monitor Schwellwerte
constexpr float V_CHARGING_OK      = 13.8f;  // V — Stator lädt bei >2000rpm
constexpr float V_CHARGING_LOW     = 12.8f;  // V — Motor läuft, keine Ladung!
constexpr float V_BATTERY_FULL     = 14.4f;  // V — Regler begrenzt hier
constexpr float V_REGULATOR_FAIL   = 15.5f;  // V — ÜBERGESPANNUNG! Regler kaputt!
constexpr float V_BATTERY_LOW      = 12.0f;  // V — Batterie fast leer
constexpr float V_BATTERY_CRIT     = 11.5f;  // V — Zündungsprobleme drohen

// RPM-abhängige Ladung
constexpr uint16_t RPM_CHARGE_START = 1500;  // Ab ~1500rpm lädt der Stator
constexpr uint16_t RPM_CHARGE_FULL   = 3000;  // Volle Ladung ab ~3000rpm
```

### Stator-Status-Logik

```cpp
enum StatorStatus {
    STATOR_UNKNOWN,       // Nicht genug Daten
    STATOR_OK,            // Ladespannung normal (13.8-14.4V @ RPM>2000)
    STATOR_LOW_CHARGE,    // Spannung zu niedrig bei hohen RPM
    STATOR_OVERVOLTAGE,   // Spannung >15.5V — Regler verdächtig!
    STATOR_NOT_CHARGING,  // Motor läuft, RPM>1500, aber <13V
    STATOR_BATTERY_LOW    // Batterie <12V, Stator vielleicht OK aber Batterie schwach
};

StatorStatus checkStator(float v_batt, uint16_t rpm) {
    if (rpm < RPM_CHARGE_START) return STATOR_UNKNOWN; // kein Laden im Leerlauf normal
    if (v_batt > V_REGULATOR_FAIL) return STATOR_OVERVOLTAGE; // SOFORT WARNEN!
    if (rpm > RPM_CHARGE_FULL && v_batt < V_CHARGING_LOW) return STATOR_NOT_CHARGING;
    if (rpm > RPM_CHARGE_START && v_batt < V_CHARGING_LOW) return STATOR_LOW_CHARGE;
    if (v_batt > V_CHARGING_OK && v_batt < V_BATTERY_FULL) return STATOR_OK;
    if (v_batt < V_BATTERY_LOW) return STATOR_BATTERY_LOW;
    return STATOR_UNKNOWN;
}
```

---

## Öldruck-Warnsystem

### Das Problem
- NX650 hat nur eine **Öldruck-Warnleuchte** (1×12V Birnchen im Tacho)
- Bei Sonneneinstrahlung **unsichtbar**
- Wenn der Öldruck fällt (Ölpumpe kaputt, Ölleck) → Kolbenfresser in <30 Sekunden
- Bei Adventure-Fahrten: vibration, Hitze, Schräglage → Öldruck kann momentan fallen

### OEM-Sensor: Einfacher Druckschalter

- **0-0.5 bar:** Schalter OFF (Öldruck-Warnleuchte AN)
- **>0.5 bar:** Schalter ON (Öldruck OK)
- **Problem:** Nur AN/AUS, keine Analogmessung, Schwellwert nicht einstellbar

### Upgrade: Analoger Öldrucksensor

| Option | Sensor | Preis | Bereich | Ausgang |
|--------|--------|-------|---------|---------|
| **A (Empfohlen)** | VDO 360-081 (M10×1.0) | ~€25 | 0-5 bar | 10-180Ω |
| B | KUS 1/8"-27 NPT | ~€20 | 0-80 psi | 0-5V |
| C | OEM-Schalter beibehalten | €0 | 0.5 bar Schalter | Digital |

**VDO 360-081 Vorteile:**
- M10×1.0 passt direkt an NX650 Öldruck-Bohrung (M10×1.0 Gewinde)
- 10-180Ω Widerstandsgeber → einfache ADC-Messung
- 0-5 bar Bereich → ideal für Motorrad (normal ~2-3 bar bei Betriebstemp)
- Kompakt, zuverlässig, VDO-Qualität

### Öltemperatur-Schwellwerte (NX650 RFVC)

```cpp
constexpr float OIL_PRESSURE_LOW      = 0.8f;   // bar — WARNUNG bei warmem Motor
constexpr float OIL_PRESSURE_NORMAL   = 2.0f;   // bar — normaler Öldruck @3000rpm, 80°C
constexpr float OIL_PRESSURE_HIGH     = 4.5f;   // bar — möglich bei Kaltstart
constexpr float OIL_PRESSURE_CRIT     = 0.5f;   // bar — MOTOR SOFORT ABSTELLEN!

constexpr float OIL_TEMP_WARM         = 85.0f;  // °C — normal
constexpr float OIL_TEMP_HOT          = 110.0f; // °C — Achtung
constexpr float OIL_TEMP_CRIT         = 125.0f; // °C — MOTOR ABSTELLEN!
```

### Öldruck-Messung (ADC)

```cpp
// VDO 360-081: 0 bar = 10Ω, 5 bar = 180Ω
// Spannungsteiler: VDO-Geber → Festwiderstand 100Ω → Masse
// ADC-Messung am Knotenpunkt
// V_adc = 3.3V × R_fixed / (R_vdo + R_fixed)

constexpr float R_FIXED = 100.0f;   // Ω Messwiderstand
constexpr float R_VDO_MIN = 10.0f;  // Ω bei 0 bar (DRUCK HOCH — Warnleuchte würde leuchten)

float vdo_to_pressure(float r_vdo) {
    // Linear Interpolation: 10Ω=0bar, 180Ω=5bar
    // Aber: VDO ist nicht perfekt linear! Tabelle verwenden:
    // resistance_to_pressure Lookup Table
    const float vdo_table[][2] = {
        {10.0f,  0.0f},   // 0 bar
        {36.4f,  1.0f},   // 1 bar
        {62.8f,  2.0f},   // 2 bar
        {89.2f,  3.0f},   // 3 bar
        {115.6f, 3.5f},   // 3.5 bar
        {142.0f, 4.0f},   // 4 bar
        {180.0f, 5.0f},   // 5 bar
    };
    // Linear interpolation between table entries
    for (int i = 0; i < 6; i++) {
        if (r_vdo <= vdo_table[i+1][0]) {
            float t = (r_vdo - vdo_table[i][0]) / (vdo_table[i+1][0] - vdo_table[i][0]);
            return vdo_table[i][1] + t * (vdo_table[i+1][1] - vdo_table[i][1]);
        }
    }
    return 5.0f; // max
}
```

---

## Warn-Logik

### Warnstufen

| Stufe | Bedingung | Anzeige | Aktion |
|-------|-----------|---------|--------|
| **INFO** | Alles normal | Grüner Rahmen | Keine |
| **WARN** | Öldruck <0.8 bar ODER Temp >110°C ODER Volt <12.5V @>2000rpm | Gelber Rahmen + Piep (1×) | Hinweis |
| **CRIT** | Öldruck <0.5 bar ODER Temp >125°C ODER Volt >15.5V | Roter blinkender Rahmen + Piep (3×) | Motor prüfen! |
| **EMERGENCY** | Öldruck = 0 bar BEI RPM >1500 | VOLLROT blinkend + Dauerpiep | SOFORT ANHALTEN! |

### Display-Warnungen

```
┌──────────────────────────────────┐
│  ⚠️ ÖLDRUCK WARNUNG ⚠️         │
│                                  │
│  ▼ Öldruck: 0.6 bar            │
│    Normal: 2.0 bar @3000rpm     │
│                                  │
│  !!! MOTOR PRÜFEN !!!          │
│  Ölstand kontrollieren          │
│  Nicht weiterfahren!            │
│                                  │
│  [Bestätigen]  [Diagnose]       │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│  🔴 STATOR ÜBERGESPANNUNG 🔴   │
│                                  │
│  ⚡ 15.7V — REGLER DEFEKT!     │
│    Motor SOFORT abstellen!       │
│    Batterie-Gefahr!             │
│                                  │
│  [Notlauf: Verbraucher reduz.]  │
└──────────────────────────────────┘
```

---

## Akustische Warnung

**Piezo-Buzzer** (aktiver Buzzer, 3-5V, ~85dB) auf GPIO33:
- 1× Piep = WARNUNG (Öldruck niedrig, Temperatur hoch)
- 3× Piep = KRITISCH (Öldruck kritisch, Stator-Überspannung)
- Dauerpiep = NOTFALL (Öldruck = 0 @ RPM > Leerlauf)

```cpp
constexpr uint8_t BUZZER_PIN = 33;

void buzzer_beep(uint8_t count, uint16_t duration_ms = 200, uint16_t pause_ms = 100) {
    for (uint8_t i = 0; i < count; i++) {
        digitalWrite(BUZZER_PIN, HIGH);
        delay(duration_ms);
        digitalWrite(BUZZER_PIN, LOW);
        if (i < count - 1) delay(pause_ms);
    }
}
```

---

## Hardware-Ergänzungen

| Komponente | Model | Preis (€) | GPIO | Bemerkung |
|-----------|-------|-----------|------|-----------|
| Öldrucksensor | VDO 360-081 (M10×1.0) | ~25 | GPIO4 | Analog, 0-5 bar |
| Messwiderstand | 100Ω 1% | ~1 | — | Für VDO-Spannungsteiler |
| Piezo Buzzer | 3V-5V aktiv | ~3 | GPIO33 | 85dB Warnung |
| — | Stator-Messung | — | GPIO35 | Nur Batteriespannung (bestehend) |

**Zusatzkosten: ~€29** (Öldrucksensor + Buzzer + Widerstand)

---

## Integration in bestehenden Code

### sensors.h — Neue Sensoren

```cpp
// Stator-Monitoring (bestehender voltage_sensor erweitert)
struct StatorData {
    float v_batt;          // Batteriespannung (V)
    float v_stator_ac;     // Stator-AC-Spitze (V) — optional, braucht extra Teiler
    StatorStatus status;   // Stator-Status
    float charging_amps;   // Ladestrom (A) — optional, braucht Shunt
    uint32_t status_changed_ms; // Letzte Statusänderung
};

// Öldruck-Monitoring (NEU)
struct OilPressureData {
    float pressure_bar;    // Aktueller Öldruck (bar)
    bool warning;          // Öldruck niedrig
    bool critical;         // Öldruck kritisch
    float resistance_ohm;  // VDO-Widerstand (debug)
    uint32_t last_update_ms;
};
```

### Warn-System

```cpp
enum class WarningLevel : uint8_t {
    NONE = 0,
    INFO = 1,
    WARN = 2,
    CRIT = 3,
    EMERGENCY = 4
};

struct Warning {
    WarningLevel level;
    const char* message;
    const char* detail;
    uint32_t since_ms;   // wann die Warnung begann
    bool acknowledged;    // Benutzer hat bestätigt
};

// Warn-Queue (max 3 aktive Warnungen)
Warning active_warnings[3];
uint8_t warning_count = 0;

void checkWarnings() {
    // Öldruck prüfen
    if (oil.pressure_bar < OIL_PRESSURE_CRIT && rpm > 1500) {
        addWarning(WarningLevel::EMERGENCY, "ÖLDRUCK KRITISCH!", "Motor sofort abstellen!");
    } else if (oil.pressure_bar < OIL_PRESSURE_LOW) {
        addWarning(WarningLevel::WARN, "Öldruck niedrig", "Ölstand prüfen");
    }

    // Stator prüfen
    if (stator.v_batt > V_REGULATOR_FAIL) {
        addWarning(WarningLevel::CRIT, "STATOR ÜBERGESPANNUNG!", "Regler möglicherweise defekt!");
    } else if (stator.status == STATOR_NOT_CHARGING && rpm > 2000) {
        addWarning(WarningLevel::WARN, "Stator lädt nicht", "Batterie entlädt sich!");
    }

    // Temperatur
    if (cylinder_temp > TEMP_CRITICAL) {
        addWarning(WarningLevel::CRIT, "MOTOR ÜBERHITZUNG!", "Temperatur >125°C!");
    } else if (cylinder_temp > TEMP_WARNING) {
        addWarning(WarningLevel::WARN, "Temperatur hoch", "Motor kühlen lassen");
    }
}
```

---

## Öldruck-Referenzwerte NX650 RFVC

| Zustand | Öldruck (bar) | Temperatur (°C) |
|----------|--------------|----------------|
| Kaltstart | 3.0-4.5 | <40°C |
| Leerlauf warm | 0.8-1.5 | 80-100°C |
| 3000rpm warm | 2.0-3.5 | 80-100°C |
| 6000rpm warm | 3.0-4.0 | 85-105°C |
| HOCHSCHUB kalt | 4.0-5.0 | <50°C |
| **WARNUNG** | <0.8 @warm | >100°C |
| **KRITISCH** | <0.5 @any | >110°C |

---

## Wiring Diagram (Öldrucksensor)

```
        3.3V
         │
    ┌────┤──── 100Ω 1% Festwiderstand
    │    │
    │    ├──→ GPIO4 (ADC1_CH0)
    │    │
    │  VDO 360-081
    │  Öldruckgeber
    │  (10-180Ω)
    │    │
    └────┤──── GND
         │

ADC → Widerstand berechnen:
R_vdo = R_fixed × (3.3V / V_adc - 1)
Pressure = vdo_to_pressure(R_vdo)
```

---

## Roadmap

1. **Phase 1 — Stator-Monitor** (1 Tag)
   - Spannungsmessung optimieren (bestehend, erweitert)
   - Stator-Status-Logik implementieren
   - Warn-Schwelle auf Display

2. **Phase 2 — Öldrucksensor** (2 Tage)
   - VDO-Sensor anbringen (M10×1.0 adaption)
   - ADC-Kalibrierung mit VDO-Tabelle
   - Warn-Logik + Piep-Buzzer

3. **Phase 3 — Warn-System** (1 Tag)
   - Warn-Queue, Prioritäten, Bestätigung
   - Display-Warnungen (Overlay)
   - Akustische Signale

4. **Phase 4 — Langzeittest** (laufend)
   - Daten aufzeichnen (BLE → Companion App)
   - Schwellwerte kalibrieren
   - Öldruckkurven bei verschiedenen Temperaturen/RPM