import bluetooth
from mqtt_client import MQTTClient
import os
import time
from dotenv import load_dotenv

hc06_address = "98:D3:51:FE:68:16"
port = 1
bike_resistance = 0
bike_incline = -10

load_dotenv('/home/pi/.env')
mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
mqtt_client.setup_mqtt_client()

print("Connecting to HC-06...")
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((hc06_address, port))
sock.send("Hello from Raspberry Pi!")
print("Connected, waiting for data")
mqtt_client.get_client().loop_start()

mqtt_client.publish(f"bike/000001/resistance/control", bike_resistance)
mqtt_client.publish(f"bike/000001/incline/control", bike_incline)


buffer = " "
try:
    while True:
            data = sock.recv(1024).decode('utf-8')
            buffer += data
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                print("Receieved: " + line.strip())
                
                if(line.strip() == "increaseResistance"):
                    if bike_resistance < 100:
                        bike_resistance += 5
                        mqtt_client.publish(f"bike/000001/resistance/control", bike_resistance)
                    else:
                        print("Resistance at max")
                
                elif(line.strip() == "decreaseResistance"):
                    if bike_resistance > 0:
                        bike_resistance -= 5
                        mqtt_client.publish(f"bike/000001/resistance/control", bike_resistance)
                    else:
                        print("Resistance at min")

                elif(line.strip() == "increaseIncline"):
                    if bike_incline < 19:
                        bike_incline += 1
                        mqtt_client.publish(f"bike/000001/incline/control", bike_incline)
                    else:
                        print("Incline at max")
                        
                elif(line.strip() == "decreaseIncline"):
                    if bike_incline > -10:
                        bike_incline -= 1
                        mqtt_client.publish(f"bike/000001/incline/control", bike_incline)
                    else:
                        print("Incline at min")
          
                    
except KeyboardInterrupt:
    print("Closing socket")

sock.close()
mqtt_client.get_client().loop_stop()
print("Done")
