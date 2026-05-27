#pragma once
// ============================================================
// African Queen Lite — Exhaust Valve Control
// Honda NX650 Dominator RFVC
// ============================================================
//
// Controls an exhaust valve (EXUP-style) via servo or gearmotor.
// Position is set as a percentage: 0% = fully closed, 100% = fully open.
//
// Hardware options:
//   1. RC Servo (MG996R) — simple but vibration/heat sensitive
//   2. 12V Gearmotor + AS5600 magnetic encoder — robust, recommended
//   3. DRV8833 H-bridge + PID — for gearmotor option
//
// For initial build, we use standard RC servo PWM (50Hz).
// Future upgrade: swap to gearmotor + AS5600 + PID.

#include "modes.h"
#include <ESP32Servo.h>

class ExhaustValve {
public:
    ExhaustValve() : position_percent_(0), target_percent_(0),
                     servo_(), attached_(false), smooth_step_(true) {}

    void begin() {
        servo_.setPeriodHertz(SERVO_FREQ_HZ);
        attached_ = servo_.attach(Pin::EXHAUST_VALVE, SERVO_MIN_US, SERVO_MAX_US);
        if (!attached_) {
            Serial.println("[EXHAUST] ERROR: Failed to attach servo!");
            return;
        }
        // Start at 50% (half-open, safe default)
        setImmediate(50);
        Serial.println("[EXHAUST] Servo initialized — default 50%");
    }

    // Called when ride mode changes — sets target position
    void setMode(RideMode mode) {
        uint8_t target = MODE_PARAMS[mode].valve_percent;
        setTarget(target);
        Serial.printf("[EXHAUST] Mode %s → Valve %d%%\n",
            MODE_NAMES[mode], target);
    }

    // Set target position (0-100%)
    void setTarget(uint8_t percent) {
        target_percent_ = constrain(percent, 0, 100);
    }

    // Set position immediately (no smooth transition)
    void setImmediate(uint8_t percent) {
        target_percent_ = constrain(percent, 0, 100);
        position_percent_ = target_percent_;
        applyPosition();
    }

    // Call in main loop for smooth position transitions
    void update() {
        if (!attached_) return;

        if (smooth_step_ && position_percent_ != target_percent_) {
            // Smooth transition: move 1% per update cycle
            if (position_percent_ < target_percent_) {
                position_percent_++;
            } else {
                position_percent_--;
            }
            applyPosition();
        } else if (!smooth_step_ && position_percent_ != target_percent_) {
            position_percent_ = target_percent_;
            applyPosition();
        }
    }

    uint8_t getPosition() const { return position_percent_; }
    uint8_t getTarget()    const { return target_percent_; }
    bool isAttached()      const { return attached_; }

    // Emergency: fully open exhaust valve (maximum flow, safest)
    void emergencyOpen() {
        setImmediate(100);
        Serial.println("[EXHAUST] EMERGENCY — Valve forced fully open");
    }

    // Emergency: fully close exhaust valve (quietest mode)
    void emergencyClose() {
        setImmediate(0);
        Serial.println("[EXHAUST] EMERGENCY — Valve forced fully closed");
    }

private:
    uint8_t position_percent_;  // Current position 0-100
    uint8_t target_percent_;     // Target position 0-100
    Servo servo_;
    bool attached_;
    bool smooth_step_;

    void applyPosition() {
        if (!attached_) return;
        // Map 0-100% to servo angle 0-180°
        uint8_t angle = map(position_percent_, 0, 100, 0, 180);
        servo_.write(angle);
    }
};