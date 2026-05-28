#pragma once
// ============================================================
// African Queen Lite — Auto RPM Valve Controller v2.3
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.3: Dedicated airbox RPM curves (AIRBOX_CURVES in modes.h).
//       Previously airbox was derived proportionally from valve curves,
//       now has its own independent RPM mapping.
//       Added calculateAirboxFromCurve() for proper airbox control.
//
// v2.2: Auto-RPM exhaust valve position.
// Instead of a fixed valve_percent, the exhaust valve position
// follows an RPM-based curve per mode. This gives much better
// throttle response and sound character across the rev range.
//
// When ENABLE_AUTO_RPM_VALVE is defined:
//   - Valve position is interpolated from VALVE_CURVES[mode]
//   - Airbox position is interpolated from AIRBOX_CURVES[mode]
//   - At each loop iteration, valve target = curve(current_rpm)
//   - The sweep_rate still controls how fast the valve moves
//   - The base valve_percent from MODE_PARAMS is used as fallback
//     if RPM is unknown (engine off / RPM = 0)

#include "modes.h"
#include <Arduino.h>

class AutoRPMValve {
public:
    AutoRPMValve() : enabled_(true), last_valve_pos_(50),
                     last_airbox_pos_(0), last_rpm_(0) {}

    void begin() {
        Serial.println("[AUTO_VALVE] RPM-based valve+airbox control initialized v2.3");
        Serial.printf("[AUTO_VALVE] %d valve curves + %d airbox curves loaded\n",
            MODE_COUNT, MODE_COUNT);
    }

    // Calculate exhaust valve position for current RPM in given mode
    // Returns 0-100% valve position
    uint8_t calculatePosition(RideMode mode, uint16_t rpm) {
        if (!enabled_) {
            return MODE_PARAMS[mode].valve_percent;  // Fallback to static
        }

        // Engine off → use base position
        if (rpm < RPM_IDLE_COLD) {
            return MODE_PARAMS[mode].valve_percent;
        }

        return interpolateCurve(VALVE_CURVES[mode], rpm);
    }

    // Calculate airbox flap position for current RPM in given mode
    // v2.3: Now uses dedicated AIRBOX_CURVES instead of proportional scaling
    // Returns 0-100% airbox position
    uint8_t calculateAirboxPosition(RideMode mode, uint16_t rpm) {
        if (!enabled_) {
            return MODE_PARAMS[mode].airbox_percent;  // Fallback to static
        }

        // Engine off → use base position
        if (rpm < RPM_IDLE_COLD) {
            return MODE_PARAMS[mode].airbox_percent;
        }

        return interpolateCurve(AIRBOX_CURVES[mode], rpm);
    }

    void setEnabled(bool en) {
        enabled_ = en;
        Serial.printf("[AUTO_VALVE] RPM-based control %s\n", en ? "ENABLED" : "DISABLED");
    }

    bool isEnabled() const { return enabled_; }

    // Get rev limiter ignition offset for current RPM
    // Returns additional ignition retard (negative degrees) for soft-cut
    // Returns 0 when below soft-cut threshold
    int8_t getRevLimiterRetard(RideMode mode, uint16_t rpm) {
        const RevLimiterParams& limiter = REV_LIMITERS[mode];

        if (rpm < limiter.soft_cut_rpm) {
            return 0;  // Below soft-cut — no retard
        }

        if (rpm >= limiter.hard_cut_rpm) {
            return limiter.max_retard_deg;  // Full retard
        }

        // Progressive retard between soft_cut and hard_cut
        float fraction = (float)(rpm - limiter.soft_cut_rpm) /
                         (float)(limiter.hard_cut_rpm - limiter.soft_cut_rpm);
        int8_t retard = (int8_t)(limiter.max_retard_deg * fraction);
        return constrain(retard, limiter.max_retard_deg, 0);
    }

    // Check if RPM is at hard limit (no spark)
    bool isHardLimit(RideMode mode, uint16_t rpm) {
        return rpm >= REV_LIMITERS[mode].hard_limit_rpm;
    }

private:
    bool enabled_;
    uint8_t last_valve_pos_;
    uint8_t last_airbox_pos_;
    uint16_t last_rpm_;

    // Generic curve interpolation — works for both VALVE_CURVES and AIRBOX_CURVES
    static uint8_t interpolateCurve(const ValveCurve& curve, uint16_t rpm) {
        // If RPM is below first point → use first point value
        if (rpm <= curve.points[0].rpm) {
            return curve.points[0].position;
        }

        // If RPM is above last point → use last point value
        if (rpm >= curve.points[curve.num_points - 1].rpm) {
            return curve.points[curve.num_points - 1].position;
        }

        // Find the two points we're between
        for (uint8_t i = 0; i < curve.num_points - 1; i++) {
            if (rpm >= curve.points[i].rpm && rpm <= curve.points[i + 1].rpm) {
                // Linear interpolation
                uint16_t rpm_range = curve.points[i + 1].rpm - curve.points[i].rpm;
                uint16_t rpm_offset = rpm - curve.points[i].rpm;
                uint8_t pos_range = (int8_t)curve.points[i + 1].position - (int8_t)curve.points[i].position;

                float fraction = (float)rpm_offset / (float)rpm_range;
                float position = curve.points[i].position + (pos_range * fraction);

                return constrain((uint8_t)position, 0, 100);
            }
        }

        // Shouldn't reach here
        return 50;
    }
};