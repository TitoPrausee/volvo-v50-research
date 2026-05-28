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

---

## 🆕 CHEFINGENIEUR RUN #7 — Neue Erkenntnisse (2026-05-28)

### Neue NX650 Teile in DB (seit Run #6)

| ID | Teil | Preis | Gewicht | Relevanz | Aktion |
|----|------|-------|---------|----------|--------|
| 723 | Mosko Moto R80 Luggage | €340 | 3.500g | ⚠️ Über Budget Phase 4 | Dokumentieren als Option |
| 722 | Koso RX-22N 7" LED (DOT/ECE) | €109 | 800g | ✅ RX-22 Alternative | **Empfehlen statt RX-22** |
| 721 | Stator 3-Pin Weatherpack | €9 | 20g | ✅ Besser als OEM | Phase 1 aufnehmen |
| 720 | Viton Fuel Hose Kit 3mm | €7 | 50g | ✅ Ethanol-Schutz | Schon in Phase 1 |
| 719 | Pilot Jet #40 (Upgrade) | €5 | 5g | 🟡 Vergaser-Tuning | Wartung, kein Power |
| 705 | Exhaust Gasket Muffler Joint | €5 | ?g | ✅ Phase 3 Zubehör | **Zur Einkaufsliste** |
| 704 | Exhaust Gasket Header-Cylinder | €6 | ?g | ✅ Phase 3 Zubehör | **Zur Einkaufsliste** |
| 702 | Deutsch DT Connector Kit | €22 | 120g | ✅ Alternative | Option zu Weatherpack |

### 🔄 Koso RX-22N Empfehlung (Chefingenieur)

**Koso RX-22N** (ID 722) ersetzt **Koso RX-22** in Option A:
- **Gewicht:** 800g (RX-22N) vs 1.000g (RX-22) = **-200g Ersparnis**
- **Preis:** €109 avg (praktisch identisch zu RX-22 €108)
- **Zulassung:** DOT/ECE (besser für TÜV als reine ECE R92)
- **Phase 3 Budget:** Kein Einfluss (±€1)

### 🔄 Stator-Connector Upgrade (Chefingenieur)

**Weatherpack 3-Pin** (ID 721, €9) als Budget-Option vs **Deutsch DT Kit** (ID 702, €22):
- Weatherpack: Schnell, wasserdicht, günstig → Phase 1
- Deutsch DT: IP67, Goldkontakte, professioneller → Für maximale Zuverlässigkeit
- **Empfehlung:** Weatherpack für Budget-Build (€9 vs €22, -130g Gewicht)

### 🔄 Exhaust Gaskets — Pflicht bei SS Header Umbau

Bei jedem Auspuffumbau (SS Header + Slip-on) müssen folgende Dichtungen ersetzt werden:
- **Exhaust Gasket Header-Cylinder NX650** (ID 704, €6) — Zylinderkopf-Dichtung
- **Exhaust Gasket Muffler Joint NX650** (ID 705, €5) — Slip-on Verbindung

**Total: €11** → Zur Phase 3 Einkaufsliste hinzufügen! (Kein Budget-Problem: Phase 3 Reserve +€345)

---

## 🎨 Styling+Sound Spezialist Anfragen (Run #6 — 2026-05-28)

### Anfrage an Chefingenieur: TÜV-Kosten einplanen

Phase 3 Änderungen brauchen TÜV-Eintragungen. Geschätzte Kosten:

| Änderung | TÜV nötig? | E-Nummer? | Kosten |
|----------|------------|-----------|--------|
| Leo Vince SBK Slip-on | ✅ JA | ✅ ABE D | €20-40 |
| Delkevic SS Header | ✅ JA | ❌ Einzeln | €50-100 |
| LED Scheinwerfer | ⚠️ Teilweise | ✅ E-Mark | €20-50 |
| LED Blinker+Rücklicht | ✅ JA | ✅ E9 | €20-40 |
| **Total TÜV Phase 3** | | | **€90-250** |

**BITTE:** TÜV-Kosten in Budget-Bilanz aufnehmen. Budget Option A = €762-1.048 + €90-250 TÜV = €852-1.298. Innerhalb des €1.200 Phase 3 Limits (mit €52 Puffer bei Maximum).

### Anfrage an Elektrik-Spezialist: LED-Umbau Verkabelung

LED-Umbau braucht folgende elektrische Anpassungen:
1. **Flasher-Relay Tausch:** Elektronisches Relais (€10-20) MUSS installiert werden für korrekte Blinkfrequenz mit LED-Blinkern
2. **Lastwiderstände:** Falls Relais nicht getauscht wird — aber Relay-Tausch ist sauberer
3. **Koso RX-22N Verkabelung:** 7" H4 LED = Plug-and-Play mit NX650 Scheinwerfergehäuse, DOT/ECE Version hat bessere Zulassungsdokumente
4. **Blinker-Thread:** Vorne M8 (8mm), hinten M10 (10mm) — Universelle Sets haben Adapter

**BITTE:** Verkabelungsplan für LED-Umbau erstellen, inkl. Relay-Typ und Anschlussschema.

### Anfrage an Budget-Jäger: FC-Moto Sammelbestellung

Folgende Teile alle bei FC-Moto verfügbar — Sammelbestellung spart Versand:
1. Leo Vince SBK M15051 (~€289-309)
2. Koso RX-22N LED (~€99-109)
3. Acerbis MX Uniko (~€39-45)
4. UNI NU-4050 (~€29-35)
5. LED Blinker Set E9 (~€25-35)
6. LED Rücklicht E-marked (~€12-20)

**BITTE:** Versandkosten prüfen, Bundle-Rabatte erfragen, Lieferzeiten verifizieren.

### Anfrage an Mechaniker: Jetting-Empfehlung

Mit SS Header + Leo Vince Slip-on + UNI Filter:
- **Empfehlung:** Hauptdüse #150-152, Pilotdüse #40, Nadel Clip Position 2
- VE81M CV-Vergaser: recht tolerant, erst fahren dann ggf. anpassen
- Düsen einzeln ~€2-4 (Keihin/NOZZLE)

**BITTE:** Jetting-Kit Preis und Verfügbarkeit verifizieren, Einbau-Tipps für SS Header.

## Chefingenieur-Empfehlungen für Team-Erweiterung (Run #4 — 2026-05-28)

### Neue Agenten vorgeschlagen:

| Agent | Rolle | Intervall | Fokus | Begründung |
|-------|------|-----------|-------|------------|
| `aql-tuv-expert` | TÜV/Zulassung | 24h | Eintragung, StVZO, ABE, Gutachten | Phase 3 Änderungen (Auspuff, LED) brauchen TÜV-Eintragung |
| `aql-ergonomics` | Ergonomie/Comfort | 24h | Sitzposition, Lenker, Fußrasten | Langstrecke-Tauglichkeit, Lenkerhöhe, Sitzbank |
| `aql-wrench` | Werkstatt-Planer | 12h | Einbau-Reihenfolge, Werkzeuge, Zeitschätzungen | Von Phase 1→4: Welche Teile zuerst, Arbeitszeit pro Phase |

### Begründung:
1. **TÜV-Experte:** Phase 3 Änderungen (Auspuff, LED-Scheinwerfer, Blinker) brauchen StVZO-Konformität. Leo Vince hat ECE R92 (ABE), aber Delkevic Header und generische LED brauchen Eintragung. Kosten: €100-200 für Gutachten + Eintragung.
2. **Ergonomie-Experte:** Der NX650 hat eine relativ aufrechte Sitzposition. Für Touring sollten Lenkerhöhe, Sitzbank-Form und Fußrasten-Position optimiert werden — das beeinflusst phase 4 (Touring-Komfort).
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

**Hardware-Kosten (ESP32 Controller): ~€205**

---

### TEAM-ANFRAGEN für nächste Runs

#### An Elektrik-Agent:
- [x] Leistungs-Bilanz aktualisieren: ESP32+Niemands-Sensoren Verbrauch (v2.2: ~80mA aktiv, ~10µA deep sleep) ✅
- [x] LiFePO4 4S 6Ah Batterie-Kompatibilität prüfen ✅
- [x] Stator-Connector-Kit: OEM-Verbinder vs. Deutsch DT → **Weatherpack €9 empfohlen als Budget-Option**
- [x] MOSFET Regler (Shindengen FH020AA) — Preis/Verfügbarkeit ✅
- [ ] Koso RX-22N vs RX-22: Verkabelungsunterschiede prüfen (DOT/ECE Version)
- [ ] Weatherpack 3-Pin Connector: Pin-Belegung und Adapter-Plan für NX650 Stator

#### An Mechanik-Agent:
- [ ] Auspuff-Klappen-System: butterfly valve 35-38mm ID — Wer fertigt das? Alu-Schweißen oder 3D-Druck?
- [ ] Airbox-Klappe: originale NX650 Airbox — wie integrieren wir eine Klappe?
- [ ] Zündzeitpunkt-Tabelle für NX650 RFVC: Standard = 15° BTDC @ idle, 35° BTDC @ advance — bestätigen!
- [ ] Übersetzung: 15/45 Kettenrad-Set (aktuell 15/42) — passt das zum Gelände-Mode?
- [ ] Exhaust Gaskets (Header+Muffler) zur Einkaufsliste Phase 3 hinzufügen (€11 total)

#### An Budget-Jäger:
- [x] DRV8833 + AS5600 + Pololu Motor: günstigste Quelle (aktuell ~€35/Achse)
- [ ] Koso RX-22N DOT/ECE Version: Best-Price prüfen (€84-129 Range)
- [ ] Weatherpack 3-Pin Stator Connector: Quelle und Preis verifizieren (€9 avg in DB)
- [ ] Exhaust Gaskets: Best-Price für Athena/Honda OEM (€5+6=€11)
- [ ] Saisonale Preisentwicklung tracken (Winter-Sale Nov-Feb)

---

## CHEFINGENIEUR UPDATE — Run #7 (2026-05-28)

### Neue Empfehlungen:

1. **Koso RX-22N statt RX-22** — 200g leichter, DOT/ECE Zulassung, gleicher Preis
2. **Weatherpack 3-Pin statt gelötet** — €9 wasserdicht, professioneller als OEM, einfacher als löten
3. **Exhaust Gaskets zur Phase 3 Liste** — €11 Pflicht bei SS Header Umbau
4. **Mosko Moto R80 dokumentieren als OPTIONAL** — €340 über Budget Phase 4, als späteres Upgrade
5. **Pilot Jet #40** — €5 Upgrade-Vergaserdichtung, keine Leistungssteigerung (Wartung)

### Budget-Guard bleibt GRÜN:

| Phase | Geplant | Budget | Reserve | Status |
|-------|---------|--------|---------|--------|
| 1: Zuverlässigkeit | €393 | €800 | +€407 (51%) | ✅ |
| 2: Fahrwerk | €880 | €1.200 | +€320 (27%) | ✅ |
| 3: Africa Twin Look | €655 | €1.000 | +€345 (35%) | ✅ |
| 4: Touring-Komfort | €187 | €800 | +€613 (77%) | ✅ |
| 5: Reserve | — | €500 | +€500 | 🔵 |
| **Total** | **€2.128** | **€4.300** | **+€2.172** | ✅ |

### ⚠️ Kompatibilitäts-Hinweise (aktualisiert Run #7)
1. YSS Z-366 Mono: Bracket muss geschweißt werden (€65 extra)
2. DID 520VX3: 520 pitch ersetzt OEM 525 — Sprockets MUSS 520 sein
3. FH020AA Regler: Adapter-Verkabelung nötig (Connector-Kit €8)
4. Stator-Connector: **Weatherpack 3-Pin (€9)** empfohlen, alternativ löten oder Deutsch DT (€22)
5. JMT YTZ10F: Geringe Batteriebox-Modifikation nötig
6. Koso RX-22N: DOT/ECE Version bevorzugen — besseres P/L und TÜV
7. Exhaust Gaskets: 2 Dichtungen (€11) MUSS bei SS Header + Slip-on Umbau ersetzt werden

---

## BUDGET-GUARD STATUS — Run #5 (2026-05-28)

KEINE Phase überschritten! Alle Budget-Guards grün.

| Phase | Geplant | Budget | Reserve | Status |
|-------|---------|--------|---------|--------|
| 1: Zuverlaessigkeit | **€393** | €800 | **+€407 (51%)** | OK — +€19 Filter+Schläuche+Connector-Kits |
| 2: Fahrwerk | **€880** | **€1.200** | **+€320 (27%)** | ✅ Verifiziert Run #3 |
| 3: Africa Twin Look | **€655** | €1.000 | **+€345 (35%)** | OK |
| 4: Touring-Komfort | **€187** | €800 | **+€613 (77%)** | OK |
| 5: Reserve | — | €500 | **+€500** | Puffer |
| **Total** | **€2.128** | **€4.300** | **+€2.172** | OK |

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
- **Mit RX-22N:** ~169.8 kg fahrfertig (weitere 200g gespart)
- Größte Ersparnis: Auspuff (-3 kg), Batterie (-2 kg), LED (-1.2 kg mit RX-22N), YSS (-1.3 kg)
- Gewichtsverteilung: vorne ~54%, hinten ~46% (ausgewogen)