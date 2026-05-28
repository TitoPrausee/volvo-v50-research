#pragma once
// ============================================================
// African Queen Lite — Config Mode v2.2
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.2: NEW — Configuration menu for on-bike settings.
// Long press encoder (3 sec) enters config mode.
// Encoder rotates navigate between settings, press to change.
// Auto-exits after 10 seconds of inactivity.
//
// Settings:
//   1. LED Brightness (10-255)
//   2. Exhaust Valve Calibration (min/max endpoints)
//   3. Airbox Flap Calibration (min/max endpoints)
//   4. Ride Mode Select (direct jump to any mode)
//   5. Exit Config

#include "modes.h"
#include <Arduino.h>

enum ConfigState : uint8_t {
    CFG_IDLE = 0,        // Normal riding, not in config
    CFG_BRIGHTNESS = 1,  // Adjusting LED brightness
    CFG_VALVE_CAL = 2,   // Calibrating exhaust valve
    CFG_AIRBOX_CAL = 3,  // Calibrating airbox flap
    CFG_MODE_SELECT = 4, // Direct mode selection
    CFG_EXIT = 5,
    CFG_STATE_COUNT = 6
};

class ConfigMode {
public:
    ConfigMode() : state_(CFG_IDLE), last_activity_ms_(0),
                   brightness_(80), valve_min_(0), valve_max_(100),
                   airbox_min_(0), airbox_max_(100),
                   enter_press_ms_(0), in_config_(false) {}

    void begin() {
        state_ = CFG_IDLE;
        in_config_ = false;
        brightness_ = 80;  // Default brightness
        Serial.println("[CONFIG] Ready — long press encoder to enter");
    }

    // Check if currently in config mode
    bool isActive() const { return in_config_; }

    // Get current config state
    ConfigState getState() const { return state_; }

    // Enter config mode (called on long press)
    void enter() {
        in_config_ = true;
        state_ = CFG_BRIGHTNESS;
        last_activity_ms_ = millis();
        Serial.println(F("[CONFIG] Entered config mode — BRIGHTNESS"));
    }

    // Exit config mode
    void exit() {
        in_config_ = false;
        state_ = CFG_IDLE;
        Serial.println(F("[CONFIG] Exited config mode"));
    }

    // Process encoder rotation in config mode
    // direction: +1 = CW, -1 = CCW
    void handleRotate(int8_t direction) {
        if (!in_config_) return;
        last_activity_ms_ = millis();

        switch (state_) {
            case CFG_BRIGHTNESS:
                // Adjust brightness ±10
                brightness_ = constrain(brightness_ + (direction * 10), 10, 255);
                Serial.printf("[CONFIG] Brightness: %d\\n", brightness_);
                break;

            case CFG_VALVE_CAL:
                // Calibrate valve endpoints
                if (direction > 0) {
                    valve_max_ = constrain(valve_max_ + 5, valve_min_ + 10, 100);
                } else {
                    valve_min_ = constrain(valve_min_ - 5, 0, valve_max_ - 10);
                }
                Serial.printf("[CONFIG] Valve: %d-%d%%\\n", valve_min_, valve_max_);
                break;

            case CFG_AIRBOX_CAL:
                // Calibrate airbox endpoints
                if (direction > 0) {
                    airbox_max_ = constrain(airbox_max_ + 5, airbox_min_ + 10, 100);
                } else {
                    airbox_min_ = constrain(airbox_min_ - 5, 0, airbox_max_ - 10);
                }
                Serial.printf("[CONFIG] Airbox: %d-%d%%\\n", airbox_min_, airbox_max_);
                break;

            case CFG_MODE_SELECT:
                // Not used in rotate — press changes mode
                break;

            default:
                break;
        }
    }

    // Process encoder press in config mode
    void handlePress() {
        if (!in_config_) return;
        last_activity_ms_ = millis();

        // Cycle through config states
        state_ = (ConfigState)((state_ + 1) % CFG_STATE_COUNT);

        if (state_ == CFG_EXIT || state_ == CFG_IDLE) {
            exit();
            return;
        }

        const char* state_names[] = {
            "IDLE", "BRIGHTNESS", "VALVE CAL", "AIRBOX CAL", "MODE SELECT", "EXIT"
        };
        Serial.printf("[CONFIG] State: %s\\n", state_names[state_]);
    }

    // Check for auto-exit timeout
    bool checkTimeout() {
        if (!in_config_) return false;
        if (millis() - last_activity_ms_ > CONFIG_TIMEOUT_MS) {
            Serial.println(F("[CONFIG] Timeout — auto-exit"));
            exit();
            return true;
        }
        return false;
    }

    // Process long press detection (3 seconds)
    // Returns true if config mode should be toggled
    bool checkLongPress(bool button_pressed) {
        unsigned long now = millis();
        if (button_pressed) {
            if (enter_press_ms_ == 0) {
                enter_press_ms_ = now;
            } else if ((now - enter_press_ms_) > 3000 && !in_config_) {
                enter_press_ms_ = 0;
                return true;  // Long press detected — enter config
            }
        } else {
            enter_press_ms_ = 0;
        }
        return false;
    }

    // Getters
    uint8_t getBrightness() const { return brightness_; }
    uint8_t getValveMin() const { return valve_min_; }
    uint8_t getValveMax() const { return valve_max_; }
    uint8_t getAirboxMin() const { return airbox_min_; }
    uint8_t getAirboxMax() const { return airbox_max_; }

    const char* getStateName() const {
        static const char* names[] = {
            "IDLE", "BRIGHT", "VALVE", "AIRBOX", "MODE", "EXIT"
        };
        if (state_ >= CFG_STATE_COUNT) return "?";
        return names[state_];
    }

private:
    ConfigState state_;
    unsigned long last_activity_ms_;
    uint8_t brightness_;
    uint8_t valve_min_, valve_max_;
    uint8_t airbox_min_, airbox_max_;
    unsigned long enter_press_ms_;
    bool in_config_;
};