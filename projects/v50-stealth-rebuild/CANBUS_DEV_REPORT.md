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

### ✅ Software-Architektur (~7000 Zeilen Code)

```
canbus/v50_can_decoder.py    — ✅ KERNMODUL: 56 CAN-Messages, 80+ Signale
canbus/v50_can_sniffer.py    — ✅ Logger, DTC-Reader, Wartungs-Tracker, Sniffer
canbus/v50_ble_server.py     — ✅ Bluetooth RFCOMM + TCP Smartphone-Server
canbus/v50_power_monitor.py  — ✅ CAN+GPIO Zündungsüberwachung + Safe-Shutdown
canbus/v50_drive_profile.py  — ✅ Eco/Normal/Sport Analyse, Verbrauchstracker
canbus/v50_dtc_reader.py    — ✅ NEU: OBD2 DTC-Diagnose (181 Fehlercodes!)
canbus/v50_app.py            — ✅ NEU: Zentraler App-Controller (Orchestrierung)
dashboard/v50_dashboard.py   — ✅ PyQt5 GUI + DTC-Overlay + Türen/Lichter/Cruise
hardware/HARDWARE_SETUP.md   — ✅ Pi4+PiCAN2 Installationsanleitung
hardware/maintenance.json    — ✅ Wartungsintervalle + km-Stand
```

---

## 🆕 2. NEU IN DIESEM RUN: DTC-DIagnose + App-Controller

### ✅ v50_dtc_reader.py — OBD2 Diagnose-Modul

**181 V50-spezifische Fehlercodes** in der Datenbank:

- **Powertrain P0xxx**: 60+ Codes (O2-Sensoren, Fehlzündungen, Kraftstoffsystem, etc.)
- **Volvo P1xxx**: 60+ Hersteller-Codes (VVT, Injektoren, CEM-Kommunikation, etc.)
- **Chassis C0xxx**: 25+ ABS/DSTC Codes (Radsensoren, Giertrate, Lenkwinkel)
- **Body Bxxxx**: 20+ Karosserie-Codes (SRS, CEM, DIM, Türmodule)
- **Network U0xxx**: 15+ CAN-Bus Kommunikationsfehler

**Funktionen**:
- Mode 03: Gespeicherte DTCs lesen
- Mode 04: DTCs löschen (mit Sicherheitsbestätigung)
- Mode 07: Ausstehende DTCs lesen
- Mode 09: VIN auslesen
- Mode 01: Live-Daten (RPM, Temp, Geschwindigkeit, etc.)
- Mode 22: Volvo-Proprietäre PIDs (Öltemperatur, ATF-Temp, etc.)
- Modul-spezifische Abfrage (ECM, TCM, ABS, CEM)

**Verwendung**:
```bash
# DTCs lesen
python3 v50_dtc_reader.py --dtc

# Live-Daten
python3 v50_dtc_reader.py --live

# VIN auslesen
python3 v50_dtc_reader.py --vin

# Wartungsstatus
python3 v50_dtc_reader.py --maint

# km-Stand aktualisieren
python3 v50_dtc_reader.py --maint-update 85000

# Service eintragen
python3 v50_dtc_reader.py --maint-service oil_change
```

### ✅ v50_app.py — Zentraler App-Controller

Verbindet alle Module zu einem Gesamtsystem:
- CAN-Bus Listener Loop (Haupt-Thread)
- V50State-Tracking (Alle 56 Messages, 80+ Signale)
- Drive Profile Analyse (Eco/Normal/Sport)
- Fuel Economy Tracker (L/100km Schätzung)
- Data Logger (SQLite + CSV, Rotation, 20Hz)
- BLE Server (Smartphone-Datenübertragung)
- Power Monitor (Sicheres Herunterfahren bei Zündung aus)
- DTC Reader (Fehlercodes lesen/löschen)

**Verwendung**:
```bash
# Komplettsystem (Pi im Auto)
python3 v50_app.py --full --ble

# Nur Daten-Logging
python3 v50_app.py --log --log-dir /mnt/usb/v50data

# Diagnose-Modus
python3 v50_app.py --diagnostics

# CAN-Sniffer
python3 v50_app.py --sniff
```

### ✅ v50_dtc_reader.py — Data Logger (SQLite + CSV)

- **SQLite-Datenbank** (`v50_can_log.db`): Strukturierte Queries, Session-Tracking
- **CSV-Export**: Automatische Rotation, 28 Spalten, 20Hz Sample-Rate
- **Rotation**: 50MB pro Datei, danach automatisch neue Session

---

## 📊 3. CAN-MESSAGE-ABDECKUNG

### ✅ Vollständig dekodiert (56 Messages, 80+ Signale)

| Kategorie | Messages | Signale | Status |
|-----------|----------|---------|--------|
| **Powertrain** (ECM→CEM) | 10 | 15 | ✅ RPM, Temp, Drosselklappe, Kraftstoff |
| **ABS/Dynamik** (ABS→CEM) | 6 | 12 | ✅ Radgeschw., Bremsdruck, Gierrate, Lenkwinkel |
| **Getriebe** (TCM→CEM) | 3 | 5 | ✅ Gang, Öltemp, Wandlerschlupf |
| **Dim/Dashboard** (CEM→DIM) | 8 | 10 | ✅ Tacho, Tank, Warnlampen, km-Stand |
| **Klima** (ACC→CEM) | 7 | 9 | ✅ Temp-Einstellung, Lüfter, A/K |
| **Komfort/Türen** (CEM→DIM) | 6 | 10 | ✅ Türstatus, Kofferraum, Gurt, Hupe |
| **Licht** (CEM/LSM→DIM) | 3 | 8 | ✅ Abblend, Fern, Nebel, Blinker |
| **Audio** (IAM↔CEM) | 2 | 3 | ✅ Quelle, Lautstärke |
| **Cruise** (CEM→SWM) | 1 | 2 | ✅ Aktiv, Geschw. |
| **Drive Profile** | — | — | ✅ Eco/Normal/Sport Klassifikation |
| **Facelift-Varianten** | 5 | 5 | ✅ RPM, Speed, Coolant (0x316/0x330/0x360) |
| **OBD2 PIDs** | 7+ | 7+ | ✅ Mode 01 Live-Daten |

### 🔬 Verifizierungsstatus

| Status | Count | Beschreibung |
|--------|-------|--------------|
| ✅ Verified | 32 | Über VIDA/Community bestätigt |
| 🔶 Community | 12 | Von Foren/DBC, physikalisch verifizieren |
| ❓ Unverified | 12 | Muss am V50 CAN-Bus gesnifft werden |

**EMPFEHLUNG**: Bei erster In-Fahrzeug-Test `-v` Flag nutzen um Unknown-Messages zu loggen. Mit `--sniff` Modus alle CAN-IDs aufzeichnen und mit Datenbank abgleichen.

---

## 🔧 4. TECHNISCHE ENTSCHEIDUNGEN

### ✅ Display-Wahl

| Display | Preis | Tageslicht | Touch | Kommentar |
|---------|-------|-----------|-------|-----------|
| 7" IPS TFT 1024x600 | ~€40 | 🔶 Ausreichend | Kapazitiv | Standard-Wahl |
| 5" HDMI IPS TFT 800x480 | ~€25 | 🔶 OK | Resistiv | Kleinere Alternative |
| 7" eInk Waveshare | ~€50 | ✅ Sehr gut | Nein | Gut lesbar, langsame Aktualisierung |
| 10.1" HDMI IPS 1280x800 | ~€65 | ✅ Gut | Kapazitiv | Größer, besser lesbar |

**EMPFEHLUNG**: 7" IPS TFT für Tageslicht + Stealth-Modus (OEM-Tacho bleibt sichtbar).

### ✅ Stromversorgung

| Option | Vorteil | Nachteil | Wahl |
|--------|---------|----------|------|
| Zigarettenanzünder | Einfach | Ohne Zündung kein Pi | ❌ |
| Festverkabelt + Step-Down | Dauerplus möglich | Batterie-Entladung | ⚠️ |
| Zündungsplus + Step-Down | Pi nur bei fahrendem Auto | Automatischer Start/Stop | ✅ |
| Zündungsplus + USV (PiZ Up) | Safe-Shutdown + Zeitpuffer | Zusätzlich ~€30 | 🏆 BESTE |

**EMPFEHLUNG**: PiZ Up UPS HAT (~€30) für sicheres Herunterfahren + Zeitpuffer. Kostet extra, aber verhindert SD-Karten-Korruption.

### ✅ Stealth-Modus Legalität (DE)

| Aspekt | Legal? | Kommentar |
|--------|--------|-----------|
| Zusätzliches Display im Auto | ✅ Ja | Solange OEM-Tacho nicht verdeckt |
| CAN-Bus Daten auslesen | ✅ Ja | OBD2-Port ist standardisiert |
| CAN-Bus Daten senden/schreiben | ⚠️ Vorsicht | Nur lesen! Keine Befehle an CAN |
| DTCs löschen | ⚠️ Vorsicht | Erlaubt, aber löscht auch Historie |
| Tageslicht-lesbares Display | ✅ Ja | IPS TFT reicht, eInk besser |
| Display verdeckt OEM-Tacho | ❌ Nein | TÜV-relevant — Sichtfreiheit! |

**WICHTIGSTE REGEL**: Das custom Dashboard darf **den OEM-Tacho NICHT verdecken**. Stealth-Modus = Knopfdruck blendet custom aus und OEM ist wieder voll sichtbar. Alternativ: Display im Handschuhfach oder Konsole platzieren.

---

## 📋 5. OFFENE AUFGABEN

### ✅ Dashboard-Enhancements (Dieser Run)

**v50_dashboard.py** wurde erweitert:

1. **Neue Warning-Lights**: Gurt-Warnung (🛟), ABS-Warnung (⚠️)
2. **Neue Readouts**: Türen (D/P/RL/RR OPEN/SHUT), Lichter (LOW/HI/FOG/TURN/OFF), Cruise Control (Speed/--)  
3. **DTC-Diagnose-Overlay** (Taste `D` drücken):
   - DTCs scannen via V50DTCReader
   - DTCs löschen (mit Bestätigung)
   - Maintenance-Tracker anzeigen
   - V50State Summary als Übersicht
4. **Tastatur-Kürzel**: Space=Stealth, N=Day/Night, D=Diagnostics, Q=Quit, F11=Fullscreen

### 🔄 Nächste Schritte

1. **PHYSISCHER TEST**: Pi4 + PiCAN2 im V50 anschließen, CAN-Bus sniffen
   - Alle 56 Decoder-Messages verifizieren
   - Unknown-IDs mit `-v` Flag aufzeichnen
   - Latenz messen (python-can auf Pi4)

2. **GEHÄUSE-ENTWURF**: Pi4 + PiCAN2 + Display im V50 unterbringen
   - Handschuhfach: Genug Platz? Kabel zum OBD2-Port?
   - Mittelkonsole: Diskreter, aber Kabelführung komplexer
   - 3D-Druck: Maße nachmessen!

3. **STEALTH-TOGGLE**: Hardware-Taste für Moduswechsel (Custom ↔ OEM)
   - GPIO-Taste am Pi4 -> Dashboard-Event
   - Alternativ: Lenkradtaste via CAN-Bus abfangen

4. **DISPLAY-TEST**: 7" IPS TFT bei Sonnenlicht testen
   - Falls nicht lesbar: eInk-Alternative evaluieren
   - Auto-Dimming über BH1750 Lichtsensor

5. **STROMVERSORGUNG**: PiZ Up USV HAT bestellen (~€30)
   - Sicheres Herunterfahren (30s Puffer)
   - Watchdog für Automatischen Neustart

### 🔬 Forschung erforderlich

- V50 P1 Facelift vs. Pre-Facelift CAN-IDs (0x316 vs 0x0C0 für RPM)
- DSTC-Module: Gierratensensor nur bei DSTC-Ausstattung?
- B5244S Motor: Ist Öltemperatur-Signal auf CAN oder nur Schalter?
- CEM-Gateway: Wie Low-Speed CAN Messages decodieren? Brauchen wir Bus B?
