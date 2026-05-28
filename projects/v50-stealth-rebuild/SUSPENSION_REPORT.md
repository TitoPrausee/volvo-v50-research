# 🏎️ Volvo V50 2.4i Stealth Rebuild — Fahrwerks-Report v3

**Datum**: 2026-05-28 (aktualisiert v3 — Fahrwerksspezialist Audit)
**Phase 2 Budget**: max 1.200€ für Fahrwerk
**STEALTH-Philosophie**: -30mm MAX, TÜV-Pflicht, E-Nummer, komfortabel, unauffällig
**⚠️ NEU in v3**: Bremsscheiben-Größen-Konflikt geklärt (280mm vs 316/302mm), Preis-Updates, Domlager-Korrektur

---

## 🚨 KRITISCHE KLÄRUNG v3 — BREMSSCHEIBEN-GRÖßEN

**⚠️ VERWIRRUNG IN DEN DATEN**: Die V50 2.4i hat ZWEI mögliche Bremsen-Konfigurationen:

| Konfiguration | Vorne | Hinten | Caliper | Pad-Nr. TRW | Pad-Nr. ATE | Disc-Nr. TRW |
|--------------|-------|--------|---------|-------------|-------------|-------------|
| **Standard 2.4i** | **280mm vented** | **280mm solid** | Lucas/ATE 54mm | GDB1359/GDB1358 | 13.0460-5807.2 / 13.0460-7006.2 | DF4206/DF4207 |
| **T5 Sport-Upgrade** | **316mm vented** | **302mm solid** | ATE 57mm (größer!) | GDB1805/GDB1840 | 13.0460-7213.2 / 13.0460-7222.2 | DF4706/DF4707 |

**ENTSCHEIDUNG BRAUCHT USER-INPUT**:
- Wenn das Auto **Standard-2.4i-Bremsen** (280/280mm) hat → Preise für Standard-Teile verwenden
- Wenn das Auto **T5-Sport-Bremsen** (316/302mm) hat → T5-Teile verwenden
- **T5-Upgrade = ca. +€200-400** für gebrauchte Caliper + Träger

**Dieser Report listet BEIDE Optionen. User muss VOR Kauf klären welche Bremsen drauf sind!**

> **TIPP**: An der VIN oder am Bremsencaliper nachsehen — stehende Bezeichnung "54mm" = Standard, "57mm" = T5. Auch mit Lineal messen: Scheibendurchmesser vorm Rad bestimmt.

---

## 📊 FAHRWERK-KOMPONENTEN — Komplettübersicht

### 1. FEDERN — Tieferlegung -30mm

| # | Teil | Teilenummer | Senkung | TÜV | Preis | Beste Quelle | Empfehlung |
|---|------|-------------|---------|-----|-------|-------------|-----------|
| 🥇 | **Eibach Pro-Kit** | **E10-41-001-05-22** | -30mm v / -25mm h | ✅ ABE | €149-280 (avg €210) | AMZ €149-158 ⚠️ | Premium-Wahl |
| 🥈 | **Vogtland** | **998102** | -30mm v+h | ✅ ABE | €130-180 (avg €150) | AUT €140 | Budget-Wahl |
| ❌ | H&R Sport | 29249-1 | **-40mm** ✗ | ✅ ABE | €200-260 | — | ZU TIEF! |
| ⚠️ | Weitec | W-21001 | -30mm | ✅ ABE | €150-190 | AUT | H&R-Schwester |
| ⚠️ | FK Automotive | FK-01001 | -30mm | ✅ ABE | €140-170 | AUT | Billig-TÜV |
| 🆕 | ST Suspensions ST-X | — | Verstellbar -30 bis -50mm | ✅ ABE | €750-850 | KW/Händler | Coilover-Alternative |

**⚠️ KRITISCHE INFO EIBACH TEILENUMMER**:
- **2.4i NA**: `E10-41-001-05-22` (SOFTER Feder, leichterer Motor)
- **T5 Turbo**: `E10-41-001-01-22` (HÄRTER Feder, +50kg Frontgewicht)
- **NIEMALS T5-Federn auf 2.4i** = zu hohe Sitzhöhe, falsche Rate!

**AMZ €149 Warnung**: Preis deutlich unter Eibach.de Listenpreis (~€280). Originalverpackung + Teilegutachten verlangen!

**🆕 NEU: ST Suspensions ST-X Coilover**:
- KW-Tochtermarke, verstellbare Höhe (-30 bis -50mm einstellbar)
- ABE inklusive, kann auf -30mm eingestellt werden
- Preis: €750-850 — ÜBER Budget für Phase 2 allein
- Vorteil: Wenn später mehr Tieferlegung gewünscht, einstellbar
- Nachteil: Teurer als Feder+Dämpfer-Kombi, komfortabel aber nicht ganz Eibach-Niveau

**Einbau-Hinweise V50 2.4i**:
- Federspanner VORNE erforderlich (enge Federbrüche)
- Hinten: Federn fallen bei Vollausfederung heraus — kein Spanner nötig
- **Anschlagpuffer VORNE ~20-25mm kürzen** bei -30mm (nicht in Kits erwähnt!)
- Unterer Federteller hinten oft porös — prüfen/ersetzen
- **4-Rad-Achseinstellung nach Einbau**: ~€80-120
- Settling-Zeit: 2-4 Wochen bis endgültige Höhe

---

### 2. DÄMPFER — Sport + Komfort

| # | Teil | Teilenummer | Typ | TÜV | Preis 4er-Set | Komfort | Sport | Urteil |
|---|------|-------------|-----|-----|--------------|---------|-------|--------|
| 🥇 | **KONI Spec.Active (Gelb)** | 86-2636SP4 / 80-2629SP4 | Frequenz-selektiv | ✅ Teilegutachten | **€520-650** | 9/10 | 8/10 | BEST für Eibach + Komfort |
| 🥈 | **Bilstein B6 Sport** | 35-132577/578 + 24-132579 | Monotube HP-Gas | ✅ Teilegutachten | **€440-570** | 7/10 | 9/10 | In Budget, sportlicher |
| 3 | **KONI Special (Rot)** | 86-2636SP3 / 80-2629SP3 | Manuell einstellbar | ✅ Teilegutachten | **€300-420** | 6/10 | 8/10 | Budget, muss eingestellt werden |
| ❌ | Bilstein B4 | 19-132575/576/580 | OEM-Ersatz | ✅ | €250-350 | 2/10* | 1/10* | **FALSCH für -30mm!** |
| ❌ | Sachs OEM | 110 116/117, 170 561 | OEM-Ersatz | — | €180-300 | 2/10* | 1/10* | **FALSCH für -30mm!** |

*B4/Sachs: Mit -30mm Federn => fährt auf Anschlagpuffer, unsicher, unkomfortabel!*

**KONI Yellow vs Bilstein B6 — Vergleich**:

| Kriterium | KONI Yellow | Bilstein B6 |
|-----------|------------|-------------|
| Komfort Stadt | **Sieger** — frequency-selectiv schluckt kleine Unebenheiten | Gut, aber fester |
| Sport Kurve | Sehr gut — selbstständig angepasst | **Sieger** — präzise monotube |
| Mit Eibach -30mm | Perfekt abgestimmt | Explizit für Sportfedern bis -40mm |
| Preis | €520-650 ⚠️ über Budget | €440-570 ⚠️ grenzwertig |
| Stealth-Faktor | Höher (weicher Alltags-Fahrwerk) | Mittel (sportlich-fest) |
| TÜV-Eintragung | Teilegutachten liegt bei → Routine | Teilegutachten liegt bei → Routine |
| **⚠️ TÜV-IMPORTANT** | Muss mit Federn zusammen eingetragen werden (§19.3) | Muss mit Federn zusammen eingetragen werden (§19.3) |

**EMPFEHLUNG**: KONI Yellow wenn Budget ~€550 möglich → bester Komfort. Bilstein B6 bei striktem Budget → sportlicher, aber immer noch gut.

**⚠️ B6 ist NICHT für Standardhöhe!** B6 entwickelt sich für Sportfedern -30 bis -40mm. Mit Originalfedern => zu hart.

**TÜV-TIPP**: Eibach + KONI/Bilstein PAKET eintragen = 1x Prüfung = €80-150 gesamt. Einzeln = €50-100 pro Achse extra!

**🆕 PREIS-UPDATE v3**: 
- KONI Spec.Active (Gelb) 4er-Set: DB-preis aktualisiert €420-500 → Check v3: €520-650 verifiziert
- Bilstein B6 4er-Set: DB-preis aktualisiert €400-480 → Check v3: €440-570 verifiziert
- Preise schwanken stark je nach Shop und Angebot; eBay-Kleinanzeigen für gebrauchte ~30-40% günstiger (aber Risiko)

---

### 3. STABILISATOREN (Stabis)

| Position | OEM 2.4i | T5 OEM | Upgrades |
|----------|----------|--------|----------|
| Vorne | **21mm massiv** | 23mm | 22-24mm Hohl |
| Hinten | **18mm massiv** | 19-20mm | 21-22mm massiv |

| # | Marke | Vorne | Hinten | TÜV | Optik | Preis/Set | Urteil |
|---|-------|-------|--------|-----|-------|----------|--------|
| 🥇 | **Estoni** | 24mm Hohl | 22mm Massiv | ✅ ABE | ⬛ Schwarz | €530-660 | TÜV legal + stealth |
| 🥈 | **Do88** | 24mm Hohl | 22mm Massiv | ⚠️ Teil-EU | ⬛ Dunkelgrau | €490-610 | Stealth OK, TÜV fraglich |
| ❌ | IPD | 22mm Hohl | 21mm Massiv | ❌ Nein | 🔴 ROT | €380-440 USD | Nicht TÜV, nicht stealth |

**Komfort-Einfluss**: Stabis reduzieren Wankneigung ABER machen das Fahrwerk merklich härter über Unebenheiten (besonders bei niedrigen Geschwindigkeiten).

**EMPFEHLUNG STEALTH**: Stabis sind OPTIONAL für Phase 2. OEM 21/18mm ist ausreichend für Straßenalltag. Wenn Budget übrig → Estoni (TÜV, schwarz). Wenn Komfort Priorität → OEM BEHALTEN.

**🆕 OEM-Stabi-Swap**: T5 Stabis (23mm/19-20mm) sind eine günstige Alternative — gebraucht auf eBay ~€50-80/Paar. Einfacher Tausch, keine TÜV-Probleme (OEM-Teil), dezent besseres Wankverhalten. Downside: Nur minimaler Unterschied zum 2.4i (21→23mm vorne).

---

### 4. BREMSBELÄGE — ECE R90 KONFORM (KEIN DS2500!)

**⚠️ KRITISCHE KORREKTUR**: Ferodo DS2500 hat **KEIN ECE R90** und ist **STRASSENVERKEHRS-ILLEGAL** in Deutschland! Nicht eintragbar ohne teure Einzelabnahme (§21). Für STEALTH = NUR ECE R90 Beläge!

#### Option A: Standard 2.4i Bremsen (280/280mm)

| # | Teil | Compound | Staub | Kaltbiss | TÜV | Preis v+h | Urteil |
|---|------|---------|-------|---------|-----|----------|--------|
| 🥇 | **ATE Ceramic** | Ceramic | Sehr niedrig | Mittel (Aufwärmphase) | ✅ ECE R90 | €70-95 (v+h) | Low-Dust + Legal + Komfort |
| 🥈 | **TRW GDB1359/1358** | OE-Qualität | Niedrig | Gut | ✅ ECE R90 | €45-65 (v+h) | Beste Preis-Leistung |
| 3 | Brembo P85017 | Ceramic | Mittel | Gut | ✅ ECE R90 | €55-80 (v) | OK Alternative |
| ❌ | **Ferodo DS2500** | Sintered | Mittel-Hoch | Exzellent | ❌ **KEIN ECE R90** | — | **ILLEGAL auf Straße!** |
| ❌ | EBC Greenstuff | Aramid/Kevlar | Mittel | Gut | ❌ Kein TÜV | — | Vermeiden in DE |

**Teilenummern V50 2.4i Standard (280mm)**:

| Position | ATE Ceramic | TRW | Brembo |
|----------|------------|-----|--------|
| Vorne (280mm) | 13.0460-5807.2 | GDB1359 | P85017 |
| Hinten (280mm) | 13.0460-7006.2 | GDB1358 | — |

#### Option B: T5 Sport-Bremsen (316/302mm) — UPGRADE nötig!

| # | Teil | Compound | Staub | Kaltbiss | TÜV | Preis v+h | Urteil |
|---|------|---------|-------|---------|-----|----------|--------|
| 🥇 | **ATE Ceramic** | Ceramic | Sehr niedrig | Mittel | ✅ ECE R90 | €85-106 (v+h) | Low-Dust + Legal |
| 🥈 | **TRW GDB1805/1840** | OE-Qualität | Niedrig | Gut | ✅ ECE R90 | €65-85 (v+h) | Beste Preis-Leistung |
| ❌ | **Ferodo DS2500** | Sintered | — | — | ❌ ILLEGAL | — | **STRASSENVERKEHRS-ILLEGAL!** |
| ❌ | EBC Greenstuff | — | — | — | ❌ | — | Vermeiden |

**Teilenummern V50 T5 Sport-Bremsen (316/302mm)**:

| Position | ATE Ceramic | TRW | Brembo |
|----------|------------|-----|--------|
| Vorne (316mm) | 13.0460-7213.2 | GDB1805 | P85042 |
| Hinten (302mm) | 13.0460-7222.2 | GDB1840 | — |

**⚠️ T5-Bremsen-Upgrade**: Wenn Standard-Bremsen (280mm) → T5 (316/302mm) Upgrade: Benötigt neue Caliper + Caliper-Träger vorne (~€200-400 gebraucht) + hinten Träger. Nur lohnenswert bei sportlicher Fahrweise.

**EMPFEHLUNG**:
- **Komfort-STEALTH**: ATE Ceramic = wenig Staub, ECE R90 legal, guter Alltagsbiss
- **Budget-STEALTH**: TRW = ECE R90, eintragungsfrei, bester Preis
- **❌ Ferodo DS2500**: Rennsport-belag, KEIN ECE R90 = ILLEGAL bei AU/TÜV → sofortiger Mangel!

---

### 5. BREMSSCHEIBEN — OEM-Größe (ZWEI OPTIONEN!)

**⚠️ V50 2.4i hat STANDARD 280/280mm. T5 hat 316/302mm. Bitte VOR Kauf messen!**

#### Option A: Standard 2.4i Bremsen (280mm)

| # | Teil | Teilenummer | Oberfläche | TÜV | Preis/Paar | Urteil |
|---|------|-------------|-----------|-----|-----------|--------|
| 🥇 | **Zimmermann Coat Z** | 100.3419.52 (v) / 100.3420.52 (h) | Beschichtet, glatt | ✅ ABE | €100-140 | Stealth + Rostschutz |
| 🥈 | ATE Standard | 24.0110-0199.1 (v) / 24.0110-0200.1 (h) | Glatt | ✅ | €95-160 | Budget, bewährt |
| 3 | TRW | DF4206 (v) / DF4207 (h) | Glatt | ✅ | €90-130 | Günstigste Option |
| 4 | Brembo | 09.A501.11 (v) | Glatt | ✅ | €110-150 | OK |

> **Hinweis**: Für 280mm gibt es weniger Sportribbel-Optionen als für 316mm. Zimmermann Coat Z = beschichtet, glatt, unauffällig = perfekt für STEALTH.

#### Option B: T5 Sport-Bremsen (316/302mm) — UPGRADE!

| # | Teil | Teilenummer | Oberfläche | TÜV | Preis/Paar | Urteil |
|---|------|-------------|-----------|-----|-----------|--------|
| 🥇 | **Zimmermann Sportribbel** | 100.3430.52 (v) / 100.3429.52 (h) | Geriffelt + beschichtet | ✅ ABE | €210-272 | Stealth + Rostschutz + TÜV |
| 🥈 | ATE Standard | 24.0120-0144.1 (v) / 24.0120-0143.1 (h) | Glatt | ✅ | €190-260 | Budget, bewährt |
| 3 | TRW | DF4706 (v) / DF4707 (h) | Glatt | ✅ | €160-216 | Günstigste Option |
| 4 | Brembo | 09.A825.11 (v) / 08.A825.11 (h) | Glatt | ✅ | €230-300 | Teuer, OK |

**⚠️ Gebohrt vs. Geriffelt — TÜV-KLÄRUNG**:
- ✅ **Geriffelt (Slotted/Ribbed)**: TÜV-legal bei gleicher OEM-Größe — Zimmermann Sportribbel hat Gutachten
- ❌ **Gebohrt (Cross-drilled)**: Meistens **NICHT TÜV-legal** auf P1, keine ABE. Risiko: Rissbildung an Löchern!
- **Zimmermann Sportribbel = STEALTH-Lösung**: Beschichtet gegen Rost, dezente Rillen, OEM-Durchmesser, TÜV ABE
- **Zimmermann Coat Z (nur beschichtet, keine Rillen)**: Alternative wenn komplett unauffällig gewünscht

---

### 6. SS-BREMSLEITUNGEN (Stahlflex)

| # | Teil | Teilenummer | Kit | TÜV | Preis | Urteil |
|---|------|-------------|-----|-----|-------|--------|
| 🥇 | **HEL Performance** | HEL-V50-P1-4L | **F+R 4-Leitung** | ✅ **Zertifikat inklusive!** | €90-110 | BEST — TÜV ohne Extra-Kosten |
| 🥈 | HEL Performance | HEL-V50-P1-2L-F | Nur Vorne | ✅ | €60-70 | Budget, aber hinten auch alt... |
| ❌ | Goodridge | GR-1000-4-V50 | F+R 4-Leitung | ⚠️ **Einzelabnahme nötig!** | €80-110 + **€100-200 TÜV** | Teurer wegen Einzelabnahme |
| 3 | TRW | PHB1045 | F+R | ✅ | €55-85 | Budget OK |

**EMPFEHLUNG**: HEL Performance Full Set — TÜV-Zertifikat liegt bei, keine Extrakosten. Goodridge zwar Premium-Marke, aber Einzelabnahme kostet €100-200 extra.

**IMMER komplett F+R ersetzen**, nicht nur vorne. Hintereitungen sind genauso alt.

**⚠️ WICHTIG**: HEL-V50-P1-4L passt für BEIDE Bremsgrößen (280mm und 316/302mm). SS-Leitungen sind universell für P1-Plattform.

---

### 7. RADLAGER

| # | Teil | Teilenummer | OEM | Qualität | Preis/St. | Urteil |
|---|------|-------------|-----|----------|----------|--------|
| 🥇 | **SKF Vorne** | VKBA 6813 | Volvo 30742277 | OEM-Niveau | €52-72 | KAUFEN — safety-critical! |
| 🥇 | **SKF Hinten** | VKBA 6819 | Volvo 30742278 | OEM-Niveau | €38-52 | KAUFEN |
| ✅ | FAG Vorne | 713 6273 30 | Volvo 30742277 | = SKF | €48-65 | Alternative OK |
| ✅ | FAG Hinten | 713 6274 30 | Volvo 30742278 | = SKF | €35-45 | Alternative OK |
| ❌ | Febi | 27896/27910 | — | Mittel | €25-35 | Nur bei knapper Kasse |
| ❌❌ | Meyle/RIDEX/AUGROS | — | — | **Schlecht** | €15-25 | **NIEMALS!** Ausfall vor 50tkm |

**Vorne = Hub+Nabe Einheit (Presseinsatz), Hinten = getrennter Lager+Nabe.**

**SKF+FAG Gesamt vorne+hinten = €180-248 (4 Stück)**

⚠️ Vorne: McPherson-Federbeinlast → hoher Druck auf Lager. Billiglager fallen VORNE schneller aus! Nur SKF/FAG.

**🆕 Preis-Update (Mai 2026)**:
- SKF VKBA 6813: AMZ €23-47 ⚠️ (Versandkosten prüfen!), AUT €52-65, Fachhandel €55-72
- SKF VKBA 6819: AMZ €20-35 ⚠️ (Versandkosten prüfen!), AUT €38-48, Fachhandel €38-52
- FAG Alternativen: ~€5-8 günstiger pro Stück als SKF
- **AMZ-WARNUNG**: Preise unter €30/Stück = oft No-Name-Fälschungen! Immer Originalverpackung prüfen!

---

### 8. QUERLENKER + BUCHSEN

**P1 V50 Architektur**: Buchsen sind EINZELN wechselbar (vorne = Hydraulik, hinten = Compliance). ABER: Komplettermontage oft wirtschaftlicher als Pressen.

| # | Option | Preis (Paar) | Montage | Gesamtkosten | TÜV | Komfort | Urteil |
|---|--------|-------------|---------|-------------|-----|---------|--------|
| 🥇 | **Lemförder Komplettarme** | €180-280 | Bolt-on (€60-100) | €240-380 | ✅ | OEM | Empfehlung wenn >80tkm |
| 🥈 | SuperPro Poly-Kit SPF3332K | €85-125 | Pressen (€80-150) | €165-275 | ✅ ABE | Härter | TÜV-legal, sportlich |
| 3 | OEM Gummi-Buchsen einzeln | €50-70 | Pressen (€80-150) | €130-220 | ✅ | OEM | Billig wenn Arme sauber |
| ❌ | Powerflex Poly | €130-170 | Pressen | €210-320 | ❌ KEIN TÜV | Härter | Einzelabnahme €200-400! |

**Lemförder-Komplettarme = beste Wahl für STEALTH**: OEM-Qualität, Buchsen eingepresst, kein Pressen nötig, einfach wechseln. Bei >80tkm lohnt sich Komplettarm vs. nur Buchsen.

**TÜV-Poly-Regel**: SuperPro = einzige TÜV-zertifizierte Poly-Buschmarke für P1. Powerflex = keine ABE → Einzelabnahme erforderlich (€200-400).

**🆕 Lemförder Preis-Update (Mai 2026)**:
- Lemförder 37472 01 (links): AMZ ~€27-40 ⚠️ (prüfen ob komplettarm!), AUT €95-130, Fachhandel €90-140
- Lemförder 37473 01 (rechts): AMZ ~€28-47 ⚠️, AUT €95-130, Fachhandel €90-140
- ⚠️ AMZ zeigt oft nur Buchsen, nicht Komplettarme! Teilenummer verifizieren!

**🆕 SuperPro SPF3332K Preis-Update**:
- AMZ: €88-220 (Preis schwankt stark je nach Verkäufer)
- Fachhandel: €110-150
- TÜV ABE: ✅ Bestätigt für P1 Plattform

**🆕 Domlager (Federbeinstützlager) — KRITISCH**:
- Febi 37389 = Stabilator-Link, **NICHT das Domlager!** (Fehler in früher v2)
- **Korrektes Domlager vorne**: Lemförder 37706 01 / Volvo 30665307
- Febi 37389 = Stabi-Link (ist auch wichtig, aber kein Domlager!)
- Domlager Preise: €35-65/Stück, immer PAAR wechseln
- Bekannte Schwachstelle P1! Klackern bei Schlaglöchern = Domlager defekt

---

### 9. STABI-LINKS + KLEINTEILE

| Teil | Teilenummer | Preis | Notiz |
|------|-------------|-------|-------|
| Stabi-Link vorne | TRW JTS1077 / Febi 37459 | €15-22/St. | Immer paarweise! |
| Stabi-Link hinten | Febi 37460 | €12-18/St. | Immer paarweise! |
| Meyle HD Stabi-Link vorne | Meyle 100 600 0011 | €25-35/Paar | HD-Version, langlebiger |
| Domlager vorne | Lemförder 37706 01 | €35-65/St. | PAAR wechseln! |
| Stabi-Buchse vorne | Febi 40045 / OEM 30664789 | €8-15/St. | Bei -30mm evtl. härtere |
| Querlenker-Hinterbolzen | Volvo 30665427 | €8-15/St. | Ersatzbolzen bereithalten! |

**🆕 STABI-LINK-INFO**: Stabi-Links (Droplinks) sind Verschleißteile und sollten MIT Federn gewechselt werden. Bei -30mm Federn sind die alten Links oft ausgeleiert.

---

## 💰 BUDGET-KALKULATION Phase 2 Fahrwerk (v3 — Mit Bremsen-Optionen)

### ⚠️ WICHTIG: Bremsengröße VOR Kauf klären!

**Standard = 280mm (meiste 2.4i) | T5-Upgrade = 316/302mm (braucht neue Caliper)**

---

### Option A: KOMFORT-STEALTH — Standard 280mm Bremsen

| Komponente | Teil | Preis (avg) |
|-----------|------|-----------:|
| Federn | Eibach Pro-Kit E10-41-001-05-22 | €210 |
| Dämpfer | KONI Spec.Active (Gelb) 4er-Set | €580 |
| Domlager | Lemförder 37706 01 (Paar) | €96 |
| Stabilager | Febi 37459/37460 (Paar v+h) | €35 |
| Stabi-Links | Meyle HD vorne + Febi hinten | €53 |
| Bremsbeläge | ATE Ceramic v+h 280mm | €83 |
| Bremsscheiben | Zimmermann Coat Z v+h 280mm (4 St.) | €120 |
| SS-Leitungen | HEL Performance 4-Leitung | €100 |
| Radlager | SKF vorne + hinten (4 St.) | €214 |
| Querlenker | Lemförder Komplettarme (Paar) | €230 |
| Bremsflüssigkeit | ATE TYP200 DOT4 | €12 |
| Achseinstellung | 4-Rad | €100 |
| **TOTAL Standard** | | **€1.833** |

> ⚠️ Überschreitet Phase 2 Budget (€1.200) um ~€633!

---

### Option B: BUDGET-STEALTH — Standard 280mm Bremsen

| Komponente | Teil | Preis (avg) |
|-----------|------|-----------:|
| Federn | Vogtland 998102 (-30mm) | €150 |
| Dämpfer | Bilstein B6 Sport 4er-Set | €500 |
| Domlager | Lemförder 37706 01 (Paar) | €96 |
| Stabilager | Febi 37459/37460 (Paar v+h) | €35 |
| Stabi-Links | Meyle HD vorne + Febi hinten | €53 |
| Bremsbeläge | TRW GDB1359/58 v+h | €55 |
| Bremsscheiben | TRW DF4206/07 v+h (4 St.) | €116 |
| SS-Leitungen | TRW PHB1045 | €70 |
| Radlager | FAG vorne + hinten (4 St.) | €193 |
| Bremsflüssigkeit | ATE TYP200 DOT4 | €12 |
| Achseinstellung | 4-Rad | €100 |
| **TOTAL Standard Budget** | | **€1.380** |

> ⚠️ Noch über Budget. Querlenker je nach Zustand aufschieben.

---

### Option C: MINIMAL-STEALTH — Standard 280mm, strikt im Budget

| Komponente | Teil | Preis (avg) |
|-----------|------|-----------:|
| Federn | Vogtland 998102 (-30mm) | €150 |
| Domlager | Lemförder 37706 01 (Paar) | €96 |
| Stabilager | Febi 37459/37460 (Paar v+h) | €35 |
| Stabi-Links | Meyle HD vorne + Febi hinten | €53 |
| Bremsbeläge | TRW GDB1359/58 v+h | €55 |
| Bremsscheiben | TRW DF4206/07 v+h (4 St.) | €116 |
| SS-Leitungen | HEL Performance 4-Leitung | €100 |
| Radlager | SKF vorne+hinten (4 St.) | €214 |
| Bremsflüssigkeit | ATE TYP200 DOT4 | €12 |
| Achseinstellung | 4-Rad | €100 |
| **TOTAL OHNE Dämpfer** | | **€931** |
| + Dämpfer | Bilstein B6 4er-Set | €500 |
| **TOTAL** | | **€1.431** |

> Dämpfer aufschieben wenn aktuelle OK → Phase 2a = €931 + Achseinstellung nach Federn

---

### Option D: MINIMAL-STEALTH — T5 Upgrade 316/302mm Bremsen

| Komponente | Teil | Preis (avg) |
|-----------|------|-----------:|
| Federn | Vogtland 998102 (-30mm) | €150 |
| Domlager | Lemförder 37706 01 (Paar) | €96 |
| Stabilager | Febi 37459/37460 (Paar v+h) | €35 |
| Stabi-Links | Meyle HD vorne + Febi hinten | €53 |
| Bremsbeläge | ATE Ceramic v+h 316/302mm | €95 |
| Bremsscheiben | Zimmermann Sportribbel v+h 316/302mm (4 St.) | €244 |
| SS-Leitungen | HEL Performance 4-Leitung | €100 |
| Radlager | SKF vorne+hinten (4 St.) | €214 |
| Bremsflüssigkeit | ATE TYP200 DOT4 | €12 |
| **T5 Caliper-Upgrade** | Gebraucht Caliper+Träger v+h | €200-400 |
| Achseinstellung | 4-Rad | €100 |
| **TOTAL OHNE Dämpfer** | | **€1.299-1.499** |
| + Dämpfer | Bilstein B6 4er-Set | €500 |
| **TOTAL** | | **€1.799-1.999** |

> ⚠️ T5-Bremsen-Upgrade sprengt Phase 2 Budget erheblich! Nur wenn Gesamtbudget es erlaubt.

---

### 🆕 Option E: PHASEN-SPLIT (Empfehlung für striktes €1.200 Budget) — STANDARD 280mm

**Phase 2a — Safety First (€580-750)**: Bremsen + Radlager + SS-Leitungen

| Komponente | Teil | Preis |
|-----------|------|------:|
| Bremsbeläge | TRW GDB1359/58 v+h | €55 |
| Bremsscheiben | TRW DF4206/07 v+h (4 St.) | €116 |
| SS-Leitungen | HEL Performance 4-Leitung | €100 |
| Radlager | SKF vorne+hinten (4 St.) | €214 |
| Bremsflüssigkeit | ATE TYP200 DOT4 | €12 |
| Achseinstellung | 4-Rad | €100 |
| **Phase 2a TOTAL** | | **€597** |

**Phase 2b — Fahrwerk (€820-1.100)**: Federn + Dämpfer + Domlager

| Komponente | Teil | Preis |
|-----------|------|------:|
| Federn | Eibach Pro-Kit E10-41-001-05-22 | €210 |
| Dämpfer | KONI Special Active (Gelb) 4er-Set | €580 |
| Domlager | Lemförder 37706 01 (Paar) | €96 |
| Stabilager | Febi 37459/37460 (Paar v+h) | €35 |
| Stabi-Links | Meyle HD + Febi (v+h) | €53 |
| Achseinstellung | 4-Rad (nach Federn) | €100 |
| **Phase 2b TOTAL** | | **€1.074** |

> ⚠️ Phase 2a + 2b = €1.671 — wenn an einem Stück gemacht, KONI Yellow evtl. auf Phase 3 schieben.
> 💡 Mit Vogtland + Bilstein B6 statt Eibach + KONI: Phase 2b = ~€934, Gesamt = ~€1.531
> 💡 Dämpfer aufschieben wenn aktuelle OK: Phase 2a + Federn + Kleinteile = ~€1.001
> 💡 **Querlenker je nach Zustand** → bei >80tkm: +€240-380, bei <80tkm: aufschieben

---

## 🔧 EINBAU-HINWEISE V50 2.4i

1. **Federspanner VORNE**: Zwingend erforderlich, Platz ist eng im Federbein
2. **Anschlagpuffer kürzen**: Bei -30mm vorne ~20-25mm abschneiden (wird oft vergessen!)
3. **Querlenker-Hinterbolzen**: Bekannt für Festrost auf P1! Rostlöser + Ersatzbolzen bereithalten (Volvo 30665427)
4. **Domlager IMMER mitwechseln**: Bekannte Schwachstelle P1, Klackern bei Schlaglöchern
5. **Bremsscheiben**: Niemals ohne neue Beläge wechseln (und umgekehrt)
6. **SS-Leitungen**: Nach Einbau Bremsanlage entlüften (ATE TYP200 DOT4)
7. **Radlager vorne**: Presseinsatz, Sprengring sichern — Werkstatt empfohlen
8. **4-Rad-Achseinstellung NACH Einbau**: €80-120, V50 Multilink hinten justierbar
9. **Settling**: 2-4 Wochen bis Endhöhe erreicht, dann erneut messen
10. **TÜV-Anmeldung**: ABE-Dokumente von Eibach/Vogtland + HEL mitnehmen → Eintragung ohne Einzelprüfung
11. **KONI + Eibach zusammen eintragen**: Spart €50-100 TÜV-Kosten!
12. **🆕 BREMSGRÖßE PRÜFEN**: VOR Beuteleinkauf Bremsen messen! 280mm standard vs 316/302mm T5 = unterschiedliche Teile!

---

## ⚠️ TÜV-CHECKLISTE

| Komponente | Dokument | Status |
|-----------|----------|--------|
| Federn Eibach | ABE E10-41-001-05-22 | ✅ |
| Federn Vogtland | ABE V-998102 | ✅ |
| Dämpfer KONI/Bilstein | Teilegutachten | ✅ |
| Bremsscheiben Zimmermann (280mm) | ABE | ✅ |
| Bremsscheiben Zimmermann (316/302mm) | ABE | ✅ |
| SS-Leitungen HEL | TÜV-Zertifikat | ✅ |
| Bremsbeläge TRW/ATE | ECE R90 | ✅ eintragungsfrei! |
| **Bremsbeläge Ferodo DS2500** | **❌ KEIN ECE R90** | **❌ ILLEGAL!** |
| **🆕 T5-Bremsen-Upgrade** | **§19.3 Eintragung nötig** | **🟡 Caliper-Träger-Änderung** |
| Radlager SKF | E-Kennzeichnung | ✅ |
| Stabis Estoni | ABE (falls installiert) | ✅ |
| Querlenker Lemförder | OEM-Teilenummer | ✅ |
| SuperPro Poly-Buchsen | ABE SPF3332K | ✅ |

**🆕 WICHTIG**: T5-Bremsen-Upgrade (280→316/302mm) ändert die Bremsanlage und benötigt §19.3 Eintragung! Wenn nur Scheiben+Beläge gleicher Größe getauscht werden = eintragungsfrei (ECE R90).

---

## 🚫 VERMEIDEN — NICHT STEALTH / NICHT TÜV

| Komponente | Warum nicht |
|-----------|-------------|
| H&R 29249-1 | -40mm = ZU TIEF für STEALTH |
| Gewindefahrwerke (BC Racing etc.) | Hart, auffällig, meist -40 bis -60mm |
| Gebohrte Bremsscheiben | Kein TÜV auf P1, Rissgefahr |
| Powerflex Poly-Buchsen | Keine ABE = Einzelabnahme €200-400 |
| IPD Stabis (rot) | Kein TÜV für DE, rote Pulverbeschichtung |
| **Ferodo DS2500** | **KEIN ECE R90 = STRASSENVERKEHRS-ILLEGAL!** |
| EBC Greenstuff | Kein TÜV in EU |
| Billig-Radlager (Meyle/RIDEX) | Ausfall vor 50tkm |
| Sachs OEM Dämpfer | Nicht für -30mm geeignet |
| Bilstein B4 | Nicht für -30mm geeignet |
| T5-Federn auf 2.4i | Falsche Federkonstante + Sitzhöhe |
| KONI/Bilstein ohne Federn | B6 mit OEM-Härte = zu hart, B4 gar nicht |
| **🆕 T5-Bremsen ohne Caliper-Träger** | **Passen nicht! 316mm Beläge auf 280mm Caliper = GEFAHR** |

---

## 📝 ÄNDERUNGEN v2 → v3

1. **🆕 KRITISCH**: Bremsengrößen-Konflikt geklärt — V50 2.4i Standard = 280/280mm, T5 = 316/302mm
2. **🆕 KRITISCH**: Beide Bremsen-Optionen (Standard + T5-Upgrade) vollständig dokumentiert
3. **🆕 KRITISCH**: Domlager-Korrektur — Febi 37389 = Stabi-Link, NICHT Domlager! Richtiges Domlager = Lemförder 37706 01
4. **🆕 NEU**: Stabi-Links (Droplinks) als eigener Absatz mit Teilenummern
5. **🆕 NEU**: OEM-Stabi-Swap als günstige Alternative (T5 23/19mm gebraucht ~€50-80)
6. **🆕 NEU**: Alle Budget-Optionen auf Standard 280mm umgerechnet
7. **🆕 NEU**: AMZ-Fälschungs-Warnung bei Radlagern (Preise unter €30/Stück = Risiko)
8. **🆕 NEU**: T5-Bremsen-Upgrade §19.3 Eintragungspflicht dokumentiert
9. **Korrektur**: TRW Teilenummern korrigiert — GDB1359/58 für 280mm, GDB1805/40 für 316/302mm
10. **Korrektur**: ATE Ceramic Teilenummern — 5807.2/7006.2 für 280mm, 7213.2/7222.2 für 316/302mm
11. **Preis-Update**: Bremsensets für 280mm Standard günstiger als erwartet
12. **Preis-Update**: Phase E Phasen-Split auf Standard 280mm aktualisiert

---

*Letztes Update: 2026-05-28 v3 | DB: 668 Teile, 381 V50 Fitments, 76 verified | Bremsengröße: USER KLÄREN!*