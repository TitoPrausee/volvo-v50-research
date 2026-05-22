# B5244S Engine — 2.4L 5-Cylinder

## Engine Specifications

| Spec | Value |
|------|-------|
| Engine code | B5244S |
| Displacement | 2,435 cc |
| Configuration | Inline 5-cylinder |
| Bore × Stroke | 83 × 90 mm |
| Compression ratio | 10.3:1 |
| Power | 103 kW (140 hp) @ 5,700 rpm |
| Torque | 220 Nm @ 4,000 rpm |
| Fuel | RON 95 (unleaded) |
| Injection | Multi-point EFI |
| Valve train | 20V DOHC |
| Management | Bosch ME9.1 / Denso (variant dependent) |

## ECU Pinout — B5244S (Bosch ME9.1)

⚠️ **Verify with VIDA before connecting anything!** This is community-documented.

### ECU Connector A (Engine sensors, 94 pins)

| Pin | Wire | Function | Signal |
|-----|------|----------|--------|
| A1 | Red | +12V battery (always) | Power |
| A2 | Red | +12V battery (always) | Power |
| A3 | Black | Ground | Chassis ground |
| A4 | Black | Ground | Chassis ground |
| A5 | Black | Ground | Engine ground |
| A6 | — | — | — |
| A7 | White/Blue | CAN-H | High-speed CAN |
| A8 | Blue | CAN-L | High-speed CAN |
| A15 | Yellow/Green | CKP signal (+) | Crankshaft position |
| A16 | Green/White | CKP signal (-) | Crankshaft shield |
| A20 | Brown | CMP signal | Camshaft position |
| A26 | Orange | MAF signal | Air mass flow (0-5V) |
| A30 | Pink | TPS signal 1 | Throttle position (0-5V) |
| A31 | Pink/Black | TPS signal 2 | Throttle position (0-5V) |
| A33 | Purple | ECT signal | Coolant temp (NTC) |
| A35 | Grey | MAP signal | Intake manifold pressure |
| A40 | Light green | O2 upstream signal | Lambda (wideband) |
| A41 | Light green/Black | O2 upstream return | Lambda ground |
| A45 | Light blue | APP signal 1 | Accelerator pedal (0-5V) |
| A46 | Light blue/Black | APP signal 2 | Accelerator pedal (0-5V) |
| A50 | White | EVAP purge | Canister valve |
| A55 | Yellow | Fuel injector cyl 1 | Ground-switched |
| A56 | Yellow/Black | Fuel injector cyl 2 | Ground-switched |
| A57 | Yellow/Red | Fuel injector cyl 3 | Ground-switched |
| A58 | Yellow/Blue | Fuel injector cyl 4 | Ground-switched |
| A59 | Yellow/Green | Fuel injector cyl 5 | Ground-switched |
| A65 | Red/Blue | Ignition coil cyl 1 | Trigger (5V) |
| A66 | Red/Black | Ignition coil cyl 2 | Trigger (5V) |
| A67 | Red/White | Ignition coil cyl 3 | Trigger (5V) |
| A68 | Red/Yellow | Ignition coil cyl 4 | Trigger (5V) |
| A69 | Red/Green | Ignition coil cyl 5 | Trigger (5V) |

## Sensor Locations & Wiring

### Crankshaft Position Sensor (CKP)
- **Location**: Near crankshaft pulley, driver side
- **Type**: Inductive (VR sensor)
- **Resistance**: 800-1200 Ω at 20°C
- **Gap**: 0.5-1.5mm
- ** wires**: Shielded twisted pair to ECU

### Camshaft Position Sensor (CMP)
- **Location**: Cam cover, rear side
- **Type**: Hall effect
- **Signal**: 0-5V square wave
- **Function**: Synchronized injection timing

### Mass Air Flow Sensor (MAF)
- **Location**: Between air filter and throttle body
- **Type**: Hot-wire (Bosch HFM5)
- **Signal**: 0-5V analog
- ** wires**: +12V, ground, signal, intake temp

### Coolant Temperature (ECT)
- **Location**: Thermostat housing
- **Type**: NTC thermistor (Bosch)
- **Resistance**: 10kΩ @ 25°C, ~1.3kΩ @ 80°C
- **Signal**: 0-5V via voltage divider in ECU

### Oxygen Sensors (O2)
- **Upstream**: Wideband (5-wire) — heater + signal + pump + common
- **Downstream**: Switching (4-wire) — heater + signal
- **Location**: Pre-cat (exhaust manifold), post-cat (after catalyst)

## OBD-II Access to Engine Data

All engine data is accessible via the OBD-II port using standard PIDs:

```python
import can
import time

# Connect to CAN via PiCAN2
bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)

# Read engine RPM (PID 0x0C)
def request_pid(pid):
    msg = can.Message(arbitration_id=0x7DF, data=[0x02, 0x01, pid, 0, 0, 0, 0, 0], is_extended_id=False)
    bus.send(msg)
    response = bus.recv(timeout=2)
    if response:
        return response.data
    return None

# Example: Engine RPM
data = request_pid(0x0C)
if data:
    rpm = (data[3] * 256 + data[4]) / 4
    print(f"Engine RPM: {rpm}")

# Example: Coolant Temperature
data = request_pid(0x05)
if data:
    temp_c = data[3] - 40
    print(f"Coolant Temp: {temp_c}°C")
```