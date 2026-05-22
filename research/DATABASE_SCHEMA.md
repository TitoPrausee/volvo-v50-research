# Database Schema — Volvo V50 Car Data

## Overview

SQLite database for storing all researched car data: CAN messages, connectors, sensors, modules, and wiring.

## Schema

```sql
-- CAN Message Definitions
CREATE TABLE can_messages (
    id INTEGER PRIMARY KEY,
    can_id INTEGER NOT NULL,           -- CAN arbitration ID (hex)
    can_bus TEXT NOT NULL,              -- 'high' or 'low'
    name TEXT NOT NULL,                 -- Human-readable name
    direction TEXT,                     -- 'TX' (module sends) or 'RX' (module receives)
    source_module TEXT,                 -- Sending module code
    dest_module TEXT,                   -- Receiving module code (or 'broadcast')
    description TEXT,
    verified INTEGER DEFAULT 0,         -- 0=unverified, 1=community, 2=confirmed
    last_verified_date TEXT,
    notes TEXT,
    UNIQUE(can_id, can_bus)
);

-- CAN Signal Definitions (within a message)
CREATE TABLE can_signals (
    id INTEGER PRIMARY KEY,
    can_id INTEGER NOT NULL,            -- References can_messages.can_id
    signal_name TEXT NOT NULL,           -- e.g. 'engine_rpm', 'coolant_temp'
    start_bit INTEGER NOT NULL,          -- Bit position in DLC
    bit_length INTEGER NOT NULL,         -- Number of bits
    byte_order TEXT DEFAULT 'little',    -- 'little' or 'big' endian
    factor REAL DEFAULT 1.0,            -- Multiplier
    offset REAL DEFAULT 0.0,             -- Additive offset
    unit TEXT,                           -- 'rpm', '°C', '%', etc.
    min_value REAL,                      -- Minimum valid value
    max_value REAL,                      -- Maximum valid value
    description TEXT,
    FOREIGN KEY (can_id) REFERENCES can_messages(can_id)
);

-- Electronic Modules
CREATE TABLE modules (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,           -- 'CEM', 'ECM', 'DIM', etc.
    full_name TEXT NOT NULL,             -- 'Central Electronic Module'
    can_bus TEXT NOT NULL,                -- 'high', 'low', 'both'
    location TEXT,                        -- Physical location in car
    part_number TEXT,                    -- Volvo part number
    connector_count INTEGER,             -- Number of connectors
    description TEXT
);

-- Module Connectors
CREATE TABLE connectors (
    id INTEGER PRIMARY KEY,
    module_code TEXT NOT NULL,            -- References modules.code
    connector_id TEXT NOT NULL,           -- 'A', 'B', 'C', etc.
    pin_count INTEGER NOT NULL,
    color TEXT,                          -- Connector housing color
    description TEXT,
    FOREIGN KEY (module_code) REFERENCES modules(code),
    UNIQUE(module_code, connector_id)
);

-- Connector Pins
CREATE TABLE pins (
    id INTEGER PRIMARY KEY,
    module_code TEXT NOT NULL,
    connector_id TEXT NOT NULL,
    pin_number INTEGER NOT NULL,
    wire_color TEXT,                      -- Wire color code
    function_name TEXT,                   -- e.g. 'CAN-H', '+12V ignition'
    signal_type TEXT,                     -- 'power', 'ground', 'can', 'analog', 'digital'
    voltage REAL,                        -- Nominal voltage (if applicable)
    notes TEXT,
    FOREIGN KEY (module_code, connector_id) REFERENCES connectors(module_code, connector_id),
    UNIQUE(module_code, connector_id, pin_number)
);

-- Sensors
CREATE TABLE sensors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,                  -- 'CKP', 'ECT', 'MAF', etc.
    full_name TEXT NOT NULL,              -- 'Crankshaft Position Sensor'
    type TEXT NOT NULL,                   -- 'NTC', 'Hall', 'VR', 'Piezo', 'Potentiometer'
    location TEXT,                        -- Where in the car
    module TEXT,                           -- Connected to which module
    resistance_cold REAL,                -- Ohms at 20°C (for NTC)
    resistance_hot REAL,                 -- Ohms at 80°C (for NTC)
    voltage_range TEXT,                   -- '0-5V', '0-12V', etc.
    signal_description TEXT,
    can_id INTEGER,                       -- CAN ID that carries this sensor's data
    FOREIGN KEY (can_id) REFERENCES can_messages(can_id)
);

-- CAN Logs (raw captures)
CREATE TABLE can_logs (
    id INTEGER PRIMARY KEY,
    timestamp REAL NOT NULL,             -- Unix timestamp
    can_bus TEXT NOT NULL,               -- 'high' or 'low'
    can_id INTEGER NOT NULL,
    dlc INTEGER NOT NULL,                -- Data Length Code
    data BLOB NOT NULL,                  -- Raw bytes
    decoded_name TEXT,                    -- If decoded
    decoded_value TEXT,                   -- Decoded value
    notes TEXT
);

-- Index for fast CAN ID lookups
CREATE INDEX idx_can_logs_id ON can_logs(can_id);
CREATE INDEX idx_can_logs_ts ON can_logs(timestamp);
CREATE INDEX idx_can_signals_name ON can_signals(signal_name);
```

## Usage Examples

```python
import sqlite3

db = sqlite3.connect("/opt/volvo/data/volvo_v50.db")

# Find all climate-related CAN messages
for row in db.execute("""
    SELECT can_id, name, description FROM can_messages 
    WHERE name LIKE '%climate%' OR name LIKE '%temp%' OR name LIKE '%fan%'
"""):
    print(f"0x{row[0]:03X}: {row[1]} — {row[2]}")

# Get all pins on CEM connector A
for row in db.execute("""
    SELECT pin_number, wire_color, function_name, signal_type 
    FROM pins WHERE module_code='CEM' AND connector_id='A' 
    ORDER BY pin_number
"""):
    print(f"  Pin {row[0]:2d}: {row[1]:15s} {row[2]:20s} ({row[3]})")

# Get sensor data for coolant temperature
for row in db.execute("""
    SELECT s.full_name, s.type, s.resistance_cold, s.resistance_hot, m.can_id
    FROM sensors s 
    JOIN can_messages m ON s.can_id = m.can_id 
    WHERE s.name = 'ECT'
"""):
    print(f"{row[0]}: {row[1]}, {row[2]}Ω@20°C, {row[3]}Ω@80°C, CAN 0x{row[4]:03X}")
```