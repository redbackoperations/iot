import os
from dotenv import load_dotenv

class ThresholdWorkout:
    def __init__(self):
        load_dotenv('/home/pi/.env')
        self.duration = 0
        self.power_data = [0]
        self.threshold_workout = os.environ.get("THRESHOLD_WORKOUT_SCORE")  # Updated variable name
        self.current_power = 0
        self.threshold_power = 0
    
    def set_threshold_workout(self, threshold_workout):  # Updated method name
        self.threshold_workout = threshold_workout
    
    def get_threshold_workout(self):  # Updated method name
        return self.threshold_workout
    
    def get_duration(self):
        return self.duration
    
    def set_duration(self, duration):
        self.duration = duration
        
    def get_power_data(self):
        return self.power_data
    
    def set_power_data(self, input_data):
        self.power_data = []
        for x in input_data:
            self.power_data.append(x)
    
    def calculate_threshold_workout(self):  # Updated method name
        avg_power = sum(self.power_data) / len(self.power_data)
        self.set_threshold_workout(avg_power * 0.95)
        
    def read_remote_data(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        try:
            dict_of_payload = json.loads(payload)
            power_value = dict_of_payload["value"]
            temp = self.power_data[-1]
            if temp != power_value:
                print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))      
            self.current_power = power_value
            self.check_threshold()
        except json.JSONDecodeError:
            power_value = payload
    
    def set_threshold_power(self, threshold):
        self.threshold_power = threshold
    
    def check_threshold(self):
        if self.current_power > self.threshold_power:
            print("Threshold power exceeded!")
            resistance_required = self.calculate_resistance_required(self.current_power)
            print("Resistance required to reach threshold power: ", resistance_required)
            # Perform threshold workout action
            # Replace this with your desired action when the threshold is exceeded
    
    def calculate_power_usage_per_second(self, start_time, power_usage):
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            return power_usage / elapsed_time
        else:
            return 0
    
    def calculate_resistance_required(self, current_power):
        # Calculate the resistance required to reach the threshold power
        # I've used a hardcoded method
        if current_power < 100:
            resistance_required = 5
        elif current_power < 200:
            resistance_required = 8
        else:
            resistance_required = 10
        return resistance_required
