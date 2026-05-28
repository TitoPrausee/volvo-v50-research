#pragma once
// ============================================================
// African Queen Lite — Speed Input Module v2.3
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.3: NEW — Proper speed input with GPS NMEA, wheel sensor,
//        and RPM-based estimation fallback.
//
// Priority: GPS (Serial2) > Wheel sensor (interrupt) > RPM estimate
// GPS NMEA parses $GPRMC for speed in knots → km/h.
// Wheel sensor counts pulses per wheel revolution via interrupt.
// Fallback uses RPM + gear ratio from sensors.h.
//
// Speed filtering: exponential moving average (α=0.3) for GPS,
// simple pulse averaging for wheel sensor.

#include "modes.h"
#include <Arduino.h>

// ---- Speed Source Priority ----
enum SpeedSource : uint8_t {
    SPEED_NONE      = 0,  // No speed data available
    SPEED_GPS       = 1,  // GPS NMEA (Serial2)
    SPEED_WHEEL     = 2,  // Wheel speed sensor (interrupt)
    SPEED_RPM_EST   = 3   // RPM-based estimation (fallback)
};

// ---- GPS Configuration ----
constexpr uint16_t GPS_BAUD          = 9600;
constexpr uint8_t  GPS_RX_PIN         = Pin::GPS_UART_RX;  // UART2 RX (GPIO15)
constexpr uint8_t  GPS_TX_PIN         = Pin::GPS_UART_TX;  // UART2 TX (GPIO14)
constexpr unsigned long GPS_TIMEOUT_MS = 5000;  // No fix for 5s → degrade to next source

// ---- Wheel Speed Sensor Configuration ----
// Assuming: 1 pulse per wheel revolution, tire circumference 2.04m
constexpr float    WHEEL_PULSES_PER_REV = 1.0f;    // 1 magnet, 1 pulse per rev
constexpr float    WHEEL_CIRCUMFERENCE_M = NX650_TIRE_CIRC_M;  // 2.04m
constexpr unsigned long WHEEL_TIMEOUT_MS = 3000;  // No pulse for 3s → no speed

// ---- Speed Filter ----
constexpr float    SPEED_EMA_ALPHA = 0.3f;  // Exponential moving average factor

class SpeedInput {
public:
    SpeedInput() : speed_kmh_x10_(0), speed_kmh_(0.0f),
                   source_(SPEED_NONE), gps_fix_(false),
                   gps_speed_knots_(0.0f),
                   wheel_pulse_count_(0), wheel_period_us_(0),
                   wheel_last_pulse_us_(0),
                   last_gps_parse_ms_(0), last_wheel_calc_ms_(0),
                   ema_speed_kmh_(0.0f), ema_initialized_(false),
                   gps_buffer_idx_(0), gps_speed_valid_(false),
                   rpm_speed_kmh_x10_(0) {}

    void begin() {
        // Try GPS on Serial2
        Serial2.begin(GPS_BAUD, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN);
        gps_buffer_idx_ = 0;
        gps_fix_ = false;
        gps_speed_valid_ = false;
        last_gps_parse_ms_ = millis();

        // Wheel speed sensor interrupt (GPIO39 is input-only — ideal for hall sensor)
        pinMode(Pin::WHEEL_SPEED, INPUT_PULLUP);
        instance_ = this;
        attachInterrupt(digitalPinToInterrupt(Pin::WHEEL_SPEED),
                      wheelPulseISR, FALLING);

        Serial.println("[SPEED] Input initialized — GPS:NMEA Serial2, Wheel:interrupt, Fallback:RPM");
    }

    // Call every sensor update cycle (100ms)
    // rpm_speed_kmh_x10: speed from RPM estimate (from sensors.h)
    void update(uint16_t rpm_speed_kmh_x10) {
        unsigned long now = millis();
        rpm_speed_kmh_x10_ = rpm_speed_kmh_x10;

        // 1. Try GPS first
        parseGPS();

        if (gps_speed_valid_ && (now - last_gps_parse_ms_ < GPS_TIMEOUT_MS)) {
            source_ = SPEED_GPS;
            float gps_kmh = gps_speed_knots_ * 1.852f;  // knots → km/h
            speed_kmh_ = filterEMA(gps_kmh);
            speed_kmh_x10_ = (uint16_t)(speed_kmh_ * 10.0f);
            gps_fix_ = true;
            return;
        }

        // 2. Try wheel speed sensor
        if (wheel_pulse_count_ > 0) {
            unsigned long pulse_age = now - (wheel_last_pulse_us_ / 1000);
            if (pulse_age < WHEEL_TIMEOUT_MS) {
                source_ = SPEED_WHEEL;
                // Speed = (pulses/sec) * (circumference / pulses_per_rev) * 3.6
                float wheel_rps = (float)wheel_pulse_count_ /
                                   ((float)(now - last_wheel_calc_ms_) / 1000.0f);
                float wheel_kmh = wheel_rps * (WHEEL_CIRCUMFERENCE_M / WHEEL_PULSES_PER_REV) * 3.6f;
                speed_kmh_ = filterEMA(wheel_kmh);
                speed_kmh_x10_ = (uint16_t)(speed_kmh_ * 10.0f);
                wheel_pulse_count_ = 0;
                last_wheel_calc_ms_ = now;
                gps_fix_ = false;
                return;
            }
        }

        // 3. Fallback to RPM-based estimation
        source_ = SPEED_RPM_EST;
        speed_kmh_ = rpm_speed_kmh_x10 / 10.0f;
        speed_kmh_x10_ = rpm_speed_kmh_x10;
        gps_fix_ = false;
    }

    // ---- Getters ----
    float    getSpeedKmh()    const { return speed_kmh_; }
    uint16_t getSpeedKmhX10() const { return speed_kmh_x10_; }
    SpeedSource getSource()    const { return source_; }
    bool     hasGPSFix()       const { return gps_fix_; }
    bool     isSpeedValid()    const { return source_ != SPEED_NONE; }

    const char* getSourceName() const {
        switch (source_) {
            case SPEED_GPS:    return "GPS";
            case SPEED_WHEEL:  return "WHEEL";
            case SPEED_RPM_EST: return "RPM";
            default:           return "NONE";
        }
    }

private:
    float    speed_kmh_;
    uint16_t speed_kmh_x10_;
    SpeedSource source_;
    bool     gps_fix_;

    // GPS NMEA parsing
    float    gps_speed_knots_;
    unsigned long last_gps_parse_ms_;
    bool     gps_speed_valid_;
    char     gps_buffer_[128];
    uint8_t  gps_buffer_idx_;

    // Wheel speed sensor
    volatile uint32_t wheel_pulse_count_;
    uint32_t wheel_period_us_;
    unsigned long wheel_last_pulse_us_;
    unsigned long last_wheel_calc_ms_;

    // Exponential moving average filter
    float    ema_speed_kmh_;
    bool     ema_initialized_;

    // RPM fallback
    uint16_t rpm_speed_kmh_x10_;

    // ---- GPS NMEA Parser (minimal — just $GPRMC speed) ----
    void parseGPS() {
        while (Serial2.available()) {
            char c = Serial2.read();
            if (c == '$') {
                gps_buffer_idx_ = 0;
                gps_buffer_[gps_buffer_idx_++] = c;
            } else if (gps_buffer_idx_ > 0 && gps_buffer_idx_ < sizeof(gps_buffer_) - 1) {
                gps_buffer_[gps_buffer_idx_++] = c;
                if (c == '\n' || c == '\r') {
                    gps_buffer_[gps_buffer_idx_] = '\0';
                    processNMEA(gps_buffer_);
                    gps_buffer_idx_ = 0;
                }
            } else {
                gps_buffer_idx_ = 0;
            }
        }
    }

    void processNMEA(const char* sentence) {
        // We only care about $GPRMC for speed
        if (strncmp(sentence, "$GPRMC", 6) != 0 &&
            strncmp(sentence, "$GNRMC", 6) != 0) {
            return;
        }

        // $GPRMC,hhmmss.ss,A,llll.ll,N,yyyyy.yy,E,x.x,x.x,ddmmyy,x.x,a,a*hh
        // Fields: 0=tag, 1=time, 2=status(A/V), 3=lat, 4=N/S, 5=lon, 6=E/W,
        //         7=speed(knots), 8=course, 9=date, ...

        // Find field 7 (speed in knots)
        const char* p = sentence;
        int field = 0;
        while (field < 7 && *p) {
            if (*p == ',') field++;
            p++;
        }

        if (field == 7 && *p) {
            float knots = atof(p);
            if (knots >= 0 && knots < 500) {  // Sanity check
                gps_speed_knots_ = knots;
                gps_speed_valid_ = true;
                last_gps_parse_ms_ = millis();
            }
        }
    }

    // ---- Exponential Moving Average Filter ----
    float filterEMA(float new_val) {
        if (!ema_initialized_) {
            ema_speed_kmh_ = new_val;
            ema_initialized_ = true;
            return ema_speed_kmh_;
        }
        ema_speed_kmh_ = SPEED_EMA_ALPHA * new_val + (1.0f - SPEED_EMA_ALPHA) * ema_speed_kmh_;
        return ema_speed_kmh_;
    }

    // ---- Wheel Speed Sensor ISR ----
    static SpeedInput* instance_;
    static void IRAM_ATTR wheelPulseISR() {
        if (instance_) {
            instance_->wheel_pulse_count_++;
            instance_->wheel_last_pulse_us_ = micros();
        }
    }
};

SpeedInput* SpeedInput::instance_ = nullptr;
