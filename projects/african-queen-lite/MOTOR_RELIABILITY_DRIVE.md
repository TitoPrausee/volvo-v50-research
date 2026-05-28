# 🏍️ African Queen Lite — Motor-Zuverlässigkeit & Antrieb Research

**Date:** 2026-05-28 (Update 2) | **Priority:** P1 (Motorlauf & Sicherheit) | **Budget:** €500-800 (Phase 1)

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
| **Stator** | RM Stator 200W Standard | 89.90-120 | FC-Moto/RM Stator | Schwererer Draht 18AWG, 200°C Isolierung. 200W vs OEM 180W |
| **Stator HD** | RM Stator 200W Heavy Duty | 130-160 | RM Stator direkt | 16AWG Draht, 220°C Isolierung, Lebenslang-Garantie |
| **Regler** | Shindengen FH020AA MOSFET | 49.90-65 | Amazon/FC-Moto | **MUSS-UPGRADE!** Schaltet Stator ab statt kurzschließen → Stator kühler |
| **Combo** | RM Stator + FH020AA separat | ~140 | Separat kaufen! | Kein Bundle günstiger als separate |
| **Regler-Verbinder-Kit** | Cycle Terminal RM14016 | 8 | Amazon/Cycle Terminal | **PFLICHT!** Bekanntes Schmelz-Problem |
| **Stator-Connector** | Cycle Terminal 3-Pin | 9 | Amazon/Cycle Terminal | **LÖTEN statt stecken!** |
| **Massekabel** | DIY 10AWG Kupferkabel | 5-10 | Baumarkt | Batterie → Rahmen → Motor |
| **Batterie** | JMT YTZ10F LiFePO4 | 49.90-75 | Amazon | -2kg Gewicht, bessere Startleistung |
| **Alternative Batterie** | Antigravity YTZ10-12 | 135-170 | Spezialshop | More CCA, Restart-Funktion, teurer |

### Stator-Lastplan (mit allen Verbrauchern)

| Verbraucher | Leistung (W) |
|-------------|-------------|
| Zündung (CDI) | ~35 |
| Scheinwerfer OEM H4 | ~55 |
| Rücklicht + Blinker | ~25 |
| **Basis-Last** | **~115W** |
| LED Scheinwerfer (erspart) | -55 → ~-40W (LED zieht ~15-20W) |
| Heizgriffe Oxford | +30 |
| USB-Ladegerät | +10 |
| **Zusatz-Last** | **~0W (LED spart mehr als Zu+verbrauch)** |
| **Gesamt** | **~80-90W** |
| **Stator RM 200W** | **110-120W RESERVE** ✅ |

### Wichtigste Maßnahmen (Reihenfolge)

1. ✅ FH020AA MOSFET Regler einbauen — **erstes Was immer zuerst!**
2. ✅ Stator-Verbinder DIREKT löten (6-Pin Stecker entfernen!)
3. ✅ Zusätzliche Masseleitung Batterie → Rahmen → Motor
4. ✅ RM Stator 200W wenn OEM-Stator schwach (unter 50V AC pro Phase bei Leerlauf)
5. ✅ Zündschloss-Kontakte reinigen + Kontaktspray
6. ✅ Regler-Verbinder-Kit ersetzen (bekanntes Schmelz-Problem!)
7. ✅ Batteriespannung testen: 13.8-14.4V @ 3000rpm = OK, >15V = Regler defekt

### Build Guide: FH020AA MOSFET Regler-Upgrade (ID#3 — STATUS: AKTIV)

**Voraussetzung:** Multimeter, Lötkolben, Schrumpfschlauch, 10AWG Kabel
**Zeit:** 1-2 Stunden | **Kosten:** ~€75

1. OEM Regler abklemmen (Batterie zuerst!)
2. Stator-Verbinder LÖTEN — 6-Pin Stecker entfernen, Dräte direkt löten + Schrumpfschlauch
3. FH020AA montieren (Original-Befestigungslöcher passen, Heatsink verwenden)
4. Connector-Kit (RM14016) anlöten an Regler-Seite
5. Massekabel 10AWG: Batterie- → Rahmen → Motorblock
6. Testen: Batteriespannung @ 3000rpm → 13.8-14.4V = ✅, >15V = Problem

### Build Guide: Stator-Wechsel (ID#4 — STATUS: AKTIV)

**Voraussetzung:** Motoröl ablassen, linke Motorabdeckung entfernen
**Zeit:** 2-3 Stunden | **Kosten:** ~€130

1. Motoröl ablassen (~2.2L)
2. Linke Motorabdeckung entfernen (8 Schrauben M6)
3. Stator Halteschrauben lösen (3 Stück)
4. RM Stator 200W einsetzen — auf korreten Sitz achten
5. Kupplungsdeckel-Dichtung ersetzen (22860-KY5-000, €12)
6. Stator-Verbinder LÖTEN (nicht stecken!)
7. Motoröl einfüllen (2.2L Honda GN4 10W-40)
8. AC-Spannung testen: >50V pro Phase bei Leerlauf = ✅

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
| **Ruckeln beim Gasgeben** | Unterdruckschlauch gerissen | Neue Silikonschläuche 3mm (ID#447) |
| **Benzin-Auslaufen** | Schwimmernadel hält nicht | Schwimmerhöhe auf 14.5mm einstellen, Nadelfett ersetzen |
| **Mageres Pochen beim Schubbetrieb** | Falsches Gemisch / Luft im Ansaugtrakt | Ansaugmanschettendichtung prüfen, Pilotdüse eine Nummer größer |
| **Ethanol-Schäden** | Korrosion im Schwimmergehäuse | Inline-Kraftstofffilter (ID#446), Ethanol-resistente Dichtungen |

### ⚠️ NEU: Inline-Kraftstofffilter — PFLICHT für VE82M!

Ethanol-Kraftstoff (E5/E10 in EU) ist der **Feind Nr.1** der VE82M-Pilotdüse. Ein Inline-Filter zwischen Kraftstoffhahn und Vergaser verhindert, dass Ablagerungen die feine #42/#38 Pilotdüse verstopfen.

| Filter | Preis (€) | Part Number | Notizen |
|--------|-----------|-------------|---------|
| **Emgo 8mm Inline Filter** | 5-8 | EM-IF8MM | Transparent, 40 Mikron, Flow >50L/h |
| UNI Inline Filter 5/16" | 7-10 | UNI-IF516 | Etwas teurer, gleiche Funktion |
| Moose 8mm Inline | 8-12 | MOOSE-IF8 | Premium-Alternativ |

**Einbau:** Zwischen Kraftstoffhahn (16950-KY5-871) und Vergaser-Eingang. 8mm Schlauchdurchmesser. Pfeilrichtung = Flussrichtung. Alle 12.000km tauschen.

### ⚠️ NEU: Silikon-Unterdruckschläuche — PFLICHT bei Ruckeln!

Nach 20+ Jahren werden die OEM-Gummischläuche rissig. Das verursacht **Falschluft → Magerlauf → Ruckeln**.

| Schlauch | Preis (€) | Notizen |
|----------|-----------|---------|
| **Silikon 3mm ID x 5mm OD** | 5-10 (1m Rolle) | Hitzebeständig -40°C bis 200°C |
| Viton 3mm (Premium-Alt) | 12-18 | Noch höher chemische Resistenz |

**Ersetzen:** 3 Unterdruckschläuche: 1) Vergaser-Sync-Port, 2) Vacuum-Kraftstoffhahn, 3) MAP-Sensor. 1m Rolle reicht für alle 3 + Reserve.

### Rebuild Kit Vergleich

| Kit | Teilenummer | Preis (€) | Qualität | Empfehlung |
|-----|------------|-----------|----------|------------|
| **All Balls** | 22-1022 | 27.90-35 | OEM-spec, passgenau | ⭐ **EMPFOHLEN** |
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
- [ ] Unterdruckschläuche prüfen/ersetzen (3mm Silikon) — **NEU! ID#447**
- [ ] **Inline-Kraftstofffilter einbauen** — NEU! ID#446, PFLICHT für Ethanol-Schutz
- [ ] Gemischschraube auf 2.5 Umdrehungen Basis
- [ ] Idle auf 1.400 U/min justieren
- [ ] Choke-Funktion testen (Kaltstart)
- [ ] Kraftstoffhahn auf Leckage prüfen (16950-KY5-871)

### Build Guide: VE82M Carburetor Rebuild (ID#5 — STATUS: PLANUNG)

**Voraussetzung:** All Balls 22-1022 Kit, Inline-Filter, Silikonschläuche, Ultraschallreiniger optional
**Zeit:** 3-4 Stunden | **Kosten:** ~€50 (Rebuild Kit €28 + Filter €7 + Schläuche €7 + Reinigung €5)

1. Vergaser ausbauen (2 Schellen, 3 Kabel, 2 Schläuche)
2. Schwimmergehäuse entfernen, Haupt- und Pilotdüse herausschrauben
3. Pilotdüse #42 mit 0.4mm Draht reinigen (NICHT vergrößern!)
4. Alle O-Ringe und Dichtungen mit All Balls 22-1022 ersetzen
5. Schwimmerhöhe auf 14.5mm einstellen (Dichtfläche messen)
6. Silikon-Unterdruckschläuche ersetzen (3 Stück)
7. Inline-Kraftstofffilter zwischen Hahn und Vergaser einbauen
8. Gemischschraube 2.5 Umdrehungen, Idle 1.400rpm
9. Testfahrt: Anfahren, Schubbetrieb, Leerlauf prüfen

---

## 3️⃣ AUSPUFF — Für SOUND + OPTIK (Priority #3)

> **KEIN Leistungstuning!** Auspuff = KLANG + OPTIK + Gewichtsersparnis. PS-Gewinn = Bonbon, kein Ziel.

### Auspuff-Optionen Vergleich

| Option | Typ | E-Nummer/StVZO | Gewicht | Sound | Preis (€) | Empfehlung |
|--------|------|----------------|---------|-------|-----------|-----------| 
| **Leo Vince SBK** | Slip-on carbon/SS | ✅ **ECE R92, TÜV** | ~2.0 kg | Tief, bassig, Single-Cylinder Thump | 215-380 | ⭐ **BESTE WAHL** (Legal!) |
| Delkevic 14" SS | Slip-on | ❌ Keine E-Nummer | ~1.2-2.0 kg | Tief, kernig, laut ohne DB-Killer | 130-180 | Budget, aber illegal auf Straße |
| FMF PowerCore 4 | Slip-on | ❌ Nur Offroad | ~1.5 kg | Laut, aggressiv, dröhnend | 250-320 | Zu laut für Straße |
| OEM mit SS Header | Header-only | ✅ OEM bleibt legal | ~5.5 kg (mit SS -2kg) | OEM-Sound, tiefer mit SS | 200 (Header) | Legalste Option |

### SS Header (Collector-Delete)

| Feature | Detail |
|---------|--------|
| **Teil** | Delkevic SS Header für NX650 |
| **Preis** | €159-250 (Delkevic EU Direct ~€159) |
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
| **Preis (€)** | 19.90-30 | 43-55 | 30-50 |
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
- Günstiger als K&N (€19.90 vs €43-55)
- Wasserabweisend bei Regen/Flussdurchfahrten
- Kein Jetting nötig bei OEM-Auspuff
- Leichtes Ansauggeräusch (Bonus, nicht Ziel)

---

## 5️⃣ KETTE + RITZEL + BREMSEN (Priority #5)

### Ketten-Kit

| Variante | Kette | Ritzel vorne/hinten | Preis (€) | Quelle |
|----------|-------|---------------------|-----------|--------|
| **DID 520VX3 + JT 15/44** | DID 520VX3 X-Ring | 15/44 (OEM) | 99.90 | Motea Bundle |
| DID 520VX3 + JT 15/45 | DID 520VX3 X-Ring | 15/45 (More acceleration) | 88-110 | Motea |
| DID 520ZVM-X Premium | DID 520ZVM-X | 15/44 | 95-110 | FC-Moto |

### Übersetzung: 15/44 vs 15/45

| Konfiguration | Vorteil | Nachteil | Für wen? |
|---------------|---------|----------|----------|
| **15/44 (OEM)** | Besser Topspeed, niedrigerer Drehzahl | Weniger Zug am Berg | Touring, viel Autobahn |
| **15/45** | Mehr Beschleunigung, besser am Berg | ~5-8 km/h weniger Topspeed | Adventure, viel Gelände, beladen |

> **Empfehlung:** 15/44 für gemischtes Fahren. 15/45 wenn Schwerlast/Gelände. Im Set enthalten, kein Preisunterschied!

### Bremsen

| Komponente | Empfehlung | Preis (€) | Notizen |
|------------|-----------|-----------|---------|
| **Bremsbeläge vorne** | EBC FA185HH Sinter | 15.90-32 | HH für Adventure, bissfest auch nass |
| **Bremsbeläge hinten** | EBC 396 Schuhe (Trommel) | 13-19 | Kein Upgrade nötig bei Trommel |
| **SS Bremsscheibenleitung** | Venhill SS Line Front | 54-65 | Pflicht-Upgrade! Best Value SS line |
| Alternative SS Leitung | HEL Performance | 55-70 | Etwas teurer |
| **Scheibe vorne** | OEM 256mm | — | OEM reicht! KEIN 260mm Kit nötig |
| Radlager vorne+hinten | All Balls Kit | 25-27 | Komplett-Set, präventiv tauschen |

---

## 6️⃣ ⚠️ NEU: CDI & ZÜNDUNG — Zuverlässigkeits-Diagnosepfad (Priority: Nach Bedarf)

> **Hintergrund:** CDI-Hot-Start-Probleme (Issues #11, #30, #45, #50) sind bekannt bei ND01/ND02.
> **Aber:** Bevor der CDI ersetzt wird → systematische Diagnose! Oft ist es die Zündspule oder decomp-Ventil.

### Diagnose-Entscheidungsbaum: Kein Start / Schlechter Hot-Start

```
Startprobleme heiß?
│
├─→ 1. Dekomp-Ventil prüfen (KOSTENLOS!)
│   └─→ Freilauf 2-3mm? → NEIN → Einstellen → Problem gelöst? ✅
│
├─→ 2. Zündspule testen (VOR CDI-Wechsel!)
│   ├─→ Primär: 2.0-3.0 Ω? → NEIN → Zündspule tauschen (€25-65)
│   ├─→ Sekundär: 10-18 kΩ? → NEIN → Zündspule tauschen
│   └─→ Werte OK? → Weiter zu 3.
│
├─→ 3. Funke prüfen bei heißem Motor
│   ├─→ Kein Funke heiß? → CDI-Wechsel wahrscheinlich
│   └─→ Funke schwach? → Zündspule trotz Ohm-Werte verdächtig
│
└─→ 4. CDI ersetzen
    ├─→ OEM gebrauch: 30410-KY5-003 (€80-200) — Risiko: gleiches Problem
    ├─→ Aftermarket: Divers (€30-80) — ⚠️ Qualität variiert!
    └─→ ⭐ Ignitech DC-CDI-P2 (€120-180) — Programmierbar, DC-betrieben, 3 Zündkurven
```

### CDI-Optionen Vergleich

| Option | Preis (€) | Zuverlässigkeit | Vorteile | Nachteile |
|--------|-----------|----------------|----------|-----------|
| **OEM gebraucht** 30410-KY5-003 | 80-200 | ⚠️ Mittel | OEM-Spezifikation | Gleiches Heat-Soak-Risiko |
| **Aftermarket** | 30-80 | ⚠️ Niedrig | Billig | Qualität variiert, keine Garantie |
| **⭐ Ignitech DC-CDI-P2** | 120-180 | ✅ Hoch | Programmierbar, 3 Maps, DC-betrieben, kein Heat-Soak | Teurer, Einbauaufwand |

### Ignitech DC-CDI-P2 Details (DB ID#445)

| Feature | Wert |
|---------|------|
| **Typ** | DC-CDI (Kondensator wird aus 12V DC geladen) |
| **Vorteil vs OEM AC-CDI** | Unabhängig von Stator-Spannung → kein Heat-Soak |
| **Programmierbar** | Ja, via USB + Ignitech-Software (Windows) |
| **Zündkurven** | 3 Maps extern schaltbar (passt zu Ride Mode Controller!) |
| **Rev-Limiter** | Einstellbar (OEM: 7.500 rpm) |
| **EC-Typgenehmigung** | Verfügbar → §19.2 Eintragung möglich |
| **Anschluss** | OEM-Stecker-kompatibel (minimaler Kabelbaum-Änderung) |
| **Ride Mode Integration** | GPIO27 (Map A/B) + GPIO33 (Map B/C) → 3 Zündkurven |

### Zündspule Test (DB ID#448 — VOR CDI-Wechsel prüfen!)

| Messung | Sollwert | Gemessen → Aktion |
|---------|----------|-------------------|
| Primär-Widerstand | 2.0-3.0 Ω | >5Ω → Zündspule tauschen |
| Sekundär-Widerstand | 10-18 kΩ | >20kΩ → Zündspule tauschen |
| Funke bei heiß | Sichtbar, blau | Kein Funke → CDI verdächtig |

**Zündspule OEM:** 30500-KY5-003 | Preis: €25-65 | Einbau: 15 min

### Dekompressions-Ventil (DB ID#449 — KOSTENLOSE Diagnose!)

| Check | Sollwert | Aktion |
|-------|----------|--------|
| Freilauf Zug | 2-3 mm | <1mm → einstellen, >5mm → nachziehen |
| Funktion Hebel | Klick beim Loslassen | Kein Klick → Dekomp freeze → reinigen |

**Teilenummer:** 12351-KY5-871 | Preis: €15-35 (falls ersetzen nötig)

### ⚠️ WICHTIG: CDI-Wechsel ist LETZTER Schrott!

1. Erst decomp einstellen (€0)
2. Dann Zündspule messen (€0 mit Multimeter)
3. Dann Funke prüfen heiß (€0)
4. ERST DANN: CDI ersetzen (€80-280)

---

## 7️⃣ ZUSAMMENFASSUNG: PRIORITÄTEN & BUDGET

### Phase 1: KRITISCH — Motorlauf & Sicherheit (~€393)

| # | Teil | Preis (€) | Priorität | DB ID |
|---|------|-----------|-----------|-------|
| 1 | RM Stator 200W Standard | 89.90 | 🔴 KRITISCH | 29/239 |
| 2 | Shindengen FH020AA MOSFET Regler | 49.90 | 🔴 KRITISCH | 13/306 |
| 3 | Regler-Verbinder-Kit RM14016 | 8 | 🔴 KRITISCH | 345 |
| 4 | Stator 3-Pin Connector Set | 9 | 🔴 KRITISCH | 346/307 |
| 5 | Massekabel Batterie-Rahmen-Motor | 5-10 | 🔴 KRITISCH | 309 |
| 6 | All Balls Carb Rebuild Kit 22-1022 | **24.90** | 🔴 KRITISCH | 40 |
| 7 | **Inline-Kraftstofffilter 8mm** | 5-8 | 🔴 KRITISCH | **446 NEU** |
| 8 | **Silikon-Unterdruckschläuche 3mm** | 5-10 | 🔴 WICHTIG | **447 NEU** |
| 9 | UNI Luftfilter NU-4050 | **14.99** | 🟡 Wichtig | 15 |
| 10 | DID 520VX3 + JT 15/44 Ketten-Kit | **94.90** | 🟡 Wichtig | 28/343 |
| 11 | EBC FA185HH Bremsbeläge (vorne) | **13.90** | 🟡 Wichtig | 219 |
| 12 | Venhill SS Bremsscheibenleitung (vorne) | **34.90** | 🟡 Wichtig | 223/450 |
| 13 | Hiflo HF131 Ölfilter | 5-9 | 🟢 Wartung | 53 |
| 14 | NGK DPR8EA-9 Zündkerze | 5-7 | 🟢 Wartung | 106 |
| 15 | Viton-Kraftstoffschlauch 3mm (5m) | 5-10 | 🟢 Wartung | 167 |
| **Phase 1 Total** | | **~€393** | | |

### Diagnose-Reserve (bei Bedarf, NICHT im Basis-Budget)

| # | Teil | Preis (€) | Wann kaufen? | DB ID |
|---|------|-----------|------------|-------|
| 16 | Zündspule OEM 30500-KY5-003 | 25-65 | Bei Funke-Schwäche (VOR CDI!) | **448 NEU** |
| 17 | Ignitech DC-CDI-P2 | 120-180 | Wenn OEM-CDI defekt bestätigt | **445 NEU** |
| 18 | Dekomp-Ventil 12351-KY5-871 | 15-35 | Wenn Einstellen nicht reicht | **449 NEU** |

### Phase 2: FAHRWERK (~€1.005) — siehe BUDGET_OPTIMIZATION.md

### Phase 3: SOUND + OPTIK (~€500-700)

| # | Teil | Preis (€) | Priorität |
|---|------|-----------|-----------|
| 1 | Delkevic SS Header | 159-250 | 🟡 Sound+Optik+Gewicht |
| 2 | Leo Vince SBK Slip-on (ECE R92) | 215-380 | 🟡 Sound+Legal |
| — *Alternative Budget:* | SS Header + OEM Muffler behalten | 159-250 | 🟡 Legal+Fokus |
| 3 | LED H4 Scheinwerfer | 25-100 | 🟡 Optik+Gewicht |
| 4 | LED Blinker + Rücklicht | 18-55 | 🟡 Optik+Gewicht |

### Phase 4+5: Touring+Reserve — siehe BUDGET_OPTIMIZATION.md

---

## 8️⃣ WISSEN AUS DER COMMUNITY

### Stator-Pflege
- Stator-Spannung prüfen: Bei Leerlauf >50V AC pro Phase (3 Phasen paaren)
- Batteriespannung bei 3.000 U/min: 13.8-14.4V = OK, >15V = Regler defekt
- **FH020AA senkt Stator-Temperatur um 30-50%** — das ist das wichtigste Upgrade!
- Stator-Verbinder LÖTEN, nicht nur stecken!

### Vergaser-Tipps
- VE82M ist CV-Vergaser — reagiert träge auf Jetting-Änderungen
- Pilotdüse ist #42 (manche Quellen #38 — OEM ist #42 für die meisten Märkte)
- Nach Rebuild: Gemischschraube 2.5 Umdr., dann für höchste Leerlaufdrehzahl feinjustieren
- **Ethanol-Kraftstoff** ist der Feind! Inline-Kraftstofffilter ist PFLICHT (neu ID#446)
- Vacuum-Schläuche müssen weich sein — 30 Jahre alte Schläuche werden rissig → Silikon 3mm (neu ID#447)

### Auspuff-Tipps
- **Leo Vince SBK ist die EINZIGE StVZO-legale Slip-on Option** unter den drei Kandidaten
- SS Header + OEM Muffler = legal und bessererer Sound, -2kg
- DB-Killer im Leo Vince für Straße drin lassen! ~93 dB legal
- Collector-Box löschen spart 2-3 kg, verbessert Antritt

### Luftfilter-Tipps
- UNI NU-4050 ist der Adventure-Standard — 2-Lagen-Schaum, Feld-wartbar
- K&N für Street, UNI für Dirt — auf der NX650 (Adventure!) → UNI
- Reinigung alle 3.000 km auf Straße, alle 1.000 km im Staub

### ⚠️ NEU: CDI/Zündungs-Tipps
- **CDI ersetzen ist der LETZTE Schritt** — erst decomp checken, Zündspule messen, Funke prüfen
- Zündspule: Primär 2.0-3.0 Ω, Sekundär 10-18 kΩ. Messen VOR CDI-Wechsel!
- Dekomp-Ventil einstellen = KOSTENLOS und behebt oft das Hot-Start-Problem
- **Ignitech DC-CDI-P2** = DC-betrieben → kein Heat-Soak, programmierbar, 3 Zündkurven
- Ignitech hat EC-Typgenehmigung → Eintragung §19.2 möglich
- Ride Mode Controller GPIO27+GPIO33 = 3-Map Schaltung für Ignitech

---

## 9️⃣ TEAM-REQUESTS UPDATE

### ✅ Neu in diesem Run (2026-05-28 Update 2):
- **5 Teile in DB hinzugefügt:** Ignitech DC-CDI-P2 (445), Inline-Kraftstofffilter (446), Silikon-Unterdruckschläuche (447), Zündspule OEM (448), Dekomp-Ventil (449)
- **3 Build Guides aktualisiert:** MOSFET Regler #3 → active, Stator #4 → active, Carburetor #5 → planning
- **CDI-Diagnosepfad** erstellt: decomp → Zündspule → Funke → CDI (NICHT sofort CDI kaufen!)
- **Inline-Kraftstofffilter** als PFLICHT identifiziert für Ethanol-Schutz
- **Silikon-Unterdruckschläuche** als PFLICHT identifiziert bei Ruckel-Problemen

### 🔄 Offene Anfragen:
- **Chefingenieur**: Gewichtsverteilung vorne/hinten berechnen (geschätzt 55/45) → ✅ ERLEDIGT (54/46)
- **Chefingenieur**: Tank voll/leer Einfluss auf Handling (15L = ~11kg Benzin) → ✅ ERLEDIGT
- **Elektrik**: Zündschloss-Kontakte prüfen und reinigen → Einbauen in Phase 1
- **Fahrwerk**: YSS Mono Bracket Schweißen (~€50-80 lokal) → ✅ Bestätigt €65
- **Stylist**: Tank-Decals African Queen rot/blau/weiß — DIY oder DecalMX? → ✅ DIY Vinyl €13
- **Entwickler**: Ignitech DC-CDI-P2 3-Map GPIO-Pins bestätigt? → GPIO27 (Map A/B) + GPIO33 (Map B/C) ✅

### 💡 Empfehlung an Chefingenieur:
Phase 1 Budget +€19-28 (Inline-Filter €7 + Silikonschläuche €7 + evtl. Zündspule €25-65 bei Diagnose). Neue Phase 1 Total: ~€445-470 statt ~€426. Immer noch €330-355 unter Phase 1 Budget von €800!
