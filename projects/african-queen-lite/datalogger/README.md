# 📊 Datalogger & BLE-Telemetrie — African Queen Lite

## Vision
**Echtzeit-Fahrdaten auf dem Smartphone anzeigen und aufzeichnen** — per Bluetooth Low Energy (NimBLE) vom ESP32 an eine Companion-App.

Alle Sensordaten die der ESP32 ohnehin erfasst (RPM, Speed, Temp, Volt, Öldruck, Gang, Tank, GPS) werden über BLE als Notification-Service gesendet. Eine Smartphone-App (React Native oder PWA) zeigt Live-Dashboard + zeichnet Fahrten als FIT/GPX auf.

---

## BLE-Service-Architektur

### GATT Services

| Service | UUID | Characteristic | UUID | Daten |
|---------|------|----------------|------|-------|
| **Ride Data** | `0x181A` (Environmental Sensing) | RPM | `0x2A1E` | uint16 (0-9999 rpm) |
| | | Speed | custom | uint16 (0-299 km/h × 10) |
| | | Gear | custom | uint8 (0=N, 1-5) |
| | | Temp | `0x2A6E` | int16 (°C × 10, -40 bis 150) |
| | | Voltage | custom | uint16 (mV, 0-20000) |
| | | Oil Press | custom | uint8 (0=OK, 1=WARN, 2=CRIT) |
| | | Fuel | custom | uint8 (0-100%) |
| | | Mode | custom | uint8 (0-5 ride modes) |
| **GPS** | `0x1819` (Location) | Lat/Lon | `0x2A6C` | int32/int32 (°×1e7) |
| | | Alt+Speed | `0x2A6D` | int16+uint16 |
| | | Satellites | custom | uint8 |
| **Trip** | custom | Trip A | custom | uint32 (meters) |
| | | Trip B | custom | uint32 (meters) |
| | | Odometer | custom | uint32 (km × 10) |
| **Config** | custom | Mode Select | custom | uint8 WRITE (0-5) |
| | | Display Mode | custom | uint8 WRITE (0-3) |
| | | Reset Trip A | custom | uint8 WRITE (0xAA=reset) |

### BLE Update-Raten

| Characteristic | Update-Intervall | Priority |
|---------------|-----------------|----------|
| RPM | 100ms | Hoch |
| Speed | 200ms | Hoch |
| Gear | 500ms | Mittel |
| Temp, Voltage | 1000ms | Niedrig |
| Oil Press | 1000ms (oder sofort bei Änderung) | Hoch |
| Fuel | 5000ms | Niedrig |
| GPS Position | 1000ms | Mittel |
| Trip/Odometer | 5000ms | Niedrig |

### Bandbreiten-Rechnung

- **Pro Update:** ~20 Bytes (RPM+Speed+Gear+Temp+Volt+Oil+Fuel+Mode)
- **Bei 100ms RPM-Interval:** max 200 Bytes/s = 1600 bps
- **BLE 4.2:** max 260 kbps → **kein Problem**, 0.6% Auslastung
- **NimBLE** auf ESP32 stack: ~2ms per Notification, also 4-5 Characteristics gleichzeitig non-blocking

---

## Companion-App

### Platform: PWA (Progressive Web App)
- **Warum PWA?** Kein App Store nötig, funktioniert auf Android+iOS, eine Codebasis
- **Tech-Stack:** React + Vite + TailwindCSS + Web Bluetooth API
- **Offline:** Service Worker cached die App, FIT-Dateien lokal bis Upload

### App-Screens

```
┌─────────────────────────────┐
│   🏍️ AQL Datalogger         │
│                              │
│   ┌─────────┐ ┌─────────┐   │
│   │ 7,500   │ │ 127     │   │
│   │  RPM    │ │  km/h   │   │
│   └─────────┘ └─────────┘   │
│                              │
│   ┌─────┐┌─────┐┌──────┐    │
│   │ 3rd ││ 78° ││ 12.8V│    │
│   │GEAR ││ C   ││      │    │
│   └─────┘└─────┘└──────┘    │
│                              │
│   ┌─────────────────────┐   │
│   │ FUEL ████░░░░ 65%   │   │
│   │ OIL  ✅ OK          │   │
│   │ MODE 🟢 STRASSE     │   │
│   └─────────────────────┘   │
│                              │
│   ─────────────────────────  │
│   🔴 REC  00:47:23  47.2km  │
│   [STOP]  [EXPORT .FIT]      │
└─────────────────────────────┘
```

### Features

1. **Live-Dashboard** — Real-Timer RPM, Speed, Temp, Volt, Gear, Oil, Fuel, Mode
2. **Aufzeichnung** — Start/Stop Rec, speichert alle Sensordaten mit Timestamp
3. **Export** — .FIT (Garmin/Strava), .GPX (Universal), .CSV (Rohdaten)
4. **Mode-Switch** — Fahrtmodi vom Smartphone aus umschalten
5. **Diagnose** — Stator-Spannung, Batterie-Verlauf, Temperatur-Verlauf als Chart
6. **OTA-Update** — ESP32-Firmware über BLE aktualisieren (NimBLE OTA Service)

### FIT-Datei Export

```javascript
// Strava-kompatibel:Activity FIT File
// Minimaler FIT-Header + Record Messages:
// - Timestamp (uint32, seconds since FIT_EPOCH)
// - Latitude (int32, semicircles)
// - Longitude (int32, semicircles)
// - Altitude (uint16, 5m resolution)
// - Heart Rate (uint8) — nicht verfügbar auf NX650, 0 = HRM optional
// - Speed (uint16, mm/s)
// - Temperature (int8, °C)
```

---

## ESP32 NimBLE-Implementation

### Service-Definition (Pseudocode)

```cpp
// In bluetooth.h (bestehend → erweitert)

class BLETelemetry {
public:
    void init();
    void startAdvertising();
    void updateRPM(uint16_t rpm);
    void updateSpeed(uint16_t speed_kmh_x10);
    void updateGear(uint8_t gear);
    void updateTemp(int16_t temp_c_x10);
    void updateVoltage(uint16_t mv);
    void updateOilPressure(uint8_t status); // 0=OK, 1=WARN
    void updateFuel(uint8_t percent);
    void updateMode(uint8_t mode);
    void updateGPS(int32_t lat, int32_t lon, int16_t alt, uint8_t sats);

    bool isConnected() { return deviceConnected; }

private:
    NimBLEServer* pServer;
    NimBLEService* pRideService;
    NimBLEService* pGPSService;
    NimBLEService* pTripService;
    NimBLEService* pConfigService;

    NimBLECharacteristic* pCharRPM;
    NimBLECharacteristic* pCharSpeed;
    NimBLECharacteristic* pCharGear;
    NimBLECharacteristic* pCharTemp;
    NimBLECharacteristic* pCharVoltage;
    NimBLECharacteristic* pCharOilPress;
    NimBLECharacteristic* pCharFuel;
    NimBLECharacteristic* pCharMode;
    NimBLECharacteristic* pCharGPSLatLon;
    NimBLECharacteristic* pCharGPSAltSpeed;
    NimBLECharacteristic* pCharGPSSats;
    NimBLECharacteristic* pCharTripA;
    NimBLECharacteristic* pCharTripB;
    NimBLECharacteristic* pCharOdometer;
    NimBLECharacteristic* pCharModeSelect;  // WRITE
    NimBLECharacteristic* pCharDisplayMode;  // WRITE
    NimBLECharacteristic* pCharResetTripA;   // WRITE

    bool deviceConnected = false;
};
```

---

## Daten-Logging (ESP32-Seite)

### Ring Buffer für Offline-Aufzeichnung

```cpp
// Wenn BLE nicht verbunden → Daten ins LittleFS loggen
constexpr size_t LOG_BUFFER_SIZE = 8192; // 8KB Ring Buffer
constexpr size_t LOG_FILE_MAX = 524288;  // 512KB max pro Datei (= ~30 Min bei 100ms)

struct LogEntry {
    uint32_t timestamp_ms;  // millis()
    uint16_t rpm;
    uint16_t speed_kmh_x10;
    uint8_t  gear;
    int16_t  temp_c_x10;
    uint16_t voltage_mv;
    uint8_t  oil_status;
    uint8_t  fuel_percent;
    uint8_t  ride_mode;
};  // 14 bytes pro Eintrag

// Bei 100ms Interval: 10 Einträge/s × 14B = 140 Bytes/s
// 512KB Datei = ~60 Minuten Aufzeichnung
// 4MB LittleFS = ~8 Dateien = ~8 Stunden
```

### Export-Format

| Format | Größe (1h) | Strava | Implementierung |
|--------|------------|--------|-----------------|
| CSV | ~500KB | ✗ | Einfachste, Debug |
| GPX | ~300KB | ✓ | Standard GPS |
| FIT | ~150KB | ✓✓ | Optimal für Strava |

---

## Companion-App Projektstruktur

```
aql-companion/
├── package.json
├── vite.config.ts
├── index.html
├── public/
│   ├── manifest.json          # PWA Manifest
│   ├── sw.js                  # Service Worker
│   └── icons/                 # App-Icons (192/512)
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── ble/
│   │   ├── connection.ts      # Web Bluetooth API, connect/disconnect
│   │   ├── services.ts        # GATT Service/Characteristic UUIDs
│   │   └── parser.ts          # DataView → Typisierte Werte
│   ├── components/
│   │   ├── Dashboard.tsx       # Live-Gauge-Grid
│   │   ├── Gauge.tsx          # Kreisförmiger RPM/Speed-Gauge
│   │   ├── BarGauge.tsx       # Tank/Temp-Balken
│   │   ├── Recording.tsx      # Start/Stop/Export
│   │   ├── Diagnostics.tsx    # Sensor-Diagnose
│   │   └── ModeSelector.tsx   # Ride Mode Buttons
│   ├── hooks/
│   │   ├── useBLE.ts          # BLE Connection Hook
│   │   └── useRecording.ts    # Aufzeichnung + FIT-Export
│   ├── lib/
│   │   ├── fit-writer.ts      # FIT-Datei Generator
│   │   ├── gpx-writer.ts      # GPX-Datei Generator
│   │   └── csv-writer.ts      # CSV-Export
│   └── styles/
│       └── globals.css
└── README.md
```

---

## Hardware-Einfluss auf bestehendes Projekt

### BLE-Modul: ESP32 intern
- **Kein extra Modul!** ESP32 hat BLE 4.2 onboard
- NimBLE läuft auf Core 0, Display+Sensoren auf Core 1
- Stromverbrauch: BLE active ≈ +20mA (vs.gesamt ~150mA ESP32 + Display)

### Antenne
- PCB-Antenne auf ESP32 DevKit → Reichweite ~10m (ausreichend für Motorrad → Helm-Display)
- Externe Antenne möglich (IPEX-Connector), aber für AQL nicht nötig

### Stromversorgung
- BLE active: ESP32 zieht ~120-160mA gesamt (mit Display + BLE)
- LM2596 Step-Down liefert 3A → kein Problem
- Sleep-Mode möglich: Display aus, BLE advertising only (~10mA)

---

## Kosten

| Komponente | Preis | Bemerkung |
|-----------|-------|-----------|
| ESP32 DevKit V1 | — | Schon im Build (Ride-Mode-Controller) |
| NimBLE Library | FOSS | Arduino Library Manager |
| PWA Companion App | FOSS | Selbst entwickelt |

**Zusatzkosten: €0** — BLE ist im ESP32 eingebaut, App ist Software.

---

## Roadmap

1. **Phase 1 — BLE Service** (2-3 Tage)
   - Alle GATT-Services implementieren
   - ESP32 advertising + connection
   - Test mit nRF Connect App (Android/iOS)

2. **Phase 2 — Daten-Logging** (1-2 Tage)
   - Ring Buffer + LittleFS-Datei-Logging
   - CSV-Export über BLE oder USB

3. **Phase 3 — PWA Companion** (3-5 Tage)
   - Web Bluetooth API Connection
   - Live-Dashboard
   - FIT/GPX Export

4. **Phase 4 — Polishing** (1-2 Tage)
   - Mode-Switch über App
   - Diagnostics-Screen
   - OTA-Update Service

**Total: ~1-2 Wochen Entwicklung**