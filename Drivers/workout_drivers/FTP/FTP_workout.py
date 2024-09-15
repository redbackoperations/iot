#!/usr/bin/env python3
#! bin/bash
#! bin/sh
import sys
import time
import os
from mqtt_client import MQTTClient
from FTP_class import FTP
from dotenv import load_dotenv, set_key
import argparse

parser = argparse.ArgumentParser(description="Run a FTP workout.")
parser.add_argument("-r", "--resistance", type=int, help="Initial resistance level", required=True)
parser.add_argument("-t", "--time", type=int, help="Duration of the FTP test in minutes", default=20)
args = parser.parse_args()


def perform_ftp_test(ftp_object, resistence_level):
    ## Reads previously saved FTP value from the .env file
    print("Current FTP: ", ftp_object.get_ftp())
    print("Starting FTP test in 5 seconds...")
    time.sleep(5)
    
    start_time = time.time()
    ## Starts with the specified resistence level
    mqtt_client.publish(f"bike/000001/resistance/control", resistence_level)
    try:
        #NOTE: adding a value in the command line will set the duration of the test in minutes
        while time.time() - start_time < (ftp_object.duration*60):
            # Counts up to the duration set by the user 
            time.sleep(1)
            if(ftp_object.power_data != None): 
                print("Current power: ", ftp_object.power_data[-1])
                print("Current time: ", time.time() - start_time)
                # adds the current power to the power data list in FTP object
                ftp_object.power_data.append(ftp_object.current_power)
            else:
                print("No power data received")

    except KeyboardInterrupt:
        print("Test stopped")
        print("Count of data points given: " + str(len(ftp_object.power_data)))
        pass

def set_workout_duration(ftp_object, duration) -> None:
    ftp_object.duration = duration
    print(f"Duration set to {duration} minutes")

    
def main():
    try:
        # Load environment variables from pi's .env file
        # This is necessary to get the MQTT credentials
        # The .env file is not included in the repository
        
        #Instantiate FTP object and initialize duration to user set parameter
        env_path = '/home/pi/.env'
        load_dotenv(env_path)
        ftp_object = FTP()
        ftp_object.__init__()
        global mqtt_client
        global deviceId
        set_workout_duration(ftp_object, args.time)
        
        # Initialize MQTT client and subscribe to power topic
        mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
        deviceId = os.getenv('DEVICE_ID')
        topic = f'bike/{deviceId}/power'
        print(deviceId)
        print(topic)
        mqtt_client.setup_mqtt_client()
        mqtt_client.subscribe(topic)
        mqtt_client.get_client().on_message = ftp_object.read_remote_data
        mqtt_client.get_client().loop_start()

        resistence_topic = f'bike/{deviceId}/resistance'
        print(deviceId)
        print(resistence_topic)
        mqtt_client.setup_mqtt_client()
        mqtt_client.subscribe(resistence_topic)
        mqtt_client.get_client().on_message = ftp_object.read_remote_data
        
        # Start FTP test
        print("Starting the FTP test...")
        resistance_level = args.resistance
        perform_ftp_test(ftp_object, resistance_level)
        ftp_object.calculate_ftp()
        result = ftp_object.get_ftp()
        print(f"Your estimated FTP is: {result:.2f} watts")
        print("Test complete, saving FTP to file...")
        set_key(env_path, 'FTP_SCORE', str(result))
        
    except KeyboardInterrupt:
        pass
    mqtt_client.get_client().loop_stop()
    
if __name__ == "__main__":
    main()



