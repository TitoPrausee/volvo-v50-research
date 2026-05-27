#pragma once
// ============================================================
// African Queen Lite — Exhaust Valve Servo Control v2.0
// Honda NX650 Dominator RFVC
// ============================================================
//
// Controls the exhaust valve position via PWM servo.
// Position is set as a percentage: 0% = closed (quiet),
// 100% = fully open (maximum flow, louder).
//
// v2.0: Configurable sweep rate per mode for realistic transitions.
//   - Mode SPORT: fast sweep (sweep_rate=8, near-instant)
//   - Mode COMFORT: slow sweep (sweep_rate=2, gentle transition)
//   - Mode STRASSE: medium sweep (sweep_rate=3)
//
// Hardware: 12V gearmotor + DRV8833 H-bridge + AS5600 angle sensor
// (See RESEARCH.md for details — RC servos NOT suitable for motorcycle!)
// Fallback: if using RC servo (testing only), direct PWM control.

#include "modes.h"
#include <ESP32Servo.h>

class ExhaustValve {
public:
    ExhaustValve() : position_percent_(0), target_percent_(50),
                     sweep_step_(3), attached_(false) {}

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

    void setMode(RideMode mode) {
        uint8_t target = MODE_PARAMS[mode].valve_percent;
        sweep_step_ = MODE_PARAMS[mode].sweep_rate;
        setTarget(target);
        Serial.printf("[EXHAUST] Mode %s → Valve %d%% (sweep=%d)\n",
            MODE_NAMES[mode], target, sweep_step_);
    }

    void setTarget(uint8_t percent) {
        target_percent_ = constrain(percent, 0, 100);
    }

    void setImmediate(uint8_t percent) {
        target_percent_ = constrain(percent, 0, 100);
        position_percent_ = target_percent_;
        applyPosition();
    }

    // Called every main loop iteration — smooth sweep toward target
    void update() {
        if (!attached_) return;

        if (position_percent_ != target_percent_) {
            if (position_percent_ < target_percent_) {
                position_percent_ = position_percent_ + min(sweep_step_, (uint8_t)(target_percent_ - position_percent_));
            } else {
                position_percent_ = position_percent_ - min(sweep_step_, (uint8_t)(position_percent_ - target_percent_));
            }
            applyPosition();
        }
    }

    uint8_t getPosition() const { return position_percent_; }
    uint8_t getTarget()    const { return target_percent_; }
    bool isAttached()      const { return attached_; }

    // Emergency: fully open exhaust valve (maximum flow, safest for cooling)
    void emergencyOpen() {
        sweep_step_ = 10;  // Fast transition for emergency
        setImmediate(100);
        Serial.println("[EXHAUST] EMERGENCY — Valve forced fully open");
    }

    // Emergency: fully close exhaust valve (quietest mode)
    void emergencyClose() {
        sweep_step_ = 10;
        setImmediate(0);
        Serial.println("[EXHAUST] EMERGENCY — Valve forced fully closed");
    }

private:
    uint8_t position_percent_;  // Current position 0-100
    uint8_t target_percent_;     // Target position 0-100
    uint8_t sweep_step_;         // Step size per update cycle (1=slow, 10=instant)
    Servo servo_;
    bool attached_;

    void applyPosition() {
        if (!attached_) return;
        // Map 0-100% to servo angle 0-180°
        uint8_t angle = map(position_percent_, 0, 100, 0, 180);
        servo_.write(angle);
    }
};