import bluetooth
import sys
import time
import os
from mqtt_client import MQTTClient
from dotenv import load_dotenv

# TO DO: store MAC address in .env file and read from os.getenv

hc06_address = os.getenv('HC06_ADDRESS')
port = 1
env_path = '/' #/home/pi/.env for lab pi
load_dotenv(env_path)
mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))

# TO DO:
## On Start:
# 1. Read from .env file
# 2. Instantiate MQTT client and subscribe to reistance and incline topic
# 3. Read from topic to get current resistance and incline (published messages must be set to retain = True, check Drivers)
## On Loop:
# 4. Listen for pico BT input (increase/decrease resistance)
# 5. Update local global resistance and incline variables
# 6. Publish resistance and incline to topic

print("Connecting to socket..")
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((hc06_address, port))

sock.send("Hello Pico")
print("Connected, waiting for data")
buffer = " "
try:
    while True:
        data = sock.recv(1024).decode('utf-8')
        buffer += data
        while '\n' in buffer:
            line, buffer = buffer.split('\n', 1)
            print("Received:", line.strip())
except KeyboardInterrupt:
    print("Closing connection")

sock.close()
print("Connection closed")
