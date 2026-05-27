import sqlite3
import json

DB = '/opt/data/home/vehicle-database/research/vehicle_database.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Schema
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("=== TABLES ===")
for t in tables:
    cur.execute(f'PRAGMA table_info({t})')
    cols = [(r[1], r[2]) for r in cur.fetchall()]
    print(f"\n{t}:")
    for c in cols:
        print(f"  {c[0]} {c[1]}")

# Counts
print("\n=== COUNTS ===")
for t in tables:
    cur.execute(f"SELECT COUNT(*) FROM {t}")
    print(f"{t}: {cur.fetchone()[0]}")

# Sample parts with prices
print("\n=== PARTS (with price info) ===")
cur.execute("SELECT * FROM parts LIMIT 20")
cols = [d[0] for d in cur.description]
print("Columns:", cols)
for row in cur.fetchall():
    print(row)

# Sample issues
print("\n=== ISSUES (sample) ===")
cur.execute("SELECT * FROM issues LIMIT 10")
cols = [d[0] for d in cur.description]
print("Columns:", cols)
for row in cur.fetchall():
    print(row)

# Sample sources
print("\n=== SOURCES (sample) ===")
cur.execute("SELECT * FROM sources LIMIT 10")
cols = [d[0] for d in cur.description]
print("Columns:", cols)
for row in cur.fetchall():
    print(row)

# Sensors
print("\n=== SENSORS (sample) ===")
cur.execute("SELECT * FROM sensors LIMIT 10")
cols = [d[0] for d in cur.description]
print("Columns:", cols)
for row in cur.fetchall():
    print(row)

# Connectors + pins
print("\n=== CONNECTORS (sample) ===")
cur.execute("SELECT * FROM connectors LIMIT 10")
cols = [d[0] for d in cur.description]
print("Columns:", cols)
for row in cur.fetchall():
    print(row)

print("\n=== PINS (sample) ===")
cur.execute("SELECT * FROM pins LIMIT 10")
cols = [d[0] for d in cur.description]
print("Columns:", cols)
for row in cur.fetchall():
    print(row)

conn.close()