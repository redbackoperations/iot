import time
import os
from mqtt_client import MQTTClient
from FTP_class import FTP


def main():
    try:
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

        #Replace hard coded MQTT client params with os.getenv('MQTT_HOSTNAME'), os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD')
        mqtt_client = MQTTClient('f5b2a345ee944354b5bf1263284d879e.s1.eu.hivemq.cloud', 'redbackiotclient', 'IoTClient@123')
        
        mqtt_client.setup_mqtt_client()
        mqtt_client.subscribe(f"bike/000001/power")
        mqtt_client.get_client().on_message = foo.message
        mqtt_client.get_client().loop_start()
        

        print("Starting the 20-minute FTP test...")
        foo.perform_ftp_test()
        foo.ftp = foo.calculate_ftp()
        print(f"Your estimated FTP is: {foo.ftp:.2f} watts")
        
    except KeyboardInterrupt:
        pass
    mqtt_client.get_client().loop_stop()
    
if __name__ == "__main__":
    main()