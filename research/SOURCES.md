# Research Sources & References

## Official Documentation

| Source | Access | Cost | Coverage |
|--------|--------|------|----------|
| **VIDA** (Volvo Information Diagnostic System) | Subscription | ~€50/3 days | Complete: wiring, modules, CAN IDs |
| **DICE** (Diagnostic Communication Equipment) | Hardware | ~€500+ genuine | Required for VIDA |
| **Volvo V50 Owners Manual** | Free | — | Basic info only |
| **SAE J2284** | Purchase | ~€70 | CAN high-speed standard |
| **ISO 15765-4** | Purchase | ~€150 | CAN diagnostics standard |

## Community Sources

### Forums (High Value)

| Forum | URL | Key Topics |
|-------|-----|------------|
| **SwedeSpeed** | swedespeed.com | P1 tuning, CAN research, V50 specific |
| **VolvoForums** | volvoforums.com | General Volvo, V50 section |
| **Matthews Volvo Site** | matthewsvolvo.site | DIY repairs, module info |
| **Volvo Owners Club UK** | voc.org.uk | UK-specific, wiring help |
| **SSV (Scandinavian Volvo)** | ssv.se | Swedish forum, technical depth |

### Reddit

| Subreddit | Focus |
|-----------|-------|
| r/Volvo | General Volvo community |
| r/CarHacking | CAN bus research, OBD-II |
| r/Raspberry_pi | Pi projects, CAN HATs |
| r/CarAV | Audio, CarPlay, head units |
| r/DIYautotune | ECU tuning, sensor data |

### GitHub Projects

| Project | Description | Language |
|---------|-------------|----------|
| python-can/can | Python CAN library | Python |
| linux-can/can-utils | Linux CAN tools | C |
| commaai/openpilot | Open driving assistant (CAN DB) | C/Python |
| collin80/SavvyCAN | CAN analysis GUI | C++ |
| GENIVI/vehicle_signal_spec | Vehicle signal specification | — |
| bsmithyman/volvo-p1-can | Volvo P1 CAN research | Python |

### Wiki & Documentation

| Resource | URL | Notes |
|----------|-----|-------|
| OpenGarages Wiki | opengarages.org | Car hacking wiki |
| CAN Wiki | canwiki.org | CAN protocol reference |
| Ford C1 Platform | Wikipedia | Platform overview |
| VIDA Online | vidadb.com | Community VIDA database |

## YouTube Channels

| Channel | Focus |
|---------|-------|
| **CarHacking** | CAN bus basics, OBD-II |
| **NewMind** | Car electronics, sensors |
| **SuperRetroDash** | Custom dashboard builds |
| **Lucky Model** | 3D printed car parts |
| **Jeff Geerling** | Raspberry Pi CAN projects |

## Hardware Vendors

| Vendor | Product | Price | Notes |
|--------|---------|-------|-------|
| SK Pang | PiCAN2 Duo | €35 | Best dual CAN HAT for Pi |
| WaveShare | RS485 CAN HAT | €10 | Budget, single CAN |
| Macchina | M2 | €80 | Arduino-based car hacking |
| CANable | USBtin | €25 | USB CAN adapter |
| Carloop | Carloop | €45 | Particle-based CAN reader |
| OBDLink | EX | €50 | OBD-II scan tool |

## VIDA/DICE Alternatives

Since VIDA access is expensive and DICE hardware is proprietary:

1. **VidaDice.com** — Aftermarket DICE clone (~€30)
2. **J2534 passthru** — Generic diagnostic interface
3. **OBDDiag** — Open source OBD tool
4. **PyVOLT** — Python Volvo OBD library (limited)