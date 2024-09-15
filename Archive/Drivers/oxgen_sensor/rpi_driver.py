#!/usr/bin/env python3

import serial
import argparse
from mqtt_client import MQTTClient

# a constant mulitiplier that is used to convert anolog signal value to the correct O2 concentration
ANOLOG_TO_O2_RATE = 0.02    # TODO: this value is subject to change when we get the actual oxgen sensor set up properly, and more calculation could be introduced soon to get the correct O2 concentration

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
    # mqtt_client.subscribe(args.topic)

    while True:
        # loop the MQTT client connection
        # mqtt_client.get_client().loop()

        if ser.in_waiting > 0:
            # read Arduino returned data line by line
            sensor_data = ser.readline().decode('utf-8').rstrip()

            if len(sensor_data) > 0:
                # apply the multiplier rate to get the correct O2 concentration rate
                o2_rate = round(float(sensor_data) * ANOLOG_TO_O2_RATE, 2)

                print("sensor data: {}, calculated O2 concentration: {}%".format(sensor_data, o2_rate))
                # send O2 concentration rate to MQTT broker
                mqtt_client.publish(args.topic, o2_rate)