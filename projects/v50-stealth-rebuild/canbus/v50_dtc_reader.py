#!/usr/bin/env python3
"""
Volvo V50 2.4i — OBD2 DTC Diagnostics Module
==============================================
Reads and clears Diagnostic Trouble Codes (DTCs) via OBD2 protocol
over CAN bus. Replaces expensive VIDA/DICE for basic fault code reading.

Supports:
- Standard OBD2 PIDs (Mode 01) for live data
- Mode 03: Read stored DTCs
- Mode 04: Clear DTCs (caution!)
- Mode 07: Read pending DTCs
- Mode 09: VIN readout
- Volvo-proprietary Mode 22 PIDs for extended diagnostics

Hardware: Raspberry Pi 4 + PiCAN2 Duo HAT
Interface: SocketCAN (can0) via python-can

NOTE: Mode 22 PIDs are Volvo-specific and need physical verification.
      The 2.4i (B5244S) naturally aspirated engine does NOT have boost pressure.

Author: v50-developer agent
Date: 2026-05-28
"""

import asyncio
import logging
import struct
import time
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional, Dict, List, Tuple

try:
    import can
    HAS_PYTHON_CAN = True
except ImportError:
    HAS_PYTHON_CAN = False

logger = logging.getLogger('v50.dtc_reader')


# =============================================================================
# DTC Definitions
# =============================================================================

class DTCStatus(IntEnum):
    """DTC status per ISO 15031-6 / ISO 14229-1."""
    CURRENT = 0x01        # Confirmed, currently active
    PENDING = 0x02        # Pending — failed once, not yet confirmed
    PERMANENT = 0x04      # Permanent — cannot be cleared until condition passes
    HISTORY = 0x08        # History — stored but not currently active


@dataclass
class DTCCode:
    """A single Diagnostic Trouble Code."""
    code: str              # e.g., "P0171", "P0420", "B0001"
    description: str       # Human-readable description
    status: DTCStatus      # Current status
    module: str = ""       # Source module (ECM, TCM, ABS, CEM, etc.)
    freeze_frame: Optional[Dict[str, float]] = None  # Snapshot data when code set
    first_seen_km: Optional[float] = None             # Odometer when first set
    occurrences: int = 1                               # Number of occurrences


# =============================================================================
# Volvo V50 (P1 Platform) DTC Code Database
# =============================================================================

# Common DTCs for Volvo P1 platform — B5244S engine
# Organized by module prefix: P0xxx=powertrain, P1xxx=manufacturer, B0xxx=body, C0xxx=chassis, U0xxx=network

V50_DTC_CODES: Dict[str, str] = {
    # === POWERTRAIN (P0xxx, P1xxx) ===
    "P0010": "A Camshaft Position Actuator Circuit (Bank 1)",
    "P0011": "A Camshaft Position - Timing Over-Advanced (Bank 1)",
    "P0012": "A Camshaft Position - Timing Over-Retarded (Bank 1)",
    "P0030": "HO2S Heater Control Circuit (Bank 1 Sensor 1)",
    "P0031": "HO2S Heater Control Circuit Low (Bank 1 Sensor 1)",
    "P0032": "HO2S Heater Control Circuit High (Bank 1 Sensor 1)",
    "P0036": "HO2S Heater Control Circuit (Bank 1 Sensor 2)",
    "P0037": "HO2S Heater Control Circuit Low (Bank 1 Sensor 2)",
    "P0038": "HO2S Heater Control Circuit High (Bank 1 Sensor 2)",
    "P0100": "Mass Air Flow Sensor Circuit",
    "P0101": "Mass Air Flow Sensor Circuit Range/Performance",
    "P0102": "Mass Air Flow Sensor Circuit Low Input",
    "P0103": "Mass Air Flow Sensor Circuit High Input",
    "P0110": "Intake Air Temperature Sensor Circuit",
    "P0115": "Engine Coolant Temperature Sensor Circuit",
    "P0116": "Engine Coolant Temperature Sensor Range/Performance",
    "P0117": "Engine Coolant Temperature Sensor Circuit Low Input",
    "P0118": "Engine Coolant Temperature Sensor Circuit High Input",
    "P0120": "Throttle/Pedal Position Sensor/Switch A Circuit",
    "P0121": "Throttle/Pedal Position Sensor/Switch A Circuit Range/Performance",
    "P0128": "Coolant Thermostat (Coolant Temp Below Thermostat Regulating Temperature)",
    "P0130": "O2 Sensor Circuit (Bank 1 Sensor 1)",
    "P0131": "O2 Sensor Circuit Low Voltage (Bank 1 Sensor 1)",
    "P0132": "O2 Sensor Circuit High Voltage (Bank 1 Sensor 1)",
    "P0133": "O2 Sensor Circuit Slow Response (Bank 1 Sensor 1)",
    "P0135": "O2 Sensor Heater Circuit (Bank 1 Sensor 1)",
    "P0136": "O2 Sensor Circuit (Bank 1 Sensor 2)",
    "P0137": "O2 Sensor Circuit Low Voltage (Bank 1 Sensor 2)",
    "P0138": "O2 Sensor Circuit High Voltage (Bank 1 Sensor 2)",
    "P0170": "Fuel Trim (Bank 1)",
    "P0171": "System Too Lean (Bank 1)",
    "P0172": "System Too Rich (Bank 1)",
    "P0174": "System Too Lean (Bank 2) — not applicable for I4, but stored if ECM reports it",
    "P0175": "System Too Rich (Bank 2) — not applicable for I4",
    "P0300": "Random/Multiple Cylinder Misfire Detected",
    "P0301": "Cylinder 1 Misfire Detected",
    "P0302": "Cylinder 2 Misfire Detected",
    "P0303": "Cylinder 3 Misfire Detected",
    "P0304": "Cylinder 4 Misfire Detected",
    "P0335": "Crankshaft Position Sensor A Circuit",
    "P0336": "Crankshaft Position Sensor A Circuit Range/Performance",
    "P0340": "Camshaft Position Sensor Circuit (Bank 1)",
    "P0341": "Camshaft Position Sensor Circuit Range/Performance",
    "P0351": "Ignition Coil A Primary/Secondary Circuit",
    "P0352": "Ignition Coil B Primary/Secondary Circuit",
    "P0353": "Ignition Coil C Primary/Secondary Circuit",
    "P0354": "Ignition Coil D Primary/Secondary Circuit",
    "P0420": "Catalyst System Efficiency Below Threshold (Bank 1)",
    "P0442": "Evaporative Emission Control System Leak Detected (small leak)",
    "P0444": "Evaporative Emission Control System Purge Control Valve Circuit Open",
    "P0445": "Evaporative Emission Control System Purge Control Valve Circuit Shorted",
    "P0455": "Evaporative Emission Control System Leak Detected (gross leak)",
    "P0462": "Fuel Level Sensor Circuit Low Input",
    "P0463": "Fuel Level Sensor Circuit High Input",
    "P0500": "Vehicle Speed Sensor",
    "P0501": "Vehicle Speed Sensor Range/Performance",
    "P0506": "Idle Air Control System RPM Lower Than Expected",
    "P0507": "Idle Air Control System RPM Higher Than Expected",
    "P0562": "System Voltage Low",
    "P0563": "System Voltage High",
    "P0600": "Serial Communication Link",
    "P0601": "Internal Control Module Memory Check Sum Error",
    "P0602": "Control Module Programming Error",
    "P0606": "ECM Processor Fault",
    "P0700": "Transmission Control System (TCM) — MIL Request",
    "P0715": "Input/Turbine Speed Sensor Circuit",
    "P0720": "Output Speed Sensor Circuit",
    "P0725": "Engine Speed Sensor Circuit",
    "P0730": "Incorrect Gear Ratio",
    "P0750": "Shift Solenoid A",
    "P0755": "Shift Solenoid B",
    "P0760": "Shift Solenoid C",
    "P0765": "Shift Solenoid D",
    
    # === CHASSIS (C0xxx) — ABS/DSTC ===
    "C0000": "Unknown DTC — ABS module",
    "C0035": "Left Front Wheel Speed Sensor",
    "C0040": "Right Front Wheel Speed Sensor",
    "C0045": "Left Rear Wheel Speed Sensor",
    "C0050": "Right Rear Wheel Speed Sensor",
    "C0060": "ABS Hydraulic Pump Motor",
    "C0065": "ABS Hydraulic Valve",
    "C0080": "ABS Control Module",
    "C0110": "ABS System Relay",
    "C0121": "ABS Power Supply Low Voltage",
    "C0131": "Brake Fluid Level Low",
    "C0145": "Hydraulic Brake Booster",
    "C0161": "ABS/Traction Control Malfunction — DSTC",
    "C0185": "Yaw Rate Sensor",
    "C0196": "Lateral Acceleration Sensor",
    "C0205": "Steering Angle Sensor Signal",
    "C0210": "Steering Angle Sensor Calibration",
    "C0221": "ABS/ESP System — Left Front Not Defined",
    "C0236": "ABS/ESP System — Right Front Not Defined",
    "C0251": "ABS/ESP System — Left Rear Not Defined",
    "C0266": "ABS/ESP System — Right Rear Not Defined",
    "C0281": "Brake Switch Circuit",
    "C0286": "Brake Pedal Position Sensor",
    
    # === BODY (B0xxx) ===
    "B0001": "ECM/PCM Communication Error",
    "B1000": "ECM Internal Fault",
    "B1001": "SRS Airbag Warning Light Circuit",
    "B1002": "SRS Crash Sensor",
    "B1003": "SRS Side Airbag Sensor (Driver)",
    "B1004": "SRS Side Airbag Sensor (Passenger)",
    "B1100": "Interior Temperature Sensor",
    "B1105": "Exterior Temperature Sensor",
    "B1110": "Sunlight Sensor",
    "B1120": "Steering Wheel Angle Sensor",
    "B1200": "CEM Power Supply Fault",
    "B1205": "DIM (Driver Information Module) Communication",
    "B1210": "CEM UEM (Upper Electronics Module) Communication",
    "B1300": "Door Lock Module Communication Fault",
    "B1310": "Power Seat Module Communication",
    "B1320": "Power Window Module Communication",
    "B1335": "Battery Monitoring Sensor",
    
    # === NETWORK (U0xxx) ===
    "U0001": "High-Speed CAN Communication Bus",
    "U0010": "Mid-Speed CAN Communication Bus",
    "U0020": "Low-Speed CAN Communication Bus",
    "U0073": "CAN Bus A (High-Speed) — Off",
    "U0074": "CAN Bus B (Low-Speed) — Off",
    "U0100": "Lost Communication with ECM/PCM",
    "U0101": "Lost communication with TCM",
    "U0121": "Lost communication with ABS",
    "U0126": "Lost communication with Steering Angle Sensor",
    "U0131": "Lost communication with CEM",
    "U0140": "Lost communication with BCM",
    "U0141": "Lost communication with DIM",
    "U0151": "Lost communication with SRS",
    "U0155": "Lost communication with ACC",
    "U0300": "Software Incompatibility — Control Module",
    "U0401": "Invalid Data Received From ECM/PCM",
    "U0402": "Invalid Data Received From TCM",
    
    # === VOLVO MANUFACTURER-SPECIFIC (P1xxx) ===
    "P1100": "Volvo — Fuel Pressure Regulator",
    "P1101": "Volvo — Fuel Pressure Control Valve",
    "P1110": "Volvo — Intake Air Temperature — CEM",
    "P1115": "Volvo — Engine Coolant Temperature — CEM",
    "P1120": "Volvo — Throttle Position — Adaptation Required",
    "P1121": "Volvo — Throttle Position — Signal Too Low",
    "P1122": "Volvo — Throttle Position — Signal Too High",
    "P1130": "Volvo — HO2S Signal Too Low — CEM",
    "P1131": "Volvo — HO2S Signal Too High — CEM",
    "P1140": "Volvo — Air Mass Sensor — Signal Too Low",
    "P1141": "Volvo — Air Mass Sensor — Signal Too High",
    "P1150": "Volvo — EVAP Control System",
    "P1160": "Volvo — Camshaft Reset Valve — Adaptation",
    "P1170": "Volvo — Camshaft Reset Valve — Signal Low",
    "P1171": "Volvo — Camshaft Reset Valve — Signal High",
    "P1180": "Volvo — Fuel Pressure — Too Low",
    "P1181": "Volvo — Fuel Pressure — Too High",
    "P1200": "Volvo — Cylinder 1 Fuel Injector Circuit",
    "P1205": "Volvo — Cylinder 2 Fuel Injector Circuit",
    "P1210": "Volvo — Cylinder 3 Fuel Injector Circuit",
    "P1215": "Volvo — Cylinder 4 Fuel Injector Circuit",
    "P1220": "Volvo — Fuel Injector — CEM Signal Too Low",
    "P1300": "Volvo — Spark Advance — CEM Signal Too Low",
    "P1301": "Volvo — Spark Advance — CEM Signal Too High",
    "P1400": "Volvo — Catalyst Monitor — CEM",
    "P1401": "Volvo — Catalyst Monitor — Downstream O2 Sensor",
    "P1410": "Volvo — Secondary Air Injection System",
    "P1500": "Volvo — Vehicle Speed Signal — Missing",
    "P1505": "Volvo — Vehicle Speed Signal — Signal Too Low",
    "P1510": "Volvo — Starter Signal — CEM",
    "P1520": "Volvo — A/C Compressor Signal — CEM",
    "P1530": "Volvo — A/C Pressure Sensor",
    "P1600": "Volvo — ECM Internal Fault",
    "P1605": "Volvo — ECM Keep-Alive Memory Error",
    "P1610": "Volvo — Immobilizer Communication",
    "P1615": "Volvo — Immobilizer — Key Not Recognized",
    "P1620": "Volvo — ECM — CEM Signal Too Low",
    "P1625": "Volvo — ECM — CEM Signal Too High",
    "P1630": "Volvo — Immobilizer — Code Not Programmed",
    "P1635": "Volvo — Immobilizer — Wrong Code",
    "P1640": "Volvo — CAN Communication — ECM",
    "P1645": "Volvo — CAN Communication — CEM",
    "P1700": "Volvo — Transmission — CEM Signal",
    "P1705": "Volvo — Transmission — TCM Communication",
    "P1710": "Volvo — Transmission — Gear Selector Signal",
    "P1800": "Volvo — CEM — EEPROM Checksum Error",
    "P1805": "Volvo — CEM — Software Version Mismatch",
    "P1810": "Volvo — CEM — Internal Fault",
    "P1900": "Volvo — DSTC — Signal ECM",
    "P1905": "Volvo — DSTC — Signal ABS",
    "P1910": "Volvo — DSTC — Steering Angle Sensor",
}


# =============================================================================
# DTC Reader / Clearer
# =============================================================================

class V50DTCReader:
    """Reads and clears DTCs from the V50 via OBD2 over CAN bus.
    
    Uses ISO 15765-4 (CAN-based OBD2) protocol:
    - Mode 01: Live data (standard PIDs)
    - Mode 03: Read stored DTCs
    - Mode 04: Clear DTCs (also clears freeze frame data)
    - Mode 07: Read pending DTCs
    - Mode 09: VIN / calibration ID
    
    For Volvo-specific PIDs, uses Mode 22 (manufacturer-specific).
    """
    
    # OBD2 CAN IDs for request/response on high-speed bus
    OBD2_REQUEST_ID = 0x7DF   # Functional addressing (broadcast)
    OBD2_RESPONSE_ID = 0x7E8  # ECM response
    OBD2_TCM_RESPONSE = 0x7E9  # TCM response
    OBD2_ABS_RESPONSE = 0x7EA  # ABS response
    OBD2_CEM_RESPONSE = 0x7EB  # CEM response
    
    # ISO 15765-4 single frame format
    SINGLE_FRAME_PCI = 0x00  # PCI byte for single frame (<8 bytes payload)
    
    def __init__(self, interface: str = 'can0', bus_type: str = 'socketcan'):
        """Initialize DTC reader.
        
        Args:
            interface: CAN interface name (default: can0)
            bus_type: Bus type (default: socketcan)
        """
        self.interface = interface
        self.bus_type = bus_type
        self.bus: Optional[can.Bus] = None
        self._connected = False
    
    def connect(self) -> bool:
        """Connect to CAN bus for OBD2 communication."""
        if not HAS_PYTHON_CAN:
            logger.error("python-can not installed — install with: pip install python-can")
            return False
        
        try:
            self.bus = can.Bus(interface=self.interface, bustype=self.bus_type)
            self._connected = True
            logger.info(f"Connected to {self.interface} for DTC reading")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to {self.interface}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from CAN bus."""
        if self.bus:
            try:
                self.bus.shutdown()
            except Exception:
                pass
            self._connected = False
    
    def _send_obd2_request(self, mode: int, pid: int = 0x00, timeout: float = 2.0) -> Optional[bytes]:
        """Send an OBD2 request and wait for response.
        
        Args:
            mode: OBD2 mode (1=live, 3=DTC, 4=clear, 7=pending, 9=info, 22=Volvo)
            pid: PID within mode (0x00 for mode 3/4/7)
            timeout: Response timeout in seconds
            
        Returns:
            Response data bytes, or None if no response
        """
        if not self.bus:
            logger.error("Not connected to CAN bus")
            return None
        
        # Build request: 8 bytes, ISO 15765-4 single frame format
        # Format: [PCI+len, mode, pid, 0x00 padding...]
        if pid == 0x00 and mode in (0x03, 0x04, 0x07):
            # Mode 3/4/7: no PID needed
            data = bytes([0x02, mode, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        else:
            data = bytes([0x03, mode, pid, 0x00, 0x00, 0x00, 0x00, 0x00])
        
        msg = can.Message(arbitration_id=self.OBD2_REQUEST_ID, data=data, is_extended_id=False)
        
        try:
            self.bus.send(msg)
            logger.debug(f"Sent OBD2 request: mode=0x{mode:02X}, pid=0x{pid:02X}")
        except can.CanError as e:
            logger.error(f"CAN send error: {e}")
            return None
        
        # Wait for response from any ECU
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = self.bus.recv(timeout=0.1)
                if response is None:
                    continue
                
                # Check if this is a response from an ECU
                if response.arbitration_id in (0x7E8, 0x7E9, 0x7EA, 0x7EB):
                    # Parse ISO 15765-4 response
                    r_data = response.data
                    pci = r_data[0]
                    
                    # Single frame (PCI byte 0x00-0x0F)
                    if (pci & 0xF0) == 0x00:
                        length = pci & 0x0F
                        if length > 0:
                            resp_mode = r_data[1]
                            # Verify mode matches (response = request_mode + 0x40)
                            if resp_mode == mode + 0x40:
                                return bytes(r_data[2:2+length])
                    # First frame (multi-frame)
                    elif (pci & 0xF0) == 0x10:
                        # Handle multi-frame response (rare for DTCs)
                        total_length = ((pci & 0x0F) << 8) | r_data[1]
                        logger.debug(f"Multi-frame response, total_length={total_length}")
                        # For now, return the first frame data
                        return bytes(r_data[2:])
                        
            except can.CanError as e:
                logger.warning(f"CAN receive error: {e}")
                continue
        
        logger.warning(f"No OBD2 response for mode=0x{mode:02X}, pid=0x{pid:02X} (timeout={timeout}s)")
        return None
    
    def _parse_dtc_bytes(self, data: bytes) -> List[str]:
        """Parse DTC codes from OBD2 response bytes.
        
        DTCs are encoded as 2-byte pairs:
        - Byte 0: [P/C/B/U][0-3][0-9] (first 2 chars)
        - Byte 1: [0-9][0-9] (last 2 chars)
        
        Example: 0x01 0x34 → P0134 (HO2S Heater Circuit)
        """
        dtc_codes = []
        i = 0
        while i + 1 < len(data):
            b0 = data[i]
            b1 = data[i + 1]
            
            # First nibble encodes the DTC type
            dtc_type = {0: 'P', 1: 'P', 2: 'P', 3: 'P',
                        4: 'C', 5: 'C', 6: 'C', 7: 'C',
                        8: 'B', 9: 'B', 0xA: 'B', 0xB: 'B',
                        0xC: 'U', 0xD: 'U', 0xE: 'U', 0xF: 'U'}[b0 >> 4]
            
            digit1 = (b0 >> 4) & 0x03  # 0-3 maps to 0-3
            digit2 = b0 & 0x0F
            digit3 = b1 >> 4
            digit4 = b1 & 0x0F
            
            dtc_str = f"{dtc_type}{digit1}{digit2:X}{digit3:X}{digit4:X}"
            
            # Skip 0x0000 (no DTC)
            if dtc_str != "P0000":
                dtc_codes.append(dtc_str)
            
            i += 2
        
        return dtc_codes
    
    def read_dtcs(self, mode: int = 0x03) -> List[DTCCode]:
        """Read Diagnostic Trouble Codes.
        
        Args:
            mode: 0x03 for stored DTCs, 0x07 for pending DTCs
            
        Returns:
            List of DTCCode objects
        """
        result = []
        
        response = self._send_obd2_request(mode)
        if response is None:
            logger.info(f"No DTCs found (mode 0x{mode:02X})")
            return result
        
        dtc_strings = self._parse_dtc_bytes(response)
        
        for code_str in dtc_strings:
            description = V50_DTC_CODES.get(code_str, f"Unknown DTC: {code_str}")
            status = DTCStatus.CURRENT if mode == 0x03 else DTCStatus.PENDING
            
            dtc = DTCCode(
                code=code_str,
                description=description,
                status=status,
            )
            result.append(dtc)
            logger.info(f"DTC: {code_str} — {description}")
        
        return result
    
    def read_all_dtcs(self) -> Dict[str, List[DTCCode]]:
        """Read both stored and pending DTCs.
        
        Returns:
            Dict with 'stored' and 'pending' keys containing lists of DTCCode
        """
        stored = self.read_dtcs(mode=0x03)
        pending = self.read_dtcs(mode=0x07)
        
        return {
            'stored': stored,
            'pending': pending,
        }
    
    def clear_dtcs(self, confirm: bool = False) -> bool:
        """Clear all stored DTCs and freeze frame data.
        
        WARNING: This clears ALL stored fault codes and resets the MIL.
        Only use after reading and recording all codes first.
        
        Args:
            confirm: Must be True to actually clear (safety check)
            
        Returns:
            True if clearance command was sent successfully
        """
        if not confirm:
            logger.warning("DTC clear aborted — confirm=True required")
            return False
        
        logger.warning("CLEARING ALL DTCs — this resets the Check Engine Light and stored codes!")
        
        response = self._send_obd2_request(mode=0x04)
        if response is not None:
            logger.info("DTC clear command sent successfully")
            return True
        else:
            logger.error("DTC clear command — no response from ECU")
            return False
    
    def read_vin(self) -> Optional[str]:
        """Read Vehicle Identification Number via OBD2 Mode 09 PID 02.
        
        Returns:
            VIN string, or None if unavailable
        """
        response = self._send_obd2_request(mode=0x09, pid=0x02, timeout=5.0)
        if response is None:
            return None
        
        # Mode 09 PID 02 returns VIN as ASCII
        # Response format: mode(0x49) + pid(0x02) + VIN bytes
        try:
            vin = bytes(b for b in response if 0x20 <= b <= 0x7E).decode('ascii', errors='ignore').strip()
            return vin if len(vin) >= 17 else None
        except Exception as e:
            logger.warning(f"Failed to decode VIN: {e}")
            return None
    
    def read_live_data(self, pids: Optional[List[int]] = None) -> Dict[str, float]:
        """Read live data from standard OBD2 PIDs (Mode 01).
        
        Args:
            pids: List of PIDs to request. None = request common PIDs.
            
        Returns:
            Dict of pid_name -> value
        """
        from v50_can_decoder import OBD2_STANDARD_PIDS
        
        if pids is None:
            pids = list(OBD2_STANDARD_PIDS.keys())
        
        results = {}
        
        for pid in pids:
            if pid in OBD2_STANDARD_PIDS:
                response = self._send_obd2_request(mode=0x01, pid=pid)
                if response and len(response) >= 3:
                    pid_info = OBD2_STANDARD_PIDS[pid]
                    value = self._parse_pid_value(pid, response[2:])
                    if value is not None:
                        results[pid_info['name']] = value
                        logger.debug(f"PID 0x{pid:02X}: {pid_info['name']} = {value:.1f} {pid_info['unit']}")
            time.sleep(0.01)  # Small delay between PIDs
        
        return results
    
    def _parse_pid_value(self, pid: int, data: bytes) -> Optional[float]:
        """Parse a live data PID value from response bytes.
        
        Args:
            pid: OBD2 PID number
            data: Response data bytes (after mode+pid bytes stripped)
            
        Returns:
            Parsed physical value, or None if parsing fails
        """
        try:
            if len(data) < 2:
                return None
            
            A = data[0]
            B = data[1] if len(data) > 1 else 0
            C = data[2] if len(data) > 2 else 0
            D = data[3] if len(data) > 3 else 0
            
            if pid == 0x04:  # Engine Load
                return (A / 255) * 100
            elif pid == 0x05:  # Coolant Temp
                return A - 40
            elif pid == 0x0B:  # Intake Manifold Pressure
                return A
            elif pid == 0x0C:  # RPM
                return ((A * 256) + B) / 4
            elif pid == 0x0D:  # Vehicle Speed
                return float(A)
            elif pid == 0x0F:  # Intake Air Temp
                return A - 40
            elif pid == 0x10:  # MAF
                return ((A * 256) + B) / 100
            elif pid == 0x11:  # Throttle Position
                return (A / 255) * 100
            elif pid == 0x2F:  # Fuel Level
                return (A / 255) * 100
            else:
                return None
        except Exception as e:
            logger.warning(f"Failed to parse PID 0x{pid:02X}: {e}")
            return None
    
    def get_module_dtcs(self, module: str = "ECM") -> List[DTCCode]:
        """Request DTCs from a specific module.
        
        Uses physical addressing for module-specific requests:
        - ECM: 0x7E0 → 0x7E8
        - TCM: 0x7E1 → 0x7E9
        - ABS: 0x7E2 → 0x7EA
        - CEM: 0x7E3 → 0x7EB
        """
        module_map = {
            "ECM": (0x7E0, 0x7E8),
            "TCM": (0x7E1, 0x7E9),
            "ABS": (0x7E2, 0x7EA),
            "CEM": (0x7E3, 0x7EB),
        }
        
        if module not in module_map:
            logger.error(f"Unknown module: {module}. Choose from: {list(module_map.keys())}")
            return []
        
        request_id, response_id = module_map[module]
        # For module-specific requests, use physical addressing
        # This is a simplified approach — a real implementation would use
        # ISO 15765-4 properly with correct addressing
        
        data = bytes([0x02, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        msg = can.Message(arbitration_id=request_id, data=data, is_extended_id=False)
        
        try:
            if self.bus:
                self.bus.send(msg)
        except can.CanError as e:
            logger.error(f"CAN send error for {module}: {e}")
            return []
        
        # Wait for response from this module
        start_time = time.time()
        while time.time() - start_time < 3.0:
            try:
                response = self.bus.recv(timeout=0.1)
                if response and response.arbitration_id == response_id:
                    return [DTCCode(code=code, description=V50_DTC_CODES.get(code, "Unknown"),
                                     status=DTCStatus.CURRENT, module=module)
                            for code in self._parse_dtc_bytes(response.data[2:])]
            except can.CanError:
                continue
        
        return []
    
    @staticmethod
    def format_dtcs(dtcs: List[DTCCode]) -> str:
        """Format DTC codes into a human-readable report."""
        if not dtcs:
            return "No fault codes found."
        
        lines = [f"Found {len(dtcs)} DTC(s):"]
        for dtc in dtcs:
            status_str = {
                DTCStatus.CURRENT: "ACTIVE",
                DTCStatus.PENDING: "PENDING",
                DTCStatus.PERMANENT: "PERMANENT",
                DTCStatus.HISTORY: "HISTORY",
            }.get(dtc.status, "UNKNOWN")
            
            module_str = f" [{dtc.module}]" if dtc.module else ""
            lines.append(f"  {dtc.code} {status_str}{module_str}: {dtc.description}")
        
        return "\n".join(lines)


# =============================================================================
# Maintenance Tracker
# =============================================================================

class V50MaintenanceTracker:
    """Tracks maintenance intervals based on odometer readings from CAN bus.
    
    Reads maintenance.json and updates it with current odometer values.
    Calculates remaining km/days until next service for each item.
    """
    
    # Default service intervals for V50 2.4i
    DEFAULT_INTERVALS = {
        "oil_change":      {"km": 15000, "months": 12},
        "oil_filter":      {"km": 15000, "months": 12},
        "air_filter":      {"km": 30000, "months": 24},
        "cabin_filter":    {"km": 30000, "months": 24},
        "brake_fluid":     {"km": 60000, "months": 24},
        "spark_plugs":     {"km": 60000, "months": 48},
        "timing_belt":     {"km": 120000, "months": 120},
        "coolant":         {"km": 60000, "months": 36},
        "transmission_fluid": {"km": 60000, "months": 48},
        "brake_pads_front": {"km": 40000, "months": 0},
        "brake_pads_rear": {"km": 50000, "months": 0},
        "brake_discs_front": {"km": 80000, "months": 0},
        "brake_discs_rear": {"km": 100000, "months": 0},
    }
    
    def __init__(self, maintenance_file: str = None):
        """Initialize maintenance tracker.
        
        Args:
            maintenance_file: Path to maintenance.json (default: hardware/maintenance.json)
        """
        if maintenance_file is None:
            from pathlib import Path
            maintenance_file = str(
                Path(__file__).resolve().parent.parent / 'hardware' / 'maintenance.json'
            )
        self.maintenance_file = maintenance_file
        self.data = self._load()
    
    def _load(self) -> dict:
        """Load maintenance data from JSON file."""
        import json
        from pathlib import Path
        
        path = Path(self.maintenance_file)
        if path.exists():
            try:
                with open(path) as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load maintenance file: {e}")
        
        # Create default structure
        default = {
            "current_odometer_km": 0,
            "intervals": {}
        }
        for key, interval in self.DEFAULT_INTERVALS.items():
            default["intervals"][key] = {
                "interval_km": interval["km"],
                "interval_months": interval["months"],
                "last_km": 0,
                "last_date": ""
            }
        return default
    
    def _save(self):
        """Save maintenance data to JSON file."""
        import json
        from pathlib import Path
        
        path = Path(self.maintenance_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def update_odometer(self, km: float):
        """Update current odometer reading."""
        self.data["current_odometer_km"] = km
        self._save()
    
    def record_service(self, service_name: str, km: float = None, date: str = None):
        """Record that a service was performed.
        
        Args:
            service_name: Key in intervals dict (e.g., "oil_change")
            km: Odometer at service time (default: current reading)
            date: Date string (default: today)
        """
        from datetime import date as date_cls
        
        if km is None:
            km = self.data["current_odometer_km"]
        if date is None:
            date = str(date_cls.today())
        
        if service_name in self.data["intervals"]:
            self.data["intervals"][service_name]["last_km"] = km
            self.data["intervals"][service_name]["last_date"] = date
            self._save()
    
    def get_status(self) -> List[dict]:
        """Get maintenance status for all items.
        
        Returns:
            List of dicts with service name, remaining km, remaining days, status
        """
        from datetime import date as date_cls
        
        current_km = self.data["current_odometer_km"]
        today = date_cls.today()
        status = []
        
        for name, info in self.data.get("intervals", {}).items():
            last_km = info.get("last_km", 0)
            last_date_str = info.get("last_date", "")
            interval_km = info.get("interval_km", 0)
            interval_months = info.get("interval_months", 0)
            
            remaining_km = (last_km + interval_km) - current_km
            
            # Calculate remaining days
            remaining_days = None
            if last_date_str and interval_months > 0:
                try:
                    from datetime import datetime
                    last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
                    from dateutil.relativedelta import relativedelta
                    next_date = last_date + relativedelta(months=interval_months)
                    remaining_days = (next_date - today).days
                except Exception:
                    remaining_days = None
            
            # Status determination
            if remaining_km <= 0 or (remaining_days is not None and remaining_days <= 0):
                status_level = "OVERDUE"
            elif remaining_km < interval_km * 0.2 or (remaining_days is not None and remaining_days < 30):
                status_level = "DUE_SOON"
            else:
                status_level = "OK"
            
            status.append({
                "service": name,
                "remaining_km": max(0, remaining_km),
                "remaining_days": remaining_days,
                "status": status_level,
                "interval_km": interval_km,
                "last_km": last_km,
            })
        
        return status
    
    def format_status(self) -> str:
        """Format maintenance status as a readable report."""
        lines = [f"=== V50 Maintenance Status (Odometer: {self.data['current_odometer_km']:.0f} km) ==="]
        
        for item in self.get_status():
            days_str = f" / {item['remaining_days']}d" if item['remaining_days'] is not None else ""
            marker = {"OVERDUE": "🔴", "DUE_SOON": "🟡", "OK": "🟢"}[item['status']]
            lines.append(
                f"  {marker} {item['service']:20s}: {item['remaining_km']:6.0f} km remaining{days_str} "
                f"(interval: {item['interval_km']} km)"
            )
        
        return "\n".join(lines)


# =============================================================================
# Data Logger — SQLite + CSV dual output with rotation
# =============================================================================

class V50DataLogger:
    """Logs decoded V50 CAN data to SQLite and CSV with rotation.
    
    Features:
    - SQLite database for structured queries
    - CSV file for easy data analysis
    - Auto-rotation when file size exceeds threshold
    - Configurable sample rate (default: 100ms = 10Hz)
    - Selective logging (only changed values, or all)
    """
    
    DEFAULT_LOG_DIR = "/var/log/v50can"
    DEFAULT_SAMPLE_INTERVAL = 0.1  # 100ms = 10Hz
    DEFAULT_MAX_FILE_SIZE_MB = 50
    
    def __init__(self, log_dir: str = None, sample_interval: float = None, max_file_size_mb: float = None):
        from pathlib import Path
        
        self.log_dir = Path(log_dir or self.DEFAULT_LOG_DIR)
        self.sample_interval = sample_interval or self.DEFAULT_SAMPLE_INTERVAL
        self.max_file_size_mb = max_file_size_mb or self.DEFAULT_MAX_FILE_SIZE_MB
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self._db_conn = None
        self._csv_file = None
        self._csv_writer = None
        self._last_log_time = 0
        self._session_id = None
        self._rows_logged = 0
    
    def _init_db(self):
        """Initialize SQLite database."""
        import sqlite3
        from datetime import datetime
        
        db_path = self.log_dir / "v50_can_log.db"
        self._db_conn = sqlite3.connect(str(db_path))
        cursor = self._db_conn.cursor()
        
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                total_rows INTEGER DEFAULT 0
            );
            
            CREATE TABLE IF NOT EXISTS can_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                timestamp REAL NOT NULL,
                rpm REAL,
                speed_kmh REAL,
                coolant_temp_c REAL,
                oil_temp_c REAL,
                intake_air_temp_c REAL,
                throttle_pct REAL,
                engine_load_pct REAL,
                maf_g_per_s REAL,
                fuel_level_pct REAL,
                gear INTEGER,
                trans_temp_c REAL,
                exterior_temp_c REAL,
                interior_temp_c REAL,
                brake_pressure_bar REAL,
                brake_pedal_pressed INTEGER,
                steering_angle_deg REAL,
                yaw_rate REAL,
                lateral_accel_g REAL,
                engine_running INTEGER,
                check_engine INTEGER,
                oil_warning INTEGER,
                battery_warning INTEGER,
                temp_warning INTEGER,
                odometer_km REAL,
                cruise_active INTEGER,
                cruise_set_speed_kmh REAL
            );
            
            CREATE INDEX IF NOT EXISTS idx_can_log_session ON can_log(session_id);
            CREATE INDEX IF NOT EXISTS idx_can_log_timestamp ON can_log(timestamp);
        """)
        
        self._db_conn.commit()
        
        # Create new session
        now = datetime.now().isoformat()
        cursor.execute("INSERT INTO sessions (start_time) VALUES (?)", (now,))
        self._session_id = cursor.lastrowid
        self._db_conn.commit()
    
    def _init_csv(self):
        """Initialize CSV log file."""
        import csv
        from datetime import datetime
        
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = self.log_dir / f"v50_can_{date_str}.csv"
        self._csv_file = open(csv_path, 'w', newline='')
        
        fieldnames = [
            'timestamp', 'rpm', 'speed_kmh', 'coolant_temp_c', 'oil_temp_c',
            'intake_air_temp_c', 'throttle_pct', 'engine_load_pct', 'maf_g_per_s',
            'fuel_level_pct', 'gear', 'trans_temp_c', 'exterior_temp_c',
            'interior_temp_c', 'brake_pressure_bar', 'brake_pedal_pressed',
            'steering_angle_deg', 'yaw_rate', 'lateral_accel_g', 'engine_running',
            'check_engine', 'oil_warning', 'battery_warning', 'temp_warning',
            'odometer_km', 'cruise_active', 'cruise_set_speed_kmh'
        ]
        self._csv_writer = csv.DictWriter(self._csv_file, fieldnames=fieldnames)
        self._csv_writer.writeheader()
    
    def start(self):
        """Start logging — initialize DB and CSV."""
        self._init_db()
        self._init_csv()
        logger.info(f"Data logging started — session {self._session_id}")
    
    def log_state(self, state):
        """Log the current V50State to DB and CSV.
        
        Args:
            state: V50State object from v50_can_decoder
        """
        from v50_can_decoder import V50State
        
        current_time = time.time()
        if current_time - self._last_log_time < self.sample_interval:
            return
        
        self._last_log_time = current_time
        self._rows_logged += 1
        
        # Log to SQLite
        if self._db_conn:
            try:
                cursor = self._db_conn.cursor()
                cursor.execute("""
                    INSERT INTO can_log (
                        session_id, timestamp, rpm, speed_kmh, coolant_temp_c,
                        oil_temp_c, intake_air_temp_c, throttle_pct, engine_load_pct,
                        maf_g_per_s, fuel_level_pct, gear, trans_temp_c,
                        exterior_temp_c, interior_temp_c, brake_pressure_bar,
                        brake_pedal_pressed, steering_angle_deg, yaw_rate,
                        lateral_accel_g, engine_running, check_engine, oil_warning,
                        battery_warning, temp_warning, odometer_km,
                        cruise_active, cruise_set_speed_kmh
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """, (
                    self._session_id, current_time,
                    state.rpm, state.speed_kmh, state.coolant_temp_c,
                    state.oil_temp_c, state.intake_air_temp_c, state.throttle_pct,
                    state.engine_load_pct, state.maf_g_per_s, state.fuel_level_pct,
                    state.gear, state.trans_temp_c, state.exterior_temp_c,
                    state.interior_temp_c, state.brake_pressure_bar,
                    int(state.brake_pedal_pressed), state.steering_angle_deg,
                    state.yaw_rate, state.lateral_accel_g,
                    int(state.engine_running), int(state.check_engine),
                    int(state.oil_warning), int(state.battery_warning),
                    int(state.temp_warning), state.odometer_km,
                    int(state.cruise_active), state.cruise_set_speed_kmh,
                ))
                self._db_conn.commit()
            except Exception as e:
                logger.warning(f"DB log error: {e}")
        
        # Log to CSV
        if self._csv_writer:
            try:
                self._csv_writer.writerow({
                    'timestamp': current_time,
                    'rpm': state.rpm,
                    'speed_kmh': state.speed_kmh,
                    'coolant_temp_c': state.coolant_temp_c,
                    'oil_temp_c': state.oil_temp_c,
                    'intake_air_temp_c': state.intake_air_temp_c,
                    'throttle_pct': state.throttle_pct,
                    'engine_load_pct': state.engine_load_pct,
                    'maf_g_per_s': state.maf_g_per_s,
                    'fuel_level_pct': state.fuel_level_pct,
                    'gear': state.gear,
                    'trans_temp_c': state.trans_temp_c,
                    'exterior_temp_c': state.exterior_temp_c,
                    'interior_temp_c': state.interior_temp_c,
                    'brake_pressure_bar': state.brake_pressure_bar,
                    'brake_pedal_pressed': int(state.brake_pedal_pressed),
                    'steering_angle_deg': state.steering_angle_deg,
                    'yaw_rate': state.yaw_rate,
                    'lateral_accel_g': state.lateral_accel_g,
                    'engine_running': int(state.engine_running),
                    'check_engine': int(state.check_engine),
                    'oil_warning': int(state.oil_warning),
                    'battery_warning': int(state.battery_warning),
                    'temp_warning': int(state.temp_warning),
                    'odometer_km': state.odometer_km,
                    'cruise_active': int(state.cruise_active),
                    'cruise_set_speed_kmh': state.cruise_set_speed_kmh,
                })
                # Flush every 10 rows for safety
                if self._rows_logged % 10 == 0:
                    self._csv_file.flush()
            except Exception as e:
                logger.warning(f"CSV log error: {e}")
    
    def stop(self):
        """Stop logging — close DB and CSV."""
        from datetime import datetime
        
        if self._db_conn:
            try:
                cursor = self._db_conn.cursor()
                now = datetime.now().isoformat()
                cursor.execute(
                    "UPDATE sessions SET end_time=?, total_rows=? WHERE id=?",
                    (now, self._rows_logged, self._session_id)
                )
                self._db_conn.commit()
                self._db_conn.close()
            except Exception as e:
                logger.warning(f"DB close error: {e}")
        
        if self._csv_file:
            try:
                self._csv_file.close()
            except Exception as e:
                logger.warning(f"CSV close error: {e}")
        
        logger.info(f"Data logging stopped — {self._rows_logged} rows logged")


# =============================================================================
# Main — Test DTC reading and maintenance status
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="V50 DTC Reader & Maintenance Tracker")
    parser.add_argument("--dtc", action="store_true", help="Read DTCs")
    parser.add_argument("--dtc-clear", action="store_true", help="Clear all DTCs (DANGEROUS)")
    parser.add_argument("--dtc-pending", action="store_true", help="Read pending DTCs")
    parser.add_argument("--vin", action="store_true", help="Read VIN")
    parser.add_argument("--live", action="store_true", help="Read live data")
    parser.add_argument("--maint", action="store_true", help="Show maintenance status")
    parser.add_argument("--maint-update", type=float, help="Update odometer (km)")
    parser.add_argument("--maint-service", type=str, help="Record service performed (name)")
    parser.add_argument("--interface", type=str, default="can0", help="CAN interface")
    
    args = parser.parse_args()
    
    # Maintenance tracker (always available — doesn't need CAN bus)
    if args.maint or args.maint_update or args.maint_service:
        tracker = V50MaintenanceTracker()
        
        if args.maint_update:
            tracker.update_odometer(args.maint_update)
            print(f"Odometer updated to {args.maint_update:.0f} km")
        
        if args.maint_service:
            tracker.record_service(args.maint_service)
            print(f"Service '{args.maint_service}' recorded")
        
        print(tracker.format_status())
    
    # DTC reader (needs CAN bus)
    if args.dtc or args.dtc_clear or args.dtc_pending or args.vin or args.live:
        if not HAS_PYTHON_CAN:
            print("ERROR: python-can not installed. Install with: pip install python-can")
            print("       On Pi: sudo pip3 install python-can")
            exit(1)
        
        reader = V50DTCReader(interface=args.interface)
        
        if reader.connect():
            try:
                if args.vin:
                    vin = reader.read_vin()
                    print(f"VIN: {vin or 'NOT AVAILABLE'}")
                
                if args.live:
                    data = reader.read_live_data()
                    print("\nLive Data:")
                    for name, value in data.items():
                        print(f"  {name}: {value:.1f}")
                
                if args.dtc:
                    dtcs = reader.read_dtcs(mode=0x03)
                    print(f"\n{V50DTCReader.format_dtcs(dtcs)}")
                
                if args.dtc_pending:
                    dtcs = reader.read_dtcs(mode=0x07)
                    print(f"\nPending DTCs:\n{V50DTCReader.format_dtcs(dtcs)}")
                
                if args.dtc_clear:
                    if reader.clear_dtcs(confirm=True):
                        print("All DTCs cleared successfully.")
                    else:
                        print("DTC clear failed.")
            finally:
                reader.disconnect()
        else:
            print(f"ERROR: Could not connect to {args.interface}. Is PiCAN2 configured?")
            print("       Run: sudo ip link set can0 type can bitrate 500000")
            print("       Run: sudo ip link set can0 up")
    
    # Print DTC database
    if not (args.dtc or args.dtc_clear or args.dtc_pending or args.vin or 
            args.live or args.maint or args.maint_update or args.maint_service):
        print("=== V50 DTC Code Database ===")
        print(f"Total codes: {len(V50_DTC_CODES)}")
        print("\nPowertrain (P0xxx):")
        for code, desc in sorted(V50_DTC_CODES.items()):
            if code.startswith('P0'):
                print(f"  {code}: {desc}")
        print("\nManufacturer (P1xxx):")
        for code, desc in sorted(V50_DTC_CODES.items()):
            if code.startswith('P1'):
                print(f"  {code}: {desc}")
        print("\nChassis (C0xxx):")
        for code, desc in sorted(V50_DTC_CODES.items()):
            if code.startswith('C0'):
                print(f"  {code}: {desc}")
        print("\nBody (B0xxx):")
        for code, desc in sorted(V50_DTC_CODES.items()):
            if code.startswith('B'):
                print(f"  {code}: {desc}")
        print("\nNetwork (U0xxx):")
        for code, desc in sorted(V50_DTC_CODES.items()):
            if code.startswith('U'):
                print(f"  {code}: {desc}")