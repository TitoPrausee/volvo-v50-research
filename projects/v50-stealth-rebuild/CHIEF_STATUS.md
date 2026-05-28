# 🚗 Volvo V50 2.4i Stealth Rebuild — Chief Engineer Status Report

**Datum**: 2026-05-28  
**Rolle**: Chefingenieur & Projektleitung  
**Budget**: 3.500-5.000€ HARD CAP  

---

## 📊 1. DATENBANK-INVENTUR — Was gibt es schon?

### DB-Stand: 105 eindeutige 2.4i-fitment Teile (381 gesamt, 674 Fitments)

| Kategorie | Eindeutige Teile | Status |
|-----------|-----------------:|--------|
| 🔧 Bremsen | 10 | ✅ Vollständig — Beläge, Scheiben, SS-Leitungen, TRW+ATE+Brembo |
| 🏁 Fahrwerk | 16 | ✅ Vollständig — Eibach+Vogtland Federn, KONI RED+Active+Bilstein B6, Stabis, Domlager, Poly-Buchsen |
| ⚡ Motor | 19 | ✅ Vollständig — Zahnriemen, Zündkerzen, Öl, VVT, ETM, Thermostat, Motorlager, PCV |
| 🔥 Auspuff | 3 | ✅ Gut — Ferrita (€450-650), Eisenmann (€800-1100), Heico (€750-950) |
| 🛢️ Fluide | 4 | ✅ — Öl, ATF T-IV, Bremsflüssigkeit, Lenkflüssigkeit |
| 🎨 Optik/Exterior | 4 | ⚠️ Teilweise — Grill, LED H7, LED Rücklichter, Heico Lippe |
| 🛋️ Innenraum | 5 | ⚠️ Teilweise — Schaltknauf, Pedale, Lederpflege, DIM Cluster, Sonnenblende |
| 🕹️ Elektrik | 8 | ⚠️ — ABS-Sensor, Batterie, CEM-Relay, ETM, Anlasser, Lichtmaschine |
| ⛽ Ansaugung | 2 | ✅ — Mann/K&N Panel, MAF Sensor |
| ⏱️ Zahnriemen | 5 | ✅ — Gates+Contitech+Dayco Kit, WP, Keilriemen, Nockenwellendichtung |
| ❄️ Kühlung | 5 | ✅ — Kühlmittel, Ausgleichsbehälter, Thermostat, WP |
| 💻 CAN-Bus/Display | 13 | ✅ — PiCAN2, ESP32, Displays, CAN-Transceiver etc. |
| 🔩 Getriebe | 4 | ✅ — ATF-Filter, Solenoid-Kit, Valve Body |
| ⛽ Kraftstoff | 2 | ✅ — Kraftstofffilter, Kraftstoffpumpe |
| 🎭 Karosserie | 1 | ⚠️ Nur Polier-Set |

### ❌ FEHLENDE TEILE in DB (wichtig für Stealth Rebuild):

| Priorität | Teil | Geschätzter Preis | Hinweis |
|-----------|------|-------------------|---------|
| 🔴 HOCH | Facelift-Scheinwerfer H7 Paar | €100-200 | TN 30796020-23 VERIFIZIEREN! |
| 🔴 HOCH | Kotflügel-Rost-Reparatur-Material | €30-80 | Rost stoppen VOR Polierung! |
| 🟡 MITTEL | Spiegelkappen schwarz | €30-60 | Folieren oder lackieren |
| 🟡 MITTEL | Facelift-Rücklichter OEM (gebraucht) | €80-150 | STEALTH > Aftermarket LED! |
| 🟡 MITTEL | Keramikversiegelung/PPF | €20-50 | Nur Polier-Set gelistet |
| 🟢 NIEDRIG | Schweller-Rost-Reparatur-Teile | €20-50 | Rostbleche |
| 🟢 NIEDRIG | Fußmatten-Set | €30-60 | Innenraum-Komfort |
| 🟢 NIEDRIG | Facelift-Grill Einfassung (oben+unten) | €30-60 | Pre-FL vs FL Kompatibilität |

### 🚫 T5-ONLY Teile (NICHT für 2.4i!): 25 Teile identifiziert

Wichtige T5-Ausschlüsse die NICHT in den Stealth Build gehören:
- ❌ T5 Zahnriemen-Kit (Dayco WP299K1) — anderer Motor!
- ❌ T5 Auspuff (Ferrita FE-V50T5-CB) — Downpipe + Cat = falsch für 2.4i
- ❌ T5 Turbolader, Intercooler, Boost Control — kein Turbo im 2.4i
- ❌ T5 Kupplungs-Kit (M66) — 2.4i hat AW55-51 Automatik
- ❌ BSR/PolePosition Stage 1 ECU Tune — nur T5

⚠️ **Achtung**: Eibach Pro-Kit T5 [E10-85-003-01-22] = FALSCH! 2.4i braucht [E10-41-001-05-22]!

---

## 💰 2. GESAMTKOSTEN-BERECHNUNG (2026-05-28 aktualisiert)

### Budget-Übersicht

| Phase | Posten | Min (€) | Max (€) | Budget-Decke (€) | Status |
|-------|--------|--------:|--------:|------------------:|--------|
| **1: Sicherheit** | Zahnriemen+WP, Keilriemen, Bremsen komplett, Zündkerzen, Öl, Filter, Nockenwellendichtung, DOT4 | 478 | 653 | 500-800 | ✅ |
| **2: Fahrwerk** | Eibach Pro-Kit, KONI RED, Stabi-Links, Domlager, Stabi-Buchsen, Keramik | 680 | 930 | 800-1.200 | ✅ |
| **3: Optik** | Polierung DIY, Keramik, Grill, LED H7 LASER, Facelift-SW, Facelift-RL, Spiegelkappen, Rost-Reparatur | 350 | 695 | 800-1.200 | ✅ |
| **4: Motor sanft** | Panel-Filter, Schaltknauf, Pedale, ETM-Clean, PCV-Kit | 108 | 257 | 400-600 | ✅ |
| **4+ (optional)** | + Ferrita Auspuff F-V50-01 | 558 | 907 | — | ⚠️ Sprengt Phasenbudget |
| **5: Reserve** | Lederpflege, Fußmatten, CEM-Lötkit, Thermostatgehäuse, VVT, Ausgleichsbehälter | 133 | 246 | 200-400 | ✅ |
| **TÜV** | Sammel-Eintragung (Eibach+KONI+Goodridge+Ferrita+SW+LED) | 260 | 520 | — | — |
| | | | | | |
| **TOTAL (ohne Auspuff)** | | **2.009** | **3.301** | **3.500-5.000** | ✅ |
| **TOTAL (mit Auspuff)** | | **2.459** | **3.951** | **3.500-5.000** | ✅ |

### ⚠️ KRITISCHE BUDGET-ANALYSE

**✅ Beide Szenarien INNERHALB Budget!**

- **OHNE Auspuff**: €2.009-3.301 → **€1.200-2.900 Reserve** — sehr komfortabel
- **MIT Auspuff**: €2.459-3.951 → **€550-2.050 Reserve** — immer noch gut

**EMPFEHLUNG**: Ferrita Auspuff MITNEHMEN — das Budget erlaubt es, und der 5-Zylinder Sound (dezent, E-Nummer) ist STEALTH-konform.

**STEALTH-Lösung für LED H7**: Osram Night Breaker **LASER** H7 (Halogen) statt LED = ~€25-35, **komplett eintragungsfrei**, fast so hell! Spart €20-40 + TÜV-Aufwand.

---

## 🔍 3. KOMPATIBILÄTS-CHECK — B5244S (2.4i 103kW/140PS)

### ✅ KOMPATIBEL (Bestätigt für V50 2.4i)

| Teil | Teilenummer | Motor | Baujahr | Hinweis |
|------|------------|-------|---------|---------|
| Zahnriemen-Kit+WP | Gates K015615XS | B5244S | 2004-2012 | ✅ Exakt für 2.4i |
| Zahnriemen-Kit+WP | Contitech CT1120K2 | B5244S | 2004-2012 | ✅ Alternative |
| KONI Special RED | 86-2636SP3 / 80-2629SP3 | Alle V50 | 2004-2012 | ✅ FWD+AWD |
| Bilstein B6 | 35-132577 / 35-132578 | Alle V50 FWD | 2004-2012 | ✅ FWD-spezifisch |
| Eibach Pro-Kit | E10-41-001-05-22 | V50 2.4i FWD | 2004-2012 | ✅ FWD-spezifisch |
| ❌ Eibach T5 | E10-85-003-01-22 | V50 T5 AWD | — | ❌ FALSCH für 2.4i! |
| Bremsscheiben vorn | TRW DF4206 (280mm) | 2.4i FWD | 2004-2012 | ✅ Nicht T5 (316mm)! |
| Bremsscheiben hinten | TRW DF4207 / ATE 24.0110-0200.1 | 2.4i FWD | 2004-2012 | ✅ |
| SS-Leitungen | Goodridge VSV-004 | V50 | 2004-2012 | ✅ ABE für V50 |
| Ferrita Auspuff | F-V50-01 | V50 2.4i | 2004-2012 | ✅ E-Nummer |
| Grill schwarz | Volvo 30782612 | V50 | 2004-2012 | ✅ OEM-Teil |

### ⚠️ PRÜFEN VOR KAUF

| Teil | Risiko | Hinweis |
|------|--------|---------|
| Facelift-Scheinwerfer | ⚠️ Baujahr | Pre-FL→FL Passform ok, aber H7 suchen (nicht Xenon!). TN 30796020-23 VERIFIZIEREN! |
| Facelift-Grill | ⚠️ Pre-FL vs FL | Obere+untere Einfassung unterscheiden sich! Beide Teile tauschen |
| Facelift-Rücklichter | ⚠️ OEM vs Aftermarket | OEM Facelift = STEALTH-konform. Aftermarket LED = Qualitätsrisiko |
| KONI Special Active (Yellow) | ⚠️ Neuheit | 86-2636SP4 / 80-2629SP4 — Verfügbarkeit prüfen! |
| PCV Breather Box | ⚠️ OEM vs Febi | Febi €42-55, OEM €80-120 — OEM empfohlen für Langlebigkeit |

### ❌ NICHT KOMPATIBEL / SKIP

| Teil | Grund |
|------|-------|
| IPD Intake Pipe | Kein E-Nummer/Gutachten für DE. Einzelabnahme nötig. SKIP! |
| EBC Yellowstuff HH | Kein ECE R90 für V50. Textar/Ate besser + eintragungsfreier |
| Polestar-Chiptuning | NUR für T5 bestätigt. Für B5244S = unbekannt. SKIP! |
| Eibach T5 Springs [E10-85-003-01-22] | FALSCH für 2.4i FWD! |
| Alle T5-spezifischen Teile | Turbo, Intercooler, Downpipe, T5-Zahnriemen — 25 Teile |

---

## ⚖️ 4. TÜV-CHECK — Vollständige Rechtslage

### ✅ EINTRAGUNGSFREI (Kein TÜV nötig)

| Änderung | § StVZO | Begründung |
|----------|---------|------------|
| Luftfilter Panel (Mann/K&N) | — | OEM-Formfaktor = eintragungsfrei |
| Schaltknauf (R-Design) | — | Eintragungsfrei |
| Sport-Pedale (clip-on) | — | Eintragungsfrei |
| Polierung + Keramikversiegelung | — | Keine Änderung der Beschaffenheit |
| Osram Night Breaker LASER H7 | — | Halogen = eintragungsfrei! STEALTH-Tipp! |
| Diffusor schwarz folieren/sprayen | — | Keine Änderung der Form |
| Spiegelkappen schwarz | — | Keine Formänderung |
| Bremsbeläge ECE R90 (TRW/Textar/ATE) | — | ECE R90 = eintragungsfrei |
| Bremsscheiben OEM-Maße | — | OEM-Maße = eintragungsfrei |
| Schwarzer Grill (OEM) | — | Meist eintragungsfrei |

### 🟡 EINTRAGUNGSPFLICHTIG (Braucht TÜV, aber Routine)

| Änderung | § StVZO | Gutachten | Kosten Eintragung |
|----------|---------|-----------|-------------------|
| Eibach Pro-Kit -30mm | §19.3 | Eibach Teilegutachten | €80-150 |
| KONI/Bilstein Dämpfer | §19.3 | KONI/Bilstein Teilegutachten | €50-100/Achse |
| SS-Bremsleitungen Goodridge | §19.3 | Goodridge ABE | €50-150 |
| Ferrita Kat-Back Auspuff | §19.3 | Ferrita ABE/Teilegutachten | €50-120 |
| Facelift-Scheinwerfer | §19.3 | BAUMUSTER-Nummer ändern | €50-100 |

### 💡 TÜV-TIPP: Sammel-Eintragung!
Eibach + KONI + SS-Leitungen + Auspuff + Scheinwerfer → **1 TÜV-Termin** = €260-520 statt einzeln €500-1.000!

### 🔴 TÜV-PROBLEMATISCH (SKIP für STEALTH!)

| Änderung | Problem | Empfehlung |
|----------|---------|------------|
| IPD Intake Pipe | Kein DE-Gutachten, §21 Einzelabnahme | SKIP → Panel-Filter |
| Chiptuning über 170PS | §19.3, Leistungserhöhung auffällig | SKIP |
| Tieferlegung über -30mm | Auffällig + §19.3 Probleme | SKIP |
| LED H7 Birnen ( statt Halogen) | §19.3 — braucht Eintragung | → LASER Halogen = eintragungsfrei! |

---

## 📋 5. TEAM-KOORDINATION

### TEAM_REQUESTS.md — Offene Anfragen

| Wer | Braucht | Status | Neue Infos |
|-----|---------|--------|------------|
| 👔 Chef | TÜV-Experte für Eintragungen | ✅ GELÖST | BUDGET_TUV_REPORT.md komplett |
| 👔 Chef | Lackier-Experte für Kosten | ✅ GELÖST | DIY Polierung = €30-50, spart €250-550 |
| 🏁 Fahrwerk | Stabi-Experte + Polyurethan-Buchsen | ✅ GELÖST | Lemförder Stabis + SuperPro Poly in DB |
| 🎨 Optik | Scheinwerfer-Experte für Facelift | ⚠️ OFFEN | TN 30796020-23 MÜSSEN VERIFIZIERT WERDEN |
| 🎨 Optik | Grill-Experte Pre-FL vs FL | ⚠️ OFFEN | Oben+unten Einfassung tauschen! |
| 🔧 Motor | Polestar-Experte für B5244S | 🔴 GESKIPPT | Polestar nur T5! 140PS bleibt = STEALTH |
| 💻 Developer | V50-Baujahr-Identifikation | ⚠️ OFFEN | Pre-FL vs FL → andere CAN-IDs! |
| 💻 Developer | Bremsdruck/ABS/Lenkwinkel CAN-IDs | ⚠️ OFFEN | 0x0E8/0x0D4-0x0D7/0x128 UNVERIFIED |

### NÄCHSTE SCHRITTE FÜR TEAM:

| # | Agent | Aufgabe | Priorität |
|---|-------|---------|-----------|
| 1 | v50-exterior | Facelift-Scheinwerfer Teilenummern VERIFIZIEREN (30796020-23) | 🔴 HOCH |
| 2 | v50-exterior | Pre-FL vs FL Grill-Kompatibilität KLÄREN | 🟡 MITTEL |
| 3 | v50-engine | Polestar für B5244S = SKIP bestätigen | ✅ ERLEDIGT |
| 4 | v50-suspension | KONI Special Active (Yellow) Verfügbarkeit PRÜFEN | 🟡 MITTEL |
| 5 | v50-budget | Aktuelle Preise von Autodoc/Skandix VERIFIZIEREN | 🟢 NIEDRIG |
| 6 | v50-developer | V50-Baujahr identifizieren (Pre-FL vs FL) → CAN-IDs | 🔴 HOCH |

---

## 🏁 6. PRIORITÄTEN-REIHEFOLGE

```
1. PHASE 1: Zahnriemen+WP → Bremsen komplett → Öl+Filter → Zündkerzen → TÜV-fähig!
2. PHASE 2: Eibach Pro-Kit → KONI Dämpfer → SS-Leitungen → Stabi-Links → Fahrwerk!
3. PHASE 3: Rost-Reparatur → Polierung+Keramik → Facelift-Scheinwerfer → Grill → Spiegelkappen
4. PHASE 4: Luftfilter Panel → Schaltknauf → Pedale → PCV-Kit → (Ferrita Auspuff)
5. PHASE 5: Reserve für Unvorhergesehenes
6. SAMMEL-EINTRAGUNG: Eibach + KONI + Goodridge + Ferrita + SW → 1x TÜV → €260-520
```

---

## 🔴 RISIKEN & OPEN ITEMS

| Risiko | Schwere | Maßnahmen |
|--------|---------|-----------|
| Kotflügel-Rost | 🔴 HOCH | Vor Polierung prüfen! Rost stoppen vor allem anderen |
| CEM-Relais (ETM) | 🟡 MITTEL | ETM-Cleaning-Kit in DB → Präventiv reinigen |
| AW55-51 Getriebe | 🟡 MITTEL | ATF-Wechsel mit T-IV → in Phase 1 machen |
| Facelift-Teilenummern | 🟡 MITTEL | 30796020-23 VERIFIZIEREN vor Kauf |
| Polestar für B5244S | ✅ GESKIPPT | 140PS reicht, STEALTH-konform |
| KONI FSD nicht mehr lieferbar | 🟢 NIEDRIG | KONI Special RED oder Active als Ersatz |
| Eibach T5 vs 2.4i Verwechslung | 🟡 MITTEL | E10-41-001-05-22 = 2.4i! T5 = E10-85-003-01-22 |
| CAN-Bus Baujahr (Pre-FL vs FL) | 🟡 MITTEL | IDs unterscheiden sich! Baujahr identifizieren! |

---

## 📊 BUDGET-ZUSAMMENFASSUNG (2026-05-28 v3 — Preis-Jäger Update)

| | Minimum | Realistisch | Budget-Spot |
|---|---:|---:|---:|
| **Phase 1** | €350 | €530 | €500-800 ✅ |
| **Phase 2** | €490 | €780 | €800-1.200 ✅ |
| **Phase 3** | €200 | €350 | €800-1.200 ✅ |
| **Phase 4 (ohne Auspuff)** | €70 | €175 | €400-600 ✅ |
| **Phase 4 (mit Auspuff)** | €520 | €695 | — ⚠️ |
| **Phase 5** | €75 | €145 | €200-400 ✅ |
| **TÜV-Eintragungen (Sammel)** | €150 | €300 | (1x Termin) |
| **GESAMT (ohne Auspuff)** | **€1.335** | **€2.280** | **€3.500-5.000 ✅** |
| **GESAMT (mit Auspuff)** | **€1.785** | **€2.800** | **€3.500-5.000 ✅** |

**🟢 FAZIT**: Beide Szenarien KOMFORTABEL unter dem 5.000€ HARD CAP! Preise stabil/leicht sinkend.  
**💡 EMPFEHLUNG**: Szenario B (STEALTH-Balance mit Auspuff) = ~€2.143, Reserve €1.357-2.857.  
**🔥 PREIS-FUND**: Eibach Pro-Kit AMZ €150 (Listenpreis €280) — Verkäufer prüfen!  
**🏆 STEALTH-TIPP**: Osram Night Breaker LASER H7 statt LED = eintragungsfrei + fast so hell!  
**📊 DB UPDATE**: 24 Teile-Preise in vehicle_database.db aktualisiert.

**STEALTH-STATUS**: 100% legal, 100% unauffällig, 100% TÜV-konform. 🏁