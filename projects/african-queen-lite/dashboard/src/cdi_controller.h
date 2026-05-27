#pragma once
// ============================================================
// African Queen Lite — CDI Ignition Timing Controller
// Honda NX650 Dominator RFVC
// ============================================================
//
// This module controls the ignition timing offset based on the
// active ride mode. It does NOT generate spark directly — instead
// it communicates with a programmable CDI (Ignitech DC-CDI-P2)
// via a digital output that selects between two pre-programmed
// timing maps (Map A = base, Map B = advanced/retarded).
//
// SAFETY: The NX650 has no ECU — just a CDI box. We switch between
// two CDI maps using a single GPIO. If the CDI is not programmable,
// we can only indicate the recommended timing; no actual control.
//
// For future DIY CDI: Teensy 4.0 + Quadspark expansion module
// would be needed for real-time ignition control.

#include "modes.h"
#include <Arduino.h>

class CDIController {
public:
    CDIController() : current_map_(0), initialized_(false) {}

    void begin() {
        pinMode(Pin::CDI_MAP_SELECT, OUTPUT);
        // Default to Map A (base timing)
        digitalWrite(Pin::CDI_MAP_SELECT, LOW);
        current_map_ = 0;
        initialized_ = true;
        Serial.println("[CDI] Initialized — Map A (base timing) active");
    }

    // Called when ride mode changes
    void setMode(RideMode mode) {
        // Determine which CDI map to select based on ignition offset
        // Map A (LOW) = retarded/eco timing (negative offset)
        // Map B (HIGH) = advanced/sport timing (positive offset)
        int8_t offset = MODE_PARAMS[mode].ignition_offset;

        if (offset <= 0) {
            // Eco/Comfort/Street — base or retarded timing
            selectMapA();
        } else {
            // Sport/Gelände/Sound — advanced timing
            selectMapB();
        }

        Serial.printf("[CDI] Mode %s — Map %c (offset %+d°)\n",
            MODE_NAMES[mode],
            current_map_ == 0 ? 'A' : 'B',
            offset);
    }

    // Force Map A (safe/base timing)
    void selectMapA() {
        digitalWrite(Pin::CDI_MAP_SELECT, LOW);
        current_map_ = 0;
    }

    // Force Map B (advanced timing)
    void selectMapB() {
        digitalWrite(Pin::CDI_MAP_SELECT, HIGH);
        current_map_ = 1;
    }

    uint8_t getCurrentMap() const { return current_map_; }

    // Calculate RPM-dependent timing advance (for future DIY CDI)
    // Returns ignition angle in degrees BTDC
    float calculateAdvance(uint16_t rpm, RideMode mode) const {
        int8_t base_offset = MODE_PARAMS[mode].ignition_offset;

        // NX650 RFVC base timing: ~10° BTDC at idle, advancing to ~32° BTDC at peak
        // This is a simplified linear advance curve
        float base_advance = 10.0f;

        if (rpm > 1500) {
            // Linear advance from 1500 to 6000 RPM
            float rpm_factor = min((float)(rpm - 1500) / 4500.0f, 1.0f);
            base_advance += rpm_factor * 22.0f;  // Up to 32° at 6000 RPM
        }

        // Apply mode-specific offset
        float advance = base_advance + (float)base_offset;

        // Clamp to safe range
        advance = constrain(advance, 5.0f, 40.0f);

        return advance;
    }

private:
    uint8_t current_map_;  // 0 = Map A, 1 = Map B
    bool initialized_;
};