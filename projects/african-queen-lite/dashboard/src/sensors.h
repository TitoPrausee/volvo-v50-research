#pragma once
// ============================================================
// African Queen Lite — Sensor Reading
// Honda NX650 Dominator RFVC
// ============================================================
//
// Sensors:
//   1. Ignition pulse coil → RPM (interrupt-based, period measurement)
//   2. Thermistor (NTC 10kΩ) → Cylinder head temperature
//   3. Voltage divider → Battery voltage
//   4. Oil pressure switch → LOW = pressure OK, HIGH = low pressure
//   5. CDI map feedback → which ignition map is active

#include "modes.h"
#include <Arduino.h>

class Sensors {
public:
    Sensors() : rpm_(0), rpm_period_us_(0), last_pulse_us_(0),
                temp_c_(25.0f), voltage_(12.0f), oil_pressure_ok_(true),
                pulse_count_(0), last_rpm_calc_ms_(0),
                rpm_timeout_(false), temp_raw_(0), voltage_raw_(0) {}

    void begin() {
        // Ignition pulse — interrupt on RISING edge (pulse generator coil)
        pinMode(Pin::IGNITION_PULSE, INPUT_PULLUP);
        attachInterrupt(digitalPinToInterrupt(Pin::IGNITION_PULSE),
                        ignitionPulseISR, RISING);

        // Oil pressure switch: LOW = OK, HIGH = warning
        pinMode(Pin::OIL_PRESSURE, INPUT_PULLUP);

        // ADC inputs (thermistor, voltage divider)
        pinMode(Pin::THERMISTOR, ANALOG);
        pinMode(Pin::VOLTAGE_DIVIDER, ANALOG);

        // ADC resolution
        analogSetAttenuation(ADC_11db);  // Full range 0-3.6V
        analogReadResolution(12);

        Serial.println("[SENSORS] Initialized — RPM, Temp, Voltage, Oil");
    }

    // Call regularly in main loop
    void update() {
        unsigned long now = millis();

        // === RPM Calculation ===
        // Single-cylinder 4-stroke: 1 pulse per 2 revolutions
        // RPM = 60,000,000 / (period_us * 2)
        if (pulse_count_ > 0 && rpm_period_us_ > 0) {
            // Average period over last N pulses
            rpm_ = 60000000UL / ((unsigned long)rpm_period_us_ * 2);
            rpm_ = constrain(rpm_, 0, 9999);
            last_rpm_calc_ms_ = now;
            pulse_count_ = 0;
        }

        // RPM timeout — if no pulse for 2 seconds, assume engine off
        if (now - last_rpm_calc_ms_ > 2000) {
            rpm_ = 0;
            rpm_timeout_ = true;
        } else {
            rpm_timeout_ = false;
        }

        // === Temperature (NTC thermistor) ===
        // Steinhart-Hart equation for 10kΩ NTC
        temp_raw_ = analogRead(Pin::THERMISTOR);
        float resistance = 10000.0f * (4095.0f / (float)temp_raw_ - 1.0f);
        float logR = log(resistance);
        // Steinhart-Hart coefficients (typical 10kΩ NTC)
        float k = 1.0f / (0.001129148f + 0.000234125f * logR +
                          0.0000000876741f * logR * logR * logR);
        temp_c_ = k - 273.15f;
        temp_c_ = constrain(temp_c_, -40.0f, 200.0f);

        // === Battery Voltage ===
        // Voltage divider: R1=100kΩ, R2=33kΩ → factor = (100+33)/33 = 4.03
        // ADC reads 0-3.6V → actual = ADC * 4.03 * 3.6 / 4095
        voltage_raw_ = analogRead(Pin::VOLTAGE_DIVIDER);
        voltage_ = (float)voltage_raw_ * 4.03f * 3.6f / 4095.0f;
        voltage_ = constrain(voltage_, 0.0f, 20.0f);

        // === Oil Pressure ===
        oil_pressure_ok_ = (digitalRead(Pin::OIL_PRESSURE) == LOW);
    }

    // ---- Getters ----
    uint16_t getRPM()          const { return rpm_; }
    float    getTemperature()  const { return temp_c_; }
    float    getVoltage()       const { return voltage_; }
    bool     getOilPressureOK() const { return oil_pressure_ok_; }
    bool     isRPMTimeout()     const { return rpm_timeout_; }
    uint16_t getTempRaw()       const { return temp_raw_; }
    uint16_t getVoltageRaw()    const { return voltage_raw_; }

    // ---- Warning Checks ----
    bool isTempWarning() const {
        return temp_c_ >= TEMP_WARNING;
    }

    bool isTempCritical() const {
        return temp_c_ >= TEMP_CRITICAL;
    }

    bool isVoltageLow() const {
        return voltage_ <= VOLTAGE_LOW;
    }

    bool isVoltageHigh() const {
        return voltage_ >= VOLTAGE_HIGH;
    }

    bool isRPMRedline() const {
        return rpm_ >= RPM_REDLINE;
    }

private:
    volatile uint32_t rpm_period_us_;   // Period between pulses (µs)
    volatile uint32_t pulse_count_;     // Pulse counter for averaging
    unsigned long last_pulse_us_;        // Timestamp of last pulse
    uint16_t rpm_;
    float temp_c_;
    float voltage_;
    bool oil_pressure_ok_;
    bool rpm_timeout_;
    unsigned long last_rpm_calc_ms_;
    uint16_t temp_raw_;
    uint16_t voltage_raw_;

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
    // Required for ISR access
    void setInstance() { instance_ = this; }
};

// Static instance pointer for ISR
Sensors* Sensors::instance_ = nullptr;