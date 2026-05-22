# Infotainment — CarPlay & Audio Integration

## Original V50 Audio Systems

| System | Code | Features | CAN |
|--------|------|----------|-----|
| Performance | IAM | Radio + CD | Low-speed |
| High Performance | IAM + AMP | Radio + CD + 4×40W amp | Low-speed |
| Premium Sound | IAM + AUD + SUB | Dynaudio, Dolby, 10 speakers | Low-speed |
| RTI Navigation | IAM + RTI | Navigation + audio | Low-speed |

## IAM (Integrated Audio Module) Integration

The IAM is on the **Low-Speed CAN** bus. All audio commands go through CEM → IAM.

### Steering Wheel Controls (SWM → CEM → IAM)

| CAN ID | Byte | Button | Function |
|--------|------|--------|----------|
| 0x400 | 0x01 | Vol+ | Volume up |
| 0x400 | 0x02 | Vol- | Volume down |
| 0x400 | 0x03 | Source | Radio/Media/Aux |
| 0x400 | 0x04 | Next | Next track/station |
| 0x400 | 0x05 | Prev | Previous track/station |
| 0x430 | 0x01 | Cruise+ | Cruise control set+ |
| 0x430 | 0x02 | Cruise- | Cruise control set- |
| 0x430 | 0x03 | Cruise cancel | Cancel cruise |

### Speaker Wiring (Standard Performance)

| Location | Size | Impedance | Wire Color |
|----------|------|-----------|-------------|
| Front left dash tweeter | 1" | 4Ω | Orange/White |
| Front left door mid | 6.5" | 4Ω | Green/White |
| Front right dash tweeter | 1" | 4Ω | Orange/Black |
| Front right door mid | 6.5" | 4Ω | Green/Black |
| Rear left | 6.5" | 4Ω | Blue/White |
| Rear right | 6.5" | 4Ω | Blue/Black |

### Amp Turn-On
- The factory amp remote turn-on wire is **green/yellow** at the IAM connector
- It gets +12V when the key is in position I or II
- For aftermarket: Use the same wire or ignition-switched +12V

## CarPlay Integration Options

### Option A: Replace Head Unit (Recommended for V50)

The V50 has a standard **double-DIN** opening (≈178mm × 100mm × 160mm depth).

**Recommended Android Head Units with CarPlay:**
1. **ATOTO F7** — 7" wireless CarPlay/Android Auto, ~€150
2. **Pumpkin 10.1"** — Large display, wireless CarPlay, ~€250
3. **Joying 9"** — UD7 platform, CarPlay, CAN bus adapter available

**Key: Must connect to Low-Speed CAN for steering wheel controls!**

### Option B: Raspberry Pi CarPlay

Build custom CarPlay with a Pi + dash display:

```
┌─────────────────────────────────────────┐
│           Raspberry Pi 5                 │
│  ┌──────────┐  ┌───────────┐            │
│  │ PiCAN2   │  │ USB BT    │            │
│  │ (CAN0    │  │ (CarPlay  │            │
│  │  CAN1)   │  │  audio)   │            │
│  └────┬─────┘  └─────┬─────┘            │
│       │               │                  │
│  ┌────▼─────┐  ┌──────▼──────┐          │
│  │ CAN      │  │ iOS Device  │          │
│  │ Decoder  │  │ (CarPlay    │          │
│  │ (car)    │  │  protocol)  │          │
│  └──────────┘  └─────────────┘          │
│                                          │
│  ┌───────────────────────────┐           │
│  │ Qt/QML Dashboard UI      │           │
│  │ - CarPlay video out       │           │
│  │ - CAN data gauges         │           │
│  │ - Climate overlay         │           │
│  └───────────────────────────┘           │
│                    │                      │
│            ┌──────▼──────┐               │
│            │  7-10" LCD   │               │
│            │  HDMI output │               │
│            └─────────────┘               │
└─────────────────────────────────────────┘
```

### CarPiPhone Integration Software

```bash
# Install CarPlay receiver on Pi
sudo apt install -y cmake libusb-1.0-0-dev libssl-dev
cd /opt && git clone https://github.com/nicknisi/CarPlay.git
cd CarPlay && mkdir build && cd build
cmake .. && make -j4

# Or use a pre-built Android head unit with CAN bus support
# ATOTO/Pumpkin units have CAN bus decoders for Volvo P1
```

## Audio Architecture for Custom System

```
Raspberry Pi HDMI Audio OUT
         │
         ▼
    ┌─────────┐     ┌─────────────┐
    │ DSP/AMP │────▶│  Speakers   │
    │ (or     │────▶│  (original  │
    │ factory │     │   4Ω wiring)│
    │ amp-in) │     └─────────────┘
    └─────────┘

Option 1: Use factory amp (connect to IAM input wires)
Option 2: Replace amp with DSP (Dayton DSP-408, ~€120)
Option 3: Pi → USB DAC → 4-channel amp → speakers
```

## CAN Bus Adapter for Aftermarket Head Units

Most aftermarket head units need a **CAN bus steering wheel adapter** for the V50:

| Brand | Adapter | Notes |
|-------|---------|-------|
| Connects2 | CTSVO004 | Volvo P1 CAN → Key1/Key2 |
| PAC | RP4-VW11 | CAN → programmable outputs |
| Metra | ASWC-1 | Universal CAN → SWC |

These adapters read the Low-Speed CAN and output:
- Steering wheel button presses (resistive or CAN)
- Amplifier turn-on signal
- Illumination dimmer signal
- Reverse gear signal (for backup camera)