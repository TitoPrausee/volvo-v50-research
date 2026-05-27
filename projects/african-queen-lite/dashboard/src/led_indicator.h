#pragma once
// ============================================================
// African Queen Lite — LED Mode Indicator (WS2812 RGB) v2.0
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.0: Added stator health indicator (yellow blink for degraded,
// red/yellow alternating for failing).
// Mode colors unchanged.

#include "modes.h"
#include <Adafruit_NeoPixel.h>

class LEDIndicator {
public:
    LEDIndicator() : strip_(1, Pin::LED_DATA, NEO_GRB + NEO_KHZ800),
                     initialized_(false), brightness_(80),
                     current_mode_(MODE_STRASSE),
                     alert_active_(false), alert_toggle_(false),
                     last_toggle_ms_(0) {}

    void begin() {
        strip_.begin();
        strip_.setBrightness(brightness_);
        strip_.show();  // All pixels off

        initialized_ = true;

        // Startup animation: cycle through mode colors
        for (int i = 0; i < MODE_COUNT; i++) {
            ModeColor c = MODE_COLORS[i];
            strip_.setPixelColor(0, strip_.Color(c.r, c.g, c.b));
            strip_.show();
            delay(150);
        }
        // Set to default mode
        setMode(MODE_STRASSE);
        Serial.println("[LED] WS2812 initialized — Mode STRASSE (green)");
    }

    void setMode(RideMode mode) {
        current_mode_ = mode;
        if (!alert_active_) {
            ModeColor c = MODE_COLORS[mode];
            strip_.setPixelColor(0, strip_.Color(c.r, c.g, c.b));
            strip_.show();
        }
    }

    // Alert: rapid flash red for critical conditions
    void setAlert(bool active) {
        alert_active_ = active;
        if (!active) {
            // Restore mode color
            ModeColor c = MODE_COLORS[current_mode_];
            strip_.setPixelColor(0, strip_.Color(c.r, c.g, c.b));
            strip_.show();
        }
    }

    // Set stator health indicator (yellow for degraded)
    void setStatorWarning(bool degraded) {
        if (degraded && !alert_active_) {
            // Slow yellow pulse for stator degradation
            unsigned long now = millis();
            if ((now / 1000) % 2 == 0) {
                strip_.setPixelColor(0, strip_.Color(255, 200, 0));  // Yellow
            } else {
                ModeColor c = MODE_COLORS[current_mode_];
                strip_.setPixelColor(0, strip_.Color(c.r / 2, c.g / 2, c.b / 2));
            }
            strip_.show();
        }
    }

    // Call regularly for alert flashing
    void update() {
        if (!initialized_) return;

        if (alert_active_) {
            unsigned long now = millis();
            if (now - last_toggle_ms_ > 200) {  // Flash at 2.5Hz
                alert_toggle_ = !alert_toggle_;
                if (alert_toggle_) {
                    strip_.setPixelColor(0, strip_.Color(255, 0, 0));  // RED
                } else {
                    strip_.setPixelColor(0, strip_.Color(0, 0, 0));    // OFF
                }
                strip_.show();
                last_toggle_ms_ = now;
            }
        }
    }

    void setBrightness(uint8_t b) {
        brightness_ = constrain(b, 10, 255);
        strip_.setBrightness(brightness_);
        strip_.show();
    }

private:
    Adafruit_NeoPixel strip_;
    bool initialized_;
    uint8_t brightness_;
    RideMode current_mode_;
    bool alert_active_;
    bool alert_toggle_;
    unsigned long last_toggle_ms_;
};