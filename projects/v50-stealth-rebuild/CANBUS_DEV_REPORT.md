# 🔧 V50 CAN-Bus & Software Entwickler-Status

**Datum**: 2026-05-28  
**Rolle**: CAN-Bus & Software-Entwickler (v50-developer)  
**Budget**: ~€90 (Pi4 + PiCAN2 Duo) + ~€50 (Display) = **~€140 Total**

---

## 📊 1. CAN-BUS INFRASTRUKTUR — ERLEDIGT

### ✅ Hardware-Spezifikation (festgelegt)

| Komponente | Modell | Preis | Status |
|-----------|--------|-------|--------|
| Raspberry Pi | Pi 4 Model B 2GB | ~€35 | ✅ In DB |
| CAN HAT | PiCAN2 Duo (2-Kanal) | ~€25 | ✅ In DB |
| Display | 7" IPS TFT 1024x600 | ~€40 | ✅ In DB |
| Gehäuse | Alu-Gehäuse Pi4 | ~€15 | ✅ Spezifiziert |
| OBD2-Adapter | OBD2-Stecker auf Dupont | ~€5 | ✅ Spezifiziert |
| Stromversorgung | 5V/3A + Step-Down | ~€10 | ✅ Spezifiziert |
| PiZ-Up USV HAT | USV + Safe-Shutdown | ~€30 | 🆕 EMPFOHLEN |
| MicroSD | 32GB A2 | ~€8 | ✅ Spezifiziert |
| **Total** | | **~€168** | Mit PiZ-Up, ohne Display ~€128 |

### ✅ CAN-Bus-Topologie (V50 P1 Plattform)

| Bus | Speed | Protokoll | Inhalte | Interface |
|-----|-------|-----------|---------|-----------|
| High-Speed CAN | 500kbps | ISO 15765-4 | Motor, ABS, TCM, OBD2 | PiCAN2 Bus A / OBD2 |
| Low-Speed CAN | 125kbps | ISO 11519-2 | CEM, DIM, ACC, Türen | PiCAN2 Bus B / CEM |

### ✅ Software-Architektur (~8500 Zeilen Code)

```
canbus/
  v50_can_decoder.py     — ✅ KERNMODUL: 56 CAN-Messages, 80+ Signale
  v50_can_sniffer.py     — ✅ Logger, DTC-Reader, Wartungs-Tracker, Sniffer
  v50_ble_server.py      — ✅ Bluetooth RFCOMM + TCP Smartphone-Server
  v50_power_monitor.py   — ✅ CAN+GPIO Zündungsüberwachung + Safe-Shutdown
  v50_drive_profile.py   — ✅ Eco/Normal/Sport Analyse, Verbrauchstracker
  v50_dtc_reader.py      — ✅ OBD2 DTC-Diagnose (181 Fehlercodes!)
  v50_app.py             — ✅ Zentraler App-Controller (Orchestrierung)
  v50_gpio_buttons.py    — ✅ NEU: GPIO Stealth-Mode Knopf-Handler
  v50_data_logger.py     — ✅ NEU: Session-basiertes Data-Logging + Rotation
  test_can_integration.py— ✅ NEU: 43 Integrationstests (alle passing)

dashboard/
  v50_dashboard.py       — ✅ PyQt5 GUI + DTC-Overlay + Türen/Lichter/Cruise
  v50_perf_monitor.py    — ✅ NEU: FPS/CAN/Memory Performance-Overlay

hardware/
  HARDWARE_SETUP.md      — ✅ Pi4+PiCAN2 Installationsanleitung
  maintenance.json        — ✅ Wartungsintervalle + km-Stand
  v50-canbus.service      — ✅ NEU: Systemd Service (CAN-Bus Interface)
  v50-dashboard.service   — ✅ NEU: Systemd Service (Dashboard GUI)
  v50-power-monitor.service— ✅ NEU: Systemd Service (Power Monitor)
  install.sh             — ✅ NEU: Pi-Setup Script (Automatische Installation)
```

---

## 🆕 2. NEU IN DIESEM RUN: Tests + Hardware-Services + Performance

### ✅ test_can_integration.py — 43 Integrationstests

**Vollständige Test-Abdeckung** für alle CAN-Decoder-Funktionen:

| Test-Klasse | Tests | Beschreibung |
|-------------|-------|-------------|
| TestCANMessageDefinitions | 7 | DB-Konsistenz, Alle IDs, Bus-Zuweisung |
| TestSignalExtraction | 11 | RPM, Speed, Temp, Fuel, Gear, Throttle, MAF, Warnings, Doors |
| TestV50StateTracking | 7 | State-Updates, Staleness, Climate, Doors, Summary |
| TestGearMapping | 2 | Gear-Namen, Unknown-Gear |
| TestFuelConsumption | 2 | Idle-Verbrauch, Highway-Verbrauch |
| TestDriveProfile | 2 | Import, Eco-Klassifikation |
| TestDTCReader | 2 | Import, DTC-Formatierung |
| TestOBD2PIDs | 2 | Standard PIDs, Volvo Proprietär |
| TestCANBusSimulation | 3 | Highway, Stadt, Warnleuchten |
| TestMessageIntegrity | 4 | Eindeutige IDs, Signal-Ranges, DLC, Boolean-Flags |
| TestListMessages | 1 | Utility-Ausgabe |
| **Total** | **43** | **Alle bestanden ✅** |

**Ausführen**:
```bash
python3 -m pytest canbus/test_can_integration.py -v
```

### ✅ v50_gpio_buttons.py — Stealth-Mode Knopf-Handler

**5 GPIO-Knöpfe** für das 7" TFT Dashboard:

| GPIO | Knopf | Funktion |
|------|-------|----------|
| GPIO17 | Stealth Toggle | Custom ↔ OEM Display wechseln |
| GPIO27 | Page Switch | Dashboard-Seite wechseln |
| GPIO22 | Brightness Up | Helligkeit erhöhen |
| GPIO23 | Brightness Down | Helligkeit verringern |
| GPIO5 | Emergency | 5s halten = Pi Shutdown |

**Features**:
- Hardware-Debounce: 200ms (RPi.GPIO bouncetime)
- Software-Debounce: Long-Press-Erkennung (2s) und Emergency (5s)
- Stealth-Modi: CUSTOM → STEALTH → OFF → CUSTOM
- Helligkeit: 10 Stufen (10%-100%), Default 50%
- Event-Callbacks für Dashboard-Integration
- Simulierter Modus für Entwicklung ohne Pi-Hardware

### ✅ v50_data_logger.py — Session-basiertes Data-Logging

**Automatische Session-Verwaltung** für CAN-Bus-Aufzeichnung:

| Feature | Beschreibung |
|---------|-------------|
| Session-Tracking | Auto-Start bei Zündung, Auto-Stop bei Zündung aus |
| Rotation | CSV max 100MB, automatische Rotation + Gzip-Kompression |
| Statistiken | Avg/Max Speed, RPM, Temp, Distanz, Verbrauch pro Session |
| Space-Management | Max 2GB Logs, älteste Sessions automatisch gelöscht |
| Alters-Limit | Sessions älter als 90 Tage automatisch gelöscht |
| Format | CSV: timestamp, can_id, dlc, data_hex, decoded |
| Metadata | session.json pro Session mit Statistiken |

**Verwendung**:
```bash
# Live-Logging starten (über v50_app.py --log <dir>)
python3 v50_app.py --log /var/log/v50/sessions

# Session-Liste anzeigen
python3 v50_data_logger.py --list

# Disk-Usage anzeigen
python3 v50_data_logger.py --disk-usage

# Simulation testen
python3 v50_data_logger.py --simulate
```

### ✅ v50_perf_monitor.py — Performance-Overlay

** Echtzeit-Performance-Monitoring** für das Dashboard:

| Metrik | Target | Methode |
|--------|--------|---------|
| FPS | ≥20 FPS | Frame-Zeit-Tracking (60-Fenster) |
| CAN Throughput | 5000+ f/s | Timestamp-basierte Zählung |
| Decoder-Rate | <0.1ms/frame | Decode-Zeit-Profilierung |
| Known CAN IDs | ≥70% | Bekannt/Unbekannt-Verhältnis |
| CPU | <30% /proc/stat | System-CPU |
| Memory | <128MB /proc/self/status | RSS Memory |
| CPU Temp | <70°C /sys/class/thermal | Pi-Thermistor |

**Compact Overlay** (1 Zeile, Dashboard oben links):
```
FPS:27 CAN:540 CPU:2% MEM:13MB T:48°C
```

**PyQt5-Integration**: `PerformanceMonitor` + `create_perf_overlay()` Widget

### ✅ Systemd Services + Install Script

**3 Services** für Pi-Autostart:

| Service | Startup | Beschreibung |
|---------|---------|-------------|
| v50-power-monitor.service | Boot | GPIO+CAN Zündungsüberwachung |
| v50-canbus.service | Nach Power-Monitor | CAN-Decoder + App-Controller |
| v50-dashboard.service | Nach CAN-Bus | PyQt5 Dashboard auf 7" TFT |

**Install-Script** (`hardware/install.sh`):
- PiCAN2 Duo Overlay-Konfiguration (MCP2515 SPI)
- SocketCAN Setup (can0=500kbps, can1=125kbps)
- Python-Dependencies (python-can, PyQt5, can-utils)
- Service-Installation und Auto-Enable
- Projekt kopieren nach `/opt/v50/`

**Installation auf Pi**:
```bash
sudo bash hardware/install.sh
sudo reboot
# Nach Reboot:
ip -details link show can0   # CAN Interface prüfen
sudo systemctl start v50-dashboard  # Dashboard starten
journalctl -u v50-canbus -f          # Logs anzeigen
```

---

## 📊 3. DATENBANK-STAND

- **160 CAN Messages** in DB (2.4i, T5, D5 Varianten)
- **218 CAN Signals** mit Faktoren, Offsets, Einheiten
- **47 OBD2 PIDs** (Standard + Volvo-proprietär)
- **663 Teile** in der Teile-Datenbank

---

## 🔧 4. LEGALITÄT — Custom Dashboard in DE

| Aspekt | Status | Hinweis |
|--------|--------|---------|
| Custom-Dashboard | ⚠️ Eingeschränkt | Zusätzliches Display erlaubt, aber OEM-Tacho MUSS sichtbar bleiben |
| Stealth-Modus (Umschaltung) | ✅ | Knopfdruck zeigt OEM-Anzeige statt Custom → legal |
| CAN-Bus auslesen | ✅ | Nur-Lese-Zugriff, keine Manipulation → legal |
| CAN-Bus senden | ❌ | KEINE Nachrichten senden! Nur lesen! |
| Touchscreen im Sichtfeld | ⚠️ | Darf nicht die Sicht behindern (§23 StVZO) |
| Bluetooth-Übertragung | ✅ | Smartphone-Daten unbedenklich |

**Wichtig**: Der Stealth-Modus (GPIO-Knopf wechselt Custom→OEM) ist DER Schlüssel für TÜV-Konformität. Bei Verkehrskontrolle oder TÜV: OEM-Anzeige zeigen.

---

## 🎯 5. NÄCHSTE SCHRITTE

1. **PiCAN2 Hardware-Test**: Can0/can1 mit physischem V50 verbinden und CAN-IDs verifizieren
2. **Display-Sonnenlicht-Test**: 7" IPS TFT bei direkter Sonne — ggf. kapazitiv + Anti-Reflexion
3. **Gehäuse-Integration**: Alu-Gehäuse im Handschuhfach oder Mittelkonsole
4. **STEALTH-Knopf**: GPIO-Knopf in Lenksäule oder Schalterleiste einbauen
5. **Fahrt-Tests**: Erste Testfahrt mit Live-Logging, DTC-Auslese, Can-Sniffer
6. **DTC-Verifikation**: Mode 03 mit echtem V50 testen (vs VIDA Vergleich)
7. **BLE Smartphone-App**: Companion App für iOS/Android entwickeln