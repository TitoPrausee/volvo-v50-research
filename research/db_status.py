import sqlite3

conn = sqlite3.connect('/opt/data/home/vehicle-database/research/vehicle_database.db')
cur = conn.cursor()

# Check existing price verification sources
cur.execute("SELECT id, url, title, category, reliability FROM sources WHERE category IN ('parts_pricing', 'pricing', 'marketplace', 'vendor', 'oem_parts', 'oem_specialist') ORDER BY id DESC LIMIT 20")
print("=== RECENT PRICING SOURCES ===")
for s in cur.fetchall():
    url_short = (s[1] or '')[:80]
    print(f"  id={s[0]} cat={s[4]} rel={s[5]} url={url_short}")

# Check all parts price ranges
print("\n=== PARTS PRICE SUMMARY ===")
cur.execute("SELECT COUNT(*), MIN(price_min), MAX(price_max), AVG(price_avg) FROM parts WHERE price_avg > 0")
row = cur.fetchone()
print(f"  {row[0]} priced parts, min={row[1]:.2f}, max={row[2]:.2f}, avg_avg={row[3]:.2f}")

# Check for parts that haven't been verified recently
cur.execute("SELECT COUNT(*) FROM parts WHERE price_avg > 0 AND (notes IS NULL OR notes NOT LIKE '%verified%')")
print(f"\n  Parts needing verification: {cur.fetchone()[0]}")

# Check parts with outdated or suspicious prices
cur.execute("SELECT id, name, part_number, price_min, price_max, price_avg, notes FROM parts WHERE price_avg > 0 AND price_min > 0 ORDER BY RANDOM() LIMIT 10")
print("\n=== SAMPLE PRICED PARTS ===")
for p in cur.fetchall():
    name_short = (p[1] or '')[:45]
    notes_short = (p[6] or '')[:60]
    print(f"  id={p[0]} {name_short} prices={p[3]:.2f}-{p[4]:.2f} avg={p[5]:.2f} notes={notes_short}")

# Check current CAN signals missing verified=2
cur.execute("SELECT COUNT(*) FROM can_messages WHERE verified < 2")
print(f"\n  CAN messages not fully verified: {cur.fetchone()[0]}")

# Check sensors needing NTC curve data
cur.execute("SELECT id, name, type, resistance_cold, resistance_hot FROM sensors WHERE type LIKE '%NTC%'")
print("\n=== NTC SENSORS ===")
for s in cur.fetchall():
    print(f"  id={s[0]} {s[1]} ({s[2]}) cold={s[3]} hot={s[4]}")

# Check V50 CEM data completeness
cur.execute("SELECT c.connector_id, c.pin_count, c.description, COUNT(p.id) as pin_count_actual FROM connectors c LEFT JOIN pins p ON p.connector_id = c.id WHERE c.description LIKE '%CEM%' GROUP BY c.id")
print("\n=== CEM CONNECTORS ===")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[2][:60]} (declared pins={row[1]}, actual={row[3]})")

conn.close()