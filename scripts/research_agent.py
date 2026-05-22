#!/usr/bin/env python3
"""
Volvo V50 Research Agent — Autonomous background researcher.
Runs as a cron job, researches car electronics topics, and pushes findings to GitHub.

Day 1: CAN Bus — Verify IDs, discover unknown messages, document protocols
Day 2: Climate & Dashboard — ACC protocol, DIM messages, sensor details  
Day 3: Body & Infotainment — Low-speed CAN, audio, steering wheel
Day 4: Deep Dives — Immobilizer, VIDA cross-reference, wiring verification
"""

import subprocess
import json
import random
import os
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path("/opt/data/home/volvo-v50-research")
STATE_FILE = REPO / ".research_state.json"

# Research topics organized by day
TOPICS = {
    1: [
        ("can_bus_discovery", "CAN Bus Discovery",
         """Research and document:
- Volvo P1 platform CAN bus architecture (high-speed 500kbps + low-speed 125kbps)
- All known CAN message IDs for V50/S40/C30
- CEM gateway behavior (message translation between buses)
- CAN bus initialization sequence on key turn
- OBD-II standard PIDs vs Volvo proprietary PIDs (Mode 22)
- Message frequency and timing patterns
- How to filter specific module messages
- CAN bus sleep/wake behavior"""),
        ("obd2_protocols", "OBD-II & Diagnostic Protocols",
         """Research:
- ISO 15765-4 (CAN-based OBD-II) specifics for Volvo
- Volvo Mode 22 proprietary PIDs
- K-Line diagnostic protocol (ISO 9141-2) for low-speed modules
- UDS (Unified Diagnostic Services) on Volvo
- VIDA/DICE communication protocol
- J2534 passthrough device compatibility
- How to read and clear DTCs via CAN"""),
        ("can_tools_setup", "CAN Sniffing Tools & Setup",
         """Research and document:
- Best CAN bus interfaces for Volvo P1 (PiCAN2, CANable, USBtin)
- SavvyCAN setup and configuration for Volvo
- can-utils (candump, cansend, cangen) cheat sheet
- Python-can library setup and Volvo examples
- How to set up dual CAN (high + low speed) on Raspberry Pi
- CAN bus termination requirements (120 ohm)
- Safe connection points (OBD-II vs direct splice)
- Logging and replaying CAN traffic"""),
    ],
    2: [
        ("acc_climate_deep", "ACC Climate Control — Deep Dive",
         """Research deeply:
- Automatic Climate Control (ACC) module internals
- All ACC CAN message IDs and their data formats
- Temperature sensor NTC thermistor specifications and curves
- Blend door motor control (stepper motors, CAN or direct?)
- Heater core valve control mechanism
- A/C compressor clutch activation via CAN
- Afterblow function (drying evaporator after shutdown)
- ECC vs manual climate differences in CAN messages
- How to read HVAC duct temperature sensors
- Defrost/windshield heating CAN activation"""),
        ("dim_instrument", "DIM Instrument Cluster — Deep Dive",
         """Research deeply:
- DIM (Driver Information Module) architecture and processors
- Stepper motor type (VID29xx / X27.589) specifications
- LCD/TFT display connector pinout and protocol (SPI? CAN? LVDS?)
- Warning light LED matrix control protocol
- Odometer storage (EEPROM? Flash? in CEM?)
- Immobilizer LED control (blinks code, solid = error)
- Trip computer button matrix and CAN messages
- DIM self-test mode activation procedure
- Aftermarket gauge cluster replacement projects
- How to decode DIM firmware version from CAN"""),
    ],
    3: [
        ("body_can_low", "Low-Speed CAN Body Commands",
         """Research:
- Complete low-speed CAN (125kbps) message ID list
- Door module (DDM/PDM) commands and status
- Power seat (PSM) memory positions and CAN protocol
- Steering wheel module (SWM) button matrix
- Cruise control CAN messages and enable/disable
- Central locking remote key fob protocol
- Alarm system CAN integration
- Sunroof/open roof module (ORM)
- Rear park assist sensor data format
- Auto-dimming mirror CAN data"""),
        ("audio_infotainment", "Audio & Infotainment CAN Protocol",
         """Research:
- IAM (Integrated Audio Module) CAN message IDs
- Volume control via CAN (steering wheel → CEM → IAM)
- Audio source switching commands
- RTI navigation module protocol
- Premium Sound (Dynaudio) amplifier CAN control
- AUX/USB input activation via CAN
- Bluetooth phone module (PHM) CAN messages
- How aftermarket head units integrate with CAN
- Steering wheel control adapter wiring (Connects2 CTSVO004)
- Reverse gear signal for backup camera activation"""),
    ],
    4: [
        ("immobilizer_security", "Immobilizer & Security Systems",
         """Research:
- Immobilizer (IMMO) system architecture — CEM + key transponder
- Key fob (RF remote) protocol and frequency (433.92 MHz EU)
- Rolling code system and resynchronization procedure
- VIDA key programming procedure
- Emergency key blade and mechanical lock cylinders
- Alarm siren module (SCM) CAN integration
- Dead-locking mechanism CAN activation
- Approach lighting (home-safe) CAN commands
- Global closing (windows via key fob) CAN messages
- Battery drain protection module behavior"""),
        ("wiring_verification", "Wiring Harness Verification & Corrections",
         """Research and verify:
- CEM connector pinout — verify every pin with multimeter (if possible)
- ECM connector pinout — verify B5244S specific wiring colors
- OBD-II connector — confirm pin assignments match V50
- ACC panel connector — verify auto vs manual climate differences
- Radio/IAM connector — verify speaker wire colors
- Ground point locations and their purpose
- Fuse box layout and ratings (under-hood and under-dash)
- Relay locations and functions
- Wiring color code legend for Volvo
- Common wiring modifications needed for PiCAN2 install"""),
    ],
}


def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {"day": 1, "topics_done": [], "started": datetime.now().isoformat()}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def git_commit_push(message):
    """Stage, commit, and push changes."""
    os.chdir(REPO)
    subprocess.run(["git", "add", "-A"], capture_output=True)
    result = subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True)
    if result.returncode == 0:
        subprocess.run(["git", "push", "origin", "main"], capture_output=True)
        return True
    return False


def get_current_day(state):
    """Calculate which day we're on based on start date."""
    started = datetime.fromisoformat(state["started"])
    delta = datetime.now() - started
    day = min(delta.days + 1, 4)
    return max(day, 1)


def pick_topic(state, day):
    """Pick the next uncompleted topic for the current day."""
    topics = TOPICS.get(day, TOPICS[4])
    done = state.get("topics_done", [])
    for topic_id, name, prompt in topics:
        if topic_id not in done:
            return topic_id, name, prompt
    # All topics for this day done, pick random
    return random.choice(topics)


def main():
    state = load_state()
    day = get_current_day(state)
    
    topic_id, name, prompt = pick_topic(state, day)
    print(f"Research Day {day} — Topic: {name}")
    print(f"Topic ID: {topic_id}")
    print(f"Prompt:\n{prompt}")
    
    # Mark topic as in-progress
    if topic_id not in state.get("topics_done", []):
        state.setdefault("topics_done", []).append(topic_id)
        state["current_topic"] = topic_id
        state["current_day"] = day
        save_state(state)


if __name__ == "__main__":
    main()