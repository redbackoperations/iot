#!/usr/bin/env python3
#
# process - Read the gas sensor output from the arduino and send it to the
# cloud using MQTTS
#
# To install dependencies:
# sudo apt-get install python3-serial
# sudo apt-get install python3-pip
# sudo pip3 install paho-mqtt

import os
import serial
import time
import paho.mqtt.client as paho
from paho import mqtt

# The Arduino should output a comma separated list
# where each field starts with the fieldNames portion
# has a space followed by a long integer (or -- if not valid)
# another space and then the unitNames portion
#
# Time: 1000 ms, O2: 210000 ppm, CO2: 400 ppm, Inflow: 18000 mL/min, Outflow: 0 mL/min
fieldNames = ["Time:", "O2:", "CO2:", "Inflow:", "Outflow:"]
unitNames = ["ms", "ppm", "ppm", "mL/min", "mL/min"]

# Augment the data with the bike's identifier
bikeId = 1

# Credentials for MQTT
mqttHostname = os.environ.get('MQTT_HOSTNAME')
mqttPort = int(os.environ.get('MQTT_PORT'))
mqttUsername = os.environ.get('MQTT_USERNAME')
mqttPassword = os.environ.get('MQTT_PASSWORD')

# Callback when MQTT connects
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# Callback when MQTT publishes
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# Callback when MQTT subscribes
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Callback when message received
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# setup_mqtt - Establish a connection with HiveMQ
# Params: None
# Returns - a client used for connecting to HiveMQ
def setup_mqtt():
  client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
  client.on_connect = on_connect
  client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
  client.username_pw_set(mqttUsername, mqttPassword)
  client.connect(mqttHostname, mqttPort)
  client.on_subscribe = on_subscribe
  client.on_message = on_message
  client.on_publish = on_publish
  return client

# Publish - Publish the values to HiveMQ
# Params: client - the client used to publish to MQTT
#         id - the identifier of the bike (used in the topic)
#         ts - the timestamp since the epoch (TODO: Confirm this is UTC not local time)
#         values - a list of fields extracted from the Arduino
# Returns: Nothing
# Currently just print the information to the screen
# Once MQTTS is set up, send it to HiveMQ
def publish(client, id, ts, values):
  #print(f"Timestamp: {ts} Bike ID: {id} O2: {values[1]} CO2: {values[2]} Inflow {values[3]} Outflow {values[4]}")
  topic=f"bike/{id}/gas"
  payload=f"{{\"ts\": {ts}, \"O2\": {values[1]}, \"CO2\": {values[2]}, \"Inflow\": {values[3]}, \"Outflow\": {values[4]}}}"
  client.publish(topic, payload=payload, qos=2)

# Main - Parse the input from the arduino and send it to the clooud
# Params: None
# Returns: Nothing
#
# The input is read from /dev/ttyACM0
# and parsed according to the specification above
#
# If an error occurs during processing, ignore that line completely
#
# Continue indefinitely (or until the user exits with Ctrl-C
def main():
  # Create a connection and start handling events in another thread
  client = setup_mqtt()
  client.loop_start()

  try:
    # Open the serial port
    with serial.Serial('/dev/ttyACM0') as ser:
      while True:
        try:
          # Read a line from the serial port and convert it to fields
          line = str(ser.readline(), 'utf-8')
          # Save the timestamp (as the Arduino gives time since boot)
          timestamp = time.time()
          fields = line.strip().split(',')

          # Initialise values for all fields to None
          values = [None, None, None, None, None]

          # Parse each field
          for field in fields:
            # There should be three tokens
            # 0 - the field name
            # 1 - the actual value
            # 2 - the units
            tokens = field.strip().split(' ')
            # Find the field name in the list
            index = fieldNames.index(tokens[0])
            # Check the units are valid
            if tokens[2].strip() != unitNames[index]:
              raise ValueError
            # If the value is not --, store it
            if tokens[1] != "--":
              values[index] = int(tokens[1])

          publish(client, bikeId, timestamp, values)
        except UnicodeDecodeError:
          print("ERROR: Unable to decode line")
        except ValueError:
          print("ERROR: Unable to determine value")
  except KeyboardInterrupt:
    pass

  # Stop automatic reconnection now the program is finished
  client.loop_stop()


if __name__=="__main__":
  main()
