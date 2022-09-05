import re
import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from lib.constants import INCLINE_MIN, INCLINE_MAX, INCLINE_CONTROL_FLAT, INCLINE_CONTROL_INCREMENT_UNIT, MAX_BYTE_VALUE, MIN_BYTE_VALUE

def service_or_characteristic_found(target_uuid, full_uuid):
    uuid_string = hex(target_uuid)[2:]

    # assume the full uuid for a FTMS service or its characteristic will be like: "00002ad9-0000-1000-8000-00805f9b34fb"
    return bool(re.search(f"0000{uuid_string}", full_uuid, re.IGNORECASE))

def service_or_characteristic_found_full_match(target_uuid, full_uuid):
    # assume the full uuid for a service or its characteristic will be like: "a026ee0b0a7d4ab397faf1500f9feb8b"
    return bool(re.search(target_uuid, re.sub('-', '', full_uuid), re.IGNORECASE))

# assume the value will be like a dbus array of bytes:
# dbus.Array([dbus.Byte(0), dbus.Byte(0), dbus.Byte(100), dbus.Byte(0), dbus.Byte(1), dbus.Byte(0)], signature=dbus.Signature('y'))
def decode_int_bytes(value):
    return [int(v) for v in value]

def decode_string_bytes(value):
    return bytes(value).decode()

def covert_negative_value_to_valid_bytes(negative_int):
    return negative_int.to_bytes(2, byteorder='big', signed=True)

# the incline control value needs to have a valid BLE op code pattern like 666c07(19%), 66000(0%), 6619fc(-10%)
def convert_incline_to_op_value(incline):
    if incline < INCLINE_MIN or incline > INCLINE_MAX:
        raise Exception("invalid incline value", incline)

    # increment op value part 1 by 50 unit, and increment part 2 by 1 when part value is greater than 256
    if incline >= 0:
        converted_value_part_1 = INCLINE_CONTROL_FLAT
        converted_value_part_2 = INCLINE_CONTROL_FLAT
        int_track_value =  0

        while int_track_value < incline:
            if converted_value_part_1 + INCLINE_CONTROL_INCREMENT_UNIT >= MAX_BYTE_VALUE:
                converted_value_part_1 = converted_value_part_1 + INCLINE_CONTROL_INCREMENT_UNIT - MAX_BYTE_VALUE
                converted_value_part_2 += 1
            else:
                converted_value_part_1 += INCLINE_CONTROL_INCREMENT_UNIT

            int_track_value += INCLINE_CONTROL_INCREMENT_UNIT/100

        return [converted_value_part_1, converted_value_part_2]
        # increment op value part 1 by 50 unit, and increment part 2 by 1 when part value is greater than 256
    elif incline < 0:
        converted_value_part_1 = INCLINE_CONTROL_FLAT
        converted_value_part_2 = MAX_BYTE_VALUE
        int_track_value =  0

        while int_track_value > incline:
            if converted_value_part_1 - INCLINE_CONTROL_INCREMENT_UNIT < MIN_BYTE_VALUE:
                converted_value_part_1 = MAX_BYTE_VALUE - converted_value_part_1 - INCLINE_CONTROL_INCREMENT_UNIT + 1
                converted_value_part_2 -= 1
            else:
                converted_value_part_1 -= INCLINE_CONTROL_INCREMENT_UNIT

            int_track_value -= INCLINE_CONTROL_INCREMENT_UNIT/100

        return [converted_value_part_1, converted_value_part_2]

# convert an array of hex values into human readable string
def covert_hex_values_to_readable_string(array):
    result = ''
    for i in range(len(array)):
        result += hex(array[i])[2:].zfill(2)

    return result