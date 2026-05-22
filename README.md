# 🚗 Volvo V50 Research — Custom Dashboard & Car Electronics

Comprehensive research project for the **Volvo V50 (2004–2012)** with **2.4L 5-cylinder engine (B5244S)** on the **P1 platform**. Goal: build a custom digital dashboard, CarPlay head unit, and full car data integration.

## 🎯 Project Goals

1. **Custom Dashboard Display** — Replace/analog instrument cluster with digital display
2. **Raspberry Pi Integration** — Intercept and decode all car signals
3. **CarPlay Head Unit** — Build a custom infotainment system controlling climate, heating, etc.
4. **Climate Control Override** — Read/display temperatures, control ACC via CAN bus
5. **Complete Car Database** — Every connector, pin, protocol, and sensor documented

## 🚘 Vehicle Info

| Detail | Value |
|--------|-------|
| Model | Volvo V50 |
| Years | 2004–2012 |
| Platform | P1 (Ford C1) |
| Engine | B5244S — 2.4L 5-cylinder, 103 kW (140 hp) |
| Transmission | 5-speed auto (AW55-51) or 5/6-speed manual |
| CAN Bus | High-speed CAN (500 kbit/s) + Low-speed CAN (125 kbit/s) |
| Shared with | Ford Focus Mk2, Mazda 3, Volvo C30, Volvo S40 |

## 📁 Repository Structure

```
volvo-v50-research/
├── docs/                    # Technical documentation
│   ├── PLATFORM.md          # P1 platform architecture
│   ├── CAN_BUS.md           # CAN bus protocols & message IDs
│   ├── ELECTRONICS.md       # All electronic modules (CEM, ECM, DIM, ACC...)
│   ├── CONNECTORS.md        # Pin diagrams & connector types
│   ├── CLIMATE_CONTROL.md   # ACC module, temperature sensors, CAN IDs
│   ├── DASHBOARD.md          # DIM, gauge protocols, display replacement
│   ├── INFOTAINMENT.md       # RTI/IVI system, CarPlay integration
│   ├── RASPBERRY_PI.md       # Pi integration, CAN hats, voltage
│   └── ENGINE.md             # B5244S ECU pinout, sensors
├── research/                 # Research tasks & sources
│   ├── TASKS.md              # Research queue with priorities
│   ├── SOURCES.md            # Known sources & forums
│   └── DATABASE_SCHEMA.md    # Database schema for car data
├── hardware/                 # Hardware specs & purchase lists
├── protocols/                # Protocol specifications & decode tables
└── wiring/                   # Wiring diagrams & pinouts
```

## 🔬 Research Status

This repo is automatically populated by a background research team over ~4 days. Check `research/TASKS.md` for progress.

## ⚠️ Disclaimer

This is for educational and personal use only. Modifying vehicle electronics can be dangerous. Always verify pinouts with VIDA/DICE before connecting anything. The author is not responsible for damage to your vehicle.