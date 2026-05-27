# 🔧 V50 CAN-Bus Hardware Setup Guide

## Raspberry Pi 4 + PiCAN2 Duo HAT Installation

### 1. Hardware Requirements

| Component | Model | Price | Notes |
|-----------|-------|-------|-------|
| Raspberry Pi | Pi 4 Model B 2GB | ~€35 | 2GB genügt für CAN-Dashboard |
| CAN HAT | PiCAN2 Duo | ~€25 | 2x CAN-Kanäle (HS + LS) |
| Display | 7" IPS TFT 1024x600 | ~€40 | HDMI, Kapazitiv Touch |
| Gehäuse | Alu-Gehäuse für Pi4 | ~€15 | Kühlkörper für Dauerbetrieb |
| OBD2 Adapter | OBD2 Stecker auf Dupont | ~€5 | Pin 6=CAN-H, Pin 14=CAN-L |
| Stromversorgung | 5V/3A USB-C + Step-Down | ~€10 | Zündungsplus gesteurt |
| MicroSD | 32GB A2 Class 10 | ~€8 | Für OS + Logging |
| Kabel | Dupont + Schrumpfschlauch | ~€5 | Verschiedene Farben |
| **Total** | | **~€143** | Ohne Display ~€103 |

### 2. PiCAN2 Duo HAT Setup

#### 2.1 Hardware-Montage

```
PiCAN2 Duo HAT Pin-Belegung:
┌─────────────────────────────────┐
│  [DB9-1] CAN-High Bus A         │  → OBD2 Pin 6 (High-Speed CAN)
│  [DB9-2] CAN-Low Bus A          │  → OBD2 Pin 14 (High-Speed CAN)
│  [DB9-7] CAN-GND Bus A          │  → Fahrzeug-Masse
│                                  │
│  [DB9-1] CAN-High Bus B         │  → CEM Gateway (Low-Speed CAN)
│  [DB9-2] CAN-Low Bus B          │  → CEM Gateway (Low-Speed CAN)
│  [DB9-7] CAN-GND Bus B          │  → Fahrzeug-Masse
└─────────────────────────────────┘
```

1. PiCAN2 Duo HAT auf Raspberry Pi 4 stecken (GPIO-Header)
2. 9-polige SUB-D-Stecker an DB9-Buchsen des HAT anschließen
3. CAN-H und CAN-L Leitungen an OBD2-Stecker löten:
   - **Bus A (High-Speed)**: Pin 6 (CAN-H) und Pin 14 (CAN-L)
   - **Bus B (Low-Speed)**: CEM-Gateway-Pins (siehe V50 Schaltplan)

#### 2.2 Software-Konfiguration (Raspberry Pi OS)

```bash
# OS installieren: Raspberry Pi OS Lite 64-bit (Bookworm)
# SSH aktivieren, Wifi konfigurieren

# SPI aktivieren (PiCAN2 verwendet MCP2515 über SPI)
sudo raspi-config
# → Interface Options → SPI → Enable

# PiCAN2 Duo Overlay in /boot/firmware/config.txt
sudo tee -a /boot/firmware/config.txt << 'EOF'
# PiCAN2 Duo HAT
dtparam=spi=on
dtoverlay=mcp251x-can0,oscillator=16000000,interrupt=25
dtoverlay=mcp251x-can1,oscillator=16000000,interrupt=24
EOF

# Neustart
sudo reboot

# CAN-Module laden
sudo modprobe can
sudo modprobe can_raw
sudo modprobe mcp251x

# CAN-Schnittstellen konfigurieren
# High-Speed CAN (500kbps) — OBD2 Bus
sudo ip link set can0 up type can bitrate 500000
# Low-Speed CAN (125kbps) — Body/Comfort Bus
sudo ip link set can1 up type can bitrate 125000

# Verify
ip link show can0
ip link show can1
```

#### 2.3 Python-Abhängigkeiten

```bash
# python-can installieren
pip3 install python-can can-isotp

# PyQt5 für Dashboard (falls Desktop-Pi)
pip3 install PyQt5

# Zusätzliche Tools
sudo apt install can-utils
pip3 install gpsd-py3  # Optional: GPS-Logging
```

### 3. OBD2-Anschluss-Optionen

#### Option A: OBD2-Port (Empfohlen für ersten Test)
- ✅ Einfach: Stecker in OBD2-Buchse
- ✅ Keine Modifikation am Fahrzeug
- ⚠️ Nur High-Speed CAN (Bus A)
- ⚠️ Sichtbar im Fahrerfußraum

```
OBD2-Stecker (Blick auf Buchse im Auto):
┌───────────────────────────┐
│ 1  2  3  4  5  6  7  8   │
│ 9  10 11 12 13 14 15 16   │
└───────────────────────────┘

Pin 6  = CAN-High (High-Speed Bus)
Pin 14 = CAN-Low (High-Speed Bus)
Pin 5  = Signal Ground
Pin 16 = +12V Batterie (Achtung!)
Pin 4  = Chassis Ground
```

#### Option B: Fest verdrahtet (Empfohlen für Dauerbetrieb)
- ✅ Unsichtbar: Verkabelung unter Armaturenbrett
- ✅ Beide CAN-Busse (HS + LS)
- ⚠️ Mehr Aufwand beim Installieren
- ⚠️ Kabel müssen im V50-Verbund bleiben

**V50 CAN-Bus-Anschlusspunkte:**
1. **Hinter dem Radio/Info-Display** — Zugang zu HS und LS CAN
2. **CEM (Central Electronic Module)** im Beifahrerfußraum — Alle Busse
3. **OBD2-Buchse** — Nur HS CAN

**Verkabelungsplan für Dauerinstallation:**
```
Pi 4 (Handschohfach/Ablage) → PiCAN2 Duo HAT
  ├── CAN A → OBD2 Pin 6+14 (High-Speed, 500kbps)
  ├── CAN B → CEM Connector Pin X (Low-Speed, 125kbps)
  ├── GND   → Fahrzeug-Masse (Karosserie-Punkt)
  └── 5V    → Step-Down-Converter (12V Zündungsplus → 5V 3A)
```

### 4. Stromversorgung

#### 4.1 Zündungsplus-Steuerung (Empfohlen)

```
12V Zündungsplus (Klemme 15)
    │
    ├── Step-Down Converter (12V → 5V, 3A)
    │   └── USB-C → Raspberry Pi 4
    │
    └── Step-Down Converter (12V → 5V, 2A) [falls Display nötig]
        └── Micro-USB → 7" Display

V50 Zündungsplus-Quellen:
- Zigarettenanzünder (Klemme 15, geschaltet)
- Sicherungskasten Beifahrer: Sicherung #33 (Zündungsplus)
- Radio-Strom (Quadlock-Anschluss, Klemme 15)
```

#### 4.2 Abschaltautomatik (WICHTIG!)

Der Pi MUSS sich sauber herunterfahren wenn die Zündung aus ist!
Ohne Abschaltautomatik → SD-Karte beschädigt!

**Option A: Software-Lösung (Empfohlen)**
```python
# /home/pi/canbus/power_monitor.py
# Überwacht CAN-Bus-Aktivität → fährt Pi herunter nach 5 Min Stille

import subprocess, time

IDLE_TIMEOUT = 300  # 5 Minuten

last_activity = time.time()
while True:
    # Prüfe ob CAN-Activity besteht
    result = subprocess.run(['ip', '-s', 'link', 'show', 'can0'], 
                          capture_output=True, text=True)
    if 'RX packets' in result.stdout:
        # CAN-Aktivität erkannt → Reset Timer
        last_activity = time.time()
    
    if time.time() - last_activity > IDLE_TIMEOUT:
        # Keine CAN-Aktivität seit 5 Min → Zündung wahrscheinlich aus
        subprocess.run(['sudo', 'shutdown', '-h', 'now'])
        break
    
    time.sleep(10)
```

**Option B: Hardware-Lösung (Sicherer)**
- Pi-Ups-Lite oder ähnliches: Erkennt Spannungsabfall → fährt Pi sauber herunter
- Oder: Eigenes Script, das GPIO-Pin überwacht (Spannungsteiler am Zündungsplus)

**CRITICAL:**
1. Niemals Pi mit Dauerplus betreiben ohne Abschaltautomatik!
2. Akku-Entladung vermeiden: Pi zieht ~3W im Idle
3. SD-Kartenschutz: `overlayfs` verwenden oder Read-Only-Root

### 5. Display-Montage

#### 5.1 Position im V50
Beste Position: **Ablage über dem Radio/Info-Display**

```
┌─────────────────────────────────────────┐
│  V50 Armaturenbrett (Blick Fahrer)       │
│                                          │
│   ┌─────────────────────────────┐       │
│   │    Kombiinstrument (Tacho)    │       │
│   │    RPM | km/h | Tank | Temp   │       │
│   └─────────────────────────────┘       │
│                                          │
│   ┌─────────────────────────────┐       │
│   │  Info-Display (OEM)          │       │
│   │  Temperatur, Radio, etc.     │       │
│   └─────────────────────────────┘       │
│                                          │
│   ┌─────────────────────────────┐       │
│   │  7" Custom Dashboard         │ ← HIER │
│   │  (Pi + TFT im Alu-Gehäuse)  │       │
│   └─────────────────────────────┘       │
│                                          │
│   ┌──────┐  ┌─────────────────┐        │
│   │ Lüft. │  │  Ablage/Koffer  │ ← Pi hier│
│   └──────┘  └─────────────────┘        │
└─────────────────────────────────────────┘
```

**Alternativen:**
1. **OBDEinbau über Info-Display** — Custom-Gehäuse 3D-drucken
2. **Mittlere Konsole (Handschuhfach)** — Diskret, aber schwerer ablesbar
3. **A-Säule-Montage** — Rennsport-Look, nicht STEALTH-konform

#### 5.2 Sonnenlicht-Lesbarkeit

| Display-Typ | Lesbarkeit Sonne | Preis | Empfehlung |
|--------------|-----------------|-------|------------|
| Standard TFT | ❌ Schlecht | €25 | Nur für Test |
| IPS TFT (1000nit) | ✅ Gut | €40-60 | EMPFEHLUNG |
| OLED (weiß auf schwarz) | ✅ Sehr gut | €80-120 | Premium |
| E-Ink | ✅ Perfekt | €50-80 | Nur statische Daten |

**Empfehlung: 7" IPS TFT 1024x600 mit 1000nit**
- Kapazitiver Touch für Menüsteuerung
- HDMI an Pi 4
- Auto-Dimming per LDR (Lichtabhängiger Widerstand) an GPIO

#### 5.3 Auto-Dimming (Lichtsensor)

```python
# LDR an GPIO18 (Pin 12) + Kondensator (0.1µF)
# LDR between 3.3V and GPIO18, Cap between GPIO18 and GND

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
LDR_PIN = 18

def read_light():
    """Read light-dependent resistor via capacitor charge time."""
    GPIO.setup(LDR_PIN, GPIO.OUT)
    GPIO.output(LDR_PIN, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.setup(LDR_PIN, GPIO.IN)
    start = time.time()
    while GPIO.input(LDR_PIN) == GPIO.LOW:
        if time.time() - start > 0.5:
            return 0
    
    charge_time = time.time() - start
    # charge_time ~ brightness (shorter = brighter)
    return charge_time

# In Dashboard: if charge_time > 0.3 → Night mode, else → Day mode
```

### 6. Stealth-Modus

**Tastenbelegung im Dashboard:**
- `Space` → Stealth-Modus umschalten (Custom ↔ OEM-Anzeige)
- `N` → Nacht/Tag-Modus umschalten
- `Q` → Beenden
- `F11` → Vollbild umschalten

**Stealth-Fähren:**
1. Custom-Dashboard zeigt erweiterte Daten (Öltemp, Bremsdruck, Verbrauch)
2. Kurzer Tastendruck → Wechsel zu OEM-artigem Display (nur RPM, km/h, Tank)
3. Langes Halten → Komplett ausblenden (Display schwarz, nur OEM-Tacho)

### 7. Bluetooth-Smartphone-Übertragung

Optional: V50-Daten per Bluetooth an Smartphone senden.

```bash
# Bluetooth-Setup auf Pi
sudo apt install bluetooth pi-bluetooth
sudo systemctl enable bluetooth
sudo systemctl start bluetooth

# RFCOMM-Server für Smartphone-App
sudo rfcomm listen /dev/rfcomm0 1 &

# Python: Daten über Bluetooth senden
# Siehe canbus/v50_ble_server.py (TODO)
```

### 8. Rechtliche Hinweise (DE)

| Aspekt | Legalität | Hinweis |
|--------|-----------|---------|
| CAN-Bus auslesen | ✅ Legal | OBD2-Port ist standardisiert |
| Zweit-Display im Auto | ✅ Legal | Solange es nicht den Blick versperrt |
| Custom-Dashboard statt OEM | ⚠️ Graubereich | OEM-Tacho MUSS sichtbar bleiben! |
| CAN-Bus senden/schreiben | 🔴 Verboten | Nur lesen! Keine Messages an Bus senden! |
| Bluetooth im Auto | ⚠️ eingeschränkt | Nur als Anzeige, nicht zum Bedienen während Fahrt |

**WICHTIGE REGEL:**
Der originale Tacho/DIM DARF nicht ersetzt werden! Das Custom-Display ist eine 
ZUSATZANZEIGE, kein Ersatz. Der OEM-Tacho muss jederzeit sichtbar und funktionsfähig bleiben.

### 9. Ersteinrichtung Checklist

```
□ Raspberry Pi OS Lite 64-bit installiert (Bookworm)
□ SSH aktiviert, WLAN konfiguriert
□ PiCAN2 Duo HAT montiert
□ SPI in /boot/firmware/config.txt aktiviert
□ MCP251x Overlay eingetragen
□ can-utils installiert (sudo apt install can-utils)
□ python-can installiert (pip3 install python-can)
□ CAN0 (500kbps) und CAN1 (125kbps) getestet
□ OBD2-Adapter an Bus A angeschlossen
□ candump can0 — Test: Werden CAN-Messages empfangen?
□ V50 Zündung AN → CAN-Aktivität auf can0 sichtbar
□ v50_can_decoder.py --list-messages → 34 Messages gelistet
□ v50_can_sniffer.py --simulate → Simulations-Modus OK
□ v50_can_sniffer.py --monitor → Live-Daten vom V50 sichtbar
□ Display angeschlossen und lesbar
□ Auto-Dimming (LDR) getestet
□ Abschaltautomatik konfiguriert (power_monitor.py als Service)
□ Systemd-Service für Dashboard erstellt
```

### 10. Systemd-Services

```ini
# /etc/systemd/system/v50-dashboard.service
[Unit]
Description=V50 Custom Dashboard
After=network.target can-setup.service

[Service]
Type=simple
User=pi
WorkingDirectory=/opt/v50/dashboard
ExecStart=/usr/bin/python3 v50_dashboard.py --fullscreen --night
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```ini
# /etc/systemd/system/can-setup.service
[Unit]
Description=Setup CAN interfaces
Before=v50-dashboard.service

[Service]
Type=oneshot
ExecStart=/sbin/ip link set can0 up type can bitrate 500000
ExecStart=/sbin/ip link set can1 up type can bitrate 125000
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

```ini
# /etc/systemd/system/v50-power-monitor.service
[Unit]
Description=V50 Power Monitor (Auto-shutdown on ignition off)
After=v50-dashboard.service

[Service]
Type=simple
User=pi
WorkingDirectory=/opt/v50/canbus
ExecStart=/usr/bin/python3 power_monitor.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Aktivieren:
```bash
sudo systemctl enable can-setup.service v50-dashboard.service v50-power-monitor.service
sudo systemctl start can-setup.service
sudo systemctl start v50-dashboard.service
sudo systemctl start v50-power-monitor.service
```