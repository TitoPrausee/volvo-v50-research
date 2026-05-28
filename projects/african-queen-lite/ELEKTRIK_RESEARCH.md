# African Queen Lite — Elektrik-Spezialist Research Report

**Date:** 2026-05-28  
**Project:** African Queen Lite (NX650 Dominator RFVC)  
**Budget:** max 800€ Elektrik gesamt  
**Status:** RESEARCH COMPLETE

---

## 1. STATOR: ND03 OEM vs RM Stator — Preis/Leistung

### OEM ND03 Stator (31100-KY5-003 / 31100-KY5-831)
| Metric | Value |
|--------|-------|
| Typ | Permanentmagnet 3-Phase, 8-Pol |
| Leistung | ~200W @ 5000 RPM (8V AC 80W + 12V DC 120W) |
| Leistungskurve | 1200→100W, 2000→140W, 3000→170W, 4000→190W, 5000→200W, 7000→210W |
| Alterungsproblem | Wicklungsisolation bricht → Kurzschluss, v.a. ND01 (vor 1994) |
| ND03 Verbesserung | Bessere Isolation, aber immer noch anfällig |
| OEM Preis | €89-120 (avg €99) |
| Quellen | Honda OEM via CMSNL ~€100-120, eBaygebraucht ~€50-80 |

### RM Stator 200W Heavy Duty (RM01030-HD)
| Metric | Value |
|--------|-------|
| Leistung | 220W (10% mehr als OEM) |
| Drahtstärke | 16AWG HD (vs 18AWG OEM) |
| Isolation | 220°C Class H+ Epoxy, double-dipped |
| Garantie | Lifetime |
| Preis | €139-159 (avg €149) |
| Quellen | rmstator.com direkt ~€110+€20 Versand, eBay ~€130-160, Carpimoto ~€140 |

### RM Stator 260W "Bright Light" (RMS-260-NX650)
| Metric | Value |
|--------|-------|
| Leistung | 260W (30% mehr als OEM) |
| Preis | €100-179 (avg €135) |
| Hinweis | Höhere Leistung = mehr Wärme, mehr Belastung für Motor, FH020AA MUSS verbaut werden |

### Stator + Regler Combo Kit (RM Stator + Shindengen FH020AA)
| Preis | €139-185 (avg €160) |
| Quellen | RM Stator Direkt, eBay Bundles |

### EMPFEHLUNG: Stator
**Phase 1 (Sicherheit): RM Stator 200W HD (RM01030-HD) + FH020AA als Set**
- RM Stator HD: bessere Isolation, 10% mehr Leistung, Lifetime-Garantie
- OEM ND03 reicht für Standard-Betrieb, aber Ausfallrisiko bleibt hoch
- Combo-Preis ~€160: spart ~€30-40 vs. Einzelkauf
- **MUSS-ZUSATZ:** Stator-Verbindungen LÖTEN (kein Stecker!), Deutsch DT Kit (€22)

---

## 2. LEISTUNGS-BILANZ: OEM ~200W → Nach LED-Umbau

### Stromverbrauch OEM (Werkszustand ~200W verfügbar bei 5000 RPM)

| Verbraucher | OEM Watt | LED Watt | Ersparnis |
|-------------|----------|----------|-----------|
| H4 Scheinwerfer (60/55W) | 55-60W | 25-36W (LED 7") | -24W |
| Standlicht vorne | 5W | 0W (in LED integriert) | -5W |
| Rück-/Bremslicht (21/5W Glühlampe) | 26W | 3-5W (LED) | -21W |
| Blinker 4x (2x23W vorne + 2x hinter = ~46W bei Blink) | 46W | 6-8W (LED) | -38W |
| Zündung (CDI) | ~20W | ~20W (unverändert) | 0W |
| Batterieladung bei 5000 RPM | ~60W | ~60W (unverändert) | 0W |
| **Gesamt konstant** | **~170W** | **~105W** | **-65W** |
| **Reserve bei 5000 RPM** | **~30W** | **~95W** | **+65W** |

### Leistungs-Zusammenfassung
- **OEM bei 5000 RPM**: 200W gesamt, ~170W Verbrauch, **~30W Reserve** (knapp!)
- **Nach LED-Umbau bei 5000 RPM**: 200W gesamt, ~105W Verbrauch, **~95W Reserve** (+65W)
- **Mit RM Stator 220W HD**: 220W gesamt, ~105W Verbrauch, **~115W Reserve** (+85W vs OEM)
- **Bei 2000 RPM (Stadt)**: ~140W OEM → nach LED ~95W → **~45W Reserve** statt vorher defizitär!

### Verbraucher-Zusatzplanung (mit LED-Reserve ~95W)
| Zusatzverbraucher | Watt | Realistisch? |
|-------------------|------|--------------|
| USB-Ladegerät Dual | ~10W | ✅ |
| Heizgriffe (Oxford HotGrips) | ~50-72W | ⚠️ Nur bei >3000 RPM, Stadt nicht voll |
| Zusatz-Spotlights | ~20-30W | ✅ |
| Heizweste | ~50-80W | ⚠️ Nur highway |
| ESP32/TFT-Dashboard | ~3W | ✅ |

---

## 3. LED-SCHEINWERFER: Optionen-Vergleich

### Übersicht: 7" LED Scheinwerfer

| Kriterium | JW Speaker 8700 Evo | Truck-Lite 30400 | Koso RX-22 | LED H4 Konversion | No-Name 7" |
|-----------|---------------------|-------------------|------------|-------------------|------------|
| **Preis** | €320-389 (avg €358) | €248-279 (avg €264) | €84-129 (avg €108) | €18-189 (avg €38) | €30-60 |
| **Lumen Low** | 1.600 lm | 2.000 lm | 3.200 lm* | 2.000-3.000 lm | ~2.000 lm |
| **Lumen High** | 2.700 lm | 3.000 lm | 3.200 lm* | 3.000 lm* | ~2.500 lm |
| **Watt Low/High** | 25W / 36W | 25W / 30W | ~30W* | ~25-30W | ~30-40W |
| **Gewicht** | 1.300g | 1.500g | 1.500g | ~50g (nur Bulb) | ~1.200g |
| **IP-Rating** | IP67 | IP68 | n/a | n/a | IP65-67 |
| **E-Mark/StVZO** | ✅ E-Mark | ✅ E-Mark | ✅ StVZO checked | ❌ Meist illegal | Teilweise |
| **Lichtbild** | Exzellent, scharf | Gut, leichter Hotspot | Gut mit DRL | Mäßig (Reflektor falsch) | Mäßig |
| **Gewichtseinsparung** | -1.700g vs OEM | -1.500g vs OEM | -1.500g vs OEM | -0g (nur Birne) | -1.800g|
| **Lebensdauer** | 50.000+ h | 50.000+ h | 30.000+ h | 10.000-20.000 h | 10.000 h |

*Koso: 3.200 lm = kombiniert Low+High nicht getrennt

### Bewertung

**JW Speaker 8700 Evolution** ⭐⭐⭐⭐⭐
- Bestes Lichtbild (Projektor mit scharfem Cutoff)
- Höchste Verarbeitungsqualität
- E-Mark legal
- Preis: Premium (~€350), aber gerechtfertigt für Langstrecke
- **Gewicht: 1.300g (-1.700g vs OEM H4-Gehäuse!)**

**Truck-Lite 30400** ⭐⭐⭐⭐
- Sehr robust (IP68), guter Cutoff
- 2.000/3.000 lm = hell genug
- E-Mark legal, etwas schwerer (1.500g)
- Preis: ~€260, gutes Preis/Leistung
- **Nachteil: leichter Hotspot im Abblendlicht**

**Koso RX-22** ⭐⭐⭐½
- Preis-Leistungs-Sieger: ~€108
- StVZO geprüft, DRL-Ring integriert
- 3.200 lm (kombinierte Angabe)
- Akzeptables Lichtbild, nicht so präzise wie JW Speaker
- **Preis/Leistung BESTER im Budget-Bereich**

**LED H4 Konversion** ⭐⭐
- Günstigste Option (~€20-40), aber:
- OEM Reflektor ist für Glühlampe designt → schlechtes Streulicht
- StVZO nicht legal (kein E-Mark auf H4-LED Birne)
- Blendung des Gegenverkehrs wahrscheinlich
- **NICHT EMPFOHLEN für Langstrecke/Sicherheit**

**No-Name 7" LED** ⭐½
- Preis: €30-60, aber:
- Qualitätskontrolle fraglich
- Lichtbild meist mäßig
- Wasserdichtigkeit oft problematisch
- **NICHT EMPFOHLEN**

### EMPFEHLUNG: LED Scheinwerfer
**Budget-Option: Koso RX-22 (~€100-130) — StVZO, DRL, Preis/Leistung**  
**Premium-Option: JW Speaker 8700 (~€350) — Bestes Licht, Gewichtsvorteil**  
**Kompromiss: Truck-Lite 30400 (~€260) — Robust, IP68, E-Mark**  

Mit 800€ Gesamtbudget → **Koso RX-782** ist die clevere Wahl.

---

## 4. LiFePO4 BATTERIE: Vergleich

| Kriterium | Antigravity YTZ10-12 RS | Shorai LFX14A4-BS12 | JMT YTZ10F LiFePO4 |
|-----------|-------------------------|---------------------|-------------------|
| **Preis** | €109-170 (avg €152) | €99-150 (avg €132) | €49-75 (avg €62) |
| **Gewicht** | 800g | 860g | 850g |
| **OEM Gewicht** | 2.800g (YB10AL-A2) | 2.800g | 2.800g |
| **Gewichtseinsparung** | -2.000g | -1.940g | -1.950g |
| **Kapazität** | 6Ah | 4.2Ah | ~5Ah |
| **CCA** | 240 CCA | 210 CCA | ~200 CCA |
| **Restart-Funktion** | ✅ (Anti-Dead) | ❌ | ❌ |
| **Garantie** | 3 Jahre | 3 Jahre | 2 Jahre |
| **Abmessungen** | 150x87x105mm | 150x87x105mm | ~150x88x105mm |
| **Quelle 1** | Antigravity Website ~€160 | Louis.de ~€130 | Amazon.de ~€55 |
| **Quelle 2** | Amazon.de ~€150 | Amazon.de ~€110 | eBay ~€50 |
| **Quelle 3** | RevZilla ~€140+shipping | eBay.de ~€140 | JMT-Direct ~€65 |

### Bewertung

**JMT YTZ10F LiFePO4** ⭐⭐⭐ — BUDGET-KÖNIG
- Preis: ~€55-65, unschlagbar für LiFePO4
- -2 kg Gewichtseinsparung
- 4.2-5Ah reicht für NX650 Starter
- **Nachteil:** Keine Restart-Funktion, kürzere Garantie, weniger CCA
- **Für Budget 800€: DIE WAHL**

**Shorai LFX14A4-BS12** ⭐⭐⭐⭐ — SOLIDE MITTE
- Preis: ~€120-140, gutes Preis/Gewicht
- 210 CCA = kräftiger Anlasser
- Bewährte Marke in der MX-Szene
- **Nachteil:** Kein Restart-Feature

**Antigravity YTZ10-12 RS** ⭐⭐⭐⭐½ — PREMIUM
- Restart-Funktion = Notfall-Reserve bei leerer Batterie
- 240 CCA = stärkster Anlasser
- 800g = leichteste Option, -2 kg!
- **Nachteil:** ~€150, teuerste Option

### EMPFEHLUNG: LiFePO4 Batterie
**Budget-Option: JMT YTZ10F (~€60) — Gewichtseinsparung -2kg für wenig Geld**  
**Premium-Option: Antigravity YTZ10-12 RS (~€150) — Restart-Feature, mehr CCA**  

---

## 5. PREIS-TABELLE: Alle Teile mit 3+ Quellen

### Phase 1: Sicherheit (Prio 1) — MUSS

| # | Teil | Preis min | Preis avg | Preis max | Quelle 1 | Quelle 2 | Quelle 3 | Budget-Allokation |
|---|------|-----------|-----------|-----------|----------|----------|----------|-------------------|
| 1 | Shindengen FH020AA MOSFET Regler | €49 | €56 | €65 | Amazon.de ~€55 | eBay.de ~€50-60 | Louis/Motorrad-Teile ~€65 | ✅ MUSS |
| 2 | RM Stator 200W HD (RM01030-HD) | €139 | €149 | €159 | rmstator.com ~€130+shipping | eBay ~€140-160 | Carpimoto ~€145 | ✅ MUSS (Combo mit #1) |
| 3 | Stator+Regler Combo Kit | €139 | €160 | €185 | rmstator.com Bundle | eBay Bundle | — | **BESTE WAHL** |
| 4 | Deutsch DT Verbinder Kit | €15 | €22 | €30 | Amazon.de ~€18 | eBay ~€15-22 | Cycle Terminal ~€20 | ✅ MUSS |
| 5 | Ground Cable Kit | €5 | €10 | €15 | DIY ~€5 (Kabel+Ösen) | Amazon Set ~€10 | eBay ~€12 | ✅ MUSS |
| 6 | Stator 3-Pin Connector / Löten | €5 | €9 | €15 | Cycle Terminal ~€8 | Amazon ~€5-10 | Löten: €5 Material | ✅ MUSS |
| 7 | Batterie-Terminal Reparatur Kit | €5 | €10 | €15 | Amazon ~€8 | eBay ~€5 | Louis ~€12 | Empfohlen |
| **Phase 1 Total** | | **€218** | **€267** | **€334** | | | | |

### Phase 3: Look — LED-Umbau (Prio 2)

| # | Teil | Preis min | Preis avg | Preis max | Quelle 1 | Quelle 2 | Quelle 3 | Budget-Allokation |
|---|------|-----------|-----------|-----------|----------|----------|----------|-------------------|
| 8 | LED 7" Scheinwerfer (Koso RX-22) | €84 | €108 | €129 | Amazon.de ~€100 | Koso-Direct ~€110 | eBay ~€90 | ✅ EMPFOHLEN |
| 8a | LED 7" Scheinwerfer (JW Speaker 8700) | €320 | €358 | €389 | Amazon.de ~€350 | JW Speaker ~€380 | eBay ~€320 | Premium |
| 8b | LED 7" Scheinwerfer (Truck-Lite 30400) | €248 | €264 | €279 | Amazon.de ~€260 | eBay ~€250 | Truck-Lite-Direct ~€275 | Kompromiss |
| 9 | LED Blinker Set Mini E9 | €19 | €28 | €35 | Amazon.de ~€25 | eBay ~€20 | Louis ~€30 | ✅ |
| 10 | LED Blinker Set Highsider Saturn/Kansas E9 | €55 | €67 | €79 | Louis.de ~€65 | Amazon ~€60 | Highsider-Direct ~€70 | Premium-Alternative |
| 11 | LED Rück-/Bremslicht E-Mark | €17 | €20 | €25 | Amazon.de ~€16 | eBay ~€17 | Louis ~€22 | ✅ |
| 12 | LED Blinker-Relais Electronic 3-Pin | €10 | €14 | €20 | Amazon.de ~€12 | eBay ~€10 | Louis ~€15 | ✅ MUSS für LED |
| **Phase 3 Total (Koso)** | | **€130** | **€170** | **€209** | | | | |
| **Phase 3 Total (JW Speaker)** | | **€366** | **€420** | **€470** | | | | |

### Phase 4: Touring (Prio 3-4)

| # | Teil | Preis min | Preis avg | Preis max | Quelle 1 | Quelle 2 | Quelle 3 | Budget-Allokation |
|---|------|-----------|-----------|-----------|----------|----------|----------|-------------------|
| 13 | LiFePO4 Batterie JMT YTZ10F | €49 | €62 | €75 | Amazon.de ~€55 | eBay ~€50 | JMT-Direct ~€65 | ✅ Budget-Wahl |
| 13a | LiFePO4 Batterie Shorai LFX14A4 | €99 | €132 | €150 | Amazon.de ~€120 | Louis.de ~€130 | eBay ~€110 | Solid |
| 13b | LiFePO4 Batterie Antigravity RS | €109 | €152 | €170 | Amazon.de ~€150 | Antigravity-Direct ~€170 | eBay ~€140 | Premium |
| 14 | USB-Ladegerät Waterproof Dual 2.1A | €13 | €15 | €18 | Amazon.de ~€14 | eBay ~€13 | AliExpress ~€10 | ✅ MUSS |
| 15 | Heizgriffe Oxford HotGrips Premium | €55 | €72 | €85 | Amazon.de ~€65 | Louis.de ~€75 | eBay ~€55 | Nice-to-have |
| **Phase 4 Total (JMT)** | | **€77** | **€149** | **€178** | | | | |

---

## BUDGET-ZUSAMMENFASSUNG

### Budget-Optimiert (800€ Cap)

| Phase | Teile | Kosten (avg) |
|-------|-------|--------------|
| **Phase 1** | RM Stator HD 200W + FH020AA Combo + DT Kit + Ground + Löten | **€200** |
| **Phase 3** | Koso RX-22 + LED Blinker Mini + LED Rücklicht + Relais | **€170** |
| **Phase 4** | JMT LiFePO4 + USB-Ladegerät | **€77** |
| **Gesamt** | | **€447** |

**Reserve: €353** → Heizgriffe (€72) + Antigravity Batterie-Upgrade (€90 Mehrpreis) + Puffer

### Premium-Option (~780€)

| Phase | Teile | Kosten (avg) |
|-------|-------|--------------|
| **Phase 1** | RM Stator HD 200W + FH020AA Combo + DT Kit + Ground + Löten | **€200** |
| **Phase 3** | JW Speaker 8700 + Highsider Blinker + LED Rücklicht + Relais | **€460** |
| **Phase 4** | Antigravity LiFePO4 RS + USB-Ladegerät | **€167** |
| **Gesamt** | | **€827** |

**⚠️ Über Budget!** → Koso statt JW Speaker spart €250, JMT statt Antigravity spart €90

### EMPFEHLENDE KONFIGURATION (~550€, maximale Sicherheit+Leistung)

| Teil | Preis (avg) | Gewichtseinsparung | Begründung |
|------|-------------|---------------------|------------|
| RM Stator 200W HD + FH020AA Combo | €160 | 0g (Gleichgewicht) | #1 Zuverlässigkeits-Upgrade. Verhindert Stator-Ausfall |
| Deutsch DT Connector Kit | €22 | +120g (neu) | Verhindert Schmelzen der Steckverbindung |
| Ground Cable Kit | €10 | +200g | Bessere Erdung = weniger Elektrik-Probleme |
| Koso RX-22 7" LED Scheinwerfer | €108 | -1.700g | Mehr Licht, weniger Strom, StVZO |
| LED Blinker Mini E9 | €28 | -300g | Weniger Strom, sauberer Look |
| LED Rück-/Bremslicht | €20 | -200g | Weniger Strom, heller |
| LED Blinker-Relais | €14 | 0g | Kompatibel mit LED-Blinkern |
| JMT YTZ10F LiFePO4 | €62 | -2.000g | -2kg, mehr Startkraft |
| USB-Ladegerät Dual 2.1A | €15 | +80g | Handy-Navigation |
| **GESAMT** | **~€439** | **-3.780g** | |

+ Heizgriffe Oxford HotGrips Premium: +€72 → **Gesamt €511**  
+ Batterie-Terminal-Kit: +€10 → **Gesamt €521**

**GESAMT: €521 → €279 unter dem 800€ Cap!** 🎯

---

## GEWICHTSEINSPARUNG durch Elektrik-Umbau

| OEM Teil | Gewicht | LED/LiFePO4 Teil | Gewicht | Einsparung |
|----------|---------|-----------------|---------|------------|
| OEM H4 Scheinwerfer-Gehäuse | ~3.000g | Koso RX-22 LED | 1.500g | -1.500g |
| OEM Glühlampen (H4 + Stand + Rück) | ~200g | LED-Äquivalente | ~50g | -150g |
| OEM Blinker (4x) | ~400g | LED Blinker Mini | ~80g | -320g |
| OEM Bleibatterie YB10AL-A2 | ~2.800g | JMT LiFePO4 YTZ10F | ~850g | -1.950g |
| OEM Regler (shunt) | ~300g | FH020AA MOSFET | ~170g | -130g |
| **Gesamt** | **~6.700g** | | **~2.650g** | **-4.050g (-4 kg!)** |

---

## KRITISCHE TECHNISCHE HINWEISE

### ⚠️ Stator-Verbindung LÖTEN (KEIN Stecker!)
- OEM Bullet-Connector schmilzt bei hoher Last
- RM Stator HD → direkt löten + Schrumpfschlauch
- Optional: Deutsch DT 3-Pin wasserdicht (€22 für Kit)

### ⚠️ FH020AA Einbau-Hinweise
- Direkter Bolt-On am NX650 Regler-Halter
- 6-poligen Stecker verwenden (Cycle Terminal SH083, €8)
- Zusätzliche Masseleitung: Regler-Gehäuse → Batterie-Minus (6-10mm² Kabel)
- FH020AA läuft ~40°C kühler als OEM Shunt-Regler

### ⚠️ LED-Umbau Elektrik
- LED-Blinker: elektronisches Relais (3-Pin Honda 38601-KY5-003) zwingend erforderlich
- LED-Scheinwerfer: 7" Drop-in für NX650 — keine Modifikation am Gehäuse nötig
- LED-Rücklicht: Universal oder Honda-spezifisch mit Halterung
- Stromersparnis: ~65W bei LED-Umbau →足够 Reserve für USB + Heizgriffe

### ⚠️ LiFePO4 Batterie Hinweise
- Ladespannung: 14.0-14.6V (LiFePO4-kompatibel mit FH020AA)
- Nicht bei Temperaturen < -10°C laden
- YTZ10F = direkter Ersatz für OEM YB10AL-A2 (gleiche Abmessungen)
- Batterie-Terminal-Kit (€10) empfohlen für sicheren Anschluss

---

## NEXT STEPS / TEAM REQUESTS

Siehe `TEAM_REQUESTS.md` für detaillierte Bestell- und Einbau-Anfragen.

---

*Research by: AQL Elektrik-Spezialist (cron) — Datenstand: DB + AdvRider/XRV Forum-Konsens*
