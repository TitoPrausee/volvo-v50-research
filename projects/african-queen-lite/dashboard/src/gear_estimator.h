#pragma once
// ============================================================
// African Queen Lite — Gear Estimation v2.2
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.2: NEW — Estimate current gear from RPM vs wheel speed.
//
// The NX650 has no gear position sensor, so we estimate gear
// by comparing known gear ratios with the RPM/speed relationship.
//
// Speed = (RPM * tire_circumference) / (primary_ratio * gear_ratio * final_ratio * 60)
// Rearranged: gear_ratio = (RPM * tire_circ) / (speed_mps * primary * final * 60)
//
// We calculate what the speed would be in each gear at the current RPM,
// then compare with actual speed (from GPS or estimated).
// The closest match = likely current gear.

#include "modes.h"
#include <Arduino.h>

// Confidence threshold for gear detection
constexpr float GEAR_MATCH_TOLERANCE = 0.15f;  // 15% speed difference tolerance

class GearEstimator {
public:
    GearEstimator() : current_gear_(3), confidence_(0), last_gear_ms_(0),
                      estimated_speed_kmh_(0), last_valid_ms_(0), valid_(false) {}

    void begin() {
        current_gear_ = 3;  // Default: 3rd gear (most common for NX650)
        confidence_ = 0;
        Serial.println("[GEAR] Estimator initialized — assuming 3rd gear");
    }

    // Call every sensor update cycle
    // rpm: current engine RPM
    // wheel_speed_kmh_x10: wheel speed in km/h * 10 (from speedometer or GPS)
    void update(uint16_t rpm, uint16_t wheel_speed_kmh_x10) {
        unsigned long now = millis();

        // Need valid RPM and speed
        if (rpm < RPM_IDLE_COLD || wheel_speed_kmh_x10 < 50) {  // < 5.0 km/h
            // Below idle or not moving — keep last gear
            if (now - last_valid_ms_ > 10000) {
                // No valid data for 10s → reset
                valid_ = false;
            }
            return;
        }

        float actual_speed_kmh = wheel_speed_kmh_x10 / 10.0f;

        // Calculate expected speed for each gear at current RPM
        float best_diff = 999.0f;
        uint8_t best_gear = current_gear_;

        for (uint8_t g = 0; g < 5; g++) {
            float expected_speed = calculateSpeed(rpm, g);
            float diff = fabsf(expected_speed - actual_speed_kmh) / actual_speed_kmh;

            if (diff < best_diff) {
                best_diff = diff;
                best_gear = g;
            }
        }

        // Only update gear if confidence is reasonable
        if (best_diff < GEAR_MATCH_TOLERANCE) {
            current_gear_ = best_gear;
            confidence_ = 1.0f - (best_diff / GEAR_MATCH_TOLERANCE);
            confidence_ *= 100.0f;  // Convert to percentage
            valid_ = true;
            last_valid_ms_ = now;
        } else if (valid_) {
            // Gradually decrease confidence
            confidence_ *= 0.95f;
        }
    }

    // Get estimated gear (0-4 = 1st-5th)
    uint8_t getGear() const { return current_gear_; }

    // Get gear name for display
    const char* getGearName() const {
        static const char* gear_names[] = {"N", "1", "2", "3", "4", "5"};
        if (!valid_) return "?";
        if (current_gear_ >= 5) return "?";
        return gear_names[current_gear_ + 1];  // +1 because neutral is [0]
    }

    // Get short gear indicator for OLED (1 char)
    char getGearChar() const {
        if (!valid_) return '?';
        if (current_gear_ >= 5) return '?';
        return '1' + current_gear_;
    }

    // Calculate expected speed in km/h for a given gear at given RPM
    static float calculateSpeed(uint16_t rpm, uint8_t gear) {
        if (gear > 4) return 0;

        float gear_ratio = NX650_GEAR_RATIOS[gear];
        float total_ratio = NX650_PRIMARY_RATIO * gear_ratio * NX650_FINAL_RATIO;

        // Speed = (RPM * tire_circ_m) / (total_ratio * 60) * 3.6  [m/s → km/h]
        float speed_mps = (rpm * NX650_TIRE_CIRC_M) / (total_ratio * 60.0f);
        return speed_mps * 3.6f;  // Convert to km/h
    }

    // Calculate expected RPM for a given gear at given speed (km/h)
    static uint16_t calculateRPM(float speed_kmh, uint8_t gear) {
        if (gear > 4) return 0;

        float gear_ratio = NX650_GEAR_RATIOS[gear];
        float total_ratio = NX650_PRIMARY_RATIO * gear_ratio * NX650_FINAL_RATIO;

        float speed_mps = speed_kmh / 3.6f;
        // RPM = (speed_mps * total_ratio * 60) / tire_circ_m
        return (uint16_t)((speed_mps * total_ratio * 60.0f) / NX650_TIRE_CIRC_M);
    }

    float getConfidence() const { return confidence_; }
    bool isValid() const { return valid_; }

private:
    uint8_t  current_gear_;       // 0=1st, 1=2nd, 2=3rd, 3=4th, 4=5th
    float    confidence_;         // 0-100% confidence in gear estimate
    unsigned long last_gear_ms_;
    float    estimated_speed_kmh_;
    unsigned long last_valid_ms_;
    bool     valid_;
};