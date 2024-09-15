import os
import time
import json
from dotenv import load_dotenv

class ThresholdWorkout:
    def __init__(self):
        load_dotenv('home/pi/.env')
        self.threshold_workout = os.environ.get('THRESHOLD_WORKOUT_SCORE')
        self.current_power = 0
        self.power_data = []
        self.calories = 0
        self.current_speed = 0
        self.speed_data = []
        self.distance = 0
        self.interval = 0
        self.duration = 0
        self.rest = 0
        self.threshold_power = 0
        
    # set and get variables
    def set_interval(self, interval):
        self.interval = interval
    def get_interval(self):
        return self.interval    
        
    def set_duration(self, duration):
        self.duration = duration
    def get_duration(self):
        return self.duration
    
    def set_rest(self, rest):
        self.rest = rest
    def get_rest(self):
        return self.rest
    
    def set_threshold_power(self, threshold):
        self.threshold_power = threshold
    def get_threshold_power(self):
        return self.threshold_power
    
    # Check threshold
    def check_threshold(self):
        if self.current_power > self.threshold_power:
            print('Threshold power exceeded!')
    
    # Calculate distance travelled
    def calculate_distance(self):
        # formula - distance(m) = speed(m/s)*time(second)
        speed = sum(self.speed_data) / len(self.speed_data)
        time = (self.duration * self.interval) * 60
        dist = speed * time
        
        self.distance = str(round(dist/1000, 2))
    def get_distance(self):
        return self.distance
    
    # Calculate calories burnt
    def calculate_calories(self):
        # formula - Cal(kcal) = avg_power(Watts)*time(hour)*3.6
        avg_power = sum(self.power_data) / len(self.power_data)
        time = (self.duration * self.interval) / 60
        Cal = avg_power * time * 3.6
        
        self.calories = str(round(Cal, 2))
    def get_calories(self):
        return self.calories
    
    # Future improvement - calculate current power per second
    def calculate_power_poer_second(self):
        pass
    
    
    # Receive message
    def read_message(self, client, userdata, msg):
        deviceId = os.getenv('DEVICE_ID')
        
        # Get power data from MQTT
        if msg.topic == f'bike/{deviceId}/power':
            power_payload = msg.payload.decode('utf-8')
            dict_of_power_payload = json.loads(power_payload)
            power_value = dict_of_power_payload['value']
            # print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
            self.current_power = power_value
            self.check_threshold()
            self.power_data.append(power_value)
            
        # Get speed data from MQTT
        if msg.topic == f'bike/{deviceId}/speed':
            speed_payload = msg.payload.decode('utf-8')
            dict_of_speed_payload = json.loads(speed_payload)
            speed_value = dict_of_speed_payload["value"]
            # print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
            self.current_speed = speed_value
            self.speed_data.append(speed_value)
            