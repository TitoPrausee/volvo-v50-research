#pragma once
// ============================================================
// African Queen Lite — Airbox Resonance Flap Control
// Honda NX650 Dominator RFVC
// ============================================================
//
// Controls the airbox intake resonance flap via servo.
// Position is set as a percentage: 0% = snorkel closed (quiet),
// 100% = fully open (maximum airflow, louder intake roar).
//
// The intake resonance flap changes the effective intake runner length,
// shifting the torque curve and also the intake sound character:
//   - Closed/low: Quieter, reduced airflow, torque at low RPM
//   - Open/high: Maximum airflow, louder intake, torque at high RPM
//
// Hardware: standard RC servo (50Hz PWM) controlled via ESP32Servo.
// Future: could use AS5600 + gearmotor for higher reliability.

#include "modes.h"
#include <ESP32Servo.h>

class AirboxFlap {
public:
    AirboxFlap() : position_percent_(0), target_percent_(0),
                   servo_(), attached_(false), smooth_step_(true) {}

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
        setTarget(target);
        Serial.printf("[AIRBOX] Mode %s → Airbox %d%%\n",
            MODE_NAMES[mode], target);
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

        if (smooth_step_ && position_percent_ != target_percent_) {
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

    void emergencyOpen() {
        setImmediate(100);
        Serial.println("[AIRBOX] EMERGENCY — Flap forced fully open");
    }

    void emergencyClose() {
        setImmediate(0);
        Serial.println("[AIRBOX] EMERGENCY — Flap forced fully closed");
    }

private:
    uint8_t position_percent_;
    uint8_t target_percent_;
    Servo servo_;
    bool attached_;
    bool smooth_step_;

    void applyPosition() {
        if (!attached_) return;
        uint8_t angle = map(position_percent_, 0, 100, 0, 180);
        servo_.write(angle);
    }
};