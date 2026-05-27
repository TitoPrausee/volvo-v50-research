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

## Offene Team-Anfragen

Agenten schreiben hier rein wen sie noch brauchen:

### 🔄 Chefingenieur benötigt:
- **Stator-Lastplan**: LED (40W) + Heizgriffe (30W) + USB (10W) = 80W Zusatzlast. Stator liefert 150W → 70W Reserve. OK! ✅
- **ESP32 Custom Dashboard**: Öldruck, Stator-Gesundheit, Batterie, Temperatur, Wartungs-Tracker → Zukünftiges Projekt, NICHT Phase 1-4
- **Reifen-Entscheidung**: Mitas E-07 empfohlen (60/40 sport/dirt, best value). Heidenau K60 für Langstrecke. Shinko 804 für Budget.
- **Übersetzung**: 15/44 OEM ist OK für Touring. 15/45 für mehr Beschleunigung (±€0 im Set enthalten)

### 🔄 Fahrwerksspezialist benötigt:
- **Fork-Setup**: RT Emulatoren + 0.55kg/mm Federn als Bundle (~€210). Budget: Wirth Federn + frisches Öl (~€90).
- **YSS Mono Bracket**: Schweißen erforderlich (~€50-80 beim lokalen Schweißer)
- **Bremsen**: FA185HH Halbsinter reichen für Adventure. SS-Leitung ist Pflicht. 256mm OEM Scheibe reicht — KEIN 260mm XL600 Kit nötig.

### 🔄 Elektrik-Spezialist benötigt:
- **LED-Last**: 7" H4 LED zieht ~30-40W. OEM Stator liefert 150W. Mit allem (Griffe, USB) sind wir bei ~80W Zusatzlast. Genug Reserve. ✅
- **Kabelbaum**: Custom LED-Umbau braucht Adapterkabel (~€10-15 selbst löten)

### 🔄 Stylist benötigt:
- **Farbschema**: African Queen rot/blau/weiß Tank-Decals → DIY Vinyldruck (€5-10) oder DecalMX (€30-60)
- **Sitzbank**: Flach umpolstern lassen → lokaler Sattler (~€80-150)
- **Auspuff-Look**: SS Header (edel) + Carbon/Alu Slip-on → Adventure-Racing-Look

### 🔄 Entwickler benötigt:
- **UI/UX-Feedback**: Build-Tracker als Web-Dashboard → Zukünftig
- **ESP32-Dashboard**: Siehe oben, nicht Phase 1-4
- **Gebrauchtteile-Scout**: eBay.de/Kleinanzeigen für Engine Guard, Auspuff, Sitzbank → Budget-Hunter hat recherchiert ✅

### 🔄 Motor/Antrieb benötigt:
- **Vergaser VE82M**: All Balls Kit (€28-35) reicht für Rebuild. Nebel und Unterdruckschläuche prüfen!
- **Kette+Ritzel**: DID 520VX3 Bundle (€87.50 Motea) ist best value. 15/44 für Touring, 15/45 für mehr Bums.
- **~~Big Bore~~**: GESTRICHEN. 44PS reichen! Siehe README.

## Kommunikations-Regeln
- Jeder Agent liest diese Datei VOR seinem Run
- Jeder Agent darf neue Anfragen hinzufügen
- Der Chefingenieur priorisiert Anfragen und kann neue Agenten vorschlagen
- Alle Daten gehen in die SQLite DB — kein Duplikat-Code