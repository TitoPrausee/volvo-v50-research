# Volvo V50 Custom Dashboard — Hardware BOM

> Bill of Materials for RPi + PiCAN2 dash project  
> Prices in € (DE/EU sources)  
> Last updated: 2026-05-27

## Required Components

### Core Electronics

| # | Item | Spec | Price (€) | Source |
|---|------|------|-----------|--------|
| 1 | Raspberry Pi 5 | 8GB RAM, 2.4GHz quad-core | ~80 | BerryBase / Reichelt |
| 2 | PiCAN2 Duo | Dual CAN (MCP2551 × 2), fits Pi 5 | ~35 | SK Pang / Amazon DE |
| 3 | microSD Card | 32GB A2, SanDisk Extreme Pro | ~12 | Amazon DE |
| 4 | 7" HDMI IPS Display | 1024×600, with driver board | ~55 | Amazon DE |
| 5 | OBD2-to-DB9 Cable | OBD2 female to DB9 male, CAN wires on pins 2/10 | ~8 | Amazon DE |
| 6 | DB9-to-Header Cable | For PiCAN2 CAN port | ~5 | SK Pang |

### Power Supply (Automotive)

| # | Item | Spec | Price (€) | Source |
|---|------|------|-----------|--------|
| 7 | Buck Converter 12V→5V | 5A output, automotive grade (LM2596 or similar) | ~8 | Amazon DE |
| 8 | Electrolytic Capacitor | 470µF 25V (input smoothing) | ~1 | Reichelt |
| 9 | Electrolytic Capacitor | 220µF 16V (output smoothing) | ~1 | Reichelt |
| 10 | Diode (Schottky) | 1N5822 (reverse polarity protection) | ~0.50 | Reichelt |
| 11 | Car Fuse + Holder | 5A blade fuse with holder | ~3 | Amazon DE |
| 12 | Ignition-sensing Relay | 12V coil, 5A contacts, for auto power-on | ~4 | Amazon DE |

### Wiring & Connectors

| # | Item | Spec | Price (€) | Source |
|---|------|------|-----------|--------|
| 13 | JST-PH Connector Kit | For PiCAN2 CAN terminations | ~8 | Amazon DE |
| 14 | Twisted Pair Wire | CAN-H / CAN-L, 22AWG, white/green | ~6 | Amazon DE (per 5m) |
| 15 | Dupont Jumper Wires | M-F, 20cm, for Pi GPIO | ~5 | Amazon DE |
| 16 | Heat Shrink Tubing Kit | Various sizes 2-10mm | ~6 | Amazon DE |
| 17 | Automotive Wire Kit | Multi-color, 16AWG + 22AWG | ~12 | Amazon DE |

### Mounting & Enclosure

| # | Item | Spec | Price (€) | Source |
|---|------|------|-----------|--------|
| 18 | 3D Printed Dash Mount | Custom V50 cluster bezel (self-print) | ~5 (filament) | Local 3D printer |
| 19 | RPi 5 Case | Aluminum heatsink case | ~12 | Amazon DE |
| 20 | Display Bezel | Custom 3D printed or flat-cut acrylic | ~5 (filament) | Local 3D printer |
| 21 | Rubber Grommets | For cable pass-through | ~3 | Amazon DE |

### Optional Upgrades

| # | Item | Spec | Price (€) | Source |
|---|------|------|-----------|--------|
| 22 | USB GPS Module | u-blox 7/8, VK-162 | ~15 | Amazon DE |
| 23 | Bluetooth USB Dongle | CSR 4.0 | ~8 | Amazon DE |
| 24 | USB Microphone | For voice commands | ~10 | Amazon DE |
| 25 | USB Hub | Powered, 4-port | ~10 | Amazon DE |
| 26 | 10.1" HDMI Display | 1280×800 IPS (upgrade from 7") | ~75 | Amazon DE |
| 27 | PiCAN2 + GPS HAT | Combined CAN + GPS (SK Pang) | ~50 | SK Pang |
| 28 | Rear Camera Module | RCA composite, IR LEDs | ~15 | Amazon DE |

## Cost Summary

| Category | Required (€) | With Upgrades (€) |
|----------|-------------|-------------------|
| Core Electronics | 195 | 195 |
| Power Supply | 17.50 | 17.50 |
| Wiring | 37 | 37 |
| Mounting | 25 | 25 |
| **Subtotal Required** | **~275** | — |
| Optional Upgrades | — | +118 |
| **Total** | **~275** | **~393** |

## Purchase Priority

1. **Phase 1** (CAN sniffing): Pi 5 + PiCAN2 + OBD cable + SD card = ~135€
2. **Phase 2** (Dashboard): Display + power supply + wiring = ~135€
3. **Phase 3** (Enclosure): Case + mount + connectors = ~25€
4. **Phase 4** (Upgrades): GPS, BT, camera = as needed