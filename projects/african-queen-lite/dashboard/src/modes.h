#pragma once
// ============================================================
// African Queen Lite — Ride Mode Definitions
// Honda NX650 Dominator RFVC
// ============================================================

#include <cstdint>

// ---- Mode IDs ----
enum RideMode : uint8_t {
    MODE_STRASSE  = 0,  // Balanced, good power, moderate sound
    MODE_STADT     = 1,  // Gentle start, quiet, fuel-efficient
    MODE_GELAENDE  = 2,  // Aggressive timing, full power, off-road
    MODE_SPORT     = 3,  // Full power, sharp timing, open exhaust
    MODE_COMFORT   = 4,  // Soft timing, quiet, gentle throttle
    MODE_SOUND     = 5,  // Pure sound mode — exhaust open, best sound
    MODE_COUNT     = 6
};

// ---- Mode Color for LED indicator (WS2812 RGB) ----
struct ModeColor {
    uint8_t r, g, b;
};

constexpr ModeColor MODE_COLORS[MODE_COUNT] = {
    {  0, 255,   0},  // STRASSE  = green
    {  0, 100, 255},  // STADT    = blue
    {255,  50,  50},  // GELÄNDE  = red
    {255, 165,   0},  // SPORT    = orange
    {148,   0, 255},  // COMFORT  = violet
    {  0, 255, 255},  // SOUND    = cyan
};

constexpr const char* MODE_NAMES[MODE_COUNT] = {
    "STRASSE",
    "STADT",
    "GELANDE",
    "SPORT",
    "COMFORT",
    "SOUND"
};

// ---- Mode Parameters ----
// ignition_offset : degrees retard (-) or advance (+) from base timing
// valve_percent   : exhaust valve position 0=closed 100=fully open
// airbox_percent  : airbox resonance flap position 0=closed 100=fully open
// display_color   : RGB for mode LED indicator

struct ModeParams {
    int8_t   ignition_offset;   // degrees: -5 to +5
    uint8_t  valve_percent;     // 0-100 exhaust valve
    uint8_t  airbox_percent;    // 0-100 airbox flap
    uint8_t  idle_target;       // target idle RPM (x10, e.g. 130 = 1300 RPM)
    uint8_t  rev_limit;         // rev limit (x100, e.g. 70 = 7000 RPM)
    ModeColor color;
};

// ---- Default Mode Parameter Sets ----
constexpr ModeParams MODE_PARAMS[MODE_COUNT] = {
    //          IGN   VALVE  AIRBOX  IDLE  REV_LIMIT  COLOR
    /* STRASSE */ {  0,    50,    50,   130,   70,   {  0, 255,   0} },
    /* STADT   */ { -2,    20,    30,   120,   65,   {  0, 100, 255} },
    /* GELAENDE*/ {  2,   100,   100,   140,   75,   {255,  50,  50} },
    /* SPORT   */ {  3,   100,   100,   135,   75,   {255, 165,   0} },
    /* COMFORT */ { -1,    40,    40,   125,   65,   {148,   0, 255} },
    /* SOUND   */ {  1,   100,    80,   130,   70,   {  0, 255, 255} },
};

// ---- Sensor Limits / Thresholds ----
constexpr uint16_t RPM_REDLINE       = 7500;   // NX650 redline
constexpr uint16_t RPM_IDLE_DEFAULT   = 1300;   // warm idle
constexpr uint16_t RPM_IDLE_COLD       = 1800;   // cold start fast idle
constexpr float    TEMP_WARNING        = 115.0f; // °C cylinder head warning
constexpr float    TEMP_CRITICAL       = 125.0f; // °C shutdown warning
constexpr float    VOLTAGE_LOW         = 11.5f;  // V battery warning
constexpr float    VOLTAGE_HIGH        = 15.5f;  // V regulator warning

// ---- Pin Definitions ----
namespace Pin {
    // Inputs
    constexpr uint8_t MODE_UP         = 4;   // Handlebar button Mode+
    constexpr uint8_t MODE_DOWN       = 5;   // Handlebar button Mode-
    constexpr uint8_t IGNITION_PULSE   = 18;  // Pulse generator coil (interrupt)
    constexpr uint8_t OIL_PRESSURE     = 19;  // Oil pressure switch (LOW = pressure OK)
    constexpr uint8_t THERMISTOR       = 34;  // ADC: cylinder head thermistor
    constexpr uint8_t VOLTAGE_DIVIDER  = 35;  // ADC: battery voltage divider

    // Outputs
    constexpr uint8_t EXHAUST_VALVE   = 25;  // PWM: exhaust valve servo
    constexpr uint8_t AIRBOX_FLAP     = 26;  // PWM: airbox resonance flap servo
    constexpr uint8_t CDI_MAP_SELECT  = 27;  // Digital: CDI timing map select (0=A, 1=B)
    constexpr uint8_t LED_DATA        = 32;  // WS2812 RGB LED data
    constexpr uint8_t OLED_SDA        = 21;  // I2C: OLED
    constexpr uint8_t OLED_SCL        = 22;  // I2C: OLED
    constexpr uint8_t BLE_TX          = 17;  // UART2 TX for BLE module (if external)
    constexpr uint8_t BLE_RX          = 16;  // UART2 RX
}

// ---- Debounce / Timing ----
constexpr unsigned long DEBOUNCE_MS       = 50;   // Button debounce time
constexpr unsigned long MODE_DISPLAY_MS   = 2000; // Show mode name after switching
constexpr unsigned long SENSOR_READ_MS    = 100;  // Sensor poll interval
constexpr unsigned long DISPLAY_UPDATE_MS = 200;  // Display refresh interval
constexpr unsigned long BLE_UPDATE_MS     = 1000; // BLE broadcast interval
constexpr unsigned long WATCHDOG_TIMEOUT  = 5000; // ESP32 watchdog timeout ms

// ---- Servo PWM Ranges ----
constexpr uint16_t SERVO_MIN_US = 500;   // Exhaust valve servo min pulse
constexpr uint16_t SERVO_MAX_US = 2500;  // Exhaust valve servo max pulse
constexpr uint8_t  SERVO_FREQ_HZ = 50;   // Standard 50Hz servo PWM