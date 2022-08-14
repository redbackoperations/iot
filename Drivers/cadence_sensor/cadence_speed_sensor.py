#!/usr/bin/env python3
import random
import time
import adafruit_ble
from adafruit_ble_cycling_speed_and_cadence import CyclingSpeedAndCadenceService
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
import serial
import argparse
from mqtt_client import MQTTClient

# a constant mulitiplier that is used to convert anolog signal value to the correct O2 concentration
#ANOLOG_TO_O2_VALUE = 0.02    # TODO: this value is subject to change when we get the actual oxgen sensor set up properly, and more calculation could be introduced soon to get the correct O2 concentration

# example values for testing. once sensors are set up, we will be using adafruit libraries to get the data and process it
cadence_values = random.uniform((80,120), 2)
speed_values = random.uniform((5,10),2)

# define CLI parse arguments
parser = argparse.ArgumentParser()

# HiveMQ connection params
parser.add_argument('--broker_address', dest='broker_address', type=str, help='The MQTT broker address getting from HiveMQ Cloud')
parser.add_argument('--username', dest='username', type=str, help='HiveMQ Cloud username')
parser.add_argument('--password', dest='password', type=str, help='HiveMQ Cloud password')
parser.add_argument('--topic', dest='topic', type=str, help='a MQTT topic the driver will subscribe to')

# Arduino serial connection params
parser.add_argument('--device_name', dest='device_name', type=str, default='/dev/ttyACM0', help='Specify serial device name for the connected Arduino (default: "/dev/ttyACM0")')
parser.add_argument('--baud_rate', dest='baud_rate', type=str, default=9600, help='Specify serial baud rate for Arduino (default: 9600)')
args = parser.parse_args()

if __name__ == '__main__':
    # setup direct serial connection between Rasperry Pi and Arduino
    ser = serial.Serial(args.device_name, args.baud_rate, timeout=1)
    ser.reset_input_buffer()

    # setup HiveMQ conneciton
    mqtt_client = MQTTClient(args.broker_address, args.username, args.password)
    mqtt_client.setup_mqtt_client()
    #mqtt_client.subscribe(args.topic)

    # part of oxygen code, could be useful depending on output datatype of sensor
    if ser.in_waiting > 0:
        # read Arduino returned data line by line
        sensor_data = ser.readline().decode('utf-8').rstrip()
    # end of oxygen code

    # initialising radio
    ble = adafruit_ble.BLERadio()


    while True:
        # loop the MQTT client connection
        # mqtt_client.get_client().loop()

        print("scanning for connected sensors...")
        advertised = {}
        for advert in ble.start_scan(ProvideServicesAdvertisement, timeout = 5):
           if CyclingSpeedAndCadenceService in advert.services:
               print("found cycling and cadence sensors")
               advertised[advert.address] = advert
        ble.stop_scan()
        print("stopped scanning")

        cycle_connections = []

        for advert in advertised.values():
            cycle_connections.append(ble.connect(advert))
            print("Connected", len(cycle_connections))

        for connection in cycle_connections:
            if connection.connected:
                if DeviceInfoService in connection:
                    dis = connection[DeviceInfoService]
                    try:
                        manufacturer = dis.manufacturer
                    except AttributeError:
                        manufacturer = "Manufacturer not specified"

                else:
                    print("No device information found")
        print("Waiting for data..")

        cycle_services = []
        for connection in cycle_connections:
            cycle_services.append(connection[CyclingSpeedAndCadenceService])

        # while connection to sensors are live
        while True:
            still_connected = False

            for connection, svc in zip(cycle_connections, cycle_services):
                if connection.connected:
                    still_connected = True
                    print(svc.measurement_values)

                    #mqtt_client.publish(args.topic, svc.measurement_values) this will be used once the sensors are setup
                    mqtt_client.publish(args.topic, speed_values, cadence_values) # this will be removed as it is only using example values.


            if not still_connected:
                break
            time.sleep(1)



# https://docs.circuitpython.org/projects/ble_cycling_speed_and_cadence/en/latest/examples.html