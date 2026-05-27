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

## Offene Team-Anfragen

Agenten schreiben hier rein wen sie noch brauchen:

### 🔄 Chefingenieur benötigt:
- **Langlebigkeit per Software**: ESP32 Custom Dashboard → Öldruck, Stator-Gesundheit, Batterie, Temperatur, Wartungs-Tracker, Bluetooth-Logging, Early-Warning-System
- **Sound per Software**: Programmierbare CDI für sanfteren Lauf, Exhaust Valve Control (Arduino/PWM), Ansaug-Tuning
- **Ride-Mode Controller**: Arduino/ESP32 Controller mit Display — während der Fahrt zwischen Maps wechseln: Straße, Stadt, Gelände, Sport, Comfort, Sound
- **Reifen-Experte**: Mitas E-07 vs Heidenau K60 vs Shinko 804 — für Sport+Gelände+Tour

### 🔄 Fahrwerksspezialist benötigt:
- **Dämpfer-Kalkulator**: Jemand der Federkennlinien berechnen kann
- **Bremsen-Experte**: 256mm Scheibe — reicht das oder 260mm XL600 Kit?

### 🔄 Elektrik-Spezialist benötigt:
- **Stator-Tester**: Jemand der weiss wie man Stator & Regler prüft
- **Kabelbaum-Designer**: Custom Wiring Harness für LED-Umbau

### 🔄 Stylist benötigt:
- **Decal/Grafik-Designer**: Custom Tank-Decals im African Queen Style
- **Sitzbank-Umpolsterer**: Wer baut flache Sitzbänke für NX650?

### 🔄 Entwickler benötigt:
- **UI/UX-Feedback**: Wie soll der Build-Tracker aussehen? Was anzeigen? Dark Mode?
- **Arduino/ESP32-Community**: Referenz-Projekte für Custom-Motorrad-Dashboards
- **3D-Druck-Spezialist**: Gehäuse für Custom-Dashboard drucken
- **Gebrauchtteile-Scout**: NX650 Teile auf eBay/Kleinanzeigen finden
- **DIY-Tutorial-Finder**: Was kann man selbst machen (Windschild, Sitzbank, Decals)?

### 🔄 Motor/Antrieb benötigt:
- **Vergaser-Experte**: VE82M Tuning — Düsengrößen, Nadellage, Unterdruckschläuche
- **Big-Bore-Experte**: 680cc/710cc Kits — was geht, was kostet, was taugt?

## Kommunikations-Regeln
- Jeder Agent liest diese Datei VOR seinem Run
- Jeder Agent darf neue Anfragen hinzufügen
- Der Chefingenieur priorisiert Anfragen und kann neue Agenten vorschlagen
- Alle Daten gehen in die SQLite DB — kein Duplikat-Code