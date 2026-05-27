# V50 CAN-Bus Decoder Package
from .v50_can_decoder import (
    V50State, CANBus, MESSAGE_DEFINITIONS,
    decode_message, extract_signal, list_known_messages,
    get_gear_name, calculate_fuel_consumption,
    OBD2_STANDARD_PIDS, VOLVO_PROPRIETARY_PIDS
)