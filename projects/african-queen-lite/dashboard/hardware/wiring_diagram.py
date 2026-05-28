#!/usr/bin/env python3
"""
African Queen Lite — Wiring Diagram Generator v2.1
Generates SVG and ASCII wiring diagrams for the ESP32 Ride-Mode Controller.
Honda NX650 Dominator RFVC

Output:
  - wiring_diagram.svg (dark-themed, color-coded)
  - wiring_diagram.txt (ASCII diagram)

Run: python3 wiring_diagram.py
"""

import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# Pin Definitions (matches modes.h v2.1)
# ============================================================
PINS = {
    # Inputs
    "MODE_UP":         {"gpio": 4,  "type": "input",  "wire": "blue",   "desc": "Handlebar Mode+ Button"},
    "MODE_DOWN":       {"gpio": 5,  "type": "input",  "wire": "blue",   "desc": "Handlebar Mode- Button"},
    "ENCODER_A":       {"gpio": 16, "type": "input",  "wire": "blue",   "desc": "Rotary Encoder CLK"},
    "ENCODER_B":       {"gpio": 17, "type": "input",  "wire": "blue",   "desc": "Rotary Encoder DT"},
    "ENCODER_BTN":     {"gpio": 0,  "type": "input",  "wire": "blue",   "desc": "Encoder Push Button"},
    "IGNITION_PULSE":  {"gpio": 18, "type": "input",  "wire": "orange", "desc": "Pulse Generator Coil"},
    "OIL_PRESSURE":    {"gpio": 19, "type": "input",  "wire": "blue",   "desc": "Oil Pressure Switch"},
    "THERMISTOR":      {"gpio": 34, "type": "adc",    "wire": "green",  "desc": "Cylinder Head NTC 10kΩ"},
    "VOLTAGE_DIVIDER": {"gpio": 35, "type": "adc",    "wire": "red",    "desc": "Battery Voltage (R1=100k R2=33k)"},
    "STATOR_SENSE":    {"gpio": 36, "type": "adc",    "wire": "red",    "desc": "Stator Output Voltage Divider"},
    # Outputs
    "EXHAUST_VALVE":   {"gpio": 25, "type": "pwm",    "wire": "orange", "desc": "Exhaust Valve Servo PWM"},
    "AIRBOX_FLAP":     {"gpio": 26, "type": "pwm",    "wire": "orange", "desc": "Airbox Flap Servo PWM"},
    "CDI_MAP_A":       {"gpio": 27, "type": "output", "wire": "blue",   "desc": "CDI Map A Select (active LOW)"},
    "CDI_MAP_B":       {"gpio": 33, "type": "output", "wire": "blue",   "desc": "CDI Map B Select (active LOW)"},
    "LED_DATA":        {"gpio": 32, "type": "output", "wire": "orange", "desc": "WS2812 RGB LED Data"},
    # I2C
    "OLED_SDA":        {"gpio": 21, "type": "i2c",    "wire": "blue",   "desc": "OLED I2C SDA"},
    "OLED_SCL":        {"gpio": 22, "type": "i2c",    "wire": "blue",   "desc": "OLED I2C SCL"},
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

NOTES = [
    "Power Conditioning: TVS SMAJ28A | 470µF+100nF caps | 1N5408 reverse polarity | 7805→3.3V LDO",
    "Conformal Coating: MG Chemicals 422B (vibration/moisture)",
    "Anti-Vibration: Rubber grommets (McMaster 9485K52)",
    "Voltage Divider: R1=100kΩ, R2=33kΩ → Factor=4.03 (measures up to ~14.5V)",
    "CDI: Ignitech DC-CDI-P2 (2-map USB programmable) — Map A=eco, Map B=sport, both HIGH=fallback C",
    "Exhaust Valve: 12V gearmotor + DRV8833 + AS5600 (NOT RC servo for production!)",
    "Waterproof: IP67 housing, silicone-sealed cable glands",
    "Fuse: 5A fast-blow on +12V input line",
]


def generate_svg():
    """Generate a dark-themed SVG wiring diagram."""
    W, H = 1200, 900
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')

    # Background
    lines.append('<rect width="100%" height="100%" fill="#1a1a2e"/>')
    lines.append(f'<text x="{W//2}" y="30" fill="#e0e0e0" font-size="20" font-family="monospace" text-anchor="middle" font-weight="bold">'
                 'African Queen Lite — ESP32 Ride-Mode Controller Wiring Diagram v2.1</text>')
    lines.append(f'<text x="{W//2}" y="48" fill="#888" font-size="11" font-family="monospace" text-anchor="middle">'
                 'Honda NX650 Dominator RFVC</text>')

    # ESP32 central box
    esp_x, esp_y, esp_w, esp_h = 450, 80, 300, 700
    lines.append(f'<rect x="{esp_x}" y="{esp_y}" width="{esp_w}" height="{esp_h}" '
                 f'rx="8" fill="#16213e" stroke="#0f3460" stroke-width="2"/>')
    lines.append(f'<text x="{esp_x + esp_w//2}" y="{esp_y + 25}" fill="#e94560" font-size="16" '
                 f'font-family="monospace" text-anchor="middle" font-weight="bold">ESP32-WROOM-32</text>')
    lines.append(f'<text x="{esp_x + esp_w//2}" y="{esp_y + 42}" fill="#888" font-size="10" '
                 f'font-family="monospace" text-anchor="middle">AQL Ride-Mode Controller</text>')

    # Draw pin assignments inside ESP32 box
    pin_y = esp_y + 60
    pin_spacing = 19

    # Left side pins (inputs)
    left_pins = SVG_CATEGORIES["INPUTS"]
    for i, pin_name in enumerate(left_pins):
        pin = PINS[pin_name]
        y = pin_y + i * pin_spacing
        if y > esp_y + esp_h - 20:
            break
        color = WIRE_COLORS[pin["wire"]]
        # Pin label inside box
        lines.append(f'<text x="{esp_x + 10}" y="{y}" fill="{color}" font-size="9" '
                     f'font-family="monospace">GPIO{pin["gpio"]:2d} {pin_name}</text>')
        # Wire going left
        lines.append(f'<line x1="{esp_x}" y1="{y - 4}" x2="{esp_x - 60}" y2="{y - 4}" '
                     f'stroke="{color}" stroke-width="2"/>')
        # Connection dot
        lines.append(f'<circle cx="{esp_x}" cy="{y - 4}" r="3" fill="{color}"/>')

    # Right side pins (outputs + I2C)
    right_pins = SVG_CATEGORIES["OUTPUTS"] + SVG_CATEGORIES["I2C"]
    for i, pin_name in enumerate(right_pins):
        pin = PINS[pin_name]
        y = pin_y + i * pin_spacing
        if y > esp_y + esp_h - 20:
            break
        color = WIRE_COLORS[pin["wire"]]
        lines.append(f'<text x="{esp_x + esp_w - 10}" y="{y}" fill="{color}" font-size="9" '
                     f'font-family="monospace" text-anchor="end">{pin_name} GPIO{pin["gpio"]}</text>')
        lines.append(f'<line x1="{esp_x + esp_w}" y1="{y - 4}" x2="{esp_x + esp_w + 60}" y2="{y - 4}" '
                     f'stroke="{color}" stroke-width="2"/>')
        lines.append(f'<circle cx="{esp_x + esp_w}" cy="{y - 4}" r="3" fill="{color}"/>')

    # Component boxes on left (sensors/inputs)
    comp_x = 50
    comp_w = 220
    comp_y_start = 80
    comp_h = 30
    comp_spacing = 55

    input_components = [
        ("Handlebar Buttons", "Mode+/Mode- Buttons\nGPIO4, GPIO5", "#3399FF"),
        ("Rotary Encoder", "KY-040 Encoder\nGPIO16(CLK) GPIO17(DT) GPIO0(BTN)", "#3399FF"),
        ("Ignition Coil", "Pulse Generator Signal\nGPIO18 (Interrupt)", "#FF9933"),
        ("Oil Pressure", "Pressure Switch\nGPIO19 (LOW=OK)", "#3399FF"),
        ("Thermistor", "NTC 10kΩ Cylinder Head\nGPIO34 (ADC1 CH6)", "#33CC33"),
        ("Battery Voltage", "R1=100kΩ R2=33kΩ Divider\nGPIO35 (ADC1 CH7)", "#FF3333"),
        ("Stator Voltage", "Voltage Divider\nGPIO36 (ADC1 CH0)", "#FF3333"),
    ]

    for i, (name, desc, color) in enumerate(input_components):
        y = comp_y_start + i * comp_spacing
        # Component box
        lines.append(f'<rect x="{comp_x}" y="{y}" width="{comp_w}" height="{comp_h}" '
                     f'rx="4" fill="#16213e" stroke="{color}" stroke-width="1.5"/>')
        lines.append(f'<text x="{comp_x + comp_w//2}" y="{y + 12}" fill="{color}" font-size="8" '
                     f'font-family="monospace" text-anchor="middle" font-weight="bold">{name}</text>')
        lines.append(f'<text x="{comp_x + comp_w//2}" y="{y + 23}" fill="#888" font-size="7" '
                     f'font-family="monospace" text-anchor="middle">{desc.split(chr(10))[0]}</text>')

    # Component boxes on right (outputs)
    out_x = esp_x + esp_w + 80
    out_w = 240
    output_components = [
        ("Exhaust Valve", "PWM Servo / DRV8833\nGPIO25 → Servo/PWM", "#FF9933"),
        ("Airbox Flap", "PWM Servo / DRV8833\nGPIO26 → Servo/PWM", "#FF9933"),
        ("CDI Map Select", "Ignitech DC-CDI-P2\nGPIO27(A) GPIO33(B)", "#3399FF"),
        ("WS2812 LED", "RGB Mode Indicator\nGPIO32 → Data In", "#FF9933"),
        ("SSD1306 OLED", "128x64 I2C Display\nSDA=GPIO21 SCL=GPIO22", "#3399FF"),
    ]

    for i, (name, desc, color) in enumerate(output_components):
        y = comp_y_start + i * comp_spacing * 1.2
        lines.append(f'<rect x="{out_x}" y="{y}" width="{out_w}" height="{comp_h + 5}" '
                     f'rx="4" fill="#16213e" stroke="{color}" stroke-width="1.5"/>')
        lines.append(f'<text x="{out_x + out_w//2}" y="{y + 14}" fill="{color}" font-size="8" '
                     f'font-family="monospace" text-anchor="middle" font-weight="bold">{name}</text>')
        lines.append(f'<text x="{out_x + out_w//2}" y="{y + 26}" fill="#888" font-size="7" '
                     f'font-family="monospace" text-anchor="middle">{desc.split(chr(10))[0]}</text>')

    # Power conditioning box (bottom)
    pc_x, pc_y, pc_w2, pc_h2 = 50, 700, 400, 150
    lines.append(f'<rect x="{pc_x}" y="{pc_y}" width="{pc_w2}" height="{pc_h2}" '
                 f'rx="6" fill="#16213e" stroke="#FF3333" stroke-width="2"/>')
    lines.append(f'<text x="{pc_x + pc_w2//2}" y="{pc_y + 18}" fill="#FF3333" font-size="12" '
                 f'font-family="monospace" text-anchor="middle" font-weight="bold">⚡ Power Conditioning (CRITICAL)</text>')

    power_items = [
        "12V Battery → 5A Fuse → TVS SMAJ28A",
        "470µF + 100nF Decoupling Caps",
        "1N5408 Reverse Polarity Protection",
        "7805 → 3.3V LDO (or Mean Well RSD-30G-3.3)",
        "Conformal Coat: MG Chemicals 422B",
        "Mount: Rubber Grommets (McMaster 9485K52)",
    ]
    for i, item in enumerate(power_items):
        lines.append(f'<text x="{pc_x + 15}" y="{pc_y + 38 + i * 16}" fill="#ccc" font-size="9" '
                     f'font-family="monospace">• {item}</text>')

    # Legend
    leg_x, leg_y = out_x, 700
    lines.append(f'<rect x="{leg_x}" y="{leg_y}" width="260" height="150" rx="6" '
                 f'fill="#16213e" stroke="#555" stroke-width="1"/>')
    lines.append(f'<text x="{leg_x + 130}" y="{leg_y + 18}" fill="#e0e0e0" font-size="11" '
                 f'font-family="monospace" text-anchor="middle" font-weight="bold">Wire Color Legend</text>')
    legend_items = [
        ("Red", "#FF3333", "Power / Battery voltage"),
        ("Blue", "#3399FF", "Signal / Digital / I2C"),
        ("Green", "#33CC33", "Analog sensor / Ground"),
        ("Orange", "#FF9933", "PWM / Digital output"),
    ]
    for i, (name, color, desc) in enumerate(legend_items):
        yy = leg_y + 38 + i * 22
        lines.append(f'<line x1="{leg_x + 15}" y1="{yy}" x2="{leg_x + 55}" y2="{yy}" '
                     f'stroke="{color}" stroke-width="3"/>')
        lines.append(f'<text x="{leg_x + 65}" y="{yy + 4}" fill="#ccc" font-size="9" '
                     f'font-family="monospace">{name}: {desc}</text>')

    # Footer
    lines.append(f'<text x="{W//2}" y="{H - 8}" fill="#555" font-size="9" font-family="monospace" '
                 f'text-anchor="middle">Version 2.1 — 3-Map CDI + DRV8833 Motor Driver + Sunlight Display</text>')

    lines.append('</svg>')
    return '\n'.join(lines)


def generate_ascii():
    """Generate ASCII wiring diagram."""
    lines = []
    lines.append("=" * 80)
    lines.append("  AFRICAN QUEEN LITE — ESP32 RIDE-MODE CONTROLLER WIRING v2.1")
    lines.append("  Honda NX650 Dominator RFVC")
    lines.append("=" * 80)
    lines.append("")

    # Inputs
    lines.append("┌─────────────────────────────────────────────────────────────────────┐")
    lines.append("│                         INPUTS (Sensors + Controls)                │")
    lines.append("├─────────────────────────┬───────┬──────────────────────────────────┤")
    lines.append("│ Component               │ GPIO  │ Signal / Notes                   │")
    lines.append("├─────────────────────────┼───────┼──────────────────────────────────┤")

    input_table = [
        ("Handlebar Mode+ Btn",   "4",  "Digital IN, Pull-up, Debounced"),
        ("Handlebar Mode- Btn",   "5",  "Digital IN, Pull-up, Debounced"),
        ("Rotary Encoder CLK",   "16",  "Interrupt-capable, Quadrature A"),
        ("Rotary Encoder DT",    "17",  "Quadrature B direction"),
        ("Encoder Push Button",  "0",   "GPIO0=BOOT pin, Pull-up"),
        ("Ignition Pulse Coil",  "18",  "Interrupt RISING → RPM calc"),
        ("Oil Pressure Switch",  "19",  "LOW=OK, HIGH=WARNING"),
        ("Cylinder Head NTC",    "34",  "ADC1_CH6, NTC 10kΩ, Steinhart-Hart"),
        ("Battery V Divider",    "35",  "ADC1_CH7, R1=100kΩ R2=33kΩ → ×4.03"),
        ("Stator V Divider",     "36",  "ADC1_CH0, Same divider ratio"),
    ]
    for name, gpio, notes in input_table:
        lines.append(f"│ {name:23s} │ GPIO{gpio:2s} │ {notes:32s} │")

    lines.append("└─────────────────────────┴───────┴──────────────────────────────────┘")
    lines.append("")

    # Outputs
    lines.append("┌─────────────────────────────────────────────────────────────────────┐")
    lines.append("│                         OUTPUTS (Actuators + Display)              │")
    lines.append("├─────────────────────────┬───────┬──────────────────────────────────┤")
    lines.append("│ Component               │ GPIO  │ Signal / Notes                   │")
    lines.append("├─────────────────────────┼───────┼──────────────────────────────────┤")

    output_table = [
        ("Exhaust Valve Servo",  "25",  "PWM 50Hz, Servo or DRV8833 IN1"),
        ("Airbox Flap Servo",    "26",  "PWM 50Hz, Servo or DRV8833 IN1"),
        ("CDI Map A Select",     "27",  "Active LOW → Map A (eco timing)"),
        ("CDI Map B Select",     "33",  "Active LOW → Map B (sport timing)"),
        ("WS2812 RGB LED",       "32",  "Data In, Neopixel 1 LED"),
        ("OLED SDA (I2C)",       "21",  "SSD1306 128×64, Addr 0x3C"),
        ("OLED SCL (I2C)",       "22",  "I2C Clock, Shared with AS5600"),
    ]
    for name, gpio, notes in output_table:
        lines.append(f"│ {name:23s} │ GPIO{gpio:2s} │ {notes:32s} │")

    lines.append("└─────────────────────────┴───────┴──────────────────────────────────┘")
    lines.append("")

    # DRV8833 Production Mode
    lines.append("┌─────────────────────────────────────────────────────────────────────┐")
    lines.append("│           PRODUCTION MOTOR DRIVER (USE_PRODUCTION_MOTOR=1)         │")
    lines.append("├─────────────────────────┬───────┬──────────────────────────────────┤")
    lines.append("│ Component               │ GPIO  │ Signal / Notes                   │")
    lines.append("├─────────────────────────┼───────┼──────────────────────────────────┤")

    prod_table = [
        ("DRV8833 Exhaust IN1",  "14",  "H-bridge AIN1 → Exhaust motor"),
        ("DRV8833 Exhaust IN2",  "13",  "H-bridge AIN2 → Exhaust motor"),
        ("DRV8833 Airbox IN1",   "23",  "H-bridge BIN1 → Airbox motor"),
        ("DRV8833 Airbox IN2",    "2",  "H-bridge BIN2 → Airbox motor"),
        ("AS5600 Exhaust",    "I2C 0x36", "Magnetic encoder (exhaust pos)"),
        ("AS5600 Airbox",     "I2C 0x37", "Magnetic encoder (airbox pos)"),
    ]
    for name, gpio, notes in prod_table:
        lines.append(f"│ {name:23s} │ {gpio:5s} │ {notes:32s} │")

    lines.append("└─────────────────────────┴───────┴──────────────────────────────────┘")
    lines.append("")

    # CDI Map Selection Logic
    lines.append("┌──────────────────────────────────────────┐")
    lines.append("│        CDI 3-MAP SELECTION (v2.1)        │")
    lines.append("├──────────┬──────────┬─────────────────────┤")
    lines.append("│ MAP_A(27)│ MAP_B(33)│ Result              │")
    lines.append("├──────────┼──────────┼─────────────────────┤")
    lines.append("│ LOW      │ HIGH     │ Map A (eco/retarded)│")
    lines.append("│ HIGH     │ LOW      │ Map B (sport/advnc) │")
    lines.append("│ HIGH     │ HIGH     │ Map C (fallback/std)│")
    lines.append("│ LOW      │ LOW      │ INVALID — DON'T USE │")
    lines.append("└──────────┴──────────┴─────────────────────┘")
    lines.append("")

    # Power Conditioning
    lines.append("┌─────────────────────────────────────────────────────────────────────┐")
    lines.append("│                 ⚡ POWER CONDITIONING (CRITICAL)                      │")
    lines.append("├─────────────────────────────────────────────────────────────────────┤")
    for note in NOTES:
        lines.append(f"│  • {note:65s} │")
    lines.append("└─────────────────────────────────────────────────────────────────────┘")
    lines.append("")

    # Schematic sketch
    lines.append("                    ┌──────────────────────────┐")
    lines.append("   12V Battery ─────┤ 5A Fuse → TVS SMAJ28A    │")
    lines.append("                    │ 470µF + 100nF Caps       │")
    lines.append("                    │ 1N5408 Rev. Polarity Prot │")
    lines.append("                    │ 7805 → 3.3V LDO          │")
    lines.append("                    └──────────┬───────────────┘")
    lines.append("                               │")
    lines.append("                    ┌──────────▼───────────────┐")
    lines.append("   Buttons/Encoder ┤                          ├─ PWM → Exhaust Valve")
    lines.append("   Ignition Pulse  │      ESP32-WROOM-32       ├─ PWM → Airbox Flap")
    lines.append("   Oil Pressure    │   AQL Ride Mode Ctrl     ├─ GPIO → CDI Map A (27)")
    lines.append("   Thermistor      │                          ├─ GPIO → CDI Map B (33)")
    lines.append("   V Divider       │   6 Modes:               ├─ Data → WS2812 LED")
    lines.append("   Stator Sense    │   STRASSE/STADT/GELÄNDE  ├─ I2C → SSD1306 OLED")
    lines.append("                    │   SPORT/COMFORT/SOUND    ├─ BLE → Smartphone")
    lines.append("                    └──────────────────────────┘")
    lines.append("")

    return '\n'.join(lines)


def main():
    # Generate SVG
    svg = generate_svg()
    svg_path = os.path.join(OUTPUT_DIR, "wiring_diagram.svg")
    with open(svg_path, 'w') as f:
        f.write(svg)
    print(f"[OK] SVG wiring diagram → {svg_path}")

    # Generate ASCII
    ascii_text = generate_ascii()
    txt_path = os.path.join(OUTPUT_DIR, "wiring_diagram.txt")
    with open(txt_path, 'w') as f:
        f.write(ascii_text)
    print(f"[OK] ASCII wiring diagram → {txt_path}")

    print(f"\n{ascii_text}")


if __name__ == "__main__":
    main()