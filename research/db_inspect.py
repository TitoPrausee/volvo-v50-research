import sqlite3

conn = sqlite3.connect('/opt/data/home/vehicle-database/research/vehicle_database.db')
cur = conn.cursor()

# Get all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()
print("=== ALL TABLES ===")
for t in tables:
    print(t[0])

# Get schemas
for t in tables:
    tname = t[0]
    cur.execute(f"PRAGMA table_info({tname})")
    cols = cur.fetchall()
    print(f"\n=== {tname} COLUMNS ===")
    for c in cols:
        pk = 'PK' if c[5] else ''
        dfl = c[4] if c[4] else ''
        print(f"  {c[1]} ({c[2]}) {pk} default={dfl}")

# Count records per table
print("\n=== RECORD COUNTS ===")
for t in tables:
    tname = t[0]
    cur.execute(f"SELECT COUNT(*) FROM {tname}")
    cnt = cur.fetchone()[0]
    print(f"  {tname}: {cnt}")

# Parts missing prices
print("\n=== PARTS MISSING PRICES ===")
cur.execute("SELECT id, name, brand, part_number FROM parts WHERE price_avg IS NULL OR price_avg = 0")
missing = cur.fetchall()
print(f"  Count: {len(missing)}")
for p in missing[:30]:
    print(f"  id={p[0]} name={p[1]} brand={p[2]} pn={p[3]}")

conn.close()