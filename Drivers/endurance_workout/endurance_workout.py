
#!/usr/bin/env python3
import sys
import time
import os
import csv
from mqtt_client import MQTTClient
from EnduranceWorkout_class import EnduranceWorkout
from dotenv import load_dotenv, set_key

MAX_WORKOUT_DURATION = 20  # Maximum duration of the workout in minutes

parser = argparse.ArgumentParser(description="Run an endurance workout.")
parser.add_argument("-t", "--time", type=int, help="Workout time in minutes", default=20)
parser.add_argument("-d", "--distance", type=float, help="Target distance in kilometers", required=True)
parser.add_argument("-r", "--resistance", type=int, help="Initial incline level", required=True)
args = parser.parse_args()

def perform_actions(incline_level):
    mqtt_client.publish(f"bike/000001/incline/control", incline_level)

# Global Variables
speed_data_file = 'speed_data.csv'

def record_speed_data(client, userdata, message):
    """Callback function to handle incoming speed data and write to a CSV."""
    with open(speed_data_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([time.time(), message.payload.decode()])  # write current time and speed value    

def perform_endurance_workout(endurance_workout_object, target_distance):
    print("Starting endurance workout in 5 seconds...")
    time.sleep(5)
    start_time = time.time()    
    
    incline_level = args.resistance  # initialize incline_level using the resistance argument

    try:
        while True:
            current_time = time.time() - start_time
            distance_covered = calculate_distance_from_csv()

            if distance_covered >= target_distance:
                print(f"Target distance of {target_distance} km reached!")
                break
            
            if current_time >= (endurance_workout_object.duration * 60) or current_time >= (MAX_WORKOUT_DURATION * 60):
                break

            # Store the incline level in the endurance workout object
            endurance_workout_object.incline_data.append(incline_level)

            # Perform the endurance workout action based on the incline level
            perform_actions(incline_level)

            if current_time % 120 == 0 and incline_level < 19:
                incline_level += 0.5

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
        speed_topic = f'bike/{deviceId}/speed'
        mqtt_client.subscribe(speed_topic)
        mqtt_client.get_client().on_message = record_speed_data

        mqtt_client.get_client().loop_start()

        # Start the endurance
        # Start the endurance workout
        target_distance = float(input("Enter the distance you want to travel (in kilometers): "))
        incline_level = args.incline        
        print("Starting the endurance workout...")
        perform_endurance_workout(endurance_workout_object, target_distance)
        print(f"Total distance covered: {calculate_distance_from_csv()} kilometers")
        print("Workout complete.")

    except KeyboardInterrupt:
        pass
    mqtt_client.get_client().loop_stop()

if __name__ == "__main__":
    main()
