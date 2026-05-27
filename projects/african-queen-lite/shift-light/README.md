# 🔴 Shift-Light & RPM-Indicator — African Queen Lite

## Vision
**WS2812 RGB LED-Ring als Shift-Light + RPM-Anzeige** — rund um den TFT-Tacho oder als separates Element am Lenker. Visualisiert Drehzahlbereich, zeigt optimalen Schaltzeitpunkt und warnt vor Überdrehung.

---

## Hardware

| Komponente | Menge | Preis (€) | Bemerkung |
|-----------|------|-----------|-----------|
| WS2812B LED Strip/Ring | 16 LEDs | ~5 | 5V, einzeln adressierbar |
| 3D-Druck Ring-Halterung | 1 | ~3 | PETG, passend zum TFT-Rahmen |
| 470Ω Widerstand | 1 | ~0.10 | Daten-Leitung Schutzwiderstand |
| 1000µF Elko | 1 | ~0.50 | Spannungs-Entkoppelung LED-Strom |

**Zusatzkosten: ~€8** (WS2812B Strip + Widerstand + Elko)

### Pin-Belegung

| Signal | GPIO | Bemerkung |
|--------|------|-----------|
| LED-Daten | GPIO32 | WS2812B Data (bestehend aus Ride-Mode Controller) |
| LED-VCC | 5V | Direkt am LM2596 Step-Down Ausgang |
| LED-GND | GND | Gemeinsame Masse |

### Stromaufnahme

```
16 LEDs × 60mA (volle Helligkeit weiß) = 960mA maximum
→ Dimmen auf 30% Helligkeit = ~288mA (akzeptabel für Step-Down)
→ Nachtfahrt: 10% Helligkeit = ~96mA
→ Einzelne LED Farbe: 20mA × 1 LED = 20mA
```

---

## LED-Layout (16 LEDs,环形 angeordnet)

```
        LED 0 (12 Uhr)
    LED 15          LED 1
  LED 14              LED 2
  LED 13              LED 3
    LED 12          LED 4
        LED 11      LED 5
     LED 10          LED 6
        LED 9  LED 8  LED 7
            LED 7.5 (6 Uhr)
```

### RPM-Zuordnung

| LED-Bereich | RPM-Bereich | Farbe | Bedeutung |
|-------------|------------|-------|-----------|
| LED 0-3 (12-3 Uhr) | 0-3000 | Grün | Normal / Schonend |
| LED 4-7 (3-6 Uhr) | 3000-5500 | Gelb | Drehzahl-Bereich |
| LED 8-10 (6-7:30) | 5500-6500 | Orange | Leistung-Bereich |
| LED 11-13 (7:30-10:30) | 6500-7200 | Rot | HOCHDREHZAHL |
| LED 14-15 (10:30-12) | 7200-7500 | Rot blinkend | REDLINE ⚠️ |

### Shift-Light Logik

```cpp
// Shift-Point pro Gang und Ride-Mode
constexpr uint16_t SHIFT_RPM[MODE_COUNT][6] = {
    // Mode      N     1.G    2.G    3.G    4.G    5.G
    /* STRASSE */ {0,    5500,  5800,  6000,  6200,  6400},
    /* STADT   */ {0,    4000,  4500,  4800,  5000,  5200},
    /* GELÄNDE */ {0,    6000,  6200,  6400,  6600,  6800},
    /* SPORT   */ {0,    7000,  7200,  7300,  7400,  7500},
    /* COMFORT */ {0,    4500,  4800,  5000,  5200,  5400},
    /* SOUND   */ {0,    5500,  5800,  6000,  6200,  6400},
};

// RPM-Grenzwerte
constexpr uint16_t RPM_IDLE      = 1300;  // Leerlauf
constexpr uint16_t RPM_LOW       = 2000;  // Unterdrehung (warnen bei Schubbetrieb)
constexpr uint16_t RPM_POWER     = 5500;  // Drehzahl wo Leistung beginnt
constexpr uint16_t RPM_SHIFT_SUG = 6000;  // Vorgeschlagener Shift-Point (STRASSE)
constexpr uint16_t RPM_REDLINE   = 7500;  // REDLINE — NICHT ÜBERSCHREITEN!
constexpr uint16_t RPM_LIMIT     = 8000;  // HARDCUT (falls CDI Rev-Limiter)
```

---

## Shift-Light Animationen

### 1. RPM-Balken (Standard)
```cpp
void drawRpmBar(uint16_t rpm, RideMode mode) {
    // Mappe RPM auf LED-Anzahl (0-15 LEDs)
    float rpm_percent = constrain((float)(rpm - RPM_IDLE) / (RPM_REDLINE - RPM_IDLE), 0.0f, 1.0f);
    int lit_leds = (int)(rpm_percent * 15.99f);  // 0-15
    
    for (int i = 0; i < 16; i++) {
        if (i <= lit_leds) {
            // Farbe basierend auf Position
            if (i <= 3)        strip.setPixelColor(i, GREEN);
            else if (i <= 7)   strip.setPixelColor(i, YELLOW);
            else if (i <= 10)  strip.setPixelColor(i, ORANGE);
            else               strip.setPixelColor(i, RED);
        } else {
            strip.setPixelColor(i, 0);  // Aus
        }
    }
    strip.show();
}
```

### 2. Shift-Flash (Schaltzeitpunkt)
```cpp
void shiftFlash(RideMode mode) {
    // Alle LEDs BLITZEN 3× weiß wenn Shift-Point erreicht
    for (int flash = 0; flash < 3; flash++) {
        for (int i = 0; i < 16; i++) strip.setPixelColor(i, WHITE_30PCT);
        strip.show();
        delay(80);
        for (int i = 0; i < 16; i++) strip.setPixelColor(i, 0);
        strip.show();
        delay(80);
    }
}
```

### 3. Redline-Warnung
```cpp
void redlineWarning() {
    // Alle LEDs PULSIEREN rot bei RPM > 7200
    static uint8_t brightness = 0;
    static int8_t dir = 5;
    brightness += dir;
    if (brightness >= 255 || brightness <= 30) dir = -dir;
    
    for (int i = 0; i < 16; i++) {
        strip.setPixelColor(i, strip.Color(brightness, 0, 0));
    }
    strip.show();
}
```

### 4. Mode-Anzeige (bei Moduswechsel)
```cpp
void modeIndicator(RideMode mode) {
    // Alle LEDs in Mode-Farbe für 2 Sekunden
    ModeColor c = MODE_COLORS[mode];
    for (int i = 0; i < 16; i++) {
        strip.setPixelColor(i, strip.Color(c.r, c.g, c.b));
    }
    strip.show();
    // Nach 2s → RPM-Anzeige
}
```

### 5. Startup-Animation
```cpp
void startupAnimation() {
    // LED-Ring läuft einmal im Kreis (Rot → Orange → Gelb → Grün)
    for (int i = 0; i < 16; i++) {
        strip.setPixelColor(i, strip.Color(0, 255, 0)); // Grün
        strip.show();
        delay(50);
    }
    delay(200);
    // Alle aus
    strip.clear();
    strip.show();
}
```

---

## Helligkeitssteuerung

### Tag/Nacht-Erkennung

| Modus | Helligkeit | Trigger |
|------|-----------|---------|
| Tag | 30% (48/255) | Standard, LDR > Schwellwert |
| Dämmerung | 15% (38/255) | LDR < Schwellwert |
| Nacht | 8% (20/255) | LDR sehr niedrig ODER manuell |
| Shift-Flash | 100% (255/255) | Immer maximale Helligkeit für 80ms |

### LDR-Schaltung (optional)

```
        3.3V
         │
    ┌────┤──── 10kΩ Pull-Up
    │    │
    │    ├──→ GPIO39 (ADC) — Lichtsensor
    │    │
    │  LDR (GL5528, ~10kΩ hell, ~1MΩ dunkel)
    │    │
    └────┤──── GND
```

**Problem:** GPIO39 ist schon für Hall-Speed belegt!
**Lösung:** Lichtsensor auf **GPIO13** verschieben (nur RPM-Pulse, der kann ADC1 lesen im Leerlauf oder zeitgemultiplext) **ODER** feste Helligkeit pro Ride-Mode:
- STRASSE/STADT/COMFORT: 15% (unauffällig)
- GELÄNDE/SPORT: 30% (Blickfang)
- SOUND: 20% (mittleres Blinken)

---

## Daytime Running Light (TVO-zulassung)

**Achtung StVZO in Deutschland:**
- Farbige LEDs am Motorrad dürfen **NICHT** nach vorne strahlen (nur weißes Abblendlicht erlaubt)
- Shift-Light muss **nach hinten/zu dem Fahrer** gerichtet sein, nicht nach vorne
- Lösung: LED-Ring **im Tacho-Gehäuse** (nur Fahrer sieht es) oder unter der Sitzbank
- Grüne/rote LEDs die nach **vorne** strahlen = **verboten** → Ring MUSS im Instrumentenbereich montiert sein

---

## Integration in bestehenden Code

### Neue Dateien

```
dashboard/src/
├── shift_light.h     ← Shift-Light Logik + Animationen (NEU)
├── led_indicator.h    ← Bestehend, erweitert um RPM-Modus
└── modes.h            ← Shift-RPM-Tabelle hinzugefügt
```

### shift_light.h (Pseudocode)

```cpp
#pragma once
#include <Adafruit_NeoPixel.h>
#include "modes.h"

class ShiftLight {
public:
    void init(uint8_t pin, uint16_t num_leds);
    void update(uint16_t rpm, uint8_t gear, RideMode mode);
    void showMode(RideMode mode, uint16_t duration_ms);
    void startup();
    void setBrightness(uint8_t percent);
    
private:
    Adafruit_NeoPixel strip;
    uint8_t brightness;
    bool shift_flash_active;
    uint32_t shift_flash_end_ms;
    
    void drawRpmBar(uint16_t rpm);
    void drawRedline();
    void drawShiftFlash();
    void drawModeColor(RideMode mode);
};
```

---

## Roadmap

1. **Phase 1 — RPM-Balken** (0.5 Tag)
   - WS2812B initialisieren
   - RPM auf LEDs mappen
   - Helligkeit dimmen

2. **Phase 2 — Shift-Flash** (0.5 Tag)
   - Gang-abhängiger Shift-Point
   - Mode-abhängige RPM-Tabelle
   - Flash-Animation

3. **Phase 3 — Redline-Warnung** (0.5 Tag)
   - Pulsierende rote LED bei >7200rpm
   - Akustische Warnung (Buzzer)

4. **Phase 4 — Integration** (0.5 Tag)
   - In main.cpp einbinden
   - Mode-Anzeige bei Moduswechsel
   - Startup-Animation

**Total: ~2 Tage**