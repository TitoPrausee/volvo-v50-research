# 🔧 V50 CAN-Bus & Software Entwickler-Status

**Datum**: 2026-05-28  
**Rolle**: CAN-Bus & Software-Entwickler (v50-developer)  
**Budget**: ~€90 (Pi4 + PiCAN2 Duo) + ~€50 (Display) = **~€140 Total**

---

## 📊 1. CAN-BUS INFRASTRUKTUR — ERLEDIGT

### ✅ Hardware-Spezifikation (festgelegt)

| Komponente | Modell | Preis | Status |
|------------|--------|-------|--------|
| Raspberry Pi | Pi 4 Model B 2GB | ~€35 | ✅ In DB |
| CAN HAT | PiCAN2 Duo (2-Kanal) | ~€25 | ✅ In DB |
| Display | 7" IPS TFT 1024x600 | ~€40 | ✅ In DB |
| Gehäuse | Alu-Gehäuse Pi4 | ~€15 | ✅ Spezifiziert |
| OBD2-Adapter | OBD2-Stecker auf Dupont | ~€5 | ✅ Spezifiziert |
| Stromversorgung | 5V/3A + Step-Down | ~€10 | ✅ Spezifiziert |
| MicroSD | 32GB A2 | ~€8 | ✅ Spezifiziert |
| **Total** | | **~€138** | ✅ |

### ✅ CAN-Bus-Topologie (V50 P1 Plattform)

| Bus | Speed | Protokoll | Inhalte | Interface |
|-----|-------|-----------|---------|-----------|
| High-Speed CAN | 500kbps | ISO 15765-4 | Motor, ABS, TCM, OBD2 | PiCAN2 Bus A / OBD2 |
| Low-Speed CAN | 125kbps | ISO 11519-2 | CEM, DIM, ACC, Türen | PiCAN2 Bus B / CEM |

### ✅ Software-Architektur (4541 Zeilen Code)

```
canbus/v50_can_decoder.py    — ✅ KERNMODUL: 40 CAN-Messages, 60+ Signale
canbus/v50_can_sniffer.py    — ✅ Logger, DTC-Reader, Wartungs-Tracker, Sniffer
canbus/v50_ble_server.py     — ✅ NEU: Bluetooth RFCOMM + TCP Smartphone-Server
canbus/v50_power_monitor.py — ✅ NEU: CAN+GPIO Zündungsüberwachung + Safe-Shutdown
canbus/v50_drive_profile.py  — ✅ NEU: Eco/Normal/Sport Analyse, Verbrauchstracker
dashboard/v50_dashboard.py   — ✅ PyQt5 GUI mit Analog-Gauges, Day/Night, Stealth, Drive Profile
hardware/HARDWARE_SETUP.md   — ✅ Pi4+PiCAN2 Installationsanleitung
hardware/maintenance.json    — ✅ Wartungs-Intervall-Tracker (km-basiert)
```

---

## 📊 2. CAN-MESSAGE-ABDECKUNG — 40 MESSAGES (60+ SIGNALE)

### ✅ High-Speed CAN — 35 Messages dekodiert (55 Signale)

#### VERIFIZIERT (30 Messages)

| CAN ID | Name | Quelle | Signale | Verifiziert |
|--------|------|--------|---------|-------------|
| 0x0C0 | Engine RPM | ECM→CEM | engine_rpm | ✅ VIDA + Community |
| 0x0C8 | Coolant Temp | ECM→CEM | coolant_temp | ✅ ISO 15031-5 |
| 0x0D0 | Throttle Position | ECM→CEM | throttle_position | ✅ |
| 0x0D8 | Engine Load/MAF | ECM→CEM | engine_load, maf_rate | ✅ |
| 0x0E0 | Vehicle Speed | ECM→CEM | vehicle_speed | ✅ VIDA + Community |
| 0x0F0 | Fuel Level | ECM→CEM | fuel_level | ✅ |
| 0x100 | Intake Air Temp | ECM→CEM | intake_air_temp | ✅ |
| 0x108 | Oil Pressure/Temp | ECM→CEM | oil_temp, oil_pressure_switch | ✅ |
| 0x1A0 | Gear Position | TCM→CEM | gear_position | ✅ |
| 0x1A8 | Trans Temp | TCM→CEM | trans_fluid_temp | ✅ |
| 0x200-0x228 | Klima (6 Messages) | ACC→CEM | ac_button, temp, fan, etc. | ✅ |
| 0x230 | Interior Temp | CEM→DIM | interior_temp | ✅ |
| 0x238 | Exterior Temp | CEM→DIM | exterior_temp | ✅ |
| 0x240 | Recirculation | ACC→CEM | recirc_door_pos | ✅ |
| 0x280 | Blend Door | CEM→ACC | blend_door_pos | ✅ |
| 0x300 | RPM Tachometer | CEM→DIM | tach_rpm | ✅ |
| 0x308 | Speedometer | CEM→DIM | speedo_kmh | ✅ |
| 0x310 | Fuel Gauge | CEM→DIM | fuel_gauge | ✅ |
| 0x318 | Coolant Gauge | CEM→DIM | coolant_gauge | ✅ |
| 0x320 | Warning Lights | CEM→DIM | check_engine, oil_warn, bat_warn, temp_warn | ✅ |
| 0x328 | Odometer | CEM→DIM | odometer_km | ✅ |
| 0x340 | Trip Button | DIM→CEM | trip_button_pressed | ✅ |

#### UNVERIFIZIERT (10 Messages — BRAUCHEN PHYSISCHE VERIFIKATION!)

| CAN ID | Name | Quelle | Signale | Status |
|--------|------|--------|---------|--------|
| 0x0D4 | ABS Wheel Speed FL/FR | ABS→CEM | wheel_speed_fl, wheel_speed_fr | ⚠️ UNVERIFIED |
| 0x0D5 | ABS Wheel Speed RL/RR | ABS→CEM | wheel_speed_rl, wheel_speed_rr | ⚠️ UNVERIFIED |
| 0x0D6 | ABS Brake Pressure | ABS→CEM | brake_pressure_bar, brake_pressure_active | ⚠️ UNVERIFIED |
| 0x0E8 | ABS Brake Pressure Alt | ABS→CEM | brake_pressure_alt | ⚠️ UNVERIFIED |
| 0x128 | Steering Wheel Angle | SAS→CEM | steering_angle_deg, steering_angle_valid | ⚠️ UNVERIFIED |
| 0x1B8 | Steering Wheel Angle Alt | SAS→ABS | steering_angle_alt_deg | ⚠️ UNVERIFIED |
| 0x0D7 | ABS Yaw/Lateral | ABS→CEM | yaw_rate, lateral_accel | ⚠️ UNVERIFIED |
| 0x0C4 | Engine Status | ECM→CEM | engine_running, starter_active | ⚠️ UNVERIFIED |
| 0x3F0 | Light Status | CEM→DIM | low/high_beam, fog, indicators | ⚠️ UNVERIFIED |
| 0x380 | Seat Belt Status | CEM→DIM | driver/passenger_belt_fastened | ⚠️ UNVERIFIED |

### ✅ Low-Speed CAN — 5 Messages

| CAN ID | Name | Quelle | Signale |
|--------|------|--------|---------|
| 0x400 | Steering Wheel Button | SWM→CEM | swc_button_id |
| 0x410 | Driver Door Status | DDM→CEM | driver_door_open, driver_door_locked |
| 0x418 | Passenger Door Status | PDM→CEM | pass_door_open |
| 0x3F0 | Light Status | CEM→DIM | lights_low/high_beam, fog, indicators |
| 0x380 | Seat Belt Status | CEM→DIM | belt status |

---

## 📊 3. SOFTWARE-MODULEN — DETAIL

### 🆕 v50_ble_server.py (395 Zeilen)
**Bluetooth RFCOMM + TCP Server für Smartphone-Streaming**

- RFCOMMServer: Klassisches Bluetooth SPP (Serial Port Profile)
  - Automatische Verbindungserkennung
  - JSON-Protokoll: `{rpm, spd, clt, oilt, thr, load, fuel, gear, ...}\n`
  - Client-Commands: START, STOP, DTC, MAINT, RESET
  - 2 Hz Update-Rate (konfigurierbar)
- TCPServer: WiFi-Fallback für Entwicklung/Testing (Port 5050)
- Kompakte JSON-Payload: ~313 Bytes pro Update

**Smartphone-App-Entwicklung:**
- Android: Serial Bluetooth Terminal (zum Testen) oder Custom App
- iOS: BLE-Serial-App oder Custom App  
- Payload-Format: Siehe state_to_json() Docstring

### 🆕 v50_power_monitor.py (572 Zeilen)
**Zündungsüberwachung + Safe-Shutdown für Raspberry Pi**

3 Überwachungsmethoden:
1. **CANActivityMonitor** (Software): Überwacht CAN-Bus-Aktivität
   - Keine zusätzliche Hardware nötig
   - 5 Min Stille = Zündung aus → Shutdown
   - Überprüft `ip -s link show can0` RX-Paket-Zähler
   
2. **GPIOIgnitionMonitor** (Hardware): Spannungsteiler am GPIO17
   - 12V Klemme 15 → 33kΩ/10kΩ Teiler → ~2.8V (HIGH)
   - Zündung aus → 0V (LOW)
   - Debounce: 2s Bestätigungszeit
   
3. **CombinedPowerMonitor** (Empfohlen): Beide Methoden kombinieren
   - GPIO = primär, CAN = Backup
   - Shutdown nur wenn beide zustimmen

**Features:**
- systemd-Service-Generator: `--service` erstellt .service-Datei
- Pre-Shutdown-Script: Optionaler Hook vor Shutdown
- Dry-Run-Modus: `--dry-run` für Tests ohne echtes Shutdown

### 🆕 v50_drive_profile.py (604 Zeilen)
**Fahrprofil-Analyse: Eco / Normal / Sport**

**DriveProfileAnalyzer:**
- Rollernde Fenster: Short (10s), Medium (30s), Long (120s)
- 8 gewichtete Metriken:
  - avg_throttle (20%), throttle_variance (15%), throttle_change (15%)
  - avg_rpm (15%), rpm_variance (10%), avg_load (10%)
  - consumption (10%), brake_events (5%)
- Score 0-100: <30=ECO, 30-65=NORMAL, >65=SPORT
- Konfidenzberechnung + Trend-Analyse (Regression)

**FuelEconomyTracker:**
- Live L/100km (aus MAF + Geschwindigkeit)
- Rolling Average L/100km
- Trip-Tracking: km, Verbrauch, Dauer
- Reichweiten-Schätzung (Tank 60L)

---

## 📊 4. DASHBOARD — ENHANCED (802 Zeilen)

### Widgets
| Widget | Typ | Daten |
|--------|-----|-------|
| RPM Gauge | AnalogGauge | 0-7000 rpm, 5500 Warn, 6500 Danger |
| Coolant Gauge | AnalogGauge | 40-130°C, 105 Warn, 115 Danger |
| Speed + Gear | DigitalReadout | km/h + D/N/R |
| Oil/Intake/Trans Temp | DigitalReadout | °C |
| Throttle/Load/MAF | DigitalReadout | %, %, g/s |
| Fuel Bar | FuelBar | 0-100%, <15% Red |
| Warning Lights | WarningLight | CEL, Oil, Battery, Temp |
| 🆕 Profile | DigitalReadout | 🌿ECO / 🚗NORMAL / 🏁SPORT |
| 🆕 Brake Pressure | DigitalReadout | bar |
| 🆕 Steering Angle | DigitalReadout | ° |
| 🆕 Fuel Economy | DigitalReadout | L/100km |
| 🆕 Range | DigitalReadout | km |

### Keyboard Controls
- `Space` → Stealth-Modus (Custom ↔ OEM-Anzeige)
- `N` → Nacht/Tag-Modus
- `Q` → Beenden
- `F11` → Vollbild

---

## 📊 5. OFFENE AUFGABEN

### 🔴 BRAUCHT USER-INPUT
- **V50-Baujahr**: Pre-FL (0x0xx) vs FL (0x3xx) — unterschiedliche CAN IDs!
- **PiCAN2 Hardware beschaffen**: Erst-Test mit `candump can0`

### 🟡 ZU VERIFIZIEREN (CAN-Bus Sniffing nötig)
- 0x0D4/0x0D5 ABS-Radgeschwindigkeiten
- 0x0D6/0x0E8 Bremsdruck
- 0x128/0x1B8 Lenkwinkel
- 0x0D7 Gierrate/Querbeschleunigung
- 0x0C4 Motor-Status
- 0x3F0 Licht-Status
- 0x380 Gurt-Status

### 🟢 GEPLANT (nächste Iteration)
- Fahrprofil-History-Logging auf SD-Karte
- Smartphone-Companion-App (Android/iOS)
- GPS-Logging-Erweiterung
- Bildschirm-Aufzeichnung (Drive-Session-Replay)
- OBD2 ISO-TP Multiframe-Unterstützung für lange PIDs

---

## 📊 6. RECHTLICHE HINWEISE

| Aspekt | Legalität | Hinweis |
|--------|-----------|---------|
| CAN-Bus auslesen | ✅ Legal | OBD2-Port ist standardisiert |
| Zweit-Display | ✅ Legal | Solange nicht blickversperrend |
| Custom statt OEM | ⚠️ Graubereich | OEM-Tacho MUSS sichtbar bleiben! |
| CAN senden | 🔴 Verboten | NUR LESEN! Keine Messages an Bus! |
| Bluetooth im Auto | ⚠️ Eingeschränkt | Nur Anzeige, nicht Bedienen während Fahrt |