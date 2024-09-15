from pickle import TRUE
import re
import os
from sqlite3 import Timestamp
import sys
import gatt
import platform
import json
import time
from time import sleep
from mqtt_custom_client import MQTTClientWithSendingFTMSCommands

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from lib.ble_helper import convert_incline_to_op_value, service_or_characteristic_found, service_or_characteristic_found_full_match, decode_int_bytes, covert_negative_value_to_valid_bytes
from lib.constants import FTMS_UUID, RESISTANCE_LEVEL_RANGE_UUID, INCLINATION_RANGE_UUID, FTMS_CONTROL_POINT_UUID, FTMS_REQUEST_CONTROL, FTMS_RESET, FTMS_SET_TARGET_RESISTANCE_LEVEL, INCLINE_REQUEST_CONTROL, INCLINE_CONTROL_OP_CODE, INCLINE_CONTROL_SERVICE_UUID, INCLINE_CONTROL_CHARACTERISTIC_UUID, INDOOR_BIKE_DATA_UUID, DEVICE_UNIT_NAMES

# a sleep time to wait for a characteristic.writevalue() action to be completed
WRITEVALUE_WAIT_TIME = 0.5 # TODO: If this doesn't work well, it needs to change this short sleep mechainism to a async process mechainism for sending consequetive BLE commands (eg., threading control)

class WahooDevice(gatt.Device):
    def __init__(self, mac_address, manager, args, managed=True):
        super().__init__(mac_address, manager, managed)

        # define the initial FTMS Service and the corresponding Characteristics
        self.ftms = None
        self.inclination_range = None
        self.resistance_level_range = None
        self.ftms_control_point = None

        # define the initial Incline Service and the corresponding Characteristics
        self.custom_incline_service = None
        self.custom_incline_characteristic = None

        # define the initial resistance and inclination values
        self.resistance = 0
        self.inclination = 0
        self.new_resistance = None
        self.new_inclination = None

        # define the Characteristics for Indoor Bike Data (reporting speed, cadence and power)
        self.indoor_bike_data = None

        # CLI parser arguments
        self.args = args
        
        # Zero count
        self.zero_count = 0

        # setup MQTT connection
        self.setup_mqtt_connection()

    def setup_mqtt_connection(self):
        self.mqtt_client = MQTTClientWithSendingFTMSCommands(self.args.broker_address, self.args.username, self.args.password, self)
        self.mqtt_client.setup_mqtt_client()

        # subscribe to both resistance and incline command topics
        self.mqtt_client.subscribe([(self.args.resistance_command_topic, 0), (self.args.incline_command_topic, 0)])

    def set_service_or_characteristic(self, service_or_characteristic):
        if service_or_characteristic_found(FTMS_UUID, service_or_characteristic.uuid):
            self.ftms = service_or_characteristic
        elif service_or_characteristic_found_full_match(INCLINE_CONTROL_SERVICE_UUID, service_or_characteristic.uuid):
            self.custom_incline_service = service_or_characteristic
        elif service_or_characteristic_found_full_match(INCLINE_CONTROL_CHARACTERISTIC_UUID, service_or_characteristic.uuid):
            self.custom_incline_characteristic = service_or_characteristic
        elif service_or_characteristic_found(INCLINATION_RANGE_UUID, service_or_characteristic.uuid):
            self.inclination_range = service_or_characteristic
        elif service_or_characteristic_found(RESISTANCE_LEVEL_RANGE_UUID, service_or_characteristic.uuid):
            self.resistance_level_range = service_or_characteristic
        elif service_or_characteristic_found(FTMS_CONTROL_POINT_UUID, service_or_characteristic.uuid):
            self.ftms_control_point = service_or_characteristic
        elif service_or_characteristic_found(INDOOR_BIKE_DATA_UUID, service_or_characteristic.uuid):
            self.indoor_bike_data = service_or_characteristic


    def read_resistance_level_range(self):
        if self.resistance_level_range:
            print("The resistance level range is: {}".format(decode_int_bytes(self.resistance_level_range.read_value())))

    def read_inclination_range(self):
        if self.inclination_range:
            print("The inclination range is: {}".format(decode_int_bytes(self.inclination_range.read_value())))

    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))
        sys.exit()

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))

    def ftms_request_control(self):
        if self.ftms_control_point:
            # request FTMS control
            print("Requesting FTMS control...")
            self.ftms_control_point.write_value(bytearray([FTMS_REQUEST_CONTROL]))
            sleep(WRITEVALUE_WAIT_TIME)

    def ftms_reset_settings(self):
        print("Initiating to reset control settings...")
        if self.ftms_control_point:
            # reset FTMS control settings
            print("Resetting FTMS control settings...")
            self.ftms_control_point.write_value(bytearray([FTMS_RESET]))
            sleep(WRITEVALUE_WAIT_TIME)

            self.resistance = 0
            self.inclination = 0

            # request resistance control
            self.ftms_request_control()
            # reset resistance down to 0%
            self.ftms_set_target_resistance_level(self.resistance)

            # request incline control
            self.custom_control_point_enable_notifications()
            # reset incline to the flat level: 0%
            self.custom_control_point_set_target_inclination(self.inclination)

            self.mqtt_client.publish(self.args.incline_report_topic, self.mqtt_data_report_payload('incline', self.inclination))
            self.mqtt_client.publish(self.args.resistance_report_topic, self.mqtt_data_report_payload('resistance', self.resistance))

    # the resistance value is UINT8 type and unitless with a resolution of 0.1
    def ftms_set_target_resistance_level(self, new_resistance):
        print(f"Trying to set a new resistance value: {new_resistance}")

        if self.ftms_control_point:
            # initiate the action
            self.ftms_control_point.write_value(bytearray([FTMS_SET_TARGET_RESISTANCE_LEVEL, new_resistance]))
            self.new_resistance = new_resistance
            sleep(WRITEVALUE_WAIT_TIME)
            
    def custom_control_point_enable_notifications(self):
        if self.custom_incline_characteristic:
            # has to do this step to be able to send incline value successfully
            print("Enabling notifications for custom incline endpoint...")
            self.custom_incline_characteristic.enable_notifications()
            sleep(WRITEVALUE_WAIT_TIME)

    # the inclination value range is -10 to 19, in Percent with a resolution of 0.5%
    def custom_control_point_set_target_inclination(self, new_inclination):
        print(f"Trying to set a new inclination value: {new_inclination}")

        if self.custom_incline_characteristic:
            # send the new inclination value to the custom characteristic
            print("values are: ", convert_incline_to_op_value(new_inclination))
            self.custom_incline_characteristic.write_value(bytearray([INCLINE_CONTROL_OP_CODE] + convert_incline_to_op_value(new_inclination)))
            #self.custom_incline_characteristic.write_value(bytearray([0x66, 0x6c, 0x07]))
            self.new_inclination = new_inclination
            sleep(WRITEVALUE_WAIT_TIME)

    def set_new_inclination(self):
        self.inclination = self.new_inclination
        self.new_inclination = None
        print(f"A new inclination has been set successfully: {self.inclination}")
        self.mqtt_client.publish(self.args.incline_report_topic, self.mqtt_data_report_payload('incline', self.inclination))

    def set_new_resistance(self):
        self.resistance = self.new_resistance
        self.new_resistance = None
        print(f"A new resistance has been set successfully: {self.resistance}")
        self.mqtt_client.publish(self.args.resistance_report_topic, self.mqtt_data_report_payload('resistance', self.resistance))

    def set_new_inclination_failed(self):
        print(f"The new inclination has not been set successfully: {self.new_inclination}")
        self.new_inclination = None

    def set_new_resistance_failed(self):
        print(f"The new resistance has not been set successfully: {self.new_resistance}")
        self.new_resistance = None

    def descriptor_read_value_failed(self, descriptor, error):
        print('descriptor value read failed:', str(error))

    def characteristic_value_updated(self, characteristic, value):
        print(f"The updated value for {characteristic.uuid} is:", value)

    def characteristic_write_value_succeeded(self, characteristic):
        print(f"A new value has been written to {characteristic.uuid}")

        # set new resistance or inclination and notify to MQTT if the async write value action is succeeded
        if service_or_characteristic_found(FTMS_CONTROL_POINT_UUID, characteristic.uuid):
            if self.new_resistance is not None:
                self.set_new_resistance()
        if service_or_characteristic_found_full_match(INCLINE_CONTROL_CHARACTERISTIC_UUID, characteristic.uuid):
            if self.new_inclination is not None:
                self.set_new_inclination()

    def characteristic_write_value_failed(self, characteristic, error):
        print(f"A new value has not been written to {characteristic.uuid} successfully: {str(error)}")

        # clear the new resistance or inclination and notify to MQTT if the async write value action is failed
        if service_or_characteristic_found(FTMS_CONTROL_POINT_UUID, characteristic.uuid):
            if self.new_resistance is not None:
                self.set_new_resistance_failed()
        if service_or_characteristic_found_full_match(INCLINE_CONTROL_CHARACTERISTIC_UUID, characteristic.uuid):
            if self.new_inclination is not None:
                self.set_new_inclination_failed()

    def characteristic_enable_notification_succeeded(self, characteristic):
        print(f"The {characteristic.uuid} has been enabled with notification!")

    def characteristic_enable_notification_failed(self, characteristic, error):
        print(f"Cannot enable notification for {characteristic.uuid}: {str(error)}")      

    # process the Indoor Bike Data
    def process_indoor_bike_data(self, value):
        flag_instantaneous_speed = not((value[0] & 1) >> 0)
        flag_average_speed = (value[0] & 2) >> 1
        flag_instantaneous_cadence = (value[0] & 4) >> 2
        flag_average_cadence = (value[0] & 8) >> 3
        flag_total_distance = (value[0] & 16) >> 4
        flag_resistance_level = (value[0] & 32) >> 5
        flag_instantaneous_power = (value[0] & 64) >> 6
        flag_average_power = (value[0] & 128) >> 7
        flag_expended_energy = (value[1] & 1) >> 0
        flag_heart_rate = (value[1] & 2) >> 1
        flag_metabolic_equivalent = (value[1] & 4) >> 2
        flag_elapsed_time = (value[1] & 8) >> 3
        flag_remaining_time = (value[1] & 16) >> 4
        offset = 2

        if flag_instantaneous_speed:
            self.instantaneous_speed = float((value[offset+1] << 8) + value[offset]) / 100.0 * 5.0 / 18.0
            offset += 2
            print(f"Instantaneous Speed: {self.instantaneous_speed} m/s")

        if flag_average_speed:
            self.average_speed = float((value[offset+1] << 8) + value[offset]) / 100.0 * 5.0 / 18.0
            offset += 2
            print(f"Average Speed: {self.average_speed} m/s")

        if flag_instantaneous_cadence:
            self.instantaneous_cadence = float((value[offset+1] << 8) + value[offset]) / 10.0
            offset += 2
            print(f"Instantaneous Cadence: {self.instantaneous_cadence} rpm")

        if flag_average_cadence:
            self.average_cadence = float((value[offset+1] << 8) + value[offset]) / 10.0
            offset += 2
            print(f"Average Cadence: {self.average_cadence} rpm")

        if flag_total_distance:
            self.total_distance = int((value[offset+2] << 16) + (value[offset+1] << 8) + value[offset])
            offset += 3
            print(f"Total Distance: {self.total_distance} m")

        if flag_resistance_level:
           self.resistance_level = int((value[offset+1] << 8) + value[offset])
           offset += 2
           print(f"Resistance Level: {self.resistance_level}")

        if flag_instantaneous_power:
            self.instantaneous_power = int((value[offset+1] << 8) + value[offset])
            offset += 2
            print(f"Instantaneous Power: {self.instantaneous_power} W")

        if flag_average_power:
            self.average_power = int((value[offset+1] << 8) + value[offset])
            offset += 2
            print(f"Average Power: {self.average_power} W")

        if flag_expended_energy:
            expended_energy_total = int((value[offset+1] << 8) + value[offset])
            offset += 2
            if expended_energy_total != 0xFFFF:
                self.expended_energy_total = expended_energy_total
                print(f"Expended Energy: {self.expended_energy_total} kCal total")

            expended_energy_per_hour = int((value[offset+1] << 8) + value[offset])
            offset += 2
            if expended_energy_per_hour != 0xFFFF:
                self.expended_energy_per_hour = expended_energy_per_hour
                print(f"Expended Energy: {self.expended_energy_per_hour} kCal/hour")

            expended_energy_per_minute = int(value[offset])
            offset += 1
            if expended_energy_per_minute != 0xFF:
                self.expended_energy_per_minute = expended_energy_per_minute
                print(f"Expended Energy: {self.expended_energy_per_minute} kCal/min")

        if flag_heart_rate:
            self.heart_rate = int(value[offset])
            offset += 1
            print(f"Heart Rate: {self.heart_rate} bpm")

        if flag_metabolic_equivalent:
            self.metabolic_equivalent = float(value[offset]) / 10.0
            offset += 1
            print(f"Metabolic Equivalent: {self.metabolic_equivalent} METS")

        if flag_elapsed_time:
            self.elapsed_time = int((value[offset+1] << 8) + value[offset])
            offset += 2
            print(f"Elapsed Time: {self.elapsed_time} seconds")

        if flag_remaining_time:
            self.remaining_time = int((value[offset+1] << 8) + value[offset])
            offset += 2
            print(f"Remaining Time: {self.remaining_time} seconds")

        if offset != len(value):
            print("ERROR: Payload was not parsed correctly")
            return

        # The KICKR Trainer only reports instantaneous speed, cadence and power
        # Publish them to MQTT topics if they were provided
        if self.zero_count < 10:
            if flag_instantaneous_speed:
                self.mqtt_client.publish(self.args.speed_report_topic, self.mqtt_data_report_payload('speed', self.instantaneous_speed))
            if flag_instantaneous_cadence:
                self.mqtt_client.publish(self.args.cadence_report_topic, self.mqtt_data_report_payload('cadence', self.instantaneous_cadence))
            if flag_instantaneous_power:
                self.mqtt_client.publish(self.args.power_report_topic, self.mqtt_data_report_payload('power', self.instantaneous_power))
                
            if self.instantaneous_speed == 0:
                self.zero_count += 1
                
            print('Zero Count:', self.zero_count)
                
        elif self.zero_count >= 10 and self.instantaneous_speed > 0:
            self.zero_count = 0
            if flag_instantaneous_speed:
                self.mqtt_client.publish(self.args.speed_report_topic, self.mqtt_data_report_payload('speed', self.instantaneous_speed))
            if flag_instantaneous_cadence:
                self.mqtt_client.publish(self.args.cadence_report_topic, self.mqtt_data_report_payload('cadence', self.instantaneous_cadence))
            if flag_instantaneous_power:
                self.mqtt_client.publish(self.args.power_report_topic, self.mqtt_data_report_payload('power', self.instantaneous_power))
        else:
            print('Bike currently idle, no data publish to MQTT')
            
    def mqtt_data_report_payload(self, device_type, value):
        # TODO: add more json data payload whenever needed later
        return json.dumps({"value": value, "unitName": DEVICE_UNIT_NAMES[device_type], "timestamp": time.time(), "metadata": { "deviceName": platform.node() } })

    # this will be called with updates from any characteristics which provide notifications (eg. Indoor Bike Data)
    def characteristic_value_updated(self, characteristic, value):
        if characteristic == self.indoor_bike_data:
            self.process_indoor_bike_data(value)

    # this is the main process that will be run all time after manager.run() is called
    def services_resolved(self):
        super().services_resolved()

        print("[%s] Resolved services" % (self.mac_address))
        for service in self.services:
            print("[%s]\tService [%s]" % (self.mac_address, service.uuid))
            self.set_service_or_characteristic(service)

            for characteristic in service.characteristics:
                print("[%s]\t\tCharacteristic [%s]" % (self.mac_address, characteristic.uuid))
                print("The characteristic value is: ", characteristic.read_value())

                if self.ftms == service:
                    # set for FTMS control point for resistance control
                    self.set_service_or_characteristic(characteristic)
                if self.custom_incline_service == service:
                    # set for custom control point for incline control
                    self.set_service_or_characteristic(characteristic)

        # continue if FTMS service is found from the BLE device
        if self.ftms and self.indoor_bike_data:
            # read the supported resistance and inclination ranges here to set correct command values later
            self.read_resistance_level_range()
            self.read_inclination_range()

            # enable notifications for Indoor Bike Data
            self.indoor_bike_data.enable_notifications()

            # reset control settings while initiating the BLE connection
            self.ftms_reset_settings()

            # start looping MQTT messages
            self.mqtt_client.loop_start()
