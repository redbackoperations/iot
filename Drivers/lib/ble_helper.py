import re

def service_or_characteristic_found(target_uuid, full_uuid):
    uuid_string = hex(target_uuid)[2:]

    # assume the full uuid for a FTMS service or its characteristic will be like: "00002ad9-0000-1000-8000-00805f9b34fb"
    return bool(re.search(f"0000{uuid_string}", full_uuid, re.IGNORECASE))

# assume the value will be like a dbus array of bytes:
# dbus.Array([dbus.Byte(0), dbus.Byte(0), dbus.Byte(100), dbus.Byte(0), dbus.Byte(1), dbus.Byte(0)], signature=dbus.Signature('y'))
def decode_int_bytes(value):
    return [int(v) for v in value]

def decode_string_bytes(value):
    return bytes(value).decode()

def covert_negative_value_to_valid_bytes(negative_int):
    return negative_int.to_bytes(2, byteorder='big', signed=True)
