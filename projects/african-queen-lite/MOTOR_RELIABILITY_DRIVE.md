# 🏍️ African Queen Lite — Motor-Zuverlässigkeit & Antrieb Research

**Date:** 2026-05-27 | **Priority:** P1 (Motorlauf & Sicherheit) | **Budget:** €500-800 (Phase 1)

> **PRINZIP:** 44PS OEM reichen. Auspuff+Filter NUR für KLANG+OPTIK. PS-Gewinn = Sahnehaube, kein Ziel.

---

## 1️⃣ STATOR + REGULATOR — 🔴 KRITISCH (Priority #1)

### Bekannte Probleme (NX650 ND01/ND02/ND03)

| Problem | Symptom | Ursache | Häufigkeit |
|---------|---------|---------|------------|
| Stator-Wicklung durchgebrannt | Batterie lädt nicht, Licht wird schwach | Hitze-Zerstörung der Isolierung, dünner Draht | **SEHR HÄUFIG** 20.000-40.000km |
| Regler-Überhitzung | Überladung (>15V), Batterie kocht | Shunt-Regler leitet Überschuss als Wärme ab | **HÄUFIG** nach 15+ Jahren |
| Verbinder geschmolzen | Ladeprobleme, sporadische Ausfälle | 6-Pin Verbinder zw. Stator & R/R → Widerstand → Hitze | **HÄUFIG** |
| Masse-Probleme | Dimmende Instrumente, Flicker | Aufbau am Lenkkopf brüchig, Widerstand | Mäßig |
| Zündschloss-Kontakt | Sporadischer Ausfall, kein Funke | Kontakt-Widerstand im Zündschloss | Gelegentlich |

### Lösung: Stator + Regulator Upgrade

| Komponente | Empfehlung | Preis (€) | Quelle | Notizen |
|------------|-----------|-----------|--------|---------|
| **Stator** | RM Stator 200W Upgrade | 119-159 | RM Stator direkt | Schwererer Draht, bessere Lackierung. 200W vs OEM 180W |
| **Regulator** | Shindengen FH020AA MOSFET | 49-65 | FC-Moto/eBay | **MUSS-UPGRADE!** Schaltet Stator ab statt kurzschließen → Stator kühler |
| **Combo Kit** | RM Stator + FH020AA Bundle | 168 | RM Stator | Best Value! Beide zusammen |
| **Batterie** | JMT YTZ10F LiFePO4 | 45-130 | Amazon.de | -2kg Gewicht, bessere Startleistung |
| **Alternative Batterie** | Antigravity YTZ10-12 | 100-130 | Spezialshop | More CCA, teurer |

### Stator-Lastplan (mit allen Verbrauchern)

| Verbraucher | Leistung (W) |
|-------------|-------------|
| Zündung (CDI) | ~35 |
| Scheinwerfer OEM H4 | ~55 |
| Rücklicht + Blinker | ~25 |
| **Basis-Last** | **~115W** |
| LED Scheinwerfer (erspart) | -55 → ~-40W (LED zieht ~15W) |
| Heizgriffe Oxford | +30 |
| USB-Ladegerät | +10 |
| **Zusatz-Last** | **~0W (LED spart mehr als Zu+verbrauch)** |
| **Gesamt** | **~80-90W** |
| **Stator RM 200W** | **110-120W RESERVE** ✅ |

### Wichtigste Maßnahmen (Reihenfolge)

1. ✅ FH020AA MOSFET Regler einbauen — **erstes Was immer zuerst!**
2. ✅ Stator-Verbinder DIREKT löten (6-Pin Stecker entfernen)
3. ✅ Zusätzliche Masseleitung Batterie → Rahmen → Motor
4. ✅ RM Stator 200W wenn OEM-Stator schwach (unter 50V AC pro Phase bei Leerlauf)
5. ✅ Zündschloss-Kontakte reinigen + Kontaktspray

---

## 2️⃣ VERGASER — Keihin VE82M (Priority #2)

### VE82M Spezifikationen

| Parameter | Wert | Anmerkung |
|-----------|------|-----------|
| Typ | Keihin VE82M (CV/Pumper) | 42mm Kolben-Vergaser |
| Hauptdüse (Main Jet) | **#145** (OEM) | +2-5 bei Auspuff+Filter |
| Nadeldüse (Needle Jet) | OEM Keihin | Clip Position 3-4 von oben |
| Leerlaufdüse (Pilot Jet) | **#42** (OEM, manche Quellen #38) | #45 für Berg/heiße Klima |
| Schwimmerhöhe | **14.5-15.0 mm** | Gemessen von Dichtfläche |
| Gemischschraube | 2.5 Umdrehungen | Von ganz geschlossen, dann für höchste Leerlaufdrehzahl feinjustieren |
| Leerlauf | 1.400 ± 100 U/min | |

### Bekannte VE82M Probleme

| Problem | Ursache | Lösung |
|---------|---------|--------|
| **Schlechter Leerlauf** | Pilotdüse verstopft (Ethanol!) | #42/#38 Pilotdüse mit feinem Draht reinigen |
| **Ruckeln beim Gasgeben** | Unterdruckschlauch gerissen | Neue Silikonschläuche (3mm) bestellen |
| **Benzin-Auslaufen** | Schwimmernadel hält nicht | Schwimmerhöhe auf 14.5mm einstellen, Nadelfett ersetzen |
| **Mageres Pochen beim Schubbetrieb** | Falsches Gemisch / Luft im Ansaugtrakt | Ansaugmanschettendichtung prüfen, Pilotdüse eine Nummer größer |
| **Ethanol-Schäden** | Korrosion im Schwimmergehäuse | Frischer Kraftstoff, Inline-Filter, Ethanol-resistente Dichtungen |

### Rebuild Kit Vergleich

| Kit | Teilenummer | Preis (€) | Qualität | Empfehlung |
|-----|------------|-----------|----------|------------|
| **All Balls** | 22-1022 | 28-35 | OEM-spec, passgenau | ⭐ **EMPFOHLEN** |
| Moose Racing | 0507-0014 | 30-40 | OK, aber O-Ringe manchmal zu groß | Alternativ |

### Jetting-Tabelle (bei Modifikationen)

| Konfiguration | Hauptdüse | Pilotdüse | Nadel-Clip | Anmerkung |
|---------------|-----------|-----------|------------|-----------|
| **OEM (Serie)** | #145 | #42 | 3. Position | Basis-Einstellung |
| **+ Slip-on Auspuff** | #148-150 | #42 | 3. Position | Nur Hauptdüse +3-5 |
| **+ UNI Filter** | #148 | #42 | 3→2 (Nadel anheben) | Leicht fetter |
| **+ Auspuff + UNI** | #150-152 | #45 | 2. Position | Beide Düsen + Stufe |
| **+500m Höhe** | #142 | #40 | 4. Position | Magerer für dünne Luft |

> **⚠️ WICHTIG:** Bei Slip-on Auspuff + UNI Filter sind Jetting-Änderungen empfohlen, aber NICHT zwingend für den ersten Start. Erst mal fahren, dann ggf. anpassen. Die VE82M CV Vergaser sind recht tolerant.

### Vergaser-Wartungs-Checkliste

- [ ] Pilotdüse reinigen (feiner Draht, 0.4mm)
- [ ] Schwimmerhöhe auf 14.5mm einstellen
- [ ] Unterdruckschläuche prüfen/ersetzen (3mm Silikon)
- [ ] Gemischschraube auf 2.5 Umdrehungen Basis
- [ ] Idle auf 1.400 U/min justieren
- [ ] Choke-Funktion testen (Kaltstart)
- [ ] Benzinfilter inline installieren (Ethanol-Schutz)

---

## 3️⃣ AUSPUFF — Für SOUND + OPTIK (Priority #3)

> **KEIN Leistungstuning!** Auspuff = KLANG + OPTIK + Gewichtsersparnis. PS-Gewinn = Bonbon, kein Ziel.

### Auspuff-Optionen Vergleich

| Option | Typ | E-Nummer/StVZO | Gewicht | Sound | Preis (€) | Empfehlung |
|--------|------|----------------|---------|-------|-----------|-----------|
| **Leo Vince SBK** | Slip-on carbon/SS | ✅ **ECE R92, TÜV** | ~2.0 kg | Tief, bassig, Single-Cylinder Thump | 310-380 | ⭐ **BESTE WAHL** (Legal!) |
| Delkevic 14" SS | Slip-on | ❌ Keine E-Nummer | ~1.2-2.0 kg | Tief, kernig, laut ohne DB-Killer | 130-180 | Budget, aber illegal auf Straße |
| FMF PowerCore 4 | Slip-on | ❌ Nur Offroad | ~1.5 kg | Laut, aggressiv, dröhnend | 250-320 | Zu laut für Straße |
| OEM mit SS Header | Header-only | ✅ OEM bleibt legal | ~5.5 kg (mit SS -2kg) | OEM-Sound, tiefer mit SS | 200 (Header) | Legalste Option |

### SS Header (Collector-Delete)

| Feature | Detail |
|---------|--------|
| **Teil** | Delkevic SS Header für NX650 |
| **Preis** | €150-250 |
| **Gewichtsersparnis** | -2 kg (Collectorkasten fällt weg) |
| **Vorteile** | Bessere Optik, weniger Hitze am Bein, leichterer Antritt |
| **Passform** | Direkter Fit, keine Anpassung nötig |
| **Mit OEM Muffler** | Ja! SS Header + OEM Endtopf = legal und bessererer Sound |
| **Mit Leo Vince** | Perfekt! SS Header + Leo Vince SBK = bester Sound + legal |

### Sound-Bewertung (Single-Cylinder 644cc)

| Konfiguration | Sound-Charakter | Lautstärke | StVZO Legal |
|---------------|----------------|-----------|-------------|
| OEM komplett | Leise, dumpf | ~80 dB | ✅ |
| SS Header + OEM Muffler | Leicht tiefer, kerniger | ~82 dB | ✅ |
| SS Header + Leo Vince (mit DB-Killer) | **Tief, voller Thump** | ~93 dB | ✅ |
| SS Header + Leo Vince (ohne DB-Killer) | Voll, dröhnend | ~100+ dB | ❌ Track only |
| Delkevic Slip-on | Laut, kernig | 95-100 dB | ❌ |
| FMF PowerCore 4 | Sehr laut, aggressiv | 100+ dB | ❌ |

### Empfehlung: AUSPUFF-STRATEGIE

**Budget-Option (~€200):** Delkevic SS Header + OEM Endtopf behalten
- -2 kg Gewicht, besserer Sound, 100% legal
- Optik: Edelstahl-Header sieht gepflegt aus
- Sound: Leicht tiefer und kerniger als OEM

**Optimal-Option (~€500):** Delkevic SS Header + Leo Vince SBK Slip-on
- -3 kg Gewicht (8→5 kg), bester Sound, ECE R92 legal ✅
- Optik: SS Header + Carbon Endtopf = Africa Twin Racing Look
- Sound: Tiefer, voller Single-Cylinder Thump mit DB-Killer legal
- Eintragung: Leo Vince kommt mit E-Nummer → einfach eintragen lassen

---

## 4️⃣ LUFTFILTER — Für Sound + Wartung (Priority #4)

### UNI NU-4050 vs K&N HA-6502 vs OEM Honda

| Feature | UNI NU-4050 | K&N HA-6502 | OEM Honda |
|---------|-------------|-------------|----------|
| **Material** | 2-Lagiger Schaumstoff (grob+fein) | Baumwollgewebe mit Ölfilm | Papier (Einweg) |
| **Preis (€)** | 18-30 | 45-55 | 30-50 |
| **Wiederverwendbar** | ✅ Ja | ✅ Ja | ❌ Nein |
| **Filterleistung Staub** | ⭐⭐⭐⭐⭐ Sehr gut | ⭐⭐⭐⭐ Gut | ⭐⭐⭐⭐⭐ Basis |
| **Filterleistung Regen** | ⭐⭐⭐⭐⭐ Wasserabweisend | ⭐⭐⭐ Befriedigend | ⭐⭐⭐⭐⭐ |
| **Ansauggeräusch** | Leiser "Whoosh" | Deutlicherer "Honk" | Leise |
| **Wartungsintervall Straße** | 3.000-5.000 km | 10.000-16.000 km | 6.000 km (tauschen) |
| **Wartungsintervall Staub** | 1.000 km | 3.000-5.000 km | Nicht geeignet |
| **Feld-Wartung** | Seife+Wasser, UNI-Öl | Spezialreiniger, trocknen lassen | Tauschen |
| **Jetting nötig?** | Nein (alleine) | Nein bis leicht (alleine) | — |
| **Adventure-Eignung** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

### Empfehlung: **UNI NU-4050** ⭐

**Begründung:**
- Beste Filterleistung bei Staub (2-Lagen-Schaum)
- Wartungsfreundlich (Seife+Wasser im Feld)
- Günstiger als K&N (€18-30 vs €45-55)
- Wasserabweisend bei Regen/Flussdurchfahrten
- Kein Jetting nötig bei OEM-Auspuff
- Leichtes Ansauggeräusch (Bonus, nicht Ziel)

**K&N HA-6502:** Option für Street-biaste Fahrer die lauteren Ansauggeräusch wollen und weniger warten. Aber: weniger Staub-Schutz, teurer, komplexere Wartung.

---

## 5️⃣ KETTE + RITZEL + BREMSEN (Priority #5)

### Ketten-Kit

| Variante | Kette | Ritzel vorne/hinten | Preis (€) | Quelle |
|----------|-------|---------------------|-----------|--------|
| **DID 520VX3 + JT** | DID 520VX3 X-Ring | 15/44 (OEM) | 85-95 | Motea/Motointegrator |
| DID 520VX3 + JT 15/45 | DID 520VX3 X-Ring | 15/45 (More acceleration) | 88-110 | Motea |
| DID 520ZVM-X Premium | DID 520ZVM-X | 15/44 | 95-110 | FC-Moto |

### Übersetzung: 15/44 vs 15/45

| Konfiguration | Vorteil | Nachteil | Für wen? |
|---------------|---------|----------|----------|
| **15/44 (OEM)** | Besser Topspeed, niedrigerer Drehzahl | Weniger Zug am Berg | Touring, viel Autobahn |
| **15/45 | Mehr Beschleunigung, besser am Berg | ~5-8 km/h weniger Topspeed | Adventure, viel Gelände, beladen |

> **Empfehlung:** 15/44 für gemischtes Fahren. 15/45 wenn Schwerlast/Gelände. Im Set enthalten, kein Preisunterschied!

### Bremsen

| Komponente | Empfehlung | Preis (€) | Notizen |
|------------|-----------|-----------|---------|
| **Bremsbeläge vorne** | EBC FA185HH Sinter | 22-32 | HH für Adventure, bissfest auch nass |
| **Bremsbeläge hinten** | EBC FA185HH (hinten) | 18-30 | Passend für NX650 |
| **SS Bremsscheibenleitung** | HEL Performance (vorne) | 55-70 | Pflicht-Upgrade! Festerer Druck |
| Alternative SS Leitung | Goodridge | 50-65 | Etwas günstiger |
| Premium Option | Spiegler | 80-100 | Custom Längen, justierbare Banjo |
| **Scheibe vorne** | OEM 256mm | — | OEM reicht! KEIN 260mm XL600 Kit nötig |
| Radlager vorne+hinten | All Balls Kit | 50 | Komplett-Set, präventiv tauschen |

---

## 6️⃣ ZUSAMMENFASSUNG: PRIORITÄTEN & BUDGET

### Phase 1: KRITISCH — Motorlauf & Sicherheit (~€420-450)

| # | Teil | Preis (€) | Priorität |
|---|------|-----------|-----------|
| 1 | RM Stator + FH020AA Combo | 168 | 🔴 KRITISCH |
| 2 | Stator-Verbinder löten + Massekabel | 5-15 | 🔴 KRITISCH |
| 3 | All Balls Carb Rebuild Kit 22-1022 | 28-35 | 🔴 KRITISCH |
| 4 | UNI Luftfilter NU-4050 | 18-30 | 🟡 Wichtig |
| 5 | DID 520VX3 + JT 15/44 Ketten-Kit | 85-95 | 🟡 Wichtig |
| 6 | EBC FA185HH Bremsbeläge (vorne) | 22-32 | 🟡 Wichtig |
| 7 | SS Bremsscheibenleitung (HEL) | 55-70 | 🟡 Wichtig |
| 8 | Hiflo HF131 Ölfilter | 5-9 | 🟢 Wartung |
| 9 | NGK DPR8EA-9 Zündkerze | 4-7 | 🟢 Wartung |
| 10 | Viton-Kraftstoffschlauch 3mm (für Vergaser) | 5-10 | 🟢 Wartung |
| **Phase 1 Total** | | **~€395-460** | |

### Phase 2: FAHRWERK (~€850) — siehe BUDGET_OPTIMIZATION.md

### Phase 3: SOUND + OPTIK (~€500-700)

| # | Teil | Preis (€) | Priorität |
|---|------|-----------|-----------|
| 1 | Delkevic SS Header | 150-250 | 🟡 Sound+Optik+Gewicht |
| 2 | Leo Vince SBK Slip-on (ECE R92) | 310-380 | 🟡 Sound+Legal |
| — *Alternative Budget:* | SS Header + OEM Muffler behalten | 150-250 | 🟡 Legal+Fokus |
| 3 | LED H4 Scheinwerfer | 25-75 | 🟡 Optik+Gewicht |
| 4 | LED Blinker + Rücklicht | 35-50 | 🟡 Optik+Gewicht |

### Phase 4+5: Touring+Reserve — siehe BUDGET_OPTIMIZATION.md

---

## 7️⃣ WISSEN AUS DER COMMUNITY

### Stator-Pflege
- Stator-Spannung prüfen: Bei Leerlauf >50V AC pro Phase (3 Phasen paaren)
- Batteriespannung bei 3.000 U/min: 13.8-14.4V = OK, >15V = Regler defekt
- **FH020AA senkt Stator-Temperatur um 30-50%** — das ist das wichtigste Upgrade!
- Stator-Verbinder LÖTEN, nicht nur stecken!

### Vergaser-Tipps
- VE82M ist CV-Vergaser — reagiert träge auf Jetting-Änderungen
- Pilotdüse ist #42 (manche Quellen #38 — OEM ist #42 für die meisten Märkte)
- Nach Rebuild: Gemischschraube 2.5 Umdr., dann für höchste Leerlaufdrehzahl feinjustieren
- **Ethanol-Kraftstoff** ist der Feind! Inline-Kraftstofffilter ist Pflicht
- Vacuum-Schläuche müssen weich sein — 30 Jahre alte Schläuche werden rissig

### Auspuff-Tipps
- **Leo Vince SBK ist die EINZIGE StVZO-legale Slip-on Option** unter den drei Kandidaten
- SS Header + OEM Muffler = legal und bessererer Sound, -2kg
- DB-Killer im Leo Vince für Straße drin lassen! ~93 dB legal
- Collector-Box löschen spart 2-3 kg, verbessert Antritt

### Luftfilter-Tipps
- UNI NU-4050 ist der Adventure-Standard — 2-Lagen-Schaum, Feld-wartbar
- K&N für Street, UNI für Dirt — auf der NX650 (Adventure!) → UNI
- Reinigung alle 3.000 km auf Straße, alle 1.000 km im Staub

---

## 8️⃣ TEAM-REQUESTS UPDATE

### ✅ Erledigt (dieser Run):
- Stator+Regler: RM Stator 200W + FH020AA Combo bestätigt, Lastplan berechnet
- Vergaser: VE82M Specs + Jetting-Tabelle + Rebuild-Kit empfohlen
- Auspuff: Leo Vince SBK als EINZIGE legale Slip-on identifiziert
- Luftfilter: UNI NU-4050 als Best Choice für Adventure bestätigt
- Kette+Ritzel: DID 520VX3 bestätigt, 15/44 OEM empfohlen

### 🔄 Offene Anfragen:
- **Chefingenieur**: Gewichtsverteilung vorne/hinten berechnen (geschätzt 55/45)
- **Chefingenieur**: Tank voll/leer Einfluss auf Handling (15L = ~11kg Benzin)
- **Elektrik**: Zündschloss-Kontakte prüfen und reinigen
- **Fahrwerk**: YSS Mono Bracket Schweißen (~€50-80 lokal)
- **Stylist**: Tank-Decals African Queen rot/blau/weiß — DIY oder DecalMX?