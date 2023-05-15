#!/usr/bin/env python3
import sys
import time
import os
from mqtt_client import MQTTClient
from FTP_class import FTP
from dotenv import load_dotenv, set_key

def perform_threshold_test(ftp_object):
    print("Current FTP: ", ftp_object.get_ftp())
    print("Starting threshold test in 5 seconds...")
    time.sleep(5)
    
    start_time = time.time()
    power_usage = 0
    try:
        while time.time() - start_time < (ftp_object.duration * 60):
            time.sleep(1)
            if ftp_object.power_data is not None:
                current_power = ftp_object.power_data[-1]
                power_usage += current_power
                print("Current power: ", current_power)
                power_usage_per_sec = ftp_object.calculate_power_usage_per_second(start_time, power_usage)
                print("Power usage per second: ", power_usage_per_sec)
                if current_power > ftp_object.threshold_power:
                    print("Threshold power exceeded!")
                    resistance_required = ftp_object.calculate_resistance_required(current_power)
                    print("Resistance required to reach threshold power: ", resistance_required)
            else:
                print("No power data received")

    except KeyboardInterrupt:
        print("Test stopped")
        print("Count of data points given: " + str(len(ftp_object.power_data)))
        pass



def set_workout_duration(ftp_object):
    if len(sys.argv) > 1:
        ftp_object.duration = int(sys.argv[1])
        print("Duration set to " + str(sys.argv[1]) + " minutes")
    else:
        ftp_object.duration = 20
        print("Duration not specified, defaulting to 20 minutes")

def set_threshold_power(ftp_object):
    if len(sys.argv) > 2:
        ftp_object.threshold_power = int(sys.argv[2])
        print("Threshold power set to " + str(sys.argv[2]) + " watts")
    else:
        ftp_object.threshold_power = 200
        print("Threshold power not specified, defaulting to 200 watts")

def main():
    try:
        env_path = '/home/pi/.env'
        load_dotenv(env_path)
        ftp_object = FTP()
        ftp_object.__init__()
        global mqtt_client
        global deviceId
        set_workout_duration(ftp_object)
        set_threshold_power(ftp_object)
        
        mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
        deviceId = os.getenv('DEVICE_ID')
        topic = f'bike/{deviceId}/power'
        print(deviceId)
        print(topic)
        mqtt_client.setup_mqtt_client()
        mqtt_client.subscribe(topic)
        mqtt_client.get_client().on_message = ftp_object.read_remote_data
        mqtt_client.get_client().loop_start()
        
        print("Starting the threshold test...")
        perform_threshold_test(ftp_object)
        
    except KeyboardInterrupt:
        pass
    mqtt_client.get_client().loop_stop()

if __name__ == "__main__":
    main()
