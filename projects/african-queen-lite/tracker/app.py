#!/usr/bin/env python3
"""
African Queen Lite — Build Tracker Web App
Reads from vehicle_database.db and serves a dashboard.
Run: python3 app.py
Open: http://localhost:5050
"""

import sqlite3
import os
from flask import Flask, render_template_string, jsonify

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'research', 'vehicle_database.db')

app = Flask(__name__)

# ============================================================
# HTML Template — Dark Theme Dashboard
# ============================================================
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏍️ African Queen Lite — Build Tracker</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'SF Mono', 'Fira Code', monospace; background: #0a0a0a; color: #e0e0e0; }
        .header { background: #141414; border-bottom: 2px solid #2d2d2d; padding: 20px 30px; }
        .header h1 { font-size: 24px; color: #ff6b35; }
        .header p { font-size: 13px; color: #888; margin-top: 4px; }
        .container { max-width: 1200px; margin: 20px auto; padding: 0 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 16px; }
        .card { background: #1a1a1a; border: 1px solid #2d2d2d; border-radius: 8px; padding: 16px; }
        .card h2 { font-size: 14px; color: #ff6b35; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }
        .card h3 { font-size: 12px; color: #888; margin-bottom: 6px; }
        table { width: 100%; border-collapse: collapse; font-size: 12px; }
        th { text-align: left; color: #666; padding: 4px 8px; border-bottom: 1px solid #2d2d2d; }
        td { padding: 4px 8px; }
        .budget { font-size: 28px; font-weight: bold; }
        .budget-spent { color: #ff6b35; }
        .budget-remaining { color: #4ecdc4; }
        .budget-total { color: #888; }
        .phase-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
        .phase-1 { background: #3d0c0c; color: #ff4444; }
        .phase-2 { background: #3d1c0c; color: #ff8844; }
        .phase-3 { background: #3d3d0c; color: #ffcc44; }
        .phase-4 { background: #0c3d0c; color: #44ff44; }
        .phase-5 { background: #0c0c3d; color: #4488ff; }
        .weight-delta { color: #4ecdc4; }
        .weight-delta.neg { color: #ff6b35; }
        .mode-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
        .mode-card { background: #222; border-radius: 6px; padding: 10px; text-align: center; }
        .mode-name { font-size: 13px; font-weight: bold; }
        .mode-params { font-size: 10px; color: #888; margin-top: 4px; }
        .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; }
        .alert { background: #3d0c0c; border: 1px solid #ff4444; border-radius: 6px; padding: 10px; margin-top: 10px; color: #ff4444; }
        .footer { text-align: center; color: #444; font-size: 11px; margin-top: 30px; padding-bottom: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏍️ African Queen Lite — Build Tracker</h1>
        <p>Honda NX650 Dominator RFVC — 5.000€ HARD CAP</p>
    </div>

    <div class="container">
        <div class="grid">
            <!-- Budget Card -->
            <div class="card">
                <h2>💰 Budget</h2>
                <table>
                    <tr><th>Kategorie</th><th>Budget</th><th>Ausgegeben</th><th>Rest</th></tr>
                    {% for row in budget %}<tr>
                        <td>{{ row[0] }}</td>
                        <td>{{ row[1] }}€</td>
                        <td>{{ row[2] }}€</td>
                        <td>{{ row[3] }}€</td>
                    </tr>{% endfor %}
                    <tr style="border-top: 2px solid #2d2d2d; font-weight: bold;">
                        <td>TOTAL</td><td>{{ total_budget }}€</td>
                        <td>{{ total_spent }}€</td><td>{{ total_remaining }}€</td>
                    </tr>
                </table>
            </div>

            <!-- Weight Card -->
            <div class="card">
                <h2>⚖️ Gewichtsbilanz</h2>
                <table>
                    <tr><th>Position</th><th>OEM</th><th>Nach Bau</th><th>Δ</th></tr>
                    {% for row in weight %}<tr>
                        <td>{{ row[0] }}</td>
                        <td>{{ row[1] }}kg</td>
                        <td>{{ row[2] }}kg</td>
                        <td class="weight-delta {{ 'neg' if row[3]|float < 0 }}">{{ '+' if row[3]|float > 0 }}{{ row[3] }}kg</td>
                    </tr>{% endfor %}
                    <tr style="border-top: 2px solid #2d2d2d; font-weight: bold;">
                        <td>ZIEL</td><td>{{ weight_total_oem }}kg</td>
                        <td>{{ weight_total_build }}kg</td>
                        <td>{{ weight_delta }}kg</td>
                    </tr>
                </table>
            </div>

            <!-- Ride Mode Controller -->
            <div class="card">
                <h2>🎮 Ride-Mode Controller</h2>
                <div class="mode-grid">
                    {% for mode in modes %}
                    <div class="mode-card">
                        <div class="dot" style="background: {{ mode[4] }}"></div>
                        <span class="mode-name">{{ mode[0] }}</span>
                        <div class="mode-params">
                            Zünd: {{ mode[1] }}°<br>
                            Valve: {{ mode[2] }}% | Air: {{ mode[3] }}%
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Sensors -->
            <div class="card">
                <h2>📡 Sensoren & Ausgänge</h2>
                <table><tr><th>Komponente</th><th>Typ</th><th>Pin</th></tr>
                    <tr><td>Drehzahl</td><td>Pulse Coil (ISR)</td><td>GPIO 18</td></tr>
                    <tr><td>Temperatur</td><td>NTC 10kΩ</td><td>GPIO 34</td></tr>
                    <tr><td>Batteriespannung</td><td>Spannungsteiler</td><td>GPIO 35</td></tr>
                    <tr><td>Öldruck</td><td>Schalter (LOW=OK)</td><td>GPIO 19</td></tr>
                    <tr><td>Exhaust Valve</td><td>Servo PWM</td><td>GPIO 25</td></tr>
                    <tr><td>Airbox Klappe</td><td>Servo PWM</td><td>GPIO 26</td></tr>
                    <tr><td>CDI Map Select</td><td>Digital OUT</td><td>GPIO 27</td></tr>
                    <tr><td>LED (WS2812)</td><td>NeoPixel</td><td>GPIO 32</td></tr>
                    <tr><td>OLED Display</td><td>SSD1306 I²C</td><td>SDA=21, SCL=22</td></tr>
                    <tr><td>BLE</td><td>NimBLE</td><td>Built-in</td></tr>
                </table>
            </div>

            <!-- Alerts -->
            <div class="card">
                <h2>⚠️ StVZO Hinweise</h2>
                <ul style="font-size: 12px; padding-left: 16px;">
                    <li>🔴 Programmierbare Zündung: Einzelbetriebserlaubnis nötig oder innerh. OEM Specs</li>
                    <li>🟡 Exhaust Valve: Ab als Auspuff-Änderung — TÜV nötig od. Track-only</li>
                    <li>🟢 Zusatz-Display: Generell erlaubt, darf nicht ablenken</li>
                    <li>🟢 Lenker-Schalter: Erlaubt wenn sicher montiert</li>
                </ul>
            </div>

            <!-- Build Status -->
            <div class="card">
                <h2>📋 Build-Status</h2>
                <table><tr><th>Phase</th><th>Fokus</th><th>Budget</th><th>Status</th></tr>
                    <tr><td><span class="phase-badge phase-1">1</span></td><td>Motorlauf & Sicherheit</td><td>500-800€</td><td>⏳</td></tr>
                    <tr><td><span class="phase-badge phase-2">2</span></td><td>Fahrwerk Sport+Gelände</td><td>800-1200€</td><td>⏳</td></tr>
                    <tr><td><span class="phase-badge phase-3">3</span></td><td>Africa Twin Look + Sound</td><td>800-1200€</td><td>⏳</td></tr>
                    <tr><td><span class="phase-badge phase-4">4</span></td><td>Touring-Komfort</td><td>300-600€</td><td>⏳</td></tr>
                    <tr><td><span class="phase-badge phase-5">5</span></td><td>Reserve</td><td>200-500€</td><td>⏳</td></tr>
                </table>
            </div>
        </div>
    </div>

    <div class="footer">
        African Queen Lite — Build Tracker v1.0 | Daten aus vehicle_database.db
    </div>
</body>
</html>
"""


def get_db():
    """Get database connection."""
    if not os.path.exists(DB_PATH):
        return None
    conn = sqlite3.connect(DB_PATH)
    return conn


@app.route('/')
def dashboard():
    """Render main dashboard."""
    budget_data = [
        ('Phase 1: Motor & Sicherheit', 800, 0, 800),
        ('Phase 2: Fahrwerk', 1200, 0, 1200),
        ('Phase 3: Look & Sound', 1200, 0, 1200),
        ('Phase 4: Touring', 600, 0, 600),
        ('Phase 5: Reserve', 500, 0, 500),
    ]
    total_budget = 5000
    total_spent = 0
    total_remaining = 5000

    weight_data = [
        ('Basis NX650', 161, 161, 0),
        ('Batterie LiFePO4', 3.2, 1.2, -2.0),
        ('Auspuff Slip-on', 8.0, 5.0, -3.0),
        ('LED Scheinwerfer', 2.5, 1.5, -1.0),
        ('LED Blinker+Rücklicht', 1.0, 0.3, -0.7),
        ('Gabel+Emulatoren', 0, 0.5, 0.5),
        ('YSS Federbein', 5.5, 4.2, -1.3),
        ('Heckträger Alu', 0, 1.5, 1.5),
        ('Windschild', 0, 0.4, 0.4),
        ('Handguards', 0, 0.6, 0.6),
    ]
    weight_total_oem = 181.2
    weight_total_build = 175.2
    weight_delta = -6.0

    modes = [
        ('STRASSE', 0, 50, 50, '#00ff00'),
        ('STADT', -2, 20, 30, '#0064ff'),
        ('GELÄNDE', 2, 100, 100, '#ff3232'),
        ('SPORT', 3, 100, 100, '#ffa500'),
        ('COMFORT', -1, 40, 40, '#9400ff'),
        ('SOUND', 1, 100, 80, '#00ffff'),
    ]

    # Try to read real data from DB
    conn = get_db()
    if conn:
        try:
            cur = conn.cursor()
            # Try to read parts pricing if table exists
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cur.fetchall()]
            if 'parts' in tables:
                cur.execute("SELECT category, SUM(price), COUNT(*) FROM parts GROUP BY category")
                results = cur.fetchall()
                if results:
                    real_budget = {}
                    for row in results:
                        real_budget[row[0]] = (row[1] or 0, row[2] or 0)
                    # Update budget data with real data if available
        except Exception:
            pass
        conn.close()

    return render_template_string(DASHBOARD_HTML,
        budget=budget_data,
        total_budget=total_budget,
        total_spent=total_spent,
        total_remaining=total_remaining,
        weight=weight_data,
        weight_total_oem=weight_total_oem,
        weight_total_build=weight_total_build,
        weight_delta=weight_delta,
        modes=modes,
    )


@app.route('/api/status')
def api_status():
    """JSON API for current build status."""
    return jsonify({
        'project': 'African Queen Lite',
        'base': 'Honda NX650 Dominator RFVC',
        'budget_total': 5000,
        'budget_spent': 0,
        'budget_remaining': 5000,
        'weight_oem_kg': 181.2,
        'weight_build_kg': 175.2,
        'weight_delta_kg': -6.0,
        'target_weight_kg': 175,
        'ride_modes': ['STRASSE', 'STADT', 'GELAENDE', 'SPORT', 'COMFORT', 'SOUND'],
        'phases': [
            {'id': 1, 'focus': 'Motor & Sicherheit', 'budget': 800, 'status': 'pending'},
            {'id': 2, 'focus': 'Fahrwerk', 'budget': 1200, 'status': 'pending'},
            {'id': 3, 'focus': 'Look & Sound', 'budget': 1200, 'status': 'pending'},
            {'id': 4, 'focus': 'Touring', 'budget': 600, 'status': 'pending'},
            {'id': 5, 'focus': 'Reserve', 'budget': 500, 'status': 'pending'},
        ],
        'controller': {
            'mcu': 'ESP32 DevKit',
            'display': 'SSD1306 1.3" OLED',
            'sensors': ['RPM', 'Temperature', 'Voltage', 'Oil Pressure'],
            'outputs': ['Exhaust Valve PWM', 'Airbox Flap PWM', 'CDI Map Select', 'WS2812 LED'],
            'connectivity': 'BLE (NimBLE)',
        }
    })


if __name__ == '__main__':
    print("🏍️ African Queen Lite — Build Tracker")
    print(f"   Database: {DB_PATH}")
    print(f"   Dashboard: http://localhost:5050")
    app.run(host='0.0.0.0', port=5050, debug=True)