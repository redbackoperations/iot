#!/usr/bin/env python3
import gatt
from mqtt_client import MQTTClient
import os
import time

# Subclass gatt.DeviceManager to allow discovery only of TICKR devices
# When the alias begins with the required prefix, connect to the device
class AnyDeviceManager(gatt.DeviceManager):
    def device_discovered(self, device):
        alias = device.alias()
        if alias is not None and self.prefix is not None and len(alias) >= len(self.prefix) and alias[0:len(self.prefix)] == self.prefix:
            print("[%s] Discovered, alias = %s" % (device.mac_address, device.alias()))
            device = AnyDevice(mac_address=device.mac_address, manager=self)
            device.connect()


# Subclass gatt.Device to implement the Heart Rate Protocol
class AnyDevice(gatt.Device):
    # When the program exits, stop measurements and discovery services
    def __del__(self):
        self.stop_measurements()
        self.manager.stop_discovery()

    # Called when the connection succeeds
    def connect_succeeded(self):
        super().connect_succeeded()
        #print("[%s] Connected" % (self.mac_address))


    # Called when the connection fails
    # Display an error message on the console
    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))


    # Called with disconnection succeeds
    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        #print("[%s] Disconnected" % (self.mac_address))


    # Called once the services offered by the bluetooth device have been resolved
    # They can now be used, so start measurements
    def services_resolved(self):
        super().services_resolved()
        self.start_measurements()


    # Find the heart rate service, and its measurement characteristic
    # Enable notifications on the measurement characteristic to ensure that
    # heart rate readings are sent to the characteristic_value_updated callback
    def start_measurements(self):
        heart_rate_service = next(
            s for s in self.services
            if s.uuid[4:8] == 'ee0c')

        self.heart_rate_measurement_characteristic = next(
            c for c in heart_rate_service.characteristics
            if c.uuid[4:8] == 'e038')

        self.heart_rate_measurement_characteristic.enable_notifications()


    # Inform the device that we are no longer interested in measurements
    # Find the heart rate service and its measurement characteristic and
    # disable notifications from it
    def stop_measurements(self):
        heart_rate_service = next(
            s for s in self.services
            if s.uuid[4:8] == 'ee0c')

        self.heart_rate_measurement_characteristic = next(
            c for c in heart_rate_service.characteristics
            if c.uuid[4:8] == 'e038')

        self.heart_rate_measurement_characteristic.enable_notifications(False)

    # Called once the heart rate measurement notification has succeeded
    # Since we will now be receiving notifications,
    # turn off the discovery service
    def characteristic_enable_notifications_succeeded(self, characteristic):
        #print('[%s] Enable Notifications Succeeded' % (self.mac_address))
        self.manager.stop_discovery()


    # Print an error to the console if enabling the heart rate measurement
    # notifications fails
    def characteristic_enable_notifications_failed(self, characteristic, error):
        print("[%s] Enable Notifications Failed: %s" % (self.mac_address, str(error)))


    # Receive a heart rate measurement and extract its information
    # The format depends on the flags set
    #
    # Byte 0: Flags
    # Bit 0 - set if the heart rate is 16 bit (otherwise 8 bit)
    # Bit 1 - set if contact is detected (only valid if bit 2 is also set)
    # Bit 2 - set if contact status is reported
    # Bit 3 - set if energy expenditure is reported
    # Bit 4 - set if rr interval is reported
    # Bits 5-7 - reserved for future use (ignored)
    #
    # Followed by:
    # Heart rate (beats per minute) [uint8, or uint16 if flags Bit 0 is set]
    # Energy (kJ) [uint16, only present if flags Bit 3 is set]
    # RR Interval (1/1024 seconds) [Remaining bytes until end of packet,
    #                               only present if flags bit 4 is set]
    def characteristic_value_updated(self, characteristic, value):
        # Store the timestamp
        ts = time.time()

        print(value)


    # Publish the fan rate to MQTT
    def publish(self, ts, fan):
        topic = f"bike/{deviceId}/fan"
        payload = f"{{timestamp: {ts}, fan: {fan}}}"
        print(f"Publishing {topic} {payload}")
        mqtt_client.publish(topic, payload)


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

        manager = AnyDeviceManager(adapter_name=adapter_name)
        manager.prefix=alias_prefix
        manager.start_discovery()
        manager.run()
    except KeyboardInterrupt:
        pass


if __name__=="__main__":
    main()
