#pragma once
// ============================================================
// African Queen Lite — Mode Transition Manager v2.3
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.3: NEW — Smooth transitions between ride modes.
// Instead of instantly snapping exhaust valve/airbox/CDI settings,
// this module interpolates between old and new mode parameters
// over a configurable transition time (default: 1.5s).
//
// This prevents:
//   - Jerky servo movements (exhaust valve snapping open/closed)
//   - Abrupt CDI map changes (can cause hesitation)
//   - Sudden throttle response changes (unsettling while riding)
//
// Transition behavior:
//   - Exhaust valve: smooth sweep over transition_time_ms
//   - Airbox flap: smooth sweep over transition_time_ms
//   - CDI map: instant change (required for engine safety)
//   - LED color: instant change (visual feedback)
//   - Idle target: smooth transition
//   - Sweep rate during transition: faster than mode default for responsiveness

#include "modes.h"
#include <Arduino.h>

// ---- Transition Configuration ----
constexpr unsigned long TRANSITION_TIME_MS     = 1500;  // 1.5s transition time
constexpr unsigned long TRANSITION_UPDATE_MS   = 20;    // 50Hz update rate
constexpr uint8_t TRANSITION_STEPS             = 75;    // Steps in transition (1500/20)

class ModeTransition {
public:
    ModeTransition() : active_(false), from_mode_(MODE_STRASSE),
                       to_mode_(MODE_STRASSE), start_ms_(0),
                       current_valve_pct_(0), current_airbox_pct_(0),
                       last_update_ms_(0), transition_progress_(0.0f) {}

    void begin() {
        active_ = false;
        Serial.println("[TRANSITION] Smooth mode transition manager initialized");
    }

    // Start a transition from one mode to another
    // current_valve/airbox: current servo positions (0-100)
    void start(RideMode from, RideMode to, uint8_t current_valve, uint8_t current_airbox) {
        from_mode_ = from;
        to_mode_ = to;
        current_valve_pct_ = current_valve;
        current_airbox_pct_ = current_airbox;
        start_ms_ = millis();
        last_update_ms_ = start_ms_;
        active_ = true;
        transition_progress_ = 0.0f;

        Serial.printf("[TRANSITION] %s → %s (valve: %d→%d, airbox: %d→%d)\n",
            MODE_NAMES[from], MODE_NAMES[to],
            current_valve, MODE_PARAMS[to].valve_percent,
            current_airbox, MODE_PARAMS[to].airbox_percent);
    }

    // Call in main loop — returns true if transition is active
    bool update(uint8_t& out_valve, uint8_t& out_airbox) {
        if (!active_) return false;

        unsigned long now = millis();
        unsigned long elapsed = now - start_ms_;

        if (elapsed >= TRANSITION_TIME_MS) {
            // Transition complete — snap to target values
            out_valve = MODE_PARAMS[to_mode_].valve_percent;
            out_airbox = MODE_PARAMS[to_mode_].airbox_percent;
            active_ = false;
            Serial.printf("[TRANSITION] Complete → %s (valve=%d, airbox=%d)\n",
                MODE_NAMES[to_mode_], out_valve, out_airbox);
            return false;
        }

        // Calculate progress (0.0 to 1.0) with ease-in-out
        float t = (float)elapsed / (float)TRANSITION_TIME_MS;
        transition_progress_ = easeInOutCubic(t);

        // Interpolate valve position
        float target_valve = MODE_PARAMS[to_mode_].valve_percent;
        float from_valve = (float)current_valve_pct_;
        out_valve = (uint8_t)(from_valve + (target_valve - from_valve) * transition_progress_);

        // Interpolate airbox position
        float target_airbox = MODE_PARAMS[to_mode_].airbox_percent;
        float from_airbox = (float)current_airbox_pct_;
        out_airbox = (uint8_t)(from_airbox + (target_airbox - from_airbox) * transition_progress_);

        return true;
    }

    // Check if transition is currently active
    bool isActive() const { return active_; }

    // Get progress (0.0 to 1.0)
    float getProgress() const { return transition_progress_; }

    // Get target mode
    RideMode getTargetMode() const { return to_mode_; }

    // Get source mode
    RideMode getSourceMode() const { return from_mode_; }

    // Force-cancel transition (snap to target)
    void cancel() {
        active_ = false;
        transition_progress_ = 1.0f;
    }

private:
    bool active_;
    RideMode from_mode_;
    RideMode to_mode_;
    unsigned long start_ms_;
    uint8_t current_valve_pct_;
    uint8_t current_airbox_pct_;
    unsigned long last_update_ms_;
    float transition_progress_;

    // Ease-in-out cubic for smooth start/stop
    // t = [0, 1], returns [0, 1]
    static float easeInOutCubic(float t) {
        return t < 0.5f
            ? 4.0f * t * t * t
            : 1.0f - powf(-2.0f * t + 2.0f, 3.0f) / 2.0f;
    }
};
