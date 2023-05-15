#!/usr/bin/env python3

import time
import paho.mqtt.client as paho
from paho import mqtt


# this is a MQTT client that is able to publish to and subscribe from MQTT topics in HiveMQ Cloud
class MQTTClient:
    def __init__(self, broker_address, username, password):
        self.broker_address = broker_address
        self.username = username
        self.password = password
        self.client = None

    def get_client(self):
        return self.client

    def setup_mqtt_client(self):
        # using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
        # userdata is user defined data of any type, updated by user_data_set()
        # client_id is the given name of the client
        self.client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
        self.client.on_connect = on_connect

        # enable TLS for secure connection
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # set username and password
        self.client.username_pw_set(self.username, self.password)
        # connect to HiveMQ Cloud on port 8883 (default for MQTT)
        self.client.connect(self.broker_address, 8883)

        # setting callbacks, use separate functions like above for better visibility
        self.client.on_subscribe = on_subscribe
        self.client.on_message = on_message
        self.client.on_publish = on_publish

    def subscribe(self, topic_name):
        # subscribe to all topics of encyclopedia by using the wildcard "#"
        self.client.subscribe(topic_name, qos=1)

    def publish(self, topic_name, payload):
        # a single publish, this can also be done in loops, etc.
        self.client.publish(topic_name, payload=payload, qos=1)

    def loop_forever(self):
        # loop_forever for simplicity, here you need to stop the loop manually
        # you can also use loop_start and loop_stop
        self.client.loop_forever()

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
