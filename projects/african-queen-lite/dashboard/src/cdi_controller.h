#pragma once
// ============================================================
// African Queen Lite — CDI Ignition Timing Controller v2.1
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.1: Full 3-position CDI map control using 2 GPIO pins.
//   GPIO 27 (CDI_MAP_A) + GPIO 33 (CDI_MAP_B):
//     Both LOW            → invalid (don't use)
//     MAP_A LOW, MAP_B HIGH → Map A (eco/retarded timing)
//     MAP_A HIGH, MAP_B LOW → Map B (advanced/sport timing)
//     Both HIGH           → Map C (fallback/standard timing)
//
// Active LOW logic for Ignitech DC-CDI-P2:
//   Map A selected when CDI_MAP_A pin is LOW
//   Map B selected when CDI_MAP_B pin is LOW
//   Fallback when both pins are HIGH (no map selected = default timing)
//
// For future DIY CDI: Teensy 4.0 + Quadspark expansion module
// would be needed for real-time ignition control.

#include "modes.h"
#include <Arduino.h>

class CDIController {
public:
    CDIController() : current_map_(CDI_MAP_A), initialized_(false) {}

    void begin() {
        pinMode(Pin::CDI_MAP_A, OUTPUT);
        pinMode(Pin::CDI_MAP_B, OUTPUT);
        // Default to Map A (base timing)
        selectMap(CDI_MAP_A);
        initialized_ = true;
        Serial.println("[CDI] Initialized — 3-map control: Map A (base timing) active");
        Serial.printf("[CDI] Pins: MAP_A=GPIO%d, MAP_B=GPIO%d\\n", Pin::CDI_MAP_A, Pin::CDI_MAP_B);
    }

    // Called when ride mode changes
    void setMode(RideMode mode) {
        CDIMap target_map = MODE_PARAMS[mode].cdi_map;
        int8_t offset = MODE_PARAMS[mode].ignition_offset;
        selectMap(target_map);

        Serial.printf("[CDI] Mode %s — Map %c (offset %+d°)\\n",
            MODE_NAMES[mode],
            target_map == CDI_MAP_A ? 'A' : (target_map == CDI_MAP_B ? 'B' : 'C'),
            offset);
    }

    // Select a specific CDI map
    void selectMap(CDIMap map) {
        switch (map) {
            case CDI_MAP_A:
                // Map A: Pin A = LOW (active), Pin B = HIGH
                digitalWrite(Pin::CDI_MAP_A, LOW);
                digitalWrite(Pin::CDI_MAP_B, HIGH);
                break;
            case CDI_MAP_B:
                // Map B: Pin A = HIGH, Pin B = LOW (active)
                digitalWrite(Pin::CDI_MAP_A, HIGH);
                digitalWrite(Pin::CDI_MAP_B, LOW);
                break;
            case CDI_MAP_C:
                // Map C (fallback): Both pins HIGH = no selection = standard timing
                digitalWrite(Pin::CDI_MAP_A, HIGH);
                digitalWrite(Pin::CDI_MAP_B, HIGH);
                break;
            default:
                // Invalid → fallback to Map C
                digitalWrite(Pin::CDI_MAP_A, HIGH);
                digitalWrite(Pin::CDI_MAP_B, HIGH);
                break;
        }
        current_map_ = map;
    }

    // Legacy compat: force Map A (safe/base timing)
    void selectMapA() { selectMap(CDI_MAP_A); }

    // Legacy compat: force Map B (advanced timing)
    void selectMapB() { selectMap(CDI_MAP_B); }

    CDIMap getCurrentMap() const { return current_map_; }

    // Get ignition offset for current mode
    int8_t getIgnitionOffset(RideMode mode) const {
        return MODE_PARAMS[mode].ignition_offset;
    }

    // Emergency: revert to Map C (standard timing, safest)
    void emergencyFallback() {
        selectMap(CDI_MAP_C);
        Serial.println("[CDI] EMERGENCY — Fallback to Map C (standard timing)");
    }

private:
    CDIMap current_map_;
    bool initialized_;
};