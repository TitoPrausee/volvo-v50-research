#!/usr/bin/env python3
"""
African Queen Lite — Build Tracker Web App v2.2
Reads from vehicle_database.db and serves a dashboard.
v2.2: Auto-RPM valve curves, fuel estimation per mode, gear detection,
      deep sleep, config mode, OTA updates
Run: python3 app.py
Open: http://localhost:5050
"""

import sqlite3
import os
from flask import Flask, render_template_string, jsonify

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'research', 'vehicle_database.db')

app = Flask(__name__)

# ============================================================
# Ride Mode Controller Configuration (matches ESP32 firmware v2.2)
# ============================================================
RIDE_MODES = {
    "STRASSE": {
        "color": "#00FF00", "ignition_offset": 0, "valve_percent": 50,
        "airbox_percent": 50, "idle_rpm": 1300, "rev_limit": 7000,
        "sweep_rate": 3, "throttle_curve": "LINEAR", "cdi_map": "A",
        "fuel_ml_per_100km": 3500, "reserve_liters": 3,
        "valve_curve": [(2000, 15), (3000, 35), (4500, 50), (6000, 65), (7000, 50)],
        "description": "Ausgewogen, gute Leistung, moderater Sound, verbrauchsoptimiert"
    },
    "STADT": {
        "color": "#0064FF", "ignition_offset": -2, "valve_percent": 20,
        "airbox_percent": 30, "idle_rpm": 1200, "rev_limit": 6500,
        "sweep_rate": 2, "throttle_curve": "SOFT", "cdi_map": "A",
        "fuel_ml_per_100km": 3000, "reserve_liters": 4,
        "valve_curve": [(1500, 10), (2500, 15), (4000, 20), (5500, 30), (6500, 20)],
        "description": "Sanfter Anfahrt, leise (Exhaust Valve geschlossen), spritsparend"
    },
    "GELÄNDE": {
        "color": "#FF3232", "ignition_offset": 2, "valve_percent": 100,
        "airbox_percent": 100, "idle_rpm": 1400, "rev_limit": 7500,
        "sweep_rate": 6, "throttle_curve": "AGGRESSIVE", "cdi_map": "B",
        "fuel_ml_per_100km": 4500, "reserve_liters": 2,
        "valve_curve": [(1500, 40), (2500, 80), (3500, 100), (5000, 100), (7000, 100)],
        "description": "Aggressiver Zündzeitpunkt, volle Leistung, Drehzahl-hoch-halten"
    },
    "SPORT": {
        "color": "#FFA500", "ignition_offset": 3, "valve_percent": 100,
        "airbox_percent": 100, "idle_rpm": 1350, "rev_limit": 7500,
        "sweep_rate": 8, "throttle_curve": "AGGRESSIVE", "cdi_map": "B",
        "fuel_ml_per_100km": 5000, "reserve_liters": 2,
        "valve_curve": [(1500, 30), (2500, 60), (3000, 90), (5000, 100), (7000, 100)],
        "description": "Volle Leistung, scharfer Zündzeitpunkt, sportlicher Sound"
    },
    "COMFORT": {
        "color": "#9400FF", "ignition_offset": -1, "valve_percent": 40,
        "airbox_percent": 40, "idle_rpm": 1250, "rev_limit": 6500,
        "sweep_rate": 2, "throttle_curve": "SOFT", "cdi_map": "A",
        "fuel_ml_per_100km": 3200, "reserve_liters": 4,
        "valve_curve": [(1500, 15), (2500, 30), (4000, 40), (5500, 40), (7000, 35)],
        "description": "Weicher Zündzeitpunkt, leise, sanfte Gasannahme, cruisen"
    },
    "SOUND": {
        "color": "#00FFFF", "ignition_offset": 1, "valve_percent": 100,
        "airbox_percent": 80, "idle_rpm": 1300, "rev_limit": 7000,
        "sweep_rate": 5, "throttle_curve": "PROGRESSIVE", "cdi_map": "C",
        "fuel_ml_per_100km": 4000, "reserve_liters": 3,
        "valve_curve": [(1200, 60), (2000, 85), (3000, 95), (4500, 100), (6500, 80)],
        "description": "Reiner Sound-Modus! Zündung für besten Sound optimiert (nicht Leistung)"
    }
}

# ============================================================
# NX650 Reference Data
# ============================================================
NX650_DATA = {
    "model": "Honda NX650 Dominator RFVC",
    "year": "1988-2003",
    "engine": "644cc RFVC single-cylinder, 4-stroke, air-cooled",
    "power": "45 PS (33 kW) @ 6000 RPM",
    "torque": "52 Nm @ 5500 RPM",
    "transmission": "5-speed",
    "gear_ratios": [2.846, 1.857, 1.389, 1.091, 0.913],
    "final_drive": 2.833,
    "primary_ratio": 2.176,
    "tire": "120/90-17 (circumference ~2.04m)",
    "tank": "16L (3.4L reserve)",
    "weight_dry": "161 kg (OEM)",
    "weight_target": "155 kg (target)",
    "budget_hard_cap": 5000,
    "stator_watts": 180,
    "battery_type": "LiFePO4 4S 12.8V"
}

# ============================================================
# HTML Dashboard Template
# ============================================================
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AQL v2.2 — Ride Mode Controller Dashboard</title>
<style>
  :root {
    --bg-dark: #0a0e17;
    --bg-card: #111827;
    --bg-card-hover: #1f2937;
    --text: #e5e7eb;
    --text-dim: #9ca3af;
    --accent: #22d3ee;
    --accent-dim: #0e7490;
    --danger: #ef4444;
    --warning: #f59e0b;
    --success: #22c55e;
    --border: #374151;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg-dark); color: var(--text); font-family: 'Inter', system-ui, sans-serif; }
  .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
  h1 { color: var(--accent); font-size: 1.8rem; margin-bottom: 0.5rem; }
  .subtitle { color: var(--text-dim); font-size: 0.9rem; margin-bottom: 2rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; margin-bottom: 24px; }
  .card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 16px; transition: border-color 0.2s; }
  .card:hover { border-color: var(--accent-dim); }
  .card-title { font-size: 0.75rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }
  .card-value { font-size: 1.5rem; font-weight: 600; }

  /* Mode Cards */
  .mode-card { position: relative; overflow: hidden; }
  .mode-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; }
  .mode-card[data-mode="STRASSE"]::before { background: #00FF00; }
  .mode-card[data-mode="STADT"]::before { background: #0064FF; }
  .mode-card[data-mode="GELÄNDE"]::before { background: #FF3232; }
  .mode-card[data-mode="SPORT"]::before { background: #FFA500; }
  .mode-card[data-mode="COMFORT"]::before { background: #9400FF; }
  .mode-card[data-mode="SOUND"]::before { background: #00FFFF; }

  .mode-name { font-size: 1.2rem; font-weight: 700; margin-bottom: 4px; }
  .mode-desc { font-size: 0.8rem; color: var(--text-dim); margin-bottom: 12px; }
  .mode-params { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; font-size: 0.78rem; }
  .mode-params span { padding: 2px 6px; background: rgba(255,255,255,0.05); border-radius: 4px; }
  .mode-params .label { color: var(--text-dim); }

  /* Valve Curve Chart */
  .curve-chart { width: 100%; height: 120px; position: relative; margin-top: 8px; }
  .curve-chart canvas { width: 100%; height: 100%; }

  /* Budget */
  .budget-bar { height: 24px; background: #1f2937; border-radius: 6px; overflow: hidden; margin-top: 8px; }
  .budget-fill { height: 100%; border-radius: 6px; transition: width 0.5s; }
  .budget-text { font-size: 0.85rem; margin-top: 4px; }

  /* Spec Table */
  .spec-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
  .spec-table th { text-align: left; color: var(--text-dim); padding: 6px 8px; border-bottom: 1px solid var(--border); }
  .spec-table td { padding: 6px 8px; border-bottom: 1px solid rgba(255,255,255,0.05); }
  .spec-table td:last-child { text-align: right; font-weight: 500; }

  /* New Features */
  .feature-badge { display: inline-block; background: var(--accent-dim); color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 600; margin-left: 6px; }
  .new-badge { background: #dc2626; }

  /* Hardware pins */
  .pin-table { width: 100%; font-size: 0.75rem; }
  .pin-table th { text-align: left; color: var(--text-dim); padding: 4px; }
  .pin-table td { padding: 4px; }
  .pin-input { color: #60a5fa; }
  .pin-output { color: #f97316; }
  .pin-i2c { color: #a78bfa; }
  .pin-adc { color: #34d399; }

  footer { text-align: center; color: var(--text-dim); font-size: 0.75rem; margin-top: 2rem; padding-bottom: 1rem; }
</style>
</head>
<body>
<div class="container">
  <h1>🏍️ African Queen Lite v2.2 <span class="feature-badge">ESP32</span><span class="feature-badge new-badge">NEW</span></h1>
  <p class="subtitle">Ride Mode Controller — Honda NX650 Dominator RFVC — Auto-RPM Valve + Fuel + Gear + Sleep</p>

  <!-- New Features Overview -->
  <div class="card" style="margin-bottom: 16px; border-color: var(--accent-dim);">
    <div class="card-title">🆕 Version 2.2 — New Features</div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 8px; margin-top: 8px;">
      <div style="background: rgba(34,211,238,0.1); padding: 10px; border-radius: 8px;">
        <strong style="color: #22d3ee;">Auto-RPM Valve</strong><br>
        <span style="font-size: 0.8rem;">Exhaust valve follows RPM curves per mode</span>
      </div>
      <div style="background: rgba(34,197,94,0.1); padding: 10px; border-radius: 8px;">
        <strong style="color: #22c55e;">Fuel Estimation</strong><br>
        <span style="font-size: 0.8rem;">mL/100km per mode + range + low fuel warning</span>
      </div>
      <div style="background: rgba(168,85,247,0.1); padding: 10px; border-radius: 8px;">
        <strong style="color: #a855f7;">Gear Detection</strong><br>
        <span style="font-size: 0.8rem;">RPM/speed correlation estimates current gear</span>
      </div>
      <div style="background: rgba(59,130,246,0.1); padding: 10px; border-radius: 8px;">
        <strong style="color: #3b82f6;">Deep Sleep</strong><br>
        <span style="font-size: 0.8rem;">80mA → 10µA after 5 min engine off</span>
      </div>
      <div style="background: rgba(245,158,11,0.1); padding: 10px; border-radius: 8px;">
        <strong style="color: #f59e0b;">Config Mode</strong><br>
        <span style="font-size: 0.8rem;">Long-press encoder for on-bike settings</span>
      </div>
    </div>
  </div>

  <!-- Ride Mode Cards -->
  <div class="grid" id="modes">
    {% for mode, params in ride_modes.items() %}
    <div class="card mode-card" data-mode="{{ mode }}">
      <div class="mode-name" style="color: {{ params.color }}">{{ mode }}</div>
      <div class="mode-desc">{{ params.description }}</div>
      <div class="mode-params">
        <span><span class="label">Ignition:</span> {{ params.ignition_offset }}°</span>
        <span><span class="label">CDI Map:</span> {{ params.cdi_map }}</span>
        <span><span class="label">Valve:</span> {{ params.valve_percent }}%</span>
        <span><span class="label">Airbox:</span> {{ params.airbox_percent }}%</span>
        <span><span class="label">Idle:</span> {{ params.idle_rpm }} RPM</span>
        <span><span class="label">Rev Lim:</span> {{ params.rev_limit }} RPM</span>
        <span><span class="label">Sweep:</span> {{ params.sweep_rate }}</span>
        <span><span class="label">Throttle:</span> {{ params.throttle_curve }}</span>
        <span><span class="label">Fuel:</span> {{ params.fuel_ml_per_100km // 10 }}L/100km</span>
        <span><span class="label">Reserve:</span> {{ params.reserve_liters }}L</span>
      </div>
      <div class="card-title" style="margin-top: 8px;">RPM Valve Curve</div>
      <canvas class="curve-chart" id="curve-{{ mode }}" data-points="{{ params.valve_curve | tojson }}"></canvas>
    </div>
    {% endfor %}
  </div>

  <!-- NX650 Specs -->
  <div class="card" style="margin-bottom: 16px;">
    <div class="card-title">📊 NX650 Dominator Reference</div>
    <table class="spec-table">
      <tr><th>Parameter</th><th>Value</th></tr>
      {% for k, v in nx_data.items() %}
      <tr><td>{{ k.replace('_', ' ').title() }}</td><td>{{ v }}</td></tr>
      {% endfor %}
    </table>
  </div>

  <!-- ESP32 Pin Mapping -->
  <div class="card" style="margin-bottom: 16px;">
    <div class="card-title">🔌 ESP32 Pin Mapping v2.2</div>
    <table class="pin-table">
      <tr><th>GPIO</th><th>Type</th><th>Function</th></tr>
      <tr><td>0</td><td style="color:#f97316">Encoder</td><td>ENCODER_BTN (BOOT)</td></tr>
      <tr><td>4</td><td style="color:#60a5fa">Input</td><td>Mode+ Button</td></tr>
      <tr><td>5</td><td style="color:#60a5fa">Input</td><td>Mode- Button</td></tr>
      <tr><td>16</td><td style="color:#60a5fa">Input</td><td>Encoder A (CLK)</td></tr>
      <tr><td>17</td><td style="color:#60a5fa">Input</td><td>Encoder B (DT)</td></tr>
      <tr><td>18</td><td style="color:#60a5fa">Input</td><td>Ignition Pulse (interrupt)</td></tr>
      <tr><td>19</td><td style="color:#60a5fa">Input</td><td>Oil Pressure Switch</td></tr>
      <tr><td>21</td><td style="color:#a78bfa">I2C</td><td>OLED SDA</td></tr>
      <tr><td>22</td><td style="color:#a78bfa">I2C</td><td>OLED SCL</td></tr>
      <tr><td>25</td><td style="color:#f97316">PWM</td><td>Exhaust Valve Servo</td></tr>
      <tr><td>26</td><td style="color:#f97316">PWM</td><td>Airbox Flap Servo</td></tr>
      <tr><td>27</td><td style="color:#f97316">Output</td><td>CDI Map A Select</td></tr>
      <tr><td>32</td><td style="color:#f97316">Output</td><td>WS2812 LED Data</td></tr>
      <tr><td>33</td><td style="color:#f97316">Output</td><td>CDI Map B Select</td></tr>
      <tr><td>34</td><td style="color:#34d399">ADC</td><td>Thermistor (cylinder head)</td></tr>
      <tr><td>35</td><td style="color:#34d399">ADC</td><td>Battery Voltage Divider</td></tr>
      <tr><td>36</td><td style="color:#34d399">ADC</td><td>Stator Voltage Divider</td></tr>
    </table>
    <div style="font-size: 0.7rem; color: var(--text-dim); margin-top: 8px;">
      v2.2 Production: GPIO14/13 → DRV8833 AIN1/AIN2 (Exhaust), GPIO23/2 → DRV8833 BIN1/BIN2 (Airbox), AS5600 @ 0x36/0x37
    </div>
  </div>

  <!-- Budget Section (when DB exists) -->
  {% if budget_data %}
  <div class="card" style="margin-bottom: 16px;">
    <div class="card-title">💰 Budget Status</div>
    <div class="budget-bar">
      <div class="budget-fill" style="width: {{ budget_pct }}%; background: {% if budget_pct > 90 %}var(--danger){% elif budget_pct > 75 %}var(--warning){% else %}var(--success){% endif %};"></div>
    </div>
    <div class="budget-text">
      €{{ budget_spent }} / €{{ budget_max }} ({{ budget_pct }}%)
      {% if budget_remaining > 0 %}— €{{ budget_remaining }} remaining{% endif %}
    </div>
  </div>
  {% endif %}

  <!-- Valve Curve Comparison Chart -->
  <div class="card" style="margin-bottom: 16px;">
    <div class="card-title">📈 Valve Position Comparison (All Modes)</div>
    <div id="comparison-chart">
      <canvas id="comparison-canvas"></canvas>
    </div>
  </div>

  <!-- Fuel Estimation & Gear Detection -->
  <div class="card" style="margin-bottom: 16px;">
    <div class="card-title">⛽ Fuel Estimation by Mode</div>
    <table class="spec-table">
      <tr><th>Mode</th><th>Consumption</th><th>Range (16L)</th><th>Reserve Warn</th></tr>
      {% for mode, params in ride_modes.items() %}
      <tr>
        <td style="color: {{ params.color }}">{{ mode }}</td>
        <td>{{ params.fuel_ml_per_100km // 10 }}L/100km</td>
        <td>{{ (16000 / params.fuel_ml_per_100km * 100) | round(0) | int }}km</td>
        <td>{{ params.reserve_liters }}L</td>
      </tr>
      {% endfor %}
    </table>
    <div style="font-size: 0.75rem; color: var(--text-dim); margin-top: 8px;">
      NX650 tank: 16L total, 3.4L reserve. Range estimated at mode-specific consumption rates.
    </div>
  </div>

  <!-- Gear Estimation Reference -->
  <div class="card" style="margin-bottom: 16px;">
    <div class="card-title">⚙️ Gear Ratios — NX650</div>
    <table class="spec-table">
      <tr><th>Gear</th><th>Ratio</th><th>Speed @ 5000 RPM</th><th>Speed @ 7000 RPM</th></tr>
      {% for ratio in nx_data.gear_ratios %}
      <tr>
        <td>{{ loop.index }}</td>
        <td>{{ ratio }}</td>
        <td>{{ ((5000 * 2.04) / (2.176 * ratio * 2.833 * 60) * 3.6) | round(1) }} km/h</td>
        <td>{{ ((7000 * 2.04) / (2.176 * ratio * 2.833 * 60) * 3.6) | round(1) }} km/h</td>
      </tr>
      {% endfor %}
    </table>
    <div style="font-size: 0.75rem; color: var(--text-dim); margin-top: 8px;">
      tire_circ=2.04m, primary_ratio={{ nx_data.primary_ratio }}, final_ratio={{ nx_data.final_drive }}
    </div>
  </div>

  <!-- OTA Update Section -->
  <div class="card" style="margin-bottom: 16px; border-color: #f59e0b;">
    <div class="card-title">📡 OTA Firmware Update</div>
    <div style="font-size: 0.85rem;">
      <p><strong>How to update firmware wirelessly:</strong></p>
      <ol style="margin-left: 1.2rem; color: var(--text-dim);">
        <li>Power off the ESP32 controller</li>
        <li>Hold the encoder button and power on</li>
        <li>Connect to WiFi <code style="color: #22d3ee;">AQL-OTA</code> (password: <code style="color: #22d3ee;">aql2026</code>)</li>
        <li>Open <code style="color: #22d3ee;">http://192.168.4.1</code> in browser</li>
        <li>Upload the <code>.bin</code> firmware file</li>
        <li>ESP32 reboots automatically with new firmware</li>
      </ol>
      <p style="font-size: 0.75rem; color: var(--warning);">⚠️ OTA mode only activates when encoder is held during boot. Cannot be triggered while riding.</p>
    </div>
  </div>

  <footer>
    African Queen Lite v2.2 — ESP32 Ride-Mode Controller — Honda NX650 Dominator RFVC<br>
    Auto-RPM Valve • Fuel Estimation • Gear Detection • Deep Sleep • Config Mode • OTA Update<br>
    <span style="font-size: 0.7rem; color: var(--text-dim);">Last updated: 2026-05-28</span>
  </footer>
</div>

<script>
// Draw valve curve charts
document.addEventListener('DOMContentLoaded', function() {
  const canvases = document.querySelectorAll('.curve-chart');
  canvases.forEach(canvas => {
    const points = JSON.parse(canvas.dataset.points);
    const modeColor = canvas.closest('.mode-card')?.dataset.mode;
    drawCurve(canvas, points, modeColor);
  });
  drawComparisonChart();
});

const MODE_COLORS_MAP = {
  'STRASSE': '#00FF00', 'STADT': '#0064FF', 'GELÄNDE': '#FF3232',
  'SPORT': '#FFA500', 'COMFORT': '#9400FF', 'SOUND': '#00FFFF'
};

function drawCurve(canvas, points, modeName) {
  const ctx = canvas.getContext('2d');
  const w = canvas.width = canvas.offsetWidth * 2;
  const h = canvas.height = canvas.offsetHeight * 2;
  ctx.scale(2, 2);
  const cw = canvas.offsetWidth;
  const ch = canvas.offsetHeight;

  // Background
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(0, 0, cw, ch);

  // Grid
  ctx.strokeStyle = '#1e293b';
  ctx.lineWidth = 0.5;
  for (let i = 0; i <= 4; i++) {
    const y = ch * i / 4;
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(cw, y); ctx.stroke();
  }
  for (let i = 0; i <= 5; i++) {
    const x = cw * i / 5;
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, ch); ctx.stroke();
  }

  // Labels
  ctx.fillStyle = '#64748b';
  ctx.font = '9px monospace';
  ctx.fillText('100%', 2, 12);
  ctx.fillText('0%', 2, ch - 4);
  ctx.fillText(points[0][0] + 'RPM', 4, ch - 12);
  ctx.fillText(points[points.length-1][0] + 'RPM', cw - 40, ch - 12);

  const color = MODE_COLORS_MAP[modeName] || '#22d3ee';
  // Curve
  const rpmMin = points[0][0];
  const rpmMax = points[points.length - 1][0];
  const rpmRange = rpmMax - rpmMin;

  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.beginPath();
  points.forEach((p, i) => {
    const x = ((p[0] - rpmMin) / rpmRange) * cw;
    const y = ch - (p[1] / 100) * (ch - 10) - 5;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();

  // Fill under curve
  ctx.lineTo(cw, ch);
  ctx.lineTo(0, ch);
  ctx.closePath();
  // Parse hex color to rgba with 10% opacity
  const r = parseInt(color.slice(1,3), 16);
  const g = parseInt(color.slice(3,5), 16);
  const b = parseInt(color.slice(5,7), 16);
  ctx.fillStyle = `rgba(${r},${g},${b},0.15)`;
  ctx.fill();

  // Points
  points.forEach(p => {
    const x = ((p[0] - rpmMin) / rpmRange) * cw;
    const y = ch - (p[1] / 100) * (ch - 10) - 5;
    ctx.beginPath();
    ctx.arc(x, y, 3, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.fill();
  });
}

// Draw combined comparison chart of all valve curves
function drawComparisonChart() {
  const container = document.getElementById('comparison-chart');
  if (!container) return;
  const canvas = document.getElementById('comparison-canvas');
  if (!canvas) return;

  const canvases = document.querySelectorAll('.curve-chart');
  if (canvases.length === 0) return;

  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const cw = container.offsetWidth;
  const ch = 200;
  canvas.width = cw * dpr;
  canvas.height = ch * dpr;
  canvas.style.width = cw + 'px';
  canvas.style.height = ch + 'px';
  ctx.scale(dpr, dpr);

  // Background
  ctx.fillStyle = '#111827';
  ctx.fillRect(0, 0, cw, ch);

  // Axis labels
  ctx.fillStyle = '#64748b';
  ctx.font = '10px monospace';
  ctx.fillText('Valve Position Comparison', 10, 15);
  ctx.fillText('100%', 2, 30);
  ctx.fillText('0%', 2, ch - 10);
  ctx.fillText('RPM →', cw - 40, ch - 10);

  // Grid
  ctx.strokeStyle = '#1e293b';
  ctx.lineWidth = 0.5;
  for (let i = 0; i <= 4; i++) {
    const y = 20 + (ch - 40) * i / 4;
    ctx.beginPath(); ctx.moveTo(30, y); ctx.lineTo(cw - 10, y); ctx.stroke();
  }

  // Draw each mode's curve
  const modes = ['STRASSE', 'STADT', 'GELÄNDE', 'SPORT', 'COMFORT', 'SOUND'];
  canvases.forEach((c, idx) => {
    const points = JSON.parse(c.dataset.points);
    const modeName = modes[idx] || '';
    const color = MODE_COLORS_MAP[modeName] || '#22d3ee';
    const rpmMin = 1000;
    const rpmMax = 7500;
    const plotW = cw - 40;
    const plotH = ch - 50;
    const plotY = 20;

    ctx.strokeStyle = color;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    points.forEach((p, i) => {
      const x = 30 + ((p[0] - rpmMin) / (rpmMax - rpmMin)) * plotW;
      const y = plotY + plotH - (p[1] / 100) * plotH;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // Legend
    ctx.fillStyle = color;
    ctx.font = '9px monospace';
    ctx.fillText(modeName, cw - 70, 25 + idx * 12);
  });
}
</script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    budget_data = None
    budget_spent = 0
    budget_max = NX650_DATA['budget_hard_cap']
    budget_remaining = budget_max
    budget_pct = 0

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        # Try to get budget data from DB
        try:
            cursor = conn.execute("""
                SELECT SUM(price_avg) as total
                FROM parts p
                JOIN part_fitment pf ON pf.part_id = p.id
                WHERE pf.variant_id = 5
            """)
            row = cursor.fetchone()
            if row and row['total']:
                budget_data = True
                budget_spent = round(row['total'], 2)
                budget_remaining = round(budget_max - budget_spent, 2)
                budget_pct = round((budget_spent / budget_max) * 100, 1)
        except:
            pass
        conn.close()
    except:
        pass

    return render_template_string(
        DASHBOARD_HTML,
        ride_modes=RIDE_MODES,
        nx_data=NX650_DATA,
        budget_data=budget_data,
        budget_spent=budget_spent,
        budget_max=budget_max,
        budget_remaining=budget_remaining,
        budget_pct=budget_pct
    )

@app.route('/api/modes')
def api_modes():
    return jsonify(RIDE_MODES)

@app.route('/api/nx650')
def api_nx650():
    return jsonify(NX650_DATA)

@app.route('/api/valve-curves')
def api_valve_curves():
    curves = {}
    for mode, params in RIDE_MODES.items():
        curves[mode] = {
            "color": params["color"],
            "valve_curve": params["valve_curve"],
            "description": params["description"]
        }
    return jsonify(curves)

if __name__ == '__main__':
    print("🏍️  African Queen Lite v2.2 — Build Tracker Dashboard")
    print(f"   Database: {DB_PATH}")
    print(f"   URL: http://localhost:5050")
    app.run(host='0.0.0.0', port=5050, debug=True)