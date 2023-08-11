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
                print('Current power:', threshold_object.current_power)
                print('Threshold power: ', threshold_object.get_threshold_power())
            else:
                print('No power data received')
                
    except KeyboardInterrupt:
        print('Workout stopped')
        print('Count of data points given: ' + str(len(threshold_object.power_data)))
        mqtt_client.get_client().loop_stop()
        exit()

def user_input(threshold_object):
    # User input for interval
    interval = input('Enter amount of interval: ')
    if interval == '':
        print('No input given, defaulting to 3 interval')
        threshold_object.set_interval(3)
    else:
        print('Interval is set to', interval, 'intervals')
        threshold_object.set_interval(int(interval))
        
    # User input for duration
    duration = input('Enter workout duration for each interval (in minutes): ')
    if duration == '':
        print('No input given, defaulting to 5 minutes')
        threshold_object.set_duration(5)
    else:
        print('Duration is set to', duration, 'minutes')
        threshold_object.set_duration(int(duration))

    # User input for rest
    rest = input('Enter rest duration between each intervals (in seconds): ')
    if rest == '':
        print('No input given, defaulting to 30 seconds')
        threshold_object.set_rest(30)    
    else:
        print('Rest is set to', rest, 'seconds')
        threshold_object.set_rest(int(rest))
        
    # user input for threshold power
    threshold_power = input('Enter threshold power (in Watts): ')
    if threshold_power == '':
        print('No input giver, defaulting to 200 Watts')
        threshold_object.set_threshold_power(200)
    else:
        print('Threshold power is set to', threshold_power, 'Watts')
        threshold_object.set_threshold_power(int(threshold_power))

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
    # possible improvement, create calculation, print result
    
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
        # topic2 = f'bike/{deviceId}/speed'
        print(deviceId)
        print(topic1)
        # print(topic2)
        mqtt_client.setup_mqtt_client()
        mqtt_client.subscribe(topic1)
        # mqtt_client.subscribe(topic2)
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