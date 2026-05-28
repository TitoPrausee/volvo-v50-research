#pragma once
// ============================================================
// African Queen Lite — OLED Display (SSD1306 128x64 I2C) v2.1
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.1: Sunlight readability optimizations:
//   - Inverted display mode (white bg, black text) for bright sun
//   - Bigger fonts for critical data (RPM, mode name)
//   - Compact layout with minimal whitespace
//   - Auto-detect sunlight via thermistor proximity (bright = hot = invert)
//   - Manual invert toggle via long encoder press
//   - CDI map display: A/B/C (was just A/B)
//
// Pages:
//   Page 0: Main ride display (mode, RPM, temp, voltage)
//   Page 1: Stator health + battery SOC
//   Page 2: Maintenance status (overdue items flash)
//   Page 3: Trip info (odometer, trip distance, peak temp)

#include "modes.h"
#include "longevity.h"
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Display pages
enum DisplayPage : uint8_t {
    PAGE_RIDE    = 0,  // Main ride mode display
    PAGE_HEALTH  = 1,  // Stator + battery
    PAGE_MAINT   = 2,  // Maintenance status
    PAGE_TRIP    = 3,  // Trip + odometer
    PAGE_COUNT   = 4
};

// Sunlight mode
enum SunlightMode : uint8_t {
    SUN_AUTO    = 0,  // Auto-detect from temperature
    SUN_NORMAL  = 1,  // Force normal (dark bg, white text)
    SUN_INVERT  = 2,  // Force inverted (white bg, black text — best in sunlight)
};

class Display {
public:
    Display() : oled_(128, 64, &Wire, -1),
                initialized_(false), show_mode_until_(0),
                current_page_(PAGE_RIDE), page_cycle_ms_(0),
                flash_alert_(false), alert_toggle_ms_(0),
                sunlight_mode_(SUN_AUTO), inverted_(false),
                last_sunlight_check_ms_(0) {}

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
        oled_.print(F("Ride Mode Ctrl v2.1"));
        oled_.setCursor(10, 42);
        oled_.print(F("NX650 RFVC"));
        oled_.setCursor(10, 54);
        oled_.print(F("3-MAP CDI+LONGEVITY"));
        oled_.display();
        delay(2000);

        Serial.println("[DISPLAY] SSD1306 initialized (128x64 I2C) v2.1");
        return true;
    }

    // Invert display for sunlight readability
    void setInverted(bool inv) {
        inverted_ = inv;
        oled_.ssd1306_command(inv ? SSD1306_INVERTDISPLAY : SSD1306_NORMALDISPLAY);
    }

    bool isInverted() const { return inverted_; }

    // Cycle sunlight mode: AUTO → NORMAL → INVERT → AUTO
    void cycleSunlightMode() {
        sunlight_mode_ = (SunlightMode)((sunlight_mode_ + 1) % 3);
        const char* modes[] = {"AUTO", "NORMAL", "INVERTED"};
        Serial.printf("[DISPLAY] Sunlight: %s\\n", modes[sunlight_mode_]);
    }

    // Page switching
    void nextPage() {
        current_page_ = (DisplayPage)((current_page_ + 1) % PAGE_COUNT);
        page_cycle_ms_ = millis();
    }

    void prevPage() {
        current_page_ = (DisplayPage)((current_page_ - 1 + PAGE_COUNT) % PAGE_COUNT);
        page_cycle_ms_ = millis();
    }

    DisplayPage getCurrentPage() const { return current_page_; }

    // Main display update — call at regular interval
    void update(RideMode mode, uint16_t rpm, float temp, float voltage,
                uint8_t valve_pos, uint8_t airbox_pos,
                bool oil_ok, uint8_t cdi_map,
                bool temp_warn, bool volt_warn,
                const LongevityMonitor& longevity) {
        if (!initialized_) return;

        oled_.clearDisplay();
        unsigned long now = millis();

        // ---- Sunlight Auto-Detect (check every 5s) ----
        if (now - last_sunlight_check_ms_ > 5000) {
            last_sunlight_check_ms_ = now;
            if (sunlight_mode_ == SUN_AUTO) {
                // Auto-invert when cylinder head is very hot (indicates strong sun)
                // Or ambient temperature > 35°C (bright sunlight likely)
                bool should_invert = (temp > 35.0f);
                if (should_invert != inverted_) {
                    setInverted(should_invert);
                }
            }
        }

        // Auto-cycle pages every 10 seconds
        if (now - page_cycle_ms_ > 10000) {
            current_page_ = (DisplayPage)((current_page_ + 1) % PAGE_COUNT);
            page_cycle_ms_ = now;
        }

        // If mode was just switched, show mode splash
        if (now < show_mode_until_) {
            drawModeSplash(mode);
            oled_.display();
            return;
        }

        // Draw current page
        switch (current_page_) {
            case PAGE_RIDE:   drawRidePage(mode, rpm, temp, voltage, valve_pos,
                                            airbox_pos, oil_ok, cdi_map, temp_warn, volt_warn); break;
            case PAGE_HEALTH:  drawHealthPage(longevity, voltage, rpm); break;
            case PAGE_MAINT:   drawMaintPage(longevity); break;
            case PAGE_TRIP:    drawTripPage(longevity, rpm); break;
            default:           drawRidePage(mode, rpm, temp, voltage, valve_pos,
                                            airbox_pos, oil_ok, cdi_map, temp_warn, volt_warn); break;
        }

        // Always show alert bar if any alerts active
        if (temp_warn || volt_warn || !oil_ok || longevity.getStatorStatus() >= STATOR_DEGRADED) {
            drawAlertBar(temp_warn, volt_warn, !oil_ok,
                         longevity.getStatorStatus() >= STATOR_DEGRADED);
        }

        // Page indicator dots in top-right corner
        for (uint8_t i = 0; i < PAGE_COUNT; i++) {
            oled_.drawPixel(120 + i * 4, 2, i == current_page_ ? SSD1306_WHITE : SSD1306_BLACK);
        }

        // Sunlight mode indicator (top-left)
        if (inverted_) {
            oled_.setCursor(0, 0);
            oled_.setTextSize(1);
            oled_.print(F("☀"));
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
    DisplayPage current_page_;
    unsigned long page_cycle_ms_;
    bool flash_alert_;
    unsigned long alert_toggle_ms_;
    SunlightMode sunlight_mode_;
    bool inverted_;
    unsigned long last_sunlight_check_ms_;

    // ============================================================
    // Page 0: Main Ride Display — BIG fonts for readability
    // ============================================================
    void drawRidePage(RideMode mode, uint16_t rpm, float temp, float voltage,
                       uint8_t valve_pos, uint8_t airbox_pos,
                       bool oil_ok, uint8_t cdi_map,
                       bool temp_warn, bool volt_warn) {
        // Line 1: Mode name (BOLD) + RPM (BIG)
        oled_.setTextSize(1);
        oled_.setCursor(0, 0);
        oled_.print(MODE_NAMES[mode]);

        // RPM — biggest number, right-aligned
        oled_.setTextSize(2);  // Big for sunlight readability
        oled_.setCursor(60, 0);
        oled_.print(rpm);

        // Line 2: Temperature + Voltage
        oled_.setTextSize(1);
        oled_.setCursor(0, 17);
        if (temp_warn) oled_.print(F("!"));
        oled_.print((int)temp);
        oled_.print(F("C"));
        oled_.setCursor(64, 17);
        oled_.print(voltage, 1);
        oled_.print(F("V"));
        if (volt_warn) oled_.print(F("!"));

        // Line 3: Valve + Airbox positions
        oled_.setCursor(0, 27);
        oled_.print(F("V:"));
        oled_.print(valve_pos);
        oled_.print(F("%"));
        oled_.setCursor(64, 27);
        oled_.print(F("A:"));
        oled_.print(airbox_pos);
        oled_.print(F("%"));

        // Line 4: Oil pressure + CDI map (v2.1: show A/B/C)
        oled_.setCursor(0, 37);
        oled_.print(F("OIL:"));
        if (oil_ok) {
            oled_.print(F("OK"));
        } else {
            if ((millis() / 500) % 2 == 0) oled_.print(F("LOW!"));
            else oled_.print(F("    "));
        }
        oled_.setCursor(64, 37);
        oled_.print(F("CDI:"));
        // v2.1: Display CDI map as A/B/C
        const char map_chars[] = {'A', 'B', 'C'};
        if (cdi_map < 3) oled_.print(map_chars[cdi_map]);
        else oled_.print(F("?"));

        // Bottom: throttle curve indicator
        oled_.setCursor(0, 47);
        const char* curve_name[] = {"LIN", "PRO", "AGR", "SFT"};
        oled_.print(F("THR:"));
        oled_.print(curve_name[MODE_PARAMS[mode].throttle_curve]);
    }

    // ============================================================
    // Page 1: Stator & Battery Health
    // ============================================================
    void drawHealthPage(const LongevityMonitor& longevity, float voltage, uint16_t rpm) {
        oled_.setTextSize(1);

        // Stator status
        oled_.setCursor(0, 0);
        oled_.print(F("STATOR:"));
        oled_.print(longevity.getStatorStatusText());

        // Stator voltage
        oled_.setCursor(0, 10);
        oled_.print(F("V:"));
        oled_.print(longevity.getStatorVoltage(), 1);
        oled_.print(F("V"));

        // Battery SOC
        oled_.setCursor(0, 22);
        oled_.print(F("BATT:"));
        oled_.print(longevity.getBatterySOCText());
        oled_.print(F(" "));
        oled_.print(longevity.getBatteryPercent());
        oled_.print(F("%"));

        // Battery voltage
        oled_.setCursor(0, 32);
        oled_.print(F("Vbatt:"));
        oled_.print(voltage, 2);
        oled_.print(F("V"));

        // Runtime
        oled_.setCursor(0, 44);
        oled_.print(F("RUN:"));
        unsigned long mins = longevity.getEngineRuntimeMin();
        oled_.print(mins / 60);
        oled_.print(F("h"));
        oled_.print(mins % 60);
        oled_.print(F("m"));
    }

    // ============================================================
    // Page 2: Maintenance Status
    // ============================================================
    void drawMaintPage(const LongevityMonitor& longevity) {
        oled_.setTextSize(1);
        oled_.setCursor(0, 0);
        oled_.print(F("MAINTENANCE"));

        for (int i = 0; i < MAINT_COUNT; i++) {
            uint8_t y = 11 + i * 9;
            if (y > 54) break;  // Screen full

            oled_.setCursor(0, y);

            // Flash overdue items
            if (longevity.isMaintenanceOverdue((MaintID)i)) {
                if ((millis() / 500) % 2 == 0) {
                    oled_.print(F("! "));
                } else {
                    oled_.print(F("  "));
                }
            } else {
                oled_.print(F("  "));
            }

            // Abbreviated name (max 8 chars)
            const char* names[] = {"OIL", "VALVE", "FILTER", "SPARK", "CHAIN", "TIRES"};
            oled_.print(names[i]);

            // km until next service
            float km_until = longevity.getKmUntilMaintenance((MaintID)i);
            oled_.setCursor(56, y);
            if (km_until < 0) {
                oled_.print(F("OVERDUE"));
            } else {
                oled_.print((int)km_until);
                oled_.print(F("km"));
            }
        }
    }

    // ============================================================
    // Page 3: Trip Info
    // ============================================================
    void drawTripPage(const LongevityMonitor& longevity, uint16_t rpm) {
        oled_.setTextSize(1);

        // Odometer + Runtime
        oled_.setCursor(0, 0);
        oled_.print(F("ODO:"));
        oled_.print(longevity.getTotalOdometerKm());
        oled_.print(F("km"));

        // Trip distance
        oled_.setCursor(0, 12);
        oled_.print(F("TRIP:"));
        oled_.print(longevity.getCurrentTripKm(), 1);
        oled_.print(F("km"));

        // Peak temperature
        oled_.setCursor(0, 24);
        oled_.print(F("PEAK:"));
        oled_.print((int)longevity.getTempPeak());
        oled_.print(F("C"));

        // Temp trend
        oled_.setCursor(0, 36);
        oled_.print(F("TREND:"));
        oled_.print(longevity.isTempTrendRising() ? "UP!" : "OK");

        // Current RPM
        oled_.setCursor(64, 0);
        oled_.print(F("RPM:"));
        oled_.print(rpm);

        // Stator status summary
        oled_.setCursor(0, 48);
        oled_.print(F("STA:"));
        oled_.print(longevity.getStatorStatusText());

        oled_.setCursor(64, 48);
        oled_.print(F("BAT:"));
        oled_.print(longevity.getBatterySOCText());
    }

    // ============================================================
    // Mode Splash (shown briefly after mode switch)
    // ============================================================
    void drawModeSplash(RideMode mode) {
        // Big mode name for readability
        oled_.setTextSize(2);
        oled_.setCursor(4, 4);
        oled_.print(MODE_NAMES[mode]);

        oled_.setTextSize(1);
        oled_.setCursor(4, 25);
        oled_.print(F("IGN:"));
        int8_t off = MODE_PARAMS[mode].ignition_offset;
        if (off >= 0) oled_.print(F("+"));
        oled_.print(off);
        oled_.print(F("d  "));

        // v2.1: Show CDI map (A/B/C)
        oled_.print(F("MAP:"));
        const char map_chars[] = {'A', 'B', 'C'};
        oled_.print(map_chars[MODE_PARAMS[mode].cdi_map]);

        oled_.setCursor(4, 37);
        oled_.print(F("V:"));
        oled_.print(MODE_PARAMS[mode].valve_percent);
        oled_.print(F("% A:"));
        oled_.print(MODE_PARAMS[mode].airbox_percent);
        oled_.print(F("%"));

        // Throttle curve
        oled_.setCursor(4, 49);
        const char* curve_name[] = {"LINEAR", "PROGR", "AGGR", "SOFT"};
        oled_.print(F("THR:"));
        oled_.print(curve_name[MODE_PARAMS[mode].throttle_curve]);
    }

    // ============================================================
    // Alert Bar (bottom of screen)
    // ============================================================
    void drawAlertBar(bool temp_warn, bool volt_warn, bool oil_warn, bool stator_warn) {
        oled_.setCursor(0, 56);
        oled_.setTextSize(1);

        if ((millis() / 300) % 2 == 0) {
            if (temp_warn)   oled_.print(F("TEMP! "));
            if (volt_warn)   oled_.print(F("BATT! "));
            if (oil_warn)    oled_.print(F("OIL! "));
            if (stator_warn) oled_.print(F("STR! "));
        }
    }
};