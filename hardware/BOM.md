# Volvo V50 Dashboard — Bill of Materials (BOM)

> **Last updated**: May 2026
> **Currency**: € (Euro)
> **Preferred vendors**: Amazon DE, Reichelt, BerryBase, SK Pang

---

## 🟢 Required Components

### 1. Raspberry Pi 5 (4GB or 8GB)

| Spec | Value |
|------|-------|
| Model | Raspberry Pi 5 |
| RAM | 4 GB or 8 GB |
| CPU | Quad Cortex-A76 @ 2.4 GHz |
| Purpose | Main dashboard computer |
| Power | 5V DC via GPIO or USB-C PD |
| Notes | 4GB is sufficient; 8GB helpful if running CarPlay VM |

| Item | Price (€) | Vendor | Link |
|------|-----------|--------|------|
| Raspberry Pi 5 4GB | ~€65 | Amazon DE | [Link](https://www.amazon.de/dp/B0D3J5B6N9) |
| Raspberry Pi 5 8GB | ~€85 | Amazon DE | [Link](https://www.amazon.de/dp/B0D3J7H3W3) |
| Official 27W USB-C PSU (spare) | ~€15 | Amazon DE | [Link](https://www.amazon.de/dp/B0CFYYCL62) |

**Pick**: RPi 5 4GB (€65) — sufficient for CAN + display rendering.

---

### 2. PiCAN2 Duo — Dual CAN Bus HAT

| Spec | Value |
|------|-------|
| Model | PiCAN2 Duo (SK Pang) |
| CAN channels | 2 independent CAN controllers |
| Interface | SPI (MCP2515 × 2 + MCP2551 transceivers) |
| Termination | On-board 120Ω resistor per channel (jumper-selectable) |
| Supply | 5V from Raspberry Pi GPIO |
| Purpose | Read both high-speed (500kbps) and low-speed (125kbps) CAN buses |

| Item | Price (€) | Vendor | Link |
|------|-----------|--------|------|
| PiCAN2 Duo | ~€38.50 | SK Pang / Amazon DE | [Link](https://www.amazon.de/dp/B07XKVP3BC) |
| PiCAN2 Duo (direct) | ~€35 + shipping | SK Pang Electronics | [Link](https://skpang.co.uk/collections/hats/products/pican2-duo-for-raspberry-pi) |

**Note**: The Duo variant is essential for this project — the V50 has two CAN buses (high-speed + low-speed). A single-CAN HAT like the WaveShare RS485 CAN module (€10) would miss half the data.

---

### 3. 7" HDMI Display (Touchscreen)

| Option | Specs | Price (€) | Vendor | Link |
|--------|-------|-----------|--------|------|
| **Waveshare 7" IPS** | 1024×600, HDMI, capacitive touch | ~€75 | Amazon DE | [Link](https://www.amazon.de/dp/B0B3TTJ7N3) |
| **Waveshare 10.1" IPS** | 1280×800, HDMI, capacitive touch | ~€110 | Amazon DE | [Link](https://www.amazon.de/dp/B08T3G8QNN) |
| **Kuman 7" IPS** | 1024×600, HDMI, resistive touch | ~€55 | Amazon DE | [Link](https://www.amazon.de/dp/B07Z2QJ8SJ) |

**Recommendation**: 7" Waveshare IPS capacitive touch (€75) — fits the V50 dashboard space well. The 10.1" requires custom bezel fabrication.

---

### 4. OBD2-to-DB9 Cable (for CAN Bus Access)

| Spec | Value |
|------|-------|
| Type | OBD2 male → DB9 female |
| Pins connected | Pin 6 (CAN-H), Pin 14 (CAN-L), Pin 4 (GND), Pin 5 (GND) |
| Purpose | Quick, reversible connection to high-speed CAN via OBD-II port |

| Item | Price (€) | Vendor | Link |
|------|-----------|--------|------|
| OBD2 to DB9 CAN cable | ~€12 | Amazon DE | [Link](https://www.amazon.de/dp/B01MRN7B6L) |
| OBD2 extension cable (DIY) | ~€8 | Amazon DE | [Link](https://www.amazon.de/dp/B07P8X7W5B) |

**Alternative**: A standard OBD2 extension cable can be cut and wired directly to screw terminals for a more permanent install.

---

### 5. Buck Converter — 12V → 5V (Automotive Grade)

| Spec | Value |
|------|-------|
| Input | 8-36V DC (automotive rated) |
| Output | 5V DC, 3A+ |
| Efficiency | ≥90% |
| Protection | Over-current, over-voltage, reverse polarity |
| Purpose | Convert car 12V to clean 5V for Pi + display |

| Item | Price (€) | Vendor | Link |
|------|-----------|--------|------|
| LM2596 based (adjustable) 3A | ~€6 | Amazon DE | [Link](https://www.amazon.de/dp/B07XVPKG3C) |
| LM2596 (fixed 5V 3A) | ~€7 | Reichelt | [Link](https://www.reichelt.de/lm2596-step-down-modul-5v-3a-debo-lm2596-5v-p298075.html) |
| **Recommended: Pololu D24V50F5** (5V 5A, automotive) | ~€20 | BerryBase | [Link](https://www.berrybase.de/pololu-5v-5a-step-down-spannungsregler-d24v50f5) |
| Mini560 (high-efficiency, 3A) | ~€10 | Amazon DE | [Link](https://www.amazon.de/dp/B08L8G3T9J) |

**Recommendation**: Pololu D24V50F5 (€20) — automotive-rated, 5A output (enough for Pi 5 + display + accessories), excellent voltage regulation.

---

### 6. Capacitors — Crank Protection

| Item | Spec | Purpose | Price (€) | Vendor | Link |
|------|------|---------|-----------|--------|------|
| Electrolytic capacitor | 2200 µF, 16V+ | 5V rail buffer during engine start | ~€2 | Reichelt | [Link](https://www.reichelt.de/elko-radial-2-200-f-16-v-105-c-low-impedance-l-elp-2200-16-p187202.html) |
| Ceramic capacitor | 100 nF, 50V | High-frequency noise suppression | ~€0.50 | Reichelt | [Link](https://www.reichelt.de/kerko-100-nf-50-v-5-mm-bk-100n-p11416.html) |
| Capacitor combo pack | — | Both included | ~€3 | Amazon DE | [Link](https://www.amazon.de/dp/B07L9DBV7T) |

---

### 7. Wiring & Connectors

| Item | Spec | Purpose | Price (€) | Vendor | Link |
|------|------|---------|-----------|--------|------|
| Twisted pair cable (CAN) | 2×0.5 mm², twisted | CAN bus wiring | ~€5/2m | Reichelt | [Link](https://www.reichelt.de/leitung-lify-y-2-x-0-5-mm-rot-schwarz-100-m-lify-2x0-50-mm-p11934.html) |
| Silicone wire kit | 0.5–2.5 mm², multi-color | General wiring | ~€10 | Amazon DE | [Link](https://www.amazon.de/dp/B07T5W5C6C) |
| Screw terminal block (2-pin) | 5mm pitch, 10-pack | CAN connections | ~€4 | Reichelt | [Link](https://www.reichelt.de/printklemme-2-polig-5-0-mm-rm-5-0-2-pol-p12929.html) |
| Ring terminals & crimp set | — | Chassis ground connections | ~€8 | Amazon DE | [Link](https://www.amazon.de/dp/B07J3JYQ6P) |
| Heat shrink tubing kit | Assorted sizes | Insulation | ~€6 | Amazon DE | [Link](https://www.amazon.de/dp/B07Z1Z1Z1Z) |
| Fuse holder + 5A fuse | In-line mini | Protection for 5V rail | ~€5 | Reichelt | [Link](https://www.reichelt.de/sicherungshalter-mini-5-x-20-mm-fh5-p12412.html) |
| 5-way terminal block | 5-pin, 12A | Power distribution hub | ~€4 | Reichelt | [Link](https://www.reichelt.de/5-fach-verteilerklemme-12a-vk-5-p15652.html) |

---

### 8. 3D Printed Dash Mount

| Item | Spec | Price (€) | Source |
|------|------|-----------|--------|
| 7" display bezel mount | PLA/PETG, custom V50 fit | ~€5-10 (filament cost) | 3D print yourself |
| 3D printing service (if no printer) | — | ~€30-50 | JLCPCB, CraftCloud |
| PETG filament (black) | 1 kg, 1.75mm | ~€18 | Amazon DE |

**Note**: The STL files need to be designed specifically for the V50 dashboard. The design should replace the existing radio/climate panel area with a flush-mount for the 7" display. Suggested 3D model design software: Fusion 360 (free for hobbyists) or Tinkercad.

---

## 🔵 Optional Components

### 9. GPS Module

| Item | Spec | Price (€) | Vendor | Link |
|------|------|-----------|--------|------|
| U-blox 7 USB GPS | NEO-7M, USB | ~€18 | Amazon DE | [Link](https://www.amazon.de/dp/B0B1BQ2S8D) |
| U-blox 8 USB GPS | NEO-8M, USB, faster lock | ~€25 | Amazon DE | [Link](https://www.amazon.de/dp/B07RP19Z4P) |
| GPS + GLONASS | BN-880, USB/UART | ~€22 | Amazon DE | [Link](https://www.amazon.de/dp/B07RQ2V3T1) |

**Recommendation**: U-blox 8 USB GPS (€25) — simple USB plug-and-play, good sensitivity, GLONASS support.

---

### 10. Bluetooth Module

| Item | Spec | Price (€) | Vendor | Link |
|------|------|-----------|--------|------|
| ASUS BT-400 | Bluetooth 4.0 USB dongle | ~€12 | Amazon DE | [Link](https://www.amazon.de/dp/B00JLRTE4S) |
| TP-Link UB400 | Bluetooth 4.0 USB dongle | ~€10 | Amazon DE | [Link](https://www.amazon.de/dp/B07W6J4B5T) |
| CSR 8510 chipset | BT 4.0, Linux-compatible | ~€8 | Amazon DE | [Link](https://www.amazon.de/dp/B07Q2F5T5K) |

**Note**: The RPi 5 has built-in Bluetooth, so an external dongle is only needed if range or audio quality (A2DP) becomes an issue.

---

### 11. USB Hub

| Item | Spec | Price (€) | Vendor | Link |
|------|------|-----------|--------|------|
| Anker 4-port USB 3.0 hub | Compact, powered | ~€15 | Amazon DE | [Link](https://www.amazon.de/dp/B00XMD7GUA) |
| RPi 5 official USB hub | USB-C, compact | ~€12 | Amazon DE | [Link](https://www.amazon.de/dp/B0CFP2F5P1) |

**Note**: Pi 5 has 2x USB 3.0 + 2x USB 2.0 native. A hub is only needed if adding GPS + BT + keyboard + storage simultaneously.

---

### 12. Protective Case

| Item | Spec | Price (€) | Vendor | Link |
|------|------|-----------|--------|------|
| Argon ONE M.2 case (Pi 5) | Aluminum, M.2 SSD support | ~€35 | Amazon DE | [Link](https://www.amazon.de/dp/B0CQ2H1Y5T) |
| Official RPi 5 case | Red/white, active cooler | ~€12 | Amazon DE | [Link](https://www.amazon.de/dp/B0CY5H5Y8X) |
| PiCAN compatible case | Laser-cut acrylic stack | ~€15 | BerryBase | [Link](https://www.berrybase.de/gehaeuse-fuer-raspberry-pi-5) |

**Note**: Not all cases fit the PiCAN2 Duo HAT (HAT + GPIO header adds ~15mm height). The Argon ONE M.2 case does NOT fit with a HAT. Recommend a stackable acrylic case or 3D-printed custom enclosure.

---

### 13. Camera Module (optional)

| Item | Spec | Price (€) | Vendor | Link |
|------|------|-----------|--------|------|
| Raspberry Pi Camera Module 3 | 12MP, autofocus | ~€35 | Amazon DE | [Link](https://www.amazon.de/dp/B0BCCNZS5B) |
| RPi Camera Module 3 Wide | 12MP, wide angle | ~€40 | Amazon DE | [Link](https://www.amazon.de/dp/B0BCCQ4B9D) |

**Use case**: Reversing camera display on the dashboard screen.

---

### 14. Real-Time Clock (RTC)

| Item | Spec | Price (€) | Vendor | Link |
|------|------|-----------|--------|------|
| DS3231 RTC module | I2C, ±2ppm accuracy | ~€4 | Reichelt | [Link](https://www.reichelt.de/raspberry-pi-real-time-clock-ds3231-rtc-pi-1-p259485.html) |

**Note**: Important for accurate timekeeping — the Pi has no battery-backed RTC and the car has no persistent network. Without this, time resets every boot.

---

## 💰 Total Estimated Cost

### Minimum Build (Required Only)

| Component | Cost (€) |
|-----------|----------|
| Raspberry Pi 5 4GB | 65 |
| PiCAN2 Duo | 38 |
| 7" HDMI Display (Waveshare) | 75 |
| OBD2-to-DB9 cable | 12 |
| Buck converter (LM2596) | 7 |
| Capacitors (2200µF + 100nF) | 3 |
| Wiring & connectors | 30 |
| 3D printed dash mount (DIY) | 10 |
| **Total (self-print)** | **€240** |

### With Optional Extras

| Component | Cost (€) |
|-----------|----------|
| Required components (above) | 240 |
| GPS module (U-blox 8) | 25 |
| RTC (DS3231) | 4 |
| USB hub | 15 |
| Protective case (acrylic stack) | 15 |
| Reversing camera | 35 |
| 3D printing service (no printer) | +20 |
| **Total (fully equipped, service-printed)** | **€354** |

### With Premium Upgrades

| Upgrade | Cost increase (€) |
|---------|-------------------|
| RPi 5 8GB (vs 4GB) | +20 |
| Pololu D24V50F5 buck (vs LM2596) | +13 |
| 10.1" display (vs 7") | +35 |
| Argon ONE M.2 case | +35 (but HAT incompatible!) |

---

## 📋 Vendor Quick Reference

| Vendor | Use For | Shipping | Returns |
|--------|---------|----------|---------|
| **Amazon DE** | Everything — displays, cables, Pi, tools | Free/Prime | 30 days easy returns |
| **Reichelt** | Electronics — caps, connectors, wire, tools | €4.90 | 14 days |
| **BerryBase** | Raspberry Pi, HATs, Pololu regulators | €3.99 | 14 days |
| **SK Pang** | PiCAN2 Duo (direct purchase) | ~€5 UK->DE | Direct contact |
| **JLCPCB** | 3D printing & PCB fabrication | ~€5 | Varies |

---

## ⚠️ Important Notes

1. **PiCAN2 Duo + Pi 5 compatibility**: PiCAN2 Duo uses SPI channels CE0 (CAN0) and CE1 (CAN1). Works with Pi 5 out of the box — no level shifter needed (both use 3.3V logic).
2. **Display power**: The 7" Waveshare display can be powered from the Pi 5's USB-C (5V 3A) or directly from the 5V buck converter. Direct power is recommended to avoid overloading the Pi.
3. **120Ω termination**: The PiCAN2 Duo has on-board 120Ω termination resistors per channel activated by jumpers. Enable them if the Pi is the only node on the bus end.
4. **Fuses**: Always fuse the 12V input line before the buck converter. A 5A inline mini-fuse is recommended.
5. **Ground loops**: Use a single ground point for all 12V returns (star grounding). Do NOT use chassis ground for signal returns.
