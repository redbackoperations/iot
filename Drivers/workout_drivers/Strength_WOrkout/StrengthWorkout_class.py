import time
import json
import os
from dotenv import load_dotenv

class StrengthWorkout():
    def __init__(self):
        
        load_dotenv('/home/pi/.env')
        self.duration = 0
        self.resistance_data = [0]
        self.current_resistance = 0
        
    def get_duration(self):
        return self.duration
    
    def set_duration(self, duration):
        self.duration = duration
        
    def get_resistance_data(self) -> list:
        return self.resistance_data
    
    def set_resistance_data(self, input_data) -> list:
        self.resistance_data = []
        for x in input_data:
            self.resistance_data.append(x)
    
    def calculate_strength(self):
        avg_resistance = sum(self.resistance_data) / len(self.resistance_data)
        return avg_resistance * 0.95
        
    # This is a callback function to be used when a message is received via MQTT in the Strength_Workout.py script.
    # Its use case is only for the strength workout mode and should not be used in any other context.
    def read_remote_data(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        try:
            # Attempt to parse the payload as JSON in line with incline and resistance script output
            dict_of_payload = json.loads(payload)
            resistance_value = dict_of_payload["value"]
            temp = self.resistance_data[-1]
            if temp != resistance_value:
                print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))      
            self.current_resistance = resistance_value
        except json.JSONDecodeError:
            # Treat it as a singular string value
            resistance_value = payload