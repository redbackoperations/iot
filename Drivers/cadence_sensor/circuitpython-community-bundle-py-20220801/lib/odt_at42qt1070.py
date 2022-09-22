# AT42QT1070 capacitive touch breakout driver.
# Author: Seth Kerr
# License: MIT License (https://opensource.org/licenses/MIT)

"""
`odt_at42qt1070`
====================================================
CircuitPython driver for the AT42QT1070 capacitive touch acorn.
See usage in the examples/simpletest.py file.
* Author(s): Seth Kerr
Implementation Notes
--------------------
**Hardware:**
* Oak Dev Tech `7-Key Capacitive Touch Sensor Breakout - AT42QT1070
  <>`
**Software and Dependencies:**
* Adafruit CircuitPython firmware for the ESP8622 and M0-based boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

import time

import adafruit_bus_device.i2c_device as i2c_device
from micropython import const

__version__ = "v1.0.6"
__repo__ = "https://github.com/skerr92/at42qt-acorn-python.git"

# Register addresses.  Unused registers commented out to save memory.
AT42QT1070_I2CADDR_DEFAULT = const(0x1B)
AT42QT107_CHIP_ID = (0x00)  # Chip ID should be 0x2F
AT42QT107_FIRMWARE = (0x01) # get firmware version number
AT42QT107_DETECT_STATUS = (0x02)
# BIT 7 (CALIBRATE) | BIT6 (OVERFLOW) | - | - | - | - | - | TOUCH

AT42QT107_KEY_STATUS = (0x03) # BIT 7 Reserved BIT 6 (KEY 6) | ... | ... | BIT 0 (Key 0)
AT42QT107_KEY_0_1 = (0x04) # Most Significant byte
AT42QT107_KEY_0_2 = (0x05) # Least Significant byte
AT42QT107_KEY_1_1 = (0x06) # MSByte
AT42QT107_KEY_1_2 = (0x07) # LSByte
AT42QT107_KEY_2_1 = (0x08)
AT42QT107_KEY_2_2 = (0x09)
AT42QT107_KEY_3_1 = (0x0A)
AT42QT107_KEY_3_2 = (0x0B)
AT42QT107_KEY_4_1 = (0x0C)
AT42QT107_KEY_4_2 = (0x0D)
AT42QT107_KEY_5_1 = (0x0E)
AT42QT107_KEY_5_2 = (0x0F)
AT42QT107_KEY_6_1 = (0x10)
AT42QT107_KEY_6_2 = (0x11)

AT42QT107_REF_DATA_0_1 = (0x12) # MSByte
AT42QT107_REF_DATA_0_2 = (0x13) # LSByte
AT42QT107_REF_DATA_1_1 = (0x14)
AT42QT107_REF_DATA_1_2 = (0x15)
AT42QT107_REF_DATA_2_1 = (0x16)
AT42QT107_REF_DATA_2_2 = (0x17)
AT42QT107_REF_DATA_3_1 = (0x18)
AT42QT107_REF_DATA_3_2 = (0x19)
AT42QT107_REF_DATA_4_1 = (0x1A)
AT42QT107_REF_DATA_4_2 = (0x1B)
AT42QT107_REF_DATA_5_1 = (0x1C)
AT42QT107_REF_DATA_5_2 = (0x1D)
AT42QT107_REF_DATA_6_1 = (0x1E)
AT42QT107_REF_DATA_6_2 = (0x1F)

AT42QT107_NTHR_K0 = (0x20) # negative threshold value.
AT42QT107_NTHR_K1 = (0x21) # Do not set this value to 0
AT42QT107_NTHR_K2 = (0x22) # 0 will cause the key to go into detection
AT42QT107_NTHR_K3 = (0x23)
AT42QT107_NTHR_K4 = (0x24)
AT42QT107_NTHR_K5 = (0x25)
AT42QT107_NTHR_K6 = (0x26)

AT42QT107_AVE_KS_K0 = (0x27) # BIT 7 - BIT 3: Average factoring
AT42QT107_AVE_KS_K1 = (0x28) # BIT 2 - BIT 0: Adjacent Key Supression
AT42QT107_AVE_KS_K2 = (0x29) # AVE values set ADC Sample Number
AT42QT107_AVE_KS_K3 = (0x2A) # AVE can be: 1, 2, 4, 8, 16, 32 ONLY, Default of 8.
AT42QT107_AVE_KS_K4 = (0x2B) # AKS bits can have a value between 0 and 3
AT42QT107_AVE_KS_K5 = (0x2C) # AKS value of 0 means key is not part of a
AT42QT107_AVE_KS_K6 = (0x2D) # AKS group. Default AVE/AKS value 0x01

AT42QT107_DI_K0 = (0x2E) # Detection integrator
AT42QT107_DI_K1 = (0x2F) # 8 bit value controls the number of consecutive
AT42QT107_DI_K2 = (0x30) # measurements that must be confirmed to having
AT42QT107_DI_K3 = (0x31) # passed the key threshold for a key being registered
AT42QT107_DI_K4 = (0x32) # as a detect.
AT42QT107_DI_K5 = (0x33) # Minimum value for DI filter is 2
AT42QT107_DI_K6 = (0x34) # Default of 4
AT42QT107_FO_MO_GA = (0x35) # FastOutDI/ Max Cal/ Guard Channel
# Fast Out DI (FO Mode) - BIT 5 is set, filters with integrator of 4.
# MAX CAL: if cleared, all keys recalibrated after Max On Duration timeout
# GUARD CHANNEL: bits 0-3 are used to set a key as the guard channel. Valid
# values 0-6, with any larger value disabling the guard key feature.

AT42QT107_CAL = (0x38) # Calibrate by writing any value not equal to zero
AT42QT107_RESET = (0x39) # active low reset, write any nonzero value to reset

AT42QT107_LP = (0x36) # lower power mode
# 8 bit value, 0 = 8ms between samples
# 1 = 8ms | 2 = 16ms | 3 = 24ms | 4 = 32 | 254 = 2.032s | 255 = 2.040s
# Default value: 2 (16ms)

AT42QT107_MAX_ON_DUR = (0x37) # maximum on duration

# 8 bit value to determine how long any key can be in touch before it
# recalibrates itself 0 = off | 1 = 160ms | 2 = 320ms | 3 = 480ms | 4 = 640ms
# | 255 = 40.8s Default value: 180(160ms*180 = 28.8s)



class AT42QT1070:
    """Driver for the AT42QT1070 capacitive touch breakout board."""

    def __init__(self, i2c, address=AT42QT1070_I2CADDR_DEFAULT):
        self._i2c = i2c_device.I2CDevice(i2c, address)
        self._buffer = bytearray(2)
        self.reset()

    def _write_register_byte(self, register, value):
        # Write a byte value to the specifier register address.
        with self._i2c:
            self._i2c.write(bytes([register, value]))

    def _read_register_bytes(self, register, result, length=None):
        # Read the specified register address and fill the specified result byte
        # array with result bytes.
        if length is None:
            length = len(result)
        with self._i2c:
            self._i2c.write_then_readinto(bytes([register]), result, in_end=length)

    def reset(self):
        """Reset the AT42QT1070 into a default state ready to detect touch inputs.
        """
        # Write to the reset register.
        self._write_register_byte(AT42QT107_RESET, 0x01)
        time.sleep(
            1
        )  # This 1ms delay here probably isn't necessary but can't hurt.
        # Set calibrate device.
        self._write_register_byte(AT42QT107_CAL, 0x01)

    def touched(self):
        """Return touch state of all pins as a 12-bit value where each bit
        represents a pin, with a value of 1 being touched and 0 not being touched.
        """
        self._read_register_bytes(AT42QT107_DETECT_STATUS, self._buffer)
        return self._buffer[0] & 0xf

    def this_key_touched(self, this_key):
        """ Return buffer containing values of key touch status. values 0-127
        bit 7 is reserved.
        """
        self._read_register_bytes(AT42QT107_KEY_STATUS, self._buffer)
        return self._buffer[this_key] & 0xf

    def set_lowpower(self, value):
        """Write to the Low Power Mode Register
        """
        try:
            if value < 0:
                raise ValueError
            
        except ValueError:
            print('low power value should be between 0 and 255')
        self._write_register_byte(AT42QT107_LP, value)

    def set_all_neg_threshold(self, neg_val):
        """Write to negative threshold register
        """
        try:
            if neg_val <= 0:
                raise ValueError

        except ValueError:
            print('negative threshold value should be greater than 0 and non-negative')
        self._write_register_byte(AT42QT107_NTHR_K0, neg_val)
        self._write_register_byte(AT42QT107_NTHR_K1, neg_val)
        self._write_register_byte(AT42QT107_NTHR_K2, neg_val)
        self._write_register_byte(AT42QT107_NTHR_K3, neg_val)
        self._write_register_byte(AT42QT107_NTHR_K4, neg_val)
        self._write_register_byte(AT42QT107_NTHR_K5, neg_val)
        self._write_register_byte(AT42QT107_NTHR_K6, neg_val)

    def set_key_neg_threshold(self, key, neg_val):
        """Write the negative threshold value for a specific key 0-6
        """
        try:
            if key < 0 or key > 6:
                raise ValueError 

        except ValueError:
            print('Key should be from 0 to 6 only')

        try:
            if neg_val <= 0:
                raise ValueError

        except ValueError:
            print('negative threshold value should be greater than 0 and non-negative')

        if key == 0:
            self._write_register_byte(AT42QT107_NTHR_K0, neg_val)
        if key == 1:
            self._write_register_byte(AT42QT107_NTHR_K1, neg_val)
        if key == 2:
            self._write_register_byte(AT42QT107_NTHR_K2, neg_val)
        if key == 3:
            self._write_register_byte(AT42QT107_NTHR_K3, neg_val)
        if key == 4:
            self._write_register_byte(AT42QT107_NTHR_K4, neg_val)
        if key == 5:
            self._write_register_byte(AT42QT107_NTHR_K5, neg_val)
        if key == 6:
            self._write_register_byte(AT42QT107_NTHR_K6, neg_val)
