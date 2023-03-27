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
    # cadence readings are sent to the characteristic_value_updated callback
    # 0x1816 is cycling speed and cadence GATT Service allocated uuid
    # 0x2A64 is Cycling Power Vector GATT Characteristic and object type
    # 0x2A65 is Cycling power feature ""
    # 0x2A66 is Cycling power control point ""
    # use above three values incase 1816 gives errors
    def start_measurements(self):
        cadence_service = next(
            s for s in self.services
            if s.uuid[4:8] == '1816')

        self.cadence_measurement_characteristic = next(
            c for c in cadence_service.characteristics
            if c.uuid[4:8] == '2a5b')

        self.cadence_measurement_characteristic.enable_notifications()


    # Inform the device that we are no longer interested in measurements
    # Find the heart rate service and its measurement characteristic and
    # disable notifications from it
    def stop_measurements(self):
        cadence_service = next(
            s for s in self.services
            if s.uuid[4:8] == '1816')

        self.cadence_measurement_characteristic = next(
            c for c in cadence_service.characteristics
            if c.uuid[4:8] == '2a5b')

        self.cadence_measurement_characteristic.enable_notifications(False)

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


    # Receive acadence payload (cadence) and extract its information
    # The format depends on the flags set
    #
    # Byte 0: Wheel revolution data present (if feature is not supported - value is 0)
    #          Also indicates if cumulative wheel revolutions and last wheel event time fields are present or not
    # Bit 0 - When both are present, set to 1. When both are absent, set to 0.
    # Bit 1 - set as 1 when cumulative crank revolutions and last crank event time fields are present else 0.
    # Bit 2 - multiple sensor locations supported
    # Bit 3 - 15 - reserved for future use.





    def characteristic_value_updated(self, characteristic, value):
        # Store the timestamp
        ts = time.time()

        print(value)
        self.publish(ts, 0)
        #return

        print(f"Interpreting {list(value.hex())}")

        # getting the binary value of the flags to check if crank data and wheel data is present or not
        bin_value = bin(value[0])

        # converting string to hex, then converting to big endian in order to calculate crank data properly
        print(value.hex())
        little_endian = value.hex()
        conversion = bytearray.fromhex(little_endian)
        conversion.reverse()
        big_endian = conversion.hex()
        print(big_endian)

        global old_crank_revolutions
        global old_crank_event_time

        if (int(bin_value[2]) == 1):
            print("crank data present, ")

            # getting the data

            crank_data = big_endian[:-2]
            crank_event_time = big_endian[0:4]
            crank_revolutions = big_endian[4:8]
            print("crank data", crank_data, "crank event time", crank_event_time, "crank cummulative time",
                  crank_revolutions)

            # converting hex to decimal

            crank_event_time = int(crank_event_time, 16)
            crank_revolutions = int(crank_revolutions, 16)
            print("crank data", crank_data, "crank event time", crank_event_time, "crank cummulative time",
                  crank_revolutions)
            print("old crank revolutions", old_crank_revolutions, "old crank event time", old_crank_event_time)


        else:
            print("crank data not present")

        if (int(bin_value[3]) == 1):
            print("wheel data present")
        else:
            print("wheel data not present")

        try:
            cadence = (crank_revolutions - old_crank_revolutions) / (
                        (crank_event_time - old_crank_event_time) / 1024) * 60
            #publish(cadence)
            self.publish(ts, cadence)
            print(".....................")
            old_crank_revolutions = crank_revolutions
            old_crank_event_time = crank_event_time

        except TypeError:
            print("Nonetype error")
            pass

            


    # Publish the cadence to MQTT
    def publish(self, ts, cadence):
        topic = f"bike/{deviceId}/cadence"
        payload = f"{{timestamp: {ts}, cadence: {cadence}}}"
        print(f"Publishing {topic} {payload}")
        mqtt_client.publish(topic, payload)


def main():
    try:
        adapter_name=os.getenv('CADENCE_ADAPTER_NAME')
        alias_prefix=os.getenv('CADENCE_ALIAS_PREFIX')

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
