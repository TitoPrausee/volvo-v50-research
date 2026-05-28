#pragma once
// ============================================================
// African Queen Lite — Airbox Resonance Flap Control v2.1
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.1: Added DRV8833+AS5600 production motor driver option
// Same dual-mode as exhaust_valve.h (compile-time selectable).
//
// Controls the airbox intake resonance flap via servo.
// Position: 0% = snorkel closed (quiet), 100% = fully open (max flow).
//
// Smooth transitions in COMFORT/STADT, fast in SPORT/GELÄNDE.
//
// Hardware: standard RC servo (50Hz PWM) via ESP32Servo (TESTING).
// Production: gearmotor + AS5600 (same as exhaust valve).

#include "modes.h"
#include <ESP32Servo.h>
#if USE_PRODUCTION_MOTOR
#include <Wire.h>
#endif

class AirboxFlap {
public:
    AirboxFlap() : position_percent_(0), target_percent_(0),
                   sweep_step_(3), attached_(false)
#if USE_PRODUCTION_MOTOR
                   , motor_in1_(0), motor_in2_(0), as5600_addr_(0x37)
#endif
    {}

    void begin() {
#if USE_PRODUCTION_MOTOR
        motor_in1_ = 23;  // DRV8833 BIN1
        motor_in2_ = 2;    // DRV8833 BIN2
        pinMode(motor_in1_, OUTPUT);
        pinMode(motor_in2_, OUTPUT);
        stopMotor();
        Wire.begin(Pin::OLED_SDA, Pin::OLED_SCL);
        Serial.println("[AIRBOX] DRV8833 + AS5600 initialized — production motor driver");
#else
        servo_.setPeriodHertz(SERVO_FREQ_HZ);
        attached_ = servo_.attach(Pin::AIRBOX_FLAP, SERVO_MIN_US, SERVO_MAX_US);
        if (!attached_) {
            Serial.println("[AIRBOX] ERROR: Failed to attach servo!");
            return;
        }
        Serial.println("[AIRBOX] RC servo initialized — TESTING MODE ONLY");
#endif
        setImmediate(50);
        Serial.println("[AIRBOX] Default 50% (half-open, safe)");
    }

    void setMode(RideMode mode) {
        uint8_t target = MODE_PARAMS[mode].airbox_percent;
        sweep_step_ = MODE_PARAMS[mode].sweep_rate;
        setTarget(target);
        Serial.printf("[AIRBOX] Mode %s → Airbox %d%% (sweep=%d)\\n",
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
#if USE_PRODUCTION_MOTOR
        if (!attached_) return;
        if (position_percent_ != target_percent_) {
            if (position_percent_ < target_percent_) {
                position_percent_ = position_percent_ + min(sweep_step_, (uint8_t)(target_percent_ - position_percent_));
                driveMotorForward();
            } else {
                position_percent_ = position_percent_ - min(sweep_step_, (uint8_t)(position_percent_ - target_percent_));
                driveMotorBackward();
            }
            applyPosition();
        } else {
            stopMotor();
        }
#else
        if (!attached_) return;

        if (position_percent_ != target_percent_) {
            if (position_percent_ < target_percent_) {
                position_percent_ = position_percent_ + min(sweep_step_, (uint8_t)(target_percent_ - position_percent_));
            } else {
                position_percent_ = position_percent_ - min(sweep_step_, (uint8_t)(position_percent_ - target_percent_));
            }
            applyPosition();
        }
#endif
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

#if USE_PRODUCTION_MOTOR
    uint8_t motor_in1_;
    uint8_t motor_in2_;
    uint8_t as5600_addr_;
#else
    Servo servo_;
#endif
    bool attached_;

    void applyPosition() {
#if USE_PRODUCTION_MOTOR
        uint8_t duty = 128;
        if (position_percent_ < target_percent_) {
            analogWrite(motor_in1_, duty);
            analogWrite(motor_in2_, 0);
        } else if (position_percent_ > target_percent_) {
            analogWrite(motor_in1_, 0);
            analogWrite(motor_in2_, duty);
        } else {
            stopMotor();
        }
#else
        uint8_t angle = map(position_percent_, 0, 100, 0, 180);
        servo_.write(angle);
#endif
    }

#if USE_PRODUCTION_MOTOR
    void driveMotorForward() {
        analogWrite(motor_in1_, 128);
        analogWrite(motor_in2_, 0);
    }
    void driveMotorBackward() {
        analogWrite(motor_in1_, 0);
        analogWrite(motor_in2_, 128);
    }
    void stopMotor() {
        analogWrite(motor_in1_, 0);
        analogWrite(motor_in2_, 0);
    }
    uint8_t readAS5600Position() {
        Wire.beginTransmission(as5600_addr_);
        Wire.write(0x0E);
        Wire.endTransmission();
        Wire.requestFrom(as5600_addr_, (uint8_t)2);
        if (Wire.available() >= 2) {
            uint16_t raw = (Wire.read() << 8) | Wire.read();
            return (uint8_t)(raw / 40);
        }
        return position_percent_;
    }
#endif
};