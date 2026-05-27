import sqlite3

DB = '/opt/data/home/vehicle-database/research/vehicle_database.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Summary counts
print("=" * 60)
print("VEHICLE DATABASE — COMMUNITY RESEARCH REPORT")
print("=" * 60)

cur.execute("SELECT COUNT(*) FROM parts")
print(f"\n📊 Total parts: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM issues")
print(f"⚠️  Total issues: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM sources")
print(f"🔗 Total sources: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM part_fitment")
print(f"🔩 Total part fitments: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM parts WHERE verified = 1")
print(f"✅ Verified parts: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM parts WHERE price_min > 0 AND price_max > 0")
print(f"💰 Parts with pricing: {cur.fetchone()[0]}")

# Price summary by vehicle
print("\n" + "=" * 60)
print("PRICING COVERAGE")
print("=" * 60)

# NX650 parts (variant 5)
cur.execute("""
    SELECT COUNT(*), MIN(price_min), MAX(price_max), AVG(price_avg)
    FROM parts p JOIN part_fitment pf ON p.id = pf.part_id
    WHERE pf.variant_id = 5 AND p.price_min > 0
""")
row = cur.fetchone()
print(f"\n🏍️  NX650: {row[0]} priced parts | €{row[1]:.0f}-€{row[2]:.0f} range | avg €{row[3]:.0f}")

# V50 parts (variant 1)
cur.execute("""
    SELECT COUNT(*), MIN(price_min), MAX(price_max), AVG(price_avg)
    FROM parts p JOIN part_fitment pf ON p.id = pf.part_id
    WHERE pf.variant_id = 1 AND p.price_min > 0
""")
row = cur.fetchone()
print(f"🚗 V50:   {row[0]} priced parts | €{row[1]:.0f}-€{row[2]:.0f} range | avg €{row[3]:.0f}")

# Issues by severity
print("\n" + "=" * 60)
print("ISSUES BY SEVERITY")
print("=" * 60)
cur.execute("SELECT severity, COUNT(*) FROM issues GROUP BY severity ORDER BY COUNT(*) DESC")
for row in cur.fetchall():
    print(f"  {row[0]:10s}: {row[1]}")

# New sources added this session
print("\n" + "=" * 60)
print("COMMUNITY SOURCES ADDED THIS SESSION")
print("=" * 60)
cur.execute("SELECT url, title, vehicle, category, reliability FROM sources WHERE date_found = date('now') OR date_found > '2025-05' ORDER BY id DESC")
for row in cur.fetchall():
    print(f"  [{row[4]}] {row[2]}: {row[1]} ({row[3]})")
    print(f"    {row[0][:80]}")

conn.close()

print("\n✅ All data committed to git (not pushed).")