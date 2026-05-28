# 🚗 Volvo V50 2.4i Stealth Rebuild — Chief Engineer Status Report

**Datum**: 2026-05-28 (v4 — Motor-Updated)  
**Rolle**: Chefingenieur & Projektleitung  
**Budget**: 3.500-5.000€ HARD CAP  

---

## 📊 1. DATENBANK-INVENTUR — Was gibt es schon?

### DB-Stand: 425+ Teile, 763 Fitments

|| Kategorie | Eindeutige Teile | Status ||
||-----------|-----------------:|--------||
|| 🔧 Bremsen | 17 | ✅ Vollständig — TRW+ATE+Brembo+Textar+Goodridge+HEL+Zimmermann ||
|| 🏁 Fahrwerk | ~20 | ✅ Vollständig — Eibach+Vogtland Federn, KONI RED+Active+Bilstein B6, Stabis, Domlager, Poly-Buchsen ||
|| ⚡ Motor | 38 | ✅ Vollständig — Zahnriemen, Zündkerzen, Öl, VVT, ETM, Thermostat, Motorlager, PCV, Zündspulen ||
|| 🔥 Auspuff | 6 | ✅ Gut — Ferrita (€420-650), Eisenmann (€800-1100), Heico (€750-950) ||
|| 🛢️ Fluide | 5 | ✅ — Öl, ATF T-IV, Bremsflüssigkeit DOT4, Lenkflüssigkeit, Kühlwasser ||
|| 🎨 Optik/Exterior | 4 | ⚠️ Teilweise — Grill, LED H7, LED Rücklichter, Heico Lippe ||
|| 🛋️ Innenraum | 5 | ⚠️ Teilweise — Schaltknauf, Pedale, Lederpflege, DIM Cluster, Sonnenblende ||
|| 🕹️ Elektrik | 8 | ⚠️ — ABS-Sensor, Batterie, CEM-Relay, ETM, Anlasser, Lichtmaschine ||
|| ⛽ Ansaugung | 2 | ✅ — **K&N 33-2873** (korrigiert!) / Mann C 25 107, MAF Sensor ||
|| ⏱️ Zahnriemen | 5 | ✅ — Gates+Contitech+Dayco Kit, WP, Keilriemen, Nockenwellendichtung ||
|| ❄️ Kühlung | 5 | ✅ — Kühlmittel, Ausgleichsbehälter, Thermostat, WP ||

### ⚠️ KRITISCHE KORREKTUR: K&N Teilenummer

| Detail | ALT | NEU |
|--------|-----|-----|
| **K&N Panel-Filter** | ~~33-2221~~ ❌ | **33-2873** ✅ |
| **Quelle** | Ung verified | Amazon.de bestätigt: "V50 2.4L L5 F/I 2004" |
| **Action** | — | Alle Referenzen auf 33-2221 korrigieren |

> 🔴 **33-2221 passt NICHT zum V50 2.4i B5244S!** Richtig: K&N 33-2873. DB-Update durchgeführt.

### ⚠️ TEILENUMMER VERIFIKATION NÖTIG

| Teil | Alte PN | Amazon zeigt | Status |
|------|---------|-------------|--------|
| Mann Luftfilter | C 25 107 | C 27 107 / C 28 110 | 🔴 **VIN-Check vor Kauf!** |
| Mann Innenraumfilter | CUK 27 003 | CUK 24 013 | 🟡 **VIN-Check vor Kauf!** |

---

## 💰 2. GESAMTKOSTEN-BERECHNUNG (2026-05-28 v4 — Motor-Update)

### Phase 1: Preise mit Amazon.de Live-Daten aktualisiert

| Teil | alte Preise | **neue Preise AMZ Live** | Delta |
|------|------------|-------------------------|-------|
| Gates K015615XS Zahnriemen-Kit+WP | €120-160 | **€60-68** | ⬇️ -50% |
| Contitech CT1120WP1 | €110-150 | **€105-161** | ≈ gleich |
| Keilriemen 5PK1130 | €12-25 | **€14-17** | ≈ gleich |
| Zündkerzen FR7KPP33+ 5er | €35-50 | **€49-52** | ↑ teurer |
| Ölfilter Mann W 719/30 | €8-12 | **€6-10** | ↓ günstiger |
| Luftfilter Mann | €8-14 | **€13-16** | ↑ teurer |
| Motoröl Castrol 5W-30 A5 | €30-45 | **€37-48** | ↑ teurer |
| Bremsflüssigkeit DOT4 | €8-15 | **€14-22** | ↑ teurer |

### Budget-Übersicht (aktualisiert)

| Phase | Posten | Min (€) | Max (€) | Budget-Decke | Status |
|-------|--------|--------:|--------:|-------------:|--------|
| **1: Sicherheit** | Zahnriemen+WP, Keilriemen, Bremsen, Zündkerzen, Öl, Filter, Nockenwellendichtung, DOT4, ATF | 350 | 580 | €500-800 | ✅ |
| **2: Fahrwerk** | Eibach Pro-Kit, KONI RED, Stabi-Links, Domlager, Stabi-Buchsen, Keramik | 490 | 780 | €800-1.200 | ✅ |
| **3: Optik** | Polierung DIY, Keramik, Grill, LED H7 LASER, Facelift-SW, Facelift-RL, Spiegelkappen, Rost | 200 | 350 | €800-1.200 | ✅ |
| **4: Motor sanft** | Mann Luftfilter, Schaltknauf, Pedale, ETM-Clean, PCV-Kit | 70 | 175 | €400-600 | ✅ |
| **4+ (optional)** | + Ferrita Auspuff F-V50-01 + TÜV | 470 | 770 | — | ⚠️ |
| **5: Reserve** | Lederpflege, Fußmatten, CEM-Lötkit, Thermostatgehäuse, VVT, Ausgleichsbehälter | 75 | 145 | €200-400 | ✅ |
| **TÜV** | Sammel-Eintragung (Eibach+KONI+Goodridge+Ferrita+SW+LED) | 150 | 300 | — | — |
| | | | | | |
| **TOTAL (ohne Auspuff)** | | **€1.335** | **€2.330** | **€3.500-5.000** | ✅ |
| **TOTAL (mit Auspuff)** | | **€1.805** | **€3.100** | **€3.500-5.000** | ✅ |

**🟢 FAZIT**: Beide Szenarien KOMFORTABEL unter dem 5.000€ HARD CAP!

---

## 🔑 3. KEY FINDINGS — Motor-Update

### Was sich geändert hat:
1. **Gates K015615XS = €60-68 auf Amazon.de** — VIEL billiger als die alten €120-160!
2. **K&N 33-2221 FALSCH** → Richtig: **33-2873** für V50 2.4i B5244S
3. **Mann C 25 107 / CUK 27 003** Teilenummern unsicher — VIN-Check nötig
4. **Polestar B5244S erneut bestätigt: NICHT verfügbar**
5. **Dayco KTB481 Vorsicht**: Manche Angebote ohne Wasserpumpe!
6. **Zündkerzen-Strategie**: 4er-Set + 1 einzeln auf Amazon = €49-52

### Was gleich geblieben ist:
- IPD Intake = SKIP (kein TÜV, kein E-Nummer)
- Ferrita F-V50-01 = bester legaler Auspuff (ABE, €420-650)
- 170PS nicht realistisch mit legalen Mitteln auf NA-Motor
- STEALTH = 140PS + clean condition = Sahnehaube

---

## 📋 4. TEAM-KOORDINATION

|| Wer | Braucht | Status | Neue Infos ||
||-----|---------|--------|------------||
|| 👔 Chef | TÜV-Experte für Eintragungen | ✅ GELÖST | BUDGET_TUV_REPORT.md komplett ||
|| 👔 Chef | Lackier-Experte für Kosten | ✅ GELÖST | DIY Polierung = €30-50 ||
|| 🏁 Fahrwerk | Stabi-Experte + Poly-Buchsen | ✅ GELÖST | Lemförder Stabis + SuperPro in DB ||
|| 🎨 Optik | Scheinwerfer-Experte für Facelift | ⚠️ OFFEN | TN 30796020-23 VERIFIZIEREN ||
|| 🎨 Optik | Grill-Experte Pre-FL vs FL | ⚠️ OFFEN | Oben+unten Einfassung tauschen! ||
|| 🔧 Motor | K&N Teilenummer-Korrektur | ✅ **GELÖST** | 33-2221 → **33-2873** ||
|| 🔧 Motor | Mann Filter Teilenummern | ⚠️ OFFEN | C 25 107 / CUK 27 003 VERIFIZIEREN ||
|| 💻 Developer | V50-Baujahr-Identifikation | ⚠️ OFFEN | Pre-FL vs FL → andere CAN-IDs! ||

---

## 🔴 RISIKEN & OPEN ITEMS

| Risiko | Schwere | Maßnahmen |
|--------|---------|-----------|
| Mann C 25 107 Teilenummer unklar | 🔴 HOCH | VIN-Check vor Kauf! |
| K&N 33-2221 Verwechslung | ✅ GELÖST | Richtig: 33-2873 |
| Kotflügel-Rost | 🔴 HOCH | Vor Polierung prüfen! |
| CEM-Relais (ETM) | 🟡 MITTEL | ETM-Cleaning-Kit → Präventiv reinigen |
| AW55-51 Getriebe | 🟡 MITTEL | ATF-Wechsel mit T-IV in Phase 1 |
| Facelift-Teilenummern | 🟡 MITTEL | 30796020-23 VERIFIZIEREN vor Kauf |
| Eibach T5 vs 2.4i Verwechslung | 🟡 MITTEL | E10-41-001-05-22 = 2.4i! |

---

**STEALTH-STATUS**: 100% legal, 100% unauffällig, 100% TÜV-konform. 🏁
**DB-STAND**: K&N 33-2873 korrigiert, Preise aktualisiert (Mai 2026).
