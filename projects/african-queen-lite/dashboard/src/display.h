#pragma once
// ============================================================
// African Queen Lite — OLED Display (SSD1306 128x64 I2C)
// Honda NX650 Dominator RFVC
// ============================================================
//
// Display layout (128x64):
//   Line 1: MODE NAME         RPM:XXXX
//   Line 2: TEMP:XXX°C  VOLT:XX.XV
//   Line 3: VALVE:XX%   AIR:XX%
//   Line 4: OIL:[OK/WARN]    MAP:[A/B]
//   + Warning bar at bottom if alerts active

#include "modes.h"
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

class Display {
public:
    Display() : oled_(128, 64, &Wire, -1),
                initialized_(false), show_mode_until_(0),
                flash_alert_(false), alert_toggle_ms_(0) {}

    bool begin() {
        Wire.begin(Pin::OLED_SDA, Pin::OLED_SCL);
        if (!oled_.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
            Serial.println("[DISPLAY] ERROR: SSD1306 not found!");
            initialized_ = false;
            return false;
        }
        initialized_ = true;
        oled_.clearDisplay();
        oled_.setTextColor(SSD1306_WHITE);
        oled_.display();

        // Show splash screen
        oled_.clearDisplay();
        oled_.setCursor(10, 8);
        oled_.setTextSize(2);
        oled_.print(F("AQL"));
        oled_.setCursor(10, 28);
        oled_.setTextSize(1);
        oled_.print(F("Ride Mode Ctrl"));
        oled_.setCursor(10, 45);
        oled_.print(F("NX650 RFVC"));
        oled_.display();
        delay(1500);  // Show splash briefly

        Serial.println("[DISPLAY] SSD1306 initialized (128x64 I2C)");
        return true;
    }

    // Main display update — call at regular interval
    void update(RideMode mode, uint16_t rpm, float temp, float voltage,
                uint8_t valve_pos, uint8_t airbox_pos,
                bool oil_ok, uint8_t cdi_map,
                bool temp_warn, bool volt_warn) {
        if (!initialized_) return;

        oled_.clearDisplay();

        unsigned long now = millis();

        // If mode was just switched, show large mode name
        if (now < show_mode_until_) {
            drawModeSplash(mode);
            oled_.display();
            return;
        }

        // ---- Normal display layout ----
        // Line 1: Mode + RPM
        oled_.setTextSize(1);
        oled_.setCursor(0, 0);
        oled_.print(MODE_NAMES[mode]);
        oled_.setCursor(80, 0);
        oled_.print(rpm);
        oled_.print(F(" RPM"));

        // Line 2: Temperature + Voltage
        oled_.setCursor(0, 12);
        if (temp_warn) {
            oled_.print(F("!"));  // Warning indicator
        }
        oled_.print((int)temp);
        oled_.print(F("C"));
        oled_.setCursor(72, 12);
        oled_.print(voltage, 1);
        oled_.print(F("V"));
        if (volt_warn) {
            oled_.print(F("!"));
        }

        // Line 3: Valve + Airbox positions
        oled_.setCursor(0, 24);
        oled_.print(F("V:"));
        oled_.print(valve_pos);
        oled_.print(F("%"));
        oled_.setCursor(64, 24);
        oled_.print(F("A:"));
        oled_.print(airbox_pos);
        oled_.print(F("%"));

        // Line 4: Oil pressure + CDI map
        oled_.setCursor(0, 36);
        oled_.print(F("OIL:"));
        if (oil_ok) {
            oled_.print(F("OK"));
        } else {
            // Flash OIL WARN
            if ((now / 500) % 2 == 0) {
                oled_.print(F("LOW!"));
            } else {
                oled_.print(F("    "));
            }
        }
        oled_.setCursor(64, 36);
        oled_.print(F("MAP:"));
        oled_.print(cdi_map == 0 ? 'A' : 'B');

        // Bottom bar: alert warnings
        if (temp_warn || volt_warn || !oil_ok) {
            drawAlertBar(temp_warn, volt_warn, !oil_ok);
        }

        oled_.display();
    }

    // Show mode name prominently after switching
    void showModeSwitch(RideMode mode) {
        show_mode_until_ = millis() + MODE_DISPLAY_MS;
    }

private:
    Adafruit_SSD1306 oled_;
    bool initialized_;
    unsigned long show_mode_until_;
    bool flash_alert_;
    unsigned long alert_toggle_ms_;

    void drawModeSplash(RideMode mode) {
        // Large mode name centered
        oled_.setTextSize(2);
        oled_.setCursor(4, 10);
        oled_.print(MODE_NAMES[mode]);

        // Mode color indicator (simplified as text, actual color shown on LED)
        oled_.setTextSize(1);
        oled_.setCursor(4, 35);
        oled_.print(F("IGN:"));
        int8_t off = MODE_PARAMS[mode].ignition_offset;
        if (off >= 0) oled_.print(F("+"));
        oled_.print(off);
        oled_.print(F("d  "));

        oled_.setCursor(4, 47);
        oled_.print(F("VALVE:"));
        oled_.print(MODE_PARAMS[mode].valve_percent);
        oled_.print(F("% AIR:"));
        oled_.print(MODE_PARAMS[mode].airbox_percent);
        oled_.print(F("%"));
    }

    void drawAlertBar(bool temp_warn, bool volt_warn, bool oil_warn) {
        oled_.setCursor(0, 54);
        oled_.setTextSize(1);
        unsigned long now = millis();

        // Flash text
        if ((now / 300) % 2 == 0) {
            if (temp_warn) { oled_.print(F("TEMP! ")); }
            if (volt_warn) { oled_.print(F("BATT! ")); }
            if (oil_warn)  { oled_.print(F("OIL! ")); }
        }
    }
};