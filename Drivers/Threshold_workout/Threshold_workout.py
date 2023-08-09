#!/usr/bin/env python3
import sys
import time
import os
from mqtt_client import MQTTClient
from Threshold_class import ThresholdWorkout
from dotenv import load_dotenv, set_key

def perform_threshold_test(threshold_workout_object):
    print("Current Threshold Workout: ", threshold_workout_object.get_threshold_workout())
    print("Starting threshold test in 5 seconds...")
    time.sleep(5)
    
    start_time = time.time()
    power_usage = 0
    try:
        while time.time() - start_time < (threshold_workout_object.get_duration() * 60):
            time.sleep(1)
            if threshold_workout_object.get_power_data() is not None:
                current_power = threshold_workout_object.get_power_data()[-1]
                power_usage += current_power
                print("Current power: ", current_power)
                power_usage_per_sec = threshold_workout_object.calculate_power_usage_per_second(start_time, power_usage)
                print("Power usage per second: ", power_usage_per_sec)
                if current_power > threshold_workout_object.threshold_power:
                    print("Threshold power exceeded!")
                    resistance_required = threshold_workout_object.calculate_resistance_required(current_power)
                    print("Resistance required to reach threshold power: ", resistance_required)
            else:
                print("No power data received")

    except KeyboardInterrupt:
        print("Test stopped")
        print("Count of data points given: " + str(len(threshold_workout_object.get_power_data())))
        pass



def set_workout_duration(threshold_workout_object):
    if len(sys.argv) > 1:
        threshold_workout_object.set_duration(int(sys.argv[1]))
        print("Duration set to " + str(sys.argv[1]) + " minutes")
    else:
        threshold_workout_object.set_duration(20)
        print("Duration not specified, defaulting to 20 minutes")

def set_threshold_power(threshold_workout_object):
    if len(sys.argv) > 2:
        threshold_workout_object.set_threshold_power(int(sys.argv[2]))
        print("Threshold power set to " + str(sys.argv[2]) + " watts")
    else:
        threshold_workout_object.set_threshold_power(200)
        print("Threshold power not specified, defaulting to 200 watts")

def main():
    try:
        env_path = '/home/pi/.env'
        load_dotenv(env_path)
        threshold_workout_object = ThresholdWorkout()  # Updated class name
        threshold_workout_object.__init__()  # Removed redundant initialization
        global mqtt_client
        global deviceId
        set_workout_duration(threshold_workout_object)
        set_threshold_power(threshold_workout_object)
        
        mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
        deviceId = os.getenv('DEVICE_ID')
        topic = f'bike/{deviceId}/power'
        print(deviceId)
        print(topic)
        mqtt_client.setup_mqtt_client()
        mqtt_client.subscribe(topic)
        mqtt_client.get_client().on_message = threshold_workout_object.read_remote_data
        mqtt_client.get_client().loop_start()
        
        print("Starting the threshold test...")
        perform_threshold_test(threshold_workout_object)  # Updated variable name
        
    except KeyboardInterrupt:
        pass
    mqtt_client.get_client().loop_stop()

if __name__ == "__main__":
    main()
