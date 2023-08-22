#!/usr/bin/env python3
import gatt
import sys
import struct
from mqtt_client import MQTTClient
import os
import json
import time
import platform


# When a message is received from MQTT on the fan topic for this bike, it is received here
def message(client, userdata, msg):
	payload = msg.payload.decode("utf-8") #msg received is speed of the bike in m/s
	print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
	
 	#Extract value from payload
	dict_of_payload = json.loads(payload)
	bike_speed = int(dict_of_payload["value"])
	print("Processed speed to set to device: ", bike_speed)
	if bike_speed != 0:
		if bike_speed < 0:
			print(f"Invalid speed in message: {msg}")
			return
		# Maximum bike speed is around 20 m/s, setting fan_speed according to bike_speed
		if bike_speed == 0:
			fan_speed = 0 # Minimum fan speed
		elif bike_speed > 0 and bike_speed <= 4:
			fan_speed = 20
		elif bike_speed > 4 and bike_speed <= 8:
			fan_speed = 40
		elif bike_speed > 8 and bike_speed <= 12:
			fan_speed = 60
		elif bike_speed > 12 and bike_speed <= 16:
			fan_speed = 80
		elif bike_speed > 16:
			fan_speed = 100 # Maximum fan speed
		else:
			print(f"Invalid speed in message: {msg}")
			return

		print(f"Setting speed to {fan_speed}")
		device.set_speed(fan_speed)

# Called when an update is published back to MQTT.
# Stop the default implementation from printing the message id to the log
def publish(client, userdata, mid, properties=None):
	pass

# Subclass gatt.DeviceManager to allow discovery only of HEADWIND devices
# When the alias begins with the required prefix, connect to the device
class AnyDeviceManager(gatt.DeviceManager):
	def device_discovered(self, dev):
		alias = dev.alias()
		if alias is not None and self.prefix is not None and len(alias) >= len(self.prefix) and alias[0:len(self.prefix)] == self.prefix:
			#print("[%s] Discovered, alias = %s" % (dev.mac_address, dev.alias()))
			dev = AnyDevice(mac_address=dev.mac_address, manager=self)
			dev.enableCount = 0
			dev.startCount = 0
			dev.sendCount = 0
			dev.speed = 0
			dev.zeroCount = 0 
			dev.connect()
			dev.zero_limit = 10
			self.stop_discovery()
			global device
			device = dev


# Send a given value to the fan through Bluetooth
class AnyDevice(gatt.Device):
	# Upper limit for number of 0 valued payloads to publish
	
	# When the program exits, stop measurements and discovery services
	def __del__(self):
		self.stop_measurements()

	# Called when the connection succeeds
	def connect_succeeded(self):
		super().connect_succeeded()
		print("[%s] Connected" % (self.mac_address))


	# Called when the connection fails
	# Display an error message on the console
	def connect_failed(self, error):
		super().connect_failed(error)
		print("[%s] Connection failed: %s" % (self.mac_address, str(error)))
		self.manager.start_discovery()

	# Called with disconnection succeeds
	def disconnect_succeeded(self):
		super().disconnect_succeeded()
		#print("[%s] Disconnected" % (self.mac_address))

	# Called externally to set a new fan speed
	# The speed should be between 0 and 100 inclusive
	def set_speed(self, new_speed):
		if new_speed < 0 or new_speed > 100:
			print(f"Invalid speed {new_speed}")
			return

		self.speed = new_speed
		self.sendCount = 0

		# Enable write permission if not already
		# or turn the fan on if it is not ready
		# and then start sending the new speed
		if self.enableCount < 3:
			value = bytes([0x20, 0xee, 0xfc])
			self.enable_characteristic.write_value(value)
		elif self.startCount < 3:
			value = bytes([0x04, 0x04])
			self.fan_characteristic.write_value(value)
		else:
			value = bytes([0x02, self.speed])
			self.fan_characteristic.write_value(value)


	# Once the connection succeded, find the appropriate services and set the fan
	# to be be ready to receive instructions
	def services_resolved(self):
		super().services_resolved()
		self.manager.stop_discovery()

		self.enable_service = next(
			s for s in self.services
			if s.uuid[4:8] == 'ee01')

		self.enable_characteristic = next(
			c for c in self.enable_service.characteristics
			if c.uuid[4:8] == 'e002')

		self.fan_service = next(
			s for s in self.services
			if s.uuid[4:8] == 'ee0c')

		self.fan_characteristic = next(
			c for c in self.fan_service.characteristics
			if c.uuid[4:8] == 'e038')

		self.enable_characteristic.enable_notifications()
		self.fan_characteristic.enable_notifications()

		# Enable write permission
		if self.enableCount < 3:
			value = bytes([0x20, 0xee, 0xfc])
			self.enable_characteristic.write_value(value)

	def stop_measurements(self):
		self.enable_characteristic.enable_notifications(False)
		self.fan_characteristic.enable_notifications(False)

	# Something was successfully written to the sensor, continue
	# with the next command in the sequence. Each command should be
	# sent 3 times to increase the likelihood it is received
	def characteristic_write_value_succeeded(self, characteristic):
		if characteristic == self.enable_characteristic:
			if self.enableCount < 3:
				value = bytes([0x20, 0xee, 0xfc])
				self.enable_characteristic.write_value(value)
				self.enableCount+=1
			elif self.startCount < 3:
				value = bytes([0x04, 0x04])
				self.fan_characteristic.write_value(value)
				self.startCount+=1
		if characteristic == self.fan_characteristic:
			if self.startCount < 3:
				value = bytes([0x04, 0x04])
				self.fan_characteristic.write_value(value)
				self.startCount+=1
			elif self.sendCount < 3:
				value = bytes([0x02, self.speed])
				self.fan_characteristic.write_value(value)
				self.sendCount = self.sendCount + 1
				if self.sendCount == 3:
					print(f"Speed set to {self.speed}")


	def characteristic_write_value_failed(self, error):
		print("Write failed")

	def characteristic_enable_notifications_succeeded(self, characteristic):
		print("Notifications enabled")

	def characteristic_enable_notifications_failed(self, characteristic, error):
		print("Notifications failed")

	def characteristic_value_updated(self, characteristic, value):
		if characteristic == self.enable_characteristic:
			# This remains for debugging, but never seems to be called
			# Instead Notifications enabled is received
			print(f"Updated Enable: {value}")
		if characteristic == self.fan_characteristic:
			# The fan has several payloads to report its speed, but when
			# idle, it returns fd 01 xx 04, where xx is the speed (0 to 100)
			if len(value) == 4 and value[0] == 0xFD and value[1] == 0x01 and value[3] == 0x04:
				# Check for zero value and value of zero counter. Continue if value is not 0 or 0 limit not reached
				if not(value[2] == 0x00 and self.zeroCount >= self.zero_limit):
					# Check if value is 0 and if so inc the zero counter. If value is not 0 then reset 0 counter
					# Zero counter will always reset when non-zero data published so it is most efficient to reset the zero counter
					# every time a non-zero is published as opposed to checking if zero counter is already 0 
					if value[2] == 0x00:
						self.zeroCount += 1
					else:
						self.zeroCount = 0
					reported_speed = value[2]
					topic = f"bike/{deviceId}/fan"
					payload = self.mqtt_data_report_payload(reported_speed)				
					mqtt_client.publish(topic, payload)
					print(f"Published speed: {reported_speed}")

	def mqtt_data_report_payload(self, value):
		# TODO: add more json data payload whenever needed later
		return json.dumps({"value": value, "unitName": 'percentage', "timestamp": time.time(), "metadata": { "deviceName": platform.node() } })

def main():
	try:
		adapter_name=os.getenv('FAN_ADAPTER_NAME')
		alias_prefix=os.getenv('FAN_ALIAS_PREFIX')

		global mqtt_client
		global deviceId
		mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), \
			os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
		mqtt_client.setup_mqtt_client()
		deviceId = os.getenv('DEVICE_ID')
		topic = f'bike/{deviceId}/speed'
		mqtt_client.subscribe(topic)
		mqtt_client.get_client().on_message = message
		mqtt_client.get_client().on_publish = publish
		mqtt_client.get_client().loop_start()

		global manager
		manager = AnyDeviceManager(adapter_name=adapter_name)
		manager.prefix=alias_prefix
		manager.start_discovery()
		manager.run()
	except KeyboardInterrupt:
		pass
	mqtt_client.get_client().loop_stop()


if __name__=="__main__":
    main()
