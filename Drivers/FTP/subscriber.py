#!/usr/bin/env python3
from mqtt_client import MQTTClient
import os
import time

def message(client, userdata, msg):
    print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

mqtt_client = MQTTClient('f5b2a345ee944354b5bf1263284d879e.s1.eu.hivemq.cloud', 'redbackiotclient', 'IoTClient@123')
mqtt_client.setup_mqtt_client()
deviceId = os.getenv('DEVICE_ID')
mqtt_client.subscribe(f"bike/000001/power")
mqtt_client.get_client().on_message = message
mqtt_client.loop_forever()
