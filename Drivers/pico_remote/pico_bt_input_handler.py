import bluetooth
import sys
import time
import os
from mqtt_client import MQTTClient
from dotenv import load_dotenv

# TO DO: store MAC address in .env file and read from os.getenv

# TO DO:
## On Start:
# 1. Read from .env file
# 2. Instantiate MQTT client and subscribe to reistance and incline topic
# 3. Read from topic to get current resistance and incline (published messages must be set to retain = True, check Drivers)
## On Loop:
# 4. Listen for pico BT input (increase/decrease resistance)
# 5. Update local global resistance and incline variables
# 6. Publish resistance and incline to topic


class PicoBTInputHandler:
    def __init__(self, sock) -> None:
        self.sock = sock
        self.resistance = 0
        self.incline = 0

    def connectToPico(self, mac_address, port):
        print("Connecting to socket..")
        self.sock.connect(mac_address, port)
        print("Connected, waiting for data")
        
    def listenForInput(self): 
        buffer = " "
        try:
            data = self.sock.recv(1024).decode('utf-8')
            buffer += data
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                result = line.strip()
                print("Received:", result)
                return result
        except KeyboardInterrupt:
            print("Closing connection")
        self.sock.close()
        print("Connection closed")

    def sendToPico(self, message):
        self.sock.send(message)
        print("Sent:", message)
        
                        
def main():
    env_path = '/' #/home/pi/.env for lab pi
    load_dotenv(env_path)
    pico_txrx_port = 1
    socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    handler = PicoBTInputHandler(socket)
    handler.connectToPico(os.getenv('HC06_ADDRESS'), pico_txrx_port)
    
    mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
    deviceId = os.getenv('DEVICE_ID')
    resistance_control = f'bike/{deviceId}/resistance/control'
    incline_control = f'bike/{deviceId}/incline/control'
    mqtt_client.setup_mqtt_client()
    mqtt_client.subscribe(resistance_control)
    mqtt_client.subscribe(incline_control)
    
    mqtt_client.get_client().loop_start()
    
    while 1:
        try:
            pico_return = handler.listenForInput
            if pico_return is not None:
                if pico_return == "increaseResistance" and handler.resistance < 100 and handler.resistance >= 0:
                    mqtt_client.publish(resistance_control, handler.resistance + 5)
                elif pico_return == "decreaseResistance"and handler.resistance < 100 and handler.resistance >= 0:
                    mqtt_client.publish(resistance_control, handler.resistance - 5)
                elif pico_return == "increaseIncline" and handler.incline >= -19 and handler.incline <= 10:
                    mqtt_client.publish(incline_control, handler.incline + 1)
                elif pico_return == "decreaseIncline"and handler.incline >= -19 and handler.incline <= 10:
                    mqtt_client.publish(incline_control, handler.incline - 1) 
                else:
                    print("Invalid input received from pico remote")
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("Closing connection")
            mqtt_client.get_client().loop_stop()
            socket.close()
            print("Connection closed")
            sys.exit(0)
    
if __name__ == "__main__":
    main()