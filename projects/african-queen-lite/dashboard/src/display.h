#pragma once
// ============================================================
// African Queen Lite — OLED Display (SSD1306 128x64 I2C) v2.0
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.0: Added longevity display pages:
//   Page 0: Main ride display (mode, RPM, temp, voltage)
//   Page 1: Stator health + battery SOC
//   Page 2: Maintenance status (overdue items flash)
//   Page 3: Trip info (odometer, trip distance, peak temp)
//
// Display cycles through pages automatically, or hold Mode- button
// to freeze current page. Short press changes mode, long press
// changes page.

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

class Display {
public:
    Display() : oled_(128, 64, &Wire, -1),
                initialized_(false), show_mode_until_(0),
                current_page_(PAGE_RIDE), page_cycle_ms_(0),
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
        oled_.print(F("Ride Mode Ctrl v2"));
        oled_.setCursor(10, 42);
        oled_.print(F("NX650 RFVC"));
        oled_.setCursor(10, 54);
        oled_.print(F("LONGEVITY+"));
        oled_.display();
        delay(2000);

        Serial.println("[DISPLAY] SSD1306 initialized (128x64 I2C) v2.0");
        return true;
    }

    // Page switching
    void nextPage() {
        current_page_ = (DisplayPage)((current_page_ + 1) % PAGE_COUNT);
        page_cycle_ms_ = millis();  // Reset auto-cycle timer
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

        // Page indicator dot in top-right
        for (uint8_t i = 0; i < PAGE_COUNT; i++) {
            oled_.drawPixel(120 + i * 4, 2, i == current_page_ ? SSD1306_WHITE : SSD1306_BLACK);
        }

        oled_.display();
    }

    // Legacy update (without longevity) for compatibility
    void update(RideMode mode, uint16_t rpm, float temp, float voltage,
                uint8_t valve_pos, uint8_t airbox_pos,
                bool oil_ok, uint8_t cdi_map,
                bool temp_warn, bool volt_warn) {
        // Use static longevity instance for backward compat
        static LongevityMonitor dummy;
        update(mode, rpm, temp, voltage, valve_pos, airbox_pos, oil_ok, cdi_map,
               temp_warn, volt_warn, dummy);
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

    // ============================================================
    // Page 0: Main Ride Display
    // ============================================================
    void drawRidePage(RideMode mode, uint16_t rpm, float temp, float voltage,
                       uint8_t valve_pos, uint8_t airbox_pos,
                       bool oil_ok, uint8_t cdi_map,
                       bool temp_warn, bool volt_warn) {
        // Line 1: Mode + RPM
        oled_.setTextSize(1);
        oled_.setCursor(0, 0);
        oled_.print(MODE_NAMES[mode]);
        oled_.setCursor(72, 0);
        oled_.print(rpm);
        oled_.print(F(" RPM"));

        // Line 2: Temperature + Voltage
        oled_.setCursor(0, 12);
        if (temp_warn) oled_.print(F("!"));
        oled_.print((int)temp);
        oled_.print(F("C"));
        oled_.setCursor(64, 12);
        oled_.print(voltage, 1);
        oled_.print(F("V"));
        if (volt_warn) oled_.print(F("!"));

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
            unsigned long now = millis();
            if ((now / 500) % 2 == 0) oled_.print(F("LOW!"));
            else oled_.print(F("    "));
        }
        oled_.setCursor(64, 36);
        oled_.print(F("MAP:"));
        oled_.print(cdi_map == 0 ? 'A' : 'B');

        // Bottom: throttle curve indicator
        oled_.setCursor(0, 48);
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
        switch (longevity.getStatorStatus()) {
            case STATOR_HEALTHY:   oled_.print(F("OK")); break;
            case STATOR_DEGRADED:  oled_.print(F("WARN")); break;
            case STATOR_FAILING:   oled_.print(F("FAIL!")); break;
            case STATOR_OVERCHARGE: oled_.print(F("OVERV!")); break;
            default:               oled_.print(F("---")); break;
        }

        // Stator voltage
        oled_.setCursor(72, 0);
        if (longevity.getStatorStatus() != STATOR_UNKNOWN) {
            oled_.print(longevity.getStatorVoltage(), 1);
            oled_.print(F("V"));
        }

        // Battery SOC
        oled_.setCursor(0, 14);
        oled_.print(F("BATT:"));
        oled_.print(longevity.getBatterySOCText());
        oled_.setCursor(64, 14);
        oled_.print(voltage, 1);
        oled_.print(F("V"));

        // Battery percentage bar
        uint8_t pct = longevity.getBatteryPercent();
        oled_.setCursor(0, 28);
        oled_.print(F("SOC:"));
        // Draw bar
        oled_.drawRect(28, 28, 100, 8, SSD1306_WHITE);
        oled_.fillRect(29, 29, (pct * 98) / 100, 6, SSD1306_WHITE);

        // RPM and charging status
        oled_.setCursor(0, 42);
        oled_.print(F("RPM:"));
        oled_.print(rpm);
        if (rpm > RPM_IDLE_DEFAULT) {
            oled_.print(F(" > charging"));
        } else {
            oled_.print(F(" (idle)"));
        }

        // Temperature trend
        oled_.setCursor(0, 54);
        oled_.print(F("T PEAK:"));
        oled_.print((int)longevity.getTempPeak());
        oled_.print(F("C"));
        if (longevity.isTempTrendRising()) {
            oled_.print(F(" RISING!"));
        }
    }

    // ============================================================
    // Page 2: Maintenance Status
    // ============================================================
    void drawMaintPage(const LongevityMonitor& longevity) {
        oled_.setTextSize(1);

        oled_.setCursor(0, 0);
        oled_.print(F("MAINTENANCE"));

        // Show maintenance items — overdue items flash
        for (int i = 0; i < min(MAINT_COUNT, (int)4); i++) {
            uint8_t y = 12 + i * 12;
            bool overdue = longevity.isMaintenanceOverdue((MaintID)i);
            float km_left = longevity.getKmUntilMaintenance((MaintID)i);

            oled_.setCursor(0, y);
            if (overdue && (millis() / 400) % 2 == 0) {
                oled_.print(F("*"));
            }
            oled_.print(MAINT_NAMES[i]);
            oled_.setCursor(72, y);
            if (km_left < 0) {
                oled_.print(F("OVERDUE"));
            } else {
                oled_.print((int)km_left);
                oled_.print(F("km"));
            }
        }

        // Remaining items on line 5 if needed
        if (longevity.isAnyMaintenanceOverdue()) {
            oled_.setCursor(0, 54);
            oled_.print(F("! SERVICE NEEDED"));
        }
    }

    // ============================================================
    // Page 3: Trip Info
    // ============================================================
    void drawTripPage(const LongevityMonitor& longevity, uint16_t rpm) {
        oled_.setTextSize(1);

        oled_.setCursor(0, 0);
        oled_.print(F("TRIP INFO"));

        oled_.setCursor(0, 14);
        oled_.print(F("ODO:"));
        oled_.print((unsigned long)longevity.getTotalOdometerKm());
        oled_.print(F("km"));

        oled_.setCursor(0, 26);
        oled_.print(F("TRIP:"));
        oled_.print(longevity.getCurrentTripKm(), 1);
        oled_.print(F("km"));

        oled_.setCursor(0, 38);
        oled_.print(F("PEAK:"));
        oled_.print((int)longevity.getTempPeak());
        oled_.print(F("C"));

        oled_.setCursor(64, 38);
        oled_.print(F("RPM:"));
        oled_.print(rpm);

        // Stator status summary
        oled_.setCursor(0, 52);
        oled_.print(F("STATOR:"));
        oled_.print(longevity.getStatorStatusText());

        oled_.setCursor(72, 52);
        oled_.print(F("BATT:"));
        oled_.print(longevity.getBatterySOCText());
    }

    // ============================================================
    // Mode Splash (shown briefly after mode switch)
    // ============================================================
    void drawModeSplash(RideMode mode) {
        oled_.setTextSize(2);
        oled_.setCursor(4, 10);
        oled_.print(MODE_NAMES[mode]);

        oled_.setTextSize(1);
        oled_.setCursor(4, 35);
        oled_.print(F("IGN:"));
        int8_t off = MODE_PARAMS[mode].ignition_offset;
        if (off >= 0) oled_.print(F("+"));
        oled_.print(off);
        oled_.print(F("d  "));

        oled_.setCursor(4, 47);
        oled_.print(F("V:"));
        oled_.print(MODE_PARAMS[mode].valve_percent);
        oled_.print(F("% A:"));
        oled_.print(MODE_PARAMS[mode].airbox_percent);
        oled_.print(F("%"));
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