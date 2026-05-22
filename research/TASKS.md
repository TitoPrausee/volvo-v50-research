# Research Tasks — 4-Day Automated Sprint

## Priority Matrix

| # | Task | Priority | Dependencies | Status |
|---|------|----------|--------------|--------|
| 1 | Verify CAN IDs with CAN dump | P0 — Critical | Hardware (PiCAN2) | ⏳ Pending |
| 2 | DIM protocol reverse engineering | P0 — Critical | CAN access | ⏳ Pending |
| 3 | ACC protocol full decode | P0 — Critical | CAN access | ⏳ Pending |
| 4 | CEM gateway message format | P1 — High | CAN dump | ⏳ Pending |
| 5 | ECU OBD-II extended PIDs | P1 — High | OBD reader | ⏳ Pending |
| 6 | Low-speed CAN body messages | P1 — High | Second CAN bus | ⏳ Pending |
| 7 | Steering wheel button mapping | P2 — Medium | SWM CAN dump | ⏳ Pending |
| 8 | Audio system CAN protocol | P2 — Medium | IAM CAN dump | ⏳ Pending |
| 9 | Immobilizer protocol docs | P2 — Medium | VIDA access | ⏳ Pending |
| 10 | Wiring harness pinout verification | P2 — Medium | VIDA/DICE | ⏳ Pending |
| 11 | 3D printable dash mount design | P3 — Low | Measurements | ⏳ Pending |
| 12 | Display brightness auto-dim | P3 — Low | Display HW | ⏳ Pending |
| 13 | CarPlay software integration | P3 — Low | Head unit HW | ⏳ Pending |
| 14 | Temperature sensor calibration | P3 — Low | Sensor data | ⏳ Pending |
| 15 | Fuel consumption calculation | P3 — Low | MAF + RPM data | ⏳ Pending |

## Day 1: CAN Bus Discovery
- [ ] Set up PiCAN2 on Pi 5
- [ ] Connect to OBD-II port (high-speed CAN)
- [ ] Capture 1 hour of CAN traffic during driving
- [ ] Capture cold-start sequence (key position 0→I→II→start)
- [ ] Document all unique CAN IDs observed
- [ ] Match observed IDs against known V50/P1 IDs
- [ ] Identify unknown IDs for further research

## Day 2: Climate & Dashboard Deep Dive
- [ ] Capture ACC CAN messages during climate operations
- [ ] Test each climate button (temp+, temp-, fan up, fan down, A/C, auto, off)
- [ ] Document button → CAN ID mapping
- [ ] Capture DIM messages for all gauge states
- [ ] Test warning light activation (door open, seatbelt, low fuel)
- [ ] Verify exterior temperature reading accuracy
- [ ] Document interior temperature sensor readings vs actual

## Day 3: Body & Infotainment
- [ ] Capture low-speed CAN (splice into CEM wiring)
- [ ] Document door module messages (open, close, lock, unlock)
- [ ] Map steering wheel button CAN messages
- [ ] Capture radio/IAM messages (volume, source, track)
- [ ] Test DIM trip computer buttons
- [ ] Research aftermarket head unit compatibility
- [ ] Verify speaker wire colors with multimeter

## Day 4: Documentation & Database
- [ ] Compile all verified CAN IDs into database
- [ ] Cross-reference with VIDA specifications
- [ ] Create wiring diagram for PiCAN2 installation
- [ ] Write CAN decoder Python module
- [ ] Design dashboard Qt/QML mockup
- [ ] Document power supply wiring (buck converter, capacitor)
- [ ] Plan hardware purchase list with estimated costs
- [ ] Create 3D dash mount measurements

## Automated Research Sources

The following sources should be periodically checked for new information:

### Forums & Communities
- **SwedeSpeed Forums** — Volvo tuning & CAN bus research
- **VolvoForums.com** — General V50 discussions
- **Reddit r/Volvo** — Community help
- **Reddit r/CarHacking** — CAN bus reverse engineering
- **EEVblog Forums** — Electronics discussion
- **OpenGarages.org** — Car hacking wiki

### Documentation
- **VIDA/DICE** — Official Volvo diagnostic system (subscription needed)
- **Volvo V50 Wiring Diagrams** — From VIDA or third-party sources
- **SAE J2284** — CAN bus standard (high-speed)
- **ISO 15765-4** — CAN diagnostics standard (ODB-II)
- **Ford C1 Platform Service Manual** — Shared with Focus Mk2

### Open Source Projects
- **can-utils** — Linux CAN tools
- **python-can** — Python CAN library
- **SavvyCAN** — CAN bus analysis tool (GitHub)
- **CANdevStudio** — CAN simulator
- **OpenVehicle/Monitor** — Open source car monitor