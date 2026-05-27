# 🏍️ African Queen Lite — Team Requests

## Aktuelle Team-Mitglieder

| Agent | Rolle | Intervall | Fokus |
|-------|------|-----------|-------|
| `aql-chief-engineer` | Chefingenieur | 8h | Koordination, Gewichts-Bilanz, Kompatibilität |
| `aql-suspension-handler` | Fahrwerk | 8h | Gabel, Dämpfer, Bremsen, Gewichtsverteilung |
| `aql-electrical` | Elektrik | 8h | Stator, LED, LiFePO4, Leistungs-Bilanz |
| `aql-stylist` | Design/Look | 12h | Africa-Twin-Look, Farbschema, Referenzen |
| `aql-developer` | Entwickler | 6h | Build-Tracker, Custom-Dashboard, Wiring-Diagrams, Tools |
| `aql-budget-hunter` | Preise | 6h | Günstigste Quellen, Alternativen, DIY |
| `aql-mechanic` | Motor/Antrieb | 12h | Vergaser, Übersetzung, Wartung, Sound |

+ 3 generische Forschungs-Agenten (vehicle-research, -community, -specs)

## Skill
Dieses Team basiert auf dem **mechanic-tuning-team** Skill — wiederverwendbar für jedes Fahrzeug-Projekt.
`skill_view(name='mechanic-tuning-team')`

---

## CHEFINGENIEUR UPDATE — 2026-05-27

### Budget-Guard Status (UPDATED 2026-05-27 — Preis-Check)
✅ **KEINE Phase überschritten!**

|| Phase | Geplant | Budget | Reserve | Status |
|-------|---------|--------|---------|--------|
| 1: Zuverlässigkeit | €409 | €800 | +€391 (49%) | ✅ Verbessert von +€320 |
| 2: Fahrwerk | €944 | €1.200 | +€256 (21%) | ⚠️ Mitas E-07+ Dakar teurer |
| 3: Africa Twin Look | €688 | €1.000 | +€312 (31%) | ✅ Stark verbessert von +€118! |
| 4: Touring-Komfort | €187 | €800 | +€613 (77%) | ✅ Verbessert |
| 5: Reserve | — | €500 | +€500 | 🔵 Puffer |
| **Total** | **€2.228** | **€4.300** | **+€2.072** | ✅ |

### Gewicht-Bilanz
- **Trockengewicht nach Bau:** ~155.4 kg (OEM: 161 kg) → **-5.6 kg**
- **Fahrfertig:** ~170-171 kg → **UNTER dem 175 kg Ziel!** ✅
- Größte Ersparnis: Auspuff (-3 kg), Batterie (-2 kg), LED (-1.7 kg), YSS (-1.3 kg)
- Gewichtsverteilung: vorne ~54%, hinten ~46% (ausgewogen)

### Kompatibilitäts-Checks ✅
Alle 12 Hauptkomponenten verifiziert kompatibel mit NX650 Dominator.

### Performance-Teile: KEINE ✅
Kein Big Bore, kein CDI-Upgrade, kein Leistungs-Auspuff im Build-Plan.

### Kürzungs-Vorschläge (falls Budget überschritten)

**Phase 3 (jetzt 31% Reserve — nicht mehr knapp!):**
1. Koso RX-22 (€100) → generischer 7" H4 LED (€25) = **€75 gespart**
2. Sitzbank Sattler (€150) → DIY Umpolstern (€40) = **€110 gespart**
3. Leo Vince SBK Slip-on (€215 gebraucht) → OEM Muffler behalten (€0) = **€215 gespart** → Budget-Option
4. Highsider Blinker (€55) → E9 generisch (€19) = **€36 gespart**
5. Heckträger (€30) → DIY Alu-Profil (€25) = **€5 gespart**

**Phase 2 (21% Reserve — etwas weniger Puffer):**
1. YSS Mono (€339) → Hagon Twins (€175) = **€164 gespart**, aber weniger Einstellbarkeit
2. Mitas E-07+ Dakar (€189) → Shinko 804/805 (€156) = **€33 gespart**, kürzere Haltbarkeit
3. Race Tech Emulator + Wirth (€260) → Wirth Federn allein (€83) = **€177 gespart**, nur ~40% der Wirkung
4. Acerbis Handguards (€35) → BBB MX-1 (€22) = **€13 gespart**

**Phase 4 (77% Reserve — hier ist maximaler Spielraum):**
- Mögliche Upgrades aus Reserve:
  - Seat Concepts Kit statt Sattler (+€60, bessere Qualität)
  - Antigravity Batterie statt JMT (+€60, mehr CCA, Restart-Funktion)
  - Kriega US-20 Drybag statt Budget-Panniers (+€80, besser wetterfest)
  - Heidenau K60 statt Mitas E-07 (+€73, bessere Haltbarkeit)
  - MRA Touring Windschild statt DIY (+€65, besserer Windschutz)

---

## Budget-Optimierung ABGESCHLOSSEN ✅
Siehe [BUDGET_OPTIMIZATION.md](./BUDGET_OPTIMIZATION.md)

### Ergebnisse:
- 11 Duplikate aus DB entfernt
- 24 neue Teile hinzugefügt (Reifen, LED, Touring, DIY-Optionen, Bundles)
- 28 Preise mit EU-Quellen verifiziert und korrigiert
- 3 Build-Optionen: Minimal €1.600 / Optimal €2.500 / Max Performance €4.200
- 2 Performance-Teile gestrichen (CDI-Upgrade, FMF)
- Bundle-Deals identifiziert: Ketten-Set, Stator+Reg, RT Fork-Kit, Reifen-Set
- Gebraucht-vs-Neu-Strategie definiert

## Motor-Zuverlässigkeit & Antrieb ABGESCHLOSSEN ✅
Siehe [MOTOR_RELIABILITY_DRIVE.md](./MOTOR_RELIABILITY_DRIVE.md)

### Ergebnisse:
- **Stator+Regler**: RM Stator 200W + FH020AA = KRITISCH. FH020AA senkt Stator-Temp um 30-50%. Stator-Verbinder LÖTEN!
- **Lastplan**: LED (~15W) + Heizgriffe (30W) + USB (10W) = ~55W Zusatzlast. RM Stator 200W liefert ~115W Basis → 85W Reserve ✅
- **Vergaser**: VE82M Specs (#145 Main, #42 Pilot, 14.5mm Float). All Balls 22-1022 empfohlen. Jetting-Tabelle für Auspuff+Filter erstellt.
- **Auspuff**: Leo Vince SBK = EINZIGE StVZO-legale Slip-on! 93dB mit DB-Killer, €310-380. Delkevic/FMF = illegal auf Straße.
- **Luftfilter**: UNI NU-4050 = Best Choice für Adventure (2-Lagen-Schaum, Feld-wartbar, €18-30). K&N für Street.
- **Kette+Ritzel**: DID 520VX3 bestätigt. 15/44 für Touring, 15/45 für Gelände.
- **Bremsen**: EBC FA185HH + HEL SS Leitung = Pflicht-Upgrade. OEM 256mm Scheibe reicht.

## Styling & Sound ABGESCHLOSSEN ✅
Siehe [STYLING_SOUND.md](./STYLING_SOUND.md)

### Ergebnisse:
- **Auspuff Strategie**: OPTIMAL = Delkevic SS Header + Leo Vince SBK Slip-on (€460-580, -3kg, 93dB, StVZO-legal) ✅
- **Farbschema**: Tricolor Weiß #F5F5F5 / Rot #C8102E / Blau #003DA5 / Schwarz #1A1A1A ✅
- **Africa Twin Design-Elemente**: 10 Schlüsselelemente identifiziert ✅
- **Sitzbank**: Flach umpolstern, Gripper-Vinyl, rote Stepp-Naht. Sattler €100-150 ✅
- **LED-Umbau**: Koso RX-22 7" LED + DRL-Ring = Africa Twin Look. -1.7kg Total ✅
- **Weight-Bilanz**: Netto -5.6kg (trocken). Ziel 175-180kg erreicht ✅
- **Phase 3 Budget**: 3 Optionen — Optimal €797-882, Budget €335-487, Max-Style €1.000-1.200 ✅

---

## Offene Team-Anfragen

Agenten schreiben hier rein wen sie noch brauchen:

### 🔄 Chefingenieur benötigt:
- **Stator-Lastplan**: ✅ ERLEDIGT — LED (15W) + Heizgriffe (30W) + USB (10W) = ~55W Zusatzlast. RM Stator 200W → ~85W Reserve. OK!
- **ESP32 Custom Dashboard**: Öldruck, Stator-Gesundheit, Batterie, Temperatur, Wartungs-Tracker → Zukünftiges Projekt, NICHT Phase 1-4
- **Reifen-Entscheidung**: Mitas E-07 empfohlen (60/40 sport/dirt, best value). Heidenau K60 für Langstrecke. Shinko 804 für Budget.
- **Übersetzung**: 15/44 OEM ist OK für Touring. 15/45 für mehr Beschleunigung (±€0 im Set enthalten)
- **Gewichtsverteilung**: ✅ ERLEDIGT — vorne: ~54%, hinten: ~46% (modifiziert durch LED und Auspuff)

### ✅ Fahrwerksspezialist ERLEDIGT (2026-05-27):
- **Fork-Setup**: RT FEGV S4101 Emulator (210€) + Wirth 0.55kg/mm Federn (80€) + Motul 5W Öl (17€) = **307€**. Budget-Alternative: Wirth Federn allein (~97€, nur ~40% der Wirkung).
  - Race Tech Bundle (Emulator+RT Federn) = 268€ bei LM.de → Wirth separat (290€) = kein Bundle-Vorteil
  - ❌ FEGV S4101D Dual-Rate (244€) = OVERKILL für NX650, standard S4101 reicht
- **Heck**: YSS Z-366 Mono (279€) + Bracket (45€) + Schweißen (50-80€) = **~374€** ✅ BESTE Wahl
  - Budget-Alt: YSS Z367 Twin (169€, Direkt-Bolt-on, +0.3kg schwerer, weniger Leistung)
  - Hagon Nitrostar Twin (175€) = Alternative zu YSS Twin
  - ❌ Öhlins = NICHT verfügbar für NX650! Custom only, 800€+
  - ❌ Wilbers = Custom Bestellung, 500-700€, über Budget
- **Bremsen**: EBC FA185HH (25€) + Venhill SS Leitung (47€) + ATE TYP200 DOT4 (10€) = **82€** ⭐ BESTES Preis/Leistung
  - 260mm Disc Kit = ❌ SCHLECHTES Preis/Leistung (350€ für +1.5% Bremsmoment)
  - OEM 256mm Scheibe reicht für 161kg Bike!
  - Hintere Trommelbremse: EBC 396 Schuhe (16€), kein Upgrade nötig
- **Reifen**: Mitas E-07 Set (177€) + HD-Schläuche (40€) = **~217€** ⭐ BEST VALUE
  - Alternativ: Shinko 804/805 (146€, kürzere Haltbarkeit), Heidenau K60 (262€, beste Haltbarkeit aber schlechte Nässe)
  - ⚠️ NX650 hat Speichenfelgen = SCHLAUCH-PFLICHT!
- **Phase 2 Total**: ~980€ (Option A Optimal) → **220€ Reserve** ✅

### ✅ Elektrik-Spezialist ERLEDIGT (2026-05-27):
- **Stator:** RM Stator 200W Standard (€95-120) BEST BUY, Heavy Duty (€130-160) nur bei Volllast nötig
- **Regler:** FH020AA MOSFET (€55-65) = KRITISCH, senkt Stator-Temp 30-50%
- **Stator+Regler Combo:** RM Stator + FH020AA = ~€168 (bestes P/L)
- **Leistungs-Bilanz:** Nach LED-Umbau: 97W Verbrauch @ 5000rpm, 200W Stator = **103W Reserve** ✅
- **LED Scheinwerfer:** Koso RX-22 E-marked (~€200) BESTES Preis/Leistung, spart 35W+1.5kg
  - Premium: JW Speaker 8700 Evo (€320-389) — bester Beam
  - Adventure: Truck-Lite 30400 (€248-279) — IP68, robusteste
  - Budget: Generic 7" H4 LED (€25-50) — ⚠️ meist KEIN E-Mark!
- **LED Blinker:** Highsider Saturn/Kansas E9 Set (€55-79) = beste E-Mark-Qualität
  - Spart 76-78W vs OEM Halogen! LED Relay zwingend (~€10-15)
- **LED Rücklicht:** Highsider LED E9 (€35-55) = zuverlässig + E-marked
- **LiFePO4 Batterie:** Antigravity YTZ10-12 (€135-170) BESTE, JMT YTZ10S (€50-75) BUDGET
  - Spart ~2kg vs Blei-Säure. Kickstart → CCA weniger kritisch
- **Gewichtsersparnis LED-Umbau:** -3.94kg (Scheinwerfer -1.5, Blinker -0.26, Rücklicht -0.18, Batterie -2.0)
- **Elektrik Budget Total:** P1 €168 + P3 €311 + P4 €139 = **€618** (Reserve: €182) ✅
- **Kabelbaum:** Custom LED-Umbau braucht Adapterkabel (~€10-15 selbst löten)
- **Zündschloss-Kontakte**: Reinigen + Kontaktspray (Kosten: €5)
- **Massekabel:** Ground Cable Kit Batterie-Rahmen-Motor (~€10, selbst löten!)

### ✅ Styling+Sound ERLEDIGT:
- Alle Styling-Entscheidungen dokumentiert ✅
- Phase 3 Budget-Optionen erstellt ✅
- Farbschema und Design-Elemente definiert ✅

### ✅ Entwickler ERLEDIGT:
- ESP32 Ride-Mode Controller implementiert ✅
- Build Tracker Flask Web-Dashboard ✅

### 🔄 Entwickler benötigt (noch offen):
- **3D-Druck Gehäuse**: CAD-Modell für IP67 ESP32-Gehäuse am Lenker
- **PCB Layout**: Custom ESP32 Shield (Stromversorgung, Servo-Treiber, Sensor-Inputs)
- **Smartphone App**: BLE-Client für Android/iOS (Logging + Mode-Switch)

### ✅ Motor/Antrieb ERLEDIGT:
- Stator+Regler Combo bestätigt ✅
- Vergaser VE82M Specs + Jetting-Tabelle ✅
- Auspuff Leo Vince SBK = EINZIGE legale Option ✅
- Kette+Ritzel DID 520VX3 + JT 15/44 ✅
- Bremsen EBC FA185HH + HEL SS ✅

## ✅ Budget-Jäger PREIS-CHECK ERLEDIGT (2026-05-27)

### Ergebnisse:
- **Alle Preise mit 3+ EU-Quellen verifiziert** (FC-Moto, Motea, Louis, Amazon.de, eBay.de, YSS-Store.de, Reiff-Moto, Delkevic EU)
- **Neue Best-Preise gefunden:** Phase 1 ~€409 (vorher ~€422-480), Phase 2 ~€944, Phase 3 ~€688, Phase 4 ~€187
- **Gesamt Option A:** €2,228 (vorher ~€2,505) = **€277 Ersparnis!**
- **Bundle Deals:** Ketten-Set spart €27 (Motea), Race Tech Bundle spart €15 (FC-Moto), Mitas Set spart €10 (Reiff)
- **Neue Budget-Alternativen:** Generisch 7" LED €25 vs Koso €100, Hagon Twins €175 vs YSS Mono €339, Shinko 804/805 €156 vs Mitas €189
- **Gebraucht-Quellen:** Leo Vince Slip-on gebraucht €215 (vs neu €329-385), SW-Motech Haube gebraucht €65 (vs neu €110-175)
- **Phase 3 jetzt bequem:** €688 / €1,000 = 31% Reserve (vorher nur 12%!)
- **Koso RX-22 Preis korrigiert:** €99.90 (FC-Moto), nicht €200+ wie ursprünglich geschätzt

### Budget-Guard Update:

| Phase | Vorher | Jetzt | Reserve | Status |
|-------|--------|-------|---------|--------|
| 1: Zuverlässigkeit | €480 | **€409** | **+€391 (49%)** | ✅ Verbessert |
| 2: Fahrwerk | €865 | **€944** | **+€256 (21%)** | ⚠️ Höher durch Mitas E-07+ Dakar |
| 3: Africa Twin Look | €882 | **€688** | **+€312 (31%)** | ✅ Stark verbessert |
| 4: Touring-Komfort | €214 | **€187** | **+€613 (77%)** | ✅ Verbessert |
| **Total** | **€2,441** | **€2,228** | **+€2,072** | ✅ |

Siehe [BUDGET_OPTIMIZATION.md](./BUDGET_OPTIMIZATION.md) für vollständige Details.

---

## Neue Team-Erweiterungsvorschläge

### Potenzielle neue Agenten:

| Agent | Fokus | Begründung |
|-------|-------|-------------|
| `aql-touring-specialist` | Touring-Ausrüstung, Packliste, Ergonomie | Phase 4 hat viel Reserve (€586) → maximieren! |
| `aql-tuv-registration` | StVZO, TÜV, Eintragung, Papierrechte | Auspuff+LED brauchen Eintragung → Rechtssicherheit |
| `aql-diy-fabricator` | DIY-Projekte, Polycarbonat, Vinyl, Schweißen | 11 DIY-Projekte identifiziert, €500-1000 Ersparnis |

## Kommunikations-Regeln
- Jeder Agent liest diese Datei VOR seinem Run
- Jeder Agent darf neue Anfragen hinzufügen
- Der Chefingenieur priorisiert Anfragen und kann neue Agenten vorschlagen
- Alle Daten gehen in die SQLite DB — kein Duplikat-Code