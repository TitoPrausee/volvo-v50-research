import sqlite3

conn = sqlite3.connect('/opt/data/home/vehicle-database/research/vehicle_database.db')
cur = conn.cursor()

# Check existing price verification sources
cur.execute("SELECT id, url, title, category, reliability FROM sources WHERE category IN ('parts_pricing', 'pricing', 'marketplace', 'vendor', 'oem_parts', 'oem_specialist') ORDER BY id DESC LIMIT 20")
rows = cur.fetchall()
print("=== RECENT PRICING SOURCES ===")
for s in rows:
    url_short = (s[1] or '')[:80]
    print(f"  id={s[0]} cat={s[3]} rel={s[4]} title={str(s[2])[:40]} url={url_short}")

# Check all parts price ranges
print("\n=== PARTS PRICE SUMMARY ===")
cur.execute("SELECT COUNT(*), MIN(price_min), MAX(price_max), AVG(price_avg) FROM parts WHERE price_avg > 0")
row = cur.fetchone()
if row:
    print(f"  {row[0]} priced parts, min={row[1]:.2f}, max={row[2]:.2f}, avg_avg={row[3]:.2f}")

# Check for parts that haven't been verified recently
cur.execute("SELECT COUNT(*) FROM parts WHERE price_avg > 0 AND (notes IS NULL OR notes NOT LIKE '%verified%')")
cnt = cur.fetchone()
print(f"\n  Parts needing verification: {cnt[0] if cnt else 0}")

# Sample priced parts
cur.execute("SELECT id, name, part_number, price_min, price_max, price_avg, notes FROM parts WHERE price_avg > 0 AND price_min > 0 ORDER BY RANDOM() LIMIT 10")
print("\n=== SAMPLE PRICED PARTS ===")
for p in cur.fetchall():
    name_short = (p[1] or '')[:45]
    notes_short = (p[6] or '')[:60]
    print(f"  id={p[0]} {name_short} prices={p[3]:.2f}-{p[4]:.2f} avg={p[5]:.2f} notes={notes_short}")

# Check current CAN signals missing verified=2
cur.execute("SELECT COUNT(*) FROM can_messages WHERE verified < 2")
cnt2 = cur.fetchone()
print(f"\n  CAN messages not fully verified: {cnt2[0] if cnt2 else 0}")

# Check V50 CEM data completeness
cur.execute("SELECT c.connector_id, c.pin_count, c.description, COUNT(p.id) as pin_count_actual FROM connectors c LEFT JOIN pins p ON p.connector_id = c.id WHERE c.description LIKE '%CEM%' GROUP BY c.id")
print("\n=== CEM CONNECTORS ===")
for row in cur.fetchall():
    desc_short = (row[2] or '')[:60]
    print(f"  {row[0]}: {desc_short} (declared pins={row[1]}, actual={row[3]})")

# CEM pin details
cur.execute("SELECT p.pin_number, p.wire_color, p.function_name, p.signal_type, p.voltage, p.notes FROM pins p JOIN connectors c ON p.connector_id = c.id WHERE c.description LIKE '%CEM%' ORDER BY c.id, p.pin_number")
print("\n=== CEM PIN DETAILS ===")
for p in cur.fetchall():
    print(f"  pin={p[0]} color={p[1]} func={p[2]} sig={p[3]} volt={p[4]} notes={str(p[5])[:40] if p[5] else ''}")

# Count total CEM pins
cur.execute("SELECT COUNT(*) FROM pins p JOIN connectors c ON p.connector_id = c.id WHERE c.description LIKE '%CEM%'")
print(f"\n  Total CEM pins in DB: {cur.fetchone()[0]}")

# NX650 specs
cur.execute("SELECT id, name, full_name, type, resistance_cold, resistance_hot, signal_description FROM sensors WHERE name IN ('CKP', 'Oil_temp', 'V_sensor')")
print("\n=== NX650 SENSORS ===")
for s in cur.fetchall():
    sig = (s[6] or '')[:80]
    print(f"  id={s[0]} {s[1]} ({s[2]}) type={s[3]} cold={s[4]} hot={s[5]} sig={sig}")

conn.close()