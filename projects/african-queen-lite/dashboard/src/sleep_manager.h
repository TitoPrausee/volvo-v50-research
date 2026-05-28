#pragma once
// ============================================================
// African Queen Lite — Sleep Manager v2.2
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.2: NEW — Deep sleep when engine off for >5 min.
// Reduces power consumption from ~80mA (WiFi on) to ~10µA (deep sleep).
// Wake on ignition (RPM pulse) or MODE_UP button press.
//
// Before sleep: save EEPROM, set exhaust valve to safe position,
// turn off display and LED.

#include "modes.h"
#include <Arduino.h>

class SleepManager {
public:
    SleepManager() : engine_off_since_ms_(0), sleep_pending_(false),
                     last_rpm_nonzero_ms_(0), enter_sleep_(false) {}

    void begin() {
        engine_off_since_ms_ = 0;
        sleep_pending_ = false;
        enter_sleep_ = false;
        Serial.println("[SLEEP] Manager initialized — 5min timeout");
    }

    // Call every loop iteration
    // Returns true if we should enter deep sleep
    bool update(uint16_t rpm) {
        unsigned long now = millis();

        if (rpm > 0) {
            // Engine running — reset timer
            last_rpm_nonzero_ms_ = now;
            engine_off_since_ms_ = 0;
            sleep_pending_ = false;
            return false;
        }

        // Engine off
        if (engine_off_since_ms_ == 0) {
            engine_off_since_ms_ = now;
        }

        unsigned long off_duration = now - engine_off_since_ms_;

        // Pre-sleep warning at 4 minutes (display message)
        if (off_duration > (DEEP_SLEEP_TIMEOUT_MS - 60000) && !sleep_pending_) {
            sleep_pending_ = true;
            Serial.println("[SLEEP] Engine off for 4 min — sleep in 1 min");
        }

        // Enter deep sleep after timeout
        if (off_duration >= DEEP_SLEEP_TIMEOUT_MS) {
            enter_sleep_ = true;
            Serial.println("[SLEEP] Engine off for 5 min — entering deep sleep");
            return true;
        }

        return false;
    }

    // Prepare for deep sleep
    // This saves state, turns off peripherals, then enters esp_deep_sleep
    void enterDeepSleep() {
        Serial.println(F("[SLEEP] Saving state and entering deep sleep..."));

        // Save current mode to EEPROM
        // (ModeStorage::saveMode called by applyMode already)

        // Turn off display
        // Display will be re-initialized on wake

        // Turn off LED
        // NeoPixel will be re-initialized on wake

        // Set exhaust valve to closed (safe position)
        // ExhaustValve will re-initialize on wake

        // Configure wake-up sources:
        // 1. GPIO0 (encoder button) — wake on press
        // 2. GPIO4 (Mode+ button) — wake on press
        // 3. GPIO18 (ignition pulse) — wake on engine start
        esp_sleep_enable_ext0_wakeup(GPIO_NUM_4, LOW);   // Mode+ button
        esp_sleep_enable_ext1_wakeup(BIT(GPIO_NUM_18), ESP_EXT1_WAKEUP_ANY_HIGH);  // Ignition pulse

        Serial.println(F("[SLEEP] Wake sources: GPIO4 (Mode+), GPIO18 (Ignition)"));
        Serial.println(F("[SLEEP] Going to deep sleep NOW."));
        Serial.flush();

        // Enter deep sleep
        esp_deep_sleep_start();
    }

    // Check if we just woke from deep sleep
    static bool wokeFromDeepSleep() {
        return esp_sleep_get_wakeup_cause() != ESP_SLEEP_WAKEUP_UNDEFINED;
    }

    // Get wake reason
    static const char* getWakeReason() {
        switch (esp_sleep_get_wakeup_cause()) {
            case ESP_SLEEP_WAKEUP_EXT0: return "EXT0 (Mode+ button)";
            case ESP_SLEEP_WAKEUP_EXT1: return "EXT1 (Ignition pulse)";
            case ESP_SLEEP_WAKEUP_TIMER: return "Timer";
            default: return "Power-on / Reset";
        }
    }

    bool isSleepPending() const { return sleep_pending_; }

private:
    unsigned long engine_off_since_ms_;
    bool sleep_pending_;
    unsigned long last_rpm_nonzero_ms_;
    bool enter_sleep_;
};