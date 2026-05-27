// ============================================================
// African Queen Lite — Main Program
// ESP32 Ride-Mode Controller for Honda NX650 Dominator RFVC
// ============================================================
//
// 6 Ride Modes: STRASSE, STADT, GELÄNDE, SPORT, COMFORT, SOUND
// Controls: Exhaust valve, Airbox flap, CDI map select, LED indicator
// Monitors: RPM, Temperature, Battery voltage, Oil pressure
// Displays: SSD1306 OLED (128x64 I2C)
// Connects: BLE for smartphone logging
//
// Hardware: ESP32 DevKit, SSD1306 OLED, WS2812 LED, 2x handlebar buttons
// Servos: Exhaust valve (PWM), Airbox flap (PWM)
//
// Safety features:
//   - Watchdog timer (5s timeout)
//   - Brownout detection enabled
//   - Emergency exhaust valve open on critical alerts
//   - Oil pressure warning with auto-alert
//   - Temperature shutdown protection

#include <Arduino.h>
#include "modes.h"
#include "cdi_controller.h"
#include "exhaust_valve.h"
#include "airbox.h"
#include "sensors.h"
#include "display.h"
#include "bluetooth.h"
#include "led_indicator.h"

// ---- Global Objects ----
Sensors         sensors;
CDIController   cdi;
ExhaustValve    exhaustValve;
AirboxFlap      airboxFlap;
Display         display;
Bluetooth       ble;
LEDIndicator    led;

// ---- State ----
RideMode currentMode = MODE_STRASSE;
RideMode previousMode = MODE_STRASSE;

// ---- Button debouncing ----
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

// ---- Alert flags ----
bool alert_temp  = false;
bool alert_volt  = false;
bool alert_oil   = false;
bool alert_rpm   = false;

// ---- Forward declarations ----
void handleButtons();
RideMode nextMode(RideMode current);
RideMode prevMode(RideMode current);
void checkAlerts();
void emergencyShutdown();
void IRAM_ATTR watchdogFeed();

void setup() {
    Serial.begin(115200);
    delay(500);
    Serial.println();
    Serial.println(F("========================================"));
    Serial.println(F("  African Queen Lite — Ride Mode Ctrl  "));
    Serial.println(F("  Honda NX650 Dominator RFVC           "));
    Serial.println(F("========================================"));
    Serial.println();

    // ---- Initialize Watchdog Timer ----
    esp_task_wdt_init(5, true);  // 5 second timeout, panic on timeout
    Serial.println("[INIT] Watchdog timer: 5s");

    // ---- Initialize GPIO ----
    pinMode(Pin::MODE_UP, INPUT_PULLUP);
    pinMode(Pin::MODE_DOWN, INPUT_PULLUP);

    // ---- Initialize Sensors ----
    sensors.setInstance();
    sensors.begin();

    // ---- Initialize CDI Controller ----
    cdi.begin();

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

    // ---- Apply Default Mode ----
    currentMode = MODE_STRASSE;
    cdi.setMode(currentMode);
    exhaustValve.setMode(currentMode);
    airboxFlap.setMode(currentMode);
    led.setMode(currentMode);
    display.showModeSwitch(currentMode);

    Serial.println();
    Serial.printf("[INIT] Mode: %s\n", MODE_NAMES[currentMode]);
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

    // ---- Handle Buttons ----
    handleButtons();

    // ---- Read Sensors (every 100ms) ----
    if (now - last_sensor_ms >= SENSOR_READ_MS) {
        sensors.update();
        last_sensor_ms = now;

        // Check alert conditions
        checkAlerts();
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
            alert_volt
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
        last_ble_ms = now;
    }
}

// ============================================================
// Button Handling with Debounce
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
            currentMode = nextMode(currentMode);
            Serial.printf("[MODE] → %s\n", MODE_NAMES[currentMode]);
            applyMode(currentMode);
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
            currentMode = prevMode(currentMode);
            Serial.printf("[MODE] → %s\n", MODE_NAMES[currentMode]);
            applyMode(currentMode);
        } else if (state_down == HIGH) {
            btn_mode_down.pressed = false;
        }
    }
    btn_mode_down.last_state = state_down;
}

void applyMode(RideMode mode) {
    cdi.setMode(mode);
    exhaustValve.setMode(mode);
    airboxFlap.setMode(mode);
    led.setMode(mode);
    display.showModeSwitch(mode);
}

RideMode nextMode(RideMode current) {
    return (RideMode)((current + 1) % MODE_COUNT);
}

RideMode prevMode(RideMode current) {
    return (RideMode)((current - 1 + MODE_COUNT) % MODE_COUNT);
}

// ============================================================
// Alert Checks — Safety Critical
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
        if (!alert_temp) led.setAlert(true);  // Don't override temp alert
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

    // Clear alert if all conditions normal
    if (!alert_temp && !alert_oil) {
        led.setAlert(false);
    }
}

void emergencyShutdown() {
    // Critical conditions detected — switch to safest mode
    Serial.println(F("[EMERGENCY] Switching to STADT (safe) mode"));
    Serial.println(F("[EMERGENCY] Exhaust valve forced OPEN for maximum cooling"));

    // Force exhaust valve fully open (maximum flow, best cooling)
    exhaustValve.emergencyOpen();
    airboxFlap.emergencyOpen();

    // Switch to STADT mode (most conservative)
    currentMode = MODE_STADT;
    cdi.setMode(currentMode);
    led.setAlert(true);  // Continuous red flash

    // Display will show alerts on next update cycle
    // Engine continues running but in safe mode
}