#pragma once
// ============================================================
// African Queen Lite — CDI Ignition Timing Controller v2.0
// Honda NX650 Dominator RFVC
// ============================================================
//
// This module controls the ignition timing offset based on the
// active ride mode. It does NOT generate spark directly — instead
// it communicates with a programmable CDI (Ignitech DC-CDI-P2)
// via a digital output that selects between two pre-programmed
// timing maps (Map A = base, Map B = advanced/retarded).
//
// v2.0: Added 3-position mode control for better map granularity.
//   GPIO 27 → CDI_MAP_A (active low = Map A / base)
//   GPIO 33 → CDI_MAP_B (active low = Map B / sport)
//   Both HIGH = Map C / fallback (standard timing)
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

    // Get ignition offset for current mode
    int8_t getIgnitionOffset(RideMode mode) const {
        return MODE_PARAMS[mode].ignition_offset;
    }

private:
    uint8_t current_map_;  // 0=Map A (base), 1=Map B (advanced)
    bool initialized_;
};