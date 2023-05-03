#!/usr/bin/env python3
#! bin/bash
#! bin/sh
import sys
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
                ftp_object.power_data.append(ftp_object.current_power)
            else:
                print("No power data received")

    except KeyboardInterrupt:
        print("Test stopped")
        print("Count of data points given: " + str(len(ftp_object.power_data)))
        pass


def set_workout_duration(ftp_object) -> FTP:
    if len(sys.argv) > 1:
        ftp_object.duration = int(sys.argv[1] * 60)
        print("Duration set to " + str(sys.argv[1]) + " minutes")
    else:
        ftp_object.duration = 20 * 60
        print("Duration not specified, defaulting to 20 minutes")
    
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
        print(ftp_object.power_data)
        
    except KeyboardInterrupt:
        pass
    mqtt_client.get_client().loop_stop()
    
if __name__ == "__main__":
    main()
