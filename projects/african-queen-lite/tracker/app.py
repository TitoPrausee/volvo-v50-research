#!/usr/bin/env python3
"""
African Queen Lite — Build Tracker Web App v2.0
Reads from vehicle_database.db and serves a dashboard.
v2.0: Added ride-mode controller section with mode parameters,
      longevity monitoring, and hardware status.
Run: python3 app.py
Open: http://localhost:5050
"""

import sqlite3
import os
from flask import Flask, render_template_string, jsonify

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'research', 'vehicle_database.db')

app = Flask(__name__)

# ============================================================
# Ride Mode Controller Configuration (matches ESP32 firmware)
# ============================================================
RIDE_MODES = {
    "STRASSE": {
        "color": "#00FF00", "ignition_offset": 0, "valve_percent": 50,
        "airbox_percent": 50, "idle_rpm": 1300, "rev_limit": 7000,
        "sweep_rate": 3, "throttle_curve": "LINEAR",
        "description": "Ausgewogen, gute Leistung, moderater Sound, verbrauchsoptimiert"
    },
    "STADT": {
        "color": "#0064FF", "ignition_offset": -2, "valve_percent": 20,
        "airbox_percent": 30, "idle_rpm": 1200, "rev_limit": 6500,
        "sweep_rate": 2, "throttle_curve": "SOFT",
        "description": "Sanfter Anfahrt, leise (Exhaust Valve geschlossen), spritsparend"
    },
    "GELÄNDE": {
        "color": "#FF3232", "ignition_offset": 2, "valve_percent": 100,
        "airbox_percent": 100, "idle_rpm": 1400, "rev_limit": 7500,
        "sweep_rate": 6, "throttle_curve": "AGGRESSIVE",
        "description": "Aggressiver Zündzeitpunkt, volle Leistung, Drehzahl-hoch-halten"
    },
    "SPORT": {
        "color": "#FFA500", "ignition_offset": 3, "valve_percent": 100,
        "airbox_percent": 100, "idle_rpm": 1350, "rev_limit": 7500,
        "sweep_rate": 8, "throttle_curve": "AGGRESSIVE",
        "description": "Volle Leistung, scharfer Zündzeitpunkt, sportlicher Sound"
    },
    "COMFORT": {
        "color": "#9400FF", "ignition_offset": -1, "valve_percent": 40,
        "airbox_percent": 40, "idle_rpm": 1250, "rev_limit": 6500,
        "sweep_rate": 2, "throttle_curve": "SOFT",
        "description": "Weicher Zündzeitpunkt, leise, sanfte Gasannahme, cruisen"
    },
    "SOUND": {
        "color": "#00FFFF", "ignition_offset": 1, "valve_percent": 100,
        "airbox_percent": 80, "idle_rpm": 1300, "rev_limit": 7000,
        "sweep_rate": 5, "throttle_curve": "PROGRESSIVE",
        "description": "Reiner Sound-Modus! Zündung für besten Sound optimiert"
    },
}

# Longevity monitoring thresholds
HEALTH_THRESHOLDS = {
    "temp_warning": 115, "temp_critical": 125,
    "voltage_low": 11.5, "voltage_high": 15.5,
    "stator_healthy": 13.0, "stator_warn": 12.5,
    "rpm_redline": 7500,
}

MAINT_INTERVALS = {
    "Oil Change": 6000, "Valve Adjust": 12000,
    "Air Filter": 12000, "Spark Plug": 12000,
    "Drive Chain": 15000, "Tire Check": 1000,
}

# ============================================================
# HTML Template — Dark Theme Dashboard v2.0
# ============================================================
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏍️ African Queen Lite — Build Tracker v2.0</title>
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
        .mode-card {
            background: #111; border: 1px solid #333; border-radius: 6px; padding: 10px;
            text-align: center; font-size: 11px;
        }
        .mode-card .mode-name { font-size: 14px; font-weight: bold; margin-bottom: 4px; }
        .mode-card .mode-param { color: #888; font-size: 10px; }
        .mode-card .mode-desc { color: #666; font-size: 9px; margin-top: 4px; }
        .health-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
        .health-item { background: #111; padding: 8px; border-radius: 4px; font-size: 11px; }
        .health-item .label { color: #888; }
        .health-item .value { font-size: 18px; font-weight: bold; }
        .health-ok { color: #4ecdc4; }
        .health-warn { color: #ffcc44; }
        .health-crit { color: #ff4444; }
        .section-divider { border: 0; border-top: 1px solid #2d2d2d; margin: 20px 0; }
        .tag { display: inline-block; padding: 2px 6px; border-radius: 3px; font-size: 10px; }
        .tag-esp32 { background: #1a3a1a; color: #4ecdc4; }
        .tag-nx650 { background: #3a1a1a; color: #ff6b35; }
        .tag-v2 { background: #3a3a1a; color: #ffcc44; }
        .wide-card { grid-column: 1 / -1; }
        .mode-color-dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; vertical-align: middle; margin-right: 4px; }
        .maint-row { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #1a1a1a; }
        .maint-name { color: #ccc; }
        .maint-bar { width: 60%; height: 8px; background: #333; border-radius: 4px; display: inline-block; margin: 0 8px; }
        .maint-bar-fill { height: 100%; border-radius: 4px; background: #4ecdc4; }
        .maint-bar-fill.overdue { background: #ff4444; }
    </style>
</head>
<body>
<div class="header">
    <h1>🏍️ African Queen Lite — Build Tracker</h1>
    <p>Honda NX650 Dominator RFVC · <span class="tag tag-v2">v2.0 LONGEVITY</span> · Budget: 5.000€ HARD CAP</p>
</div>

<div class="container">
    <div class="grid">
        <!-- Budget Card -->
        <div class="card">
            <h2>💰 Budget</h2>
            <div id="budget-content">Loading...</div>
        </div>

        <!-- Weight Card -->
        <div class="card">
            <h2>⚖️ Gewicht</h2>
            <div id="weight-content">Loading...</div>
        </div>

        <!-- Ride Mode Controller -->
        <div class="card wide-card">
            <h2>🎮 Ride Mode Controller <span class="tag tag-esp32">ESP32</span> <span class="tag tag-v2">v2.0</span></h2>
            <div class="mode-grid">
                {% for mode, params in modes.items() %}
                <div class="mode-card">
                    <div class="mode-name">
                        <span class="mode-color-dot" style="background:{{params.color}}"></span>
                        {{mode}}
                    </div>
                    <div class="mode-param">IGN: {{'+' if params.ignition_offset >= 0 else ''}}{{params.ignition_offset}}° · V:{{params.valve_percent}}% · A:{{params.airbox_percent}}%</div>
                    <div class="mode-param">Idle:{{params.idle_rpm}} · Rev:{{params.rev_limit}} · Sweep:{{params.sweep_rate}}</div>
                    <div class="mode-param">Throttle: {{params.throttle_curve}}</div>
                    <div class="mode-desc">{{params.description}}</div>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- Longevity Monitoring -->
        <div class="card">
            <h2>🛡️ Langlebigkeit <span class="tag tag-v2">LONGEVITY</span></h2>
            <div class="health-grid">
                <div class="health-item">
                    <span class="label">Zylinderkopf</span><br>
                    <span class="value health-ok">{{thresholds.temp_warning}}°C</span>
                    <span class="label">Warn /</span>
                    <span class="value health-crit">{{thresholds.temp_critical}}°C</span>
                    <span class="label">Kritisch</span>
                </div>
                <div class="health-item">
                    <span class="label">Stator</span><br>
                    <span class="value health-ok">{{thresholds.stator_healthy}}V+</span>
                    <span class="label">Health /</span>
                    <span class="value health-warn">{{thresholds.stator_warn}}V</span>
                    <span class="label">Warn</span>
                </div>
                <div class="health-item">
                    <span class="label">Batterie (LiFePO4)</span><br>
                    <span class="label">14.6V Voll · 13.2V Nominal · 10.0V Leer</span>
                </div>
                <div class="health-item">
                    <span class="label">Öldruckschalter</span><br>
                    <span class="value health-ok">LOW = OK</span>
                    <span class="label">/</span>
                    <span class="value health-crit">HIGH = WARN</span>
                </div>
            </div>
        </div>

        <!-- Maintenance Intervals -->
        <div class="card">
            <h2>🔧 Wartungsintervalle NX650</h2>
            {% for name, interval in maint.items() %}
            <div class="maint-row">
                <span class="maint-name">{{name}}</span>
                <span>{{interval}} km</span>
            </div>
            {% endfor %}
        </div>

        <!-- Hardware -->
        <div class="card">
            <h2>🔌 Hardware <span class="tag tag-esp32">ESP32</span></h2>
            <table>
                <tr><th>Komponente</th><th>Typ</th><th>Preis</th></tr>
                <tr><td>MCU</td><td>ESP32 DevKit V1</td><td>€5</td></tr>
                <tr><td>Display</td><td>SSD1306 OLED 128x64</td><td>€2</td></tr>
                <tr><td>LED</td><td>WS2812 RGB</td><td>€1</td></tr>
                <tr><td>Encoder</td><td>KY-040 Rotary</td><td>€2</td></tr>
                <tr><td>Exhaust Servo</td><td>Gearmotor + DRV8833</td><td>€28</td></tr>
                <tr><td>Airbox Servo</td><td>Gearmotor + DRV8833</td><td>€28</td></tr>
                <tr><td>CDI</td><td>Ignitech DC-CDI-P2</td><td>€120</td></tr>
                <tr><td>Sensoren</td><td>NTC+Spannungsteiler+Öldruck</td><td>€10</td></tr>
                <tr><td>Gehäuse</td><td>3D-Druck PETG</td><td>€5</td></tr>
                <tr><td>Kabel/Stecker</td><td>Deutsch DT + Silikonkabel</td><td>€15</td></tr>
                <tr style="border-top: 2px solid #ff6b35"><th colspan="2"><strong>Controller Gesamt</strong></th><td><strong>~€216</strong></td></tr>
            </table>
        </div>

        <!-- StVZO -->
        <div class="card">
            <h2>📋 StVZO Status</h2>
            <table>
                <tr><th>Komponente</th><th>Status</th></tr>
                <tr><td>Custom Display</td><td style="color:#4ecdc4">✅ Erlaubt</td></tr>
                <tr><td>Exhaust Valve</td><td style="color:#ffcc44">⚠️ TÜV nötig</td></tr>
                <tr><td>Programmierbare CDI</td><td style="color:#ffcc44">⚠️ Ignitech hat EC-Zulassung</td></tr>
                <tr><td>BLE Logging</td><td style="color:#4ecdc4">✅ Erlaubt</td></tr>
                <tr><td>Lenker-Schalter</td><td style="color:#4ecdc4">✅ Wenn §30-konform</td></tr>
                <tr><td>LED-Indikator</td><td style="color:#4ecdc4">✅ Im Gehäuse</td></tr>
            </table>
        </div>
    </div>
</div>
</body>
</html>
"""

# ============================================================
# Routes
# ============================================================
@app.route('/')
def dashboard():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Budget data
        cur.execute("SELECT category, SUM(cost_actual) as spent, SUM(cost_budget) as budget FROM builds GROUP BY category")
        budget_rows = cur.fetchall()

        # Weight data
        cur.execute("SELECT category, SUM(weight_delta) as delta FROM builds GROUP BY category")
        weight_rows = cur.fetchall()

        conn.close()
    except Exception as e:
        budget_rows = []
        weight_rows = []

    # Render template with ride modes and thresholds
    from flask import render_template_string
    return render_template_string(DASHBOARD_HTML,
        modes=RIDE_MODES,
        thresholds=HEALTH_THRESHOLDS,
        maint=MAINT_INTERVALS)

@app.route('/api/modes')
def api_modes():
    return jsonify(RIDE_MODES)

@app.route('/api/health')
def api_health():
    return jsonify(HEALTH_THRESHOLDS)

@app.route('/api/maintenance')
def api_maintenance():
    return jsonify(MAINT_INTERVALS)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)