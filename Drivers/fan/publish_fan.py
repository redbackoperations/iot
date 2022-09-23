#!/usr/bin/env python3
from mqtt_client import MQTTClient
import os
import time
import sys
import struct

# Publish a speed value to MQTT for testing purposes
def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} speed")
        print("Where speed is in range 0 to 100")
        exit(1)

    speed = int(sys.argv[1])
    if speed < 0 or speed > 100:
        print(f"Usage: {sys.argv[0]} speed")
        print("Where speed is in range 0 to 100")
        exit(1)

    try:
        global mqtt_client
        global deviceId
        mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), \
            os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
        mqtt_client.setup_mqtt_client()
        deviceId = os.getenv('DEVICE_ID')
        topic = f"bike/{deviceId}/fan/control"
        payload = str(speed)
        print(f"Publishing {topic} {payload}")
        mqtt_client.publish(topic, payload)
    except KeyboardInterrupt:
        pass


if __name__=="__main__":
    main()
