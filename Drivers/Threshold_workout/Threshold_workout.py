import sys
import time
import os
from mqtt_client import MQTTClient
from Threshold_class import ThresholdWorkout
from dotenv import load_dotenv, set_key

def perform_threshold_workout(threshold_object):
    # Countdown
    for i in range(5):
        print('Starting threshold workout in', 5-i)
        time.sleep(1)
    print('Good Luck!!!')
    
    # Start timer
    start_time = time.time()
    
    # Fetch data from sensor while in workout duration
    try:
        while time.time() - start_time < (threshold_object.get_duration()*60):
            time.sleep(1)
            if threshold_object.current_power is not None:
                print('Current Speed:', threshold_object.current_speed)
                print('Current power:', threshold_object.current_power)
                print('Threshold power: ', threshold_object.get_threshold_power())
                print('-------------------------------')
            else:
                print('No power data received')
                
    except KeyboardInterrupt:
        print('Workout stopped')
        print('Count of data points given: ' + str(len(threshold_object.power_data)))
        mqtt_client.get_client().loop_stop()
        exit()

def user_input(threshold_object):
    """
    Example input: python Threshold_workout.py a b c d, where 
    a -> interval
    b -> duration (in minutes)
    c -> rest (in seconds)
    d -> threshold power (in Watts)
    """
    # Interval
    threshold_object.set_interval(int(sys.argv[1]))
    print("Interval is set to " + str(sys.argv[1]) + " intervals")
    
    # Duration
    threshold_object.set_duration(int(sys.argv[2]))
    print("Duration is set to " + str(sys.argv[2]) + " minutes")

    # Rest
    threshold_object.set_rest(int(sys.argv[3]))
    print("Rest is set to " + str(sys.argv[3]) + " seconds")
        
    # Threshold Power
    threshold_object.set_threshold_power(int(sys.argv[4]))
    print("Threshold power is set to " + str(sys.argv[4]) + " Watts")
    
def start_workout(threshold_object):
    
    # Start Threshold workout, looping for amount of interval
    for i in range(threshold_object.get_interval()):
        print('Starting threshold workout')
        print('Interval number: ', i+1)
        perform_threshold_workout(threshold_object)
        print('Interval number', i+1, 'complete')
        # Rest between each interval, in the last interval no rest
        if i+1 != threshold_object.get_interval():
            print('Resting for', threshold_object.get_rest(), 'seconds')
            time.sleep(threshold_object.get_rest())
            
    print('Congratulations on finishing your workout!!!')
    # possible improvement - create calculation, print result
    threshold_object.calculate_distance()
    threshold_object.calculate_calories()
    print('-----Your Result-----')
    print('Distance travelled:', threshold_object.get_distance(), 'km')
    print('Calories burnt:', threshold_object.get_calories(), 'kcal')
    
def main():
    try:
        env_path = '/home/pi/.env'
        load_dotenv(env_path)
        threshold_object = ThresholdWorkout()  # Create threshold object
        threshold_object.__init__()
        global mqtt_client
        global deviceId
        
        # Create user input
        print('-----Welcome to threshold workout-----')
        user_input(threshold_object)
        
        # Initialize MQTT client and subcribe to power topic
        mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
        deviceId = os.getenv('DEVICE_ID')
        topic1 = f'bike/{deviceId}/power'
        topic2 = f'bike/{deviceId}/speed'
        print(deviceId)
        print(topic1)
        print(topic2)
        mqtt_client.setup_mqtt_client()
        mqtt_client.subscribe(topic1)
        mqtt_client.subscribe(topic2)
        mqtt_client.get_client().on_message = threshold_object.read_message
        mqtt_client.get_client().loop_start()
        time.sleep(1)
        
        # Start workout program
        start_workout(threshold_object)
                
    except KeyboardInterrupt:
        pass
    
    mqtt_client.get_client().loop_stop()
    
if __name__ == '__main__':
    main()