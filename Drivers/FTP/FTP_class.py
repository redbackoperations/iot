import time
import json

class FTP():
    def __init__(self):
        self.duration = 0
        self.power_data = [1]
        self.ftp = 0
        self.power_data.append(1)
        
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
        
    def read_remote_data(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        try:
            # Attempt to parse the payload as JSON in line with incline and resistance script output
            dict_of_payload = json.loads(payload)
            power_value = dict_of_payload["value"]
            temp = self.power_data[-1]
            if temp != power_value:
                print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))      
                
        except json.JSONDecodeError:
            # treat it as a singular string value
            power_value = payload
        
        self.power_data.append(power_value)

        
        


