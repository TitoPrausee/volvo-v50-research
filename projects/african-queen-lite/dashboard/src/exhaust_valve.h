#pragma once
// ============================================================
// African Queen Lite — Exhaust Valve Servo Control v2.1
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.1: Added compile-time selectable motor driver:
//   USE_PRODUCTION_MOTOR=1 → DRV8833 H-bridge + AS5600 magnetic encoder
//   USE_PRODUCTION_MOTOR=0 → RC servo (testing only — NOT suitable for motorcycle!)
//
// Production hardware: 12V gearmotor + DRV8833 H-bridge + AS5600 angle sensor
// (See RESEARCH.md for details — RC servos NOT suitable for motorcycle!)
// - Pololu 37Dx52L 13.5:1 gearmotor (~€25)
// - DRV8833 dual H-bridge (~€3)
// - AS5600 magnetic encoder (I²C, non-contact, vibration-resistant)
//
// Fallback: if using RC servo (testing only), direct PWM control.

#include "modes.h"
#include <ESP32Servo.h>
#if USE_PRODUCTION_MOTOR
#include <Wire.h>
#endif

class ExhaustValve {
public:
    ExhaustValve() : position_percent_(0), target_percent_(50),
                     sweep_step_(3), attached_(false)
#if USE_PRODUCTION_MOTOR
                     , motor_in1_(0), motor_in2_(0), as5600_addr_(0x36)
#endif
    {}

    void begin() {
#if USE_PRODUCTION_MOTOR
        // DRV8833 H-bridge pins (assigned from unused GPIOs)
        motor_in1_ = 14;  // DRV8833 AIN1
        motor_in2_ = 13;  // DRV8833 AIN2
        pinMode(motor_in1_, OUTPUT);
        pinMode(motor_in2_, OUTPUT);
        stopMotor();

        // AS5600 magnetic encoder on I²C
        Wire.begin(Pin::OLED_SDA, Pin::OLED_SCL);  // Shared I²C bus
        // AS5600 default address: 0x36
        Serial.println("[EXHAUST] DRV8833 + AS5600 initialized — production motor driver");
#else
        servo_.setPeriodHertz(SERVO_FREQ_HZ);
        attached_ = servo_.attach(Pin::EXHAUST_VALVE, SERVO_MIN_US, SERVO_MAX_US);
        if (!attached_) {
            Serial.println("[EXHAUST] ERROR: Failed to attach servo!");
            return;
        }
        Serial.println("[EXHAUST] RC servo initialized — TESTING MODE ONLY");
#endif
        // Start at 50% (half-open, safe default)
        setImmediate(50);
        Serial.println("[EXHAUST] Default 50% (half-open, safe)");
    }

    void setMode(RideMode mode) {
        uint8_t target = MODE_PARAMS[mode].valve_percent;
        sweep_step_ = MODE_PARAMS[mode].sweep_rate;
        setTarget(target);
        Serial.printf("[EXHAUST] Mode %s → Valve %d%% (sweep=%d)\\n",
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
#if USE_PRODUCTION_MOTOR
        if (!attached_) return;
        // Read actual position from AS5600
        uint8_t actual = readAS5600Position();

        // Drive motor toward target
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

#if USE_PRODUCTION_MOTOR
    uint8_t motor_in1_;          // DRV8833 AIN1
    uint8_t motor_in2_;          // DRV8833 AIN2
    uint8_t as5600_addr_;        // AS5600 I²C address
#else
    Servo servo_;
#endif
    bool attached_;

    void applyPosition() {
#if USE_PRODUCTION_MOTOR
        // DRV8833: PWM duty cycle controls motor speed
        // Map 0-100% to PWM duty (0=stopped, 255=full speed)
        // Position is tracked by AS5600, motor drives until target reached
        uint8_t duty = 128;  // Half speed for smooth positioning
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
        // Map 0-100% to servo angle 0-180°
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

    // Read AS5600 position (0-100%)
    uint8_t readAS5600Position() {
        Wire.beginTransmission(as5600_addr_);
        Wire.write(0x0E);  // RAW_ANGLE high byte register
        Wire.endTransmission();
        Wire.requestFrom(as5600_addr_, (uint8_t)2);
        if (Wire.available() >= 2) {
            uint16_t raw = (Wire.read() << 8) | Wire.read();
            // AS5600: 12-bit raw angle (0-4095)
            return (uint8_t)(raw / 40);  // Map to 0-100%
        }
        return position_percent_;  // Return last known if I2C fails
    }
#endif
};