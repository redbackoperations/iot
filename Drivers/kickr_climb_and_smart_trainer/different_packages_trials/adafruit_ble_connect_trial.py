#!/usr/bin/env python3

from sqlite3 import connect
from adafruit_ble import BLERadio
from adafruit_ble.services.standard.device_info import DeviceInfoService

radio = BLERadio()
print("scanning")
found = set()
for entry in radio.start_scan(timeout=60, minimum_rssi=-80):
    addr = entry.address
    connection = None
    if addr not in found:
        print(entry)
        if entry.complete_name == 'YESOUL2513961': # my own indoor bike device name
            print("found the fitness bike!!!")
            connection = radio.connect(entry)
            print("Connected", connection)

            if connection.connected:
                if DeviceInfoService in connection:
                    dis = connection[DeviceInfoService]
                    try:
                        manufacturer = dis.manufacturer
                        print(f"Manufacturer name is {manufacturer}")
                    except AttributeError:
                        manufacturer = "Manufacturer not specified"
                else:
                    print("No device information found")
                
                while True:
                    print("Waiting for data..")            

    found.add(addr)

print("scan done")