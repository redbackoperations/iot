#!/usr/bin/env python3
import gatt
from mqtt_client import MQTTClient
import os
import time
import platform
import json

# Subclass gatt.DeviceManager to allow discovery only of TICKR devices
# When the alias begins with the required prefix, connect to the device
class AnyDeviceManager(gatt.DeviceManager):
    def device_discovered(self, device):
        alias = device.alias()
        if alias is not None and self.prefix is not None and len(alias) >= len(self.prefix) and alias[0:len(self.prefix)] == self.prefix:
            #print("[%s] Discovered, alias = %s" % (device.mac_address, device.alias()))
            device = AnyDevice(mac_address=device.mac_address, manager=self)
            device.connect()
            device.zero_limit = 10
            device.zeroCount = 0

# Subclass gatt.Device to implement the Heart Rate Protocol
class AnyDevice(gatt.Device):
    # When the program exits, stop measurements and discovery services
    #def __del__(self):
        #self.stop_measurements()
        #self.manager.stop_discovery()

    # Called when the connection succeeds
    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))


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
            if s.uuid[4:8] == '180d')

        self.heart_rate_measurement_characteristic = next(
            c for c in heart_rate_service.characteristics
            if c.uuid[4:8] == '2a37')

        self.heart_rate_measurement_characteristic.enable_notifications()


    # Inform the device that we are no longer interested in measurements
    # Find the heart rate service and its measurement characteristic and
    # disable notifications from it
    #def stop_measurements(self):
        #heart_rate_service = next(
            #s for s in self.services
            #if s.uuid[4:8] == '180d')

        #self.heart_rate_measurement_characteristic = next(
            #c for c in heart_rate_service.characteristics
            #if c.uuid[4:8] == '2a37')

        #self.heart_rate_measurement_characteristic.enable_notifications(False)

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
    #rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
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

        # Check the flags
        hr16bit = value[0] & 1
        sensorcontact = (value[0] & 6) >> 1
        energyexpended = (value[0] & 8) >> 3
        rrinterval = (value[0] & 16) >> 4

        # Offset is the current byte in the packet being processed
        offset = 1

        # Parse the heartrate
        if hr16bit:
            heartrate = (value[offset+1] << 8) + value[offset]
            offset += 2
        else:
            heartrate = value[offset]
            offset += 1

        #check for zero heartrate and if limit reached
        if not(heartrate == 0 and self.zeroCount >= self.zero_limit):
            # Parse the sensor contact information (if present)
            if sensorcontact == 2:
                contact = "Not detected"
            elif sensorcontact == 3:
                contact = "Detected"
            else:
                contact = None

            #Parse heartrate to check if 0
            if heartrate == 0:
                self.zeroCount += 1
            else:
                self.zeroCount = 0

            # Parse the energy expended (if present)
            if energyexpended:
                energy = (value[offset+1] << 8) + value[offset]
                offset += 2
            else:
                energy = None

            # Parse the RR interval(s) (if present)
            # If several intervals have occurred since the last measurement
            # they are sent from oldest to newest
            if rrinterval:
                interval = []
                for index in range(offset, len(value), 2):
                    interval.append(float((value[index+1] << 8) + value[index])/1024.0)
                offset = len(value)
            else:
                interval = None

            #print("Heart Rate:",heartrate,"Contact:",contact,"Energy:",energy,"RR:",interval)
            self.publish(ts, heartrate)


    # Publish the heart rate to MQTT
    def publish(self, ts, heartrate):
        topic = f"bike/{deviceId}/heartrate"
        payload = self.mqtt_data_report_payload(heartrate, ts)
        print(f"Publishing {topic} {payload}")
        mqtt_client.publish(topic, payload)

    def mqtt_data_report_payload(self, value, timestamp):
        # TODO: add more json data payload whenever needed later
        return json.dumps({"value": value, "unitName": 'BPM', "timestamp": timestamp, "metadata": { "deviceName": platform.node() } })        

def main():
    try:
        adapter_name=os.getenv('HEART_RATE_ADAPTER_NAME')
        alias_prefix=os.getenv('HEART_RATE_ALIAS_PREFIX')

        global mqtt_client
        global deviceId
        mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), \
            os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
        mqtt_client.setup_mqtt_client()
        deviceId = os.getenv('DEVICE_ID')
        mqtt_client.get_client().loop_start()

        manager = AnyDeviceManager(adapter_name=adapter_name)
        manager.prefix=alias_prefix
        manager.start_discovery()
        manager.run()
    except KeyboardInterrupt:
        pass
    mqtt_client.get_client().loop_stop()


if __name__=="__main__":
    main()
