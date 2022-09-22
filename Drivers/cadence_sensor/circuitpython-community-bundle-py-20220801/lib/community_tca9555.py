# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 James Carr
#
# SPDX-License-Identifier: MIT

"""
`community_tca9555`
================================================================================

CircuitPython library for connecting a TCA9555 16-Bit I2C GPIO expander
Library for TCA9555 Low-Voltage 16-Bit I2C and SMBus I/O Expander with Interrupt Output
and Configuration Registers


* Author(s): James Carr

Implementation Notes
--------------------

**Hardware:**

* `Pimoroni Pico RGB Keybad Base <https://shop.pimoroni.com/products/pico-rgb-keypad-base>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
    https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

__version__ = "0.2.2"
__repo__ = "https://github.com/lesamouraipourpre/Community_CircuitPython_TCA9555.git"


import busio
from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bit import ROBit, RWBit
from adafruit_register.i2c_bits import ROBits, RWBits


ADDRESS_MINIMUM = const(0x20)
"""The minimum I2C address the TCA9555 supports"""
ADDRESS_MAXIMUM = const(0x27)
"""The maximum I2C address the TCA9555 supports"""

INPUT_PORT_0 = const(0x00)
INPUT_PORT_1 = const(0x01)
OUTPUT_PORT_0 = const(0x02)
OUTPUT_PORT_1 = const(0x03)
POLARITY_INVERSION_PORT_0 = const(0x04)
POLARITY_INVERSION_PORT_1 = const(0x05)
CONFIGURATION_PORT_0 = const(0x06)
CONFIGURATION_PORT_1 = const(0x07)


class TCA9555:
    # pylint: disable=too-few-public-methods
    """CircuitPython driver for the Texas Instruments TCA9555 expander."""

    def __init__(self, i2c: busio.I2C, address: int = ADDRESS_MINIMUM):
        """
        :param busio.I2C i2c: the I2C bus object to use. *Note:* This will
            be converted to an `adafruit_bus_device.i2c_device.I2CDevice`
            internally.
        :param int address: The I2C address of the TCA9555. This must be in
            the range `ADDRESS_MINIMUM` to `ADDRESS_MAXIMUM`. (Defaults to
            `ADDRESS_MINIMUM`)
        """
        if not ADDRESS_MINIMUM <= address <= ADDRESS_MAXIMUM:
            raise ValueError(
                "Address '{}' is not in the allowed range: {}-{}".format(
                    address, ADDRESS_MINIMUM, ADDRESS_MAXIMUM
                )
            )

        # This MUST be named i2c_device for register to work
        self.i2c_device = I2CDevice(i2c, address)

    input_ports = ROBits(16, INPUT_PORT_0, 0, register_width=2)
    """
    Read all 16 bits from port 0 and 1.
    The Input Port registers reflect the incoming logic levels of the pins,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_ports`.
    """

    input_port_0 = ROBits(8, INPUT_PORT_0, 0)
    """
    Read all 8 bits from port 0.
    The Input Port register reflect the incoming logic levels of the pins,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_0`.
    """

    input_port_0_pin_0 = ROBit(INPUT_PORT_0, 0)
    """
    Read the state of port 0 pin 0.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_0_pin_0`.
    """

    input_port_0_pin_1 = ROBit(INPUT_PORT_0, 1)
    """
    Read the state of port 0 pin 1.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_0_pin_1`.
    """

    input_port_0_pin_2 = ROBit(INPUT_PORT_0, 2)
    """
    Read the state of port 0 pin 2.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_0_pin_2`.
    """

    input_port_0_pin_3 = ROBit(INPUT_PORT_0, 3)
    """
    Read the state of port 0 pin 3.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_0_pin_3`.
    """

    input_port_0_pin_4 = ROBit(INPUT_PORT_0, 4)
    """
    Read the state of port 0 pin 4.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_0_pin_4`.
    """

    input_port_0_pin_5 = ROBit(INPUT_PORT_0, 5)
    """
    Read the state of port 0 pin 5.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_0_pin_5`.
    """

    input_port_0_pin_6 = ROBit(INPUT_PORT_0, 6)
    """
    Read the state of port 0 pin 6.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_0_pin_6`.
    """

    input_port_0_pin_7 = ROBit(INPUT_PORT_0, 7)
    """
    Read the state of port 0 pin 7.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_0_pin_7`.
    """

    input_port_1 = ROBits(8, INPUT_PORT_1, 0)
    """
    Read all 8 bits from port 1.
    The Input Port register reflect the incoming logic levels of the pins,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_1`.
    """

    input_port_1_pin_0 = ROBit(INPUT_PORT_1, 0)
    """
    Read the state of port 1 pin 0.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_1_pin_0`.
    """

    input_port_1_pin_1 = ROBit(INPUT_PORT_1, 1)
    """
    Read the state of port 1 pin 1.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_1_pin_1`.
    """

    input_port_1_pin_2 = ROBit(INPUT_PORT_1, 2)
    """
    Read the state of port 1 pin 2.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_1_pin_2`.
    """

    input_port_1_pin_3 = ROBit(INPUT_PORT_1, 3)
    """
    Read the state of port 1 pin 3.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_1_pin_3`.
    """

    input_port_1_pin_4 = ROBit(INPUT_PORT_1, 4)
    """
    Read the state of port 1 pin 4.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_1_pin_4`.
    """

    input_port_1_pin_5 = ROBit(INPUT_PORT_1, 5)
    """
    Read the state of port 1 pin 5.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_1_pin_5`.
    """

    input_port_1_pin_6 = ROBit(INPUT_PORT_1, 6)
    """
    Read the state of port 1 pin 6.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_1_pin_6`.
    """

    input_port_1_pin_7 = ROBit(INPUT_PORT_1, 7)
    """
    Read the state of port 1 pin 7.
    The Input Port register reflect the incoming logic level of the pin,
    regardless of whether the pin is defined as an input or an output by the
    Configuration register :py:attr:`configuration_port_1_pin_7`.
    """

    output_ports = RWBits(16, OUTPUT_PORT_0, 0, register_width=2)
    """
    Write 16 bits of state to the outputs. This will only apply to pins that
    are configured as outputs.
    """

    output_port_0 = RWBits(8, OUTPUT_PORT_0, 0)
    """
    Write 8 bits of state to port 0. This will only apply to pins that are
    configured as outputs.
    """

    output_port_0_pin_0 = RWBit(OUTPUT_PORT_0, 0)
    """
    Write boolean state to port 0 pin 0. This will only apply if the pin is
    configured as an output.
    """

    output_port_0_pin_1 = RWBit(OUTPUT_PORT_0, 1)
    """
    Write boolean state to port 0 pin 1. This will only apply if the pin is
    configured as an output.
    """

    output_port_0_pin_2 = RWBit(OUTPUT_PORT_0, 2)
    """
    Write boolean state to port 0 pin 2. This will only apply if the pin is
    configured as an output.
    """

    output_port_0_pin_3 = RWBit(OUTPUT_PORT_0, 3)
    """
    Write boolean state to port 0 pin 3. This will only apply if the pin is
    configured as an output.
    """

    output_port_0_pin_4 = RWBit(OUTPUT_PORT_0, 4)
    """
    Write boolean state to port 0 pin 4. This will only apply if the pin is
    configured as an output.
    """

    output_port_0_pin_5 = RWBit(OUTPUT_PORT_0, 5)
    """
    Write boolean state to port 0 pin 5. This will only apply if the pin is
    configured as an output.
    """

    output_port_0_pin_6 = RWBit(OUTPUT_PORT_0, 6)
    """
    Write boolean state to port 0 pin 6. This will only apply if the pin is
    configured as an output.
    """

    output_port_0_pin_7 = RWBit(OUTPUT_PORT_0, 7)
    """
    Write boolean state to port 0 pin 7. This will only apply if the pin is
    configured as an output.
    """

    output_port_1 = RWBits(8, OUTPUT_PORT_1, 0)
    """
    Write 8 bits of state to port 1. This will only apply to pins that are
    configured as outputs.
    """

    output_port_1_pin_0 = RWBit(OUTPUT_PORT_1, 0)
    """
    Write boolean state to port 1 pin 0. This will only apply if the pin is
    configured as an output.
    """

    output_port_1_pin_1 = RWBit(OUTPUT_PORT_1, 1)
    """
    Write boolean state to port 1 pin 1. This will only apply if the pin is
    configured as an output.
    """

    output_port_1_pin_2 = RWBit(OUTPUT_PORT_1, 2)
    """
    Write boolean state to port 1 pin 2. This will only apply if the pin is
    configured as an output.
    """

    output_port_1_pin_3 = RWBit(OUTPUT_PORT_1, 3)
    """
    Write boolean state to port 1 pin 3. This will only apply if the pin is
    configured as an output.
    """

    output_port_1_pin_4 = RWBit(OUTPUT_PORT_1, 4)
    """
    Write boolean state to port 1 pin 4. This will only apply if the pin is
    configured as an output.
    """

    output_port_1_pin_5 = RWBit(OUTPUT_PORT_1, 5)
    """
    Write boolean state to port 1 pin 5. This will only apply if the pin is
    configured as an output.
    """

    output_port_1_pin_6 = RWBit(OUTPUT_PORT_1, 6)
    """
    Write boolean state to port 1 pin 6. This will only apply if the pin is
    configured as an output.
    """

    output_port_1_pin_7 = RWBit(OUTPUT_PORT_1, 7)
    """
    Write boolean state to port 1 pin 7. This will only apply if the pin is
    configured as an output.
    """

    polarity_inversions = RWBits(16, POLARITY_INVERSION_PORT_0, 0, register_width=2)
    """Read or write 16 bits of polarity inversion state."""

    polarity_inversion_port_0 = RWBits(8, POLARITY_INVERSION_PORT_0, 0)
    """Read or write 8 bits of port 0 polarity inversion state."""

    polarity_inversion_port_0_pin_0 = RWBit(POLARITY_INVERSION_PORT_0, 0)
    """Read or write port 0 pin 0 polarity inversion state."""

    polarity_inversion_port_0_pin_1 = RWBit(POLARITY_INVERSION_PORT_0, 1)
    """Read or write port 0 pin 1 polarity inversion state."""

    polarity_inversion_port_0_pin_2 = RWBit(POLARITY_INVERSION_PORT_0, 2)
    """Read or write port 0 pin 2 polarity inversion state."""

    polarity_inversion_port_0_pin_3 = RWBit(POLARITY_INVERSION_PORT_0, 3)
    """Read or write port 0 pin 3 polarity inversion state."""

    polarity_inversion_port_0_pin_4 = RWBit(POLARITY_INVERSION_PORT_0, 4)
    """Read or write port 0 pin 4 polarity inversion state."""

    polarity_inversion_port_0_pin_5 = RWBit(POLARITY_INVERSION_PORT_0, 5)
    """Read or write port 0 pin 5 polarity inversion state."""

    polarity_inversion_port_0_pin_6 = RWBit(POLARITY_INVERSION_PORT_0, 6)
    """Read or write port 0 pin 6 polarity inversion state."""

    polarity_inversion_port_0_pin_7 = RWBit(POLARITY_INVERSION_PORT_0, 7)
    """Read or write port 0 pin 7 polarity inversion state."""

    polarity_inversion_port_1 = RWBits(8, POLARITY_INVERSION_PORT_1, 0)
    """Read or write 8 bits of port 1 polarity inversion state."""

    polarity_inversion_port_1_pin_0 = RWBit(POLARITY_INVERSION_PORT_1, 0)
    """Read or write port 1 pin 0 polarity inversion state."""

    polarity_inversion_port_1_pin_1 = RWBit(POLARITY_INVERSION_PORT_1, 1)
    """Read or write port 1 pin 1 polarity inversion state."""

    polarity_inversion_port_1_pin_2 = RWBit(POLARITY_INVERSION_PORT_1, 2)
    """Read or write port 1 pin 2 polarity inversion state."""

    polarity_inversion_port_1_pin_3 = RWBit(POLARITY_INVERSION_PORT_1, 3)
    """Read or write port 1 pin 3 polarity inversion state."""

    polarity_inversion_port_1_pin_4 = RWBit(POLARITY_INVERSION_PORT_1, 4)
    """Read or write port 1 pin 4 polarity inversion state."""

    polarity_inversion_port_1_pin_5 = RWBit(POLARITY_INVERSION_PORT_1, 5)
    """Read or write port 1 pin 5 polarity inversion state."""

    polarity_inversion_port_1_pin_6 = RWBit(POLARITY_INVERSION_PORT_1, 6)
    """Read or write port 1 pin 6 polarity inversion state."""

    polarity_inversion_port_1_pin_7 = RWBit(POLARITY_INVERSION_PORT_1, 7)
    """Read or write port 1 pin 7 polarity inversion state."""

    configuration_ports = RWBits(16, CONFIGURATION_PORT_0, 0, register_width=2)
    """
    Read or write 16 bits of configuration state.
    If a bit is set to 1, the corresponding port pin is enabled as an input
    with a high-impedance output driver. If a bit in this register is cleared
    to 0, the corresponding port pin is enabled as an output.
    """

    configuration_port_0 = RWBits(8, CONFIGURATION_PORT_0, 0)
    """Read or write 8 bits of port 0 configuration state. 0 = Output, 1 = Input"""

    configuration_port_0_pin_0 = RWBit(CONFIGURATION_PORT_0, 0)
    """Read or write port 0 pin 0 configuration state. 0 = Output, 1 = Input"""

    configuration_port_0_pin_1 = RWBit(CONFIGURATION_PORT_0, 1)
    """Read or write port 0 pin 1 configuration state. 0 = Output, 1 = Input"""

    configuration_port_0_pin_2 = RWBit(CONFIGURATION_PORT_0, 2)
    """Read or write port 0 pin 2 configuration state. 0 = Output, 1 = Input"""

    configuration_port_0_pin_3 = RWBit(CONFIGURATION_PORT_0, 3)
    """Read or write port 0 pin 3 configuration state. 0 = Output, 1 = Input"""

    configuration_port_0_pin_4 = RWBit(CONFIGURATION_PORT_0, 4)
    """Read or write port 0 pin 4 configuration state. 0 = Output, 1 = Input"""

    configuration_port_0_pin_5 = RWBit(CONFIGURATION_PORT_0, 5)
    """Read or write port 0 pin 5 configuration state. 0 = Output, 1 = Input"""

    configuration_port_0_pin_6 = RWBit(CONFIGURATION_PORT_0, 6)
    """Read or write port 0 pin 6 configuration state. 0 = Output, 1 = Input"""

    configuration_port_0_pin_7 = RWBit(CONFIGURATION_PORT_0, 7)
    """Read or write port 0 pin 7 configuration state. 0 = Output, 1 = Input"""

    configuration_port_1 = RWBits(8, CONFIGURATION_PORT_1, 0)
    """Read or write 8 bits of port 1 configuration state. 0 = Output, 1 = Input"""

    configuration_port_1_pin_0 = RWBit(CONFIGURATION_PORT_1, 0)
    """Read or write port 1 pin 0 configuration state. 0 = Output, 1 = Input"""

    configuration_port_1_pin_1 = RWBit(CONFIGURATION_PORT_1, 1)
    """Read or write port 1 pin 1 configuration state. 0 = Output, 1 = Input"""

    configuration_port_1_pin_2 = RWBit(CONFIGURATION_PORT_1, 2)
    """Read or write port 1 pin 2 configuration state. 0 = Output, 1 = Input"""

    configuration_port_1_pin_3 = RWBit(CONFIGURATION_PORT_1, 3)
    """Read or write port 1 pin 3 configuration state. 0 = Output, 1 = Input"""

    configuration_port_1_pin_4 = RWBit(CONFIGURATION_PORT_1, 4)
    """Read or write port 1 pin 4 configuration state. 0 = Output, 1 = Input"""

    configuration_port_1_pin_5 = RWBit(CONFIGURATION_PORT_1, 5)
    """Read or write port 1 pin 5 configuration state. 0 = Output, 1 = Input"""

    configuration_port_1_pin_6 = RWBit(CONFIGURATION_PORT_1, 6)
    """Read or write port 1 pin 6 configuration state. 0 = Output, 1 = Input"""

    configuration_port_1_pin_7 = RWBit(CONFIGURATION_PORT_1, 7)
    """Read or write port 1 pin 7 configuration state. 0 = Output, 1 = Input"""
