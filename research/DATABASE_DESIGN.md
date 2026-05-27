# Vehicle Research Database — Schema Design

## Architecture

**SQLite** as primary query engine, **Markdown** for human-readable auto-generated docs.

### Why not just Markdown files?

| Need | Markdown | SQLite |
|------|----------|--------|
| "Show all CAN IDs for my 2005 V50 2.4i" | Search 5 files, read each | `WHERE variant_id=1` → instant |
| "Which vehicles share the AW55-51?" | Grep + manual cross-ref | `JOIN vehicle_components` |
| "Find sensor behind CAN 0x0C8" | Grep + hope | `JOIN can_messages` on can_id |
| "Add a new car model" | Create files, update 3 docs | `INSERT INTO variants` |
| "Sort issues by severity" | Manual | `ORDER BY severity` |

### Schema Hierarchy

```
vehicles/
  ├── makes/           → makes table (Volvo, Ford, Mazda...)
  │   └── models/      → models table (V50, S40, C30, Focus...)
  │       └── variants/ → variants table (2.4i Pre-FL, T5, D5...)
  │           ├── components ← linked via vehicle_components
  │           ├── can_messages ← filtered by variant_id + bus_id
  │           ├── sensors     ← linked to component → variant
  │           ├── connectors  ← linked to component → variant
  │           │   └── pins    ← linked to connector
  │           └── issues      ← filtered by variant_id
  └── cross-cutting:
      ├── can_buses      → high-speed (500kbps), low-speed (125kbps)
      ├── can_signals    → bit-level decoding (start_bit, length, factor, offset)
      ├── obd_pids       → standard + Volvo proprietary (Mode 22)
      ├── sources        → forum posts, VIDA docs, personal notes
      └── can_logs       → raw CAN captures for real verification
```

## Tables (15)

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `makes` | Car manufacturers | name, country |
| `models` | Car models per make | name, platform, years, body_type |
| `variants` | Engine/year variants per model | engine_code, transmission, drive_type |
| `components` | Electronic modules, sensors, transmissions | category, part_number, manufacturer |
| `vehicle_components` | Links variants to their components | variant_id, component_id, role |
| `can_buses` | CAN bus definitions | name, speed_kbps, protocol |
| `can_messages` | Every CAN message ID | can_id, bus_id, variant_id, source→dest, description |
| `can_signals` | Signal bits within messages | start_bit, bit_length, factor, offset, unit |
| `sensors` | Physical sensors | type (NTC/Hall/etc), location, resistance, voltage, CAN link |
| `connectors` | Module connectors | connector_id (A/B/C), pin_count, color |
| `pins` | Individual connector pins | pin_number, wire_color, function, signal_type |
| `obd_pids` | OBD-II PIDs (standard + proprietary) | pid, mode, formula, unit, verified |
| `issues` | Known problems per variant | symptom, cause, fix, severity, cost |
| `sources` | Research provenance | url, reliability, raw_data |
| `can_logs` | Raw CAN captures | timestamp, can_id, data_hex, decoded |

## Verification Levels

Every CAN message and OBD PID has a `verified` field:

| Level | Value | Meaning |
|-------|-------|---------|
| ⚠️ Community | 1 | Found in forum posts, untested |
| ✓ Verified | 2 | Confirmed by real CAN dump |
| ✓✓ VIDA | 3 | Confirmed by VIDA documentation |

## Current Data Status (May 2026)

| Table | Count | Source |
|-------|-------|--------|
| makes | 1 | Volvo |
| models | 1 | V50 |
| variants | 4 | 2.4i PF, 2.4i FL, T5 PF, D5 PF |
| components | 5 | CEM, ECM, DIM, ACC, TCM |
| can_messages | 34 | 27 high-speed + 7 low-speed (⚠️ community) |
| can_signals | 0 | Needs real CAN dump |
| sensors | 10 | 6 engine + 4 climate (⚠️ unverified) |
| connectors | 0 | Needs VIDA data |
| pins | 0 | Needs VIDA data |
| obd_pids | 10 | 7 standard + 3 Volvo Mode 22 |
| issues | 6 | CEM solder, DIM pixels, AW55-51, etc. |

## Query Examples

```sql
-- All CAN messages for my car (pre-facelift 2.4i)
SELECT printf('0x%03X', can_id), source_module, dest_module, name, description
FROM can_messages WHERE variant_id=1 AND bus_id=1 ORDER BY can_id;

-- Which sensors connect to which CAN messages?
SELECT s.name, s.full_name, printf('0x%03X', cm.can_id) as can_id, cm.name
FROM sensors s LEFT JOIN can_messages cm ON s.can_message_id=cm.can_id;

-- All known issues sorted by severity
SELECT component, symptom, fix, severity FROM issues WHERE variant_id=1 ORDER BY
  CASE severity WHEN 'critical' THEN 0 WHEN 'major' THEN 1 WHEN 'minor' THEN 2 ELSE 3 END;

-- Unverified CAN messages that need real CAN dump confirmation
SELECT printf('0x%03X', can_id), name, source_module FROM can_messages WHERE verified < 2;
```

## Next Steps

1. **Get real CAN dump** from V50 → import all verified IDs
2. **Populate connectors + pins** from VIDA or manual tracing
3. **Add can_signals** with exact bit decoding from CAN dump analysis
4. **Add more vehicles** (S40, C30, Focus Mk2, Mazda 3 — all P1 platform)
5. **Automate**: cron job that queries sources and suggests new data to add