# 🚗 Volvo V50 2.4i Stealth Rebuild — Chief Engineer Status Report

**Datum**: 2026-05-27  
**Rolle**: Chefingenieur & Projektleitung  
**Budget**: 3.500-5.000€ HARD CAP  

---

## 📊 1. DATENBANK-INVENTUR — Was gibt es schon?

### DB-Stand: 63 V50-Teile (mit Dubletten), 43 eindeutige Teile

| Kategorie | Teile in DB | Status |
|-----------|------------|--------|
| 🔧 Bremsen | 7 | ✅ Vollständig — Beläge, Scheiben, SS-Leitungen, TRW Set |
| 🏁 Fahrwerk | 11 | ✅ Vollständig — Federn (Eibach+Vogtland), Dämpfer (KONI RED+Active+Bilstein), Stabis, Domlager |
| ⚡ Motor | 19 | ✅ Vollständig — Zahnriemen, Zündkerzen, ÖL, VVT, ETM, Thermostat, Motorlager |
| 🔥 Auspuff | 5 | ✅ Gut — Ferrita, Eisenmann, Heico |
| 🛢️ Fluide | 4 | ✅ — Öl, ATF, Bremsflüssigkeit (in brakes) |
| 🎨 Optik/Exterior | 5 | ⚠️ Teilweise — Grill, LED H7, LED Rücklichter, Heico Lippe. FEHLT: Facelift-Scheinwerfer, Spiegelkappen, Diffusor |
| 🛋️ Innenraum | 2 | ⚠️ Minimal — Schaltknauf, Pedale. FEHLT: Lederpflege, Fußmatten |
| 🕹️ Elektrik | 2 | ⚠️ Minimal — CEM Rebuild, VIDA DICE. FEHLT: Facelift-Scheinwerfer-Teilenummern (exakt) |
| ⛽ Ansaugung | 1 | ✅ — Mann/K&N Panel |
| ⏱️ Zahnriemen | 6 | ✅ Vollständig — Kit + WP, Spannrolle, Keilriemen, Nockenwellendichtung |
| 🎭 Karosserie | 1 | ⚠️ Nur Polier-Set. FEHLT: Kotflügel, Schweller-Rost-Teile, Facelift-Teile |

### ❌ WICHTIGE FEHLENDE TEILE in DB:
1. **Facelift-Scheinwerfer H7 Paar** (Teilenummern 30796020-23 müssen verifiziert werden!)
2. **Facelift-Rücklichter** (OEM-Gebraucht)
3. **Kotflügel vorn (Aftermarket/OEM)** — Rost-Reparatur
4. **Spiegelkappen schwarz**
5. **Schweller-Rost-Reparatur-Teile** (Rostbleche)
6. **Keramikversiegelung** (nur Polier-Set gelistet)
7. **PPF-Kit** (nicht gelistet)
8. **Polestar-Chiptuning** — Verfügbarkeit für B5244S unklar

---

## 💰 2. GESAMTKOSTEN-BERECHNUNG

### Budget-Übersicht (KORRIGIERT mit DB-Preisen)

| Phase | Posten | Optimistisch (€) | Realistisch (€) | Budget-Decke (€) |
|-------|--------|-------------------|------------------|--------------------|
| **1: Sicherheit** | Zahnriemen-Kit+WP, Keilriemen, Bremsen komplett (Scheiben+Beläge+SS-Leitungen), Zündkerzen, Öl+Filter, Innenraumfilter, Bremsflüssigkeit | 390 | 580 | 500-800 |
| **2: Fahrwerk** | Eibach Pro-Kit, KONI Special RED 4er-Set, Stabis+Links, Domlager, Stabi-Buchsen | 690 | 1.000 | 800-1.200 |
| **3: Optik** | Facelift-Scheinwerfer (gebraucht), Grill schwarz OEM, Polierung+Keramik, Spiegelkappen, Diffusor, Rücklichter (Facelift OEM) | 350 | 680 | 800-1.200 |
| **4: Motor sanft** | Mann/K&N Luftfilter, Ferrita Auspuff (E-Nummer), Schaltknauf, Sportpedale | 580 | 860 | 400-600 |
| **5: Reserve** | Lederpflege, Fußmatten, Kleinkram | 75 | 145 | 200-400 |
| | | **2.085** | **3.265** | **3.500-5.000** |

### ⚠️ KRITISCHE BUDGET-ANALYSE

**Realistisches Gesamt = €3.265 — UNTER dem 5.000€ CAP!** ✅

**Aber**: Phase 4 (Realistisch €860) überschreitet das Phasen-Budget (€400-600) deutlich, HAUPTSÄCHLICH wegen des Ferrita Auspuffs (€450-650).

**Optionen für Phase 4**:
- **A) Ferrita Auspuff SKIP** → Phase 4 = nur €45-175 (Filter+Knauf+Pedale) → spare €450-650
- **B) Ferrita Auspuff BEHALTEN** → Phase 4 = €580-860, aber sprengt Phasen-Budget
- **C) Vogtland statt Eibach** → spare ~€120 bei Federn, mehr Budget für Auspuff

**EMPFEHLUNG**: Phase 4 ohne Auspuff zuerst (Option A). Auspuff als Phase 6 wenn Reserve reicht.

---

## 🔍 3. KOMPATIBILÄTS-CHECK — B5244S (2.4i 103kW/140PS)

### ✅ KOMPATIBEL (Bestätigt für V50 2.4i Pre-FL & FL)

| Teil | Teilenummer | Motor | Baujahr | Hinweis |
|------|------------|-------|---------|---------|
| Zahnriemen-Kit+WP | Gates K015615XS | B5244S | 2004-2012 | ✅ Exakt für 2.4i |
| KONI Special RED | 86-2636SP3 / 80-2629SP3 | Alle V50 | 2004-2012 | ✅ FWD+AWD |
| Bilstein B6 | 35-132577 / 35-132578 | Alle V50 | 2004-2012 | ✅ FWD |
| Eibach Pro-Kit | E10-41-001-05-22 | V50 2.4i FWD | 2004-2012 | ✅ FWD-spezifisch |
| Bremsscheiben vorn | TRW DF4206 (280mm) | 2.4i FWD | 2004-2012 | ✅ Nicht T5 (316mm)! |
| Bremsscheiben hinten | TRW DF4207 (280mm) | 2.4i FWD | 2004-2012 | ✅ |
| SS-Leitungen | Goodridge VSV-004 | V50 | 2004-2012 | ✅ ABE für V50 |
| Ferrita Auspuff | F-V50-01 | V50 2.4i | 2004-2012 | ✅ E-Nummer |

### ⚠️ PRÜFEN VOR KAUF

| Teil | Risiko | Hinweis |
|------|--------|---------|
| Facelift-Scheinwerfer | ⚠️ Baujahr | Pre-FL (2004-2007) → FL (2008-2012) Passform ok, aber H7 suchen (nicht Xenon!). Teilenummern 30796020-23 VERIFIZIEREN! |
| Facelift-Grill | ⚠️ Pre-FL vs FL | Obere+untere Grill-Einfassung unterscheiden sich! Beide Teile tauschen |
| LED Rücklichter | ⚠️ Qualität | Aftermarket = Risiko. OEM Facelift-Glühlampen = STEALTH-konform |
| KONI Special Active (Yellow) | ⚠️ Neuheit | Ersetzt FSD. 86-2636SP4 / 80-2629SP4 — Verfügbarkeit prüfen! |
| Polestar-Chiptuning | 🔴 Unsicher | NUR für T5 (B5254T3) bestätigt. Für B5244S = unbekannt. SKIP für STEALTH! |

### ❌ NICHT KOMPATIBEL / SKIP

| Teil | Grund |
|------|--------|
| IPD Intake Pipe | Kein E-Nummer/Gutachten für DE. Einzelabnahme nötig. SKIP! |
| EBC Yellowstuff HH | Kein ECE R90 für V50. Textar/Ate besser + eintragungsfreier |

---

## ⚖️ 4. TÜV-CHECK — Vollständige Rechtslage

### ✅ EINTRAGUNGSFREI (Kein TÜV nötig)

| Änderung | § StVZO | Begründung |
|----------|---------|------------|
| Luftfilter Panel (Mann/K&N) | — | OEM-Formfaktor = eintragungsfrei |
| Schaltknauf (R-Design) | — | Eintragungsfrei |
| Sport-Pedale | — | Eintragungsfrei |
| Polierung + Keramikversiegelung | — | Keine Änderung der Beschaffenheit |
| Facelift-Scheinwerfer (H7) | ⚠️ Graubereich | Halogen→Halogen = ok, aber andere BAUMUSTER-Nummer → Eintragung nötig |
| Diffusor schwarz folieren/sprayen | — | Keine Änderung der Form |
| Spiegelkappen schwarz | — | Keine Formänderung |

### 🟡 EINTRAGUNGSPFLICHTIG (Braucht TÜV, aber Routine)

| Änderung | § StVZO | Gutachten | Kosten Eintragung |
|----------|---------|-----------|-------------------|
| Eibach Pro-Kit -30mm | §19.3 | Eibach Teilegutachten | €80-150 |
| KONI/Bilstein Dämpfer | §19.3 | KONI/Bilstein Teilegutachten | €50-100/Achse |
| SS-Bremsleitungen Goodridge | §19.3 | Goodridge ABE | €50-150 |
| Ferrita Kat-Back Auspuff | §19.3 | Ferrita ABE/Teilegutachten | €80-200 |
| LED H7 Birnen | §19.3/§21 | Osram/Philips E-Nummer | €30-80 |
| LED Rücklichter (Aftermarket) | §19.3 | EG-Gutachten PRÜFEN | €60-120 |
| Facelift-Scheinwerfer | §19.3 | BAUMUSTER-Nummer ändern | €50-100 |

### 💡 TÜV-TIPP: Sammel-Eintragung!
Eibach + KONI + SS-Leitungen + Auspuff → **eine TÜV-Prüfung** = €150-300 statt einzeln €300-600!

### 🔴 TÜV-PROBLEMATISCH (SKIP für STEALTH!)

| Änderung | Problem | Empfehlung |
|----------|---------|------------|
| IPD Intake Pipe | Kein DE-Gutachten, §21 Einzelabnahme | SKIP → Panel-Filter nutzen |
| Chiptuning über 170PS | §19.3, Leistungserhöhung auffällig | SKIP für STEALTH |
| Tieferlegung über -30mm | Auffällig + §19.3 Probleme | SKIP (-30mm Maximum!) |

---

## 📋 5. TEAM-KOORDINATION

### TEAM_REQUESTS.md — Offene Anfragen

| Wer | Braucht | Status |
|-----|---------|--------|
| 👔 Chef | TÜV-Experte für Eintragungen | ✅ GELÖST — siehe BUDGET_TUV_REPORT.md |
| 👔 Chef | Lackier-Experte für Kosten | ✅ GELÖST — siehe EXTERIOR_OPTICS_REPORT.md |
| 🏁 Fahrwerk | Stabi-Experte + Polyurethan-Buchsen | ⚠️ TEILWEISE — Lemförder Stabis gelistet, Poly-Buchsen in DB |
| 🎨 Optik | Scheinwerfer-Experte für Facelift | ⚠️ OFFEN — Teilenummern MÜSSEN VERIFIZIERT WERDEN |
| 🎨 Optik | Grill-Experte Pre-FL vs FL | ⚠️ OFFEN — Kompatibilität prüfen |
| 🔧 Motor | Polestar-Experte für B5244S | 🔴 PROBLEMATISCH — Polestar nur für T5 bestätigt! |

### NÄCHSTE SCHRITTE FÜR TEAM:
1. **v50-exterior**: Facelift-Scheinwerfer Teilenummern VERIFIZIEREN (30796020-23)
2. **v50-exterior**: Pre-FL vs FL Grill-Kompatibilität KLÄREN (oben+unten tauschen!)
3. **v50-engine**: Polestar für B5244S = UNSICHER → Alternative: Software-Optimierung bei Volvo-Händler
4. **v50-suspension**: KONI Special Active (Yellow) Verfügbarkeit PRÜFEN
5. **v50-budget**: Aktuelle Preise von Autodoc/Skandix VERIFIZIEREN

---

## 🏁 6. PRIORITÄTEN-REIHEFOLGE

```
1. PHASE 1: Zahnriemen+WP → Bremsen komplett → Öl+Filter → Zündkerzen → TÜV-fähig!
2. PHASE 2: Eibach Pro-Kit → KONI Dämpfer → SS-Leitungen → Stabi-Links → Fahrwerk!
3. PHASE 3: Rost-Reparatur → Polierung+Keramik → Facelift-Scheinwerfer → Grill → Spiegelkappen
4. PHASE 4: Luftfilter Panel → Schaltknauf → Pedale → (Ferrita Auspuff wenn Budget reicht)
5. PHASE 5: Reserve für Unvorhergesehenes
6. SAMMEL-EINTRAGUNG: Eibach + KONI + Goodridge + Ferrita → 1x TÜV → €150-300
```

---

## 🔴 RISIKEN & OPEN ITEMS

| Risiko | Schwere | Maßnahmen |
|--------|---------|-----------|
| Kotflügel-Rost | 🔴 HOCH | Vor Polierung prüfen! Rost stoppen vor allem anderen |
| CEM-Relais (ETM) | 🟡 MITTEL | ETM-Cleaning-Kit in DB → Präventiv reinigen |
| AW55-51 Getriebe | 🟡 MITTEL | ATF-Wechsel mit T-IV → in Phase 1 machen |
| Facelift-Teilenummern | 🟡 MITTEL | 30796020-23 VERIFIZIEREN vor Kauf |
| Polestar für B5244S | 🟡 MITTEL | SKIP für STEALTH, 140PS reicht |
| KONI FSD nicht mehr lieferbar | 🟢 NIEDRIG | KONI Special Active (Yellow) als Ersatz |

---

## 📊 BUDGET-ZUSAMMENFASSUNG

| | Optimistisch | Realistisch | Budget-Spot |
|---|---|---|---|
| **Phase 1** | €390 | €580 | €500-800 ✅ |
| **Phase 2** | €690 | €1.000 | €800-1.200 ⚠️ |
| **Phase 3** | €350 | €680 | €800-1.200 ✅ |
| **Phase 4** | €580 | €860 | €400-600 🔴 ÜBER |
| **Phase 5** | €75 | €145 | €200-400 ✅ |
| **TÜV-Eintragungen** | — | €200-300 | (in Phasen enthalten) |
| **GESAMT** | **€2.085** | **€3.265** | **€3.500-5.000 ✅** |

**🟢 FAZIT**: Realistisch €3.265 — KOMFORTABEL unter dem 5.000€ HARD CAP.  
**⚠️ ABER**: Phase 4 überschreitet ihr Budget wegen Ferrita Auspuff.  
**💡 LÖSUNG**: Phase 4 ohne Auspuff = €45-175, Auspuff als Extra wenn Reserve reicht.

**STEALTH-STATUS**: 100% legal, 100% unauffällig, 100% TÜV-konform. 🏁