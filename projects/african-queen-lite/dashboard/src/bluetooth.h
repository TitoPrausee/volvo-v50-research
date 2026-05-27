#pragma once
// ============================================================
// African Queen Lite — BLE Bluetooth Service
// Honda NX650 Dominator RFVC
// ============================================================
//
// BLE GATT service for smartphone logging and monitoring.
// Exposes ride data as BLE characteristics:
//   - Current mode
//   - RPM
//   - Temperature
//   - Battery voltage
//   - Valve/Airbox positions
//   - Oil pressure status
//   - CDI map
//
// Uses NimBLE for lower memory footprint than classic BLE.
// Phone app can read/subscribe to these characteristics.

#include "modes.h"
#include <NimBLEDevice.h>

// BLE Service UUID (custom for AQL)
#define AQL_BLE_SERVICE_UUID        "426f5441-414c51-4e524541-4c544541"
#define AQL_CHAR_MODE_UUID         "426f5441-0001-4e52-4541-4c5445414d31"
#define AQL_CHAR_RPM_UUID          "426f5441-0002-4e52-4541-4c5445414d31"
#define AQL_CHAR_TEMP_UUID         "426f5441-0003-4e52-4541-4c5445414d31"
#define AQL_CHAR_VOLTAGE_UUID      "426f5441-0004-4e52-4541-4c5445414d31"
#define AQL_CHAR_VALVE_UUID        "426f5441-0005-4e52-4541-4c5445414d31"
#define AQL_CHAR_AIRBOX_UUID      "426f5441-0006-4e52-4541-4c5445414d31"
#define AQL_CHAR_OIL_UUID         "426f5441-0007-4e52-4541-4c5445414d31"
#define AQL_CHAR_CDI_UUID         "426f5441-0008-4e52-4541-4c5445414d31"

class Bluetooth {
public:
    Bluetooth() : pServer_(nullptr), initialized_(false),
                  ble_connected_(false) {}

    void begin() {
        NimBLEDevice::init("AQL-RideCtrl");

        // Create BLE Server
        pServer_ = NimBLEDevice::createServer();
        pServer_->setCallbacks(new ServerCallbacks(this));

        // Create BLE Service
        NimBLEService* pService = pServer_->createService(AQL_BLE_SERVICE_UUID);

        // Create Characteristics
        pMode_ = pService->createCharacteristic(
            AQL_CHAR_MODE_UUID,
            NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY
        );
        pRPM_ = pService->createCharacteristic(
            AQL_CHAR_RPM_UUID,
            NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY
        );
        pTemp_ = pService->createCharacteristic(
            AQL_CHAR_TEMP_UUID,
            NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY
        );
        pVoltage_ = pService->createCharacteristic(
            AQL_CHAR_VOLTAGE_UUID,
            NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY
        );
        pValve_ = pService->createCharacteristic(
            AQL_CHAR_VALVE_UUID,
            NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY
        );
        pAirbox_ = pService->createCharacteristic(
            AQL_CHAR_AIRBOX_UUID,
            NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY
        );
        pOil_ = pService->createCharacteristic(
            AQL_CHAR_OIL_UUID,
            NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY
        );
        pCDI_ = pService->createCharacteristic(
            AQL_CHAR_CDI_UUID,
            NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY
        );

        // Start the service
        pService->start();

        // Start advertising
        NimBLEAdvertising* pAdvertising = NimBLEDevice::createAdvertising();
        pAdvertising->addServiceUUID(AQL_BLE_SERVICE_UUID);
        pAdvertising->setScanResponse(true);
        pAdvertising->setMinPreferred(0x06);
        NimBLEDevice::startAdvertising();

        initialized_ = true;
        Serial.println("[BLE] NimBLE initialized — advertising as 'AQL-RideCtrl'");
    }

    // Update BLE characteristics — call at regular interval
    void update(RideMode mode, uint16_t rpm, float temp, float voltage,
                uint8_t valve_pos, uint8_t airbox_pos,
                bool oil_ok, uint8_t cdi_map) {
        if (!initialized_ || !ble_connected_) return;

        uint8_t buf[4];

        // Mode (1 byte)
        buf[0] = (uint8_t)mode;
        pMode_->setValue(buf, 1);
        pMode_->notify();

        // RPM (2 bytes, big-endian)
        buf[0] = (rpm >> 8) & 0xFF;
        buf[1] = rpm & 0xFF;
        pRPM_->setValue(buf, 2);
        pRPM_->notify();

        // Temperature (2 bytes: int16, x10 for 0.1°C resolution)
        int16_t temp_x10 = (int16_t)(temp * 10);
        buf[0] = (temp_x10 >> 8) & 0xFF;
        buf[1] = temp_x10 & 0xFF;
        pTemp_->setValue(buf, 2);
        pTemp_->notify();

        // Voltage (2 bytes: int16, x100 for 0.01V resolution)
        int16_t volt_x100 = (int16_t)(voltage * 100);
        buf[0] = (volt_x100 >> 8) & 0xFF;
        buf[1] = volt_x100 & 0xFF;
        pVoltage_->setValue(buf, 2);
        pVoltage_->notify();

        // Valve position (1 byte)
        buf[0] = valve_pos;
        pValve_->setValue(buf, 1);
        pValve_->notify();

        // Airbox position (1 byte)
        buf[0] = airbox_pos;
        pAirbox_->setValue(buf, 1);
        pAirbox_->notify();

        // Oil pressure (1 byte: 1=OK, 0=LOW)
        buf[0] = oil_ok ? 1 : 0;
        pOil_->setValue(buf, 1);
        pOil_->notify();

        // CDI map (1 byte: 0=A, 1=B)
        buf[0] = cdi_map;
        pCDI_->setValue(buf, 1);
        pCDI_->notify();
    }

    bool isConnected() const { return ble_connected_; }

private:
    NimBLEServer* pServer_;
    NimBLECharacteristic* pMode_;
    NimBLECharacteristic* pRPM_;
    NimBLECharacteristic* pTemp_;
    NimBLECharacteristic* pVoltage_;
    NimBLECharacteristic* pValve_;
    NimBLECharacteristic* pAirbox_;
    NimBLECharacteristic* pOil_;
    NimBLECharacteristic* pCDI_;

    bool initialized_;
    bool ble_connected_;

    // Server callbacks for connection state
    class ServerCallbacks : public NimBLEServerCallbacks {
    public:
        ServerCallbacks(Bluetooth* parent) : parent_(parent) {}

        void onConnect(NimBLEServer* pServer) override {
            parent_->ble_connected_ = true;
            Serial.println("[BLE] Client connected");
        }

        void onDisconnect(NimBLEServer* pServer) override {
            parent_->ble_connected_ = false;
            Serial.println("[BLE] Client disconnected — restarting advertising");
            NimBLEDevice::startAdvertising();
        }

    private:
        Bluetooth* parent_;
    };
};