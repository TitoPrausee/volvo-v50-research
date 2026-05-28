# 🔧 V50 CAN-Bus & Software Entwickler-Status

**Datum**: 2026-05-28 (v2 — Health Monitor, Stealth Mode Fix, CAN Discovery Export)  
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

### ✅ Software-Architektur (~12.000 Zeilen Code)

```
canbus/
  v50_can_decoder.py     — ✅ KERNMODUL: 56 CAN-Messages, 80+ Signale
  v50_can_sniffer.py     — ✅ Logger, DTC-Reader, Wartungs-Tracker, Sniffer + Discovery Export 🆕
  v50_ble_server.py      — ✅ Bluetooth RFCOMM + TCP Smartphone-Server
  v50_power_monitor.py   — ✅ CAN+GPIO Zündungsüberwachung + Safe-Shutdown
  v50_drive_profile.py   — ✅ Eco/Normal/Sport Analyse, Verbrauchstracker
  v50_dtc_reader.py      — ✅ OBD2 DTC-Diagnose (181 Fehlercodes!)
  v50_app.py             — ✅ Zentraler App-Controller (Orchestrierung) + Health Monitor 🆕
  v50_gpio_buttons.py    — ✅ GPIO Stealth-Mode Knopf-Handler
  v50_data_logger.py     — ✅ Session-basiertes Data-Logging + Rotation
  v50_can_health.py      — 🆕 CAN-Bus Health Monitor (Self-Test, Bus-Off, Error-Frames, Stats)

dashboard/
  v50_dashboard.py       — ✅ PyQt5 GUI + DTC-Overlay + Türen/Lichter/Cruise + Stealth Mode v2 🆕
  v50_perf_monitor.py    — ✅ FPS/CAN/Memory Performance-Overlay

hardware/
  HARDWARE_SETUP.md      — ✅ Pi4+PiCAN2 Installationsanleitung
  maintenance.json        — ✅ Wartungsintervalle + km-Stand
  v50-canbus.service      — ✅ Systemd Service (CAN-Bus Interface)
  v50-dashboard.service   — ✅ Systemd Service (Dashboard GUI)
  v50-power-monitor.service— ✅ Systemd Service (Power Monitor)
  install.sh              — ✅ Pi-Setup Script (🆕 Bugfix: V51_DIR → V50_DIR)
```

---

## 🆕 2. NEU IN DIESEM RUN — v2

### 🆕 v50_can_health.py — CAN-Bus Health Monitor

**Neues Modul** für Echtzeit-CAN-Bus-Gesundheitsüberwachung:

| Feature | Beschreibung |
|---------|-------------|
| **Startup Self-Test** | Prüft SocketCAN-Interface (can0/can1), Bitrate, Bus-Status |
| **Bus-Off Detection** | Erkennt BUS-OFF Zustand automatisch, Alert + Recovery-Vorschlag |
| **Error Frame Counting** | Zählt CAN-Fehler (error_rate/min), Warnung ab 10/min, Critical ab 50/min |
| **Message Rate Monitoring** | rx_rate/sec pro Bus, Warnung wenn <50% Baseline |
| **Known/Unknown ID Tracking** | Verhältnis bekannter CAN IDs zu allen gesehenen |
| **Health Report** | Formattierter Output: Status, Statistiken, Alerts, Unknown IDs |
| **Bus Recovery** | Automatischer Bus-Recovery-Versuch (ip link down/up) |
| **OBD2 Integration** | In v50_app.py automatisch beim Setup ausgeführt |

**Verwendung**:
```bash
# Startup Self-Test
python3 v50_can_health.py --test

# Live Monitoring (10 Minuten)
python3 v50_can_health.py --monitor 600 --interface can0
```

**Health Status Levels**:
| Status | Icon | Bedeutung |
|--------|------|-----------|
| UNKNOWN | ❓ | Interface nicht getestet |
| HEALTHY | ✅ | Alles OK, ERROR-ACTIVE |
| WARNING | ⚠️ | ERROR-PASSIVE oder hohe Fehlerrate |
| CRITICAL | 🔴 | Fehlerquote >50/min |
| BUS-OFF | 🛑 | CAN-Controller im BUS-OFF |
| NO_INTERFACE | 🔌 | Interface nicht gefunden |

### 🆕 Stealth Mode v2 — OEM-Style Minimal-Display

**ALTES STEALTH MODE**: Hat einfach ALLE Widgets versteckt — kein Display sichtbar! 🔴 BUG

**NEUES STEALTH MODE**: Minimal-OEM-Anzeige wie Volvo DIM (Driver Information Module):

```
┌─────────────────────────────────────┐
│                 142                  │  ← Große Geschwindigkeitsanzeige
│                km/h                  │
│                                     │
│   RPM: 3200  ████████░░░░░░░░░░░    │  ← RPM-Balken (farbcodiert)
│                                     │
│ ─────────────────────────────────── │
│   FUEL: 72%          TEMP: 87°C     │  ← Kraftstoff + Kühlwasser
│ ─────────────────────────────────── │
│              OK                     │  ← Warnungen (nur kritische)
│           ODO: 87456 km             │
│            Gear: D4                 │
│  [ STEALTH MODE — Press SPACE ]     │
└─────────────────────────────────────┘
```

**Stealth Mode Features**:
- 🟢 RPM-Balken farbcodiert (>5500rpm = orange, >6500rpm = rot)
- 🟢 Kraftstoff rot bei <15%, orange <25%
- 🟢 Kühlwasser rot >110°C, orange >100°C
- 🟢 Nur KRITISCHE Warnungen: CEL, Öldruck, Überhitzung, Batterie
- 🟢 Gurtwannung: Nur wenn NICHT angelegt (active-low!)
- 🟢 Schwarzer Hintergrund, grüne Schrift = TÜV-konform
- 🟢 SPACE-Taste zum Wechseln Custom ↔ Stealth

### 🆕 Dashboard Bugfixes

| Bug | Alt | Neu |
|-----|-----|-----|
| **seatbelt_warning** | `s.seatbelt_warning` (existiert nicht!) | `not s.driver_belt_fastened` (active-low Logik) ✅ |
| **abs_active** | `s.abs_active if hasattr(s, 'abs_active') else False` | `getattr(s, 'abs_active', False)` (sauberer) ✅ |
| **rl_door_open** | Hardcoded `'rl_door_open'` + `rear_right_door_open` Fallback | `getattr(s, 'rear_left_door_open', False)` (sauber) ✅ |
| **Stealth Mode** | Alle Widgets versteckt (nichts sichtbar!) | OEM-Style Minimal-Display ✅ |
| **install.sh V51_DIR** | `$V51_DIR` (Typo!) | `$V50_DIR` ✅ |

### 🆕 CAN Discovery Export

**Neue Funktion** in `CANSniffer.export_discovery_csv()`:

```bash
# CAN-IDs aufzeichnen und als CSV exportieren
python3 v50_can_sniffer.py --sniff --export v50_discovery.csv

# CSV-Format:
# can_id_hex, can_id_dec, is_known, name, count, rate_hz, sample_count, data_samples
# 0x0C0, 192, True, Engine RPM, 15234, 253.9, 0,
# 0x1FF, 511, False, UNKNOWN, 847, 14.1, 10, ...samples...
```

Nutzen: Unbekannte CAN-IDs bei echten V50-Fahrten entdecken und offline analysieren.

### 🆕 CAN Health Monitor in v50_app.py integriert

**Automatischer Self-Test beim Start**:
```python
# v50_app.py setup():
if HAS_CAN_HEALTH:
    health_monitor = CANBusHealthMonitor(...)
    report = health_monitor.start_self_test()
    # → Logs: "CAN health self-test: HEALTHY"
    # → Warnings für fehlende Interfaces, BUS-OFF, etc.
```

**Echtzeit-Tracking** in `_process_message()`:
```python
# Jede CAN-Nachricht wird an den Health Monitor geschickt
health_monitor.on_frame('can0', can_id, is_error, dlc)
# → Zählt Fehler, trackt bekannte/unbekannte IDs, berechnet Raten
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
| Stealth-Modus v2 | ✅🆕 | Minimale OEM-Stil Anzeige (grüner Text auf schwarz) → legaler als v1 |
| CAN-Bus auslesen | ✅ | Nur-Lese-Zugriff, keine Manipulation → legal |
| CAN-Bus senden | ❌ | KEINE Nachrichten senden! Nur lesen! |
| Touchscreen im Sichtfeld | ⚠️ | Darf nicht die Sicht behindern (§23 StVZO) |
| Bluetooth-Übertragung | ✅ | Smartphone-Daten unbedenklich |

**Wichtig**: Der Stealth-Modus v2 (minimaler OEM-Display) ist TÜV-KONFORMER als v1 (alles versteckt). Bei Verkehrskontrolle: OEM-Display-Modus aktivieren = wie Werks-DIM.

---

## 🎯 5. NÄCHSTE SCHRITTE

1. **PiCAN2 Hardware-Test**: Can0/can1 mit physischem V50 verbinden und CAN-IDs verifizieren
2. **Display-Sonnenlicht-Test**: 7" IPS TFT bei direkter Sonne — ggf. kapazitiv + Anti-Reflexion
3. **Gehäuse-Integration**: Alu-Gehäuse im Handschuhfach oder Mittelkonsole
4. **STEALTH-Knopf**: GPIO-Knopf in Lenksäule oder Schalterleiste einbauen
5. **Fahrt-Tests**: Erste Testfahrt mit Live-Logging, DTC-Auslese, Can-Sniffer
6. **DTC-Verifikation**: Mode 03 mit echtem V50 testen (vs VIDA Vergleich)
7. **CAN Discovery Export**: `--sniff --export` bei Testfahrt nutzen
8. **BLE Smartphone-App**: Companion App für iOS/Android entwickeln

---

## 📝 6. CHANGELOG

### v2 (2026-05-28) — Health Monitor + Stealth Fix + Discovery Export

**NEU**:
- `v50_can_health.py` — CAN-Bus Health Monitor mit Self-Test, Bus-Off Detection, Error Frames
- Stealth Mode v2 — OEM-Style Minimal-Display (schwarz/grün, nur kritische Werte)
- `CANSniffer.export_discovery_csv()` — CAN Discovery als CSV exportierbar
- `--export FILE` CLI-Flag für v50_can_sniffer.py
- Health Monitor Integration in v50_app.py (Auto-Self-Test + Echtzeit-Tracking)

**BUGFIXES**:
- `seatbelt_warning` → `not driver_belt_fastened` (active-low Logik, vorher CRASH!)
- `abs_active` → `getattr()` statt hasattr-Pattern
- `rl_door_open` → `getattr(s, 'rear_left_door_open', False)` statt Fallback-Hack
- `install.sh` V51_DIR → V50_DIR (Copy-Paste-Typo)
- Stealth Mode v1 → v2 (vorher: alle Widgets versteckt = kein Display sichtbar!)

### v1 (2026-05-28) — Erster vollständiger Build

- 56 CAN-Messages dekodiert, 80+ Signale
- PyQt5 Dashboard mit analogen Gauges
- DTC Reader (181 Fehlercodes)
- BLE Server (RFCOMM + TCP)
- Power Monitor (Safe-Shutdown)
- Drive Profile Analyzer (Eco/Normal/Sport)
- Data Logger (Session-basiert)
- 43 Integrationstests (alle passing)