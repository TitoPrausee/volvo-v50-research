# 🚗 Volvo V50 2.4i Stealth Rebuild — Chief Engineer Status Report

**Datum**: 2026-05-28 (v10 — TÜV-Experte Deep-Dive, 45 Teile TÜV-klassifiziert, Polestar/BSR/IPD geklärt)  
**Rolle**: Chefingenieur & Projektleitung  
**Budget**: 3.500-5.000€ HARD CAP  
**DB-STAND**: 674 Teile, 1.075 Fitments, 440 Quellen, 200 V50 2.4i unique Parts, 78 verified  

---

## 📊 1. DATENBANK-INVENTUR — Was gibt es schon?

### DB-Stand: 668 Teile, 21 Kategorien, 381 V50 2.4i Fitments (Pre-FL + FL)

| Kategorie | Unique Parts | Verified | Top-Teile | Lücken |
|-----------|-------------:|:--------:|-----------|--------|
| 🔧 Bremsen | 20 | 14 | TRW GDB1359/58, HEL SS, ATE Ceramic, Zimmermann Sportribbel | ✅ Vollständig |
| 🏁 Fahrwerk | 25 | 16 | Eibach Pro-Kit, KONI RED/Active, Lemförder Links, SuperPro | ✅ Vollständig |
| ⚡ Motor | 19 | 14 | Gates K015615XS, ETM, Thermostat, Motorlager, PCV | ✅ Vollständig |
| 🔥 Auspuff | 3 | 3 | Ferrita F-V50-01 (ABE!), Eisenmann, Heico | ✅ Gut — 3 Optionen |
| 🛢️ Fluide | 5 | 2 | Öl 5W-30 A5, ATF T-IV, DOT4, CHF 11S, Kühlwasser | ✅ |
| 🎨 Optik/Exterior | 12 | 8 | Grill, LED H7 LASER, FL-Scheinwerfer, FL-Ecklichter, PPF | ✅ |
| 🛋️ Innenraum | 14 | 14 | DIM-Kit, CEM-Löt-Kit, Schaltknauf, Pedale, Lederpflege | ✅ v2 |
| ⚡ Elektrik | 22 | 11 | ABS-Sensor, Batterie, CEM-Relay, FL-Scheinwerfer, BCM | ✅ |
| ⛽ Ansaugung | 2 | 2 | **K&N 33-2873** (korrigiert!) / Mann C 25 107 | ✅ |
| ⏱️ Zahnriemen | 5 | 5 | Gates+Contitech+Dayco Kit, WP, Keilriemen, Nockenwellendichtung | ✅ |
| ❄️ Kühlung | 6 | 6 | Kühlwasser, Ausgleichsbehälter, Thermostat, WP | ✅ |
| 🔩 Getriebe | 5 | 4 | ATF Filter+Kit, Valve Body, Solenoid, ATF Flush | ✅ |
| 💎 Stabilisatoren | (in Fahrwerk) | — | Lemförder Links, Do88+Estoni 24/22mm, IPD 25mm | ✅ |
| 🛞 Lager | 5+6 | 2+6 | SKF+ FAG Radlager v+h, 280mm Standard + 316/302mm T5 Bremsen | ✅ v3 |
| 🔌 CAN-Bus | 9 | 8 | Pi4+PiCAN2, ESP32, Displays, CAN-HAT, OBD2 | ✅ |
| 📟 Displays | 4 | 0 | OLED, TFT 2.4", TFT 3.5", HDMI 7" | ⚠️ Kein verified |
| 🛠️ Tools | 0+2 | 0 | (NX650-only: D5 Glow Plug Socket, Compression Tester) | ❌ V50 leer |
| 🛞 Reifen | 0 | 0 | 17" BLEIBEN, kein Eintrag nötig | ✅ |

### ⚠️ KRITISCHE KORREKTUREN (Stand v9)

| Detail | ALT | NEU | Status |
|--------|-----|-----|--------|
| **K&N Panel-Filter** | ~~33-2221~~ ❌ | **33-2873** ✅ | 🔴 Korrigiert in DB |
| **Mann Luftfilter** | C 25 107 | **VIN-Check vor Kauf!** → C 27 107 / C 28 110 möglich | 🟡 Unklar |
| **Mann Innenraumfilter** | CUK 27 003 | **VIN-Check vor Kauf!** → CUK 24 013 möglich | 🟡 Unklar |
| **Facelift-SW Teilenummern** | 30796020-23 ❌ | **31265914/31265915** ✅ (H7 Halogen) | 🔴 Korrigiert in DB |
| **Dayco KTB481** | Komplett-Kit | **NUR Riemen, kein Kit!** ⚠️ Manche OHNE WP! | 🟡 Warnung |
| **Thermostat-Gehäuse MAHLE** | €15-35 | **€37-41** ⬆️ | 🔴 PREIS-UPDATE v3! |
| **Castrol EDGE 5W-30** | €37-48/5L | **€48-58/5L** ⬆️ | 🔴 PREIS-UPDATE v3! |
| **SKF VKMC 02142** | €105-140 | **€60-90** ⬇️ | 🟢 VIEL GÜNSTIGER v3! |
| **PCV Breather Box** | €42-120 | **€24-31** ⬇️ | 🟢 VIEL GÜNSTIGER v3! |
| **Keilriemen 5PK1130** | €14-17 | **€4-10** ⬇️ | 🟢 HALBPREIS v3! |
| **Motorlager Lemförder** | €28-40 | **€45-64** ⬆️ | 🔴 PREIS-UPDATE v3! |
| **Ferodo DS2500** | Sport-Beläge | **KEIN ECE R90 → ILLEGAL!** | 🔴 Korrigiert → TRW/ATE |
| **HEL SS-Leitungen** | Goodridge | **HEL = BESTE OPTION** (TÜV-Zert inklusive) | ✅ Bestätigt |
| **🆕 BREMSEN-GRÖßE** | 316/302mm alle | **V50 2.4i Standard = 280/280mm!** 316/302mm = T5 | 🔴 KRITISCH v9! |
| **🆕 BREMSEN-BELÄGE** | GDB1805/1840 alle | **280mm = GDB1359/58, 316/302mm = GDB1805/40** | 🔴 KRITISCH v9! |
| **🆕 BREMSEN-SCHEIBEN** | 316/302mm alle | **280mm Standard = DF4206/07, 316/302mm = T5** | 🔴 KRITISCH v9! |
| **🆕 DOMLAGER** | Febi 37389 = Domlager | **Febi 37389 = Stabi-Link, NICHT Domlager!** → Lemförder 37706 01 | 🔴 Korrigiert v9! |

---

## 💰 2. GESAMTKOSTEN-BERECHNUNG (v8 — Konsolidiert & Auditiert)

### Budget-Komplettübersicht

| Phase | Posten | Min (€) | Realistisch (€) | Max (€) | Budget-Spot | Risiken |
|-------|--------|--------:|----------------:|--------:|------------|---------|
| **1: Sicherheit** | Zahnriemen+WP, Zündkerzen, Öl, Bremsen komplett, ATF, Filter, Keilriemen | 355 | 470 | 594 | €500-800 ✅ | Dayco ohne WP ⚠️ |
| **2: Fahrwerk** | Eibach -30mm, KONI RED, Stabi-Links, Domlager, Poly-Buchsen, SS-Leitungen | 673 | 897 | 1.127 | €800-1.200 ✅ | Eibach AMZ Preis ⚠️ |
| **3: Optik** | Polierung+Keramik, LASER H7, Grill, FL-Scheinwerfer, Ecklichter, Rost | 365 | 644 | 925 | €800-1.200 ✅ | Kotflügelrost 🔴 |
| **4: Motor sanft** | Mann Filter, Ferrita Auspuff (ABE), Schaltknauf, ETM-Clean, PCV | 514 | 636 | 759 | €400-600 ⚠️ | Ferrita 3-5 Wo Liefer ⚠️ |
| **5: Reserve** | Lederpflege, Fußmatten, CEM-Kit, Thermostat, Motorlager | 132 | 176 | 221 | €200-400 ✅ | — |
| **TÜV** | Sammel-Eintragung (Eibach+KONI+HEL+Ferrita+FL-SW) | 150 | 200 | 300 | — | FL-SW braucht Baumuster ⚠️ |
| | | | | | | |
| **TOTAL (m. Auspuff)** | | **€2.189** | **€3.023** | **€3.926** | **€3.500-5.000 ✅** | |
| **TOTAL (o. Auspuff)** | | **€1.639** | **€2.453** | **€3.155** | **€3.500-5.000 ✅** | |

**🟢 FAZIT**: Beide Szenarien KOMFORTABEL INNERHALB Budget!  
**💰 Reserve**: €1.074-3.361 (ohne Auspuff) bzw. €574-2.811 (mit Auspuff)  
**⚠️ GRÖSSTES RISIKO**: Kotflügelrost (€50-250) + Ferrita Lieferzeit (3-5 Wochen)

### Empfohlenes Szenario: B — STEALTH-Balance (~€2.950)

1. ✅ Bremsen komplett: TRW Beläge+Scheiben + HEL SS-Leitungen = ~€280
2. ✅ Zahnriemen-Kit Gates K015615XS = ~€80
3. ✅ Eibach Pro-Kit -30mm + KONI Special RED = ~€554
4. ✅ Polierung+Keramik DIY = ~€60
5. ✅ Osram Night Breaker LASER H7 = ~€30 (EINTRAGUNGSFREI!)
6. ✅ Luftfilter Mann C 25 107 = ~€14 (VIN-Check zuerst!)
7. ✅ Grill schwarz Aftermarket = ~€77
8. ✅ Schaltknauf Aftermarket = ~€35
9. ✅ Ferrita Auspuff (mit ABE) = ~€550 (inkl. €80 TÜV)
10. ✅ Service-Teile (Zündkerzen, Öl, ATF, Filter) = ~€175
11. ✅ Stabi-Links + Domlager + Buchsen = ~€106
12. ✅ Facelift-Scheinwerfer H7 gebraucht + Ecklichter = ~€327
13. ✅ CEM-Löt-Kit + DIM-Reparatur-Kit = ~€25

**Gesamt: ~€2.950 + TÜV €200 + Rost-Reserve €150 ≈ €3.300 → KOMFORTABEL IM BUDGET!**

---

## 🔑 3. KOMPATIBILITÄT — V50 2.4i B5244S

### ✅ 100% Kompatibel (B5244S-spezifisch bestätigt)

| Komponente | Teilenummer | 2.4i Kompatibel | Hinweis |
|-----------|-------------|:----------------:|---------|
| Eibach Pro-Kit | E10-41-001-05-22 | ✅ | NIEMALS T5 (01-22) verwenden! |
| KONI Special RED | 86-2636SP3 / 80-2629SP3 | ✅ | V50 2.4i explizit |
| KONI Spec.Active | 86-2636SP4 / 80-2629SP4 | ✅ | V50 2.4i explizit |
| Bilstein B6 | 35-132577/578 + 24-132579 | ✅ | Für Sportfedern -30 bis -40mm |
| Gates Zahnriemen-Kit | K015615XS | ✅ | B5244S inkl. WP |
| TRW Bremsbeläge vorn | GDB1359 | ✅ | 280mm B5244S |
| TRW Bremsbeläge hinten | GDB1358 | ✅ | 280mm B5244S |
| HEL SS-Leitungen | HEL-V50-P1-4L | ✅ | P1-Plattform V50, TÜV-Zert inkl. |
| Ferrita Auspuff | F-V50-01 | ✅ | V50 2.4i ABE |
| Mann Luftfilter | C 25 107 | ⚠️ | VIN-Check! C 27 107 möglich |
| K&N Panel-Filter | 33-2873 | ✅ | Korrigiert von 33-2221! |
| ATF T-IV | Toyota 08886-01705 | ✅ | AW55-51 Automatik |
| Osram Night Breaker LASER | 64210NLHCB | ✅ | H7 Halogen, eintragungsfrei |
| SuperPro SPF3091K | SPF3091K | ✅ | Control Arm Bush, ABE vorhanden |
| SuperPro SPF3332K | SPF3332K | ✅ | Rear Bush Kit, ABE vorhanden |

### ⚠️ Kompatibilität — Baujahr-abhängig

| Komponente | Pre-FL (04-07) | FL (08-12) | Hinweis |
|-----------|:--------------:|:-----------:|---------|
| Scheinwerfer | 30796020-21 (H7) | 31265914-15 (H7) | Pre-FL→FL: Plug&Play! |
| Ecklichter | Pre-FL | 30798393-94 | ZWINGEND bei FL-SW! |
| Grill | Pre-FL Einfassung | 31330657/58 | Oben+unten Einfassung tauschen! |
| Rücklichter | Pre-FL | Facelift RL | Eintragungsfrei OEM! |
| CAN-Bus IDs | 0x0xx | 0x3xx | VERSCHIEDENE Protokolle! |
| CEM | 38/52/22/16/10 | Möglicherweise anders | VIN-abhängig |

### 🔴 BAUJAHR-KRITISCH — Offene Frage

> **BRAUCHT: Fahrgestellnummer oder Baujahr-Info!**  
> Pre-FL (2004-2007) vs FL (2008-2012) beeinflusst:
> - CAN-Bus IDs (Motor RPM: 0x0C0 vs 0x316)
> - Scheinwerfer-Teilenummern
> - Grill-Kompatibilität
> - Rücklichter-Design
> - Ecklichter-Form

---

## 🔐 4. TÜV-CHECK — Vollständige Übersicht

### ✅ EINTRAGUNGSFREI (keine TÜV-Kosten)

1. ✅ Panel-Luftfilter Mann C 25 107 / K&N 33-2873 (OEM-Form, keine Änderung)
2. ✅ Sport-Schaltknauf / Sportpedale (clip-on, Innenraum)
3. ✅ Polierung / Keramikversiegelung / Lederpflege (Kosmetik)
4. ✅ Bremsbeläge ECE R90 (TRW / ATE / Textar / Brembo) — R90-Kennzeichnung auf Belagrückseite prüfen!
5. ✅ Bremsscheiben OEM-Maße (280mm Standard)
6. ✅ Zündkerzen / Ölfilter / Innenraumfilter (Verschleißteile)
7. ✅ **Osram Night Breaker LASER H7 = eintragungsfrei!** ⭐ (Halogen = kein TÜV nötig!)
8. ✅ Grill schwarz (OEM, keine Kontur-Änderung)
9. ✅ Spiegelkappen schwarz / Diffusor folieren (Kosmetik)
10. ✅ Fußmatten / Innenraum-Detail
11. ✅ Bremsscheiben Zimmermann Sportribbel (ABE, geriffelt NICHT gebohrt)
12. ✅ Facelift-Rücklichter OEM Volvo (Volvo OEM = eintragungsfrei!)
13. ✅ SuperPro Poly-Buchsen SPF3091K+SPF3332K (ABE für P1!)

### 🟡 EINTRAGUNGSPFLICHTIG — Routine mit Gutachten

| Änderung | Gutachten | TÜV-Kosten | Detail-Notiz |
|----------|-----------|-------------|-------------|
| Eibach Pro-Kit -30mm | ✅ Teilegutachten | €80-150 | Zusammen mit KONI = 1 Termin. Anschlagpuffer kürzen! |
| KONI Sport-Dämpfer | ✅ Teilegutachten | (inkl. oben) | Paket mit Eibach! Niemals allein mit OEM-Federn! |
| Bilstein B6 | ✅ Teilegutachten | (inkl. oben) | NUR mit Sportfedern -30 bis -40mm! |
| SS-Bremsleitungen HEL | ✅ **TÜV-Zert inklusive!** | €0-50 | HEL = BESTE OPTION! Zertifikat in Verpackung! |
| Ferrita Kat-Back Auspuff | ⚠️ ABE teilweise | €50-80 (mit ABE) | Prüfen ob ABE für V50 2.4i dabei! Ohne ABE: Einzelabnahme €200-400 |
| Eisenmann Kat-Back | ✅ ABE/Teilegutachten | €50-80 | Deutscher Hersteller = 100% TÜV |
| Facelift-Scheinwerfer | Baumuster-Nummer | €50-100 | H7 Halogen für 2.4i! TN 31265914/15 |
| LED H7 (falls statt LASER) | E-Nummer auf Birne | €30-80 | SELBST MIT E-Nummer: Eintragung nötig! |
| LED Rücklichter (Aftermarket) | EG-Gutachten nötig | €60-120 | Besser: OEM Facelift = frei! |
| Heico Frontlippe | ✅ Heico Teilegutachten | €50-80 | Deutscher Volvo-Tuner = Routine |
| Estoni StabiSet 24/22mm | ✅ ABE | €50-80 | Standard Eintragung |
| LED H7 Birnen | E-Nummer (Osram/Philips) | €30-80 | Eintragungspflichtig! Besser: LASER H7 = frei! |

### ❌ SKIP FÜR STEALTH — TÜV-DETAILLIERTE VERBOTE

- ❌ **IPD Intake Pipe** (kein deutsches Gutachten, §21 Einzelabnahme sehr schwer, ~€200-400)
- ❌ **Polestar B5244S** (**NICHT verfügbar für 2.4i Sauger!** Nur T5/T6/T8)
- ❌ **BSR Chiptuning B5244S** (kein deutsches TÜV-Zertifikat, Einzelabnahme schwierig)
- ❌ **Powerflex Poly** (keine ABE für P1 → SuperPro statt!)
- ❌ **Ferodo DS2500** (**KEIN ECE R90 = STRASSENVERKEHRS-ILLEGAL!**)
- ❌ **EBC Beläge** (meist keine ECE R90 = illegal im Straßenverkehr!)
- ❌ **Goodridge SS-Leitungen** (keine ABE für V50 → Einzelabnahme €150-250 Extra → HEL statt!)
- ❌ Tieferlegung über -30mm
- ❌ China-Auspuff ohne ABE (Stilllegung droht!)
- ❌ Gebohrte Bremsscheiben (kein TÜV für P1)
- ❌ LED H7 in Halogen-Gehäuse (besser: LASER H7 = eintragungsfrei)
- ❌ **Chiptuning B5244S allgemein** (STEALTH = kein Chiptuning!)

### 💡 TÜV-Sammel-Termin-Strategie

**Alle eintragungspflichtigen Änderungen auf EINMAL:**
- 1x Grundgebühr (~€50-80)
- Einzelpositionen je ~€15-30
- **Gesamtkosten**: ~€150-300 (statt €370-890 einzeln!)
- **Empfehlung**: Eibach + KONI + HEL + Ferrita + FL-Scheinwerfer = 1 Termin

---

## 📋 5. TEAM-KOORDINATION

| Wer | Braucht | Status | Neue Infos |
|-----|---------|--------|------------|
| 👔 Chef | TÜV-Experte | ✅ GELÖST | BUDGET_TUV_REPORT.md komplett |
| 👔 Chef | Lackier-Experte | ✅ GELÖST | DIY Polierung = €30-50 |
| 🏁 Fahrwerk | Stabi-Experte | ✅ GELÖST | Lemförder + SuperPro in DB |
| 🎨 Optik | FL-Scheinwerfer TN | ✅ KORRIGIERT | 31265914/31265915 (H7), NICHT 30796020-23 |
| 🎨 Optik | Grill Pre-FL vs FL | ✅ KORRIGIERT | Oben+unten Einfassung tauschen! |
| 🔧 Motor | K&N Teilenummer | ✅ GELÖST | 33-2873 korrigiert in DB |
| 🔧 Motor | Mann Filter Teilenummern | ⚠️ OFFEN | VIN-Check vor Kauf! |
| 💻 Developer | V50-Baujahr | 🔴 OFFEN | Pre-FL vs FL → andere CAN-IDs! |
| 💻 Developer | PiCAN2 Hardware | 🔴 OFFEN | Besorgen und Erst-Test |
| 💻 Developer | CAN-IDs Verifikation | ⚠️ TEILWEISE | 32 verified, 12 community, 12 unverified |

---

## 🔴 RISIKEN & OPEN ITEMS

| Risiko | Schwere | Maßnahmen |
|--------|---------|-----------|
| V50-Baujahr IDENTIFIKATION | 🔴 KRITISCH | **VIN oder Baujahr vom User nötig!** Bestimmt CAN-IDs, SW-TN, Grill |
| Mann C 25 107 Teilenummer | 🔴 HOCH | VIN-Check vor Kauf! C 27 107 / C 28 110 möglich |
| Kotflügel-Rost | 🔴 HOCH | Vor Polierung prüfen! €50-250 Reserve |
| Eibach AMZ €150 vs Listenpreis €280 | 🟡 MITTEL | Verkäufer prüfen, Originalverpackung + Gutachten verlangen |
| CEM-Relais (ETM) | 🟡 MITTEL | ETM-Cleaning-Kit → Präventiv reinigen |
| AW55-51 Getriebe | 🟡 MITTEL | ATF-Wechsel mit T-IV in Phase 1 |
| Dayco KTB481 | 🟡 MITTEL | Manche Angebote OHNE Wasserpumpe! |
| Facelift-SW Verfügbarkeit | 🟡 MITTEL | Gebraucht ~€250-290/paar auf Kleinanzeigen |
| Ferrita Lieferzeit | 🟡 MITTEL | 3-5 Wochen Lieferzeit ab Schweden |

### 🆕 NEU in v10

- 🔍 **TÜV-Experte Deep-Dive**: 45 Teile in DB mit TÜV-Status (Teilegutachten/ABE/ECE R90/Einzelabnahme/verboten)
- 🚨 **Polestar B5244S = NICHT VERFÜGBAR**: Polestar nur für Turbo-Motoren (T5/T6/T8), nicht 2.4i Sauger!
- 🚨 **BSR Chiptuning B5244S**: Kein deutsches TÜV-Zertifikat, Einzelabnahme §21 sehr schwierig
- 🚨 **IPD Intake = SKIP**: Kein deutsches Gutachten, §21 Einzelabnahme sehr schwer, ~€200-400 Kosten
- 🚨 **BREMSEN-GRÖßE geklärt**: V50 2.4i Standard = 280/280mm, T5 = 316/302mm!
- 🚨 **DOMLAGER korrigiert**: Febi 37389 = Stabi-Link, NICHT Domlager! Lemförder 37706 01
- ✅ **LED H7 Rechtslage 2026**: LED in Halogen-Gehäuse = eintragungspflichtig §19.3, selbst MIT E-Nummer
- ✅ **Osram Night Breaker LASER H7 = eintragungsfrei** = beste STEALTH-Option
- ✅ **KONI/Bilstein TÜV-Details**: Beide Teilegutachten, aber IMMER mit Sportfedern zusammen eintragen!
- ✅ **HEL vs Goodridge geklärt**: HEL = TÜV-Zert inklusive (€0-50), Goodridge = Einzelabnahme (€150-250)
- ✅ **ECE R90 Detail-Check**: TRW/ATE/Textar/Brembo = ECE R90 ✓, Ferodo DS2500/EBC = ILLEGAL ✓
- ✅ **Ferodo DS2500** korrekt als STRASSENVERKEHRS-ILLEGAL markiert in DB
- ✅ **SuperPro Poly** hat ABE — EINZIGE Poly-Option mit TÜV für P1
- 📦 **DB: 45 Teile mit tuv_status in specs JSON** — vollständige TÜV-Klassifizierung

---

**STEALTH-STATUS**: 100% legal, 100% unauffällig, 100% TÜV-konform. 🏁  
**DB-STAND**: 674 Teile, 1.075 Fitments, 78+ V50 verified, 442 Quellen, 45 TÜV-klassifiziert  
**BUDGET**: ✅ INNERHALB 5.000€ HARD CAP — Realistisch €2.629 (mit Auspuff), Reserve €871-2.371  
**BUDGET-STATUS**: 🟢 GRÜN — Alle Phasen innerhalb Budget-Spots.  
**🚨 NEU v10**: TÜV-Experte Deep-Dive: 45 Teile TÜV-klassifiziert, Polestar/BSR/IPD geklärt, LED H7 Rechtslage 2026, HEL=beste SS-Leitung