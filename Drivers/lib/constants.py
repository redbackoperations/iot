##### Section 1: MQTT Topics #####
BIKE_01_INCLINE_COMMAND = 'bike/000001/incline'
BIKE_01_RESISTANCE_COMMAND = 'bike/000001/resistance'
BIKE_01_INCLINE_REPORT = 'bike/000001/incline/report'
BIKE_01_RESISTANCE_REPORT = 'bike/000001/resistance/report'
BIKE_01_SPEED_REPORT = 'bike/000001/speed'
BIKE_01_CADENCE_REPORT = 'bike/000001/cadence'
BIKE_01_POWER_REPORT = 'bike/000001/power'

BIKE_02_INCLINE_COMMAND = 'bike/000002/incline'
BIKE_02_RESISTANCE_COMMAND = 'bike/000002/resistance'
BIKE_02_INCLINE_REPORT = 'bike/000002/incline/report'
BIKE_02_RESISTANCE_REPORT = 'bike/000002/resistance/report'
BIKE_02_SPEED_REPORT = 'bike/000002/speed'
BIKE_02_CADENCE_REPORT = 'bike/000002/cadence'
BIKE_02_POWER_REPORT = 'bike/000002/power'

##### Section 2: BLE devices reserved UUIDs #####
# More BLE specification details can be found at: https://www.bluetooth.com/specifications/specs/fitness-machine-service-1-0 and https://github.com/oesmith/gatt-xml

# Fitness Machine Service (FTMS)
FTMS_UUID = 0x1826
# Characteristics
TREADMILL_DATA_UUID = 0X2ACD
STEP_CLIMBER_DATA_UUID = 0X2ACF
CROSS_TRAINER_DATA_UUID = 0X2ACE
ROWER_DATA_UUID = 0X2AD1
INDOOR_BIKE_DATA_UUID = 0X2AD2
FITNESS_MACHINE_FEATURES_UUID = 0X2ACC
RESISTANCE_LEVEL_RANGE_UUID = 0X2AD6
POWER_RANGE_UUID = 0X2AD8
INCLINATION_RANGE_UUID = 0X2AD5
HEART_RATE_RANGE_UUID = 0X2AD7
FTMS_CONTROL_POINT_UUID = 0X2AD9
FITNESS_MACHINE_STATUS_UUID = 0X2ADA

# Device Information Service (DIS)
DIS_UUID = 0x180A
# Characteristics
MANUFACTURER_NAME_STRING_UUID = 0X2A29
MODEL_NUMBER_STRING_UUID = 0X2A24
FIRMWARE_REVISION_STRING_UUID = 0X2A26
SOFTWARE_REVISION_STRING_UUID = 0X2A28
HARDWARE_REVISION_UUID = 0X2A27 # only present if a value was set on the fitness equipment

# Heart Rate Service (HRS) – only present if HR pairing is enabled
HRS_UUID = 0x180D
# Characteristics
HEART_RATE_MEASUREMENT_UUID = 0X2A37

# Fitness Machine Control Point Op Codes (more details in https://www.bluetooth.com/specifications/specs/fitness-machine-service-1-0)
FTMS_REQUEST_CONTROL = 0x00
FTMS_RESET = 0x01
FTMS_SET_TARGET_SPEED = 0x02
FTMS_SET_TARGET_INCLINATION = 0x03
FTMS_SET_TARGET_RESISTANCE_LEVEL = 0x04
FTMS_SET_TARGET_POWER = 0x05
FTMS_SET_TARGET_HEART_RATE = 0x06
FTMS_START_OR_RESUME = 0x07
FTMS_STOP_OR_PAUSE = 0x08
FTMS_SET_TARGETED_EXPENDED_ENERGY = 0x09
FTMS_SET_TARGETED_NUMBER_OF_STEPS = 0x0A
FTMS_SET_TARGETED_NUMBER_OF_STRIDES = 0x0B
FTMS_SET_TARGETED_DISTANCE = 0x0C
FTMS_SET_TARGETED_TRAINING_TIME = 0x0D
FTMS_SET_TARGETED_TIME_IN_TWO_HEART_RATE_ZONES = 0x0E
FTMS_SET_TARGETED_TIME_IN_THREE_HEART_RATE_ZONES = 0x0F
FTMS_SET_TARGETED_TIME_IN_FIVE_HEART_RATE_ZONES = 0x10
FTMS_SET_INDOOR_BIKE_SIMULATION_PARAMETERS = 0x11
FTMS_SET_WHEEL_CIRCUMFERENCE = 0x12
FTMS_SPIN_DOWN_CONTROL = 0x13
FTMS_SET_TARGETED_CADENCE = 0x14
FTMS_RESPONSE_CODE = 0x80

# Incline Control's Custom Service and Characteristic (found from a BLE sniffer, not mentioned anywhere online)
INCLINE_CONTROL_SERVICE_UUID = "a026ee0b0a7d4ab397faf1500f9feb8b"
INCLINE_CONTROL_CHARACTERISTIC_UUID = "a026e0370a7d4ab397faf1500f9feb8b"

# Incline Control Op Values
INCLINE_REQUEST_CONTROL = 0x67
INCLINE_CONTROL_OP_CODE = 0x66
INCLINE_CONTROL_MAX_PART_1 = 0x6c # '0x666c07' is 19% incline
INCLINE_CONTROL_MAX_PART_2 = 0x07 
INCLINE_CONTROL_FLAT = 0x00 # '0x660000' is 0% incline
INCLINE_CONTROL_MIN_PART_1 = 0x19 # '0x6619fc' is -10% incline
INCLINE_CONTROL_MIN_PART_2 = 0xfc
INCLINE_CONTROL_INCREMENT_UNIT = 50 # the incline value is up or down by 50 unit each time

##### Section 3: Wahoo Device Mac Addresses #####
BIKE_01_KICKR_TRAINER_ADDRESS = "d9:07:e8:1c:db:94"
BIKE_01_KICKR_CLIMB_ADDRESS = "cf:5c:f0:0d:c7:68"
BIKE_01_HEADWIND_ADDRESS = "ed:cb:f5:da:d3:f5"

##### Section 4: Other Constants #####
# TODO: set the correct resistance and inclination range values once we've got the real Wahoo device data
RESISTANCE_MIN = 0
RESISTANCE_MAX = 100 # 100% resistance

INCLINE_MIN = -10 # -10% incline down
INCLINE_FLAT = 0 # 0% incline flat
INCLINE_MAX = 19 # 19% incline up

MIN_BYTE_VALUE = 0
MAX_BYTE_VALUE = 256

DEVICE_UNIT_NAMES = {
  "speed": "m/s",
  "cadence": "RPM",
  "power": "W",
  "heartRate": "BPM",
  "resistance": "percentage",
  "incline": "degree",
  "headWind": "percentage"
}
