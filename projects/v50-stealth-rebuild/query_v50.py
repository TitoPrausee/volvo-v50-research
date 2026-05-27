import sqlite3
conn = sqlite3.connect('/opt/data/home/vehicle-database/research/vehicle_database.db')
cursor = conn.cursor()

# Get unique V50 parts (deduplicated by name)
cursor.execute("""
SELECT DISTINCT p.name, p.brand, p.part_number, p.price_min, p.price_max, p.price_avg, 
       pc.name as category, p.verified, p.notes
FROM parts p 
JOIN part_categories pc ON p.category_id = pc.id
JOIN part_fitment pf ON pf.part_id = p.id
WHERE pf.variant_id IN (1, 2, 3, 4)
AND p.name NOT LIKE '%NX650%'
AND p.name NOT LIKE '%Honda%'
AND p.name NOT LIKE '%Dominator%'
AND p.name NOT LIKE '%Africa%'
AND p.name NOT LIKE '%Keihin%'
AND p.name NOT LIKE '%Carburetor%'
AND p.name NOT LIKE '%Heidenau%'
AND p.name NOT LIKE '%Mitas%'
AND p.name NOT LIKE '%Shinko%'
AND p.name NOT LIKE '%Chain%'
AND p.name NOT LIKE '%Sprocket%'
AND p.name NOT LIKE '%Fork%'
AND p.name NOT LIKE '%YSS%'
AND p.name NOT LIKE '%Hagon%'
AND p.name NOT LIKE '%Race Tech%'
AND p.name NOT LIKE '%Wirth%'
AND p.name NOT LIKE '%Stator%'
AND p.name NOT LIKE '%Battery%'
AND p.name NOT LIKE '%Voltage Regulator%'
AND p.name NOT LIKE '%LED H4%'
AND p.name NOT LIKE '%LED Blinker%'
AND p.name NOT LIKE '%LED Rear%'
AND p.name NOT LIKE '%Wheel Bearing%'
AND p.name NOT LIKE '%OEM Oil Filter (Honda)%'
AND p.name NOT LIKE '%Hiflo%'
AND p.name NOT LIKE '%UNI%'
AND p.brand NOT LIKE '%Honda%'
AND p.brand NOT LIKE '%All Balls%'
AND p.brand NOT LIKE '%DID%'
AND p.brand NOT LIKE '%Delkevic%'
AND p.brand NOT LIKE '%Koso%'
ORDER BY pc.name, p.name
""")

parts = cursor.fetchall()
print(f"=== UNIQUE V50 PARTS ({len(parts)}) ===")
current_cat = None
for p in parts:
    cat = p[7] if isinstance(p[7], str) else str(p[7])
    if cat != current_cat:
        current_cat = cat
        print(f"\n--- {current_cat.upper()} ---")
    verified = "V" if p[6] == 1 else "?"
    price = f"E{p[3]}-{p[4]}" if p[3] and p[4] else f"E{p[5]}" if p[5] else "?"
    name = p[0][:60]
    brand = p[1] if p[1] else ""
    pn = p[2] if p[2] else ""
    print(f"  [{verified}] {name} ({brand}) PN:{pn} | {price}")

# Count V50-unique parts
print(f"\n\n=== V50 PARTS BY CATEGORY ===")
cursor.execute("""
SELECT pc.name, COUNT(DISTINCT p.id)
FROM parts p 
JOIN part_categories pc ON p.category_id = pc.id
JOIN part_fitment pf ON pf.part_id = p.id
WHERE pf.variant_id IN (1, 2)
GROUP BY pc.name
ORDER BY pc.name
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} parts")

conn.close()