#!/usr/bin/env python3
"""
AQL ESP32 Ride-Mode Controller — Parts Compatibility Checker
=============================================================
Reads the vehicle_database.db and checks which parts are compatible
with the African Queen Lite (AQL) ESP32 Ride-Mode Controller build
on a Honda NX650 Dominator RFVC.

Budget: 5 000 € hard cap
Vehicle: NX650 Dominator (variant_id = 5)
Focus: Exhaust system, electrical, sensors, display, controller (CAN/ESP32)
"""

import sqlite3
import os
import sys
from datetime import datetime
from pathlib import Path

# ── paths ──────────────────────────────────────────────────────────────
DB_PATH = Path("/opt/data/home/vehicle-database/research/vehicle_database.db")
OUT_DIR = Path("/opt/data/home/vehicle-database/projects/african-queen-lite/tracker")
REPORT_MD = OUT_DIR / "parts_report.md"
SCRIPT_PATH = OUT_DIR / "parts_checker.py"

BUDGET_MAX = 5000.0  # € hard cap
NX650_VARIANT_ID = 5  # NX650 Dominator RFVC

# AQL build focuses – categories we care about
AQL_CATEGORIES = {
    "exhaust":         {"cat_ids": [2],  "label": "Exhaust System"},
    "electrical":      {"cat_ids": [7],  "label": "Electrical System"},
    "sensors":         {"cat_ids": [],   "label": "Sensors"},           # handled separately from sensors table
    "display":         {"cat_ids": [10, 15], "label": "Display / Instruments"},
    "controller":      {"cat_ids": [4, 14, 1], "label": "Controller / CAN / Ignition"},
}

# Known direct component / sensor IDs for NX650
NX650_COMPONENT_IDS = (6, 7, 8, 9, 10, 11, 12, 13, 14)

# ── helpers ────────────────────────────────────────────────────────────

def db_connect():
    if not DB_PATH.exists():
        print(f"❌ Database not found at {DB_PATH}")
        sys.exit(1)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def fmt_price(val, currency="€"):
    if val is None:
        return "—"
    return f"{currency}{val:.2f}"


def parse_price_range(price_range_str):
    """Best-effort parse of price_range text like '€49-65' or '80-200 EUR'."""
    if not price_range_str:
        return None, None
    s = price_range_str.replace("€", "").replace("EUR", "").replace("EUR", "").strip()
    parts = s.split("-")
    try:
        lo = float(parts[0].strip())
        hi = float(parts[1].strip()) if len(parts) > 1 else lo
        return lo, hi
    except (ValueError, IndexError):
        return None, None


# ── queries ────────────────────────────────────────────────────────────

def get_nx650_parts(conn):
    """All parts explicitly fitted to NX650 Dominator (variant 5)."""
    query = """
        SELECT p.id, p.name, p.brand, p.part_number, p.oem_part_number,
               p.type, p.price_range, p.price_min, p.price_max, p.price_avg,
               p.price_currency, p.specs, p.notes, p.install_difficulty,
               p.install_time, p.verified,
               pc.id AS cat_id, pc.name AS cat_name
        FROM parts p
        JOIN part_categories pc ON p.category_id = pc.id
        JOIN part_fitment pf ON pf.part_id = p.id
        WHERE pf.variant_id = ?
        ORDER BY pc.name, p.name
    """
    cursor = conn.execute(query, (NX650_VARIANT_ID,))
    return cursor.fetchall()


def get_sensors_for_nx650(conn):
    """Sensors belonging to NX650-relevant components (CDI, engine, etc.)."""
    query = """
        SELECT s.id, s.component_id, s.name, s.full_name, s.type,
               s.location, s.resistance_cold, s.resistance_hot,
               s.voltage_range, s.signal_description, s.notes,
               c.name AS component_name, c.category AS component_category
        FROM sensors s
        LEFT JOIN components c ON s.component_id = c.id
        WHERE s.component_id IN ({})
        ORDER BY s.component_id, s.name
    """.format(",".join("?" * len(NX650_COMPONENT_IDS)))
    cursor = conn.execute(query, NX650_COMPONENT_IDS)
    return cursor.fetchall()


def get_variant_info(conn):
    """NX650 variant details."""
    cursor = conn.execute("SELECT * FROM variants WHERE id = ?", (NX650_VARIANT_ID,))
    return cursor.fetchone()


def get_model_info(conn, model_id):
    cursor = conn.execute("SELECT * FROM models WHERE id = ?", (model_id,))
    return cursor.fetchone()


# ── classification ─────────────────────────────────────────────────────

def classify_aql_part(part, sensors, conn):
    """
    Classify a part into AQL build categories.
    Returns (category_label, compatibility_notes, is_needed).
    """
    cat_id = part["cat_id"]
    name = (part["name"] or "").lower()
    notes = (part["notes"] or "").lower()
    ptype = (part["type"] or "").lower()

    needed = False
    compat_notes = []

    # 1) Exhaust system
    if cat_id == 2:
        needed = True
        if "nla" in notes or "discontinued" in notes:
            compat_notes.append("⚠ NLA/discontinued — source used/vintage")
        if "ss" in name or "stainless" in notes:
            compat_notes.append("✓ Stainless steel — good for AQL build")
        if "legal" in notes or "ece" in notes:
            compat_notes.append("✓ ECE-approved — street legal")
        if "slip-on" in name or "slipon" in notes:
            compat_notes.append("Slip-on only — header may need separate sourcing")

    # 2) Electrical system
    elif cat_id == 7:
        needed = True
        if "mosfet" in notes or "fh020" in name:
            compat_notes.append("✓ MOSFET regulator — recommended upgrade for ESP32 power stability")
        if "led" in name:
            compat_notes.append("LED — low power draw, good for electrical budget")
        if "stator" in name or "alternator" in name:
            compat_notes.append("Charging system — verify output ≥200W for ESP32 + accessories")
        if "battery" in name:
            if "lifepo4" in notes or "lithium" in name:
                compat_notes.append("✓ LiFePO4 — lightweight, good for AQL")
            else:
                compat_notes.append("Verify CCA & capacity for ESP32 standby draw")

    # 3) Controller / CAN / Ignition
    elif cat_id in (4, 14):
        needed = True
        if "can" in name or "can" in notes:
            compat_notes.append("CAN bus component — compatible with ESP32 CAN dashboard")
        if "esp32" in name or "esp" in name:
            compat_notes.append("✓ ESP32 — core AQL controller")
        if "cdi" in name or cat_id == 4:
            compat_notes.append("Ignition system — may need interface with ESP32 RPM reader")
        if "mcp" in name or "transceiver" in name:
            compat_notes.append("CAN transceiver — required for ESP32 CAN bus")

    # 4) Display / Instruments
    elif cat_id in (10, 15):
        needed = True
        if "tft" in notes or "tft" in name or "ili" in name:
            compat_notes.append("✓ TFT display — compatible with ESP32 dashboard")
        if "oled" in name or "sh1106" in name:
            compat_notes.append("OLED — low power, good for secondary display")
        if "hdmi" in notes:
            compat_notes.append("HDMI — requires ESP32 with parallel/SPI interface or HDMI driver")
        if "custom" in name or "dashboard" in name:
            compat_notes.append("✓ ESP32 dashboard — core AQL component")

    # 5) Engine / ignition parts that relate to the controller
    elif cat_id == 1 and ("cdi" in name or "spark" in name or "ignition" in name):
        needed = True
        compat_notes.append("Engine controller-related — verify ESP32 compatibility")
        
    # 6) Sensors — cross-reference with sensor table
    if part["id"] in [s["component_id"] for s in sensors]:
        needed = True
        compat_notes.append("Has associated sensor data — relevant for AQL monitoring")

    if not needed and cat_id not in AQL_CATEGORIES:
        return None, [], False

    if not compat_notes:
        compat_notes.append("Compatible — no specific notes")

    # Determine which category label to use
    for key, cfg in AQL_CATEGORIES.items():
        if cat_id in cfg["cat_ids"]:
            return cfg["label"], compat_notes, needed

    # Fallback
    return part["cat_name"], compat_notes, needed


# ── report generation ──────────────────────────────────────────────────

def generate_report(conn):
    variant = get_variant_info(conn)
    model = get_model_info(conn, variant["model_id"])

    parts = get_nx650_parts(conn)
    sensors = get_sensors_for_nx650(conn)

    # Classify and filter
    aql_parts = []
    total_cost = 0.0
    cost_items = []

    for p in parts:
        label, notes_list, needed = classify_aql_part(p, sensors, conn)
        if not needed:
            continue

        # Best price estimate
        price_est = p["price_avg"]
        if price_est is None and p["price_range"]:
            lo, hi = parse_price_range(p["price_range"])
            price_est = (lo + hi) / 2 if lo else None

        if price_est is not None:
            total_cost += price_est

        compat_str = "; ".join(notes_list) if notes_list else "—"

        aql_parts.append({
            "name": p["name"] or "—",
            "part_number": p["part_number"] or "—",
            "oem_number": p["oem_part_number"] or "—",
            "brand": p["brand"] or "—",
            "category": label or p["cat_name"],
            "type": p["type"] or "—",
            "price_est": price_est,
            "price_range": p["price_range"] or "—",
            "compat_notes": compat_str,
            "difficulty": p["install_difficulty"] or "—",
            "verified": bool(p["verified"]),
            "notes": p["notes"] or "—",
        })

    # ── sensors section ──
    sensor_data = []
    for s in sensors:
        sensor_data.append({
            "name": s["full_name"] or s["name"],
            "short": s["name"],
            "component": s["component_name"] or f"Comp #{s['component_id']}",
            "type": s["type"],
            "location": s["location"] or "—",
            "signal": s["signal_description"] or "—",
            "voltage_range": s["voltage_range"] or "—",
        })

    # ── budget analysis ──
    budget_remaining = BUDGET_MAX - total_cost
    over_budget = total_cost > BUDGET_MAX

    # Flag over-budget items
    over_budget_items = [p for p in aql_parts if p["price_est"] is not None and p["price_est"] > 200]
    # Also flag items with issues
    flagged_items = [p for p in aql_parts if "⚠" in p["compat_notes"] or p["type"] == "repair"]

    # ── assemble markdown ──
    md_lines = []
    md_lines.append("# AQL ESP32 Ride-Mode Controller — Parts Compatibility Report")
    md_lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md_lines.append(f"**Vehicle**: {model['name']} ({variant['name']})")
    md_lines.append(f"**Years**: {variant['year_start']}–{variant['year_end']}")
    md_lines.append(f"**Engine**: {variant['engine_code']}")
    md_lines.append(f"**Budget**: {fmt_price(BUDGET_MAX)} hard cap")
    md_lines.append(f"**Total Estimated Cost**: {fmt_price(total_cost)}")
    md_lines.append(f"**Remaining**: {fmt_price(budget_remaining)}")
    md_lines.append("")
    if over_budget:
        md_lines.append("> ⛔ **OVER BUDGET** — total exceeds 5 000 € cap!")
    elif budget_remaining < 200:
        md_lines.append("> ⚠ **Budget tight** — less than 200 € remaining")
    else:
        md_lines.append("> ✅ **Within budget**")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

    # ── summary table ──
    md_lines.append("## 📋 Parts Summary")
    md_lines.append("")
    md_lines.append(f"**{len(aql_parts)}** parts identified for the AQL build across all categories.")
    md_lines.append("")
    md_lines.append("| # | Part Name | OEM Number | Category | Price Est. | Type | Compatibility Notes |")
    md_lines.append("|---|-----------|------------|----------|------------|------|---------------------|")
    for i, p in enumerate(aql_parts, 1):
        flag = " ⚠" if p["type"] == "repair" or "⚠" in p["compat_notes"] else ""
        price_str = fmt_price(p["price_est"]) if p["price_est"] is not None else p["price_range"]
        oem = p["oem_number"][:18] if p["oem_number"] != "—" else p["part_number"][:18]
        md_lines.append(f"| {i} | {p['name'][:45]} | {oem} | {p['category'][:20]} | {price_str} | {p['type'][:12]}{flag} | {p['compat_notes'][:55]} |")
    md_lines.append("")

    # ── by category ──
    md_lines.append("---")
    md_lines.append("## 📂 Parts by Category")
    md_lines.append("")

    for label_key, cfg in AQL_CATEGORIES.items():
        cat_parts = [p for p in aql_parts if p["category"] == cfg["label"]]
        if not cat_parts:
            continue
        md_lines.append(f"### {cfg['label']} ({len(cat_parts)} parts)")
        md_lines.append("")
        md_lines.append("| Part Name | Part # / OEM | Brand | Price | Difficulty | Notes |")
        md_lines.append("|-----------|-------------|-------|-------|------------|-------|")
        for p in cat_parts:
            price_str = fmt_price(p["price_est"]) if p["price_est"] is not None else p["price_range"]
            part_no = p["part_number"] if p["part_number"] != "—" else (p["oem_number"] if p["oem_number"] != "—" else "—")
            md_lines.append(f"| {p['name'][:40]} | {part_no[:25]} | {p['brand'][:15]} | {price_str} | {p['difficulty'][:12]} | {p['compat_notes'][:50]} |")
        md_lines.append("")

    # ── sensors ──
    md_lines.append("---")
    md_lines.append("## 🔌 Sensors & Inputs")
    md_lines.append("")
    md_lines.append(f"**{len(sensor_data)}** sensors available for NX650 monitoring.")
    md_lines.append("")
    md_lines.append("| Sensor | Full Name | Component | Type | Location | Signal |")
    md_lines.append("|--------|-----------|-----------|------|----------|--------|")
    for s in sensor_data:
        md_lines.append(f"| {s['short']} | {s['name'][:30]} | {s['component'][:25]} | {s['type'][:20]} | {s['location'][:25]} | {s['signal'][:35]} |")
    md_lines.append("")

    # ── budget breakdown ──
    md_lines.append("---")
    md_lines.append("## 💰 Budget Breakdown")
    md_lines.append("")
    md_lines.append(f"| Category | Count | Total Est. |")
    md_lines.append("|----------|-------|------------|")
    cat_totals = {}
    for p in aql_parts:
        cat_totals.setdefault(p["category"], {"count": 0, "total": 0.0})
        cat_totals[p["category"]]["count"] += 1
        if p["price_est"] is not None:
            cat_totals[p["category"]]["total"] += p["price_est"]
    for cat, data in sorted(cat_totals.items()):
        md_lines.append(f"| {cat} | {data['count']} | {fmt_price(data['total'])} |")
    md_lines.append(f"| **Total** | **{len(aql_parts)}** | **{fmt_price(total_cost)}** |")
    md_lines.append(f"| **Budget** | | **{fmt_price(BUDGET_MAX)}** |")
    md_lines.append(f"| **Remaining** | | **{fmt_price(budget_remaining)}** |")
    md_lines.append("")

    # ── flags ──
    md_lines.append("---")
    md_lines.append("## 🚩 Flagged Items")
    md_lines.append("")

    if over_budget_items:
        md_lines.append("### ⚠ High-Value Parts (>200€)")
        md_lines.append("")
        md_lines.append("| Part Name | Price | Category | Note |")
        md_lines.append("|-----------|-------|----------|------|")
        for p in over_budget_items:
            md_lines.append(f"| {p['name'][:40]} | {fmt_price(p['price_est'])} | {p['category'][:20]} | Single item >200€ — check priority |")
        md_lines.append("")

    if flagged_items:
        md_lines.append("### ⚠ Compatibility / Quality Flags")
        md_lines.append("")
        md_lines.append("| Part Name | Type | Issue |")
        md_lines.append("|-----------|------|-------|")
        for p in flagged_items:
            md_lines.append(f"| {p['name'][:40]} | {p['type'][:15]} | {p['compat_notes'][:55]} |")
        md_lines.append("")

    if over_budget:
        md_lines.append("### ⛔ BUDGET EXCEEDED")
        md_lines.append(f"Total estimated cost **{fmt_price(total_cost)}** exceeds the hard cap of **{fmt_price(BUDGET_MAX)}**.")
        md_lines.append(f"Reduce by **{fmt_price(total_cost - BUDGET_MAX)}** to fit budget.")
        md_lines.append("")

    # ── raw notes appendix ──
    md_lines.append("---")
    md_lines.append("## 📝 Raw Database Notes")
    md_lines.append("")
    for p in aql_parts:
        if p["notes"] and p["notes"] != "—" and len(p["notes"]) > 10:
            md_lines.append(f"- **{p['name'][:45]}**: {p['notes'][:200]}")
    md_lines.append("")

    # ── method ──
    md_lines.append("---")
    md_lines.append(f"*Report generated by `parts_checker.py` | DB: `{DB_PATH.name}` | Budget: {fmt_price(BUDGET_MAX)}*")

    return "\n".join(md_lines), aql_parts, sensor_data, total_cost, over_budget


# ── main ───────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("  AQL ESP32 Ride-Mode Controller — Parts Compatibility Checker")
    print("=" * 70)
    print(f"  DB:        {DB_PATH}")
    print(f"  Vehicle:   NX650 Dominator (variant_id={NX650_VARIANT_ID})")
    print(f"  Budget:    €{BUDGET_MAX:,.2f} hard cap")
    print(f"  Output:    {REPORT_MD}")
    print("=" * 70)
    print()

    conn = db_connect()
    try:
        md_report, aql_parts, sensors, total_cost, over_budget = generate_report(conn)

        # ── terminal report ──
        print(f"\n{'─' * 70}")
        print(f"  PARTS FOUND: {len(aql_parts)} AQL-relevant parts in database")
        print(f"  SENSORS:     {len(sensors)} NX650-related sensors")
        print(f"  TOTAL COST:  €{total_cost:,.2f}")
        print(f"  REMAINING:   €{BUDGET_MAX - total_cost:,.2f}")
        if over_budget:
            print(f"  ⛔ OVER BUDGET by €{total_cost - BUDGET_MAX:,.2f}")
        else:
            print(f"  ✅ Within budget")
        print(f"{'─' * 70}\n")

        # Category summary
        print(f"{'Category':<30} {'Count':>6} {'Total':>10}")
        print("-" * 48)
        cat_totals = {}
        for p in aql_parts:
            cat_totals.setdefault(p["category"], {"count": 0, "total": 0.0})
            cat_totals[p["category"]]["count"] += 1
            if p["price_est"] is not None:
                cat_totals[p["category"]]["total"] += p["price_est"]
        for cat, data in sorted(cat_totals.items()):
            print(f"  {cat:<28} {data['count']:>6}  €{data['total']:>8.2f}")
        print(f"  {'TOTAL':<28} {len(aql_parts):>6}  €{total_cost:>8.2f}")

        # Top items by cost
        print(f"\n{'─' * 70}")
        print("  HIGHEST-COST ITEMS (>200€)")
        print(f"{'─' * 70}")
        costly = [p for p in aql_parts if p["price_est"] is not None and p["price_est"] > 200]
        costly.sort(key=lambda x: x["price_est"] or 0, reverse=True)
        for p in costly[:10]:
            print(f"  €{p['price_est']:>7.2f}  {p['name'][:50]}")
        print()

        # Flagged
        flagged = [p for p in aql_parts if "⚠" in p["compat_notes"] or p["type"] == "repair"]
        if flagged:
            print(f"{'─' * 70}")
            print(f"  FLAGGED: {len(flagged)} items with issues")
            print(f"{'─' * 70}")
            for p in flagged[:8]:
                print(f"  ⚠ {p['name'][:48]} — {p['compat_notes'][:50]}")

        print()
        if over_budget:
            print(f"  ⛔ WARNING: Total €{total_cost:,.2f} exceeds €{BUDGET_MAX:,.2f} budget!")
            print(f"     Reduce by €{total_cost - BUDGET_MAX:,.2f}")
        else:
            print(f"  ✅ Total €{total_cost:,.2f} is within €{BUDGET_MAX:,.2f} budget (€{BUDGET_MAX - total_cost:,.2f} remaining)")

        # ── write markdown ──
        REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_MD, "w", encoding="utf-8") as f:
            f.write(md_report)
        print(f"\n  ✅ Report saved to: {REPORT_MD}")

    finally:
        conn.close()

    print(f"\n{'=' * 70}\n")


if __name__ == "__main__":
    main()
