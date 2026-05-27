#!/usr/bin/env python3
"""
Update vehicle_database.db with additional CAN signals discovered during
V50 CAN-Bus development. Adds missing low-speed CAN messages and
updates existing records with verification notes and facelift alternatives.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path('/opt/data/home/vehicle-database/research/vehicle_database.db')

def update_database():
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    # =========================================================================
    # Add missing low-speed CAN signals for existing messages
    # =========================================================================
    
    # Add signals for messages 28-31 that were missing in DB
    # Message 29 (0x410 = 1040) - Driver Door Status - already has signals
    
    # But let's check what signals exist for low-speed messages
    c.execute("""SELECT cm.id, cm.can_id, cm.name, COUNT(cs.id) as signal_count
                 FROM can_messages cm 
                 LEFT JOIN can_signals cs ON cs.message_id = cm.id
                 WHERE cm.bus_id = 2
                 GROUP BY cm.id""")
    ls_messages = c.fetchall()
    print("Low-speed CAN messages and signals:")
    for m in ls_messages:
        print(f"  ID={m[0]} can_id=0x{m[1]:03X} name={m[2]} signals={m[3]}")
    
    # Check if we have remaining messages beyond id=31
    c.execute("SELECT id, can_id, name FROM can_messages WHERE id > 31 ORDER BY id")
    extra_msgs = c.fetchall()
    print(f"\nMessages beyond id 31: {len(extra_msgs)}")
    for m in extra_msgs:
        print(f"  id={m[0]} can_id=0x{m[1]:03X} name={m[2]}")
    
    # =========================================================================
    # Add additional CAN messages not in the original DB
    # These are discovered through community research and VIDA reverse engineering
    # =========================================================================
    
    # Rear door status messages (low-speed CAN)
    new_messages = [
        # Rear Left Door
        (0x420, 2, 1, 'RDM', 'CEM', 'TX', 'Rear Left Door Status', None, 8, 1, 'community', 'Low-speed CAN body'),
        # Rear Right Door
        (0x428, 2, 1, 'RDM', 'CEM', 'TX', 'Rear Right Door Status', None, 8, 1, 'community', 'Low-speed CAN body'),
        # Trunk/Tailgate Status
        (0x438, 2, 1, 'CEM', 'DIM', 'TX', 'Trunk/Tailgate Status', None, 8, 1, 'community', 'Low-speed CAN body'),
        # Light Switch Status
        (0x440, 2, 1, 'LSM', 'CEM', 'TX', 'Light Switch Position', None, 8, 1, 'community', 'Low-speed CAN body'),
        # Horn Status
        (0x448, 2, 1, 'SWM', 'CEM', 'TX', 'Horn Status', None, 8, 1, 'community', 'Low-speed CAN body'),
        # Seatbelt Status
        (0x450, 2, 1, 'SRS', 'CEM', 'TX', 'Seatbelt Warning', None, 8, 1, 'community', 'Low-speed CAN body'),
        # ABS Brake Pressure (high-speed CAN)
        (0x0E8, 1, 1, 'ABS', 'CEM', 'TX', 'Brake Pressure', 'Byte 0-1: pressure', 8, 0, 'community', 'UNVERIFIED — needs physical verification on V50'),
        # ABS Yaw Rate (high-speed CAN)
        (0x0F8, 1, 1, 'ABS', 'CEM', 'TX', 'Yaw Rate', 'Byte 0-1: deg/s', 8, 0, 'community', 'UNVERIFIED'),
        # Steering Angle (high-speed CAN)
        (0x128, 1, 1, 'SAS', 'CEM', 'TX', 'Steering Angle', 'Byte 0-1: degrees', 8, 0, 'community', 'UNVERIFIED'),
        # Wheel Speeds (high-speed CAN)
        (0x0D4, 1, 1, 'ABS', 'CEM', 'TX', 'Wheel Speed FL', 'Byte 0-1: km/h', 8, 0, 'community', 'UNVERIFIED — individual wheel speeds'),
        (0x0D5, 1, 1, 'ABS', 'CEM', 'TX', 'Wheel Speed FR', 'Byte 0-1: km/h', 8, 0, 'community', 'UNVERIFIED'),
        (0x0D6, 1, 1, 'ABS', 'CEM', 'TX', 'Wheel Speed RL', 'Byte 0-1: km/h', 8, 0, 'community', 'UNVERIFIED'),
        (0x0D7, 1, 1, 'ABS', 'CEM', 'TX', 'Wheel Speed RR', 'Byte 0-1: km/h', 8, 0, 'community', 'UNVERIFIED'),
    ]
    
    added_count = 0
    for msg in new_messages:
        can_id, bus_id, variant_id, src, dest, direction, name, desc, dlc, verified, vsrc, notes = msg
        # Check if message already exists
        c.execute("SELECT id FROM can_messages WHERE can_id = ?", (can_id,))
        if c.fetchone() is None:
            c.execute("""INSERT INTO can_messages 
                        (can_id, bus_id, variant_id, source_module, dest_module, direction, name, description, dlc, verified, verification_source, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                     (can_id, bus_id, variant_id, src, dest, direction, name, desc, dlc, verified, vsrc, notes))
            added_count += 1
            print(f"  Added: 0x{can_id:03X} {name}")
        else:
            print(f"  Exists: 0x{can_id:03X} {name}")
    
    # =========================================================================
    # Add signals for the new low-speed messages
    # =========================================================================
    
    # Get message IDs for newly added messages
    new_signals = [
        # Rear Left Door (0x420)
        (0x420, 'rear_left_door_open', 0, 1, 'little', 1.0, 0.0, 'boolean', 0, 1, 'Rear left door open status'),
        (0x420, 'rear_left_door_locked', 1, 1, 'little', 1.0, 0.0, 'boolean', 0, 1, 'Rear left door locked status'),
        # Rear Right Door (0x428)
        (0x428, 'rear_right_door_open', 0, 1, 'little', 1.0, 0.0, 'boolean', 0, 1, 'Rear right door open status'),
        (0x428, 'rear_right_door_locked', 1, 1, 'little', 1.0, 0.0, 'boolean', 0, 1, 'Rear right door locked status'),
        # Trunk (0x438)
        (0x438, 'trunk_open', 0, 1, 'little', 1.0, 0.0, 'boolean', 0, 1, 'Trunk/tailgate open status'),
        # Light Switch (0x440)
        (0x440, 'light_switch_pos', 0, 3, 'little', 1.0, 0.0, 'position', 0, 7, '0=off, 1=parking, 2=dipped, 3=main beam'),
        # Horn (0x448)
        (0x448, 'horn_active', 0, 1, 'little', 1.0, 0.0, 'boolean', 0, 1, 'Horn button pressed'),
        # Seatbelt (0x450)
        (0x450, 'driver_belt', 0, 1, 'little', 1.0, 0.0, 'boolean', 0, 1, 'Driver seatbelt buckled'),
        (0x450, 'pass_belt', 1, 1, 'little', 1.0, 0.0, 'boolean', 0, 1, 'Passenger seatbelt buckled'),
        # Brake Pressure (0x0E8) — UNVERIFIED
        (0x0E8, 'brake_pressure', 0, 16, 'little', 0.1, 0.0, 'bar', 0, 200, 'UNVERIFIED — brake hydraulic pressure'),
        # Yaw Rate (0x0F8) — UNVERIFIED
        (0x0F8, 'yaw_rate', 0, 16, 'little', 0.01, 0.0, 'deg/s', -150, 150, 'UNVERIFIED — vehicle yaw rate'),
        # Steering Angle (0x128) — UNVERIFIED
        (0x128, 'steering_angle', 0, 16, 'little', 0.1, 0.0, 'degrees', -720, 720, 'UNVERIFIED — steering wheel angle'),
        # Wheel Speeds — UNVERIFIED
        (0x0D4, 'wheel_speed_fl', 0, 16, 'little', 0.01, 0.0, 'km/h', 0, 300, 'UNVERIFIED — front left wheel speed'),
        (0x0D5, 'wheel_speed_fr', 0, 16, 'little', 0.01, 0.0, 'km/h', 0, 300, 'UNVERIFIED — front right wheel speed'),
        (0x0D6, 'wheel_speed_rl', 0, 16, 'little', 0.01, 0.0, 'km/h', 0, 300, 'UNVERIFIED — rear left wheel speed'),
        (0x0D7, 'wheel_speed_rr', 0, 16, 'little', 0.01, 0.0, 'km/h', 0, 300, 'UNVERIFIED — rear right wheel speed'),
    ]
    
    for can_id, sig_name, start_bit, bit_length, byte_order, factor, offset, unit, min_val, max_val, desc in new_signals:
        c.execute("SELECT id FROM can_messages WHERE can_id = ?", (can_id,))
        msg_row = c.fetchone()
        if msg_row:
            msg_id = msg_row[0]
            # Check if signal already exists
            c.execute("SELECT id FROM can_signals WHERE message_id = ? AND name = ?", (msg_id, sig_name))
            if c.fetchone() is None:
                c.execute("""INSERT INTO can_signals 
                            (message_id, name, start_bit, bit_length, byte_order, factor, offset, unit, min_value, max_value, description)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                         (msg_id, sig_name, start_bit, bit_length, byte_order, factor, offset, unit, min_val, max_val, desc))
                print(f"  Added signal: {sig_name} → 0x{can_id:03X}")
    
    # =========================================================================
    # Add facelift CAN ID alternatives as notes
    # =========================================================================
    
    # Update existing messages with facelift alternatives
    facelift_notes = {
        0x0C0: "Pre-FL: 0x0C0, FL: 0x316 — Engine RPM",
        0x0E0: "Pre-FL: 0x0E0, FL: 0x360 — Vehicle Speed",  
        0x0F0: "Pre-FL: 0x0F0, FL: 0x320 — Fuel Level",
        0x400: "Pre-FL: 0x400, FL: 0x260 — Steering Wheel",
    }
    
    for can_id, note in facelift_notes.items():
        c.execute("UPDATE can_messages SET notes = COALESCE(notes || '; ', '') || ? WHERE can_id = ?", (note, can_id))
    
    conn.commit()
    
    # Print summary
    c.execute("SELECT COUNT(*) FROM can_messages")
    total_msgs = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM can_signals")
    total_sigs = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM can_messages WHERE verified = 1")
    verified_msgs = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM can_messages WHERE verified = 0")
    unverified_msgs = c.fetchone()[0]
    
    print(f"\n{'='*50}")
    print(f"Database updated!")
    print(f"New messages added: {added_count}")
    print(f"Total CAN messages: {total_msgs}")
    print(f"  Verified: {verified_msgs}")
    print(f"  Unverified: {unverified_msgs}")
    print(f"Total CAN signals: {total_sigs}")
    print(f"{'='*50}")
    
    conn.close()

if __name__ == "__main__":
    update_database()