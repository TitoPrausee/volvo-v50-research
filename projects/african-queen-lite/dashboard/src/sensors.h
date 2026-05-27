#pragma once
// ============================================================
// African Queen Lite — Sensor Reading v2.0
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.0: Added speed estimation from RPM+gear ratio for
// odometer/trip tracking. The NX650 has no speed sensor, so we
// estimate speed from RPM and known gear ratios.
//
// Sensors:
//   1. Ignition pulse coil → RPM (interrupt-based)
//   2. Thermistor (NTC 10kΩ) → Cylinder head temperature
//  3. Voltage divider → Battery voltage
//   4. Oil pressure switch → LOW=OK, HIGH=warning
//   5. Stator sense → Voltage at regulator output
//
// NX650 Gear Ratios (for speed estimation):
//   1st: 2.846  2nd: 1.857  3rd: 1.389  4th: 1.091  5th: 0.913
//   Final: 2.833  Primary: 2.176
//   Tire: 120/90-17 (circumference ~2.04m)

#include "modes.h"
#include <Arduino.h>

// NX650 gear ratios
constexpr float NX650_GEAR_RATIOS[5] = {2.846f, 1.857f, 1.389f, 1.091f, 0.913f};
constexpr float NX650_FINALRatio  = 2.833f;
constexpr float NX650_PRIMARY_RATIO = 2.176f;
constexpr float NX650_TIRE_CIRC_M = 2.04f; // meters

class Sensors {
public:
    Sensors() : rpm_(0), rpm_period_us_(0), last_pulse_us_(0),
                temp_c_(25.0f), voltage_(12.0f), oil_pressure_ok_(true),
                stator_voltage_(0.0f),
                pulse_count_(0), last_rpm_calc_ms_(0),
                rpm_timeout_(false), temp_raw_(0), voltage_raw_(0),
                stator_raw_(0),
                current_gear_(3),  // Assume 3rd gear at startup
                speed_kmh_x10_(0),
                engine_running_(false),
                rpm_samples_(0), rpm_sum_(0) {}

    void begin() {
        // Ignition pulse — interrupt on RISING edge
        pinMode(Pin::IGNITION_PULSE, INPUT_PULLUP);
        attachInterrupt(digitalPinToInterrupt(Pin::IGNITION_PULSE),
                        ignitionPulseISR, RISING);

        // Oil pressure switch
        pinMode(Pin::OIL_PRESSURE, INPUT_PULLUP);

        // ADC inputs
        pinMode(Pin::THERMISTOR, ANALOG);
        pinMode(Pin::VOLTAGE_DIVIDER, ANALOG);
        pinMode(Pin::STATOR_SENSE, ANALOG);

        // ADC resolution
        analogSetAttenuation(ADC_11db);  // Full range 0-3.6V
        analogReadResolution(12);

        // Button pins for gear indication (future: handlebar up/down)
        pinMode(Pin::MODE_UP, INPUT_PULLUP);
        pinMode(Pin::MODE_DOWN, INPUT_PULLUP);

        Serial.println("[SENSORS] Initialized — RPM, Temp, Voltage, Oil, Stator, Speed");
    }

    // Call regularly in main loop (every 100ms)
    void update() {
        unsigned long now = millis();

        // === RPM Calculation ===
        if (pulse_count_ > 0 && rpm_period_us_ > 0) {
            uint32_t period = rpm_period_us_;
            // Single-cylinder 4-stroke: 1 pulse per 2 revolutions
            rpm_ = 60000000UL / (period * 2);
            rpm_ = constrain(rpm_, 0, 9999);
            last_rpm_calc_ms_ = now;
            pulse_count_ = 0;

            // Running average for speed stability
            rpm_sum_ += rpm_;
            rpm_samples_++;
        }

        // RPM timeout — engine off
        if (now - last_rpm_calc_ms_ > 2000) {
            rpm_ = 0;
            rpm_timeout_ = true;
            engine_running_ = false;
            rpm_samples_ = 0;
            rpm_sum_ = 0;
            speed_kmh_x10_ = 0;
        } else {
            engine_running_ = true;
        }

        // === Temperature (NTC thermistor) ===
        temp_raw_ = analogRead(Pin::THERMISTOR);
        if (temp_raw_ > 0) {
            float resistance = 10000.0f * (4095.0f / (float)temp_raw_ - 1.0f);
            resistance = constrain(resistance, 100.0f, 100000.0f);
            float logR = log(resistance);
            float k = 1.0f / (0.001129148f + 0.000234125f * logR +
                              0.0000000876741f * logR * logR * logR);
            temp_c_ = k - 273.15f;
            temp_c_ = constrain(temp_c_, -40.0f, 200.0f);
        }

        // === Battery Voltage ===
        voltage_raw_ = analogRead(Pin::VOLTAGE_DIVIDER);
        // Voltage divider: R1=100kΩ, R2=33kΩ → factor = (100+33)/33 = 4.03
        voltage_ = (float)voltage_raw_ * 4.03f * 3.6f / 4095.0f;
        voltage_ = constrain(voltage_, 0.0f, 20.0f);

        // === Stator Voltage (separate ADC channel) ===
        stator_raw_ = analogRead(Pin::STATOR_SENSE);
        // Same divider ratio, but measured at regulator output
        stator_voltage_ = (float)stator_raw_ * 4.03f * 3.6f / 4095.0f;
        stator_voltage_ = constrain(stator_voltage_, 0.0f, 20.0f);

        // === Oil Pressure ===
        oil_pressure_ok_ = (digitalRead(Pin::OIL_PRESSURE) == LOW);

        // === Speed Estimation (from RPM + gear ratio) ===
        estimateSpeed();
    }

    // ---- Getters ----
    uint16_t getRPM()          const { return rpm_; }
    float    getTemperature()  const { return temp_c_; }
    float    getVoltage()       const { return voltage_; }
    float    getStatorVoltage() const { return stator_voltage_; }
    bool     getOilPressureOK() const { return oil_pressure_ok_; }
    bool     isRPMTimeout()     const { return rpm_timeout_; }
    bool     isEngineRunning()  const { return engine_running_; }
    uint16_t getTempRaw()       const { return temp_raw_; }
    uint16_t getVoltageRaw()    const { return voltage_raw_; }
    uint16_t getSpeedKmhX10()  const { return speed_kmh_x10_; }
    uint8_t  getCurrentGear()  const { return current_gear_; }

    // Gear shift (called from encoder or button)
    void gearUp() {
        if (current_gear_ < 4) current_gear_++;
        Serial.printf("[GEAR] → %d\n", current_gard_ + 1);
    }
    void gearDown() {
        if (current_gear_ > 0) current_gear_--;
        Serial.printf("[GEAR] → %d\n", current_gear_ + 1);
    }

    // ---- Warning Checks ----
    bool isTempWarning() const { return temp_c_ >= TEMP_WARNING; }
    bool isTempCritical() const { return temp_c_ >= TEMP_CRITICAL; }
    bool isVoltageLow() const { return voltage_ <= VOLTAGE_LOW; }
    bool isVoltageHigh() const { return voltage_ >= VOLTAGE_HIGH; }
    bool isRPMRedline() const { return rpm_ >= RPM_REDLINE; }

private:
    volatile uint32_t rpm_period_us_;
    volatile uint32_t pulse_count_;
    unsigned long last_pulse_us_;
    uint16_t rpm_;
    float temp_c_;
    float voltage_;
    float stator_voltage_;
    bool oil_pressure_ok_;
    bool rpm_timeout_;
    bool engine_running_;
    unsigned long last_rpm_calc_ms_;
    uint16_t temp_raw_;
    uint16_t voltage_raw_;
    uint16_t stator_raw_;
    uint8_t current_gear_;
    uint16_t speed_kmh_x10_;
    uint16_t rpm_samples_;
    uint32_t rpm_sum_;

    // Estimate road speed from RPM and gear ratio
    void estimateSpeed() {
        if (!engine_running_ || rpm_ == 0) {
            speed_kmh_x10_ = 0;
            return;
        }

        // Total reduction: primary * gear * final
        float total_ratio = NX650_PRIMARY_RATIO *
                           NX650_GEAR_RATIOS[current_gear_] *
                           NX650_FINAL_RATIO;

        // Wheel RPM from engine RPM
        float wheel_rpm = (float)rpm_ / total_ratio;

        // Speed in m/min = wheel_rpm * tire_circumference
        // Speed in km/h = (wheel_rpm * tire_circumference * 60) / 1000
        float speed_kmh = (wheel_rpm * NX650_TIRE_CIRC_M * 60.0f) / 1000.0f;

        // Convert to 0.1 km/h units
        speed_kmh_x10_ = (uint16_t)(speed_kmh * 10.0f);
        speed_kmh_x10_ = constrain(speed_kmh_x10_, 0, 2000);  // Max 200 km/h
    }

    // ISR for ignition pulse — must be IRAM_ATTR for ESP32
    static void IRAM_ATTR ignitionPulseISR() {
        unsigned long now = micros();
        if (instance_) {
            uint32_t period = now - instance_->last_pulse_us_;
            if (period > 5000) {  // Debounce: ignore pulses < 5ms
                instance_->rpm_period_us_ = period;
                instance_->pulse_count_++;
                instance_->last_pulse_us_ = now;
            }
        }
    }

    static Sensors* instance_;
public:
    void setInstance() { instance_ = this; }
};

// Static instance pointer for ISR
Sensors* Sensors::instance_ = nullptr;