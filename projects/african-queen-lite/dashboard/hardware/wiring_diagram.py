#!/usr/bin/env python3
"""
AQL Ride-Mode Controller — Wiring Diagram Generator
====================================================
Generates SVG + ASCII wiring diagrams for the ESP32-based
Honda NX650 Dominator ride-mode controller.

Pin definitions from: src/modes.h
Outputs:
  - hardware/wiring_diagram.svg   (dark-themed SVG)
  - hardware/wiring_diagram.txt   (ASCII art diagram)

Author: Hermes Agent / Nous Research
Date:   2026-05-28
"""

import os
import math

# ──────────────────────────────────────────────────────────
# PIN MAPPING (from src/modes.h + CDI_MAP_B addition)
# ──────────────────────────────────────────────────────────
PINS = {
    # UI — Buttons & Encoder
    "MODE_UP":         {"pin": 4,  "group": "Input",   "desc": "Mode+ button",          "color": "signal"},
    "MODE_DOWN":       {"pin": 5,  "group": "Input",   "desc": "Mode- button",          "color": "signal"},
    "ENCODER_A":       {"pin": 16, "group": "Input",   "desc": "Encoder CLK (int)",     "color": "signal"},
    "ENCODER_B":       {"pin": 17, "group": "Input",   "desc": "Encoder DT",            "color": "signal"},
    "ENCODER_BTN":     {"pin": 0,  "group": "Input",   "desc": "Encoder push (BOOT)",   "color": "signal"},
    # Sensors
    "IGNITION_PULSE":  {"pin": 18, "group": "Sensor",  "desc": "Ignition pulse coil",   "color": "signal"},
    "OIL_PRESSURE":    {"pin": 19, "group": "Sensor",  "desc": "Oil pressure switch",   "color": "signal"},
    "THERMISTOR":      {"pin": 34, "group": "Sensor",  "desc": "Cyl. head NTC 10kΩ",    "color": "signal"},
    "VOLTAGE_DIVIDER": {"pin": 35, "group": "Sensor",  "desc": "Battery 12V÷ /100k33k", "color": "signal"},
    "STATOR_SENSE":    {"pin": 36, "group": "Sensor",  "desc": "Stator volt ÷ /100k33k","color": "signal"},
    # Actuators
    "EXHAUST_VALVE":   {"pin": 25, "group": "Actuator","desc": "Exhaust valve servo",   "color": "pwm"},
    "AIRBOX_FLAP":     {"pin": 26, "group": "Actuator","desc": "Airbox flap servo",     "color": "pwm"},
    "CDI_MAP_SELECT":  {"pin": 27, "group": "Actuator","desc": "CDI map select A/B",    "color": "signal"},
    "CDI_MAP_B":       {"pin": 33, "group": "Actuator","desc": "CDI map B (new)",       "color": "signal"},
    "LED_DATA":        {"pin": 32, "group": "Actuator","desc": "WS2812 LED data",        "color": "signal"},
    # I²C / Display
    "OLED_SDA":        {"pin": 21, "group": "UI",     "desc": "OLED I2C SDA",           "color": "signal"},
    "OLED_SCL":        {"pin": 22, "group": "UI",     "desc": "OLED I2C SCL",           "color": "signal"},
}

# Wire colour mapping
WIRE_COLORS = {
    "power":  "#E53935",   # red
    "signal": "#42A5F5",   # blue
    "ground": "#66BB6A",   # green
    "pwm":    "#FFA726",   # orange
}

WIRE_NAMES = {
    "power":  "Power (red)",
    "signal": "Signal (blue)",
    "ground": "Ground (green)",
    "pwm":    "PWM (orange)",
}

# ──────────────────────────────────────────────────────────
# SVG GENERATOR
# ──────────────────────────────────────────────────────────

def gen_svg(path: str) -> str:
    W, H = 1200, 900
    cx, cy = 600, 420  # ESP32 centre

    # Colours
    BG      = "#1a1a2e"
    ESP_BG  = "#16213e"
    BOX_BG  = "#0f3460"
    BOX_BD  = "#e94560"
    TEXT    = "#e0e0e0"
    SUB     = "#90a4ae"
    ACCENT  = "#e94560"
    TITLE_C = "#ffffff"

    lines = []
    def S(*args, **kw):
        attrs = " ".join(f'{k.replace("_","-")}="{v}"' for k, v in kw.items())
        lines.append(f"  <{args[0]} {attrs}>{' '.join(args[1:])}</{args[0]}>")
    def R(x, y, w, h, rx=6, fill=BOX_BG, stroke=BOX_BD, sw=2, opacity=1):
        S("rect", x=x, y=y, w=w, h=h, rx=rx, fill=fill, stroke=stroke,
          stroke_width=sw, opacity=opacity)
    def T(x, y, txt, fill=TEXT, fs=13, anchor="middle", bold=False, ff="sans-serif"):
        fw = "bold" if bold else "normal"
        S("text", x=x, y=y, fill=fill, font_size=fs,
          text_anchor=anchor, font_family=ff, font_weight=fw, dominant_baseline="central",
          _raw=txt)
    def LINE(x1, y1, x2, y2, col="#42A5F5", sw=2, dash=""):
        da = f'stroke-dasharray="{dash}"' if dash else ""
        lines.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                     f'stroke="{col}" stroke-width="{sw}" {da}/>')

    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
                 f'width="{W}" height="{H}">')
    lines.append(f'  <rect width="{W}" height="{H}" fill="{BG}"/>')
    lines.append(f'  <defs>')
    lines.append(f'    <filter id="shadow"><feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity=".4"/></filter>')
    lines.append(f'    <marker id="dot" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6">')
    lines.append(f'      <circle cx="5" cy="5" r="3" fill="{ACCENT}"/>')
    lines.append(f'    </marker>')
    lines.append(f'  </defs>')

    # ── Title ──
    T(W/2, 28, "AQL Ride-Mode Controller — ESP32 Wiring Diagram", TITLE_C, 22, bold=True)
    T(W/2, 52, "Honda NX650 Dominator • v2.0  •  Dark Theme", SUB, 13)

    # ── Power Conditioning Block (top) ──
    px, py = 40, 75
    pw, ph = 340, 130
    R(px, py, pw, ph, fill="#1b2838", stroke="#e94560")
    T(px+pw/2, py+18, "🔋 POWER CONDITIONING", "#ffffff", 14, bold=True)
    T(px+20, py+45, "12V Bat ──┬─ 1N5408 (reverse-protect)", TEXT, 11, "start")
    T(px+20, py+63, "          ├─ SMAJ28A TVS (28V clamp)", TEXT, 11, "start")
    T(px+20, py+81, "          ├─ 470µF + 100nF (filter)", TEXT, 11, "start")
    T(px+20, py+99, "          └─ 7805 reg → 5V/1A → ESP32 VIN", TEXT, 11, "start")
    T(px+20, py+117, "Fuse: 5A main · 3A servo · 500mA ESP32 (polyfuse)", SUB, 10, "start")

    # ── Voltage Divider Detail ──
    vx, vy = 40, 215
    vw, vh = 340, 90
    R(vx, vy, vw, vh, fill="#1b2838", stroke="#FFA726")
    T(vx+vw/2, vy+16, "⚡ VOLTAGE DIVIDER SPEC (Battery & Stator)", "#FFA726", 12, bold=True)
    T(vx+20, vy+38, "R1 = 100 kΩ (¼W)  ── from 12V sense line", TEXT, 11, "start")
    T(vx+20, vy+56, "R2 =  33 kΩ (¼W)  ── to GND", TEXT, 11, "start")
    T(vx+20, vy+74, "Vout = Vin × R2/(R1+R2)  =  Vin × 0.248", SUB, 10, "start")

    # ── Legend (top-right) ──
    lx, ly = 820, 75
    lw, lh = 340, 130
    R(lx, ly, lw, lh, fill="#1b2838", stroke="#555")
    T(lx+lw/2, ly+18, "🎨 WIRE COLOR LEGEND", "#ffffff", 14, bold=True)
    yoff = ly + 48
    for cname, chex in WIRE_COLORS.items():
        LINE(lx+30, yoff, lx+80, yoff, chex, sw=4)
        T(lx+90, yoff, WIRE_NAMES[cname], TEXT, 12, "start")
        yoff += 24

    # ── ESP32 Box ──
    ew, eh = 220, 380
    ex, ey = cx - ew//2, cy - eh//2
    R(ex, ey, ew, eh, rx=12, fill=ESP_BG, stroke="#e94560", sw=3)
    T(cx, ey+22, "ESP32 DevKit V1", "#ffffff", 16, bold=True)
    T(cx, ey+42, "Xtensa LX6  •  240 MHz", SUB, 11)
    # Internal sections
    T(cx, ey+68, "── INPUTS (ADC/GPIO) ──", "#42A5F5", 11)
    T(cx, ey+88, "GPIO 0  ENC_BTN  (pullup)", TEXT, 10)
    T(cx, ey+104, "GPIO 4  MODE_UP   (pullup)", TEXT, 10)
    T(cx, ey+120, "GPIO 5  MODE_DOWN (pullup)", TEXT, 10)
    T(cx, ey+136, "GPIO 16 ENCODER_A (int)", TEXT, 10)
    T(cx, ey+152, "GPIO 17 ENCODER_B", TEXT, 10)
    T(cx, ey+168, "GPIO 18 IGN_PULSE (optocpl)", TEXT, 10)
    T(cx, ey+184, "GPIO 19 OIL_PRESS_SW", TEXT, 10)
    T(cx, ey+200, "GPIO 34 THERMISTOR  (ADC)", TEXT, 10)
    T(cx, ey+216, "GPIO 35 VOLT_DIV    (ADC)", TEXT, 10)
    T(cx, ey+232, "GPIO 36 STATOR_SENSE (ADC)", TEXT, 10)
    T(cx, ey+256, "── OUTPUTS (PWM/GPIO) ──", "#FFA726", 11)
    T(cx, ey+276, "GPIO 25 EXH_VALVE   (PWM)", TEXT, 10)
    T(cx, ey+292, "GPIO 26 AIRBOX_FLAP (PWM)", TEXT, 10)
    T(cx, ey+308, "GPIO 27 CDI_MAP_SEL (dig)", TEXT, 10)
    T(cx, ey+324, "GPIO 33 CDI_MAP_B  (new)", TEXT, 10)
    T(cx, ey+340, "GPIO 32 WS2812_LED (data)", TEXT, 10)
    T(cx, ey+360, "GPIO 21/22 I2C  OLED", TEXT, 10)

    # ── Helper: component box with wires ──
    def component_box(x, y, w, h, title, pins_label, color, icon=""):
        """Draw a component box and return connection points."""
        R(x, y, w, h, fill="#0d1b2a", stroke=color)
        if icon:
            T(x+w/2, y+18, icon + " " + title, "#ffffff", 13, bold=True)
        else:
            T(x+w/2, y+18, title, "#ffffff", 13, bold=True)
        T(x+w/2, y+h-14, pins_label, SUB, 9)
        # Return centre-left and centre-right connection points
        return (x, y+h//2), (x+w, y+h//2)

    bx_h = 70   # component box height

    # ── SENSORS (left side) ──
    sensor_x = 60
    sensor_w = 180
    sensor_gap = 20
    sensor_start_y = 330
    sensors = [
        ("🌡️  THERMISTOR", "GPIO 34 • ADC\nNTC 10kΩ pullup", "#42A5F5"),
        ("⚡ VOLTAGE DIV", "GPIO 35 • ADC\nR1=100k R2=33k", "#FFA726"),
        ("🔌 STATOR SENSE", "GPIO 36 • ADC\nR1=100k R2=33k", "#FFA726"),
        ("🛢️  OIL PRESS", "GPIO 19 • DIG\nSwitch LOW=OK", "#42A5F5"),
        ("⚡ IGN PULSE", "GPIO 18 • INT\nOptocoupler PC817", "#42A5F5"),
    ]
    sensor_conns = []
    sy = sensor_start_y
    for title, label, sc in sensors:
        (lx, ly), (rx, ry) = component_box(sensor_x, sy, sensor_w, bx_h, title, label, sc)
        # Wire from box right → ESP32 left edge
        esp_left_x = ex
        esp_left_y = ey + 80 + (sensors.index((title, label, sc))) * 34
        col = WIRE_COLORS["signal"] if sc != "#FFA726" else WIRE_COLORS["pwm"]
        LINE(rx, ry, esp_left_x, esp_left_y, col, sw=2)
        # Dot at ESP32 entry
        lines.append(f'  <circle cx="{esp_left_x}" cy="{esp_left_y}" r="4" fill="{ACCENT}"/>')
        sensor_conns.append((esp_left_x, esp_left_y, title))
        sy += bx_h + sensor_gap

    # ── ACTUATORS (right side) ──
    act_x = 960
    act_w = 180
    act_start_y = 320
    actuators = [
        ("🔧 EXH VALVE", "GPIO 25 • PWM\nServo/DRV8833", "#FFA726"),
        ("💨 AIRBOX FLAP", "GPIO 26 • PWM\nServo/DRV8833", "#FFA726"),
        ("🎛️  CDI MAP SEL", "GPIO 27 • DIG\nIgnitech CDI", "#42A5F5"),
        ("🎛️  CDI MAP B", "GPIO 33 • DIG\n(new pin)", "#42A5F5"),
        ("💡 WS2812 LED", "GPIO 32 • DATA\n5V • 470Ω R", "#42A5F5"),
    ]
    ay = act_start_y
    for title, label, ac in actuators:
        (lx, ly), (rx, ry) = component_box(act_x, ay, act_w, bx_h, title, label, ac)
        # ESP32 right edge → box left
        esp_right_x = ex + ew
        esp_right_y = ey + 268 + (actuators.index((title, label, ac))) * 34
        col = WIRE_COLORS["pwm"] if ac == "#FFA726" else WIRE_COLORS["signal"]
        LINE(esp_right_x, esp_right_y, lx, ly, col, sw=2)
        lines.append(f'  <circle cx="{esp_right_x}" cy="{esp_right_y}" r="4" fill="{ACCENT}"/>')
        ay += bx_h + sensor_gap

    # ── UI (bottom) ──
    ui_y = 770
    ui_h = 80
    ui_gap = 40

    # OLED I2C
    oled_x, oled_w = 200, 220
    (_, _), (rx_oled, ry_oled) = component_box(oled_x, ui_y, oled_w, ui_h,
        "🖥️  OLED SSD1306", "GPIO 21(SDA) • 22(SCL)\nI2C 128×64", "#42A5F5")
    LINE(ex + ew//2 - 60, ey + eh, rx_oled + oled_w//2 - 20, ry_oled, WIRE_COLORS["signal"], sw=2)
    T(ex + ew//2 - 60, ey + eh + 10, "I2C", SUB, 9)

    # Encoder
    enc_x, enc_w = 500, 220
    (_, _), (rx_enc, ry_enc) = component_box(enc_x, ui_y, enc_w, ui_h,
        "🔄 ROTARY ENCODER", "GPIO 16(A) • 17(B) • 0(BTN)\n10kΩ pullups • KY-040", "#42A5F5")
    LINE(ex + ew//2, ey + eh, rx_enc + enc_w//2 - 20, ry_enc, WIRE_COLORS["signal"], sw=2)
    T(ex + ew//2, ey + eh + 10, "ENC", SUB, 9)

    # Buttons
    btn_x, btn_w = 780, 220
    (_, _), (rx_btn, ry_btn) = component_box(btn_x, ui_y, btn_w, ui_h,
        "🔘 MODE BUTTONS", "GPIO 4 (MODE_UP) • 5 (MODE_DOWN)\nPullup to 3.3V • Handlebar", "#42A5F5")
    LINE(ex + ew//2 + 60, ey + eh, rx_btn + btn_w//2 - 20, ry_btn, WIRE_COLORS["signal"], sw=2)
    T(ex + ew//2 + 60, ey + eh + 10, "BTN", SUB, 9)

    # ── Power/GND rails ──
    # 3.3V rail
    V3_Y = 310
    LINE(400, V3_Y, 800, V3_Y, WIRE_COLORS["power"], sw=1.5, dash="4,4")
    T(405, V3_Y-8, "3.3V rail", WIRE_COLORS["power"], 9, "start")

    # GND rail
    GND_Y = 760
    LINE(400, GND_Y, 800, GND_Y, WIRE_COLORS["ground"], sw=1.5, dash="4,4")
    T(405, GND_Y-8, "GND rail", WIRE_COLORS["ground"], 9, "start")

    # ── Notes box (bottom right) ──
    nx, ny = 880, 770
    nw, nh = 280, 100
    R(nx, ny, nw, nh, fill="#1b2838", stroke="#e94560")
    T(nx+nw/2, ny+16, "📋 NOTES", "#ffffff", 12, bold=True)
    T(nx+15, ny+38, "• All wires: vibration-resistant,", TEXT, 9, "start")
    T(nx+15, ny+52, "  waterproof (Deutsch DT conn.)", TEXT, 9, "start")
    T(nx+15, ny+66, "• TVS diode SMAJ28A on 12V input", TEXT, 9, "start")
    T(nx+15, ny+80, "• 7805 heatsink required (>200mA)", TEXT, 9, "start")
    T(nx+15, ny+94, "• I²C pullups: 4.7kΩ to 3.3V", TEXT, 9, "start")

    # ── Footer ──
    T(W/2, H-15, "AQL Ride-Mode Controller  •  African Queen Lite  •  Honda NX650 Dominator", SUB, 10)

    # ── Pin labels on ESP32 box edges ──
    # Left edge pin labels
    left_pins = [
        (4, ey+85, "GPIO4 MODE_UP"),
        (5, ey+102, "GPIO5 MODE_DN"),
        (0, ey+119, "GPIO0 ENC_BTN"),
        (16, ey+136, "GPIO16 ENC_A"),
        (17, ey+153, "GPIO17 ENC_B"),
        (18, ey+170, "GPIO18 IGN_PLS"),
        (19, ey+187, "GPIO19 OIL_PR"),
        (34, ey+204, "GPIO34 THERM"),
        (35, ey+221, "GPIO35 VBAT"),
        (36, ey+238, "GPIO36 STATOR"),
    ]
    for pin_num, pyy, plabel in left_pins:
        T(ex-10, pyy, f"⦿{pin_num}", "#e94560", 8, "end")

    # Right edge pin labels
    right_pins = [
        (25, ey+274, "GPIO25 EXH_VLV"),
        (26, ey+291, "GPIO26 AIRBX"),
        (27, ey+308, "GPIO27 CDI_A"),
        (33, ey+325, "GPIO33 CDI_B"),
        (32, ey+342, "GPIO32 LED"),
    ]
    for pin_num, pyy, plabel in right_pins:
        T(ex+ew+10, pyy, f"{plabel} ⦿", "#e94560", 8, "start")

    lines.append("</svg>")
    svg = "\n".join(lines)

    with open(path, "w") as f:
        f.write(svg)
    return svg


# ──────────────────────────────────────────────────────────
# ASCII DIAGRAM GENERATOR
# ──────────────────────────────────────────────────────────

def gen_ascii(path: str) -> str:
    lines = []
    def P(s):
        lines.append(s)

    P("=" * 78)
    P("  AQL RIDE-MODE CONTROLLER — WIRING DIAGRAM (ASCII)")
    P("  Honda NX650 Dominator  •  ESP32 DevKit V1  •  v2.0")
    P("=" * 78)
    P("")

    P("┌─────────────────────────────────────────────────────────────────────────────┐")
    P("│                            POWER CONDITIONING                               │")
    P("├─────────────────────────────────────────────────────────────────────────────┤")
    P("│                                                                             │")
    P("│  12V Battery ──┬── [5A Fuse] ── 1N5408 (reverse-protect) ──┬── TVS SMAJ28A │")
    P("│                │                                            │  (28V clamp)   │")
    P("│                │                                            │                │")
    P("│                ├── 470µF Electrolytic ── 100nF Ceramic ────┤                │")
    P("│                │                                                           │")
    P("│                └── 7805 Regulator (heatsink req'd) ── 5V/1A ── ESP32 VIN   │")
    P("│                                                                             │")
    P("│  Fuses:  5A main  |  3A servo  |  500mA ESP32 (polyfuse)                   │")
    P("│  Wire:   18 AWG (power)  |  22-24 AWG (signal)  |  26 AWG (I2C)            │")
    P("│  Connectors:  Deutsch DT / Superseal  IP67 (all external)                   │")
    P("└─────────────────────────────────────────────────────────────────────────────┘")
    P("")

    P("┌─────────────────────────────────────────────────────────────────────────────┐")
    P("│                      VOLTAGE DIVIDER SPECIFICATION                          │")
    P("├─────────────────────────────────────────────────────────────────────────────┤")
    P("│                                                                             │")
    P("│  12V Sense ─── R1 = 100 kΩ (¼W) ──┬── To ESP32 GPIO 35/36 (ADC)           │")
    P("│                                    │                                        │")
    P("│                                 R2 = 33 kΩ (¼W)                            │")
    P("│                                    │                                        │")
    P("│                                  GND                                        │")
    P("│                                                                             │")
    P("│  Vout = Vin × R2/(R1+R2) = Vin × 0.248                                     │")
    P("│  Max sense: 14.6V → 3.62V  (safe for 3.3V ADC w/attenuation)               │")
    P("│  Two identical dividers: GPIO 35 = battery, GPIO 36 = stator/regulator      │")
    P("└─────────────────────────────────────────────────────────────────────────────┘")
    P("")

    P("┌─────────────────────────────────────────────────────────────────────────────┐")
    P("│                           ESP32 PIN MAPPING                                 │")
    P("├─────────────────────────────────────────────────────────────────────────────┤")
    P("│                                                                             │")
    P("│  ┌───────────────────────────────────────────────────────────────────────┐  │")
    P("│  │                         ESP32 DevKit V1                               │  │")
    P("│  │                                                                       │  │")
    P("│  │  INPUTS:                          OUTPUTS:                            │  │")
    P("│  │    GPIO  0  ← ENCODER_BTN (pullup)   GPIO 25 → EXHAUST_VALVE (PWM)   │  │")
    P("│  │    GPIO  4  ← MODE_UP  (pullup)      GPIO 26 → AIRBOX_FLAP  (PWM)    │  │")
    P("│  │    GPIO  5  ← MODE_DOWN (pullup)      GPIO 27 → CDI_MAP_SEL (DIG)    │  │")
    P("│  │    GPIO 16  ← ENCODER_A (int)         GPIO 33 → CDI_MAP_B (DIG new)  │  │")
    P("│  │    GPIO 17  ← ENCODER_B               GPIO 32 → WS2812_LED (DATA)    │  │")
    P("│  │    GPIO 18  ← IGNITION_PULSE (int)                                     │  │")
    P("│  │    GPIO 19  ← OIL_PRESSURE_SWITCH     I2C:                            │  │")
    P("│  │    GPIO 34  ← THERMISTOR (ADC)        GPIO 21 → OLED_SDA             │  │")
    P("│  │    GPIO 35  ← VOLTAGE_DIVIDER (ADC)   GPIO 22 → OLED_SCL             │  │")
    P("│  │    GPIO 36  ← STATOR_SENSE (ADC)                                      │  │")
    P("│  │                                                                       │  │")
    P("│  │  POWER:  VIN ← 5V (7805)  │  3V3 → sensors  │  GND ← common ground   │  │")
    P("│  └───────────────────────────────────────────────────────────────────────┘  │")
    P("│                                                                             │")
    P("└─────────────────────────────────────────────────────────────────────────────┘")
    P("")

    P("┌────── SENSORS ──────┐         ┌────── ACTUATORS ──────┐")
    P("│                      │         │                        │")
    P("│  THERMISTOR          │         │  EXHAUST VALVE SERVO   │")
    P("│    GPIO 34           │◄───────►│    GPIO 25 (PWM)       │")
    P("│    NTC 10kΩ + pullup │         │    DRV8833/MG996R      │")
    P("│                      │         │                        │")
    P("│  VOLTAGE DIVIDER     │         │  AIRBOX FLAP SERVO     │")
    P("│    GPIO 35           │◄───────►│    GPIO 26 (PWM)       │")
    P("│    R1=100k R2=33k    │         │    DRV8833/MG996R      │")
    P("│                      │         │                        │")
    P("│  STATOR SENSE        │         │  CDI MAP SELECT A      │")
    P("│    GPIO 36           │◄───────►│    GPIO 27 (DIG)       │")
    P("│    R1=100k R2=33k    │         │    Ignitech DC-CDI-P2  │")
    P("│                      │         │                        │")
    P("│  OIL PRESSURE SWITCH │         │  CDI MAP SELECT B      │")
    P("│    GPIO 19           │◄───────►│    GPIO 33 (DIG new)   │")
    P("│    LOW = pressure OK │         │                        │")
    P("│                      │         │  WS2812 RGB LED        │")
    P("│  IGNITION PULSE COIL │         │    GPIO 32 (DATA)      │")
    P("│    GPIO 18 (INT)     │◄───────►│    470Ω series R       │")
    P("│    PC817 optocoupler │         │    5V / GND            │")
    P("└──────────────────────┘         └────────────────────────┘")
    P("")
    P("┌──────── UI COMPONENTS ─────────┐")
    P("│                                 │")
    P("│  OLED SSD1306 (I2C)             │")
    P("│    GPIO 21 (SDA)  •  22 (SCL)  │")
    P("│    128×64  •  3.3V  •  GND     │")
    P("│    4.7kΩ pullups to 3.3V       │")
    P("│                                 │")
    P("│  ROTARY ENCODER (KY-040)        │")
    P("│    GPIO 16 (CLK)  •  17 (DT)   │")
    P("│    GPIO  0 (SW/button)          │")
    P("│    10kΩ pullups  •  3.3V  GND  │")
    P("│                                 │")
    P("│  MODE BUTTONS (handlebar)        │")
    P("│    GPIO  4 (MODE_UP)            │")
    P("│    GPIO  5 (MODE_DOWN)          │")
    P("│    Pullup to 3.3V  •  GND      │")
    P("│                                 │")
    P("└─────────────────────────────────┘")
    P("")
    P("─" * 78)
    P("  WIRE COLOR CODE:  Red = Power  |  Blue = Signal  |  Green = Ground  |  Orange = PWM")
    P("  TVS DIODE:  SMAJ28A (28V clamp, bidirectional) on 12V input line")
    P("  ALL EXTERNAL CONNECTIONS:  Deutsch DT or Superseal (IP67)")
    P("  ENCLOSURE:  3D-printed PETG/ABS  •  IP67  •  22mm handlebar clamp")
    P("─" * 78)
    P("")
    P("  Generated by wiring_diagram.py  •  Pin definitions from src/modes.h")
    P("  African Queen Lite  •  Nous Research  •  May 2026")
    P("=" * 78)

    ascii_txt = "\n".join(lines)
    with open(path, "w") as f:
        f.write(ascii_txt)
    return ascii_txt


# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(base, "wiring_diagram.svg")
    ascii_path = os.path.join(base, "wiring_diagram.txt")

    print("=" * 60)
    print("  AQL Wiring Diagram Generator")
    print("=" * 60)

    print(f"\n[1/2] Generating SVG diagram...")
    svg = gen_svg(svg_path)
    print(f"  ✓  Written: {svg_path}  ({len(svg)} chars)")

    print(f"\n[2/2] Generating ASCII diagram...")
    ascii_txt = gen_ascii(ascii_path)
    print(f"  ✓  Written: {ascii_path}  ({len(ascii_txt)} chars)")

    # Print the ASCII diagram inline as well
    print("\n" + "=" * 60)
    print("  ASCII DIAGRAM OUTPUT")
    print("=" * 60)
    print(ascii_txt)

    print("\nDone. Generated wiring_diagram.svg and wiring_diagram.txt")
    print(f"\nPin count: {len(PINS)} pins mapped")
    print("Includes CDI_MAP_B (GPIO 33) as new pin.")
