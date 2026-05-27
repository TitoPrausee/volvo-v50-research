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

### Budget-Guard Status
✅ **KEINE Phase überschritten!**

| Phase | Geplant | Budget | Reserve | Status |
|-------|---------|--------|---------|--------|
| 1: Zuverlässigkeit | €480 | €800 | +€320 | ✅ 40% Reserve |
| 2: Fahrwerk | €865 | €1.200 | +€335 | ✅ 28% Reserve |
| 3: Africa Twin Look | €882 | €1.000 | +€118 | ⚠️ 12% Reserve — knapp! |
| 4: Touring-Komfort | €214 | €800 | +€586 | ✅ 73% Reserve |
| 5: Reserve | — | €500 | +€500 | 🔵 Puffer |
| **Total** | **€2.441** | **€4.300** | **+€1.859** | ✅ |

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

**Phase 3 knapp (€118 Reserve):**
1. Koso RX-22 (€90) → generischer 7" H4 LED (€40) = **€50 gespart**
2. Sitzbank Sattler (€115) → DIY Umpolstern (€50) = **€65 gespart**
3. Leo Vince SBK (€345) → OEM Muffler behalten (€0) = **€345 gespart** → Budget-Option
4. Heckträger (€40) → DIY Alu-Profil (€25) = **€15 gespart**

**Phase 2 knapp (€335 Reserve):**
1. YSS Mono (€375) → Hagon Twins (€175) = **€200 gespart**, aber -0.6kg Leistung
2. Mitas E-07 (€160 Set) → Shinko 804/805 (€135 Set) = **€25 gespart**
3. Race Tech Bundle (€210) → Wirth Federn + Öl (€90) = **€120 gespart**, weniger Performance

**Phase 4 (€586 Reserve — hier ist Spielraum für Upgrades):**
- Mögliche Upgrades aus Reserve:
  - Seat Concepts Kit statt Sattler (+€85)
  - DecalMX Pro-Tank-Decals statt DIY (+€30)
  - Heidenau K60 statt Mitas E-07 (+€51)
  - Antigravity Batterie statt JMT (+€65)
  - Kriega US-20 statt Budget Panniers (+€85)

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

### 🔄 Fahrwerksspezialist benötigt:
- **Fork-Setup**: RT Emulatoren + 0.55kg/mm Federn als Bundle (~€210). Budget: Wirth Federn + frisches Öl (~€90).
- **YSS Mono Bracket**: Schweißen erforderlich (~€50-80 beim lokalen Schweißer)
- **Bremsen**: FA185HH Halbsinter reichen für Adventure. SS-Leitung ist Pflicht. 256mm OEM Scheibe reicht ✅ BESTÄTIGT

### 🔄 Elektrik-Spezialist benötigt:
- **LED-Last**: 7" H4 LED zieht ~15W (nicht 40W wie ursprünglich geschätzt). OEM Stator liefert 180W → mit FH020AA und RM Stator 200W: ausreichend Reserve. ✅
- **Kabelbaum**: Custom LED-Umbau braucht Adapterkabel (~€10-15 selbst löten)
- **Zündschloss-Kontakte**: Reinigen + Kontaktspray (Kosten: €5)
- **Zusätzlich Massekabel**: Batterie → Rahmen → Motor direkt löten (Kosten: €5-15)

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