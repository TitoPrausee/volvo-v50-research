#pragma once
// ============================================================
// African Queen Lite — Airbox Resonance Flap Control v2.0
// Honda NX650 Dominator RFVC
// ============================================================
//
// Controls the airbox intake resonance flap via servo.
// Position: 0% = snorkel closed (quiet), 100% = fully open (max flow).
//
// v2.0: Configurable sweep rate per mode (same as exhaust valve).
// Smooth transitions in COMFORT/STADT, fast in SPORT/GELÄNDE.
//
// Hardware: standard RC servo (50Hz PWM) via ESP32Servo.
// Production: gearmotor + AS5600 (same as exhaust valve).

#include "modes.h"
#include <ESP32Servo.h>

class AirboxFlap {
public:
    AirboxFlap() : position_percent_(0), target_percent_(0),
                   sweep_step_(3), attached_(false) {}

    void begin() {
        servo_.setPeriodHertz(SERVO_FREQ_HZ);
        attached_ = servo_.attach(Pin::AIRBOX_FLAP, SERVO_MIN_US, SERVO_MAX_US);
        if (!attached_) {
            Serial.println("[AIRBOX] ERROR: Failed to attach servo!");
            return;
        }
        // Start at 50% (half-open, safe default)
        setImmediate(50);
        Serial.println("[AIRBOX] Servo initialized — default 50%");
    }

    void setMode(RideMode mode) {
        uint8_t target = MODE_PARAMS[mode].airbox_percent;
        sweep_step_ = MODE_PARAMS[mode].sweep_rate;
        setTarget(target);
        Serial.printf("[AIRBOX] Mode %s → Airbox %d%% (sweep=%d)\n",
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

    void emergencyOpen() {
        sweep_step_ = 10;
        setImmediate(100);
        Serial.println("[AIRBOX] EMERGENCY — Flap forced fully open");
    }

    void emergencyClose() {
        sweep_step_ = 10;
        setImmediate(0);
        Serial.println("[AIRBOX] EMERGENCY — Flap forced fully closed");
    }

private:
    uint8_t position_percent_;
    uint8_t target_percent_;
    uint8_t sweep_step_;
    Servo servo_;
    bool attached_;

    void applyPosition() {
        if (!attached_) return;
        uint8_t angle = map(position_percent_, 0, 100, 0, 180);
        servo_.write(angle);
    }
};