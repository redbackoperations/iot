import time
import json
import os
from dotenv import load_dotenv

class FTP():
    def __init__(self):
        
        load_dotenv('/home/pi/.env')
        self.duration = 0
        self.power_data = [0]
        self.ftp = os.environ.get("FTP_SCORE")
        self.current_power = 0
        
    def set_ftp(self, ftp):
        self.ftp = ftp    
    
    def get_ftp(self):
        return self.ftp
    
    def get_duration(self):
        return self.duration
    
    def set_duration(self, duration):
        self.duration = duration
        
    def get_power_data(self) -> list:
        return self.power_data
    
    def set_power_data(self, input_data) -> list:
        self.power_data = []
        for x in input_data:
            self.power_data.append(x)
    
    def calculate_ftp(self):
        avg_power = sum(self.power_data) / len(self.power_data)
        self.set_ftp(avg_power * 0.95)  
        
    # This is a callback function is to be used a message is received via MQTT in the FTP_Workout.py script,
    # Its use case is only for the FTP workout mode, and it is not to be used in any other context
    def read_remote_data(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        try:
            # Attempt to parse the payload as JSON in line with incline and resistance script output
            dict_of_payload = json.loads(payload)
            power_value = dict_of_payload["value"]
            temp = self.power_data[-1]
            if temp != power_value:
                print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))      
            self.current_power = power_value
        except json.JSONDecodeError:
            # treat it as a singular string value
            power_value = payload
        
        

        
        


