#!/usr/bin/env python3
"""Volvo V50 2.4i BLE/Bluetooth Data Server
=========================================
Streams decoded CAN-bus data to a smartphone via Bluetooth RFCOMM
or TCP (for testing without BT hardware).

Protocol:
  Server sends JSON lines (one per update cycle):
  {"rpm":3200,"spd":120.5,"clt":88,"oil":82,...}

  Client can send commands:
  - "START" -> begin streaming
  - "STOP" -> pause streaming
  - "DTC" -> request DTC read
  - "MAINT" -> request maintenance status
  - "RESET" -> reset connection

Author: v50-developer agent
Date: 2026-05-28
"""

import argparse
import json
import logging
import socket
import threading
import time
from pathlib import Path
from typing import Optional, Dict, List, Callable

from v50_can_decoder import (
    V50State, CANBus, MESSAGE_DEFINITIONS,
    decode_message, get_gear_name, calculate_fuel_consumption
)

logger = logging.getLogger('v50.ble_server')


# Configuration
RFCOMM_PORT = 1
UPDATE_INTERVAL = 0.5  # 2 Hz
MAX_CLIENTS = 1
CLIENT_TIMEOUT = 30


def state_to_json(state: V50State) -> str:
    """Serialize V50State to compact JSON for BT transmission."""
    data = {
        "rpm": round(state.rpm, 0),
        "spd": round(state.speed_kmh, 1),
        "clt": round(state.coolant_temp_c, 0),
        "oilt": round(state.oil_temp_c, 0),
        "iat": round(state.intake_air_temp_c, 0),
        "thr": round(state.throttle_pct, 1),
        "load": round(state.engine_load_pct, 1),
        "maf": round(state.maf_g_per_s, 1),
        "fuel": round(state.fuel_level_pct, 1),
        "gear": get_gear_name(state.gear),
        "trnt": round(state.trans_temp_c, 0),
        "odo": round(state.odometer_km, 0),
        "cel": state.check_engine,
        "oil_w": state.oil_warning,
        "bat_w": state.battery_warning,
        "tmp_w": state.temp_warning,
        "int_t": round(state.interior_temp_c, 0),
        "ext_t": round(state.exterior_temp_c, 0),
        "ac": state.ac_active,
        "fan": state.fan_speed,
        "dr_open": state.driver_door_open,
        "dr_lock": state.driver_door_locked,
        "ps_open": state.pass_door_open,
        "brk_bar": round(state.brake_pressure_bar, 1),
        "steer_deg": round(state.steering_angle_deg, 1),
        "ws_fl": round(state.wheel_speed_fl, 0),
        "ws_fr": round(state.wheel_speed_fr, 0),
    }
    return json.dumps(data, separators=(',', ':'))


def dtc_to_json(dtcs: List[Dict]) -> str:
    """Serialize DTC list to JSON."""
    return json.dumps({"type": "dtc", "codes": dtcs}, separators=(',', ':'))


def maintenance_to_json(status: List[Dict]) -> str:
    """Serialize maintenance status to JSON."""
    compact = [{"item": s["item"], "rem_km": round(s["km_remaining"], 0),
                "status": s["status"]} for s in status]
    return json.dumps({"type": "maint", "items": compact}, separators=(',', ':'))


class RFCOMMServer:
    """Bluetooth RFCOMM (Serial Port Profile) server for V50 data streaming.

    Requires: sudo apt install bluetooth pi-bluetooth
    Pair smartphone with Pi first, then connect via SPP app.
    """

    def __init__(self, state: V50State, port: int = RFCOMM_PORT):
        self.state = state
        self.port = port
        self.server_sock = None
        self.client_sock = None
        self.running = False
        self.streaming = False
        self.client_address = None
        self.last_client_activity = time.time()
        self.on_dtc_request: Optional[Callable] = None
        self.on_maint_request: Optional[Callable] = None
        self.messages_sent = 0
        self.bytes_sent = 0
        self.start_time = None

    def start(self):
        """Start the RFCOMM server."""
        try:
            self.server_sock = socket.socket(
                socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM
            )
            self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_sock.bind(('', self.port))
            self.server_sock.listen(MAX_CLIENTS)
            self.running = True
            self.start_time = time.time()

            logger.info(f"RFCOMM server listening on channel {self.port}")

            while self.running:
                try:
                    self.server_sock.settimeout(1.0)
                    try:
                        self.client_sock, self.client_address = self.server_sock.accept()
                    except socket.timeout:
                        continue

                    logger.info(f"Client connected: {self.client_address}")
                    self._handle_client()

                except OSError as e:
                    if self.running:
                        logger.error(f"Accept error: {e}")
                    break

        except Exception as e:
            logger.error(f"RFCOMM server error: {e}")
            logger.info("Enable Bluetooth: sudo systemctl start bluetooth")
        finally:
            self.stop()

    def stop(self):
        """Stop the server."""
        self.running = False
        self.streaming = False
        if self.client_sock:
            try: self.client_sock.close()
            except: pass
            self.client_sock = None
        if self.server_sock:
            try: self.server_sock.close()
            except: pass
            self.server_sock = None
        logger.info("RFCOMM server stopped")

    def _handle_client(self):
        """Handle a connected client."""
        self.streaming = True
        self.last_client_activity = time.time()
        self.client_sock.settimeout(0.1)

        try:
            while self.running and self.client_sock:
                try:
                    cmd = self.client_sock.recv(256).decode('utf-8', errors='ignore').strip()
                    if cmd:
                        self.last_client_activity = time.time()
                        self._process_command(cmd)
                except socket.timeout:
                    pass
                except ConnectionError:
                    break

                if self.streaming:
                    try:
                        payload = state_to_json(self.state) + "\n"
                        data = payload.encode('utf-8')
                        self.client_sock.send(data)
                        self.messages_sent += 1
                        self.bytes_sent += len(data)
                    except ConnectionError:
                        break

                time.sleep(UPDATE_INTERVAL)
        finally:
            if self.client_sock:
                try: self.client_sock.close()
                except: pass
                self.client_sock = None

    def _process_command(self, cmd: str):
        """Process client command."""
        cmd = cmd.upper().strip()
        if cmd == "START":
            self.streaming = True
        elif cmd == "STOP":
            self.streaming = False
        elif cmd == "DTC" and self.on_dtc_request:
            dtcs = self.on_dtc_request()
            if dtcs:
                payload = dtc_to_json(dtcs) + "\n"
                self.client_sock.send(payload.encode('utf-8'))
        elif cmd == "MAINT" and self.on_maint_request:
            status = self.on_maint_request()
            if status:
                payload = maintenance_to_json(status) + "\n"
                self.client_sock.send(payload.encode('utf-8'))
        elif cmd == "RESET":
            self.streaming = False
            self.messages_sent = 0

    def get_stats(self) -> Dict:
        """Return server statistics."""
        uptime = time.time() - self.start_time if self.start_time else 0
        return {
            "running": self.running,
            "streaming": self.streaming,
            "client_connected": self.client_sock is not None,
            "messages_sent": self.messages_sent,
            "bytes_sent": self.bytes_sent,
            "uptime_seconds": round(uptime, 0),
        }


class TCPServer:
    """TCP server for V50 data streaming - fallback when no Bluetooth.

    Works over WiFi. Use for development/testing on non-Pi hardware.
    Connect with: nc <pi_ip> 5050
    """

    def __init__(self, state: V50State, host: str = '0.0.0.0', port: int = 5050):
        self.state = state
        self.host = host
        self.port = port
        self.server_sock = None
        self.client_sock = None
        self.running = False
        self.streaming = False
        self.on_dtc_request: Optional[Callable] = None
        self.on_maint_request: Optional[Callable] = None
        self.messages_sent = 0

    def start(self):
        """Start the TCP server."""
        try:
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_sock.bind((self.host, self.port))
            self.server_sock.listen(MAX_CLIENTS)
            self.running = True

            logger.info(f"TCP server listening on {self.host}:{self.port}")
            logger.info("Connect with: nc <pi_ip> 5050")

            while self.running:
                try:
                    self.server_sock.settimeout(1.0)
                    try:
                        self.client_sock, addr = self.server_sock.accept()
                    except socket.timeout:
                        continue

                    logger.info(f"TCP client connected: {addr}")
                    self._handle_client()

                except OSError:
                    if self.running: break

        except Exception as e:
            logger.error(f"TCP server error: {e}")
        finally:
            self.stop()

    def stop(self):
        """Stop the TCP server."""
        self.running = False
        self.streaming = False
        if self.client_sock:
            try: self.client_sock.close()
            except: pass
            self.client_sock = None
        if self.server_sock:
            try: self.server_sock.close()
            except: pass
            self.server_sock = None
        logger.info("TCP server stopped")

    def _handle_client(self):
        """Handle a TCP client connection."""
        self.streaming = True
        self.client_sock.settimeout(0.1)

        try:
            while self.running and self.client_sock:
                try:
                    cmd = self.client_sock.recv(256).decode('utf-8', errors='ignore').strip()
                    if cmd:
                        cmd_upper = cmd.upper()
                        if cmd_upper == "STOP": self.streaming = False
                        elif cmd_upper == "START": self.streaming = True
                        elif cmd_upper == "DTC" and self.on_dtc_request:
                            dtcs = self.on_dtc_request()
                            if dtcs:
                                payload = dtc_to_json(dtcs) + "\n"
                                self.client_sock.send(payload.encode('utf-8'))
                        elif cmd_upper == "MAINT" and self.on_maint_request:
                            status = self.on_maint_request()
                            if status:
                                payload = maintenance_to_json(status) + "\n"
                                self.client_sock.send(payload.encode('utf-8'))
                except socket.timeout:
                    pass
                except ConnectionError:
                    break

                if self.streaming:
                    try:
                        payload = state_to_json(self.state) + "\n"
                        self.client_sock.send(payload.encode('utf-8'))
                        self.messages_sent += 1
                    except ConnectionError:
                        break

                time.sleep(UPDATE_INTERVAL)
        finally:
            if self.client_sock:
                try: self.client_sock.close()
                except: pass
                self.client_sock = None


def main():
    parser = argparse.ArgumentParser(description='V50 BLE/Bluetooth Data Server')
    parser.add_argument('--tcp', action='store_true', help='Use TCP instead of Bluetooth')
    parser.add_argument('--tcp-port', type=int, default=5050, help='TCP port')
    parser.add_argument('--bt-port', type=int, default=RFCOMM_PORT, help='BT RFCOMM port')
    parser.add_argument('--simulate', action='store_true', help='Simulate data')
    parser.add_argument('--verbose', '-v', action='store_true')

    args = parser.parse_args()
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s %(levelname)s %(name)s: %(message)s')

    state = V50State()

    if args.simulate:
        import random
        def simulate_data():
            t = 0
            while True:
                rpm = int(800 + 4000 * (0.5 + 0.5 * abs((t * 0.1) % 2 - 1)))
                speed = int(80 * abs((t * 0.05) % 2 - 1))
                temp = int(85 + 10 * (0.5 + 0.5 * abs((t * 0.01) % 2)))

                state.update(0x0C0, int(rpm / 0.25).to_bytes(2, 'little') + b'\x00' * 6)
                state.update(0x0E0, int(speed / 0.01).to_bytes(2, 'little') + b'\x00' * 6)
                state.update(0x0C8, bytes([temp + 40]) + b'\x00' * 7)
                state.update(0x0F0, bytes([int(65 / 0.390625)]) + b'\x00' * 7)
                state.update(0x0D8, bytes([int(min(rpm/70,100)/0.390625)]) + b'\x00' * 7)
                state.update(0x1A0, bytes([3]) + b'\x00' * 7)
                state.update(0x238, bytes([18+40]) + b'\x00' * 7)
                state.update(0x328, int(142500).to_bytes(4, 'little') + b'\x00' * 4)

                t += 1
                time.sleep(0.5)

        sim_thread = threading.Thread(target=simulate_data, daemon=True)
        sim_thread.start()

    if args.tcp:
        server = TCPServer(state, port=args.tcp_port)
    else:
        server = RFCOMMServer(state, port=args.bt_port)

    try:
        server.start()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())