#pragma once
// ============================================================
// African Queen Lite — Ride Mode Definitions v2.1
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.1 Changes:
//   - Fixed: NX650_FINAL_RATIO naming (was inconsistent NX650_FINALRatio)
//   - Added: CDI_MAP_B pin (GPIO33) for 3-map CDI control
//   - Added: CDI map index per mode (0=A/eco, 1=B/sport, 2=C/fallback)
//   - Added: Engine runtime increment logic constants
//   - Fixed: EEPROM layout addresses (aligned properly)

#include <cstdint>
#include <EEPROM.h>

// ---- EEPROM Layout ----
#define EEPROM_SIZE             64
#define EEPROM_MAGIC            0xA7  // Magic byte to validate EEPROM data
#define EEPROM_ADDR_MAGIC       0
#define EEPROM_ADDR_MODE        1     // Last active mode
#define EEPROM_ADDR_ODOMETER    4     // 4 bytes: total odometer (km * 10)
#define EEPROM_ADDR_RUNTIME     8     // 4 bytes: total engine runtime (minutes)
#define EEPROM_ADDR_MAINT_OIL   12    // 2 bytes: km * 10 since last oil change
#define EEPROM_ADDR_MAINT_VALVE 14    // 2 bytes: km * 10 since last valve adjust
#define EEPROM_ADDR_MAINT_FILT 16    // 2 bytes: km * 10 since last filter change

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

// ---- Throttle Response Curves ----
// 0=linear, 1=progressive (gentle start, aggressive mid-top)
// 2=aggressive, 3=soft
enum ThrottleCurve : uint8_t {
    THROTTLE_LINEAR     = 0,
    THROTTLE_PROGRESSIVE = 1,
    THROTTLE_AGGRESSIVE  = 2,
    THROTTLE_SOFT       = 3
};

// ---- CDI Map Selection ----
// Map A = base/retarded (eco), Map B = advanced (sport), Map C = fallback (standard)
enum CDIMap : uint8_t {
    CDI_MAP_A      = 0,  // Eco/retarded timing
    CDI_MAP_B      = 1,  // Advanced/sport timing
    CDI_MAP_C      = 2,  // Fallback/standard timing (both pins HIGH)
};

// ---- Mode Parameters ----
// ignition_offset : degrees retard (-) or advance (+) from base timing
// valve_percent   : exhaust valve position 0=closed 100=fully open
// airbox_percent  : airbox resonance flap 0=closed 100=fully open
// idle_target     : target idle RPM (x10, e.g. 130 = 1300 RPM)
// rev_limit      : rev limit (x100, e.g. 70 = 7000 RPM)
// sweep_rate     : servo transition speed 1=slow 10=instant
// throttle_curve : throttle response mapping
// cdi_map        : which CDI timing map to select (A/B/C)
// display_color  : RGB for mode LED indicator

struct ModeParams {
    int8_t   ignition_offset;   // degrees: -5 to +5
    uint8_t  valve_percent;     // 0-100 exhaust valve
    uint8_t  airbox_percent;    // 0-100 airbox flap
    uint8_t  idle_target;       // target idle RPM (x10, e.g. 130=1300)
    uint8_t  rev_limit;         // rev limit (x100, e.g. 70=7000)
    uint8_t  sweep_rate;        // servo transition speed: 1=slow smooth, 10=instant
    ThrottleCurve throttle_curve;
    CDIMap   cdi_map;           // CDI timing map selection
    ModeColor color;
};

// ---- Default Mode Parameter Sets ----
constexpr ModeParams MODE_PARAMS[MODE_COUNT] = {
    //          IGN   VALVE  AIRBOX  IDLE  REV_LIMIT  SWEEP  THROTTLE         CDI_MAP       COLOR
    /* STRASSE */ {  0,    50,    50,   130,   70,   3,  THROTTLE_LINEAR,     CDI_MAP_A, {  0, 255,   0} },
    /* STADT   */ { -2,    20,    30,   120,   65,   2,  THROTTLE_SOFT,       CDI_MAP_A, {  0, 100, 255} },
    /* GELAENDE*/ {  2,   100,   100,   140,   75,   6,  THROTTLE_AGGRESSIVE,  CDI_MAP_B, {255,  50,  50} },
    /* SPORT   */ {  3,   100,   100,   135,   75,   8,  THROTTLE_AGGRESSIVE,  CDI_MAP_B, {255, 165,   0} },
    /* COMFORT */ { -1,    40,    40,   125,   65,   2,  THROTTLE_SOFT,       CDI_MAP_A, {148,   0, 255} },
    /* SOUND   */ {  1,   100,    80,   130,   70,   5,  THROTTLE_PROGRESSIVE, CDI_MAP_C, {  0, 255, 255} },
};

// ---- Sensor Limits / Thresholds ----
constexpr uint16_t RPM_REDLINE        = 7500;   // NX650 redline
constexpr uint16_t RPM_IDLE_DEFAULT   = 1300;   // warm idle
constexpr uint16_t RPM_IDLE_COLD      = 1800;   // cold start fast idle

constexpr float    TEMP_WARNING       = 115.0f; // °C cylinder head warning
constexpr float    TEMP_CRITICAL      = 125.0f; // °C shutdown warning

constexpr float    VOLTAGE_LOW        = 11.5f;  // V battery warning
constexpr float    VOLTAGE_HIGH       = 15.5f;  // V regulator warning

// ---- Stator Health Monitoring ----
// NX650 stator: ~180W @ 5000 RPM, 12V system
// Healthy charging: 13.0V - 14.8V at 3000+ RPM
// Stator failing: voltage drops below 12V with RPM over idle
constexpr float    STATOR_HEALTHY_V   = 13.0f;  // V minimum at 3000+ RPM
constexpr float    STATOR_WARN_V      = 12.5f;  // V warning at 3000+ RPM
constexpr uint16_t STATOR_RPM_THRESH  = 3000;    // RPM threshold for stator check
constexpr uint16_t STATOR_RPM_HIGH    = 5000;    // RPM for full output check

// ---- LiFePO4 Battery Voltage Curves ----
// 4S LiFePO4: nominal 12.8V, range 10.0V - 14.6V
constexpr float    LIFEPO4_FULL       = 14.6f;  // V fully charged
constexpr float    LIFEPO4_NOMINAL    = 13.2f;  // V nominal
constexpr float    LIFEPO4_75_PCT     = 13.6f;  // V ~75% SOC
constexpr float    LIFEPO4_50_PCT     = 13.2f;  // V ~50% SOC
constexpr float    LIFEPO4_25_PCT     = 12.8f;  // V ~25% SOC
constexpr float    LIFEPO4_EMPTY      = 10.0f;  // V depleted — disconnect load
constexpr float    LIFEPO4_CHARGE_14_6= 14.6f;  // V max charge voltage

// ---- Maintenance Intervals ----
constexpr uint16_t MAINT_OIL_CHANGE_KM    = 6000;  // km between oil changes (NX650 spec)
constexpr uint16_t MAINT_VALVE_ADJUST_KM  = 12000; // km between valve adjustments
constexpr uint16_t MAINT_FILTER_CHANGE_KM = 12000; // km between air filter changes
constexpr uint16_t MAINT_SPARK_PLUG_KM    = 12000; // km between spark plug changes
constexpr uint16_t MAINT_DRIVE_CHAIN_KM   = 15000; // km between chain replacements
constexpr uint16_t MAINT_TIRE_CHECK_KM    = 1000;  // km between tire pressure checks

// ---- Runtime Tracking ----
constexpr unsigned long RUNTIME_INCREMENT_MS = 60000; // 1 minute increment

// ---- Pin Definitions ----
namespace Pin {
    // Inputs
    constexpr uint8_t MODE_UP         = 4;   // Handlebar button Mode+
    constexpr uint8_t MODE_DOWN       = 5;   // Handlebar button Mode-
    constexpr uint8_t ENCODER_A       = 16;  // Rotary encoder CLK (interrupt)
    constexpr uint8_t ENCODER_B       = 17;  // Rotary encoder DT
    constexpr uint8_t ENCODER_BTN     = 0;   // Rotary encoder push button (GPIO0 = BOOT)
    constexpr uint8_t IGNITION_PULSE  = 18;  // Pulse generator coil (interrupt)
    constexpr uint8_t OIL_PRESSURE    = 19;  // Oil pressure switch (LOW = pressure OK)
    constexpr uint8_t THERMISTOR      = 34;  // ADC: cylinder head thermistor
    constexpr uint8_t VOLTAGE_DIVIDER = 35;  // ADC: battery voltage divider
    constexpr uint8_t STATOR_SENSE    = 36;  // ADC: stator output voltage divider (high-side)

    // Outputs
    constexpr uint8_t EXHAUST_VALVE   = 25;  // PWM: exhaust valve servo
    constexpr uint8_t AIRBOX_FLAP    = 26;   // PWM: airbox resonance flap servo
    constexpr uint8_t CDI_MAP_A       = 27;   // Digital: CDI Map A select (active LOW)
    constexpr uint8_t CDI_MAP_B       = 33;   // Digital: CDI Map B select (active LOW) — v2.1 NEW
    constexpr uint8_t LED_DATA        = 32;   // WS2812 RGB LED data

    // I2C
    constexpr uint8_t OLED_SDA       = 21;   // I2C: OLED
    constexpr uint8_t OLED_SCL       = 22;   // I2C: OLED
}

// ---- Debounce / Timing ----
constexpr unsigned long DEBOUNCE_MS        = 50;    // Button debounce time
constexpr unsigned long ENCODER_DEBOUNCE_MS = 5;     // Encoder debounce (faster)
constexpr unsigned long MODE_DISPLAY_MS     = 2000;  // Show mode name after switching
constexpr unsigned long SENSOR_READ_MS      = 100;   // Sensor poll interval
constexpr unsigned long DISPLAY_UPDATE_MS   = 200;    // Display refresh interval
constexpr unsigned long BLE_UPDATE_MS       = 1000;  // BLE broadcast interval
constexpr unsigned long EEPROM_SAVE_MS      = 30000;  // EEPROM save interval (30s)
constexpr unsigned long STATOR_CHECK_MS    = 5000;   // Stator health check interval
constexpr unsigned long WATCHDOG_TIMEOUT   = 5000;   // ESP32 watchdog timeout ms

// ---- Servo PWM Ranges ----
constexpr uint16_t SERVO_MIN_US  = 500;    // Exhaust valve servo min pulse
constexpr uint16_t SERVO_MAX_US  = 2500;   // Exhaust valve servo max pulse
constexpr uint8_t  SERVO_FREQ_HZ = 50;     // Standard 50Hz servo PWM

// ---- Motor Driver Selection (compile-time) ----
// Set to 1 for production (DRV8833+AS5600), 0 for RC servo (testing)
#ifndef USE_PRODUCTION_MOTOR
#define USE_PRODUCTION_MOTOR  0
#endif

// ---- EEPROM Persistence Helper ----
class ModeStorage {
public:
    static void begin() {
        EEPROM.begin(EEPROM_SIZE);
    }

    // Save current mode to EEPROM (for power-on restore)
    static void saveMode(RideMode mode) {
        uint8_t magic = 0;
        EEPROM.get(EEPROM_ADDR_MAGIC, magic);
        if (magic != EEPROM_MAGIC) {
            EEPROM.write(EEPROM_ADDR_MAGIC, EEPROM_MAGIC);
        }
        EEPROM.write(EEPROM_ADDR_MODE, (uint8_t)mode);
        EEPROM.commit();
    }

    // Load last mode from EEPROM
    static RideMode loadMode() {
        uint8_t magic = 0;
        EEPROM.get(EEPROM_ADDR_MAGIC, magic);
        if (magic != EEPROM_MAGIC) {
            return MODE_STRASSE;  // Default
        }
        uint8_t mode = EEPROM.read(EEPROM_ADDR_MODE);
        if (mode >= MODE_COUNT) return MODE_STRASSE;
        return (RideMode)mode;
    }

    // Save odometer (km * 10 for 100m resolution)
    static void saveOdometer(uint32_t decikm) {
        EEPROM.put(EEPROM_ADDR_ODOMETER, decikm);
        EEPROM.commit();
    }

    static uint32_t loadOdometer() {
        uint32_t val = 0;
        EEPROM.get(EEPROM_ADDR_ODOMETER, val);
        return val;
    }

    // Save runtime (minutes)
    static void saveRuntime(uint32_t minutes) {
        EEPROM.put(EEPROM_ADDR_RUNTIME, minutes);
        EEPROM.commit();
    }

    static uint32_t loadRuntime() {
        uint32_t val = 0;
        EEPROM.get(EEPROM_ADDR_RUNTIME, val);
        return val;
    }
};
