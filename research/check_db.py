import sqlite3

DB = '/opt/data/home/vehicle-database/research/vehicle_database.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Parts with ID > 80 (recent additions)
print("=== Parts with ID > 80 ===")
cur.execute("SELECT id, name, part_number, oem_part_number, price_min, price_max, price_avg FROM parts WHERE id > 80")
for row in cur.fetchall():
    print(row)

# Part categories
print("\n=== Part categories ===")
cur.execute("SELECT id, name, description FROM part_categories")
for row in cur.fetchall():
    print(row)

# Part fitment for V50 variants
print("\n=== Part fitment (V50 variants 1-4) ===")
cur.execute("""
    SELECT pf.part_id, p.name, pf.variant_id, v.name as variant 
    FROM part_fitment pf 
    JOIN parts p ON pf.part_id = p.id 
    JOIN variants v ON pf.variant_id = v.id 
    WHERE pf.variant_id IN (1,2,3,4)
    ORDER BY pf.variant_id, pf.part_id
""")
for row in cur.fetchall():
    print(row)

# Part fitment for NX650 variants  
print("\n=== Part fitment (NX650 variants 5-6) ===")
cur.execute("""
    SELECT pf.part_id, p.name, pf.variant_id, v.name as variant 
    FROM part_fitment pf 
    JOIN parts p ON pf.part_id = p.id 
    JOIN variants v ON pf.variant_id = v.id 
    WHERE pf.variant_id IN (5,6)
    ORDER BY pf.variant_id, pf.part_id
""")
for row in cur.fetchall():
    print(row)

conn.close()