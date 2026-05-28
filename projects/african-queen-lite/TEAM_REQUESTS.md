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

## Chefingenieur-Empfehlungen für Team-Erweiterung (Run #4 — 2026-05-28)

### Neue Agenten vorgeschlagen:

| Agent | Rolle | Intervall | Fokus | Begründung |
|-------|------|-----------|-------|------------|
| `aql-tuv-expert` | TÜV/Zulassung | 24h | Eintragung, StVZO, ABE, Gutachten | Phase 3 Änderungen (Auspuff, LED) brauchen TÜV-Eintragung |
| `aql-ergonomics` | Ergonomie/Comfort | 24h | Sitzposition, Lenker, Fußrasten | Langstrecke-Tauglichkeit, Lenkerhöhe, Sitzbank |
| `aql-wrench` | Werkstatt-Planer | 12h | Einbau-Reihenfolge, Werkzeuge, Zeitschätzungen | Von Phase 1→4: Welche Teile zuerst, Arbeitszeit pro Phase |

### Begründung:
1. **TÜV-Experte:** Phase 3 Änderungen (Auspuff, LED-Scheinwerfer, Blinker) brauchen StVZO-Konformität. Leo Vince hat ECE R92 (ABE), aber Delkevic Header und generische LED brauchen Eintragung. Kosten: €100-200 für Gutachten + Eintragung.
2. **Ergonomie-Experte:** Der NX650 hat eine relativ aufrechte Sitzposition. Für Touring sollten Lenkerhöhe, Sitzbank-Form und Fußrasten-Position optimiert werden — das beeinflusst Phase 4 (Touring-Komfort).
3. **Werkstatt-Planer:** Mit 4 Phasen und ~30 Teilen braucht's eine klare Einbau-Reihenfolge. Some jobs hängen voneinander ab (z.B. Gabel zerlegen → Federn+Emulatoren einbauen → Öl einfüllen). Schätzungen: Phase 1 ~6h, Phase 2 ~8h, Phase 3 ~4h, Phase 4 ~2h.

## Skill
Dieses Team basiert auf dem **mechanic-tuning-team** Skill — wiederverwendbar für jedes Fahrzeug-Projekt.
`skill_view(name='mechanic-tuning-team')`

---

## DEVELOPER UPDATE — 2026-05-28 (v2.2)

### ESP32 Ride-Mode Controller v2.2 — Neue Features

**5 neue Module gebaut:**

| Modul | Datei | Beschreibung |
|-------|-------|-------------|
| Auto-RPM Valve | `auto_rpm_valve.h` | Auspuffklappe folgt RPM-Kurven pro Mode (5 Interpolationspunkte) |
| Fuel Estimator | `fuel_estimator.h` | Verbrauchsschätzung pro Mode (mL/100km), Reichweite, Reserve-Warnung |
| Gear Estimator | `gear_estimator.h` | Gang-Erkennung aus RPM/Speed-Korrelation (5 Gänge NX650) |
| Sleep Manager | `sleep_manager.h` | Deep Sleep nach 5 Min Motor aus (80mA → 10µA), Wake an Zündung/Taste |
| Config Mode | `config_mode.h` | Long-Press Encoder (3s) → Helligkeit, Ventil-Kalibrierung, Mode-Select |

**Neue Mode-Parameter (v2.2):**

| Mode | Ign | Valve | Airbox | Fuel (L/100km) | CDI | Sweep |
|------|-----|-------|--------|-----------------|-----|-------|
| STRASSE | 0° | 50% | 50% | 3.5 | A | 3 |
| STADT | -2° | 20% | 30% | 3.0 | A | 2 |
| GELÄNDE | +2° | 100% | 100% | 4.5 | B | 6 |
| SPORT | +3° | 100% | 100% | 5.0 | B | 8 |
| COMFORT | -1° | 40% | 40% | 3.2 | A | 2 |
| SOUND | +1° | 100% | 80% | 4.0 | C | 5 |

**RPM-Valve-Kurven (Auto-RPM Valve):**
Jeder Mode hat 5 Interpolationspunkte (RPM → Ventilposition %):
- **STADT:** 1500RPM=10% → 2500=15% → 4000=20% → 5500=30% → 6500=20% (geschlossen für Ruhe)
- **GELÄNDE:** 1500=40% → 2500=80% → 3500=100% → 5000=100% → 7000=100% (voll offen ab 3500)
- **SPORT:** 1500=30% → 2500=60% → 3000=90% → 5000=100% → 7000=100% (aggressiv öffnend)
- **SOUND:** 1200=60% → 2000=85% → 3000=95% → 4500=100% → 6500=80% (Sound-optimiert!)

**platformio.ini Build-Flags:**
```
-DENABLE_AUTO_RPM_VALVE=1
-DENABLE_FUEL_ESTIMATION=1
-DENABLE_GEAR_ESTIMATION=1
-DENABLE_DEEP_SLEEP=1
-DENABLE_OTA_UPDATE=1
```

**Neue Dateien:**
- `dashboard/src/auto_rpm_valve.h`
- `dashboard/src/fuel_estimator.h`
- `dashboard/src/gear_estimator.h`
- `dashboard/src/sleep_manager.h`
- `dashboard/src/config_mode.h`

**Tracker Web-App v2.2:**
- Neue Mode-Parameter mit Fuel-Spalten
- RPM-Valve-Kurven als SVG-Charts (Canvas im Browser)
- Pin-Mapping-Tabelle für v2.2
- Feature-Overviews für Neue Features

**Hardware-Kosten (ESP32 Controller): ~€205**

---

### TEAM-ANFRAGEN für nächste Runs

#### An Elektrik-Agent:
- [ ] Leistungs-Bilanz aktualisieren: ESP32+Niemands-Sensoren Verbrauch (v2.2: ~80mA aktiv, ~10µA deep sleep)
- [ ] LiFePO4 4S 6Ah Batterie-Kompatibilität prüfen
- [ ] Stator-Connector-Kit: OEM-Verbinder vs. Deutsch DT
- [ ] MOSFET Regler (Shindengen FH020AA) — Preis/Verfügbarkeit

#### An Mechanik-Agent:
- [ ] Auspuff-Klappen-System: butterfly valve 35-38mm ID — Wer fertigt das? Alu-Schweißen oder 3D-Druck?
- [ ] Airbox-Klappe: originale NX650 Airbox — wie integrieren wir eine Klappe?
- [ ] Zündzeitpunkt-Tabelle für NX650 RFVC: Standard = 15° BTDC @ idle, 35° BTDC @ advance — bestätigen!
- [ ] Übersetzung: 15/45 Kettenrad-Set (aktuell 15/42) — passt das zum Gelände-Mode?

#### An Budget-Jäger:
- [ ] DRV8833 + AS5600 + Pololu Motor: günstigste Quelle (aktuell ~€35/Achse)
- [ ] Ignitech DC-CDI-P2: aktuell ~€120 — gibt es Alternativen?
- [ ] 3D-Druck Gehäuse (IP67): PETG vs ABS vs Nylon — Kostenvergleich

---

## CHEFINGENIEUR UPDATE — 2026-05-28 (Preis-Jäger Run #2)

### DB-Verifizierung (2026-05-28 — Run #2)
- **143 NX650-fitment Teile** in DB (inkl. alle Alternativen + neue Bundle/Kits)
- **DB SUM(price_avg):** EUR12.657 fuer alle NX650-Teile (NICHT Build-Budget — enthaelt alle Alternativen + Optionen)
- **Option A Build-Kosten:** EUR2.264 (28 Teile)
- **54 NX650 Known Issues:** 5 critical (Stator, Regler, Verbinder), 4 high (Verkabelung, CDI)
- **7 Preise aktualisiert:** Stator EUR95, Regler EUR55, EBC FA185HH EUR20, Koso RX-22 EUR99.90, Mitas E-07+ Dakar EUR89.90/109
- **6 neue Teile (Run #2):** Bundle-Deals (Ketten-Set, Mitas Set, RT Fork Kit), Schweißarbeiten, Regler-Verbinder-Kit, Stator-Connector
- **Keine Performance-Teile** in DB fuer NX650 eingefuegt

### FAHRWERK-SPEZIALIST UPDATE — 2026-05-28 (Run #3)

**Neue Erkenntnisse:**
- **Reifen-Gewichte shop-verifiziert:** Mitas E-07 Front 5.2kg (statt 6.2kg), Rear 6.9kg (statt 7.0kg)
- **Pirelli MT60 RS + Conti TKC70** zu Vergleich hinzugefügt mit 4 Quellen je
- **Netto-Gewichtsersparnis korrigiert:** Option A Mono = +0.25kg (statt +0.75kg), Option B Twin = +1.85kg (statt +2.35kg)
- **EBC FA185HH Preise verifiziert:** Min 21.90€ (FC-Moto), Max 42.60€, Avg 27€
- **Bremsen-Budget bleibt unschlagbar:** 93€ avg für 30-40% Bremsverbesserung
- **YSS Z-366 Mono+Blech** bleibt Empfehlung: 379€ avg, bestes Preis/Leistung
- **Reifen-Tipp:** Conti TKC70 bei 303€ Set-Preis teuer für NX650, Mitas E-07 bleibt Best Value

**Budget-Guard Status (RUN #3 — aktualisiert):**

| Phase | Geplant | Budget | Reserve | Status |
|-------|---------|--------|---------|--------|
| 1: Zuverlässigkeit | **EUR470** | EUR800 | **+EUR330 (41%)** | OK |
| 2: Fahrwerk | **EUR1.005** | **EUR1.200** | **+EUR195 (16%)** | ✅ Verifiziert Run #3 |
| 3: Africa Twin Look | EUR688 | EUR1.000 | +EUR312 (31%) | OK |
| 4: Touring-Komfort | EUR187 | EUR800 | +EUR613 (77%) | OK |
| 5: Reserve | — | EUR500 | +EUR500 | Puffer |
| **Total** | **EUR2.350** | **EUR4.300** | **+EUR1.950** | OK |

### Budget-Guard Status (VERIFIZIERT 2026-05-28 — Run #2)
KEINE Phase ueberschritten!

| Phase | Geplant | Budget | Reserve | Status |
|-------|---------|--------|---------|--------|
| 1: Zuverlaessigkeit | **EUR470** | EUR800 | **+EUR330 (41%)** | OK — +EUR19 Filter+Schläuche+Connector-Kits |
| 2: Fahrwerk | €944 | **€1.005** | **+€195 (16%)** | ✅ Deep-Dive Update (2026-05-28) |
| 3: Africa Twin Look | EUR688 | EUR1.000 | +EUR312 (31%) | OK |
| 4: Touring-Komfort | EUR187 | EUR800 | +EUR613 (77%) | OK |
| 5: Reserve | — | EUR500 | +EUR500 | Puffer |
| **Total** | **EUR2.289** | **EUR4.300** | **+EUR2.011** | OK |

### ESP32 Controller Budget (separat von Motorrad-Build):
| Komponente | Preis |
|-----------|-------|
| ESP32 DevKit V1 | ~€6 |
| SSD1306 OLED | ~€3 |
| DRV8833 H-bridge | ~€3 |
| Pololu 37Dx52L gearmotor (2x) | ~€50 |
| AS5600 Encoder (2x) | ~€10 |
| KY-040 Encoder | ~€2 |
| WS2812B LED | ~€1 |
| Ignitech DC-CDI-P2 | ~€120 |
| NTC 10kΩ + voltage dividers | ~€5 |
| 3D-printed case (PETG) | ~€15 |
| **Total** | **~€205** |

### Gewicht-Bilanz
- **Trockengewicht nach Bau:** ~155.4 kg (OEM: 161 kg) = -5.6 kg
- **Fahrfertig:** ~170-171 kg = UNTER dem 175 kg Ziel!
- Groesste Ersparnis: Auspuff (-3 kg), Batterie (-2 kg), LED (-1.7 kg), YSS (-1.3 kg)
- Gewichtsverteilung: vorne ~54%, hinten ~46% (ausgewogen)