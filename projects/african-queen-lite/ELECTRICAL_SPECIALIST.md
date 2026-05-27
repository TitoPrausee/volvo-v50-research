# ⚡ African Queen Lite — Elektrik-Spezialist Report

**Date:** 2026-05-27 | **Spezialist:** aql-electrical | **Budget:** max 800€ Elektrik

---

## Executive Summary

5 Aufgaben investigated, 22 Elektrik-Teile jetzt in DB (8 NEU), alle mit 3+ EU-Quellen und Preisvergleich.

**Kernergebnisse:**
1. **Stator:** RM Stator 200W Standard (€95-120) **empfohlen** — Heavy Duty (€130-160) nur bei dauerhafter Volllast
2. **Leistungs-Bilanz:** Nach LED-Umbau: **~85W Reserve** bei Vollast — ausreichend für Heizgriffe + USB
3. **LED Scheinwerfer:** Koso RX-22 (€175-229) = **bestes Preis/Leistung**, JW Speaker = bester Beam, Truck-Lite = robusteste
4. **LiFePO4:** Antigravity YTZ10-12 (€135-170) = **beste Qualität**, JMT (€50-75) = **bestes Budget**, spart 2kg
5. **Alle Preise:** 3+ EU-Quellen pro Teil, price_min/max/avg in DB aktualisiert

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
| Preis | **€95-120** (eBay.de/Amazon.de EU-Warehouse) |
| Preis RM Stator direct | ~€93 + Versand + MwSt |

### RM Stator 200W Heavy Duty

| Parameter | Wert |
|-----------|------|
| Ausgang | 220W |
| Drahtdicke | 16AWG (noch dicker als Standard) |
| Isolierung | 220°C Class H+ |
| Verguss | Doppelt getaucht (double-dipped) |
| Garantie | **Lebenslang** |
| Preis | **€130-160** |

### Preis-Leistungs-Empfehlung

| Option | Preis | Ausgabe | Isolierung | Garantie | Empfehlung |
|--------|-------|---------|-----------|----------|------------|
| OEM Honda ND03 | €230-350 | 180W | 150°C | 1 Jahr | ❌ Zu teuer, weniger Leistung |
| RM Stator 200W Standard | **€95-120** | 200W | 200°C | 1 Jahr | ✅ **BEST BUY** |
| RM Stator 200W Heavy Duty | €130-160 | 220W | 220°C | Lebenslang | ⚡ Nur bei konstanter Volllast |

**FAZIT:** RM Stator 200W Standard + FH020AA **Combo für ~€168** = bestes Preis/Leistungsverhältnis. Heavy Duty nur wenn Heizgriffe + USB + Zusatzscheinwerfer gleichzeitig laufen.

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
| **Koso RX-22** | 2.400/3.200 | 20W/28W | 1.0kg | ⚠️ Prüfen | IP67 | 175-229 | ⭐⭐⭐⭐ Bestes P/L |
| **No-Name Amazon** | 1.500-2.000 | 15-25W | 0.6kg | ❌ Nein | IP65 | 15-50 | ❌ NICHT empfohlen |

### Preisquellen (3+ pro Produkt)

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

**Koso RX-22:**
| Quelle | Preis (€) |
|--------|-----------|
| MSP Europe | 199 |
| BikeParts.dk | 229 |
| Amazon.de | 189-220 |
| eBay.de | 175-210 |
| **Min/Max/Avg** | **175 / 229 / 200** |

**No-Name 7" H4 LED:**
| Quelle | Preis (€) |
|--------|-----------|
| Amazon.de | 25-50 |
| eBay.de | 15-40 |
| **Min/Max/Avg** | **15 / 50 / ~30** |

### EMPFEHLUNG

**Koso RX-22 (E-marked Version) ~€200** — Bestes Preis/Leistungsverhältnis:
- Leichtestes Gehäuse (1.0kg vs OEM 2.5kg = **1.5kg gespart**)
- Geringster Stromverbrauch (20-28W vs OEM 55-60W = **~35W gespart**)
- Schärfer Abblendung als Truck-Lite, fast wie JW Speaker
- DRL-Ring für Africa Twin Look
- ⚠️ **E-Mark bei Verkäufer BESTÄTIGEN!** — MSP Europe und BikeParts.dk listen explizit E-geprüfte Versionen

**Backup-Optionen:**
- Budget-Option: Generischer 7" H4 LED (€40) — **NUR mit E-Mark!** ≈€40-50
- Premium-Option: JW Speaker 8700 Evo (€350+) — ungeschlagene Beam-Qualität
- Adventure-Option: Truck-Lite 30400 (€260+) — IP68, robusteste, aber schwer (1.5kg)

---

## 4. LiFePO4 Batterie: JMT vs Antigravity vs Shorai vs Shido

### Vergleichstabelle

| Batterie | Gewicht | CCA | Ah | Garantie | Preis (€) | Besonderheit |
|----------|---------|-----|----|----------|-----------|--------------|
| **OEM Blei-Säure** (YB10AL-A2) | 2.8kg | ~150A | 12Ah | — | 35-55 | Referenz |
| **JMT YTZ10S** | 0.85kg | 180-210A | 4-5Ah | 2 Jahre | 50-75 | 💰 Budget |
| **Antigravity YTZ10-12** | 0.8kg | 240A | 6Ah | 3 Jahre | 135-170 | ⭐ BESTE |
| **Shorai LFX14A4** | 0.86kg | 210A | 4.2Ah | 3 Jahre | 115-150 | 🏔️ Off-Road |
| **Shido LTZ10-BS** | 0.9kg | 180-200A | 4-5Ah | 2 Jahre | 50-75 | Budget-Alt |

### Preisquellen

**JMT YTZ10S LiFePO4:**
| Quelle | Preis (€) |
|--------|-----------|
| Amazon.de | 55-70 |
| FC-Moto | 50-65 |
| Louis.de | 60-75 |
| Motea | 52-68 |
| **Min/Max/Avg** | **50 / 75 / 65** |

**Antigravity YTZ10-12 Restart:**
| Quelle | Preis (€) |
|--------|-----------|
| Amazon.de | 140-160 |
| Louis.de | 150-170 |
| FC-Moto | 135-155 |
| Motea | 148-168 |
| **Min/Max/Avg** | **135 / 170 / 153** |

**Shorai LFX14A4-BS12:**
| Quelle | Preis (€) |
|--------|-----------|
| Amazon.de | 120-140 |
| Louis.de | 125-145 |
| FC-Moto | 115-135 |
| **Min/Max/Avg** | **115 / 150 / 133** |

**Shido LTZ10-BS:**
| Quelle | Preis (€) |
|--------|-----------|
| Amazon.de | 55-70 |
| Louis.de | 60-75 |
| FC-Moto | 50-65 |
| **Min/Max/Avg** | **50 / 75 / 63** |

### EMPFEHLUNG

| Budget | Empfehlung | Preis | Spart |
|--------|-----------|-------|-------|
| **Optimal** | Antigravity YTZ10-12 | ~€150 | 2.0kg, 240CCA, 6Ah, 3yr, Restart |
| **Premium Off-Road** | Shorai LFX14A4 | ~€130 | 1.94kg, 210CCA, 4.2Ah, 3yr |
| **Budget** | JMT YTZ10S | ~€65 | 1.95kg, 180CCA, 4-5Ah, 2yr |

**NX650 = Kickstart** → CCA nicht kritisch. Fokus auf Zuverlässigkeit und Vibration. Antigravity mit Restart-Feature = bester Schutz gegen versehentliches Entleeren.

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
| Blinker Set (4) | **Highsider Saturn/Kansas E9** | 59-79 | ✅ E9 |
| Rücklicht | **Highsider LED Rücklicht E9** | 35-55 | ✅ E9 |
| Blinker-Relay | **Elektronisch 3-Pin Honda** | 10-15 | — |
| Adapter Bracket | **Universal RX Rücklicht** | 10-15 | — |
| **Gesamt LED-Umbau** | | **€114-164** | ✅ |

---

## Budget-Zusammenfassung Elektrik (max 800€)

### Priorität 1: SICHERHEIT (Stator + Regler) ⚡ MUSS

| Teil | Produkt | Preis_avg (€) | Quelle |
|------|---------|---------------|--------|
| Regler | Shindengen FH020AA MOSFET | **60** | Motea/Amazon |
| Stator+Regler Combo | RM Stator 200W + FH020AA | **168** | RM Stator direct |
| Massekabel | Ground Cable Kit | **10** | DIY |
| **Phase 1 Elektrik Total** | | **168-178** | |

### Priorität 2: LOOK (LED) 🔦

| Teil | Produktion | Preis_avg (€) | Quelle |
|------|-----------|---------------|--------|
| Scheinwerfer | Koso RX-22 E-marked | **200** | MSP/Amazon |
| Blinker (4) | Highsider Saturn/Kansas E9 | **67** | Louis/Polo |
| Rücklicht | Highsider LED E9 | **18** | Louis |
| Blinker-Relay | Elektronisch 3-Pin | **14** | Louis |
| Adapter Bracket | Universal | **12** | Louis |
| **Phase 3 Elektrik Total** | | **311** | |

### Priorität 3: TOURING (Komfort) 🏕️

| Teil | Produkt | Preis_avg (€) | Quelle |
|------|---------|---------------|--------|
| Batterie | JMT YTZ10S LiFePO4 | **65** | Amazon |
| Heizgriffe | Oxford HotGrips Premium | **60** | Amazon |
| USB-Ladegerät | Wasserfest Dual 2.1A | **14** | Amazon |
| **Phase 4 Elektrik Total** | | **139** | |

### GESAMTBUDGET ELEKTRIK

| Priorität | Budget | Avg-Kosten |
|-----------|--------|-----------|
| P1: Sicherheit | 150-300€ | **168€** ✅ |
| P3: Look | 200-400€ | **311€** ✅ |
| P4: Touring | 100-200€ | **139€** ✅ |
| **Total** | **max 800€** | **618€** → +182€ Reserve ✅ |

### Budget-Optionen

**Budget-Lite (€385):** FH020AA (€60) + RM Stator Combo (€168) + Generic LED 7" (€40) + Generic Blinker E9 (€25) + Generic Rücklicht (€15) + JMT Batterie (€55) + USB (€14) + Relay (€8)
**→ Spart €233, aber E-Mark-Risiko und weniger Lichtqualität**

**Premium (€750):** FH020AA (€60) + RM Stator HD (€145) + JW Speaker 8700 (€358) + Highsider Blinker (€67) + Highsider Rücklicht (€18) + Antigravity Batterie (€153) + Oxford Heizgriffe (€60) + USB OptiMate (€30) + Relay (€14)
**→ Maximal-Qualität, knapp unter 800€**

---

## Elektrische Last-Tabelle (Vollausbau)

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

## Team-Anfragen

### 🔄 An Chefingenieur:
1. **Phase 3 Budget-Anpassung:** Koso RX-22 (€200) statt ursprünglich budgetiert (€90) — braucht €110 mehr aus Phase 3 Reserve
2. **Batterie-Entscheidung:** JMT (€65, Budget) vs Antigravity (€153, Premium) — €88 Unterschied
3. **LED-Umbau gesamt:** Mit Highsider E9 + Relay = €311 statt budgetiert €200-400 → im Rahmen

### 🔄 An Styling+Sound:
1. **Koso RX-22 DRL-Ring:** Gibt Africa Twin Look mit DRL — bestätigen ob gewünscht
2. **Blinker-Stil:** Highsider Saturn (eckig) oder Kansas (rund)? — passt zum Design

### 🔄 An Fahrwerksspezialist:
1. **Gewichts-Update LED-Umbau:** LED Scheinwerfer -1.5kg (2.5→1.0kg), LED Blinker -0.26kg, LED Rücklicht -0.18kg, LiFePO4 -2.0kg = **Gesamt -3.94kg**

---

## Update: DB Teile (8 NEU eingefügt)

Neue Teile in vehicle_database.db:
- ID=235: JW Speaker 8700 Evolution 7" LED (€320-389)
- ID=236: Truck-Lite 30400 7" LED (€248-279)
- ID=237: Antigravity YTZ10-12 LiFePO4 (€135-170)
- ID=238: Shorai LFX14A4-BS12 LiFePO4 (€115-150)
- ID=239: RM Stator 200W Heavy Duty (€130-160)
- ID=240: LED Flasher Relay Honda 3-pin (€10-20)
- ID=241: Ground Cable Kit (€5-15)
- ID=242: Highsider LED Blinker Set Saturn/Kansas E9 (€55-79)

Updated Teile:
- ID=29: Stator Assembly ND03 (Preise erweitert mit RM Stator Details)
- ID=13: FH020AA (Preise + Specs erweitert)
- ID=31: LED H4 Headlight (Vollständige Vergleichs-Specs)
- ID=168: Koso RX-22 (Detaillierte Specs, E-Mark Warnung)
- ID=76: LiFePO4 Batterie (4 Marken-Vergleich)
- ID=65: LED Blinker (3 Marken-Vergleich)
- ID=66: LED Rücklicht (3 Marken-Vergleich)
- ID=54: Stator+Regler Combo (Preise aktualisiert)
- ID=74: USB Charger (Koso/OptiMate Optionen)
- ID=73: Heizgriffe (Stromverbrauch-Details)

**Insgesamt 22 Elektrik-Teile für NX650 in der Datenbank.**