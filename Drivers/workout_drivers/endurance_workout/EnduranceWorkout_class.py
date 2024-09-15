import time
import json
import os
from dotenv import load_dotenv

class EnduranceWorkout:
    def __init__(self):
        load_dotenv('/home/pi/.env')
        self.duration = 0
        self.incline_data = [0]
        self.endurance_score = os.environ.get("ENDURANCE_SCORE")
        self.current_incline = 0

    def set_endurance_score(self, score):
        self.endurance_score = score

    def get_endurance_score(self):
        return self.endurance_score

    def get_duration(self):
        return self.duration

    def set_duration(self, duration):
        self.duration = duration

    def get_incline_data(self):
        return self.incline_data

    def set_incline_data(self, input_data):
        self.incline_data = []
        for x in input_data:
            self.incline_data.append(x)

    def calculate_endurance_score(self):
        total_incline = sum(self.incline_data)
        self.set_endurance_score(total_incline)

    # This callback function is to be used when a message is received via MQTT in the Endurance_Workout.py script.
    # Its use case is only for the endurance workout mode, and it is not to be used in any other context.
    def read_remote_data(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        try:
            # Attempt to parse the payload as JSON in line with incline data script output
            dict_of_payload = json.loads(payload)
            incline_value = dict_of_payload["value"]
            temp = self.incline_data[-1]
            if temp != incline_value:
                print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
            self.current_incline = incline_value
            self.incline_data.append(incline_value)
        except json.JSONDecodeError:
            # Treat it as a singular string value
            incline_value = payload
            self.current_incline = incline_value
            self.incline_data.append(incline_value)
