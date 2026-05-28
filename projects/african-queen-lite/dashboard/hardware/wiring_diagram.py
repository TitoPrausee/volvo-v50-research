#!/usr/bin/env python3
"""
African Queen Lite — Wiring Diagram Generator v2.2
Generates SVG and ASCII wiring diagrams for the ESP32 Ride-Mode Controller.
Honda NX650 Dominator RFVC

v2.2: Added Auto-RPM valve, fuel estimation (software only),
      gear detection (software only), deep sleep wiring, config mode.

Output:
  - wiring_diagram.svg (dark-themed, color-coded)
  - wiring_diagram.txt (ASCII diagram)

Run: python3 wiring_diagram.py
"""

import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# Pin Definitions (matches modes.h v2.2)
# ============================================================
PINS = {
    # Inputs
    "MODE_UP":         {"gpio": 4,  "type": "input",  "wire": "blue",   "desc": "Handlebar Mode+ Button"},
    "MODE_DOWN":       {"gpio": 5,  "type": "input",  "wire": "blue",   "desc": "Handlebar Mode- Button"},
    "ENCODER_A":       {"gpio": 16, "type": "input",  "wire": "blue",   "desc": "Rotary Encoder CLK"},
    "ENCODER_B":       {"gpio": 17, "type": "input",  "wire": "blue",   "desc": "Rotary Encoder DT"},
    "ENCODER_BTN":     {"gpio": 0,  "type": "input",  "wire": "blue",   "desc": "Encoder Push Button (BOOT)"},
    "IGNITION_PULSE":  {"gpio": 18, "type": "input",  "wire": "orange", "desc": "Pulse Generator Coil"},
    "OIL_PRESSURE":    {"gpio": 19, "type": "input",  "wire": "blue",   "desc": "Oil Pressure Switch"},
    "THERMISTOR":      {"gpio": 34, "type": "adc",    "wire": "green",  "desc": "Cylinder Head NTC 10kΩ"},
    "VOLTAGE_DIVIDER": {"gpio": 35, "type": "adc",    "wire": "red",    "desc": "Battery Voltage (R1=100k R2=33k)"},
    "STATOR_SENSE":    {"gpio": 36, "type": "adc",    "wire": "red",    "desc": "Stator Output Voltage Divider"},
    # Outputs
    "EXHAUST_VALVE":   {"gpio": 25, "type": "pwm",    "wire": "orange", "desc": "Exhaust Valve Servo PWM"},
    "AIRBOX_FLAP":     {"gpio": 26, "type": "pwm",    "wire": "orange", "desc": "Airbox Flap Servo PWM"},
    "CDI_MAP_A":       {"gpio": 27, "type": "output", "wire": "blue",   "desc": "CDI Map A Select (active LOW)"},
    "LED_DATA":        {"gpio": 32, "type": "output", "wire": "orange", "desc": "WS2812 RGB LED Data"},
    "CDI_MAP_B":       {"gpio": 33, "type": "output", "wire": "blue",   "desc": "CDI Map B Select (active LOW)"},
    # I2C
    "OLED_SDA":        {"gpio": 21, "type": "i2c",    "wire": "blue",   "desc": "OLED + AS5600 I2C SDA"},
    "OLED_SCL":        {"gpio": 22, "type": "i2c",    "wire": "blue",   "desc": "OLED + AS5600 I2C SCL"},
}

# DRV8833 production motor driver pins (USE_PRODUCTION_MOTOR=1)
DRV8833_PINS = {
    "EXHAUST_IN1": {"gpio": 14, "type": "output", "wire": "orange", "desc": "DRV8833 AIN1 (Exhaust)"},
    "EXHAUST_IN2": {"gpio": 13, "type": "output", "wire": "orange", "desc": "DRV8833 AIN2 (Exhaust)"},
    "AIRBOX_IN1":  {"gpio": 23, "type": "output", "wire": "orange", "desc": "DRV8833 BIN1 (Airbox)"},
    "AIRBOX_IN2":  {"gpio": 2,  "type": "output", "wire": "orange", "desc": "DRV8833 BIN2 (Airbox)"},
    "AS5600_EXH":  {"addr": "0x36", "type": "i2c", "desc": "AS5600 Exhaust Valve Encoder"},
    "AS5600_AIR":  {"addr": "0x37", "type": "i2c", "desc": "AS5600 Airbox Encoder"},
}

# Deep sleep wake sources
SLEEP_WAKE_PINS = {
    "WAKE_MODE_UP":    {"gpio": 4,  "type": "wake", "desc": "Deep sleep wake: Mode+ button (EXT0)"},
    "WAKE_IGNITION":   {"gpio": 18, "type": "wake", "desc": "Deep sleep wake: Ignition pulse (EXT1)"},
}

WIRE_COLORS = {
    "red":    "#FF3333",   # Power
    "blue":   "#3399FF",   # Signal
    "green":  "#33CC33",   # Ground / Sensor analog
    "orange": "#FF9933",   # PWM / Digital output
}

SVG_CATEGORIES = {
    "INPUTS":  ["MODE_UP", "MODE_DOWN", "ENCODER_A", "ENCODER_B", "ENCODER_BTN",
                 "IGNITION_PULSE", "OIL_PRESSURE", "THERMISTOR", "VOLTAGE_DIVIDER", "STATOR_SENSE"],
    "OUTPUTS": ["EXHAUST_VALVE", "AIRBOX_FLAP", "CDI_MAP_A", "CDI_MAP_B", "LED_DATA"],
    "I2C":     ["OLED_SDA", "OLED_SCL"],
}


def generate_svg():
    """Generate dark-themed SVG wiring diagram."""

    width = 900
    height = 1450

    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" style="background:#0a0e17">')

    # Title
    svg_parts.append(f'<text x="{width//2}" y="30" fill="#22d3ee" font-family="monospace" font-size="18" text-anchor="middle">African Queen Lite — ESP32 Wiring v2.2</text>')
    svg_parts.append(f'<text x="{width//2}" y="50" fill="#9ca3af" font-family="monospace" font-size="11" text-anchor="middle">Honda NX650 Dominator RFVC • Auto-RPM Valve + Fuel + Gear + Sleep</text>')

    # ESP32 chip (center)
    chip_x = width // 2 - 60
    chip_y = 180
    chip_w = 120
    chip_h = 360

    svg_parts.append(f'<rect x="{chip_x}" y="{chip_y}" width="{chip_w}" height="{chip_h}" rx="8" fill="#1e293b" stroke="#22d3ee" stroke-width="2"/>')
    svg_parts.append(f'<text x="{chip_x + chip_w//2}" y="{chip_y + 25}" fill="#22d3ee" font-family="monospace" font-size="12" text-anchor="middle">ESP32</text>')
    svg_parts.append(f'<text x="{chip_x + chip_w//2}" y="{chip_y + 40}" fill="#64748b" font-family="monospace" font-size="9" text-anchor="middle">v2.2</text>')

    # Deep sleep indicator
    svg_parts.append(f'<text x="{chip_x + chip_w//2}" y="{chip_y + chip_h - 10}" fill="#f59e0b" font-family="monospace" font-size="8" text-anchor="middle">DEEP SLEEP 10µA</text>')

    # Input pins (left side)
    inputs = list(SVG_CATEGORIES["INPUTS"])
    y_start = chip_y + 10
    y_step = 30
    for i, pin_name in enumerate(inputs):
        pin = PINS[pin_name]
        y = y_start + i * y_step
        color = WIRE_COLORS.get(pin["wire"], "#fff")
        # Pin dot on left of ESP32
        svg_parts.append(f'<circle cx="{chip_x}" cy="{y + 8}" r="4" fill="{color}"/>')
        # Pin label on chip
        svg_parts.append(f'<text x="{chip_x + 10}" y="{y + 12}" fill="#e5e7eb" font-family="monospace" font-size="8" text-anchor="start">GPIO{pin["gpio"]:2d}</text>')
        # Wire to left label
        label_x = 40
        svg_parts.append(f'<line x1="{label_x + 140}" y1="{y + 8}" x2="{chip_x}" y2="{y + 8}" stroke="{color}" stroke-width="1.5"/>')
        svg_parts.append(f'<text x="{label_x}" y="{y + 12}" fill="{color}" font-family="monospace" font-size="8" text-anchor="end">{pin_name}</text>')

    # Output pins (right side)
    outputs = list(SVG_CATEGORIES["OUTPUTS"])
    for i, pin_name in enumerate(outputs):
        pin = PINS[pin_name]
        y = y_start + i * y_step
        color = WIRE_COLORS.get(pin["wire"], "#fff")
        # Pin dot on right of ESP32
        svg_parts.append(f'<circle cx="{chip_x + chip_w}" cy="{y + 8}" r="4" fill="{color}"/>')
        # Pin label on chip
        svg_parts.append(f'<text x="{chip_x + chip_w - 10}" y="{y + 12}" fill="#e5e7eb" font-family="monospace" font-size="8" text-anchor="end">GPIO{pin["gpio"]:2d}</text>')
        # Wire to right label
        label_x = width - 40
        svg_parts.append(f'<line x1="{chip_x + chip_w}" y1="{y + 8}" x2="{label_x - 140}" y2="{y + 8}" stroke="{color}" stroke-width="1.5"/>')
        svg_parts.append(f'<text x="{label_x}" y="{y + 12}" fill="{color}" font-family="monospace" font-size="8" text-anchor="start">{pin_name}</text>')

    # I2C pins (bottom)
    i2c_pins = SVG_CATEGORIES["I2C"]
    i2c_y = chip_y + chip_h + 20
    for i, pin_name in enumerate(i2c_pins):
        pin = PINS[pin_name]
        x = chip_x + 20 + i * 50
        color = WIRE_COLORS.get(pin["wire"], "#fff")
        svg_parts.append(f'<circle cx="{x}" cy="{chip_y + chip_h}" r="4" fill="{color}"/>')
        svg_parts.append(f'<text x="{x}" y="{i2c_y}" fill="{color}" font-family="monospace" font-size="8" text-anchor="middle">{pin_name}</text>')

    # === External Components ===
    comp_y = chip_y + chip_h + 60

    # Power supply section
    svg_parts.append(f'<text x="20" y="{comp_y}" fill="#22c55e" font-family="monospace" font-size="13" text-anchor="start">⚡ Power Supply</text>')
    svg_parts.append(f'<rect x="20" y="{comp_y + 5}" width="860" height="60" rx="6" fill="#111827" stroke="#374151" stroke-width="1"/>')
    svg_parts.append(f'<text x="35" y="{comp_y + 25}" fill="#e5e7eb" font-family="monospace" font-size="9">Battery 12V → 1N5408 → SMAJ28A → 470µF+100nF → 7805 (5V/1A) → ESP32 VIN</text>')
    svg_parts.append(f'<text x="35" y="{comp_y + 40}" fill="#9ca3af" font-family="monospace" font-size="8">3.3V LDO for sensors/OLED•Voltage dividers: GPIO35 (100k/33k) • GPIO36 (100k/33k)</text>')
    svg_parts.append(f'<text x="35" y="{comp_y + 55}" fill="#f59e0b" font-family="monospace" font-size="8">DEEP SLEEP: 80mA → 10µA after 5 min engine off • Wake: GPIO4 (Mode+) or GPIO18 (Ignition)</text>')

    # Exhaust valve system
    comp_y += 80
    svg_parts.append(f'<text x="20" y="{comp_y}" fill="#22d3ee" font-family="monospace" font-size="13">🔧 Exhaust Valve + Airbox (DRV8833 Production)</text>')
    svg_parts.append(f'<rect x="20" y="{comp_y + 5}" width="860" height="80" rx="6" fill="#111827" stroke="#374151" stroke-width="1"/>')
    svg_parts.append(f'<text x="35" y="{comp_y + 22}" fill="#e5e7eb" font-family="monospace" font-size="9">Exhaust: Pololu 37Dx52L gearmotor → DRV8833 (GPIO14=AIN1, GPIO13=AIN2) → AS5600 @ 0x36</text>')
    svg_parts.append(f'<text x="35" y="{comp_y + 37}" fill="#e5e7eb" font-family="monospace" font-size="9">Airbox: Pololu 37Dx52L gearmotor → DRV8833 (GPIO23=BIN1, GPIO2=BIN2) → AS5600 @ 0x37</text>')
    svg_parts.append(f'<text x="35" y="{comp_y + 52}" fill="#9ca3af" font-family="monospace" font-size="8">Mode: EXHAUST_VALVE=GPIO25(PWM), AIRBOX_FLAP=GPIO26(PWM) — used in RC servo testing only</text>')
    svg_parts.append(f'<text x="35" y="{comp_y + 60}" fill="#f59e0b" font-family="monospace" font-size="8">v2.2 NEW: Auto-RPM valve curves — position follows RPM per mode (5 interpolation points)</text>')
    svg_parts.append(f'<text x="35" y="{comp_y + 72}" fill="#9ca3af" font-family="monospace" font-size="8">Production: USE_PRODUCTION_MOTOR=1 in platformio.ini → DRV8833+AS5600</text>')

    # CDI system
    comp_y += 100
    svg_parts.append(f'<text x="20" y="{comp_y}" fill="#ef4444" font-family="monospace" font-size="13">⚡ Ignition (Ignitech DC-CDI-P2 3-Map)</text>')
    svg_parts.append(f'<rect x="20" y="{comp_y + 5}" width="860" height="50" rx="6" fill="#111827" stroke="#374151" stroke-width="1"/>')
    svg_parts.append(f'<text x="35" y="{comp_y + 22}" fill="#e5e7eb" font-family="monospace" font-size="9">CDI Map A (eco): GPIO27=LOW, GPIO33=HIGH → STRASSE/STADT/COMFORT</text>')
    svg_parts.append(f'<text x="35" y="{comp_y + 37}" fill="#e5e7eb" font-family="monospace" font-size="9">CDI Map B (sport): GPIO27=HIGH, GPIO33=LOW → GELÄNDE/SPORT</text>')
    svg_parts.append(f'<text x="35" y="{comp_y + 50}" fill="#e5e7eb" font-family="monospace" font-size="9">CDI Map C (fallback): GPIO27=HIGH, GPIO33=HIGH → SOUND/Emergency</text>')

    # Sensors section
    comp_y += 70
    svg_parts.append(f'<text x="20" y="{comp_y}" fill="#a78bfa" font-family="monospace" font-size="13">📡 Sensors + Display</text>')
    svg_parts.append(f'<rect x="20" y="{comp_y + 5}" width="860" height="70" rx="6" fill="#111827" stroke="#374151" stroke-width="1"/>')
    svg_parts.append(f'<text x="35" y="{comp_y + 22}" fill="#e5e7eb" font-family="monospace" font-size="9">SSD1306 OLED (128x64 I2C) @ 0x3C — SDA=GPIO21, SCL=GPIO22</text>')
    svg_parts.append(f'<text x="35" y="{comp_y + 37}" fill="#e5e7eb" font-family="monospace" font-size="9">NTC 10kΩ Thermistor → GPIO34 (ADC) • Oil Pressure → GPIO19 • Ignition Pulse → GPIO18</text>')
    svg_parts.append(f'<text x="35" y="{comp_y + 52}" fill="#9ca3af" font-family="monospace" font-size="8">Battery Voltage → GPIO35 (100k/33k divider) • Stator Output → GPIO36 (100k/33k divider)</text>')
    svg_parts.append(f'<text x="35" y="{comp_y + 65}" fill="#f59e0b" font-family="monospace" font-size="8">v2.2 NEW: Fuel estimation (software) • Gear detection (RPM/speed correlation) • Config mode (3s press)</text>')

    # Controls section
    comp_y += 90
    svg_parts.append(f'<text x="20" y="{comp_y}" fill="#60a5fa" font-family="monospace" font-size="13">🎮 Controls + LED</text>')
    svg_parts.append(f'<rect x="20" y="{comp_y + 5}" width="860" height="50" rx="6" fill="#111827" stroke="#374151" stroke-width="1"/>')
    svg_parts.append(f'<text x="35" y="{comp_y + 22}" fill="#e5e7eb" font-family="monospace" font-size="9">KY-040 Encoder: CLK=GPIO16, DT=GPIO17, BTN=GPIO0 • Mode+=GPIO4, Mode-=GPIO5</text>')
    svg_parts.append(f'<text x="35" y="{comp_y + 37}" fill="#e5e7eb" font-family="monospace" font-size="9">WS2812 RGB LED → GPIO32 • Long press (3s) → Config Mode • Encoder toggle → Mode/Page select</text>')
    svg_parts.append(f'<text x="35" y="{comp_y + 50}" fill="#9ca3af" font-family="monospace" font-size="8">Config: Brightness → Valve Cal → Airbox Cal → Mode Select → Exit</text>')

    # Footer
    svg_parts.append(f'<text x="{width//2}" y="{height - 20}" fill="#64748b" font-family="monospace" font-size="9" text-anchor="middle">AQL v2.2 • Auto-RPM Valve • Fuel Estimation • Gear Detection • Deep Sleep • Config Mode • BLE</text>')

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def generate_ascii():
    """Generate ASCII wiring diagram."""
    lines = []
    lines.append("=" * 80)
    lines.append("  African Queen Lite — ESP32 Wiring Diagram v2.2")
    lines.append("  Honda NX650 Dominator RFVC")
    lines.append("  Auto-RPM Valve + Fuel + Gear + Sleep + Config")
    lines.append("=" * 80)
    lines.append("")

    lines.append("  ESP32 DevKit V1 — Pin Mapping v2.2")
    lines.append("  " + "-" * 76)

    lines.append("")
    lines.append("  INPUTS:")
    lines.append("    GPIO  4  ← Mode+ button (handlebar, pullup)")
    lines.append("    GPIO  5  ← Mode- button (handlebar, pullup)")
    lines.append("    GPIO  0  ← Encoder BTN (BOOT pin, internal pullup)")
    lines.append("    GPIO 16  ← Encoder A (CLK, interrupt)")
    lines.append("    GPIO 17  ← Encoder B (DT)")
    lines.append("    GPIO 18  ← Ignition pulse coil (interrupt, optocoupler)")
    lines.append("    GPIO 19  ← Oil pressure switch (LOW = pressure OK)")
    lines.append("    GPIO 34  ← ADC: Thermistor (NTC 10kΩ)")
    lines.append("    GPIO 35  ← ADC: Battery voltage divider")
    lines.append("    GPIO 36  ← ADC: Stator voltage divider (v2.0+)")
    lines.append("")

    lines.append("  OUTPUTS:")
    lines.append("    GPIO 25  → PWM: Exhaust valve servo")
    lines.append("    GPIO 26  → PWM: Airbox flap servo")
    lines.append("    GPIO 27  → CDI Map A select (active LOW)")
    lines.append("    GPIO 33  → CDI Map B select (active LOW)")
    lines.append("    GPIO 32  → WS2812 RGB LED data")
    lines.append("")

    lines.append("  I2C Bus (SDA=GPIO21, SCL=GPIO22):")
    lines.append("    SSD1306 OLED @ 0x3C")
    lines.append("    AS5600 Exhaust @ 0x36 (production: DRV8833)")
    lines.append("    AS5600 Airbox   @ 0x37 (production: DRV8833)")
    lines.append("")

    lines.append("  DRV8833 Production Motor Driver (USE_PRODUCTION_MOTOR=1):")
    lines.append("    GPIO 14  → DRV8833 AIN1 (Exhaust valve)")
    lines.append("    GPIO 13  → DRV8833 AIN2 (Exhaust valve)")
    lines.append("    GPIO 23  → DRV8833 BIN1 (Airbox flap)")
    lines.append("    GPIO  2  → DRV8833 BIN2 (Airbox flap)")
    lines.append("")

    lines.append("  DEEP SLEEP WAKE SOURCES:")
    lines.append("    GPIO  4  ← EXT0: Mode+ button (wake on LOW)")
    lines.append("    GPIO 18  ← EXT1: Ignition pulse (wake on HIGH)")
    lines.append("")

    lines.append("=" * 80)
    lines.append("  POWER SUPPLY")
    lines.append("=" * 80)
    lines.append("")
    lines.append("  Motorcycle Battery (12V, LiFePO4 4S)")
    lines.append("      │")
    lines.append("      ├── 1N5408 Reverse Polarity Protection Diode")
    lines.append("      ├── SMAJ28A TVS Diode (28V clamp)")
    lines.append("      ├── 470µF Electrolytic Cap (bulk filtering)")
    lines.append("      ├── 100nF Ceramic Cap (HF decoupling)")
    lines.append("      ├── 7805 Voltage Regulator → 5V/1A")
    lines.append("      │       └── ESP32 VIN (5V input)")
    lines.append("      │")
    lines.append("      ├── Voltage Divider #1 (Battery ADC)")
    lines.append("      │       R1 = 100kΩ → Battery+")
    lines.append("      │       R2 = 33kΩ  → GND")
    lines.append("      │       Junction → GPIO 35")
    lines.append("      │")
    lines.append("      └── Voltage Divider #2 (Stator ADC)")
    lines.append("              R1 = 100kΩ → Regulator output+")
    lines.append("              R2 = 33kΩ  → GND")
    lines.append("              Junction → GPIO 36")
    lines.append("")

    lines.append("=" * 80)
    lines.append("  CDI 3-MAP CONTROL (Ignitech DC-CDI-P2)")
    lines.append("=" * 80)
    lines.append("")
    lines.append("  Mode         CDI_MAP_A  CDI_MAP_B  Map  Used By")
    lines.append("  ────────────────────────────────────────────────")
    lines.append("  Eco/Retard   LOW        HIGH       A    STRASSE, STADT, COMFORT")
    lines.append("  Advanced     HIGH       LOW        B    GELÄNDE, SPORT")
    lines.append("  Fallback     HIGH       HIGH       C    SOUND, Emergency")
    lines.append("")

    lines.append("=" * 80)
    lines.append("  RIDE MODES v2.2")
    lines.append("=" * 80)
    lines.append("")
    lines.append("  Mode       Ign  Valve Airbox Idle  RevL  Sweep CDI Throttle Fuel")
    lines.append("  ─────────────────────────────────────────────────────────────────")
    lines.append("  STRASSE     0°   50%   50%  1300  7000   3    A   LINEAR   3.5L")
    lines.append("  STADT      -2°   20%   30%  1200  6500   2    A   SOFT     3.0L")
    lines.append("  GELÄNDE    +2°  100%  100%  1400  7500   6    B   AGGR     4.5L")
    lines.append("  SPORT      +3°  100%  100%  1350  7500   8    B   AGGR     5.0L")
    lines.append("  COMFORT    -1°   40%   40%  1250  6500   2    A   SOFT     3.2L")
    lines.append("  SOUND      +1°  100%   80%  1300  7000   5    C   PROG     4.0L")
    lines.append("")

    lines.append("=" * 80)
    lines.append("  v2.2 NEW FEATURES")
    lines.append("=" * 80)
    lines.append("")
    lines.append("  1. AUTO-RPM VALVE: Exhaust & airbox follow RPM curves per mode")
    lines.append("     - 5 interpolation points per mode (RPM → valve position %)")
    lines.append("     - Overrides static valve_percent when ENABLE_AUTO_RPM_VALVE=1")
    lines.append("")
    lines.append("  2. FUEL ESTIMATION: mL/100km per mode + range + low fuel alert")
    lines.append("     - RPM-adjusted consumption (idle -30%, high RPM +25%)")
    lines.append("     - 16L tank, 3.4L reserve warning, 1.5L critical")
    lines.append("")
    lines.append("  3. GEAR DETECTION: RPM/speed correlation estimates current gear")
    lines.append("     - Uses NX650 gear ratios: 2.846, 1.857, 1.389, 1.091, 0.913")
    lines.append("     - 15% tolerance, confidence percentage display")
    lines.append("")
    lines.append("  4. DEEP SLEEP: 5 min engine off → ESP32 deep sleep (~10µA)")
    lines.append("     - Wake sources: GPIO4 (Mode+ button) and GPIO18 (Ignition pulse)")
    lines.append("")
    lines.append("  5. CONFIG MODE: Long press encoder (3s) → on-bike settings")
    lines.append("     - Brightness → Valve Cal → Airbox Cal → Mode Select → Exit")
    lines.append("     - Auto-exit after 10s inactivity")
    lines.append("")

    return "\n".join(lines)


def main():
    # Generate SVG
    svg_content = generate_svg()
    svg_path = os.path.join(OUTPUT_DIR, "wiring_diagram.svg")
    with open(svg_path, 'w') as f:
        f.write(svg_content)
    print(f"SVG written to {svg_path}")

    # Generate ASCII
    ascii_content = generate_ascii()
    txt_path = os.path.join(OUTPUT_DIR, "wiring_diagram.txt")
    with open(txt_path, 'w') as f:
        f.write(ascii_content)
    print(f"ASCII written to {txt_path}")


if __name__ == '__main__':
    main()