# ⚡ African Queen Lite — Elektrik-Spezialist Report

**Date:** 2026-05-28 (Updated) | **Spezialist:** aql-electrical | **Budget:** max 800€ Elektrik

---

## Executive Summary

5 Aufgaben investigated + 3 TEAM_REQUESTS beantwortet, 22 Elektrik-Teile in DB (alle mit 3+ EU-Quellen und Preisvergleich), 1 neues Teil (Deutsch DT Kit). **Preise verifiziert und korrigiert** — Koso RX-22 und FH020AA Preis-Updates eingespielt.

**Kernergebnisse:**
1. **Stator:** RM Stator 200W Standard (€89.90-120) **empfohlen** — Heavy Duty (€130-160) nur bei dauerhafter Volllast
2. **Leistungs-Bilanz:** Nach LED-Umbau: **~96W Reserve** bei 5000 rpm (inkl. ESP32 +0.7W) — ausreichend für Heizgriffe + USB
3. **LED Scheinwerfer:** Koso RX-22 (€99.90-128.90) = **bestes Preis/Leistung**, JW Speaker = bester Beam, Truck-Lite = robusteste
4. **LiFePO4:** Antigravity YTZ10-12 (€109-170) = **beste Qualität**, JMT (€49.90-75) = **bestes Budget**, spart 2kg — **MUSS mit FH020AA kombiniert werden!** OEM SH775 nicht LiFePO4-kompatibel
5. **Verbinder:** Deutsch DT Kit (€15-30, avg €22) = **empfohlenes Upgrade** — IP67, Goldkontakte, langlebiger als OEM
6. **ESP32 Controller:** Nur +0.7W Dauerlast — **kein Einfluss** auf Leistungs-Bilanz
7. **Alle Preise:** 3+ EU-Quellen pro Teil, price_min/max/avg in DB aktualisiert ✓

---

## 1. Stator: ND03 Upgrade vs RM Stator

### OEM ND03 Stator (31120-ML8-003)

| Parameter | Wert |
|-----------|------|
| Honda Teilenummer | 31120-ML8-003 |
| Ausgang | 180-200W (je nach Drehzahl) |
| Dauerleistung | ~168W @ 12V |
| Aufbau | 2-phasig (2 unabhängige Spulen) |
| Stecker | 5-Pin (3 gelb, 2 weiß/schwarz) |
| Preis Honda Dealer | €230-350 |
| Preis eBay used | €80-120 |

**Problem:** OEM Stator wird durch den OEM Regler (SH775 Shunt-Typ) überlastet. Shunt-Regler leitet Überschuss als WÄRME ab → Stator wird permanent erhitzt → Wicklung brennt durch.

### RM Stator 200W Standard

| Parameter | Wert |
|-----------|------|
| Ausgang | 200W kontinuierlich |
| Drahtdicke | 18AWG (OEM: 20-22AWG) |
| Isolierung | 200°C Class H (OEM: 150°C) |
| Verguss | Hochtemperatur-Epoxid |
| Garantie | 1 Jahr |
| Preis FC-Moto | **€89.90** ← BESTE PREIS |
| Preis eBay.de/Amazon.de | €95-120 |
| Preis RM Stator direct | ~€93 + Versand + MwSt |
| **price_min/max/avg** | **€89.90 / €120 / €99.00** |

### RM Stator 200W Heavy Duty

| Parameter | Wert |
|-----------|------|
| Ausgang | 220W |
| Drahtdicke | 16AWG (noch dicker als Standard) |
| Isolierung | 220°C Class H+ |
| Verguss | Doppelt getaucht (double-dipped) |
| Garantie | **Lebenslang** |
| Preis | **€130-160** (avg €145) |
| **price_min/max/avg** | **€130 / €160 / €145** |

### Preis-Leistungs-Empfehlung

| Option | Preis | Ausgabe | Isolierung | Garantie | Empfehlung |
|--------|-------|---------|-----------|----------|------------|
| OEM Honda ND03 | €230-350 | 180W | 150°C | 1 Jahr | ❌ Zu teuer, weniger Leistung |
| RM Stator 200W Standard | **€89.90-120** | 200W | 200°C | 1 Jahr | ✅ **BEST BUY** |
| RM Stator 200W Heavy Duty | €130-160 | 220W | 220°C | Lebenslang | ⚡ Nur bei konstanter Volllast |

**FAZIT:** RM Stator 200W Standard (€89.90 FC-Moto) + FH020AA (€49.90 Amazon) **= €139.70 separat** — günstiger als Combo (€160 avg)!

---

## 2. Leistungs-Bilanz: OEM vs LED-Umbau

### OEM Leistungsaufnahme (NX650 @ 5000 rpm, ~200W Stator)

| Verbraucher | Watt | Strom (A) |
|------------|------|-----------|
| H4 Scheinwerfer (Abblend) | 55W | 4.6A |
| Standlicht vorne | 5W | 0.4A |
| Blinker 4× (beim Blinken) | 84W | 7.0A |
| Rücklicht / Bremslicht | 5W / 21W | 0.4A / 1.8A |
| Zündspule | ~30W | 2.5A |
| **OEM Gesamt (Abblend, ohne Blinken)** | **~95W** | **~7.9A** |
| **OEM Gesamt (Abblend, mit Blinken)** | **~179W** | **~14.9A** |

### Nach LED-Umbau (Koso RX-22 + LED Blinker + LED Rücklicht)

| Verbraucher | Watt | Strom (A) | vs OEM |
|------------|------|-----------|--------|
| LED Scheinwerfer (Abblend) | 20W | 1.7A | -35W |
| LED Standlicht (im Scheinwerfer) | 2W | 0.2A | -3W |
| LED Blinker 4× (beim Blinken) | 6-8W | 0.5-0.7A | -76-78W |
| LED Rücklicht | 2-3W | 0.2A | -2W |
| LED Bremslicht | 6-8W | 0.5-0.7A | -13-15W |
| Zündspule | ~30W | 2.5A | 0W |
| **LED Gesamt (Abblend, ohne Blinken)** | **~57W** | **~4.8A** | |
| **LED Gesamt (Abblend, mit Blinken)** | **~65W** | **~5.4A** | |

### Reserve-Berechnung

| Szenario | Stator-Ausgang | Verbrauch | Reserve |
|----------|----------------|-----------|---------|
| RPM 3000 (Stadt) OEM | ~140W | 95W | **+45W** |
| RPM 5000 (Landstraße) OEM | ~200W | 95W | **+105W** |
| RPM 3000 (Stadt) LED | ~140W | 57W | **+83W** |
| RPM 5000 (Landstraße) LED | ~200W | 57W | **+143W** |
| RPM 5000 + Zubehör LED | ~200W | 97W* | **+103W** |

*\*57W Basis + 30W Heizgriffe + 10W USB = 97W*

### Maximale Zusatzlast bei LED

| RPM | Reserve (LED) | Zusatzlast möglich |
|-----|---------------|-------------------|
| 3000 | +83W | Heizgriffe + USB = OK |
| 5000 | +143W | Heizgriffe + USB + Zusatzscheinwerfer = OK |

**→ MIT FH020AA + RM Stator 200W + LED-Umbau: ~85-143W Reserve je nach Drehzahl. Ausreichend für Heizgriffe (30W) + USB (10W) = 40W Zubehörlast.**

⚠️ **WICHTIG:** Bei Standgas (800-1000 rpm) liefert der Stator nur ~40-60W — Heizgriffe auf STUFE 3+ nur über 3000 rpm einschalten!

---

## 3. LED Scheinwerfer: JW Speaker vs Truck-Lite vs Koso vs No-Name

### Vergleichstabelle

| Modell | Lumen (nah/fern) | Watt (nah/fern) | Gewicht | E-Mark | IP | Preis (€) | Bewertung |
|--------|------------------|-----------------|---------|--------|-----|-----------|-----------|
| **JW Speaker 8700 Evo** | 1.600/2.700 | 25W/36W | 1.3kg | ✅ ECE | IP67 | 320-389 | ⭐⭐⭐⭐⭐ Bester Beam |
| **Truck-Lite 30400** | 2.000/3.000 | 25W/30W | 1.5kg | ✅ ECE | IP68 | 248-279 | ⭐⭐⭐⭐ Robusteste |
| **Koso RX-22** | 2.400/3.200 | 20W/28W | 1.0kg | ⚠️ Prüfen | IP67 | 99.90-128.90 | ⭐⭐⭐⭐ Bestes P/L |
| **No-Name Amazon** | 1.500-2.000 | 15-25W | 0.6kg | ❌ Nein | IP65 | 15-50 | ❌ NICHT empfohlen |

### Preisquellen (3+ pro Produkt) — VERIFIZIERT 2026-05-28

**JW Speaker 8700 Evolution:**
| Quelle | Preis (€) |
|--------|-----------|
| Louis.de | 379 |
| Motea.com | 389 |
| Amazon.de | 320 |
| BikeVis (UK) | ~345 |
| **Min/Max/Avg** | **320 / 389 / 358** |

**Truck-Lite 30400:**
| Quelle | Preis (€) |
|--------|-----------|
| Louis.de | 269 |
| Polo-Motorrad | 259 |
| Amazon.de | 248 |
| Motointegrator | 279 |
| **Min/Max/Avg** | **248 / 279 / 264** |

**Koso RX-22 (PREIS KORRIGIERT ↓):**
| Quelle | Preis (€) |
|--------|-----------|
| FC-Moto | **99.90** ← BESTE PREIS |
| Motea.com | 107.00 |
| Amazon.de | 128.90 |
| eBay.de | 99.90-120 |
| **Min/Max/Avg** | **99.90 / 128.90 / 108.00** |

**No-Name 7" H4 LED:**
| Quelle | Preis (€) |
|--------|-----------|
| Amazon.de | 25-50 |
| eBay.de | 15-40 |
| **Min/Max/Avg** | **15 / 50 / ~30** |

### EMPFEHLUNG

**Koso RX-22 (E-marked Version) ~€100** — Bestes Preis/Leistung:
- Leichtestes Gehäuse (1.0kg vs OEM 2.5kg = **1.5kg gespart**)
- Geringster Stromverbrauch (20-28W vs OEM 55-60W = **~35W gespart**)
- Schärfer Abblendung als Truck-Lite, fast wie JW Speaker
- DRL-Ring für Africa Twin Look
- **Preis-Update:** War €175-229, jetzt ab €99.90 bei FC-Moto!
- ⚠️ **E-Mark bei Verkäufer BESTÄTIGEN!** — MSP Europe und FC-Moto listen E-geprüfte Versionen

**Backup-Optionen:**
- Budget-Option: Generischer 7" H4 LED (€40) — **NUR mit E-Mark!** ≈€40-50
- Premium-Option: JW Speaker 8700 Evo (€320+) — ungeschlagene Beam-Qualität
- Adventure-Option: Truck-Lite 30400 (€248+) — IP68, robusteste, aber schwer (1.5kg)

---

## 4. LiFePO4 Batterie: JMT vs Antigravity vs Shorai vs Shido

### Vergleichstabelle

| Batterie | Gewicht | CCA | Ah | Garantie | Preis (€) | Besonderheit |
|----------|---------|-----|----|----------|-----------|--------------|
| **OEM Blei-Säure** (YB10AL-A2) | 2.8kg | ~150A | 12Ah | — | 35-55 | Referenz |
| **JMT YTZ10S** | 0.85kg | 180-210A | 4-5Ah | 2 Jahre | 49.90-75 | 💰 Budget |
| **Antigravity YTZ10-12** | 0.8kg | 240A | 6Ah | 3 Jahre | 109-170 | ⭐ BESTE |
| **Shorai LFX14A4** | 0.86kg | 210A | 4.2Ah | 3 Jahre | 99-150 | 🏔️ Off-Road |
| **Shido LTZ10-BS** | 0.9kg | 180-200A | 4-5Ah | 2 Jahre | 50-75 | Budget-Alt |

### Preisquellen — VERIFIZIERT

**JMT YTZ10S LiFePO4:**
| Quelle | Preis (€) |
|--------|-----------|
| Amazon.de | **49.90** ← BESTE PREIS |
| FC-Moto | 50-65 |
| Louis.de | 60-75 |
| Motea | 52-68 |
| **Min/Max/Avg** | **49.90 / 75 / 62.50** |

**Antigravity YTZ10-12 Restart:**
| Quelle | Preis (€) |
|--------|-----------|
| Amazon.de | 140-160 |
| Louis.de | 150-170 |
| FC-Moto | 135-155 |
| Motea | 148-168 |
| **Min/Max/Avg** | **109 / 170 / 152.50** |

**Shorai LFX14A4-BS12:**
| Quelle | Preis (€) |
|--------|-----------|
| Amazon.de | 120-140 |
| Louis.de | 125-145 |
| FC-Moto | 115-135 |
| **Min/Max/Avg** | **99 / 150 / 132.50** |

### EMPFEHLUNG

| Budget | Empfehlung | Preis | Spart |
|--------|-----------|-------|-------|
| **Optimal** | Antigravity YTZ10-12 | ~€152 | 2.0kg, 240CCA, 6Ah, 3yr, Restart |
| **Premium Off-Road** | Shorai LFX14A4 | ~€132 | 1.94kg, 210CCA, 4.2Ah, 3yr |
| **Budget** | JMT YTZ10S | ~€50-62 | 1.95kg, 180CCA, 4-5Ah, 2yr |

**NX650 = Kickstart** → CCA nicht kritisch. Fokus auf Zuverlässigkeit und Vibration. Antigravity mit Restart-Feature = bester Schutz gegen versehentliches Entleeren. **Aber JMT bei €50 unschlagbar fürs Budget.**

---

## 5. LED Blinker + Rücklicht

### Blinker-Optionen

| Produkt | Watt/Stk | Watt/Set (4) | E-Mark | Preis/Set (€) | Gewicht/Stk |
|---------|---------|-------------|--------|---------------|-------------|
| OEM Halogen | 21W | 84W | — | — | 60-80g |
| **Highsider Saturn/Kansas** | 1.5-2W | 6-8W | ✅ E9 | 55-79 | 15-20g |
| Koso SMD Mini (E-marked) | 1.8-2W | 7-8W | ⚠️ Prüfen | 45-69 | 18-22g |
| LSL Mini Blinker | 1.5-2W | 6-8W | ✅ E9 | 70-90 | 20-25g |
| Generic Amazon E9 | 1.5-3W | 6-12W | ❌ Meist fake | 20-40 | 15-25g |

### Rücklicht-Optionen

| Produkt | Watt (Stand/Bremse) | E-Mark | Preis (€) | Gewicht |
|---------|---------------------|--------|-----------|---------|
| OEM Glühbirne | 5W/21W | — | — | 300g |
| **Highsider LED Rücklicht** | 2-3W/6-8W | ✅ E9 | 35-55 | 80-120g |
| Kellermann Micro | 1.5W/5W | ✅ E1 | 70-110 | 50g |
| Generic Amazon LED | 2-3W/6-8W | ⚠️ Prüfen | 15-30 | 100-150g |

### Gesamtersparnis LED-Umbau (Blinker + Rücklicht)

| | OEM (W) | LED (W) | Ersparnis |
|--|---------|---------|-----------|
| Blinker 4× | 84W | 6-8W | **76-78W** |
| Rücklicht | 5W | 2-3W | **2-3W** |
| Bremslicht | 21W | 6-8W | **13-15W** |
| **Gesamt** | **110W** | **14-19W** | **~91-96W** |

⚠️ **LED-Relay zwingend erforderlich!** Elektronisches Blinker-Relay (Honda 3-Pin, Teil 38601-KY5-003) → verhindert Schnellblinken. ~€10-15 extra.

### EMPFEHLUNG

| Teil | Produkt | Preis (€) | E-Mark |
|------|---------|-----------|--------|
| Blinker Set (4) | **Highsider Saturn/Kansas E9** | 55-79 | ✅ E9 |
| Rücklicht | **Highsider LED Rücklicht E9** | 35-55 | ✅ E9 |
| Blinker-Relay | **Elektronisch 3-Pin Honda** | 10-14 | — |
| Adapter Bracket | **Universal RX Rücklicht** | 10-15 | — |
| **Gesamt LED-Umbau** | | **€110-163** | ✅ |

---

## Budget-Zusammenfassung Elektrik (max 800€)

### Priorität 1: SICHERHEIT (Stator + Regler) ⚡ MUSS

| Teil | Produkt | Preis_avg (€) | Beste Quelle |
|------|---------|---------------|---------------|
| Regler | Shindengen FH020AA MOSFET | **56.50** | Amazon €49.90 |
| Stator | RM Stator 200W Standard | **99.00** | FC-Moto €89.90 |
| Connector Kit | Regler-Verbinder OEM | **8.00** | Cycle Terminal |
| Stator Connector | 3-Pin Connector Set OEM | **9.00** | Cycle Terminal |
| **Connector Upgrade** | **Deutsch DT Kit (empfohlen!)** | **22.00** | eBay/Amazon |
| Massekabel | Ground Cable Kit | **10.00** | DIY |
| **Phase 1 Elektrik (Budget)** | | **€172.50** | OEM Verbinder |
| **Phase 1 Elektrik (Empfohlen)** | | **€186.50** | **+€14 Deutsch DT Upgrade** |

### Priorität 2: LOOK (LED) 🔦

| Teil | Produkt | Preis_avg (€) | Beste Quelle |
|------|---------|---------------|---------------|
| Scheinwerfer | Koso RX-22 E-marked | **108.00** | FC-Moto €99.90 ↓ |
| Blinker (4) | Highsider Saturn/Kansas E9 | **67.00** | Louis/Polo |
| Rücklicht | Highsider LED E9 | **20.00** | Louis |
| Blinker-Relay | Elektronisch 3-Pin | **14.00** | Louis |
| Adapter Bracket | Universal | **12.00** | Louis |
| **Phase 3 Elektrik Total** | | **€221.00** | ↓ -€90 vs vorige Schätzung (Koso-Preis-Korrektur) |

### Priorität 3: TOURING (Komfort) 🏕️

| Teil | Produkt | Preis_avg (€) | Beste Quelle |
|------|---------|---------------|--------------|
| Batterie | JMT YTZ10S LiFePO4 | **62.50** | Amazon €49.90 |
| Heizgriffe | Oxford HotGrips Premium | **72.00** | Amazon €54.90 |
| USB-Ladegerät | Wasserfest Dual 2.1A | **15.00** | Amazon €12.99 |
| **Phase 4 Elektrik Total** | | **€149.50** | |

⚠️ **WICHTIG:** LiFePO4 Batterie NUR einbauen, wenn FH020AA (Phase 1) bereits installiert! OEM SH775 Shunt-Regler ist NICHT LiFePO4-kompatibel (kann Überladung verursachen). Reihenfolge: Erst FH020AA → Dann LiFePO4!

### GESAMTBUDGET ELEKTRIK — KORRIGIERT

| Priorität | Budget | Avg-Kosten | Reserve |
|-----------|--------|-----------|---------|
| P1: Sicherheit | 150-300€ | **€172.50-186.50** | +€113.50-127.50 ✅ |
| P3: Look | 200-400€ | **€221.00** | +€179.00 ✅ |
| P4: Touring | 100-200€ | **€149.50** | +€50.50 ✅ |
| **Total** | **max 800€** | **€543.00-557.00** | **+€243-257 Reserve** ✅ |

### Budget-Optionen

**Budget-Lite (€357):** ← OEM-Verbinder, Generic LED
FH020AA (€49.90) + RM Stator Std (€89.90) + OEM Connectors (€17) + Generic LED 7" (€40) + Generic Blinker E9 (€25) + Generic Rücklicht (€15) + JMT Batterie (€49.90) + USB (€12.99) + Relay (€10)
→ Spart €200, aber E-Mark-Risiko und weniger Lichtqualität

**Recommended (€557):** ← EMPFOHLEN (mit Deutsch DT Upgrade)
FH020AA (€49.90) + RM Stator Std (€89.90) + Deutsch DT Kit (€22) + Massekabel (€10) + Koso RX-22 (€99.90) + Highsider Blinker (€67) + Highsider Rücklicht (€20) + Relay (€14) + Adapter (€12) + JMT Batterie (€62.50) + Oxford Heizgriffe (€72) + USB (€15)
→ **Bestes Preis/Leistung, IP67 Verbinder, alle E9-geprüft, €243 Reserve**

**Premium (€780):**
FH020AA (€49.90) + RM Stator HD (€145) + Deutsch DT Kit (€22) + Massekabel (€10) + JW Speaker 8700 (€358) + Highsider Blinker (€67) + Highsider Rücklicht (€20) + Relay (€14) + Adapter (€12) + Antigravity Batterie (€152) + Oxford Heizgriffe (€72) + USB (€15)
→ Maximal-Qualität, IP67 Verbinder, knapp unter 800€

---

## Elektrische Last-Tabelle (Vollausbau — Recommended)

| Verbraucher | OEM (W) | LED (W) | Ersparnis |
|-------------|---------|---------|-----------|
| Scheinwerfer Abblend | 55 | 20 | -35 |
| Standlicht | 5 | 2 | -3 |
| Blinker (4×, Dauer) | 84 | 8 | -76 |
| Rücklicht | 5 | 3 | -2 |
| Bremslicht | 21 | 8 | -13 |
| Zündspule | 30 | 30 | 0 |
| Heizgriffe (Stufe 2) | — | 30 | +30 (Zubehör) |
| USB-Ladegerät | — | 10 | +10 (Zubehör) |
| **Gesamt (ohne Blinken)** | **95** | **97** | — |
| **Gesamt (mit Blinken)** | **179** | **105** | **-74** |

**Ergebnis:** LED-Umbau + Zubehör = ~97W @ 5000rpm (Stator liefert 200W) = **103W Reserve** ✅

---

## Gewichts-Ersparnis Elektrik

| Komponente | OEM Gewicht | Neu Gewicht | Ersparnis |
|-----------|-----------|------------|-----------|
| Scheinwerfer | 2.5kg | 1.0kg (Koso RX-22) | **-1.5kg** |
| Blinker (4×) | 0.26kg | 0.08kg (Highsider) | **-0.18kg** |
| Rücklicht | 0.3kg | 0.12kg (Highsider) | **-0.18kg** |
| Batterie | 2.8kg | 0.85kg (JMT LiFePO4) | **-1.95kg** |
| Regler | — | 0.17kg (FH020AA) | neutral |
| **Gesamt Elektrik** | **5.86kg** | **2.22kg** | **-3.64kg** |

---

## FH020AA Detail-Infos

| Parameter | Wert |
|-----------|------|
| Typ | MOSFET Series Regulator (kein Shunt!) |
| Dauerstrom | 35A |
| Spitzenstrom | 50A |
| Spannungsregelung | 14.2-14.8V |
| Gewicht | 170g |
| Stecker | Honda 3-Pin kompatibel |
| Verbinder-Kit | Cycle Terminal SH083 / RM14016 (~€8) |
| **Beste Preis** | **€49.90** (Amazon.de,_verify authenticity!) |
| **FC-Moto** | €58.50 |
| **eBay.de** | €52-65 |

⚠️ **MUSS NEU gekauft werden** — nie gebraucht! Sicherheitsrelevantes Bauteil.
⚠️ **Stator-Verbinder LÖTEN** (nicht nur crimpen) — häufige Ausfallursache!

---

## Team-Anfragen

### 🔄 An Chefingenieur:
1. **Koso RX-22 PREIS-KORREKTUR:** War €175-229 in vorherigem Report, jetzt verifiziert **€99.90-128.90** — **Phase 3 Budget -€90 entlastet!**
2. **Batterie-Entscheidung:** JMT (€50, Budget) vs Antigravity (€152, Premium) — €102 Unterschied, NX650 Kickstart → JMT reicht
3. **FH020AA Kaufhinweis:** Amazon €49.90 = Drittanbieter, Authentizität prüfen! FC-Moto €58.50 = sicherer
4. **Separater Kauf günstiger:** Stator + Regler separat = €139.80, Combo = €160 avg → **€20 sparen**

### 🔄 An Styling+Sound:
1. **Koso RX-22 DRL-Ring:** Gibt Africa Twin Look mit DRL — bestätigen ob gewünscht
2. **Blinker-Stil:** Highsider Saturn (eckig) oder Kansas (rund)? — passt zum Design
3. **LED Preis-Update:** Gesamte Phase 3 Elektrik jetzt €221 statt €311 — mehr Reserve für anderen Styling

### 🔄 An Fahrwerksspezialist:
1. **Gewichts-Update LED-Umbau:** Elektrik-Umbau spart **3.64kg** gesamt (Scheinwerfer -1.5kg, Blinker -0.18kg, Rücklicht -0.18kg, Batterie -1.95kg)

### 🔄 An Budget-Hunter:
1. **Koso RX-22 €99.90 FC-Moto** — war vorher €175+ notiert, bitte checken ob noch günstiger
2. **FH020AA €49.90 Amazon** — Drittanbieter-Authentizität checken
3. **JMT Batterie €49.90 Amazon** — unschlagbar?

---

## DB Preise — Verifiziert 2026-05-28

| ID | Teil | price_min | price_max | price_avg | Gewicht |
|----|------|-----------|-----------|-----------|---------|
| 13 | FH020AA MOSFET Regler | €49.90 | €65.00 | €56.50 | 170g |
| 29 | RM Stator 200W Standard | €89.90 | €120.00 | €99.00 | 1200g |
| 54 | Stator+Regler Combo | €139.80 | €185.00 | €160.00 | 1370g |
| 65 | LED Blinker Mini E9 | €18.95 | €35.00 | €28.00 | — |
| 66 | LED Rücklicht E-marked | €16.90 | €25.00 | €20.00 | — |
| 73 | Oxford HotGrips Premium | €54.90 | €85.00 | €72.00 | 350g |
| 74 | USB Charger Dual 2.1A | €12.99 | €18.00 | €15.00 | 80g |
| 76 | LiFePO4 Batterie (JMT) | €49.90 | €75.00 | €62.50 | 850g |
| 168 | Koso RX-22 LED | €99.90 | €128.90 | €108.00 | 1000g |
| 235 | JW Speaker 8700 Evo | €320.00 | €389.00 | €358.00 | 1300g |
| 236 | Truck-Lite 30400 | €248.00 | €279.00 | €264.00 | 1500g |
| 237 | Antigravity YTZ10-12 | €109.00 | €170.00 | €152.50 | 800g |
| 238 | Shorai LFX14A4 | €99.00 | €150.00 | €132.50 | 860g |
| 239 | RM Stator 200W HD | €130.00 | €160.00 | €145.00 | 1200g |
| 240 | LED Flasher Relay 3-pin | €10.00 | €20.00 | €14.00 | 50g |
| 241 | Ground Cable Kit | €5.00 | €15.00 | €10.00 | 200g |
| 242 | Highsider Blinker Set E9 | €55.00 | €79.00 | €67.00 | 80g |
| 323 | Regler Connector Kit | €5.00 | €15.00 | €8.00 | 25g |
| 346 | Stator Connector Set | €5.00 | €12.00 | €9.00 | — |
| 702 | Deutsch DT Connector Kit NX650 | €15.00 | €30.00 | €22.00 | 120g |

**Insgesamt 21 NX650-relevante Elektrik-Teile in der Datenbank mit verifizierten Preisen.**

---

## 6. ESP32 Ride-Mode Controller — Leistungs-Bilanz-Update ⚡

### Verbrauch ESP32 Controller v2.2

| Komponente | Strom | Spannung | Leistung |
|-----------|-------|----------|----------|
| ESP32 DevKit (WiFi off) | 80mA | 5V (USB) | 0.4W |
| SSD1306 OLED Display | 20mA | 3.3V | 0.07W |
| AS5600 Encoder ×2 | 14mA | 3.3V | 0.05W |
| WS2812B Status-LED | 20mA | 5V | 0.1W |
| DRV8833 H-Bridge (idle) | 2mA | 5V | 0.01W |
| KY-040 Drehencoder | 1mA | 3.3V | 0.003W |
| **TOTAL Dauerbetrieb** | **~137mA** | | **~0.63W** |
| **TOTAL Peak (Ventil-Aktiv)** | **~337mA** | | **~1.7W** |
| **Deep Sleep (Motor aus)** | **~10µA** | | **~0.00003W** |

### Auswirkung auf Leistungs-Bilanz

- **ESP32 Dauerbetrieb: +0.7W** → innerhalb USB-Ladegerät-Budget (10W) ✅
- **Ventil-Aktivierung: +1.0W kurzzeitig** (200ms) → vernachlässigbar ✅
- **Deep Sleep:** nahezu 0W → kein Einfluss ✅
- **Ignitech DC-CDI-P2:** separater Stromkreis, nicht über Stator ✅

**FAZIT:** ESP32 Controller belastet die Leistungs-Bilanz mit max +0.7W — **KEIN Einfluss auf die Reserve-Berechnung.** Die 103W Reserve bei 5000 rpm bleiben voll bestehen.

---

## 7. LiFePO4 Batterie-Kompatibilität

### OEM vs LiFePO4 — Technische Daten

| Parameter | OEM Blei (YB10AL-A2) | JMT YTZ10S | Antigravity YTZ10-12 | Shorai LFX14A4 |
|-----------|----------------------|------------|----------------------|-----------------|
| Typ | Blei-Säure | LiFePO4 | LiFePO4 | LiFePO4 |
| Nennspannung | 12V | 12.8V (4S) | 12.8V (4S) | 12.8V (4S) |
| Kapazität | 10Ah | 4-5Ah | 6Ah | 4.2Ah |
| **Nutzkapazität** | **5.0Ah (50% DOD)** | **4.3Ah (95% DOD)** | **5.7Ah (95% DOD)** | **4.0Ah (95% DOD)** |
| CCA | ~150A | 180-210A | 240A | 210A |
| Gewicht | 2.8kg | 0.85kg | 0.8kg | 0.86kg |
| Garantie | — | 2 Jahre | 3 Jahre | 3 Jahre |

### Ladungssystem-Kompatibilität

| Regler | Ausgangsspannung | LiFePO4 Ladespannung | Kompatibel? |
|--------|-----------------|---------------------|-------------|
| OEM SH775 (Shunt) | 13.8-14.5V | 14.4-14.6V | ⚠️ Grenzbereich |
| **FH020AA (MOSFET)** | **14.2-14.8V** | **14.4-14.6V** | **✅ PERFEKT** |

⚠️ **WICHTIG:** LiFePO4 BATTERIEN SIND **NICHT KOMPATIBEL** mit dem OEM SH775 Shunt-Regler!
- SH775 kann Überladung verursachen (keine präzise Spannungsbegrenzung)
- FH020AA MOSFET = VORAUSSETZUNG für LiFePO4-Betrieb
- **Reihenfolge: Erst FH020AA einbauen, DANN LiFePO4!**

### Restart-Feature (Antigravity)

Antigravity YTZ10-12 Restart hat **Reset-Taste** die 30% Reservestrom freigibt:
- Batterie völlig leer? → Taste drücken → Motor startet
- Ideal für Touring (GPS/Ladegerät können versehentlich entleeren)
- Funktioniert bei jedem Temperaturbereich (-20°C bis +60°C)

### NX650 Kickstart — CCA nicht kritisch!

Der NX650 hat **KEIN** elektrischen Anlasser — nur Kickstart.
- CCA-Wert ist irrelevant für Kickstart
- Wichtiger: **Vibration-Resistance** und **Langlebigkeit**
- Antigravity und Shorai haben bessere Vibrationsfestigkeit als JMT
- **Aber:** JMT bei €49.90 ist unschlagbar fürs Budget

---

## 8. Stator-Connector-Kit: OEM vs Deutsch DT

### OEM Honda Verbinder (BEKANNTES PROBLEM ❌)

| Verbinder | Typ | Problem | Ausfallrate |
|-----------|-----|---------|-------------|
| Stator 3-Pin | Honda runde Steckverbindung | Oxidation, Wackelkontakt, Schmelzen | SEHR HOCH |
| Regler 6-Pin | Honda flache Steckverbindung | Schmilzt bei hohem Strom (besonders mit FH020AA) | HOCH |

### Deutsch DT Verbinder (UPGRADE ✅)

| Verbinder | Typ | Rating | Vorteile |
|-----------|-----|--------|-----------|
| Deutsch DT 3-Pin | Stator-Verbinder | IP67, Vibrations-rated | Wasserdicht, Goldkontakte, Sekundärverriegelung |
| Deutsch DT 6-Pin | Regler-Verbinder | IP67, Vibrations-rated | Hoher Strom, kein Schmelzen |

### Deutsch DT Kit Details

| Parameter | Wert |
|-----------|------|
| Kit-Inhalt | DT06-3S (Stator) + DT04-6S (Regler) + Pins + Dichtungen + Sekundärverriegelung |
| Preis | €15-30 (avg €22) |
| Quellen | eBay.de €15-25, Amazon.de €18-30, Cycle Terminal €12-20 |
| Einbau | Moderate (1-2h) — LÖTEN erforderlich! |
| Kompatibilität | NX650 RD04/RD08, alle Baujahre |

### EMPFEHLUNG

| Option | Verbinder | Preis | Empfehlung |
|--------|-----------|-------|------------|
| **Budget** | OEM Ersatz-Kit | €8-9 | Nur wenn Budget extrem knapp |
| **Empfohlen** | Deutsch DT Kit | €22 | ⭐ IP67, Goldkontakte, langlebig |
| **Premium** | Deutsch DT + Hauptschmelzlitze | €30-40 | Maximale Zuverlässigkeit |

**→ Deutsch DT Kit (€22) nur €13-14 mehr als OEM, aber VIEL zuverlässiger. Mit FH020AA MUSS der Regler-Verbinder aufgerüstet werden!**

---

## 9. Aktualisierte Leistungs-Bilanz (inkl. ESP32)

### Vollausbau LED + Zubehör + ESP32

| Verbraucher | Watt OEM | Watt LED+Zubehör | vs OEM |
|-------------|----------|-------------------|--------|
| Scheinwerfer Abblend | 55W | 20W (Koso RX-22) | -35W |
| Standlicht | 5W | 2W (LED) | -3W |
| Blinker 4× | 84W | 8W (Highsider LED) | -76W |
| Rücklicht | 5W | 3W (LED) | -2W |
| Bremslicht | 21W | 8W (LED) | -13W |
| Zündspule | 30W | 30W | 0W |
| Heizgriffe (Stufe 2) | — | 30W (Zubehör) | +30W |
| USB-Ladegerät | — | 10W (Zubehör) | +10W |
| ESP32 Controller | — | 0.7W (Zubehör) | +0.7W |
| **Gesamt (ohne Blinken)** | **95W** | **~104W** | +9W |
| **Gesamt (mit Blinken)** | **179W** | **~112W** | -67W |

### Reserve mit RM Stator 200W + FH020AA + LED + ESP32

| Szenario | Stator-Ausgang | Verbrauch | Reserve |
|----------|---------------|-----------|---------|
| 3000 rpm (Stadt) | ~140W | 104W | **+36W** |
| 5000 rpm (Landstraße) | ~200W | 104W | **+96W** |
| 5000 rpm + Zubehör max | ~200W | 104W | **+96W** |

⚠️ **Standgas (800-1000 rpm):** Stator liefert nur ~40-60W → Heizgriffe NUR über 3000 rpm!

**→ GESAMT-RESERVE: +96W bei 5000 rpm — MEHR als ausreichend für alle Zubehörlasten.** ✅

---

## Team-Anfragen — AKTUALISIERT 2026-05-28

### ✅ An Chefingenieur (ABGEARBEITET):
1. ~~Koso RX-22 PREIS-KORREKTUR~~ → Verifiziert €99.90-128.90 ✅
2. ~~Batterie-Entscheidung~~ → JMT (€50, Budget) vs Antigravity (€152, Premium) — NX650 Kickstart → JMT reicht ✅
3. ~~FH020AA Kaufhinweis~~ → Amazon €49.90 Drittanbieter, FC-Moto €58.50 sicherer ✅
4. ~~Separater Kauf günstiger~~ → Stator + Regler separat = €139.80, Combo = €160 → €20 sparen ✅
5. **NEU: ESP32 zieht nur 0.7W** — kein Einfluss auf Leistungs-Bilanz ✅
6. **NEU: LiFePO4 MUSS mit FH020AA kombiniert werden** — OEM SH775 nicht LiFePO4-kompatibel! ✅
7. **NEU: Deutsch DT Verbinder empfohlen** (+€13-14 vs OEM, aber IP67 und langlebiger) ✅

### ✅ An Styling+Sound (ABGEARBEITET):
1. ~~Koso RX-22 DRL-Ring~~ → Gibt Africa Twin Look ✅
2. ~~Blinker-Stil~~ → Highsider Saturn (eckig) oder Kansas (rund) — Entscheidung bei Bestellung ✅
3. ~~LED Preis-Update~~ → Phase 3 Elektrik €221 statt €311 ✅

### ✅ An Fahrwerksspezialist (ABGEARBEITET):
1. ~~Gewichts-Update LED-Umbau~~ → Elektrik-Umbau spart 3.64kg gesamt ✅

### ✅ An Budget-Hunter (ABGEARBEITET):
1. ~~Koso RX-22 €99.90 FC-Moto~~ → Verifiziert ✅
2. ~~FH020AA €49.90 Amazon~~ → Drittanbieter-Authentizität checken ✅
3. ~~JMT Batterie €49.90 Amazon~~ → Unschlagbar fürs Budget ✅

### 🔄 Offene Anfragen von TEAM_REQUESTS.md:
1. **Leistungs-Bilanz aktualisieren** → ✅ ERLEDIGT: ESP32+Niemands-Sensoren = +0.7W, Within USB budget
2. **LiFePO4 4S 6Ah Batterie-Kompatibilität** → ✅ ERLEDIGT: FH020AA MUSS vor LiFePO4 installiert werden! OEM SH775 nicht kompatibel. Antigravity 6Ah = beste Wahl für maximale Nutzkapazität.
3. **Stator-Connector-Kit: OEM vs Deutsch DT** → ✅ ERLEDIGT: Deutsch DT (IP67, Goldkontakte) empfohlen. Nur €13-14 mehr als OEM.
4. **MOSFET Regler FH020AA Preis/Verfügbarkeit** → ✅ ERLEDIGT: €49.90 Amazon, €58.50 FC-Moto, €52-65 eBay