import time
import os
from mqtt_client import MQTTClient
from FTP_class import FTP


def message(self, client, userdata, msg, foo):
    print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    foo.power_data.append(int(msg.payload.decode("utf-8")))

def main():
    try:
        #Create FTP object and initialize duration to user set parameter
        init = False
        foo = FTP()
        global mqtt_client
        global deviceId
        while(init == False):
            print("Enter selection for FTP Workout mode:\n1: Test/Dev mode (2 minutes)\n2: FTP Workout mode (20 minutes)")
            mode_selection = input("Enter selection: ")
            if(mode_selection == "1"):
                foo.duration = 120
                init = True
            elif(mode_selection == "2"):
                foo.duration = 1200
                init = True
            else:
                print("Invalid selection, enter 1 or 2 for selection")

        # Initialize MQTT client and subscribe to power topic
        mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
        mqtt_client.setup_mqtt_client()
        deviceId = os.getenv("DEVICE_ID")
        mqtt_client.subscribe(f"bike/{deviceId}/power")
        mqtt_client.get_client().on_message = message
        mqtt_client.get_client().loop_start()
        
        # Start FTP test
        print("Starting the 20-minute FTP test...")
        foo.perform_ftp_test()
        foo.ftp = foo.calculate_ftp()
        print(f"Your estimated FTP is: {foo.ftp:.2f} watts")
        
    except KeyboardInterrupt:
        pass
    mqtt_client.get_client().loop_stop()
    
if __name__ == "__main__":
    main()