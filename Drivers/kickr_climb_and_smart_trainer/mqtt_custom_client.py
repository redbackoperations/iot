#!/usr/bin/env python3

import re
import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from lib.mqtt_client import MQTTClient
from lib.constants import RESISTANCE_MIN, RESISTANCE_MAX, INCLINE_MIN, INCLINE_MAX

# define a custom MQTT Client to be able send BLE FTMS commands while receiving command messages from a MQTT command topic
class MQTTClientWithSendingFTMSCommands(MQTTClient):
    def __init__(self, broker_address, username, password, device):
        super().__init__(broker_address, username, password)
        self.device = device

    def on_message(self, client, userdata, msg):
        # positve number for resistance value; positve/negative number for inclination value
        value = str(msg.payload, 'utf-8')
        print(f"[MQTT message received for Topic: '{msg.topic}', QOS: {str(msg.qos)}] ", str(value))

        if bool(re.search("[-+]?\d+$", value)):
            int_value = int(value)
            if bool(re.search("/incline", msg.topic, re.IGNORECASE)):
                if int_value > INCLINE_MAX or int_value < INCLINE_MIN:
                    message = f"Skip invalid incline value: {int_value} (the range has to be: {INCLINE_MIN}% - {INCLINE_MAX}%)"
                    print(message)

                    self.publish(self.device.args.incline_report_topic, message)
                else:
                    self.device.custom_control_point_set_target_inclination(int_value)
            elif bool(re.search("/resistance", msg.topic, re.IGNORECASE)):
                if int_value > RESISTANCE_MAX or int_value < RESISTANCE_MIN:
                    message = f"Skip invalid resistance value: {int_value}"
                    print(message)

                    self.publish(self.device.args.resistance_report_topic, message)
                else:
                    self.device.ftms_set_target_resistance_level(int_value)
            else:
                print("The command topic is not idetified.")
        else:
            print("Skip the invalid command payload.")