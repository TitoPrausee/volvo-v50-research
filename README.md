# 🚗🏍️ Vehicle Research Database

Comprehensive multi-vehicle research database — CAN bus protocols, electronics, tuning parts, known issues, and build guides.

## Vehicles

| Vehicle | Years | Engine | CAN/OBD | Status |
|---------|-------|--------|---------|--------|
| Volvo V50 2.4i Pre-Facelift | 2004-2007 | B5244S 2.4L 5-cyl | CAN 500/125kbps + OBD-II | 34 CAN msgs, 10 sensors, 6 issues |
| Volvo V50 2.4i Facelift | 2008-2012 | B5244S | CAN (possibly 0x3xx range) | 4 OBD PIDs |
| Volvo V50 T5 Pre-Facelift | 2004-2007 | B5254T3 2.5L turbo | CAN + OBD-II | Boost PID 0x220105 |
| Volvo V50 D5 Pre-Facelift | 2004-2007 | D5244T 2.4L diesel | Denso CAN protocol | Cross-ref needed |
| Honda NX650 Dominator | 1988-2003 | RFVC 644cc single | No CAN/ECU — analog + CDI | 12 issues, 24 parts |

## Database

**SQLite** at `research/vehicle_database.db` — 18 tables, queryable:

```bash
# All CAN messages for pre-facelift V50
sqlite3 research/vehicle_database.db \
  "SELECT printf('0x%03X', can_id), source_module, name FROM can_messages WHERE variant_id=1"

# Known issues for NX650 Dominator sorted by severity
sqlite3 research/vehicle_database.db \
  "SELECT component, symptom, fix, severity FROM issues WHERE variant_id=5 ORDER BY CASE severity WHEN 'critical' THEN 0 WHEN 'major' THEN 1 WHEN 'minor' THEN 2 ELSE 3 END"

# All tuning/upgrade parts for NX650
sqlite3 research/vehicle_database.db \
  "SELECT name, brand, price_range FROM parts WHERE fitment LIKE '%5%' AND type IN ('tuning','upgrade')"
```

## Schema (18 tables)

- **Vehicle hierarchy**: `makes` → `models` → `variants`
- **Components**: `components` → `vehicle_components` (cross-reference)
- **CAN bus**: `can_buses` → `can_messages` → `can_signals`
- **Physical**: `sensors` → `connectors` → `pins`
- **Diagnostics**: `obd_pids`, `issues`
- **Parts & Tuning**: `part_categories` → `parts` → `part_fitment`
- **Projects**: `build_guides`
- **Research**: `sources`, `can_logs`

## Verification Levels

| Level | Badge | Meaning |
|-------|-------|---------|
| 0 | ⚠️ | Unverified/rumored |
| 1 | 📝 | Community/forum source |
| 2 | ✓ | Confirmed by real CAN dump |
| 3 | ✓✓ | VIDA/official documentation |

## Continuous Research

Automated cron (`vehicle-research`) runs every 6 hours, researching missing data and adding to the database. Topics rotate: CAN signals, connector pinouts, maintenance specs, forum issues, cross-references, parts verification.

## Directory Structure

```
├── research/
│   ├── vehicle_database.db    ← Main SQLite database
│   ├── DATABASE_DESIGN.md     ← Schema documentation
│   ├── CAN_DATABASE.md        ← CAN ID reference (legacy)
│   ├── PRE_FACELIFT_RESEARCH.md
│   └── web_research_day1.md
├── docs/
│   ├── CAN_BUS.md
│   ├── ENGINE.md
│   ├── ELECTRONICS.md
│   ├── CONNECTORS.md
│   ├── PRE_FACELIFT_ENGINE.md
│   └── PLATFORM.md
├── hardware/
│   ├── BOM.md                 ← Shopping list for CAN dashboard
│   └── WIRING_GUIDE.md
└── README.md
```