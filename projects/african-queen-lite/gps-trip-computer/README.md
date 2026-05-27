# 🗺️ GPS-Trip-Computer — African Queen Lite

## Vision
**Vollständiger Trip-Computer mit GPS-Tracking, Odometer, Durchschnittsgeschwindigkeit und Höhenprofil** — alles auf dem ESP32 + NEO-M8N GPS-Modul, Daten lokal gespeichert und per BLE an die Companion-App exportierbar.

---

## Warum GPS-Trip-Computer?

- **NX650 hat KEINEN E-Odometer** — mechanischer Tacho mit Tachowelle
- Trip A/B und Gesamtkilometer sind **analog und ungenau**
- GPS liefert: **Position, Speed, Höhe, Uhrzeit, Satelliten** — alles was man braucht
- Kombiniert mit Hall-Speed-Sensor: GPS = Referenz, Hall = Echtzeit-Speed
- FIT/GPX-Export direkt auf dem ESP32 → Strava-kompatibel

---

## Hardware

| Komponente | Model | Preis (€) | Interface | Bemerkung |
|-----------|-------|-----------|-----------|-----------|
| GPS-Modul | U-Blox NEO-M8N | ~10 | UART (9600 baud) | 72 Kanäle, 10Hz Update, -167dBm |
| GPS-Antenne | Keramik-Patch (onboard) | ~0 | — | Im NEO-M8N Modul integriert |
| Externe Antenne | SMA-Adapter + Antenne | ~5 | IPEX → SMA | Für Unter-Sitzbank-Montage |

**Zusatzkosten: ~€10-15** (NEO-M8N Modul)

### Pin-Belegung

| Signal | GPIO | Bemerkung |
|--------|------|-----------|
| GPS TX → ESP32 RX | GPIO16 | UART2 RX (bestehend, geteilt mit BLE!) |
| GPS RX ← ESP32 TX | GPIO17 | UART2 TX (bestehend, geteilt mit BLE!) |

**⚠️ KONFLIKT: UART2 wird bereits für BLE (NimBLE) genutzt!**

### Lösung: GPS auf UART1 (Hardware Serial)

```cpp
// UART0: USB Debug (115200)
// UART1: GPS (9600) — GPIO4 (RX) und GPIO2 (TX) oder andere freie Pins
// UART2: BLE Module (falls extern) — GPIO16/17

// GPS auf UART1 mit flexiblen Pins
HardwareSerial gpsSerial(1);  // UART1
gpsSerial.begin(9600, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN);

// Pin-Optionen für UART1:
// RX: GPIO9 (Flash-Pin! Vermeiden) oder GPIO13 oder GPIO35(nur Input)
// TX: GPIO10 (Flash-Pin! Vermeiden) oder GPIO12
// → Best: GPIO12 (TX) und GPIO13 (RX) — beide frei nach Pin-Remap
```

**Finale GPS-Pins:**
| Signal | GPIO | Bemerkung |
|--------|------|-----------|
| GPS RX (ESP TX) | GPIO12 | UART1 TX |
| GPS TX (ESP RX) | GPIO13 | UART1 RX |

*(GPIO13 war ursprünglich für RPM Pulse geplant → RPM auf GPIO14 oder GPIO27 verschieben)*

---

## GPS-Bibliothek

**TinyGPSPlus** (aka TinyGPS++) — Arduino Library von Mikal Hart

```cpp
#include <TinyGPSPlus.h>

TinyGPSPlus gps;

void gpsLoop() {
    while (gpsSerial.available() > 0) {
        char c = gpsSerial.read();
        if (gps.encode(c)) {
            // Neue GPS-Daten verfügbar
            if (gps.location.isValid()) {
                current_lat = gps.location.lat();  // Double
                current_lon = gps.location.lng();  // Double
                current_alt = gps.altitude.meters(); // Double
                current_sat = gps.satellites.value(); // uint32
                current_hdop = gps.hdop.hdop();     // float (meters)
            }
            if (gps.speed.isValid()) {
                current_speed_kmh = gps.speed.kmph(); // Double
            }
            if (gps.date.isValid() && gps.time.isValid()) {
                // GPS-Zeit → RTC oder Systemzeit
                current_hour = gps.time.hour();
                current_min = gps.time.minute();
                current_sec = gps.time.second();
            }
        }
    }
}
```

---

## Trip-Computer Features

### 1. Trip A/B — Zwei unabhängige Trip-Zähler

```cpp
struct TripData {
    uint32_t distance_m;       // Meter (aus GPS oder Hall-Sensor)
    uint32_t duration_s;       // Sekunden
    uint16_t max_speed_kmh;    // km/h (Maximum)
    uint32_t avg_speed_kmh_x10; // km/h × 10 (gewichtet)
    uint32_t fuel_used_ml;     // Milliliter (geschätzt aus Speed+RPM)
    uint32_t start_time_unix;  // Unix-Timestamp Start
    float    start_lat;        // Start-Position
    float    start_lon;
    // Berechnet:
    float avg_speed() { return duration_s > 0 ? (distance_m / 1000.0f) / (duration_s / 3600.0f) : 0; }
};
```

### 2. Odometer — Gesamtkilometer (persistiert in NVS)

```cpp
#include <Preferences.h>

Preferences prefs;

void saveOdometer(uint32_t total_km_x10) {
    prefs.begin("odometer", false);
    prefs.putUInt("total_km", total_km_x10);
    prefs.end();
}

uint32_t loadOdometer() {
    prefs.begin("odometer", true);
    uint32_t km = prefs.getUInt("total_km", 0);
    prefs.end();
    return km;
}
// NVS hat 100.000 Schreibzyklen → bei 10m-Auflösung = 10.000 km Updates
// Bei 50.000 km Lebensdauer → alle 500m schreiben = 100 Schreibzyklen → kein Problem
```

### 3. Höhenprofil

```cpp
struct AltitudeData {
    float current_alt;         // m (GPS)
    float alt_gain_total;     // m (Aufstieg gesamt)
    float alt_loss_total;     // m (Abstieg gesamt)
    float alt_max;            // m (Höchster Punkt)
    float alt_min;            // m (Tiefster Punkt)
    uint16_t grade_percent;   // Steigung/Gefälle (%)
};

// Steigungsberechnung aus GPS:
// grade = (alt_delta / dist_delta) × 100
// Gefiltert: gleitender Durchschnitt über 5 Sekungen
```

### 4. Fahrtenbuch

```cpp
struct RideLog {
    uint32_t ride_id;         // Eindeutige ID
    uint32_t date_start;      // Unix-Timestamp
    uint32_t date_end;
    uint32_t duration_s;
    uint32_t distance_m;
    uint16_t max_speed_kmh;
    float    max_rpm;
    float    avg_temp_c;
    float    avg_voltage;
    uint8_t  mode_most_used;  // Häufigster Ride-Mode
    float    start_lat, start_lon;
    float    end_lat, end_lon;
    float    alt_gain, alt_loss;
};
```

---

## Geschwindigkeitsquellen

### Dual-Source: Hall-Sensor + GPS

```cpp
enum SpeedSource {
    SPEED_HALL,    // Hall-Sensor am Vorderrad (primär, Echtzeit)
    SPEED_GPS,     // GPS-basiert (sekundär, Referenz)
    SPEED_BLEND    // Blended: Hall für Echtzeit, GPS für Kalibrierung
};

float current_speed;  // km/h, final
float speed_hall;      // vom Hall-Sensor
float speed_gps;       // vom GPS

// Blended Mode:
// - Hall-Sensor für Display-Update (100ms Latency)
// - GPS für Odometer (genauer, 1s Update)
// - GPS für Kalibrierung des Hall-Faktors
void updateSpeed() {
    if (gps.speed.isValid() && gps.speed.kmph() > 5.0f) {
        // GPS verfügbar und > 5 km/h (unter 5 km/h zu ungenau)
        speed_gps = gps.speed.kmph();
        
        // Kalibrierung: Hall-Faktor anpassen
        if (speed_hall > 5.0f) {
            float ratio = speed_gps / speed_hall;
            hall_calib_factor = hall_calib_factor * 0.95f + ratio * 0.05f; // Tiefpass
        }
    }
    
    // Finale Geschwindigkeit: Hall bevorzugt, GPS als Fallback
    if (speed_hall > 2.0f) {
        current_speed = speed_hall * hall_calib_factor; // Kalibriert
    } else if (speed_gps > 2.0f) {
        current_speed = speed_gps;
    } else {
        current_speed = 0.0f;
    }
}
```

---

## FIT-Datei Export (Strava-kompatibel)

### Minimaler FIT Activity File

```
Header (12 bytes):
  Protocol Version: 2.0
  Profile Version: 21.40
  Data Type: ".FIT"

Records (Timestamp + Daten):
  ogni 1-2 Sekunden:
  - timestamp (uint32, seconds since FIT_EPOCH = 1989-12-31)
  - position_lat (int32, semicircles = degrees × (2^31/180))
  - position_long (int32, semicircles)
  - altitude (uint16, 5 × meters + 500)
  - speed (uint16, 1000 × m/s)
  - heart_rate (uint8, 0 = keine HRM)
  - temperature (int8, °C)

Session Summary:
  - total_timer_time
  - total_distance
  - avg_speed
  - max_speed
  - avg_temperature
  - max_temperature
```

### FIT-Writer Implementierung

```cpp
// In gps_handler.cpp
class FITWriter {
public:
    bool begin(const char* filename);
    void writeHeader();
    void writeRecord(uint32_t timestamp, int32_t lat, int32_t lon, 
                     uint16_t alt, uint16_t speed, int8_t temp);
    void writeSessionSummary();
    bool end();
    
private:
    File fitFile;
    uint32_t start_time;
    uint32_t record_count;
    uint16_t crc;  // FIT CRC-16
};
```

---

## Companion App Integration

### Neue BLE-Characteristics (GPS Service)

| Characteristic | UUID | Type | Update | Inhalt |
|---------------|------|------|--------|--------|
| Position | 0x2A6C | int32+int32 | 1s | Lat/Lon (°×1e7 semicircles) |
| Alt+Speed | 0x2A6D | int16+uint16 | 1s | Alt(m) + Speed(0.01 m/s) |
| Satellites | custom | uint8 | 5s | Anzahl GPS-Satelliten |
| Trip A | custom | uint32+uint32 | 5s | Distance(m) + Duration(s) |
| Trip B | custom | uint32+uint32 | 5s | Distance(m) + Duration(s) |
| Odometer | custom | uint32 | 30s | Total km × 10 |
| Altitude | custom | float+float+float | 2s | Gain, Loss, Current alt |
| Ride Stats | custom | struct | 5s | Max speed, Avg speed, Max RPM, etc. |

### App-Feature: Live-Tracking

- **Auf dem Smartphone:** Echtzeit-Position + Geschwindigkeits-Balkendiagramm
- **Trip-Aufzeichnung:** Start → Fahrt → Stop → FIT-Export
- **Karten-Overlay:** Aktuelle Position auf Karte (OSM offline tiles)
- **Höhenprofil:** Live-Steigung/Gefälle als farbiger Balken

---

## Display-Anzeige (Trip-Computer Modus)

```
┌─────────────────────────────────────────┐
│  ┌─────────────────────────────────────┐│
│  │          127  km/h                  ││
│  │          ▕████████░░░░▏            ││
│  └─────────────────────────────────────┘│
│  ┌──────┐┌──────┐┌──────┐┌───────────┐│
│  │ TRIP ││  A:  ││  B:  ││ODO:       ││
│  │ 47.2 ││ 247  ││ 12.3 ││45,230 km  ││
│  │ km   ││ km   ││ km   ││           ││
│  └──────┘└──────┘└──────┘└───────────┘│
│  ┌─────────────────────────────────────┐│
│  │ AVG: 62 km/h  MAX: 135 km/h       ││
│  │ ↑523m ↓412m  ⛰ Max: 654m         ││
│  │ 🛣 12° 14.567'N  50° 55.234'E    ││
│  │ 📡 8 SAT  HDOP: 1.2m  🕐 14:32    ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

---

## GPS-Antennenplatzierung

### Option A: Unter Sitzbank (Empfohlen)
- ✅ Wettergeschützt
- ✅ Keine optische Störung
- ✅ Nah am ESP32 (kurzes Kabel)
- ⚠️ GPS-Signal leicht reduziert durch Rahmen (aber NEO-M8N ist sensitiv)
- → Patch-Antenne nach oben, kein Metall direkt darüber

### Option B: Unter Lenker-Clamp
- ✅ Gute Sicht nach oben
- ⚠️ Exponiert (Regen, Vibration)
- → Braucht IP67-Gehäuse

### Option C: Am Tacho-Gehäuse
- ✅ Integriert
- ⚠️ Störung durch TFT-SPI-Signale möglich
- ⚠️ Platzbegrenzung

**→ Empfehlung: Option A (Unter Sitzbank)**

---

## Stromverbrauch GPS

| Zustand | Strom | Bemerkung |
|--------|-------|-----------|
| Continuous | ~25mA | 10Hz Update (max) |
| 1Hz Mode | ~18mA | 1 Update/s (Standard) |
| Power Save | ~8mA | Periodic, 1 Update/s |
| Backup | ~15µA | Nur RTC, kein Fix |

**→ 1Hz Mode reicht für Trip-Computer (18mA sind vernachlässigbar)**

---

## Konfiguration NEO-M8N

```cpp
// UBX-Kommandos für Optimierung (via UART1)
// 1Hz Update-Rate (Standard)
constexpr uint8_t CFG_RATE_1HZ[] = {
    0xB5, 0x62, 0x06, 0x08, 0x06, 0x00, 0xE8, 0x03, 0x01, 0x00, 0x01, 0x00, 0x01, 0x39
};

// Nur NMEA-GGA + RMC (minimale Datenmenge)
constexpr uint8_t CFG_NMEA_MINIMAL[] = {
    // ... UBX-CFG-NMEA mit msg mask für GGA+RMC only
};

// Power Save Mode (Periodic)
constexpr uint8_t CFG_PSM[] = {
    0xB5, 0x62, 0x06, 0x11, 0x02, 0x00, 0x05, 0x00, 0x1E, 0x3A
};
```

---

## Projektstruktur

```
gps-trip-computer/
├── README.md               ← This file
├── gps_handler.h           ← GPS-Modul Treiber (NEO-M8N)
├── gps_handler.cpp
├── trip_meter.h            ← Trip A/B, Odometer
├── trip_meter.cpp
├── fit_writer.h            ← FIT-Datei Generator
├── fit_writer.cpp
├── altitude.h              ← Höhenprofil, Steigungsberechnung
├── altitude.cpp
└── CALIBRATION.md          ← Hall-Sensor vs GPS Kalibrierung
```

---

## Roadmap

1. **Phase 1 — GPS-Treiber** (1 Tag)
   - NEO-M8N auf UART1 initialisieren
   - NMEA-Parsing mit TinyGPSPlus
   - Position, Speed, Altitude, UTC extrahieren

2. **Phase 2 — Trip A/B + Odometer** (1 Tag)
   - Trip-Zähler (GPS-Distanz oder Hall-Distanz)
   - NVS-Persistenz (Odometer)
   - Trip-Reset über Taste oder BLE

3. **Phase 3 — FIT-Export** (2 Tage)
   - FIT-Datei Format implementieren
   - Header + Records + Session
   - LittleFS-Speicherung (1 FIT ≈ 150KB/h)

4. **Phase 4 — Companion App** (2-3 Tage)
   - BLE GPS-Service in PWA
   - Live-Position + Trip-Anzeige
   - FIT/GPX Download über BLE

**Total: ~6-7 Tage**