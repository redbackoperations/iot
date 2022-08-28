#!/usr/bin/env python3
from mqtt_client import MQTTClient
import os
import time

def message(client, userdata, msg):
    print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), \
    os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
mqtt_client.setup_mqtt_client()
deviceId = os.getenv('DEVICE_ID')
mqtt_client.subscribe(f"bike/{deviceId}/heartrate")
mqtt_client.get_client().on_message = message
mqtt_client.loop_forever()
