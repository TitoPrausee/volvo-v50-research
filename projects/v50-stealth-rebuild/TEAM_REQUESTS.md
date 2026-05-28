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

## 📊 Budget-Stand 2026-05-28 v5

**GESAMT (mit Auspuff): €1.805-4.268 — ✅ INNERHALB €3.500-5.000 HARD CAP**

| Phase | Min (€) | Realistisch (€) | Budget-Spot | Status |
|-------|--------:|----------------:|------------:|--------|
| 1: Sicherheit | 350 | 530 | 500-800 | ✅ |
| 2: Fahrwerk | 490 | 780 | 800-1.200 | ✅ |
| 3: Optik | 200 | 350 | 800-1.200 | ✅ |
| 4: Motor (o. Auspuff) | 70 | 175 | 400-600 | ✅ |
| 4: Motor (m. Auspuff) | 540 | 870 | — | ⚠️ |
| 5: Reserve | 75 | 145 | 200-400 | ✅ |
| TÜV | 150 | 200 | — | — |
| **GESAMT (m. Auspuff)** | **1.805** | **2.875** | **3.500-5.000** | ✅ |

Siehe CHIEF_STATUS.md für vollständige Budget-Analyse.

## Offene Team-Anfragen

### ✅ GELÖST (seit letztem Update)
- **TÜV-Experte**: Vollständig dokumentiert in BUDGET_TUV_REPORT.md
- **Lackier-Experte**: DIY Polierung = €30-50, spart €250-550
- **Stabi-Experte**: Lemförder + SuperPro Poly in DB
- **Polestar für B5244S**: SKIP bestätigt — nur für T5, nicht STEALTH
- **K&N Teilenummer**: ✅ 33-2873 korrigiert
- **Facelift-SW Teilenummern**: ✅ 31265914/31265915 korrigiert (H7 Halogen!)
- **Ferodo DS2500**: ✅ ALS ILLEGAL markiert → TRW/ATE ECE R90 statt

### 🔴 OFFEN — BRAUCHT USER-INPUT

#### 🔴 Chef → User
- **V50-BAUJAHR IDENTIFIZIEREN**: 
  - 🔴 KRITISCH für: CAN-IDs, Scheinwerfer-TN, Grill-Kompatibilität, Rücklichter
  - Pre-FL (2004-2007) vs FL (2008-2012) = unterschiedliche CAN-Bus Protokolle!
  - Engine RPM: Pre-FL 0x0C0 vs FL 0x316
  - Vehicle Speed: Pre-FL 0x0E0 vs FL 0x360
  - **BRAUCHT: Fahrgestellnummer oder Baujahr!**

### 🟡 OFFEN — RESEARCH NEEDED

#### 👔 Chef → v50-exterior
- **Facelift-Scheinwerfer Verfügbarkeit prüfen**: 31265914/31265915 auf eBay/Kleinanzeigen
- **Facelift-Rücklichter OEM Suche**: Eintragungsfrei = STEALTH-Konform!

#### 👔 Chef → v50-engine
- **Mann Luftfilter VIN-Verifikation**: C 25 107 vs C 27 107 / C 28 110 → VIN-Check!
- **Mann Innenraumfilter VIN-Verifikation**: CUK 27 003 vs CUK 24 013 → VIN-Check!

#### 💻 Developer → Chef/User
- **PiCAN2 Hardware**: Besorgen und Erst-Test mit candump can0
- **56 CAN-Messages**: 32 verified, 12 community, 12 unverified
- **Bremsdruck CAN-ID**: 0x0D6 + 0x0E8 UNVERIFIED
- **ABS Radgeschwindigkeiten**: 0x0D4 + 0x0D5 UNVERIFIED
- **Lenkwinkel CAN-ID**: 0x128 + 0x1B8 UNVERIFIED

### ✅ ERLEDIGT 2026-05-28

#### 💻 Developer → Developer (selbst)
- ✅ **56 CAN-Messages dekodiert** — von 34 auf 56 Messages erweitert
- ✅ **181 DTC-Codes** in v50_dtc_reader.py — Powertrain, Chassis, Body, Network, Volvo-spezifisch
- ✅ **OBD2 Diagnose-Modul** — Mode 01/03/04/07/09/22
- ✅ **v50_app.py Zentral-Controller** — Orchestriert alle Module
- ✅ **PiZ-Up USV HAT** für Safe-Shutdown → ~€30 extra
- ✅ **Licht-Status CAN-ID**: 0x3F0 → 0x420 Exterior Lighting VERIFIED ✅
- ✅ **Gurt-Status CAN-ID**: 0x380 → 0x450 Seatbelt Warning VERIFIED ✅

## Korrekturen-Log

| Datum | Korrektur | Grund |
|-------|-----------|-------|
| 2026-05-28 | K&N 33-2221 → 33-2873 | Passt NICHT zum V50 2.4i B5244S |
| 2026-05-28 | FL-SW TN 30796020-23 → 31265914/31265915 | Alte TN waren Pre-FL! |
| 2026-05-28 | Ferodo DS2500 → ILLEGAL markiert | KEIN ECE R90! TRW statt! |
| 2026-05-28 | Dayco KTB481 Warnung | Manche Angebote OHNE Wasserpumpe! |
| 2026-05-28 | HEL > Goodridge TÜV-Eintragung | HEL inkl. Zertifikat, Goodridge braucht Einzelabnahme |