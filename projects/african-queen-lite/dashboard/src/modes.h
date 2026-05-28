#pragma once
// ============================================================
// African Queen Lite — Ride Mode Definitions v2.3
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.3 Changes:
//   - Added: Dedicated airbox RPM curves (AIRBOX_CURVES) — independent from exhaust
//   - Added: Rev limiter soft-cut parameters (REV_LIMITERS) per mode
//   - Added: Speed input pins (GPS_UART_RX/TX, WHEEL_SPEED)
//   - Fixed: Display splash version updated to v2.3
//
// v2.2 Changes:
//   - Added: Auto-RPM exhaust valve curves per mode (valve position follows RPM)
//   - Added: Fuel consumption estimation per mode (mL/100km)
//   - Added: Gear estimation parameters
//   - Added: Deep sleep timeout
//   - Added: Config mode constants
//   - Improved: Sweep rate ranges refined for smoother transitions
//
// v2.1:
//   - Fixed: NX650_FINAL_RATIO naming
//   - Added: CDI_MAP_B pin (GPIO33) for 3-map CDI control
//   - Added: Engine runtime increment logic constants
//   - Fixed: EEPROM layout addresses

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

// ---- Config Mode IDs ----
enum ConfigMode : uint8_t {
    CONFIG_IDLE         = 0,  // Normal riding
    CONFIG_BRIGHTNESS   = 1,  // Adjust LED brightness
    CONFIG_VALVE_CAL    = 2,  // Calibrate exhaust valve endpoints
    CONFIG_AIRBOX_CAL   = 3,  // Calibrate airbox flap endpoints
    CONFIG_RIDE_MODE    = 4,  // Select ride mode
    CONFIG_COUNT        = 5
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

constexpr const char* MODE_NAMES_SHORT[MODE_COUNT] = {
    "STR",   // 4 chars max for OLED
    "STD",
    "GLD",
    "SPT",
    "CMF",
    "SND"
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

// ---- RPM-based Valve Curve Point ----
// Valves follow an RPM curve: at rpm_low, position=start%; at rpm_high, position=end%
// Interpolation is linear between points
struct ValveCurvePoint {
    uint16_t rpm;        // RPM at this point
    uint8_t  position;   // Valve position 0-100%
};

// ---- Auto RPM Valve Curve per Mode ----
// Each mode has a curve that maps RPM → valve position
// This is used when ENABLE_AUTO_RPM_VALVE is active
// Points should be listed in ascending RPM order
constexpr uint8_t MAX_VALVE_CURVE_POINTS = 5;

struct ValveCurve {
    ValveCurvePoint points[MAX_VALVE_CURVE_POINTS];
    uint8_t        num_points;  // 2-5 points
};

// ---- Fuel Consumption Estimate per Mode ----
// mL/100km estimated for NX650 (based on riding style)
struct FuelEstimate {
    uint16_t ml_per_100km;  // Estimated fuel consumption in mL per 100km
    uint8_t  reserve_l;      // Reserve warning threshold in liters (NX650: 3.4L tank reserve)
};

// ---- Mode Parameters ----
// ignition_offset : degrees retard (-) or advance (+) from base timing
// valve_percent   : exhaust valve position 0=closed 100=fully open (base position)
// airbox_percent  : airbox resonance flap 0=closed 100=fully open (base position)
// idle_target     : target idle RPM (x10, e.g. 130 = 1300 RPM)
// rev_limit      : rev limit (x100, e.g. 70 = 7000 RPM)
// sweep_rate     : servo transition speed 1=slow 10=instant
// throttle_curve : throttle response mapping
// cdi_map        : which CDI timing map to select (A/B/C)
// fuel_est       : fuel consumption estimate for this mode
// display_color  : RGB for mode LED indicator

struct ModeParams {
    int8_t   ignition_offset;   // degrees: -5 to +5
    uint8_t  valve_percent;     // 0-100 exhaust valve (base position)
    uint8_t  airbox_percent;    // 0-100 airbox flap (base position)
    uint8_t  idle_target;       // target idle RPM (x10, e.g. 130=1300)
    uint8_t  rev_limit;         // rev limit (x100, e.g. 70=7000)
    uint8_t  sweep_rate;        // servo transition speed: 1=slow smooth, 10=instant
    ThrottleCurve throttle_curve;
    CDIMap   cdi_map;           // CDI timing map selection
    FuelEstimate fuel;          // Fuel consumption estimate
    ModeColor color;
};

// ---- Default Mode Parameter Sets ----
constexpr ModeParams MODE_PARAMS[MODE_COUNT] = {
    //          IGN   VALVE  AIRBOX  IDLE  REV_LIMIT  SWEEP  THROTTLE         CDI_MAP       FUEL(ml/100km,reserveL)           COLOR
    /* STRASSE */ {  0,    50,    50,   130,   70,   3,  THROTTLE_LINEAR,     CDI_MAP_A, {3500, 3}, {  0, 255,   0} },
    /* STADT   */ { -2,    20,    30,   120,   65,   2,  THROTTLE_SOFT,       CDI_MAP_A, {3000, 4}, {  0, 100, 255} },
    /* GELAENDE*/ {  2,   100,   100,   140,   75,   6,  THROTTLE_AGGRESSIVE,  CDI_MAP_B, {4500, 2}, {255,  50,  50} },
    /* SPORT   */ {  3,   100,   100,   135,   75,   8,  THROTTLE_AGGRESSIVE,  CDI_MAP_B, {5000, 2}, {255, 165,   0} },
    /* COMFORT */ { -1,    40,    40,   125,   65,   2,  THROTTLE_SOFT,       CDI_MAP_A, {3200, 4}, {148,   0, 255} },
    /* SOUND   */ {  1,   100,    80,   130,   70,   5,  THROTTLE_PROGRESSIVE, CDI_MAP_C, {4000, 3}, {  0, 255, 255} },
};

// ---- Auto RPM Valve Curves ----
// Each mode has an RPM-based valve position curve
// When ENABLE_AUTO_RPM_VALVE is active, valve position is
// interpolated from these curves instead of using valve_percent directly
constexpr ValveCurve VALVE_CURVES[MODE_COUNT] = {
    // STRASSE: gradual opening from 2000-6000 RPM, peak at 6500
    {{ {{2000, 15}, {3000, 35}, {4500, 50}, {6000, 65}, {7000, 50}} }, 5},
    // STADT: mostly closed, slight opening at higher RPM for scavenging
    {{{1500, 10}, {2500, 15}, {4000, 20}, {5500, 30}, {6500, 20}} }, 5},
    // GELÄNDE: fully open above 2500 RPM (maximum flow for power)
    {{{1500, 40}, {2500, 80}, {3500, 100}, {5000, 100}, {7000, 100}} }, 5},
    // SPORT: early opening, fully open above 3000
    {{{1500, 30}, {2500, 60}, {3000, 90}, {5000, 100}, {7000, 100}} }, 5},
    // COMFORT: moderate opening, smooth delivery
    {{{1500, 15}, {2500, 30}, {4000, 40}, {5500, 40}, {7000, 35}} }, 5},
    // SOUND: wide open for maximum acoustic output
    {{{1200, 60}, {2000, 85}, {3000, 95}, {4500, 100}, {6500, 80}} }, 5},
};

// ---- Auto RPM Airbox Curves ----
// v2.3: Dedicated airbox RPM curves (previously derived from valve curves)
// Airbox behavior is different from exhaust valve:
//   - Airbox affects intake resonance, not backpressure
//   - Closed airbox = quiet, rich low-end torque
//   - Open airbox = loud, free-flowing, peakier power band
//   - Airbox has a narrower effective RPM band than exhaust
constexpr ValveCurve AIRBOX_CURVES[MODE_COUNT] = {
    // STRASSE: moderate resonance tuning, 50% midrange
    {{ {{1500, 20}, {2500, 35}, {4000, 50}, {5500, 55}, {7000, 45}} }, 5},
    // STADT: mostly closed for quiet, slight opening at high RPM
    {{{1500, 10}, {2500, 20}, {4000, 30}, {5500, 35}, {7000, 25}} }, 5},
    // GELÄNDE: fully open above 3000 for maximum flow
    {{{1500, 30}, {2500, 60}, {3000, 90}, {5000, 100}, {7000, 100}} }, 5},
    // SPORT: aggressive opening, fully open above 4000
    {{{1500, 25}, {2500, 50}, {4000, 85}, {5500, 100}, {7000, 100}} }, 5},
    // COMFORT: gentle opening, never fully open
    {{{1500, 15}, {2500, 25}, {4000, 40}, {5500, 40}, {7000, 30}} }, 5},
    // SOUND: wide open early for resonance howl, tapers at top end
    {{{1200, 50}, {2000, 70}, {3000, 85}, {4500, 100}, {6500, 90}} }, 5},
};

// ---- Rev Limiter Soft-Cut Curves ----
// v2.3: Progressive ignition retard before hard rev limit.
// Each mode has 3 rev limiter stages:
//   1. SOFT_CUT_START: begin retarding timing (°offset added)
//   2. HARD_CUT_START: timing fully retarded, cylinder dropout begins
//   3. HARD_LIMIT: absolute rev limit (no spark above this)
struct RevLimiterParams {
    uint16_t soft_cut_rpm;    // RPM where timing retard begins
    int8_t   max_retard_deg;  // Maximum timing retard (degrees) at hard cut
    uint16_t hard_cut_rpm;    // RPM where cylinder dropout begins
    uint16_t hard_limit_rpm;  // Absolute rev limit
};

constexpr RevLimiterParams REV_LIMITERS[MODE_COUNT] = {
    // STRASSE: conservative limiter for road safety
    { 6800, -3, 7100, 7300 },
    // STADT: early limiter, maximize fuel economy
    { 6300, -4, 6600, 6800 },
    // GELÄNDE: high limiter for off-road power needs
    { 7200, -2, 7400, 7600 },
    // SPORT: aggressive limiter, high revs
    { 7200, -2, 7400, 7600 },
    // COMFORT: early limiter, smooth and relaxed
    { 6300, -3, 6600, 6800 },
    // SOUND: moderate limiter, focus on acoustic range
    { 6800, -2, 7000, 7200 },
};

// ---- Sensor Limits / Thresholds ----
constexpr uint16_t RPM_REDLINE        = 7500;   // NX650 redline
constexpr uint16_t RPM_IDLE_DEFAULT   = 1300;   // warm idle
constexpr uint16_t RPM_IDLE_COLD      = 1800;   // cold start fast idle
constexpr uint16_t RPM_SHIFT_OPTIMAL  = 5500;   // optimal shift point (fuel economy)

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

// ---- NX650 Tank ----
constexpr float    NX650_TANK_CAPACITY_L = 16.0f;  // liters
constexpr float    NX650_RESERVE_L      = 3.4f;     // liters reserve

// ---- Maintenance Intervals ----
constexpr uint16_t MAINT_OIL_CHANGE_KM    = 6000;  // km between oil changes (NX650 spec)
constexpr uint16_t MAINT_VALVE_ADJUST_KM  = 12000; // km between valve adjustments
constexpr uint16_t MAINT_FILTER_CHANGE_KM = 12000; // km between air filter changes
constexpr uint16_t MAINT_SPARK_PLUG_KM    = 12000; // km between spark plug changes
constexpr uint16_t MAINT_DRIVE_CHAIN_KM   = 15000; // km between chain replacements
constexpr uint16_t MAINT_TIRE_CHECK_KM    = 1000;  // km between tire pressure checks

// ---- Runtime Tracking ----
constexpr unsigned long RUNTIME_INCREMENT_MS = 60000; // 1 minute increment

// ---- Deep Sleep ----
constexpr unsigned long DEEP_SLEEP_TIMEOUT_MS = 300000; // 5 minutes engine off → deep sleep
constexpr unsigned long DEEP_SLEEP_WAKEUP_US = 0;       // No timer wake (wake on ignition)

// ---- Config Mode Timeout ----
constexpr unsigned long CONFIG_TIMEOUT_MS = 10000; // Auto-exit config after 10s inactivity

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
    constexpr uint8_t CDI_MAP_B       = 33;   // Digital: CDI Map B select (active LOW) — v2.1
    constexpr uint8_t LED_DATA        = 32;   // WS2812 RGB LED data

    // I2C
    constexpr uint8_t OLED_SDA       = 21;   // I2C: OLED
    constexpr uint8_t OLED_SCL       = 22;   // I2C: OLED

    // v2.3: Speed Input
    constexpr uint8_t GPS_UART_RX    = 15;  // UART2 RX for GPS NMEA (GPIO15)
    constexpr uint8_t GPS_UART_TX    = 14;  // UART2 TX for GPS NMEA (GPIO14)
    constexpr uint8_t WHEEL_SPEED    = 39;  // Wheel speed sensor (hall effect, input-only)
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
constexpr unsigned long FUEL_CALC_MS       = 10000;  // Fuel estimation update interval (10s)

// ---- Servo PWM Ranges ----
constexpr uint16_t SERVO_MIN_US  = 500;    // Exhaust valve servo min pulse
constexpr uint16_t SERVO_MAX_US  = 2500;   // Exhaust valve servo max pulse
constexpr uint8_t  SERVO_FREQ_HZ = 50;     // Standard 50Hz servo PWM

// ---- Motor Driver Selection (compile-time) ----
// Set to 1 for production (DRV8833+AS5600), 0 for RC servo (testing)
#ifndef USE_PRODUCTION_MOTOR
#define USE_PRODUCTION_MOTOR  0
#endif

// ---- Gear Estimation ----
// NX650 gear ratios (used to estimate current gear from RPM/speed)
// Gear detection: wheel_speed = (RPM * tire_circ) / (primary_ratio * gear_ratio * final_ratio * 60)
// If estimated speed matches actual speed → likely in that gear
constexpr float NX650_GEAR_RATIOS[5] = {2.846f, 1.857f, 1.389f, 1.091f, 0.913f};
constexpr float NX650_FINAL_RATIO   = 2.833f;
constexpr float NX650_PRIMARY_RATIO = 2.176f;
constexpr float NX650_TIRE_CIRC_M   = 2.04f;     // meters (120/90-17)

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