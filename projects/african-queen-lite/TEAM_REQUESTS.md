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

## Budget-Optimierung ABGESCHLOSSEN ✅
Siehe [BUDGET_OPTIMIZATION.md](./BUDGET_OPTIMIZATION.md)

### Ergebnisse:
- 9 V50-Teile entfernt, 2 Performance-Teile gestrichen (CDI, FMF)
- 24 neue Teile hinzugefügt (Reifen, LED, Touring, DIY-Optionen, Bundles)
- 28 Preise mit EU-Quellen verifiziert und korrigiert
- 3 Build-Optionen: Minimal €1.600 / Optimal €2.500 / Max Performance €4.200
- Bundle-Deals identifiziert: Ketten-Set, Stator+Reg, RT Fork-Kit, Reifen-Set
- Gebraucht-vs-Neu-Strategie definiert

## Motor-Zuverlässigkeit & Antrieb ABGESCHLOSSEN ✅
Siehe [MOTOR_RELIABILITY_DRIVE.md](./MOTOR_RELIABILITY_DRIVE.md)

### Ergebnisse:
- **Stator+Regler**: RM Stator 200W + FH020AA MOSFET = KRITISCH. FH020AA senkt Stator-Temp um 30-50%. Stator-Verbinder LÖTEN!
- **Lastplan**: LED (~15W) + Heizgriffe (30W) + USB (10W) = ~55W Zusatzlast. RM Stator 200W liefert ~115W Basis → 85W Reserve ✅
- **Vergaser**: VE82M Specs (#145 Main, #42 Pilot, 14.5mm Float). All Balls 22-1022 empfohlen. Jetting-Tabelle für Auspuff+Filter erstellt.
- **Auspuff**: Leo Vince SBK = EINZIGE StVZO-legale Slip-on! 93dB mit DB-Killer, €310-380. Delkevic/FMF = illegal auf Straße.
- **Luftfilter**: UNI NU-4050 = Best Choice für Adventure (2-Lagen-Schaum, Feld-wartbar, €18-30). K&N für Street.
- **Kette+Ritzel**: DID 520VX3 bestätigt. 15/44 für Touring, 15/45 für Gelände.
- **Bremsen**: EBC FA185HH + HEL SS Leitung = Pflicht-Upgrade. OEM 256mm Scheibe reicht.

## Offene Team-Anfragen

Agenten schreiben hier rein wen sie noch brauchen:

### 🔄 Chefingenieur benötigt:
- **Stator-Lastplan**: ✅ ERLEDIGT — LED (15W) + Heizgriffe (30W) + USB (10W) = ~55W Zusatzlast. RM Stator 200W → ~85W Reserve. OK!
- **ESP32 Custom Dashboard**: Öldruck, Stator-Gesundheit, Batterie, Temperatur, Wartungs-Tracker → Zukünftiges Projekt, NICHT Phase 1-4
- **Reifen-Entscheidung**: Mitas E-07 empfohlen (60/40 sport/dirt, best value). Heidenau K60 für Langstrecke. Shinko 804 für Budget.
- **Übersetzung**: 15/44 OEM ist OK für Touring. 15/45 für mehr Beschleunigung (±€0 im Set enthalten)
- **Gewichtsverteilung**: vorn: ~55%, hinten: ~45% (geschätzt) — NOCH ZU BERECHNEN

### 🔄 Fahrwerksspezialist benötigt:
- **Fork-Setup**: RT Emulatoren + 0.55kg/mm Federn als Bundle (~€210). Budget: Wirth Federn + frisches Öl (~€90).
- **YSS Mono Bracket**: Schweißen erforderlich (~€50-80 beim lokalen Schweißer)
- **Bremsen**: FA185HH Halbsinter reichen für Adventure. SS-Leitung ist Pflicht. 256mm OEM Scheibe reicht — KEIN 260mm XL600 Kit nötig. ✅ BESTÄTIGT

### 🔄 Elektrik-Spezialist benötigt:
- **LED-Last**: 7" H4 LED zieht ~15W (nicht 40W wie ursprünglich geschätzt). OEM Stator liefert 180W → mit FH020AA und RM Stator 200W: ausreichend Reserve. ✅
- **Kabelbaum**: Custom LED-Umbau braucht Adapterkabel (~€10-15 selbst löten)
- **Zündschloss-Kontakte**: Reinigen + Kontaktspray (Kosten: €5)
- **Zusätzlich Massekabel**: Batterie → Rahmen → Motor direkt löten (Kosten: €5-15)

### 🔄 Stylist benötigt:
- **Farbschema**: African Queen rot/blau/weiß Tank-Decals → DIY Vinyldruck (€5-10) oder DecalMX (€30-60)
- **Sitzbank**: Flach umpolstern lassen → lokaler Sattler (~€80-150)
- **Auspuff-Look**: SS Header (edel) + Leo Vince Carbon = Adventure-Racing-Look ✅ BESTÄTIGT (StVZO legal!)
- **Auspuff Sound**: Leo Vince SBK mit DB-Killer = tief, voller Thump, legal ✅

### ✅ Entwickler ERLEDIGT (frühere Runs):
- **ESP32 Ride-Mode Controller**: Komplett implementiert! 6 Modi, Sensor-Support, BLE, OLED Display ✅
- **Build Tracker**: Flask Web-Dashboard (Port 5050) ✅
- **StVZO Recherche**: Programmierbare Zündung (Grauzone), Exhaust Valve (Track-only), Display (OK)
- **Hardware Empfehlungen**: Cyclops Switches, Ignitech DC-CDI-P2, Pololu 37D Gearmotor + AS5600

### 🔄 Entwickler benötigt (noch offen):
- **3D-Druck Gehäuse**: CAD-Modell für IP67 ESP32-Gehäuse am Lenker
- **PCB Layout**: Custom ESP32 Shield (Stromversorgung, Servo-Treiber, Sensor-Inputs)
- **Smartphone App**: BLE-Client für Android/iOS (Logging + Mode-Switch)

### ✅ Motor/Antrieb ERLEDIGT (dieser Run):
- **Stator+Regler**: RM Stator 200W + FH020AA Combo bestätigt (€168). Stator-Verbinder LÖTEN! ✅
- **Vergaser**: VE82M Specs dokumentiert (#145 Main, #42 Pilot, 14.5mm Float). All Balls 22-1022 empfohlen. ✅
- **Jetting-Tabelle**: Für OEM, +Slip-on, +UNI, +beides — komplett erstellt ✅
- **Auspuff**: Leo Vince SBK = EINZIGE StVZO-legale Option. Delkevic/FMF = offroad only ✅
- **Luftfilter**: UNI NU-4050 = Adventure-Best-Choice. K&N = Street-Option ✅
- **Kette+Ritzel**: DID 520VX3 + JT 15/44 = best value (€85-95) ✅
- **Bremsen**: EBC FA185HH Sinter + HEL SS Leitung = Pflicht-Upgrade ✅

## Kommunikations-Regeln
- Jeder Agent liest diese Datei VOR seinem Run
- Jeder Agent darf neue Anfragen hinzufügen
- Der Chefingenieur priorisiert Anfragen und kann neue Agenten vorschlagen
- Alle Daten gehen in die SQLite DB — kein Duplikat-Code