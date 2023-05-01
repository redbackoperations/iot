#!/usr/bin/env python3
#! bin/bash
#! bin/sh

import time
import os
from mqtt_client import MQTTClient
from FTP_class import FTP



def perform_ftp_test(ftp_object):
    # 20 minutes in seconds
    start_time = time.time()
    try:
        while time.time() - start_time < ftp_object.duration:
            time.sleep(1)
            if(ftp_object.power_data != None): 
                print("Current power: ", ftp_object.power_data[-1])
                print("Current time: ", time.time() - start_time)
            else:
                print("No power data received")

    except KeyboardInterrupt:
        print("Test stopped")
        print("Count of data points given: " + str(len(ftp_object.power_data)))
        pass


def set_workout_duration(ftp_object) -> FTP:
    init = False
    while(init == False):
        print("Enter selection for FTP Workout mode:\n1: Test/Dev mode (2 minutes)\n2: FTP Workout mode (20 minutes)")
        mode_selection = input("Enter selection: ")
        if(mode_selection == "1"):
            ftp_object.duration = 120
            init = True
        elif(mode_selection == "2"):
            ftp_object.duration = 1200
            init = True
        else:
            print("Invalid selection, enter 1 or 2 for selection")

def main():
    try:
        #Create FTP object and initialize duration to user set parameter

        ftp_object = FTP()
        ftp_object.__init__()
        global mqtt_client
        global deviceId
        set_workout_duration(ftp_object)
        # Initialize MQTT client and subscribe to power topic
        mqtt_client = MQTTClient('f5b2a345ee944354b5bf1263284d879e.s1.eu.hivemq.cloud', 'redbackiotclient', 'IoTClient@123')
        print(os.getenv('MQTT_HOSTNAME'), os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
        deviceId = os.getenv('DEVICE_ID')
        mqtt_client.setup_mqtt_client()
        mqtt_client.subscribe(f'bike/000001/power')
        mqtt_client.get_client().on_message = ftp_object.read_remote_data
        mqtt_client.get_client().loop_start()
        
        # Start FTP test
        print("Starting the FTP test...")
        perform_ftp_test(ftp_object)
        ftp_object.calculate_ftp()
        result = ftp_object.get_ftp()
        print(f"Your estimated FTP is: {result:.2f} watts")
        
    except KeyboardInterrupt:
        pass
    mqtt_client.get_client().loop_stop()
    
if __name__ == "__main__":
    main()