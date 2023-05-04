#!/usr/bin/env python3
from mqtt_client import MQTTClient
import os
import time
import keyboard
import json


from dotenv import load_dotenv
def message(client, userdata, msg):
    print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

vars = load_dotenv('/home/pi/.env')
load_dotenv(vars)
mqtt_client = MQTTClient('f5b2a345ee944354b5bf1263284d879e.s1.eu.hivemq.cloud', 'redbackiotclient', 'IoTClient@123')
mqtt_client.setup_mqtt_client()
deviceId = os.getenv('DEVICE_ID')
mqtt_client.subscribe(f"bike/000001/power")
mqtt_client.get_client().on_message = message
mqtt_client.get_client().loop_start()

while 1:
    if(keyboard.is_pressed('space')):
        user_input = input("Enter power: ")
        user_input = user_input.strip()
        if user_input.isdigit():
            user_input = int(user_input)
            dump = json.dumps({"value": user_input})
            mqtt_client.publish(f"bike/000001/power", f"{dump}")
            print("Published power to MQTT Broker: ", user_input)
            time.sleep(1)
        else:
            print("invalid input")
        
mqtt_client.get_client().loop_stop()