#pragma once
// ============================================================
// African Queen Lite — Auto RPM Valve Controller v2.2
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.2: NEW — Auto-RPM exhaust valve position.
// Instead of a fixed valve_percent, the exhaust valve position
// follows an RPM-based curve per mode. This gives much better
// throttle response and sound character across the rev range.
//
// When ENABLE_AUTO_RPM_VALVE is defined:
//   - Valve position is interpolated from VALVE_CURVES[mode]
//   - At each loop iteration, valve target = curve(current_rpm)
//   - The sweep_rate still controls how fast the valve moves
//   - The base valve_percent from MODE_PARAMS is used as fallback
//     if RPM is unknown (engine off / RPM = 0)

#include "modes.h"
#include <Arduino.h>

class AutoRPMValve {
public:
    AutoRPMValve() : enabled_(true), last_position_(50), last_rpm_(0) {}

    void begin() {
        Serial.println("[AUTO_VALVE] RPM-based valve control initialized");
        Serial.printf("[AUTO_VALVE] %d valve curves loaded\\n", MODE_COUNT);
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

        const ValveCurve& curve = VALVE_CURVES[mode];

        // Interpolate between curve points
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

        // Shouldn't reach here, but fallback
        return MODE_PARAMS[mode].valve_percent;
    }

    // Same for airbox — uses the same curve but with airbox percentages
    // Each mode has its own valve_percent and airbox_percent,
    // and the RPM curve scales them proportionally
    uint8_t calculateAirboxPosition(RideMode mode, uint16_t rpm) {
        // Airbox follows valve curve but scaled by airbox_percent/valve_percent ratio
        uint8_t valve_pos = calculatePosition(mode, rpm);
        uint8_t valve_base = MODE_PARAMS[mode].valve_percent;
        uint8_t airbox_base = MODE_PARAMS[mode].airbox_percent;

        if (valve_base == 0) return airbox_base;  // Avoid division by zero

        float ratio = (float)airbox_base / (float)valve_base;
        return constrain((uint8_t)(valve_pos * ratio), 0, 100);
    }

    void setEnabled(bool en) {
        enabled_ = en;
        Serial.printf("[AUTO_VALVE] RPM-based control %s\\n", en ? "ENABLED" : "DISABLED");
    }

    bool isEnabled() const { return enabled_; }

private:
    bool enabled_;
    uint8_t last_position_;
    uint16_t last_rpm_;
};