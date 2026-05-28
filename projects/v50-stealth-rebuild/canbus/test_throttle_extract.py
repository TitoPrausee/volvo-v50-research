#!/usr/bin/env python3
"""Test throttle signal extraction from CAN decoder."""
import sys
sys.path.insert(0, '/opt/data/home/vehicle-database/projects/v50-stealth-rebuild/canbus')

from v50_can_decoder import extract_signal, CANSignalDef, decode_message, V50State

# Test: throttle in byte 1 (start_bit=8, bit_length=8)
signal = CANSignalDef('throttle_position', 8, 8, 'little', 0.390625, 0.0, '%', 0, 100, 'test')

# Simulate: byte[1] = 128 (50% throttle approx: 128 * 0.390625 = 50)  
data = bytes([0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
val = extract_signal(data, signal)
print(f'Byte[1]=0x80 -> throttle={val:.1f}%')

# Simulate: byte[1] = 0 (0% throttle)
data0 = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
val0 = extract_signal(data0, signal)
print(f'Byte[1]=0x00 -> throttle={val0:.1f}%')

# Full decode test for 0x0D0
results = decode_message(0x0D0, data)
print(f'Decode 0x0D0 byte[1]=0x80: {results}')

# Test V50State update
state = V50State()
state.update(0x0D0, data)
print(f'V50State after update: throttle_pct={state.throttle_pct:.1f}%')

# Test: 100% throttle = 255 * 0.390625 = 99.6
data100 = bytes([0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
val100 = extract_signal(data100, signal)
print(f'Byte[1]=0xFF -> throttle={val100:.1f}%')