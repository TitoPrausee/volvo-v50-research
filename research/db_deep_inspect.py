import sqlite3
import json

conn = sqlite3.connect('/opt/data/home/vehicle-database/research/vehicle_database.db')
cur = conn.cursor()

# 1. Parts missing prices details
print("=== PARTS MISSING PRICES (DETAILED) ===")
cur.execute("SELECT id, name, brand, part_number, oem_part_number, specs, notes FROM parts WHERE price_avg IS NULL OR price_avg = 0")
for p in cur.fetchall():
    print(f"  id={p[0]} name={p[1]} brand={p[2]} pn={p[3]} oem={p[4]} specs={p[5]} notes={p[6]}")

# 2. Check existing prices for verification
print("\n=== EXISTING PRICES (first 20) ===")
cur.execute("SELECT id, name, brand, part_number, price_min, price_max, price_avg, price_currency FROM parts WHERE price_avg IS NOT NULL AND price_avg > 0 ORDER BY id LIMIT 20")
for p in cur.fetchall():
    print(f"  id={p[0]} {p[1]} ({p[2]}) pn={p[3]} min={p[4]} max={p[5]} avg={p[6]} {p[7]}")

# 3. Count parts with prices
cur.execute("SELECT COUNT(*) FROM parts WHERE price_avg IS NOT NULL AND price_avg > 0")
print(f"\n  Parts WITH prices: {cur.fetchone()[0]}")

# 4. CAN signals overview
print("\n=== CAN SIGNALS OVERVIEW ===")
cur.execute("SELECT cs.name, cs.start_bit, cs.bit_length, cs.factor, cs.offset, cs.unit, cs.description, cm.name as msg_name, cm.can_id FROM can_signals cs JOIN can_messages cm ON cs.message_id = cm.id")
signals = cur.fetchall()
print(f"  Total CAN signals: {len(signals)}")
for s in signals[:20]:
    print(f"  msg={s[7]}(0x{s[8]:03X}) sig={s[0]} start={s[1]} len={s[2]} factor={s[3]} offset={s[4]} unit={s[5]} desc={s[6]}")

# 5. Count signals missing factor/offset
cur.execute("SELECT COUNT(*) FROM can_signals WHERE factor IS NULL OR factor = 0 OR offset IS NULL")
print(f"\n  Signals missing factor/offset: {cur.fetchone()[0]}")

# 6. Sensors overview
print("\n=== SENSORS OVERVIEW ===")
cur.execute("SELECT id, name, type, resistance_cold, resistance_hot, voltage_range, signal_description FROM sensors")
for s in cur.fetchall():
    print(f"  id={s[0]} name={s[1]} type={s[2]} cold={s[3]} hot={s[4]} vrange={s[5]} sig={s[6]}")

# 7. Connectors & pins overview
print("\n=== CONNECTORS OVERVIEW ===")
cur.execute("SELECT id, connector_id, pin_count, color, description FROM connectors")
for c in cur.fetchall():
    print(f"  id={c[0]} conn={c[1]} pins={c[2]} color={c[3]} desc={c[4]}")

# 8. Check V50 and NX650 variants
print("\n=== VARIANTS ===")
cur.execute("SELECT v.id, m.name, v.name, v.year_start, v.year_end, v.engine_code, v.market FROM variants v JOIN models m ON v.model_id = m.id")
for v in cur.fetchall():
    print(f"  id={v[0]} model={v[1]} variant={v[2]} years={v[3]}-{v[4]} engine={v[5]} market={v[6]}")

# 9. Sources count
cur.execute("SELECT category, COUNT(*) FROM sources GROUP BY category ORDER BY COUNT(*) DESC")
print("\n=== SOURCES BY CATEGORY ===")
for s in cur.fetchall():
    print(f"  {s[0]}: {s[1]}")

conn.close()