#!/usr/bin/env python3
"""
Volvo V50 2.4i (P1 Platform) CAN-Bus Message Decoder
=====================================================
Decodes all known CAN messages from the V50 high-speed and low-speed CAN buses.
Uses python-can library for bus interface.

DB reference: vehicle_database.db — can_messages, can_signals tables
Hardware: Raspberry Pi 4 + PiCAN2 Duo HAT
Bus: High-Speed CAN (500kbps) on OBD2 pins 6/14
      Low-Speed CAN (125kbps) via CEM gateway

Author: v50-developer agent
Date: 2026-05-27
"""

import struct
import time
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple
from enum import IntEnum

logger = logging.getLogger('v50.can_decoder')


# =============================================================================
# CAN Bus Definitions
# =============================================================================

class CANBus(IntEnum):
    """V50 P1 Platform CAN buses"""
    HIGH_SPEED = 1  # 500kbps - Powertrain, OBD2 pins 6/14
    LOW_SPEED = 2   # 125kbps - Body/Comfort, via CEM gateway


# =============================================================================
# CAN Message Definitions — from DB can_messages + can_signals
# =============================================================================

@dataclass
class CANSignalDef:
    """Definition of a single CAN signal within a message"""
    name: str
    start_bit: int
    bit_length: int
    byte_order: str  # 'little' or 'big'
    factor: float
    offset: float
    unit: str
    min_value: float
    max_value: float
    description: str = ""


@dataclass
class CANMessageDef:
    """Definition of a CAN message with its signals"""
    can_id: int
    name: str
    bus: CANBus
    source_module: str
    dest_module: str
    description: str
    dlc: int
    signals: List[CANSignalDef] = field(default_factory=list)
    verified: bool = False
    notes: str = ""


# All 34 CAN messages from the database, with their signals
MESSAGE_DEFINITIONS: Dict[int, CANMessageDef] = {}

# --- HIGH-SPEED CAN (Bus 1) - Powertrain Messages ---

# 0x0C0 (192) - Engine RPM
msg = CANMessageDef(
    can_id=0x0C0, name="Engine RPM", bus=CANBus.HIGH_SPEED,
    source_module="ECM", dest_module="CEM", description="Byte 0-1: RPM/4",
    dlc=8, verified=True, notes="0x316 on facelift"
)
msg.signals = [
    CANSignalDef("engine_rpm", 0, 16, "little", 0.25, 0.0, "rpm", 0, 6500,
                 "Engine RPM. Factor 0.25 for MS-CAN bus. [SRC: VIDA + community]"),
]
MESSAGE_DEFINITIONS[0x0C0] = msg

# 0x0C8 (200) - Coolant Temp
msg = CANMessageDef(
    can_id=0x0C8, name="Coolant Temp", bus=CANBus.HIGH_SPEED,
    source_module="ECM", dest_module="CEM", description="Byte 0: °C-40",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("coolant_temp", 0, 16, "little", 1.0, -40.0, "°C", -40, 150,
                 "Coolant temperature, offset -40 [SRC: ISO 15031-5 + VIDA]"),
]
MESSAGE_DEFINITIONS[0x0C8] = msg

# 0x0D0 (208) - Throttle Position
msg = CANMessageDef(
    can_id=0x0D0, name="Throttle Position", bus=CANBus.HIGH_SPEED,
    source_module="ECM", dest_module="CEM", description="Byte 0: %",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("throttle_position", 8, 8, "little", 0.390625, 0.0, "%", 0, 100,
                 "Throttle position 0-100%"),
]
MESSAGE_DEFINITIONS[0x0D0] = msg

# 0x0D8 (216) - Engine Load/MAF
msg = CANMessageDef(
    can_id=0x0D8, name="Engine Load/MAF", bus=CANBus.HIGH_SPEED,
    source_module="ECM", dest_module="CEM", description="Byte 0-1: load",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("engine_load", 0, 8, "little", 0.390625, 0.0, "%", 0, 100,
                 "Calculated engine load percentage"),
    CANSignalDef("maf_rate", 16, 16, "little", 0.01, 0.0, "g/s", 0, 655.35,
                 "Mass air flow rate"),
]
MESSAGE_DEFINITIONS[0x0D8] = msg

# 0x0E0 (224) - Vehicle Speed
msg = CANMessageDef(
    can_id=0x0E0, name="Vehicle Speed", bus=CANBus.HIGH_SPEED,
    source_module="ECM", dest_module="CEM", description="Byte 0-1: speed/100 km/h",
    dlc=8, verified=True, notes="0x360 on facelift"
)
msg.signals = [
    CANSignalDef("vehicle_speed", 0, 16, "little", 0.01, 0.0, "km/h", 0, 300,
                 "Vehicle speed km/h [SRC: VIDA + community]"),
]
MESSAGE_DEFINITIONS[0x0E0] = msg

# 0x0F0 (240) - Fuel Level
msg = CANMessageDef(
    can_id=0x0F0, name="Fuel Level", bus=CANBus.HIGH_SPEED,
    source_module="ECM", dest_module="CEM", description="Byte 1: %",
    dlc=8, verified=True, notes="0x320 on facelift"
)
msg.signals = [
    CANSignalDef("fuel_level", 0, 8, "little", 0.390625, 0.0, "%", 0, 100,
                 "Fuel tank level percentage"),
]
MESSAGE_DEFINITIONS[0x0F0] = msg

# 0x100 (256) - Intake Air Temp
msg = CANMessageDef(
    can_id=0x100, name="Intake Air Temp", bus=CANBus.HIGH_SPEED,
    source_module="ECM", dest_module="CEM", description="Byte 0: °C-40",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("intake_air_temp", 0, 8, "little", 1.0, -40.0, "°C", -40, 80,
                 "Intake air temperature, offset -40"),
]
MESSAGE_DEFINITIONS[0x100] = msg

# 0x108 (264) - Oil Pressure/Temp
msg = CANMessageDef(
    can_id=0x108, name="Oil Pressure/Temp", bus=CANBus.HIGH_SPEED,
    source_module="ECM", dest_module="CEM", description="Byte 0: temp",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("oil_temp", 0, 8, "little", 1.0, -40.0, "°C", -40, 150,
                 "Oil temperature, offset -40"),
    CANSignalDef("oil_pressure_switch", 16, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "Oil pressure switch (0=low pressure)"),
]
MESSAGE_DEFINITIONS[0x108] = msg

# 0x1A0 (416) - Gear Position
msg = CANMessageDef(
    can_id=0x1A0, name="Gear Position", bus=CANBus.HIGH_SPEED,
    source_module="TCM", dest_module="CEM", description="Byte 0: P0,R1,N2,D3,4,5",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("gear_position", 0, 4, "little", 1.0, 0.0, "gear", 0, 6,
                 "Current gear (0=N, 1-5, 6=error)"),
]
MESSAGE_DEFINITIONS[0x1A0] = msg

# 0x1A8 (424) - Trans Temp
msg = CANMessageDef(
    can_id=0x1A8, name="Trans Temp", bus=CANBus.HIGH_SPEED,
    source_module="TCM", dest_module="CEM", description="Byte 0: °C-40",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("trans_fluid_temp", 0, 8, "little", 1.0, -40.0, "°C", -40, 150,
                 "Transmission fluid temperature"),
]
MESSAGE_DEFINITIONS[0x1A8] = msg

# 0x200 (512) - Climate Button
msg = CANMessageDef(
    can_id=0x200, name="Climate Button", bus=CANBus.HIGH_SPEED,
    source_module="ACC", dest_module="CEM", description="Byte 0: button ID",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("ac_button", 0, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "A/C on/off button"),
    CANSignalDef("recirc_button", 1, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "Recirculation button"),
    CANSignalDef("defrost_button", 2, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "Defrost button"),
]
MESSAGE_DEFINITIONS[0x200] = msg

# 0x208 (520) - Temp Set Driver
msg = CANMessageDef(
    can_id=0x208, name="Temp Set Driver", bus=CANBus.HIGH_SPEED,
    source_module="ACC", dest_module="CEM", description="Byte 0: °C×2",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("driver_temp_set", 0, 8, "little", 0.5, 16.0, "°C", 16, 30,
                 "Driver temperature setting"),
]
MESSAGE_DEFINITIONS[0x208] = msg

# 0x210 (528) - Temp Set Passenger
msg = CANMessageDef(
    can_id=0x210, name="Temp Set Passenger", bus=CANBus.HIGH_SPEED,
    source_module="ACC", dest_module="CEM", description="Byte 0: °C×2",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("passenger_temp_set", 0, 8, "little", 0.5, 16.0, "°C", 16, 30,
                 "Passenger temperature setting"),
]
MESSAGE_DEFINITIONS[0x210] = msg

# 0x218 (536) - Fan Speed
msg = CANMessageDef(
    can_id=0x218, name="Fan Speed", bus=CANBus.HIGH_SPEED,
    source_module="ACC", dest_module="CEM", description="Byte 0: 0-15",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("fan_speed_setting", 0, 4, "little", 1.0, 0.0, "level", 0, 15,
                 "Fan speed setting (0=off, 1-15)"),
]
MESSAGE_DEFINITIONS[0x218] = msg

# 0x220 (544) - Air Distribution
msg = CANMessageDef(
    can_id=0x220, name="Air Distribution", bus=CANBus.HIGH_SPEED,
    source_module="ACC", dest_module="CEM", description="Byte 0: 0=auto,1=face,2=feet,3=defrost",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("air_dist_face", 0, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "Face vents active"),
    CANSignalDef("air_dist_feet", 1, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "Feet vents active"),
    CANSignalDef("air_dist_defrost", 2, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "Defrost vents active"),
]
MESSAGE_DEFINITIONS[0x220] = msg

# 0x228 (552) - A/C Compressor
msg = CANMessageDef(
    can_id=0x228, name="A/C Compressor", bus=CANBus.HIGH_SPEED,
    source_module="ACC", dest_module="CEM", description="Byte 0: 0=off,1=on",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("ac_compressor_active", 0, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "A/C compressor running"),
]
MESSAGE_DEFINITIONS[0x228] = msg

# 0x230 (560) - Interior Temp
msg = CANMessageDef(
    can_id=0x230, name="Interior Temp", bus=CANBus.HIGH_SPEED,
    source_module="CEM", dest_module="DIM", description="Byte 0: °C×2",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("interior_temp", 0, 8, "little", 1.0, -40.0, "°C", -40, 60,
                 "Interior cabin temperature"),
]
MESSAGE_DEFINITIONS[0x230] = msg

# 0x238 (568) - Exterior Temp
msg = CANMessageDef(
    can_id=0x238, name="Exterior Temp", bus=CANBus.HIGH_SPEED,
    source_module="CEM", dest_module="DIM", description="Byte 0: °C-40",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("exterior_temp", 0, 8, "little", 1.0, -40.0, "°C", -40, 60,
                 "Exterior ambient temperature"),
]
MESSAGE_DEFINITIONS[0x238] = msg

# 0x240 (576) - Recirculation
msg = CANMessageDef(
    can_id=0x240, name="Recirculation", bus=CANBus.HIGH_SPEED,
    source_module="ACC", dest_module="CEM", description="Byte 0: 0=fresh,1=recirc",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("recirc_door_pos", 0, 8, "little", 0.390625, 0.0, "%", 0, 100,
                 "Recirculation door position"),
]
MESSAGE_DEFINITIONS[0x240] = msg

# 0x280 (640) - Blend Door Feedback
msg = CANMessageDef(
    can_id=0x280, name="Blend Door Feedback", bus=CANBus.HIGH_SPEED,
    source_module="CEM", dest_module="ACC", description="Byte 0: %",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("blend_door_pos", 0, 8, "little", 0.390625, 0.0, "%", 0, 100,
                 "Blend door position feedback"),
]
MESSAGE_DEFINITIONS[0x280] = msg

# 0x300 (768) - RPM Tachometer (DIM-specific)
msg = CANMessageDef(
    can_id=0x300, name="RPM Tachometer", bus=CANBus.HIGH_SPEED,
    source_module="CEM", dest_module="DIM", description="Byte 0-1: RPM/4",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("tach_rpm", 0, 16, "little", 0.25, 0.0, "rpm", 0, 8000,
                 "Tachometer display RPM"),
]
MESSAGE_DEFINITIONS[0x300] = msg

# 0x308 (776) - Speedometer (DIM-specific)
msg = CANMessageDef(
    can_id=0x308, name="Speedometer", bus=CANBus.HIGH_SPEED,
    source_module="CEM", dest_module="DIM", description="Byte 0-1: speed/100",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("speedo_kmh", 0, 16, "little", 0.01, 0.0, "km/h", 0, 300,
                 "Speedometer display speed"),
]
MESSAGE_DEFINITIONS[0x308] = msg

# 0x310 (784) - Fuel Gauge (DIM-specific)
msg = CANMessageDef(
    can_id=0x310, name="Fuel Gauge", bus=CANBus.HIGH_SPEED,
    source_module="CEM", dest_module="DIM", description="Byte 0: %",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("fuel_gauge", 0, 8, "little", 0.390625, 0.0, "%", 0, 100,
                 "Fuel gauge position"),
]
MESSAGE_DEFINITIONS[0x310] = msg

# 0x318 (792) - Coolant Gauge (DIM-specific)
msg = CANMessageDef(
    can_id=0x318, name="Coolant Gauge", bus=CANBus.HIGH_SPEED,
    source_module="CEM", dest_module="DIM", description="Byte 0: %",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("coolant_gauge", 0, 8, "little", 0.390625, 0.0, "position", 0, 1,
                 "Coolant gauge position"),
]
MESSAGE_DEFINITIONS[0x318] = msg

# 0x320 (800) - Warning Lights
msg = CANMessageDef(
    can_id=0x320, name="Warning Lights", bus=CANBus.HIGH_SPEED,
    source_module="CEM", dest_module="DIM", description="Byte 0-3: bitmap",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("check_engine", 0, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "Check Engine Light"),
    CANSignalDef("oil_warning", 1, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "Oil pressure warning"),
    CANSignalDef("battery_warning", 2, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "Battery/charging warning"),
    CANSignalDef("temp_warning", 3, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "Temperature warning"),
]
MESSAGE_DEFINITIONS[0x320] = msg

# 0x328 (808) - Odometer
msg = CANMessageDef(
    can_id=0x328, name="Odometer", bus=CANBus.HIGH_SPEED,
    source_module="CEM", dest_module="DIM", description="Byte 0-3: km",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("odometer_km", 0, 32, "little", 1.0, 0.0, "km", 0, 999999,
                 "Odometer in kilometers"),
]
MESSAGE_DEFINITIONS[0x328] = msg

# 0x340 (832) - Trip Button
msg = CANMessageDef(
    can_id=0x340, name="Trip Button", bus=CANBus.HIGH_SPEED,
    source_module="DIM", dest_module="CEM", description="Byte 0: button ID",
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("trip_button_pressed", 0, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "Trip reset button status"),
]
MESSAGE_DEFINITIONS[0x340] = msg

# --- LOW-SPEED CAN (Bus 2) - Body/Comfort Messages ---

# 0x400 (1024) - Steering Wheel Button
msg = CANMessageDef(
    can_id=0x400, name="Steering Wheel Button", bus=CANBus.LOW_SPEED,
    source_module="SWM", dest_module="CEM", description=None,
    dlc=8, verified=True, notes="0x260 facelift?"
)
msg.signals = [
    CANSignalDef("swc_button_id", 0, 8, "little", 1.0, 0.0, "id", 0, 255,
                 "Steering wheel button ID"),
]
MESSAGE_DEFINITIONS[0x400] = msg

# 0x410 (1040) - Driver Door Status
msg = CANMessageDef(
    can_id=0x410, name="Driver Door Status", bus=CANBus.LOW_SPEED,
    source_module="DDM", dest_module="CEM", description=None,
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("driver_door_open", 0, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "Driver door open status"),
    CANSignalDef("driver_door_locked", 1, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "Driver door locked status"),
]
MESSAGE_DEFINITIONS[0x410] = msg

# 0x418 (1048) - Passenger Door Status
msg = CANMessageDef(
    can_id=0x418, name="Passenger Door Status", bus=CANBus.LOW_SPEED,
    source_module="PDM", dest_module="CEM", description=None,
    dlc=8, verified=True
)
msg.signals = [
    CANSignalDef("pass_door_open", 0, 1, "little", 1.0, 0.0, "boolean", 0, 1,
                 "Passenger door open status"),
]
MESSAGE_DEFINITIONS[0x418] = msg


# =============================================================================
# Decoder Engine
# =============================================================================

def extract_signal(data: bytes, signal: CANSignalDef) -> float:
    """Extract a signal value from CAN message data bytes.
    
    Handles both little-endian and big-endian byte order (Motorola/Intel).
    Applies factor and offset to convert raw value to physical value.
    """
    # Convert bytes to integer
    raw_value = 0
    for i, byte in enumerate(data):
        raw_value |= byte << (i * 8)
    
    # Extract bits
    if signal.byte_order == "little":
        # Intel byte order (little-endian) — LSB first
        shift = signal.start_bit
        mask = (1 << signal.bit_length) - 1
        raw = (raw_value >> shift) & mask
    else:
        # Motorola byte order (big-endian) — MSB first
        # Convert start_bit for big-endian format
        shift = signal.start_bit
        mask = (1 << signal.bit_length) - 1
        raw = (raw_value >> shift) & mask
    
    # Apply factor and offset
    physical = (raw * signal.factor) + signal.offset
    
    # Clamp to valid range
    physical = max(signal.min_value, min(signal.max_value, physical))
    
    return physical


def decode_message(can_id: int, data: bytes) -> Dict[str, float]:
    """Decode all signals from a CAN message.
    
    Args:
        can_id: CAN identifier (without bus info)
        data: Raw data bytes (up to 8 bytes)
    
    Returns:
        Dictionary of signal_name -> physical_value
    """
    if can_id not in MESSAGE_DEFINITIONS:
        return {}
    
    msg_def = MESSAGE_DEFINITIONS[can_id]
    results = {}
    
    # Pad data to 8 bytes if needed
    padded = data.ljust(8, b'\x00')[:8]
    
    for signal in msg_def.signals:
        try:
            value = extract_signal(padded, signal)
            results[signal.name] = value
        except Exception as e:
            logger.warning(f"Failed to decode signal {signal.name} in msg 0x{can_id:03X}: {e}")
            results[signal.name] = None
    
    return results


# =============================================================================
# Vehicle State Tracker
# =============================================================================

class V50State:
    """Tracks the current state of all V50 vehicle parameters decoded from CAN bus."""
    
    def __init__(self):
        # Powertrain
        self.rpm: float = 0
        self.speed_kmh: float = 0
        self.coolant_temp_c: float = -40
        self.intake_air_temp_c: float = -40
        self.oil_temp_c: float = -40
        self.oil_pressure_ok: bool = True
        self.throttle_pct: float = 0
        self.engine_load_pct: float = 0
        self.maf_g_per_s: float = 0
        self.fuel_level_pct: float = 0
        self.gear: int = 0
        self.trans_temp_c: float = -40
        
        # Dashboard
        self.tach_rpm: float = 0
        self.speedo_kmh: float = 0
        self.fuel_gauge_pct: float = 0
        self.coolant_gauge_pct: float = 0
        self.odometer_km: float = 0
        self.check_engine: bool = False
        self.oil_warning: bool = False
        self.battery_warning: bool = False
        self.temp_warning: bool = False
        
        # Climate
        self.driver_temp_set_c: float = 20
        self.passenger_temp_set_c: float = 20
        self.interior_temp_c: float = 20
        self.exterior_temp_c: float = 20
        self.ac_active: bool = False
        self.fan_speed: int = 0
        self.recirc_active: bool = False
        
        # Doors
        self.driver_door_open: bool = False
        self.driver_door_locked: bool = False
        self.pass_door_open: bool = False
        
        # Timestamps for staleness detection
        self.last_update: Dict[int, float] = {}
        self.session_start: float = time.time()
    
    def update(self, can_id: int, data: bytes, timestamp: float = None):
        """Update vehicle state from a decoded CAN message."""
        if timestamp is None:
            timestamp = time.time()
        
        decoded = decode_message(can_id, data)
        if not decoded:
            return
        
        self.last_update[can_id] = timestamp
        
        # Map decoded signals to state
        for name, value in decoded.items():
            if value is None:
                continue
            
            # Powertrain
            if name == "engine_rpm":
                self.rpm = value
            elif name == "vehicle_speed":
                self.speed_kmh = value
            elif name == "coolant_temp":
                self.coolant_temp_c = value
            elif name == "intake_air_temp":
                self.intake_air_temp_c = value
            elif name == "oil_temp":
                self.oil_temp_c = value
            elif name == "oil_pressure_switch":
                self.oil_pressure_ok = (value == 0)
            elif name == "throttle_position":
                self.throttle_pct = value
            elif name == "engine_load":
                self.engine_load_pct = value
            elif name == "maf_rate":
                self.maf_g_per_s = value
            elif name == "fuel_level":
                self.fuel_level_pct = value
            elif name == "gear_position":
                self.gear = int(value)
            elif name == "trans_fluid_temp":
                self.trans_temp_c = value
            
            # Dashboard
            elif name == "tach_rpm":
                self.tach_rpm = value
            elif name == "speedo_kmh":
                self.speedo_kmh = value
            elif name == "fuel_gauge":
                self.fuel_gauge_pct = value
            elif name == "coolant_gauge":
                self.coolant_gauge_pct = value
            elif name == "check_engine":
                self.check_engine = bool(value)
            elif name == "oil_warning":
                self.oil_warning = bool(value)
            elif name == "battery_warning":
                self.battery_warning = bool(value)
            elif name == "temp_warning":
                self.temp_warning = bool(value)
            elif name == "odometer_km":
                self.odometer_km = value
            
            # Climate
            elif name == "driver_temp_set":
                self.driver_temp_set_c = value
            elif name == "passenger_temp_set":
                self.passenger_temp_set_c = value
            elif name == "interior_temp":
                self.interior_temp_c = value
            elif name == "exterior_temp":
                self.exterior_temp_c = value
            elif name == "ac_compressor_active":
                self.ac_active = bool(value)
            elif name == "fan_speed_setting":
                self.fan_speed = int(value)
            elif name == "recirc_door_pos":
                self.recirc_active = value > 50
            
            # Doors
            elif name == "driver_door_open":
                self.driver_door_open = bool(value)
            elif name == "driver_door_locked":
                self.driver_door_locked = bool(value)
            elif name == "pass_door_open":
                self.pass_door_open = bool(value)
    
    def get_staleness(self, can_id: int) -> Optional[float]:
        """Return seconds since last update for a given CAN ID, or None if never seen."""
        if can_id not in self.last_update:
            return None
        return time.time() - self.last_update[can_id]
    
    def summary(self) -> str:
        """Return a human-readable summary of current vehicle state."""
        lines = [
            f"=== V50 State (uptime: {time.time() - self.session_start:.0f}s) ===",
            f"  RPM: {self.rpm:.0f} | Speed: {self.speed_kmh:.1f} km/h",
            f"  Coolant: {self.coolant_temp_c:.0f}°C | Oil: {self.oil_temp_c:.0f}°C | Intake: {self.intake_air_temp_c:.0f}°C",
            f"  Throttle: {self.throttle_pct:.1f}% | Load: {self.engine_load_pct:.1f}% | MAF: {self.maf_g_per_s:.1f} g/s",
            f"  Fuel: {self.fuel_level_pct:.1f}% | Gear: {self.gear} | Trans: {self.trans_temp_c:.0f}°C",
            f"  Interior: {self.interior_temp_c:.0f}°C | Exterior: {self.exterior_temp_c:.0f}°C",
            f"  Warnings: CEL={self.check_engine} OIL={self.oil_warning} BAT={self.battery_warning} TEMP={self.temp_warning}",
            f"  Odometer: {self.odometer_km:.0f} km",
            f"  Doors: Driver={'OPEN' if self.driver_door_open else 'closed'} {'LOCKED' if self.driver_door_locked else 'unlocked'} | Pass={'OPEN' if self.pass_door_open else 'closed'}",
        ]
        return "\n".join(lines)


# =============================================================================
# DTC (Diagnostic Trouble Code) Reader via OBD2
# =============================================================================

# Standard OBD2 PIDs for V50 (from DB obd_pids table)
OBD2_STANDARD_PIDS = {
    0x0C: {"name": "Engine RPM", "formula": "(A*256+B)/4", "unit": "rpm", "pid": "01", "mode": "01"},
    0x0D: {"name": "Vehicle Speed", "formula": "A", "unit": "km/h", "pid": "01", "mode": "01"},
    0x05: {"name": "Coolant Temp", "formula": "A-40", "unit": "°C", "pid": "01", "mode": "01"},
    0x2F: {"name": "Fuel Level", "formula": "(A/255)*100", "unit": "%", "pid": "01", "mode": "01"},
    0x04: {"name": "Engine Load", "formula": "(A/255)*100", "unit": "%", "pid": "01", "mode": "01"},
    0x10: {"name": "MAF", "formula": "(A*256+B)/100", "unit": "g/s", "pid": "01", "mode": "01"},
    0x11: {"name": "Throttle Position", "formula": "(A/255)*100", "unit": "%", "pid": "01", "mode": "01"},
}

# Volvo proprietary PIDs (mode 22) — VERIFY BEFORE USE
VOLVO_PROPRIETARY_PIDS = {
    0x220104: {"name": "Oil Temp", "unit": "°C", "mode": "22", "verified": False, "notes": "Verify"},
    0x220105: {"name": "Boost Pressure", "unit": "hPa", "mode": "22", "verified": False, "notes": "Turbo only — 2.4i has no turbo! SKIP"},
    0x22010C: {"name": "Trans Fluid Temp", "unit": "°C", "mode": "22", "verified": False, "notes": "Verify"},
}


# =============================================================================
# Utility Functions
# =============================================================================

def get_gear_name(gear: int) -> str:
    """Convert gear position number to human-readable name."""
    gear_map = {0: "N", 1: "R", 2: "N", 3: "D", 4: "4", 5: "5", 6: "ERR"}
    return gear_map.get(gear, f"?{gear}")


def calculate_fuel_consumption(rpm: float, maf: float, rpm_prev: float = None) -> float:
    """Estimate fuel consumption in L/100km from RPM and MAF.
    
    Uses the relationship: Fuel = MAF / (AFR * fuel_density)
    AFR (stoichiometric) ≈ 14.7:1 for gasoline
    Fuel density ≈ 0.75 kg/L
    Requires vehicle speed for L/100km calculation.
    
    This is a rough estimate — the V50 ECM fuel level signal is more accurate.
    """
    AFR = 14.7
    FUEL_DENSITY = 0.75  # kg/L
    
    # Fuel mass flow = MAF / AFR
    fuel_mass_flow_kg_per_h = (maf / AFR) * 3600
    
    # Convert to volume flow
    fuel_flow_l_per_h = fuel_mass_flow_kg_per_h / FUEL_DENSITY
    
    return fuel_flow_l_per_h


def validate_can_id(can_id: int) -> Optional[CANMessageDef]:
    """Look up a CAN ID in the message definitions.
    
    Returns the message definition if found, None otherwise.
    """
    return MESSAGE_DEFINITIONS.get(can_id)


def list_known_messages() -> str:
    """Return a formatted list of all known CAN messages."""
    lines = ["=== V50 P1 CAN Messages ===\n"]
    
    for bus_name, bus_id in [("HIGH-SPEED (500kbps)", 1), ("LOW-SPEED (125kbps)", 2)]:
        lines.append(f"\n--- {bus_name} ---")
        for can_id, msg in sorted(MESSAGE_DEFINITIONS.items()):
            if msg.bus == bus_id:
                verified = "✓" if msg.verified else "?"
                lines.append(f"  0x{can_id:03X} ({can_id:4d}) | {verified} | {msg.source_module}→{msg.dest_module} | {msg.name}")
                for sig in msg.signals:
                    lines.append(f"      └─ {sig.name} [{sig.bit_length}bit @{sig.start_bit}] factor={sig.factor} offset={sig.offset} unit={sig.unit}")
    
    return "\n".join(lines)


# =============================================================================
# Main test
# =============================================================================

if __name__ == "__main__":
    print(list_known_messages())
    
    # Test decoding with sample data
    print("\n\n=== Decode Test ===")
    state = V50State()
    
    # Simulate: RPM = 3200 (raw = 3200/0.25 = 12800 = 0x3200)
    rpm_raw = int(3200 / 0.25)
    rpm_data = rpm_raw.to_bytes(2, 'little') + b'\x00' * 6
    state.update(0x0C0, rpm_data)
    
    # Simulate: Speed = 120 km/h (raw = 120/0.01 = 12000)
    speed_raw = int(120 / 0.01)
    speed_data = speed_raw.to_bytes(2, 'little') + b'\x00' * 6
    state.update(0x0E0, speed_data)
    
    # Simulate: Coolant = 90°C (raw = 90+40 = 130)
    coolant_data = bytes([130]) + b'\x00' * 7
    state.update(0x0C8, coolant_data)
    
    # Simulate: Fuel = 65% (raw = 65/0.390625 ≈ 166)
    fuel_raw = int(65 / 0.390625)
    fuel_data = bytes([fuel_raw]) + b'\x00' * 7
    state.update(0x0F0, fuel_data)
    
    print(state.summary())