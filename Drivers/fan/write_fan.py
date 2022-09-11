#!/usr/bin/env python3

import gatt
import sys
import struct

manager = gatt.DeviceManager(adapter_name='hci0')

# Send a given value to the fan through Bluetooth
class AnyDevice(gatt.Device):
	def services_resolved(self):
		super().services_resolved()

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
		value = bytes([0x20, 0xee, 0xfc])
		self.enable_characteristic.write_value(value)

	def characteristic_write_value_succeeded(self, characteristic):
		if characteristic == self.enable_characteristic:
			print(f"Communication enabled")
			value = bytes([0x02, self.speed])
			self.fan_characteristic.write_value(value)
		if characteristic == self.fan_characteristic:
			print(f"Speed set to {self.speed}")

	def characteristic_write_value_failed(self, error):
		print("Write failed")

	def characteristic_enable_notifications_succeeded(self, characteristic):
		print("Notifications enabled")

	def characteristic_enable_notifications_failed(self, characteristic, error):
		print("Notifications failed")

	def characteristic_value_updated(self, characteristic, value):
		if characteristic == self.enable_characteristic:
			print(f"Updated Enable: {value}")
		if characteristic == self.fan_characteristic:
			print(f"Updated Fan: {value}")


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} speed")
    print("Where speed is in range 0 to 100")
    exit(1)

speed = int(sys.argv[1])
if speed < 0 or speed > 100:
    print(f"Usage: {sys.argv[0]} speed")
    print("Where speed is in range 0 to 100")
    exit(1)

device = AnyDevice(mac_address='ed:cb:f5:da:d3:f5', manager=manager)
device.speed = speed
device.connect()
manager.run()
