#pragma once
// ============================================================
// African Queen Lite — Fuel Estimation v2.2
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.2: NEW — Fuel consumption estimation per ride mode.
// NX650 stock fuel consumption: ~3.5L/100km (mixed riding)
// Per mode estimates based on riding style impact.
//
// Tank: 16L total, ~3.4L reserve
// Reserve warning at ~3.4L remaining, critical at ~1.5L

#include "modes.h"
#include <Arduino.h>

class FuelEstimator {
public:
    FuelEstimator() : fuel_ml_(16000), fuel_low_warned_(false),
                      fuel_critical_warned_(false),
                      distance_m_x10_(0), last_fuel_calc_ms_(0),
                      fuel_consumed_ml_(0), current_rate_ml_per_100km_(0) {}

    void begin() {
        // Start with full tank (16L = 16000 mL)
        fuel_ml_ = NX650_TANK_CAPACITY_L * 1000.0f;
        Serial.printf("[FUEL] Initialized — %.1fL in tank\\n", fuel_ml_ / 1000.0f);
    }

    // Call periodically (every FUEL_CALC_MS)
    // distance_m_x10: distance traveled in decimeters since last call
    // current_mode: active ride mode for consumption estimation
    void update(float distance_km, RideMode current_mode, uint16_t rpm) {
        if (distance_km <= 0.001f) return;  // No distance = no consumption

        // Get mode-specific fuel consumption
        float base_ml_per_100km = MODE_PARAMS[current_mode].fuel.ml_per_100km;

        // RPM adjustment: higher RPM = more fuel
        // At idle (1300 RPM): ~0.5L/h = ~30mL/100km at standstill
        // At cruise (4500 RPM): base rate
        // At high RPM (6500+): +20-30% consumption
        float rpm_factor = 1.0f;
        if (rpm > 6500) {
            rpm_factor = 1.25f;  // +25% at high RPM
        } else if (rpm > 5500) {
            rpm_factor = 1.10f;  // +10% at mid-high RPM
        } else if (rpm < 1500) {
            rpm_factor = 0.70f;  // -30% at idle/crawl
        }

        float effective_rate = base_ml_per_100km * rpm_factor;
        current_rate_ml_per_100km_ = effective_rate;

        // Calculate fuel consumed for this distance segment
        float consumed_ml = (effective_rate / 100.0f) * distance_km;
        fuel_consumed_ml_ += consumed_ml;
        fuel_ml_ -= consumed_ml;

        // Prevent negative fuel
        if (fuel_ml_ < 0) fuel_ml_ = 0;
    }

    // Set current fuel level manually (e.g., after refueling)
    void setFuelLevel(float liters) {
        fuel_ml_ = constrain(liters * 1000.0f, 0, NX650_TANK_CAPACITY_L * 1000.0f);
        fuel_low_warned_ = false;
        fuel_critical_warned_ = false;
        Serial.printf("[FUEL] Level set: %.1fL\\n", liters);
    }

    // Refuel: add fuel to current level
    void refuel(float liters) {
        fuel_ml_ += liters * 1000.0f;
        if (fuel_ml_ > NX650_TANK_CAPACITY_L * 1000.0f) {
            fuel_ml_ = NX650_TANK_CAPACITY_L * 1000.0f;
        }
        fuel_low_warned_ = false;
        fuel_critical_warned_ = false;
        Serial.printf("[FUEL] Refueled %.1fL — total: %.1fL\\n", liters, fuel_ml_ / 1000.0f);
    }

    // Get estimated fuel remaining in liters
    float getFuelLiters() const { return fuel_ml_ / 1000.0f; }

    // Get estimated range (km) based on current mode consumption
    float getEstimatedRange(RideMode mode) const {
        if (current_rate_ml_per_100km_ <= 0) return 0;
        // Range = remaining fuel / (consumption per km)
        float liters_for_100km = current_rate_ml_per_100km_ / 1000.0f;
        if (liters_for_100km <= 0) return 0;
        return (fuel_ml_ / 1000.0f) / liters_for_100km * 100.0f;
    }

    // Get current consumption rate (mL/100km)
    float getCurrentRate() const { return current_rate_ml_per_100km_; }

    // Fuel warning checks
    bool isLowFuel() const {
        return fuel_ml_ <= (MODE_PARAMS[MODE_STRASSE].fuel.reserve_l * 1000.0f);
    }

    bool isCriticalFuel() const {
        return fuel_ml_ <= 1500.0f;  // 1.5L critical
    }

    // Percentage of tank remaining
    uint8_t getFuelPercent() const {
        return (uint8_t)((fuel_ml_ / (NX650_TANK_CAPACITY_L * 1000.0f)) * 100.0f);
    }

    // Total fuel consumed since last reset (mL)
    float getTotalConsumed() const { return fuel_consumed_ml_; }

private:
    float  fuel_ml_;                  // Current fuel in mL
    bool   fuel_low_warned_;           // Low fuel warning issued
    bool   fuel_critical_warned_;      // Critical fuel warning issued
    float  distance_m_x10_;           // Distance accumulator (decimeters)
    unsigned long last_fuel_calc_ms_;   // Last calculation timestamp
    float  fuel_consumed_ml_;          // Total mL consumed since reset
    float  current_rate_ml_per_100km_; // Current consumption rate
};