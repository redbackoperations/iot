import re
import os
import sys
import gatt
from time import sleep
from mqtt_custom_client import MQTTClientWithSendingFTMSCommands
 
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from lib.ble_helper import service_or_characteristic_found, decode_int_bytes, covert_negative_value_to_valid_bytes
from lib.constants import FTMS_UUID, RESISTANCE_LEVEL_RANGE_UUID, INCLINATION_RANGE_UUID, FTMS_CONTROL_POINT_UUID, FTMS_REQUEST_CONTROL, FTMS_RESET, FTMS_SET_TARGET_INCLINATION, FTMS_SET_TARGET_RESISTANCE_LEVEL

# a sleep time to wait for a characteristic.writevalue() action to be completed
WRITEVALUE_WAIT_TIME = 0.3 # TODO: If this doesn't work well, it needs to change this short sleep mechainism to a async process mechainism for sending consequetive BLE commands (eg., threading control)

class WahooDevice(gatt.Device):
    def __init__(self, mac_address, manager, args, managed=True):
        super().__init__(mac_address, manager, managed)

        # define the initial FTMS Service and the corresponding Characteristics
        self.ftms = None
        self.inclination_range = None
        self.resistance_level_range = None
        self.ftms_control_point = None
        
        # define the initial resistance and inclination values
        self.resistance = 0
        self.inclination = 0
        self.new_resistance = None
        self.new_inclination = None
        
        # CLI parser arguments 
        self.args = args
        
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
        elif service_or_characteristic_found(INCLINATION_RANGE_UUID, service_or_characteristic.uuid):
            self.inclination_range = service_or_characteristic 
        elif service_or_characteristic_found(RESISTANCE_LEVEL_RANGE_UUID, service_or_characteristic.uuid):
            self.resistance_level_range = service_or_characteristic 
        elif service_or_characteristic_found(FTMS_CONTROL_POINT_UUID, service_or_characteristic.uuid):
            self.ftms_control_point = service_or_characteristic
    
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
            self.mqtt_client.publish(self.args.incline_report_topic, self.inclination)
            self.mqtt_client.publish(self.args.resistance_report_topic, self.resistance)

    # the resistance value is UINT8 type and unitless with a resolution of 0.1
    def ftms_set_target_resistance_level(self, new_resistance):
        print(f"Trying to set a new resistance value: {new_resistance}")

        # always request control first
        self.ftms_request_control()
        
        if self.ftms_control_point:
            # initiate the action
            self.ftms_control_point.write_value(bytearray([FTMS_SET_TARGET_RESISTANCE_LEVEL]))
            sleep(WRITEVALUE_WAIT_TIME)
            
            # then send the new resistance value
            self.ftms_control_point.write_value(bytearray([new_resistance]))
            self.new_resistance = new_resistance
            sleep(WRITEVALUE_WAIT_TIME)
            
    # the inclination value is SINT16, in Percent with a resolution of 0.1 %
    def ftms_set_target_inclination(self, new_inclination):
        print(f"Trying to set a new inclination value: {new_inclination}")
        
        # always request control first
        self.ftms_request_control()
        
        if self.ftms_control_point:
            # convert negative int to valid bytes
            bytes_value = bytearray([new_inclination]) if new_inclination >=0 else bytearray(covert_negative_value_to_valid_bytes(new_inclination))
            
            # initiate the action
            self.ftms_control_point.write_value(bytearray([FTMS_SET_TARGET_INCLINATION]))
            sleep(WRITEVALUE_WAIT_TIME)
            
            # then send the new inclination value
            self.ftms_control_point.write_value(bytes_value)
            self.new_inclination = new_inclination
            sleep(WRITEVALUE_WAIT_TIME)
            
    def set_new_inclication(self):
        self.inclination = self.new_inclination
        self.new_inclination = None
        print(f"A new inclination has been set successfully: {self.inclination}") 
        self.mqtt_client.publish(self.args.incline_report_topic, self.inclination)
        
    def set_new_resistance(self):
        self.resistance = self.new_resistance
        self.new_resistance = None
        print(f"A new resistance has been set successfully: {self.resistance}")
        self.mqtt_client.publish(self.args.resistance_report_topic, self.resistance)

    def set_new_inclication_failed(self):
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
        
        # set new resistance or inclication and notify to MQTT if the async write value action is succeeded
        if service_or_characteristic_found(FTMS_CONTROL_POINT_UUID, characteristic.uuid):
            if self.new_resistance is not None:
                self.set_new_resistance()
            elif self.new_inclination is not None:
                self.set_new_inclication()

    def characteristic_write_value_failed(self, characteristic, error):
        print(f"A new value has not been written to {characteristic.uuid} successfully: {str(error)}")
        
        # clear the new resistance or inclication and notify to MQTT if the async write value action is failed
        if service_or_characteristic_found(FTMS_CONTROL_POINT_UUID, characteristic.uuid):
            if self.new_resistance is not None:
                self.set_new_resistance_failed()
            elif self.new_inclination is not None:
                self.set_new_inclication_failed()
    
                
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
                    self.set_service_or_characteristic(characteristic)

        # continue if FTMS service is found from the BLE device
        if self.ftms:
            # read the supported resistance and incliation ranges here to set correct command values later
            self.read_resistance_level_range()
            self.read_inclination_range()

            # reset control settings while initiating the BLE connection
            self.ftms_reset_settings()
            
            # start looping MQTT messages
            self.mqtt_client.loop_start()
