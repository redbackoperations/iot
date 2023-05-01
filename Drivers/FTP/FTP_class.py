import time
import json

class FTP():
    def __init__(self):
        self.duration = 0
        self.power_data = [0]
        self.ftp = 0
        
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
        print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        dict_of_payload = json.loads(msg.payload.decode("utf-8"))
        power_value = dict_of_payload["value"]
        self.power_data.append(power_value)

        
        


