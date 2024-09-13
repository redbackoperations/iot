#!/usr/bin/env python3

"""
Renamed folder & file
Move onto Pi
Delete old files
give permissions to new files
"""

import os
import sys
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import json
from argparse import ArgumentParser
import logging

# append this file's directory to path
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from lib.mqtt_client import MQTTClient

# set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger_formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

logger_file_handler = logging.FileHandler('turning_control.log') # TODO: setup a logging folder and write all logging files to that folder
logger_file_handler.setFormatter(logger_formatter)

logger_stream_handler = logging.StreamHandler() # this will print all logs to the terminal also

logger.addHandler(logger_file_handler)
logger.addHandler(logger_stream_handler)

# define pins
RIGHT_PIN = 11
LEFT_PIN = 12
BREAK_PIN = 15

# get MQTT credentials from passed values
parser = ArgumentParser(description="Bike turning controller")
parser.add_argument('--broker_address', dest='broker_address', default=os.getenv('MQTT_HOSTNAME'), type=str, help='The MQTT broker address getting from HiveMQ Cloud')
parser.add_argument('--username', dest='username', default=os.getenv('MQTT_USERNAME'), type=str, help='MQTT username')
parser.add_argument('--password', dest='password', default=os.getenv('MQTT_PASSWORD'), type=str, help='MQTT password')
parser.add_argument('--port', dest='port', default=os.getenv('MQTT_PORT'), type=int, help='MQTT broker port')
parser.add_argument('--device_id', dest='device_id', default=os.getenv('DEVICE_ID'), type=str, help="Bike's unique id")
parser.add_argument('--button_topic', dest='button_topic', default=f"bike/{os.getenv('DEVICE_ID')}/button", help='MQTT topic for activity of the buttons on the bike')
args = parser.parse_args()

class Button():

    def __init__(self, pin: int, name: str, client: MQTTClient):

        # define properties
        self._pin = pin
        self._name = name
        self._client = client
        self._state = 0
        self._topic = args.button_topic 
        self._control_topic = args.button_topic + '/report'

        # set up pin & callbacks
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self._pin, GPIO.BOTH, callback=self.state_change, bouncetime=200)

        logger.info(f'initialised {self._name} button')
    
    def state_change(self, pin: int):
        """the callback passes the pin for some reason."""
        # grab the current state
        self._state = GPIO.input(self._pin)

        # publish to MQTT
        payload = json.dumps({'button' : self._name, 'state' : self._state, 'timestamp' : time.time()})
        self._client.publish(self._control_topic, payload)

        # log the change
        if self._state == 0:
            logger.debug(f'{self._name} button released')
        elif self._state == 1:
            logger.debug(f'{self._name} button pressed')    

def main():
    # set up MQTT client
    client = MQTTClient(args.broker_address, args.username, args.password, port=args.port)
    client.setup_mqtt_client()

    # set up GPIO
    GPIO.setmode(GPIO.BOARD)
    
    # create buttons
    left_button = Button(LEFT_PIN, 'LEFT', client)
    right_button = Button(RIGHT_PIN, 'RIGHT', client)
    break_button = Button(BREAK_PIN, 'BREAK', client)

    # loop until terminated
    # TODO: is this actually ok to do?
    try:
        while True:
            pass

    except KeyboardInterrupt:
        GPIO.cleanup()  
        #client.disconnect()
   
if __name__=="__main__":
    main()