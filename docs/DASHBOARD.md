# Dashboard — Custom Instrument Cluster

## DIM (Driver Information Module) Details

### Original Dashboard Components

| Gauge | Protocol | CAN ID | Motor Type |
|-------|----------|--------|------------|
| Tachometer | CAN | 0x300 | VID29xx stepper |
| Speedometer | CAN | 0x308 | VID29xx stepper |
| Fuel | CAN | 0x310 | VID29xx stepper |
| Coolant temp | CAN | 0x318 | VID29xx stepper |
| Warning lights | CAN | 0x320 | LED matrix |
| Odometer | CAN | 0x328 | LCD display |
| Trip computer | CAN | 0x340 | LCD display |

### Warning Light Bitmap (CAN ID 0x320)

| Bit | Light | Meaning |
|-----|-------|---------|
| 0 | Check engine | MIL |
| 1 | ABS | ABS fault |
| 2 | Battery | Charging system |
| 3 | Oil pressure | Low oil pressure |
| 4 | Temperature | Overheating |
| 5 | Brake | Brake fluid/pads |
| 6 | Airbag | SRS fault |
| 7 | ESP | Stability control |
| 8 | Power steering | EPS fault |
| 9 | Door open | Door ajar |
| 10 | Seatbelt | Not fastened |
| 11 | Low fuel | Fuel < 8L |
| 12 | Service | Maintenance due |
| 13 | TPMS | Tire pressure |
| 14 | Glow plug | Diesel preheat (not for 2.4L petrol) |
| 15 | Immobilizer | Key not recognized |

## Custom Dashboard Options

### Option A: Add Pi Display (Non-invasive)

Keep original cluster, add a **secondary display**:
```
┌───────────────────────────────────┐
│  Original V50 Instrument Cluster    │
│  (keeps working, all warnings OK)  │
│                                    │
│  ┌──────────────────────────┐      │
│  │ ADD: 7-10" LCD below or  │      │
│  │ beside cluster showing:   │      │
│  │ - Climate status          │      │
│  │ - Boost/AFR (if turbo)    │      │
│  │ - Trip computer           │      │
│  │ - TPMS if added           │      │
│  └──────────────────────────┘      │
└───────────────────────────────────┘
```

### Option B: Full Replacement (Advanced)

Replace entire cluster with custom display:
- ⚠️ **Risk**: Warning lights are legally required in most countries
- ⚠️ **Risk**: Immobilizer LED is in DIM — removing may prevent starting
- ⚠️ **Risk**: Odometer must be accurate for legal reasons
- Need to replicate ALL warning lights on the new display

### Option C: Hybrid (Recommended)

Replace DIM display board, keep original gauge stepper motors:
1. Open the instrument cluster housing
2. Remove the LCD/LED display PCB only
3. Replace with custom RGB LCD panel (same size)
4. Keep original stepper motors (they respond to CAN directly)
5. New LCD shows: climate data, navigation, CarPlay, trip computer

## Display Hardware

### Recommended Displays for V50 Cluster

| Display | Size | Resolution | Interface | Notes |
|---------|------|-----------|-----------|-------|
| Pimoroni HyperPixel 4 | 4" | 800×480 | DPI | Fits in cluster housing |
| Waveshare 7" IPS | 7" | 1024×600 | HDMI | Dash mount |
| Standard 10.1" | 10.1" | 1280×800 | HDMI | Full DIN slot replacement |

### 3D Printed Mounts
- V50 dashboard has standard DIN and custom radio openings
- Measure: ~178mm × 100mm (single DIN) or ~178mm × 200mm (double DIN)
- Use ABS or PETG for heat resistance
- Consider a tilt/swivel mount for viewing angle