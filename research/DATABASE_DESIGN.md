# Vehicle Research Database — Schema Design

## Philosophy

Instead of flat files per topic, we use a **vehicle-centric hierarchy**:

```
vehicles/
  ├── make/volvo/
  │   ├── models.json          # All Volvo models
  │   └── v50_2004_2012/       # This specific vehicle
  │       ├── meta.json         # Vehicle identity, years, variants
  │       ├── engines/          # Engine variants + specs
  │       ├── can/              # CAN bus messages, signals, DBC
  │       ├── modules/          # ECUs, CEM, DIM, etc.
  │       ├── connectors/       # Pinouts, wiring
  │       ├── sensors/          # All sensors with resistance/voltage
  │       ├── obd/              # OBD-II PIDs, Mode 22
  │       ├── issues/           # Known problems, fixes
  │       └── projects/         # Build guides, BOMs, wiring
  └── ...
```

**Key principle**: Every piece of data links back to a specific vehicle + variant + model year.
No orphan data. No ambiguity about which year or engine a CAN ID belongs to.

## Access Patterns

1. "What CAN IDs does my 2005 V50 2.4i send?" → vehicle → year → engine → can
2. "Which vehicles use the AW55-51 transmission?" → component → vehicles (cross-reference)
3. "Show me all CEM pinouts" → component → connectors (across vehicles)
4. "What issues does the pre-facelift V50 have?" → vehicle → issues
5. "Which sensor is behind CAN ID 0x0C8?" → can_id → signal → sensor

## Database: SQLite + JSON hybrid

- **SQLite** for structured, queryable data (CAN messages, sensors, modules, connectors)
- **JSON files** for unstructured/research data (forum posts, build guides, notes)
- **Markdown** for human-readable documentation (auto-generated from SQLite)

This gives us:
- SQL queries for precise lookups
- JSON for flexible per-vehicle data
- Markdown for readable docs