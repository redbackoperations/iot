# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2020 Philip Howard, written for Pimoroni Ltd
#
# SPDX-License-Identifier: MIT
"""
`pimoroni_circuitpython_ltr559`
================================================================================

Library for the LTR559 Proximity/Presence/Light Sensor


* Author(s): Philip Howard

Implementation Notes
--------------------

**Hardware:**

Written to support Pimoroni's LTR559 breakout and Enviro+ FeatherWing.

* Pimoroni LTR559 Breakout Garden Breakout:
  https://shop.pimoroni.com/products/ltr-559-light-proximity-sensor-breakout

* Pimoroni Enviro+ FeatherWing:
  https://shop.pimoroni.com/products/enviro-plus-featherwing

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library:
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

* Adafruit's Register library:
  https://github.com/adafruit/Adafruit_CircuitPython_Register
"""
import time
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bits import RWBits, ROBits
from adafruit_register.i2c_bit import RWBit, ROBit
from micropython import const

__version__ = "0.0.1"
__repo__ = "https://github.com/pimoroni/Pimoroni_CircuitPython_LTR559.git"


_LTR559_I2C_ADDR = const(0x23)
_LTR559_PART_ID = const(0x09)
_LTR559_REVISION_ID = const(0x02)

_LTR559_REG_ALS_CONTROL = const(0x80)
_LTR559_REG_PS_CONTROL = const(0x81)
_LTR559_REG_PS_LED = const(0x82)
_LTR559_REG_PS_N_PULSES = const(0x83)
_LTR559_REG_PS_MEAS_RATE = const(0x84)
_LTR559_REG_ALS_MEAS_RATE = const(0x85)
_LTR559_REG_PART_ID = const(0x86)
_LTR559_REG_MANUFACTURER_ID = const(0x87)
_LTR559_REG_ALS_DATA_CH1 = const(0x88)
_LTR559_REG_ALS_DATA_CH0 = const(0x8A)
_LTR559_REG_ALS_PS_STATUS = const(0x8C)
_LTR559_REG_PS_DATA_CH0 = const(0x8D)
_LTR559_REG_PS_DATA_SAT = const(0x8E)
_LTR559_REG_INTERRUPT = const(0x8F)
_LTR559_REG_PS_THRESHOLD_UPPER = const(0x90)
_LTR559_REG_PS_THRESHOLD_LOWER = const(0x92)
_LTR559_REG_PS_OFFSET = const(0x94)
_LTR559_REG_ALS_THRESHOLD_UPPER = const(0x97)
_LTR559_REG_ALS_THRESHOLD_LOWER = const(0x99)
_LTR559_REG_INTERRUPT_PERSIST = const(0x9E)

LTR559_INTERRUPT_MODE_OFF = const(0b00)
LTR559_INTERRUPT_MODE_PS = const(0b01)
LTR559_INTERRUPT_MODE_ALS = const(0b10)

LTR559_LED_FREQ_30KHZ = const(0b000)
LTR559_LED_FREQ_40KHZ = const(0b001)
LTR559_LED_FREQ_50KHZ = const(0b010)
LTR559_LED_FREQ_60KHZ = const(0b011)
LTR559_LED_FREQ_70KHZ = const(0b100)
LTR559_LED_FREQ_80KHZ = const(0b100)
LTR559_LED_FREQ_90KHZ = const(0b110)
LTR559_LED_FREQ_100KHZ = const(0b111)

LTR559_LED_DUTY_25 = const(0b00)
LTR559_LED_DUTY_50 = const(0b01)
LTR559_LED_DUTY_75 = const(0b10)
LTR559_LED_DUTY_100 = const(0b11)

LTR559_LED_CURRENT_5MA = const(0b000)
LTR559_LED_CURRENT_10MA = const(0b001)
LTR559_LED_CURRENT_20MA = const(0b010)
LTR559_LED_CURRENT_50MA = const(0b011)
LTR559_LED_CURRENT_100MA = const(0b100)

LTR559_PS_INTEGRATION_TIME_100MS = const(0b000)
LTR559_PS_INTEGRATION_TIME_50MS = const(0b001)
LTR559_PS_INTEGRATION_TIME_200MS = const(0b010)
LTR559_PS_INTEGRATION_TIME_400MS = const(0b011)
LTR559_PS_INTEGRATION_TIME_150MS = const(0b100)
LTR559_PS_INTEGRATION_TIME_250MS = const(0b101)
LTR559_PS_INTEGRATION_TIME_300MS = const(0b110)
LTR559_PS_INTEGRATION_TIME_350MS = const(0b111)

LTR559_PS_RATE_50MS = const(0b000)
LTR559_PS_RATE_100MS = const(0b001)
LTR559_PS_RATE_200MS = const(0b010)
LTR559_PS_RATE_500MS = const(0b011)
LTR559_PS_RATE_1000MS = const(0b100)
LTR559_PS_RATE_2000MS = const(0b101)

LTR559_ALS_GAIN_1X = const(0b000)
LTR559_ALS_GAIN_2X = const(0b001)
LTR559_ALS_GAIN_4X = const(0b010)
LTR559_ALS_GAIN_8X = const(0b011)
LTR559_ALS_GAIN_48X = const(0b110)
LTR559_ALS_GAIN_96X = const(0b111)

LTR559_ALS_RATE_50MS = const(0b000)
LTR559_ALS_RATE_100MS = const(0b001)
LTR559_ALS_RATE_200MS = const(0b010)
LTR559_ALS_RATE_500MS = const(0b011)
LTR559_ALS_RATE_1000MS = const(0b100)
LTR559_ALS_RATE_2000MS = const(0b101)

LTR559_ALS_INTEGRATION_TIME_100MS = const(0b000)
LTR559_ALS_INTEGRATION_TIME_50MS = const(0b001)
LTR559_ALS_INTEGRATION_TIME_200MS = const(0b010)
LTR559_ALS_INTEGRATION_TIME_400MS = const(0b011)
LTR559_ALS_INTEGRATION_TIME_150MS = const(0b100)
LTR559_ALS_INTEGRATION_TIME_250MS = const(0b101)
LTR559_ALS_INTEGRATION_TIME_300MS = const(0b110)
LTR559_ALS_INTEGRATION_TIME_350MS = const(0b111)


class ALSControl:  # pylint: disable-msg=too-few-public-methods
    """Control registers for the LTR559 light sensor"""

    def __init__(self, i2c):
        self.i2c_device = i2c  # self.i2c_device required by RWBit class

    gain = RWBits(3, _LTR559_REG_ALS_CONTROL, 2)
    mode = RWBit(_LTR559_REG_ALS_CONTROL, 0)
    integration_time_ms = RWBits(3, _LTR559_REG_ALS_MEAS_RATE, 3)
    repeat_rate_ms = RWBits(3, _LTR559_REG_ALS_MEAS_RATE, 0)

    data = ROBits(32, _LTR559_REG_ALS_DATA_CH1, 0, register_width=4)

    threshold_lower = RWBits(16, _LTR559_REG_ALS_THRESHOLD_LOWER, 0, register_width=2)
    threshold_upper = RWBits(16, _LTR559_REG_ALS_THRESHOLD_UPPER, 0, register_width=2)

    interrupt_persist = RWBits(4, _LTR559_REG_INTERRUPT_PERSIST, 4)

    data_valid = ROBit(_LTR559_REG_ALS_PS_STATUS, 7)
    data_gain = ROBits(3, _LTR559_REG_ALS_PS_STATUS, 4)

    new_data = ROBit(_LTR559_REG_ALS_PS_STATUS, 2)
    interrupt_active = ROBit(_LTR559_REG_ALS_PS_STATUS, 3)


class PSControl:  # pylint: disable-msg=too-few-public-methods
    """Control registers for the LTR559 proximity sensor"""

    def __init__(self, i2c):
        self.i2c_device = i2c  # self.i2c_device required by RWBit class

    saturation_indicator_enable = RWBit(_LTR559_REG_PS_CONTROL, 5)
    active = RWBits(2, _LTR559_REG_PS_CONTROL, 0)
    rate_ms = RWBits(4, _LTR559_REG_PS_MEAS_RATE, 0)

    data_ch0 = ROBits(16, _LTR559_REG_PS_DATA_CH0, 0, register_width=2)
    saturation = RWBit(_LTR559_REG_PS_DATA_SAT, 7)

    threshold_lower = RWBits(16, _LTR559_REG_PS_THRESHOLD_LOWER, 0, register_width=2)
    threshold_upper = RWBits(16, _LTR559_REG_PS_THRESHOLD_UPPER, 0, register_width=2)

    offset = RWBits(10, _LTR559_REG_PS_OFFSET, 0, register_width=2)

    interrupt_persist = RWBits(4, _LTR559_REG_INTERRUPT_PERSIST, 0)

    new_data = ROBit(_LTR559_REG_ALS_PS_STATUS, 0)
    interrupt_active = ROBit(_LTR559_REG_ALS_PS_STATUS, 1)


class DeviceControl:  # pylint: disable-msg=too-few-public-methods
    """General LTR559 control registers"""

    def __init__(self, i2c):
        self.i2c_device = i2c  # self.i2c_device required by RWBit class

    sw_reset = RWBit(_LTR559_REG_ALS_CONTROL, 1)
    part_number = ROBits(4, _LTR559_REG_PART_ID, 4)
    revision = ROBits(4, _LTR559_REG_PART_ID, 0)
    manufacturer_id = ROBits(8, _LTR559_REG_MANUFACTURER_ID, 0)

    led_pulse_freq_khz = RWBits(3, _LTR559_REG_PS_LED, 5)
    led_duty_cycle = RWBits(2, _LTR559_REG_PS_LED, 3)
    led_current_ma = RWBits(3, _LTR559_REG_PS_LED, 0)
    led_pulse_count = RWBits(4, _LTR559_REG_PS_N_PULSES, 0)

    interrupt_polarity = RWBit(_LTR559_REG_INTERRUPT, 2)
    interrupt_mode = RWBits(2, _LTR559_REG_INTERRUPT, 0)


class Pimoroni_LTR559:  # pylint: disable-msg=too-many-instance-attributes
    """
    A driver for the LTR559 Proximity/Distance/Light sensor.
    """

    def __init__(
        self,
        i2c,
        address=_LTR559_I2C_ADDR,
        enable_interrupts=False,
        interrupt_pin_polarity=1,
        timeout=5,
    ):  # pylint: disable-msg=too-many-arguments
        """Initialize the sensor."""
        self._device = I2CDevice(i2c, address)
        self.settings = DeviceControl(self._device)
        self.light = ALSControl(self._device)
        self.proximity = PSControl(self._device)

        self._als0 = 0
        self._als1 = 0
        self._ps0 = 0
        self._lux = 0
        self._ratio = 100

        self._gain = 4
        self._integration_time = 50

        self._lookup_light_gain = {
            0b000: 1,
            0b001: 2,
            0b010: 4,
            0b011: 8,
            0b110: 48,
            0b111: 96,
        }
        self._lookup_light_integration_time = {
            0b000: 100,
            0b001: 50,
            0b010: 200,
            0b011: 400,
            0b100: 150,
            0b101: 250,
            0b110: 300,
            0b111: 350,
        }

        self._ch0_c = (17743, 42785, 5926, 0)
        self._ch1_c = (-11059, 19548, -1185, 0)

        if (self.settings.part_number, self.settings.revision) != (
            _LTR559_PART_ID,
            _LTR559_REVISION_ID,
        ):
            raise RuntimeError("LTR559 not found")

        self.settings.sw_reset = 1

        t_start = time.monotonic()
        while time.monotonic() - t_start < timeout:
            if self.settings.sw_reset == 0:
                break
            time.sleep(0.05)

        if self.settings.sw_reset:
            raise RuntimeError("Timeout waiting for software reset.")

        # Interrupt register must be set before device is switched to active mode
        # see datasheet page 12/40, note #2
        if enable_interrupts:
            self.settings.interrupt_mode = (
                LTR559_INTERRUPT_MODE_PS | LTR559_INTERRUPT_MODE_ALS
            )
            self.settings.interrupt_polarity = interrupt_pin_polarity

        # No need to run the proximity LED at 100mA, so we pick 50 instead.
        # Tests suggest this works pretty well.
        self.settings.led_current_ma = LTR559_LED_CURRENT_50MA
        self.settings.led_duty_cycle = LTR559_LED_DUTY_100
        self.settings.led_pulse_freq_khz = LTR559_LED_FREQ_30KHZ

        # 1 pulse is the default value
        self.settings.led_pulse_count = 1

        self.proximity.active = 0b11
        self.proximity.saturation_indicator_enable = 1
        self.proximity.rate_ms = LTR559_PS_RATE_50MS

        self.light.repeat_rate_ms = LTR559_ALS_RATE_50MS
        self.light.integration_time_ms = LTR559_ALS_INTEGRATION_TIME_50MS

        self.light.threshold_lower = 0x0000
        self.light.threshold_upper = 0xFFFF

        self.light.mode = 1
        self.light.gain = LTR559_ALS_GAIN_4X

        self.proximity.threshold_lower = 0x0000
        self.proximity.threshold_upper = 0xFFFF

        self.proximity.offset = 0

    @property
    def lux(self):
        """The light sensor lux value.

        Updates the sensor if new data is available or the interrupt has fired.

        """
        self.update_sensor()
        return self._lux

    @property
    def prox(self):
        """The proximity sensor value.

        Updates the sensor if new data is available or the interrupt has fired.

        """
        self.update_sensor()
        return self._ps0

    def get_lux(self):
        """Get the light sensor lux value."""
        return self.lux

    def get_proximity(self):
        """Get the proximity sensor value."""
        return self.prox

    def update_sensor(self):
        """Updates the sensor.

        Calculates and store lux and proximity values if new data is available.

        """
        als_int = self.light.new_data or self.light.interrupt_active
        ps_int = self.proximity.new_data or self.proximity.interrupt_active

        if ps_int:
            self._ps0 = self.proximity.data_ch0

        if als_int:
            als_data = self.light.data
            self._als0 = (als_data >> 16) & 0xFFFF
            self._als1 = als_data & 0xFFFF

            self._ratio = (
                self._als1 * 100 / (self._als1 + self._als0)
                if self._als0 + self._als1 > 0
                else 101
            )

            if self._ratio < 45:
                ch_idx = 0
            elif self._ratio < 64:
                ch_idx = 1
            elif self._ratio < 85:
                ch_idx = 2
            else:
                ch_idx = 3

            gain = self._lookup_light_gain[self.light.data_gain]
            integration_time = self._lookup_light_integration_time[
                self.light.integration_time_ms
            ]

            self._gain = gain
            self._integration_time = integration_time

            try:
                self._lux = (self._als0 * self._ch0_c[ch_idx]) - (
                    self._als1 * self._ch1_c[ch_idx]
                )
                self._lux /= integration_time / 100.0
                self._lux /= gain
                self._lux /= 10000.0
            except ZeroDivisionError:
                self._lux = 0
