# 🚗 Volvo V50 2.4i — Team Requests

## Aktuelle Team-Mitglieder

| Agent | Rolle | Intervall | Fokus |
|-------|------|-----------|-------|
| `v50-chief` | Projektleitung | 8h | Budget, Kompatibilität, TÜV-Konformität |
| `v50-suspension` | Fahrwerk | 8h | Federn, Dämpfer, Stabis, Bremsen |
| `v50-exterior` | Optik & Detail | 12h | Lack, Scheinwerfer, Rücklichter, Grill |
| `v50-engine` | Motor sanft | 12h | Intake, Auspuff (E-Nummer!), Zahnriemen |
| `v50-interior` | Innenraum | 12h | Lederpflege, Schaltknauf, Pedale, Detail |
| `v50-budget` | Preise & Legalität | 6h | Günstigste Quellen, TÜV-Eintragungen |
| `v50-developer` | CAN-Bus & Software | 8h | Digitaler Tacho, Fahrdynamik-Displays |

+ 3 generische Forschungs-Agenten (vehicle-research, -community, -specs)

## Stealth-Regeln für ALLE Agenten
1. **100% legal** — jede Änderung muss TÜV-konform oder eintragbar sein
2. **Dezent** — man soll es fühlen, nicht sehen. Werksmäßig, aber frisch
3. **17" bleiben** — keine Felgen-Änderung
4. **LED schon verbaut** — Fern+Abblend, Rücklichter optional falls OEM-quality
5. **Kein Ricer** — kein Spoiler, keine Schürzen, kein Chip über 170PS

## 📊 Budget-Stand 2026-05-28

**GESAMT (mit Auspuff): €2.459-3.951 — ✅ INNERHALB €3.500-5.000 HARD CAP**

Siehe CHIEF_STATUS.md für vollständige Budget-Analyse.

## Offene Team-Anfragen

### ✅ GELÖST (seit letztem Update)
- **TÜV-Experte**: Vollständig dokumentiert in BUDGET_TUV_REPORT.md
- **Lackier-Experte**: DIY Polierung = €30-50, spart €250-550
- **Stabi-Experte**: Lemförder + SuperPro Poly in DB
- **Polestar für B5244S**: SKIP bestätigt — nur für T5, nicht STEALTH

### 🔄 OFFENE ANFRAGEN

#### 👔 Chef → v50-exterior
- **Facelift-Scheinwerfer Teilenummern VERIFIZIEREN**: 30796020-23 muss bestätigt werden
  - Pre-FL (2004-2007) → FL (2008-2012) Umbau: H7 Halogen, NICHT Xenon!
  - Braucht: Obere+untere Grill-Einfassung wenn Pre-FL→FL

#### 👔 Chef → v50-exterior
- **Grill Pre-FL vs FL Kompatibilität**: 
  - Wenn Pre-FL V50: obere+untere Einfassung tauschen für FL-Grill
  - OEM 30782612 = schwarzer Grill, aber welches Baujahr?

#### 💻 Developer → Chef/User
- **V50-Baujahr-Identifikation**: 
  - CRITICAL für CAN-Bus! Pre-FL (0x0xx) vs FL (0x3xx) unterschiedliche IDs
  - Engine RPM: Pre-FL 0x0C0 vs FL 0x316
  - Vehicle Speed: Pre-FL 0x0E0 vs FL 0x360
  - Steering Wheel: Pre-FL 0x400 vs FL 0x260
  - **BRAUCHT: Fahrgestellnummer oder Baujahr-Info vom User!**

#### 💻 Developer → CAN-Community
- **Bremsdruck CAN-ID**: 0x0D6 + 0x0E8 (beide UNVERIFIED) — Implementiert, braucht physikalische Verifikation
- **ABS Radgeschwindigkeiten**: 0x0D4 + 0x0D5 (UNVERIFIED) — Implementiert, braucht Sniffer-Verifikation
- **Lenkwinkel CAN-ID**: 0x128 + 0x1B8 (beide UNVERIFIED) — Implementiert, braucht Verifikation
- **Gierrate/Querbeschleunigung**: 0x0D7 (UNVERIFIED) — Implementiert, braucht Verifikation
- **Motor-Status**: 0x0C4 (UNVERIFIED) — Implementiert, braucht Verifikation
- **Licht-Status**: 0x3F0 → jetzt 0x420 Exterior Lighting (VERIFIED in DB) ✅
- **Gurt-Status**: 0x380 → jetzt 0x450 Seatbelt Warning (VERIFIED in DB) ✅
- **PiCAN2 Hardware**: Besorgen und Erst-Test mit candump can0
- **56 CAN-Messages** dekodiert (32 verified, 12 community, 12 unverified)

#### 💻 Developer → Developer (selbst) — ERLEDIGT 2026-05-28
- ✅ **56 CAN-Messages dekodiert** — von 34 auf 56 Messages erweitert
- ✅ **181 DTC-Codes** in v50_dtc_reader.py — Powertrain, Chassis, Body, Network, Volvo-spezifisch
- ✅ **OBD2 Diagnose-Modul** — Mode 01/03/04/07/09 vollständig implementiert
- ✅ **Data Logger (SQLite+CSV)** — Session-Tracking, Rotation, 20Hz
- ✅ **App-Controller (v50_app.py)** — Zentraler Orchestrierer für alle Module
- ✅ **Wartungs-Tracker erweitert** — 12 Service-Intervalle, km-Stand-basiert
- ✅ **Dashboard DTC-Diagnose-Overlay** — Taste `D` öffnet DTC-Scan, Clear, Maintenance-Anzeige
- ✅ **Dashboard Doors/Lights/Cruise** — Neue Readouts für Türstatus, Lichter, Tempomat
- ✅ **Dashboard Warning-Lights** — Gurt (🛟), ABS (⚠️) hinzugefügt
- ✅ **Neue CAN-Messages**: Bremslichtschalter (0x0B4), ABS 4ch (0x1C0), Getriebe AT (0x180), Giertrate (0x0F8), Exterior Lighting (0x420), Heckklappe (0x438), Tempomat (0x430), Lichtschalter (0x440), Hupe (0x448), Gurt (0x450), Audio (0x500/0x510), Facelift (0x316/0x330/0x360)

#### 💻 Developer → Chef/User — NEUE ANFRAGEN
- **PiZ-Up USV HAT (~€30)**: Empfohlen für sicheres Herunterfahren. Verhindert SD-Karten-Korruption. Budget-Erhöhung nötig?
- **Display-Platzierung**: Wo im V50? OEM-Tacho darf NICHT verdeckt werden (TÜV!). Optionen:
  - Handschuhfach (diskret, aber nicht direkt sichtbar)
  - Mittelkonsole (sichtbar, Kabelführung komplexer)
  - 3D-gedrucktes Gehäuse unterhalb des OEM-Tachos?
- **Stealth-Toggle Hardware**: GPIO-Taste am Pi4? Oder Lenkradtaste via CAN?

#### 🏁 Fahrwerk → v50-budget
- **KONI Special Active (Yellow) Verfügbarkeit**: 86-2636SP4 / 80-2629SP4
  - Ersetzt FSD-Serie — lieferbar oder nicht?
  - Falls nicht: KONI Special RED = bewährte Alternative

#### 🎨 Optik → v50-budget
- **Aktuelle Preis-Verifikation**: Autodoc/Skandix Preise überprüfen
  - Besonders: Eibach Pro-Kit, KONI RED, Goodridge VSV-004

### 📋 NEUE ERKENNTNISSE vom Chief (2026-05-28)

1. **Eibach T5 vs 2.4i VERWECHSLUNGS-GEFAHR**: 
   - ✅ 2.4i FWD = E10-41-001-05-22
   - ❌ T5 AWD = E10-85-003-01-22 (in DB für beide gelistet — FALSCH für 2.4i!)
   
2. **25 T5-only Teile identifiziert**: Turbo, Intercooler, Downpipe etc. — alle SKIP

3. **Osram Night Breaker LASER H7 statt LED**:
   - Halogen = komplett EINTRAGUNGSFREI
   - Fast so hell wie LED
   - Spart €20-40 + TÜV-Eintragungskosten
   - = Besserer STEALTH-Ansatz!

4. **Ferrita Auspuff MITNEHMEN**: Budget erlaubt es (€550-2.050 Reserve mit Auspuff)

5. **PCV Breather Box**: Febi vs OEM — OEM empfohlen (€80-120 vs €42-55)