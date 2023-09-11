#!/usr/bin/env python3
import sys
import time
import os
from mqtt_client import MQTTClient
from EnduranceWorkout_class import EnduranceWorkout
from dotenv import load_dotenv, set_key

MAX_WORKOUT_DURATION = 20  # Maximum duration of the workout in minutes

def perform_endurance_workout(endurance_workout_object):
    print("Starting endurance workout in 5 seconds...")
    time.sleep(5)

    start_time = time.time()
    try:
        while True:
            current_time = time.time() - start_time
            if current_time >= (endurance_workout_object.duration * 60) or current_time >= (MAX_WORKOUT_DURATION * 60):
                break

            # Read the user's desired incline from the command line
            incline_input = input("Enter the incline (-10 to 19 with a step of 0.5): ")
            try:
                incline = float(incline_input)
                if incline < -10 or incline > 19 or incline % 0.5 != 0:
                    print("Invalid incline value. Please enter a value between -10 and 19 with a step of 0.5.")
                    continue

                # Store the incline, current time, and perform the endurance workout action
                endurance_workout_object.incline_data.append(incline)
                endurance_workout_object.time_data.append(current_time)
                endurance_workout_object.perform_action(incline)

            except ValueError:
                print("Invalid incline value. Please enter a value between -10 and 19 with a step of 0.5.")

            time.sleep(1)

    except KeyboardInterrupt:
        print("Workout stopped")
        print("Count of data points given: " + str(len(endurance_workout_object.incline_data)))

def set_workout_duration(endurance_workout_object):
    # Read the command line argument for setting the duration of the workout
    if len(sys.argv) > 1:
        endurance_workout_object.duration = int(sys.argv[1])
        if endurance_workout_object.duration > MAX_WORKOUT_DURATION:
            endurance_workout_object.duration = MAX_WORKOUT_DURATION
            print("Duration exceeds maximum limit of 20 minutes. Setting duration to 20 minutes.")
        print("Duration set to " + str(endurance_workout_object.duration) + " minutes")
    else:
        # Default duration is 20 minutes (no argument given)
        endurance_workout_object.duration = 20
        print("Duration not specified, defaulting to 20 minutes")

def main():
    try:
        # Load environment variables from the .env file
        env_path = '/home/pi/.env'
        load_dotenv(env_path)

        # Instantiate EnduranceWorkout object and initialize duration to user-set parameter
        endurance_workout_object = EnduranceWorkout()
        endurance_workout_object.__init__()

        global mqtt_client
        global deviceId

        set_workout_duration(endurance_workout_object)

        # Initialize MQTT client and subscribe to incline topic
        mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
        deviceId = os.getenv('DEVICE_ID')
        topic = f'bike/{deviceId}/incline'
        print(deviceId)
        print(topic)
        mqtt_client.setup_mqtt_client()
        mqtt_client.subscribe(topic)
        mqtt_client.get_client().on_message = endurance_workout_object.read_remote_data

        mqtt_client.get_client().loop_start()

        # Start the endurance
        # Start the endurance workout
        print("Starting the endurance workout...")
        perform_endurance_workout(endurance_workout_object)
        print("Workout complete.")

    except KeyboardInterrupt:
        pass
    mqtt_client.get_client().loop_stop()

if __name__ == "__main__":
    main()
