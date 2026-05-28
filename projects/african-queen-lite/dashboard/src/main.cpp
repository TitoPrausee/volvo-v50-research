// ============================================================
// African Queen Lite — Main Program v2.2
// ESP32 Ride-Mode Controller for Honda NX650 Dominator RFVC
// ============================================================
//
// v2.2 Changes:
//   - Auto-RPM exhaust valve: position follows RPM curves per mode
//   - Fuel estimation per mode: mL/100km, range, low fuel warning
//   - Gear estimation: RPM/speed correlation for gear detection
//   - Config mode: long-press encoder for on-bike settings
//   - Deep sleep: 5 min engine off → deep sleep (wake on ignition)
//   - Display: gear indicator, fuel level, estimated range
//
// v2.1:
//   - CDI 3-map control (Map A/B/C via GPIO27 + GPIO33)
//   - Engine runtime counter
//   - BLE longevity data
//   - CDI emergency fallback to Map C
//   - Fixed: NX650_FINAL_RATIO naming
//
// 6 Ride Modes: STRASSE, STADT, GELÄNDE, SPORT, COMFORT, SOUND
// Controls: Exhaust valve, Airbox flap, CDI map select, LED indicator
// Monitors: RPM, Temperature, Battery, Oil pressure, Stator health, Fuel
// Displays: SSD1306 OLED (128x64 I2C) — 4 auto-cycling pages
// Connects: BLE for smartphone logging

#include <Arduino.h>
#include "modes.h"
#include "cdi_controller.h"
#include "exhaust_valve.h"
#include "airbox.h"
#include "sensors.h"
#include "display.h"
#include "longevity.h"
#include "bluetooth.h"
#include "led_indicator.h"
#include "encoder.h"
#include "auto_rpm_valve.h"
#include "fuel_estimator.h"
#include "gear_estimator.h"
#include "sleep_manager.h"
#include "config_mode.h"

// ---- Global Objects ----
Sensors         sensors;
CDIController   cdi;
ExhaustValve    exhaustValve;
AirboxFlap      airboxFlap;
Display         display;
Bluetooth       ble;
LEDIndicator    led;
LongevityMonitor longevity;
RotaryEncoder   encoder;
AutoRPMValve    autoRPMValve;
FuelEstimator   fuelEstimator;
GearEstimator   gearEstimator;
SleepManager    sleepManager;
ConfigMode      configMode;

// ---- State ----
RideMode currentMode = MODE_STRASSE;
RideMode previousMode = MODE_STRASSE;

// ---- Button debouncing (legacy — kept for Mode+/Mode- buttons) ----
struct Button {
    uint8_t pin;
    bool last_state;
    bool pressed;
    unsigned long last_debounce;
};

Button btn_mode_up   = {Pin::MODE_UP,   HIGH, false, 0};
Button btn_mode_down = {Pin::MODE_DOWN,  HIGH, false, 0};

// ---- Timing ----
unsigned long last_sensor_ms    = 0;
unsigned long last_display_ms   = 0;
unsigned long last_ble_ms       = 0;
unsigned long last_watchdog_ms  = 0;
unsigned long last_eeprom_ms    = 0;
unsigned long last_fuel_ms     = 0;
unsigned long last_sleep_check_ms = 0;

// ---- Alert flags ----
bool alert_temp  = false;
bool alert_volt  = false;
bool alert_oil   = false;
bool alert_rpm   = false;
bool alert_stator = false;
bool alert_fuel  = false;

// ---- Forward declarations ----
void handleButtons();
void handleEncoder();
RideMode nextMode(RideMode current);
RideMode prevMode(RideMode current);
void checkAlerts();
void emergencyShutdown();
void applyMode(RideMode mode);

void setup() {
    Serial.begin(115200);
    delay(500);
    Serial.println();
    Serial.println(F("========================================"));
    Serial.println(F("  African Queen Lite — Ride Mode Ctrl  "));
    Serial.println(F("  v2.2 — AutoValve + Fuel + Gear + Sleep"));
    Serial.println(F("  Honda NX650 Dominator RFVC           "));
    Serial.println(F("========================================"));
    Serial.println();

    // ---- Check wake from deep sleep ----
    if (SleepManager::wokeFromDeepSleep()) {
        Serial.printf("[WAKE] Woke from deep sleep: %s\n", SleepManager::getWakeReason());
    }

    // ---- Initialize Watchdog Timer ----
    esp_task_wdt_init(5, true);  // 5 second timeout, panic on timeout
    Serial.println("[INIT] Watchdog timer: 5s");

    // ---- Initialize EEPROM ----
    ModeStorage::begin();
    Serial.println("[INIT] EEPROM initialized");

    // ---- Initialize GPIO ----
    pinMode(Pin::MODE_UP, INPUT_PULLUP);
    pinMode(Pin::MODE_DOWN, INPUT_PULLUP);

    // ---- Initialize CDI Controller (3-map: GPIO27 + GPIO33) ----
    cdi.begin();

    // ---- Initialize Sensors ----
    sensors.setInstance();
    sensors.begin();

    // ---- Initialize Exhaust Valve ----
    exhaustValve.begin();

    // ---- Initialize Airbox Flap ----
    airboxFlap.begin();

    // ---- Initialize LED Indicator ----
    led.begin();

    // ---- Initialize Display ----
    display.begin();

    // ---- Initialize Bluetooth ----
    ble.begin();

    // ---- Initialize Encoder ----
    encoder.begin();

    // ---- Initialize Longevity Monitor ----
    longevity.begin();

    // ---- Initialize Auto RPM Valve ----
    autoRPMValve.begin();

    // ---- Initialize Fuel Estimator ----
    fuelEstimator.begin();

    // ---- Initialize Gear Estimator ----
    gearEstimator.begin();

    // ---- Initialize Sleep Manager ----
    sleepManager.begin();

    // ---- Initialize Config Mode ----
    configMode.begin();

    // ---- Restore Last Mode from EEPROM ----
    RideMode saved_mode = ModeStorage::loadMode();
    if (saved_mode >= MODE_COUNT) saved_mode = MODE_STRASSE;
    currentMode = saved_mode;

    // ---- Apply Restored Mode ----
    applyMode(currentMode);

    Serial.println();
    Serial.printf("[INIT] Mode: %s (restored from EEPROM)\n", MODE_NAMES[currentMode]);
    Serial.printf("[INIT] CDI: Map %c (GPIO%d + GPIO%d)\n",
        cdi.getCurrentMap() == CDI_MAP_A ? 'A' : (cdi.getCurrentMap() == CDI_MAP_B ? 'B' : 'C'),
        Pin::CDI_MAP_A, Pin::CDI_MAP_B);
    Serial.printf("[INIT] Auto-RPM Valve: %s\n", autoRPMValve.isEnabled() ? "ON" : "OFF");
    Serial.println(F("[INIT] Ready — ride safe!"));
    Serial.println();

    // Feed watchdog
    esp_task_wdt_reset();
}

void loop() {
    unsigned long now = millis();

    // ---- Feed Watchdog ----
    if (now - last_watchdog_ms > 1000) {
        esp_task_wdt_reset();
        last_watchdog_ms = now;
    }

    // ---- Config Mode: Check for long press ----
    bool encoder_btn = (digitalRead(Pin::ENCODER_BTN) == LOW);
    if (configMode.checkLongPress(encoder_btn)) {
        configMode.enter();
    }

    // ---- If in Config Mode, handle differently ----
    if (configMode.isActive()) {
        // Handle config mode encoder actions
        EncoderAction action = encoder.update();
        switch (action) {
            case ACTION_MODE_UP:
                configMode.handleRotate(1);
                break;
            case ACTION_MODE_DOWN:
                configMode.handleRotate(-1);
                break;
            case ACTION_PRESS:
                configMode.handlePress();
                break;
            default:
                break;
        }

        // Check config timeout
        configMode.checkTimeout();

        // Apply brightness
        led.setBrightness(configMode.getBrightness());

        // Update display with config screen
        // (display module handles this)
        // Still update sensors for safety
        sensors.update();

        // Feed watchdog
        esp_task_wdt_reset();
        return;  // Skip normal riding logic while in config
    }

    // ---- Handle Buttons (legacy Mode+/Mode-) ----
    handleButtons();

    // ---- Handle Rotary Encoder ----
    handleEncoder();

    // ---- Read Sensors (every 100ms) ----
    if (now - last_sensor_ms >= SENSOR_READ_MS) {
        sensors.update();
        last_sensor_ms = now;

        // Update longevity monitor (includes runtime counter)
        longevity.update(
            sensors.getVoltage(),
            sensors.getRPM(),
            sensors.getTemperature(),
            sensors.getSpeedKmhX10()
        );

        // Update gear estimator
        gearEstimator.update(sensors.getRPM(), sensors.getSpeedKmhX10());

        // Update fuel estimator (every 10s)
        if (now - last_fuel_ms >= FUEL_CALC_MS) {
            float speed_km = sensors.getSpeedKmhX10() / 10.0f;
            float distance_km = speed_km * (FUEL_CALC_MS / 3600000.0f);  // distance in this interval
            fuelEstimator.update(distance_km, currentMode, sensors.getRPM());
            last_fuel_ms = now;
        }

        // Check alert conditions
        checkAlerts();
    }

    // ---- Auto RPM Valve Control ----
    // When enabled, exhaust and airbox positions follow RPM curves
    if (autoRPMValve.isEnabled()) {
        uint16_t rpm = sensors.getRPM();
        uint8_t valve_pos = autoRPMValve.calculatePosition(currentMode, rpm);
        uint8_t airbox_pos = autoRPMValve.calculateAirboxPosition(currentMode, rpm);
        exhaustValve.setTarget(valve_pos);
        airboxFlap.setTarget(airbox_pos);
    }

    // ---- Update Servos (smooth transitions) ----
    exhaustValve.update();
    airboxFlap.update();

    // ---- Update LED (alert flashing) ----
    led.update();

    // ---- Update Display (every 200ms) ----
    if (now - last_display_ms >= DISPLAY_UPDATE_MS) {
        display.update(
            currentMode,
            sensors.getRPM(),
            sensors.getTemperature(),
            sensors.getVoltage(),
            exhaustValve.getPosition(),
            airboxFlap.getPosition(),
            sensors.getOilPressureOK(),
            cdi.getCurrentMap(),
            alert_temp,
            alert_volt,
            longevity
        );
        last_display_ms = now;
    }

    // ---- Update BLE (every 1s) ----
    if (now - last_ble_ms >= BLE_UPDATE_MS) {
        ble.update(
            currentMode,
            sensors.getRPM(),
            sensors.getTemperature(),
            sensors.getVoltage(),
            exhaustValve.getPosition(),
            airboxFlap.getPosition(),
            sensors.getOilPressureOK(),
            cdi.getCurrentMap()
        );

        // Longevity data via BLE
        ble.updateLongevity(
            (uint8_t)longevity.getStatorStatus(),
            longevity.getBatteryPercent(),
            longevity.getTotalOdometerKm(),
            longevity.getMaintenanceBitmap()
        );

        last_ble_ms = now;
    }

    // ---- Sleep Manager ----
    if (now - last_sleep_check_ms > 5000) {
        if (sleepManager.update(sensors.getRPM())) {
            // 5 minutes engine off → deep sleep
            sleepManager.enterDeepSleep();
            // Doesn't return from here — ESP32 resets on wake
        }
        last_sleep_check_ms = now;
    }

    // ---- EEPROM Save (every 30s) ----
    if (now - last_eeprom_ms >= EEPROM_SAVE_MS) {
        ModeStorage::saveMode(currentMode);
        // Also update odometer and runtime
        ModeStorage::saveOdometer(longevity.getTotalOdometerKm() * 10);
        ModeStorage::saveRuntime(longevity.getEngineRuntimeMin());
        last_eeprom_ms = now;
    }
}

// ============================================================
// Button Handling with Debounce (legacy Mode+/Mode-)
// ============================================================
void handleButtons() {
    // Mode+ button
    bool state_up = digitalRead(btn_mode_up.pin);
    if (state_up != btn_mode_up.last_state) {
        btn_mode_up.last_debounce = millis();
    }
    if ((millis() - btn_mode_up.last_debounce) > DEBOUNCE_MS) {
        if (state_up == LOW && !btn_mode_up.pressed) {
            btn_mode_up.pressed = true;
            if (!encoder.isModeSelect()) {
                display.nextPage();
            } else {
                currentMode = nextMode(currentMode);
                applyMode(currentMode);
            }
        } else if (state_up == HIGH) {
            btn_mode_up.pressed = false;
        }
    }
    btn_mode_up.last_state = state_up;

    // Mode- button
    bool state_down = digitalRead(btn_mode_down.pin);
    if (state_down != btn_mode_down.last_state) {
        btn_mode_down.last_debounce = millis();
    }
    if ((millis() - btn_mode_down.last_debounce) > DEBOUNCE_MS) {
        if (state_down == LOW && !btn_mode_down.pressed) {
            btn_mode_down.pressed = true;
            if (!encoder.isModeSelect()) {
                display.prevPage();
            } else {
                currentMode = prevMode(currentMode);
                applyMode(currentMode);
            }
        } else if (state_down == HIGH) {
            btn_mode_down.pressed = false;
        }
    }
    btn_mode_down.last_state = state_down;
}

// ============================================================
// Rotary Encoder Handling
// ============================================================
void handleEncoder() {
    EncoderAction action = encoder.update();

    switch (action) {
        case ACTION_MODE_UP:
            currentMode = nextMode(currentMode);
            applyMode(currentMode);
            Serial.printf("[ENCODER] Mode → %s\n", MODE_NAMES[currentMode]);
            break;

        case ACTION_MODE_DOWN:
            currentMode = prevMode(currentMode);
            applyMode(currentMode);
            Serial.printf("[ENCODER] Mode → %s\n", MODE_NAMES[currentMode]);
            break;

        case ACTION_PAGE_UP:
            display.nextPage();
            Serial.println("[ENCODER] Page → next");
            break;

        case ACTION_PAGE_DOWN:
            display.prevPage();
            Serial.println("[ENCODER] Page → prev");
            break;

        case ACTION_PRESS:
            encoder.toggleMode();
            break;

        default:
            break;
    }
}

// ============================================================
// Mode Application
// ============================================================
void applyMode(RideMode mode) {
    cdi.setMode(mode);

    // If auto RPM valve is DISABLED, use static positions from MODE_PARAMS
    // If enabled, auto_rpm_valve handles it in the main loop
    if (!autoRPMValve.isEnabled()) {
        exhaustValve.setMode(mode);
        airboxFlap.setMode(mode);
    }

    led.setMode(mode);
    display.showModeSwitch(mode);
    ModeStorage::saveMode(mode);  // Persist to EEPROM
}

RideMode nextMode(RideMode current) {
    return (RideMode)((current + 1) % MODE_COUNT);
}

RideMode prevMode(RideMode current) {
    return (RideMode)((current - 1 + MODE_COUNT) % MODE_COUNT);
}

// ============================================================
// Alert Checks — Safety Critical + Longevity + Fuel
// ============================================================
void checkAlerts() {
    // Temperature warnings
    bool prev_temp = alert_temp;
    alert_temp = sensors.isTempWarning();

    if (sensors.isTempCritical()) {
        Serial.println(F("[ALERT] CRITICAL TEMPERATURE — Emergency shutdown!"));
        emergencyShutdown();
        return;
    }

    if (alert_temp && !prev_temp) {
        Serial.println(F("[ALERT] Temperature warning!"));
        led.setAlert(true);
    }

    // Voltage warnings
    bool prev_volt = alert_volt;
    alert_volt = sensors.isVoltageLow() || sensors.isVoltageHigh();

    if (alert_volt && !prev_volt) {
        Serial.printf("[ALERT] Voltage warning: %.1fV\n", sensors.getVoltage());
        if (!alert_temp) led.setAlert(true);
    }

    // Oil pressure warning
    bool prev_oil = alert_oil;
    alert_oil = !sensors.getOilPressureOK();

    if (alert_oil && !prev_oil) {
        Serial.println(F("[ALERT] OIL PRESSURE LOW!"));
        if (!alert_temp) led.setAlert(true);
    }

    // Redline warning
    bool prev_rpm = alert_rpm;
    alert_rpm = sensors.isRPMRedline();

    if (alert_rpm && !prev_rpm) {
        Serial.printf("[ALERT] Redline: %d RPM!\n", sensors.getRPM());
    }

    // Stator health warning
    StatorStatus stator = longevity.getStatorStatus();
    if (stator >= STATOR_DEGRADED) {
        Serial.printf("[ALERT] Stator: %s (%.1fV)\n",
            longevity.getStatorStatusText(), longevity.getStatorVoltage());
        if (!alert_temp) led.setAlert(true);
    }

    // Fuel level warning
    bool prev_fuel = alert_fuel;
    alert_fuel = fuelEstimator.isLowFuel();

    if (alert_fuel && !prev_fuel) {
        Serial.printf("[ALERT] Low fuel: %.1fL remaining!\n", fuelEstimator.getFuelLiters());
        if (!alert_temp && !alert_oil) {
            led.setStatorWarning(true);  // Reuse yellow flash for fuel warning
        }
    }

    if (fuelEstimator.isCriticalFuel()) {
        Serial.printf("[ALERT] CRITICAL FUEL: %.1fL — refuel NOW!\n", fuelEstimator.getFuelLiters());
    }

    // Clear alert if all conditions normal
    if (!alert_temp && !alert_oil && stator < STATOR_DEGRADED && !alert_fuel) {
        led.setAlert(false);
    }
}

void emergencyShutdown() {
    Serial.println(F("[EMERGENCY] Switching to STADT (safe) mode"));
    Serial.println(F("[EMERGENCY] Exhaust valve forced OPEN for maximum cooling"));
    Serial.println(F("[EMERGENCY] CDI fallback to Map C (standard timing)"));

    exhaustValve.emergencyOpen();
    airboxFlap.emergencyOpen();
    cdi.emergencyFallback();  // v2.1: CDI Map C for safest timing

    currentMode = MODE_STADT;
    cdi.setMode(currentMode);  // Apply STADT CDI map after fallback clears emergency
    led.setAlert(true);
    ModeStorage::saveMode(currentMode);
}