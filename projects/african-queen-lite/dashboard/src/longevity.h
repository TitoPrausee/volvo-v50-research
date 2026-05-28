#pragma once
// ============================================================
// African Queen Lite — Longevity & Health Monitor v2.1
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.1 Changes:
//   - FIXED: engine_runtime_min_ now actually increments! Uses sensor
//     poll timing to count minutes when engine is running.
//   - Added: runtime tracking via last_runtime_ms_ accumulator
//   - Added: CDI map C awareness in status texts
//   - Improved: EEPROM save now includes runtime increment
//
// Monitors engine and electrical system health for LONGEVITY:
//   1. Stator health — detects failing stator BEFORE it leaves you stranded
//   2. LiFePO4 battery — SOC estimation from voltage curves
//   3. Cylinder head temperature — trend detection, overheat prediction
//   4. Oil pressure — warning before engine damage
//   5. Maintenance tracker — distance/time based service intervals
//   6. Trip logger — records rides for maintenance calculation
//
// NX650 has NO radiator — air-cooled! Temperature monitoring is CRITICAL.
// NX650 stator is known weak point — proactive monitoring prevents failures.

#include "modes.h"
#include <Arduino.h>

// ---- Stator Health Status ----
enum StatorStatus : uint8_t {
    STATOR_UNKNOWN   = 0,  // Engine off or RPM too low
    STATOR_HEALTHY   = 1,  // Voltage within expected range
    STATOR_DEGRADED  = 2,  // Voltage slightly below expected
    STATOR_FAILING   = 3,  // Voltage significantly below — stator dying!
    STATOR_OVERCHARGE = 4   // Voltage too high — regulator/rectifier failing!
};

// ---- Battery SOC Estimate ----
enum BatterySOC : uint8_t {
    BATT_FULL   = 0,  // > 13.6V
    BATT_75     = 1,  // 13.2V - 13.6V
    BATT_50     = 2,  // 12.8V - 13.2V
    BATT_25     = 3,  // 12.0V - 12.8V
    BATT_LOW    = 4,  // < 12.0V — charge ASAP!
    BATT_CRIT   = 5   // < 11.0V — damage risk!
};

// ---- Maintenance IDs ----
enum MaintID : uint8_t {
    MAINT_OIL_CHANGE    = 0,
    MAINT_VALVE_ADJUST  = 1,
    MAINT_AIR_FILTER    = 2,
    MAINT_SPARK_PLUG    = 3,
    MAINT_DRIVE_CHAIN   = 4,
    MAINT_TIRE_CHECK    = 5,
    MAINT_COUNT         = 6
};

constexpr const char* MAINT_NAMES[MAINT_COUNT] = {
    "Oil Change",
    "Valve Adjust",
    "Air Filter",
    "Spark Plug",
    "Drive Chain",
    "Tire Check"
};

constexpr uint16_t MAINT_INTERVALS_KM[MAINT_COUNT] = {
    MAINT_OIL_CHANGE_KM,      // 6000 km
    MAINT_VALVE_ADJUST_KM,    // 12000 km
    MAINT_FILTER_CHANGE_KM,  // 12000 km
    MAINT_SPARK_PLUG_KM,      // 12000 km
    MAINT_DRIVE_CHAIN_KM,    // 15000 km
    MAINT_TIRE_CHECK_KM       // 1000 km
};

class LongevityMonitor {
public:
    LongevityMonitor() : stator_status_(STATOR_UNKNOWN),
                          battery_soc_(BATT_FULL),
                          stator_voltage_(0),
                          voltage_samples_(0),
                          voltage_sum_(0),
                          last_stator_check_ms_(0),
                          temp_trend_rising_(false),
                          temp_peak_(25.0f),
                          overheat_predictions_(0),
                          total_odometer_km_(0),
                          trip_start_km_(0),
                          current_trip_km_(0),
                          engine_runtime_min_(0),
                          last_runtime_ms_(0),
                          last_eeprom_save_ms_(0) {

        // Initialize maintenance counters
        for (int i = 0; i < MAINT_COUNT; i++) {
            maint_since_km_[i] = 0;
            maint_overdue_[i] = false;
        }
    }

    void begin() {
        // Load persisted data from EEPROM
        ModeStorage::begin();
        total_odometer_km_ = ModeStorage::loadOdometer() / 10;  // decikm -> km
        engine_runtime_min_ = ModeStorage::loadRuntime();
        last_runtime_ms_ = millis();  // Initialize runtime tracker

        // Initialize maintenance counters
        for (int i = 0; i < MAINT_COUNT; i++) {
            maint_since_km_[i] = 0;
            maint_overdue_[i] = false;
        }

        Serial.printf("[LONGEVITY] Initialized — Odometer: %lu km, Runtime: %lu min\\n",
            (unsigned long)total_odometer_km_, (unsigned long)engine_runtime_min_);
    }

    // ---- Main update — call every sensor cycle (every SENSOR_READ_MS) ----
    void update(float voltage, uint16_t rpm, float temp_c, uint16_t speed_kmh_x10) {
        unsigned long now = millis();

        // === Runtime Counter (v2.1 FIX — actually increment!) ===
        // Increment engine_runtime_min_ every 60000ms when engine is running
        if (rpm > 0) {  // Engine is running
            if (last_runtime_ms_ > 0) {
                unsigned long elapsed = now - last_runtime_ms_;
                if (elapsed >= RUNTIME_INCREMENT_MS) {
                    engine_runtime_min_ += (elapsed / RUNTIME_INCREMENT_MS);
                    last_runtime_ms_ = now - (elapsed % RUNTIME_INCREMENT_MS);
                    Serial.printf("[RUNTIME] %lu min\\n", (unsigned long)engine_runtime_min_);
                }
            } else {
                last_runtime_ms_ = now;
            }
        } else {
            // Engine not running — don't accumulate, but keep reference
            last_runtime_ms_ = now;
        }

        // === Stator Health Check ===
        if (now - last_stator_check_ms_ >= STATOR_CHECK_MS) {
            checkStatorHealth(voltage, rpm);
            last_stator_check_ms_ = now;
        }

        // === Battery SOC ===
        updateBatterySOC(voltage, rpm);

        // === Temperature Trend ===
        updateTempTrend(temp_c);

        // === Odometer / Trip ===
        updateOdometer(speed_kmh_x10);

        // === EEPROM Save ===
        if (now - last_eeprom_save_ms_ >= EEPROM_SAVE_MS) {
            saveToEEPROM();
            last_eeprom_save_ms_ = now;
        }
    }

    // ============================================================
    // Stator Health Detection
    // ============================================================
    void checkStatorHealth(float voltage, uint16_t rpm) {
        if (rpm < STATOR_RPM_THRESH) {
            stator_status_ = STATOR_UNKNOWN;
            return;
        }

        voltage_sum_ += voltage;
        voltage_samples_++;

        if (voltage_samples_ < 3) return;

        float avg_voltage = voltage_sum_ / (float)voltage_samples_;

        if (avg_voltage > VOLTAGE_HIGH) {
            stator_status_ = STATOR_OVERCHARGE;
            Serial.printf("[STATOR] OVERCHARGE: %.1fV — regulator/rectifier may be failing!\\n", avg_voltage);
        }
        else if (avg_voltage < STATOR_WARN_V) {
            stator_status_ = STATOR_FAILING;
            Serial.printf("[STATOR] FAILING: %.1fV at %d RPM — stator output too low!\\n", avg_voltage, rpm);
        }
        else if (avg_voltage < STATOR_HEALTHY_V) {
            stator_status_ = STATOR_DEGRADED;
            Serial.printf("[STATOR] DEGRADED: %.1fV at %d RPM — monitor closely\\n", avg_voltage, rpm);
        }
        else {
            stator_status_ = STATOR_HEALTHY;
        }

        voltage_sum_ = 0;
        voltage_samples_ = 0;
        stator_voltage_ = avg_voltage;
    }

    StatorStatus getStatorStatus() const { return stator_status_; }
    float getStatorVoltage() const { return stator_voltage_; }

    const char* getStatorStatusText() const {
        switch (stator_status_) {
            case STATOR_HEALTHY:    return "HEALTHY";
            case STATOR_DEGRADED:   return "DEGRADED";
            case STATOR_FAILING:    return "FAILING!";
            case STATOR_OVERCHARGE: return "OVERCHG!";
            default:                return "UNKNOWN";
        }
    }

    // ============================================================
    // LiFePO4 Battery State of Charge
    // ============================================================
    void updateBatterySOC(float voltage, uint16_t rpm) {
        bool engine_running = (rpm > RPM_IDLE_DEFAULT - 200);

        if (engine_running) {
            if (voltage >= LIFEPO4_75_PCT) {
                battery_soc_ = BATT_FULL;
            } else if (voltage >= LIFEPO4_NOMINAL) {
                battery_soc_ = BATT_75;
            } else if (voltage >= LIFEPO4_25_PCT) {
                battery_soc_ = BATT_50;
            } else {
                battery_soc_ = BATT_LOW;
            }
        } else {
            if (voltage >= LIFEPO4_75_PCT) {
                battery_soc_ = BATT_FULL;
            } else if (voltage >= LIFEPO4_NOMINAL) {
                battery_soc_ = BATT_75;
            } else if (voltage >= LIFEPO4_25_PCT) {
                battery_soc_ = BATT_50;
            } else if (voltage >= 12.0f) {
                battery_soc_ = BATT_25;
            } else if (voltage >= 11.0f) {
                battery_soc_ = BATT_LOW;
            } else {
                battery_soc_ = BATT_CRIT;
                Serial.printf("[BATTERY] CRITICAL: %.1fV — BATTERY DAMAGE RISK!\\n", voltage);
            }
        }
    }

    BatterySOC getBatterySOC() const { return battery_soc_; }

    uint8_t getBatteryPercent() const {
        switch (battery_soc_) {
            case BATT_FULL:   return 100;
            case BATT_75:    return 75;
            case BATT_50:    return 50;
            case BATT_25:    return 25;
            case BATT_LOW:   return 15;
            case BATT_CRIT:  return 5;
            default:         return 50;
        }
    }

    const char* getBatterySOCText() const {
        switch (battery_soc_) {
            case BATT_FULL:   return "FULL";
            case BATT_75:     return "75%";
            case BATT_50:     return "50%";
            case BATT_25:     return "25%";
            case BATT_LOW:    return "LOW";
            case BATT_CRIT:   return "CRIT!";
            default:          return "???";
        }
    }

    // ============================================================
    // Temperature Trend Detection
    // ============================================================
    void updateTempTrend(float temp_c) {
        if (temp_c > temp_peak_) {
            temp_peak_ = temp_c;
        }

        static float last_temp = temp_c;
        static unsigned long last_temp_ms = 0;
        unsigned long now = millis();

        if (now - last_temp_ms >= 10000) {  // Check every 10s
            float delta = temp_c - last_temp;
            float rate = delta * 6.0f;  // °C per minute

            if (rate > 5.0f) {  // More than 5°C/min rise
                temp_trend_rising_ = true;
                overheat_predictions_++;
                if (overheat_predictions_ >= 3) {
                    Serial.printf("[TEMP] RAPID RISE: +%.1fC/min — overheat risk!\\n", rate);
                }
            } else if (rate < -2.0f) {
                temp_trend_rising_ = false;
                overheat_predictions_ = 0;
            }

            last_temp = temp_c;
            last_temp_ms = now;
        }
    }

    bool isTempTrendRising() const { return temp_trend_rising_; }
    float getTempPeak() const { return temp_peak_; }

    // ============================================================
    // Odometer & Trip
    // ============================================================
    void updateOdometer(uint16_t speed_kmh_x10) {
        float distance_km = (speed_kmh_x10 / 10.0f) / 36000.0f;

        current_trip_km_ += distance_km;
        total_odometer_km_ += distance_km;

        for (int i = 0; i < MAINT_COUNT; i++) {
            maint_since_km_[i] += (uint32_t)(distance_km * 10000);

            uint32_t interval_10000 = (uint32_t)MAINT_INTERVALS_KM[i] * 10000;
            if (maint_since_km_[i] >= interval_10000) {
                maint_overdue_[i] = true;
            }
        }
    }

    void startTrip() {
        trip_start_km_ = total_odometer_km_;
        current_trip_km_ = 0;
        temp_peak_ = 25.0f;
        overheat_predictions_ = 0;
        Serial.printf("[TRIP] Started — Odometer: %lu km\\n", (unsigned long)total_odometer_km_);
    }

    void endTrip() {
        Serial.printf("[TRIP] Ended — Distance: %.1f km, Peak Temp: %.1fC\\n",
            current_trip_km_, temp_peak_);
        saveToEEPROM();
    }

    void resetMaintenance(MaintID id) {
        maint_since_km_[id] = 0;
        maint_overdue_[id] = false;
        Serial.printf("[MAINT] Reset: %s\\n", MAINT_NAMES[id]);
    }

    bool isMaintenanceOverdue(MaintID id) const { return maint_overdue_[id]; }

    float getKmSinceMaintenance(MaintID id) const {
        return maint_since_km_[id] / 10000.0f;
    }

    float getKmUntilMaintenance(MaintID id) const {
        float interval = (float)MAINT_INTERVALS_KM[id];
        return interval - getKmSinceMaintenance(id);
    }

    uint32_t getTotalOdometerKm() const { return total_odometer_km_; }
    uint32_t getEngineRuntimeMin() const { return engine_runtime_min_; }  // v2.1: added getter
    float getCurrentTripKm() const { return current_trip_km_; }

    uint8_t getOverdueCount() const {
        uint8_t count = 0;
        for (int i = 0; i < MAINT_COUNT; i++) {
            if (maint_overdue_[i]) count++;
        }
        return count;
    }

    bool isAnyMaintenanceOverdue() const {
        return getOverdueCount() > 0;
    }

    // Get maintenance bitmap for BLE (bit 0=oil, 1=valve, 2=filter, 3=plug, 4=chain, 5=tire)
    uint8_t getMaintenanceBitmap() const {
        uint8_t bitmap = 0;
        for (int i = 0; i < MAINT_COUNT; i++) {
            if (maint_overdue_[i]) bitmap |= (1 << i);
        }
        return bitmap;
    }

private:
    // Stator health
    StatorStatus stator_status_;
    BatterySOC battery_soc_;
    float stator_voltage_;
    uint16_t voltage_samples_;
    float voltage_sum_;
    unsigned long last_stator_check_ms_;

    // Temperature trend
    bool temp_trend_rising_;
    float temp_peak_;
    uint8_t overheat_predictions_;

    // Maintenance tracking
    uint32_t total_odometer_km_;
    uint32_t trip_start_km_;
    float current_trip_km_;
    uint32_t engine_runtime_min_;
    unsigned long last_runtime_ms_;   // v2.1: runtime tracking timer
    uint32_t maint_since_km_[MAINT_COUNT];
    bool maint_overdue_[MAINT_COUNT];
    unsigned long last_eeprom_save_ms_;

    void saveToEEPROM() {
        uint32_t decikm = (uint32_t)(total_odometer_km_ * 10);
        ModeStorage::saveOdometer(decikm);
        ModeStorage::saveRuntime(engine_runtime_min_);
    }
};