#!/usr/bin/env python3
#! bin/bash
#! bin/sh
import sys
import csv
import time
import os
import json
import argparse
from mqtt_client import MQTTClient
from StrengthWorkout_class import StrengthWorkout
from dotenv import load_dotenv, set_key

MAX_WORKOUT_DURATION = 20  # Maximum duration of the workout in minutes

parser = argparse.ArgumentParser(description="Run a strength workout.")
parser.add_argument("-t", "--time", type=int, help="Workout time in minutes", default=20)
parser.add_argument("-d", "--distance", type=float, help="Target distance in kilometers", required=True)
parser.add_argument("-r", "--resistance", type=int, help="Initial resistance level", required=True)
args = parser.parse_args()

def perform_actions(resistence_level):
    mqtt_client.publish(f"bike/000001/resistance/control", resistence_level)


# Global Variables
speed_data_file = 'speed_data.csv'

def record_speed_data(client, userdata, message):
    """Callback function to handle incoming speed data and write to a CSV."""
    with open(speed_data_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        payload = message.payload.decode("utf-8")
        dict_of_payload = json.loads(payload)
        speed = dict_of_payload["value"]
        writer.writerow([time.time(), speed])  # write current time and speed value


def perform_strength_workout(strength_workout_object, target_distance, resistance_level):
    print("Starting strength workout in 5 seconds...")
    time.sleep(5)
    start_time = time.time()    
    
    try:
        while True:
            current_time = time.time() - start_time
            distance_covered = calculate_distance_from_csv()
            
            if distance_covered >= target_distance:
                print(f"Target distance of {target_distance} km reached!")
                break
            
            if current_time >= (strength_workout_object.duration * 60) or current_time >= (MAX_WORKOUT_DURATION * 60):
                break

            # Store the resistance level in the strength workout object
            strength_workout_object.resistance_data.append(resistance_level)

            # Perform the strength workout action based on the resistance level
            perform_actions(resistance_level)

            if current_time % 120 == 0 and resistance_level < 96:
                resistance_level += 5

            time.sleep(1)

    except KeyboardInterrupt:
        print("Workout stopped")
        print("Count of data points given: " + str(len(strength_workout_object.resistance_data)))


def calculate_distance_from_csv():
    last_time = None
    distance = 0.0  # in kilometers or the unit of speed

    with open(speed_data_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            current_time, speed = float(row[0]), float(row[1])  # Extract time and speed
            if last_time:  # Skip the first row
                time_difference = current_time - last_time  # Time difference in seconds
                distance += (speed * (time_difference / 3600))  # speed * time (converted to hours)
            last_time = current_time

    return distance

def main():
    try:
        # Load environment variables from the .env file
        env_path = '/home/pi/.env'
        load_dotenv(env_path)

        # Instantiate StrengthWorkout object and initialize duration to user-set parameter
        strength_workout_object = StrengthWorkout()
        strength_workout_object.__init__()

        global mqtt_client
        global deviceId


        # Initialize MQTT client and subscribe to resistance topic
        mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
        deviceId = os.getenv('DEVICE_ID')
        topic = f'bike/{deviceId}/resistance'
        print(deviceId)
        print(topic)
        mqtt_client.setup_mqtt_client()
        mqtt_client.subscribe(topic)
        mqtt_client.get_client().on_message = strength_workout_object.read_remote_data

        mqtt_client.get_client().loop_start()
        speed_topic = f'bike/{deviceId}/speed'
        mqtt_client.subscribe(speed_topic)
        mqtt_client.get_client().on_message = record_speed_data

        # Start the strength workout
        target_distance = args.distance
        resistance_level = args.resistance
        strength_workout_object.duration = args.time
        print("Starting the strength workout...")
        perform_strength_workout(strength_workout_object, target_distance, resistance_level)
        print("Workout complete.")
        print(f"Total distance covered: {calculate_distance_from_csv()} kilometers")

    except KeyboardInterrupt:
        pass
    mqtt_client.get_client().loop_stop()

if __name__ == "__main__":
    main()
