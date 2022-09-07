#!/usr/bin/env python3
from mqtt_client import MQTTClient
import os
import time


def main():
    try:
        global mqtt_client
        global deviceId
        mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), \
            os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
        mqtt_client.setup_mqtt_client()
        deviceId = os.getenv('DEVICE_ID')
        topic = f"bike/{deviceId}/fan"
        payload = f"{{fan: 0}}"
        print(f"Publishing {topic} {payload}")
        mqtt_client.publish(topic, payload)

    except KeyboardInterrupt:
        pass


if __name__=="__main__":
    main()
