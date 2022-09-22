#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CircuitPython

# The MIT License (MIT)
#
# Copyright (c) 2018 Stefan Krüger
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# 1 blank line required between summary line and description
# pylama:ignore=D205

u"""
s-light CircuitPython TLC5957 library.
====================================================

CircuitPython library for
`TI TLC5957 48-channel 16bit LED-Driver
<http://www.ti.com/product/TLC5957/>`_

* Author(s): Stefan Krüger


Implementation Notes
--------------------

**Hardware:**

* example PCB with TLC5957 and 4x4 SMD RGB LEDs
  https://github.com/s-light/magic_amulet_pcbs/tree/master/LEDBoard_4x4_HD

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""


__version__ = "0.1.2"
__repo__ = "https://github.com/s-light/slight_CircuitPython_TLC5957.git"

# imports

# import time

# from enum import Enum, unique
# https://docs.python.org/3/library/enum.html
# currently not supported by CircuitPython


class TLC5957(object):
    """TLC5957 16-bit 48 channel LED PWM driver.

    This chip is designed to drive 16 RGB LEDs with 16-bit PWM per Color.
    The class has an interface compatible with FancyLED.
    and with this is similar to the NeoPixel and DotStar Interfaces.

    :param ~busio.SPI spi: An instance of the SPI bus connected to the chip.
        The clock and MOSI must be set
        the MISO (input) is currently unused.
        Maximal data clock frequence is:
        - TLC5957: 33MHz
    :param ~digitalio.DigitalInOut latch: The chip LAT (latch) pin object
        that implements the DigitalInOut API.
    :param ~pulseio.PWMOut gsclk: The chip Grayscale Clock pin object
        that implements the PWMOut API.
    :param bool pixel_count: Number of RGB-LEDs (=Pixels) are connected.
    """

    # TLC5957 data / register structure
    #
    # some detailed information on the protocol based on
    # http://www.ti.com/lit/ds/symlink/t

    ##########################################
    # helper
    ##########################################

    CHIP_LED_COUNT = 16
    COLORS_PER_PIXEL = 3
    BUFFER_BYTES_PER_COLORS = 2
    BUFFER_BYTES_PER_PIXEL = BUFFER_BYTES_PER_COLORS * COLORS_PER_PIXEL
    CHIP_SHIFT_BUFFER_BIT_COUNT = 48
    CHIP_SHIFT_BUFFER_BYTE_COUNT = CHIP_SHIFT_BUFFER_BIT_COUNT // 8
    CHIP_GS_BUFFER_BYTE_COUNT = CHIP_SHIFT_BUFFER_BYTE_COUNT * CHIP_LED_COUNT
    CHIP_FUNCTION_CMD_BIT_COUNT = 16
    CHIP_FUNCTION_CMD_BYTE_COUNT = CHIP_FUNCTION_CMD_BIT_COUNT // 8

    # https://docs.python.org/3/library/enum.html#intenum
    # @unique
    # class Function_Command(IntEnum):
    class Function_Command(object):
        """Enum for available function commands."""

        # Yet another pylint issue, it fails to recognize a
        # 'Enum' class by definition has no public methods.  Disable the check.
        # pylint: disable=too-few-public-methods

        # """
        # Enum for available function commands.
        #
        # 3.10 Function Commands Summary (page 30)
        # http:#www.ti.com/lit/ug/slvuaf0/slvuaf0.pdf#page=30&zoom=auto,-110,464
        #
        # WRTGS
        # -----
        #     48-bit GS data write
        #     copy common 48bit to GS-data-latch[GS-counter]
        #     GS-counter -1
        # LATGS
        # -----
        #     latch grayscale
        #     (768-bit GS data latch)
        #     copy common 48bit to GS-data-latch[0]
        #     if XREFRESH = 0
        #         GS-data-latch copy to GS-data-latch 2
        #     if XREFRESH = 1
        #         GS-data-latch copy to GS-data-latch 2
        # WRTFC
        # -----
        #     write FC data
        #     copy common 48bit to FC-data
        #     if used after FCWRTEN
        # LINERESET
        # ---------
        #     Line Counter register clear.
        #     copy common 48bit to GS-data-latch[0]
        #     data-latch-counter reset
        #     if XREFRESH = 0
        #         Autorefresh enabled
        #         wehn GS-counter == 65535: GS-data-latch copyto GS-data-latch2
        #     if XREFRESH = 1
        #         Autorefresh disabled
        #         GS-data-latch copy to GS-data-latch 2
        #         GS-counter reset
        #         OUTx forced off
        #     change group pattern when received
        # READFC
        # ------
        #     read FC data
        #     copy FC-data to common 48bit
        #     (can be read at SOUT)
        # TMGRST
        # ------
        #     reset line-counter
        #     GS-counter = 0
        #     OUTx forced off
        # FCWRTEN
        # -------
        #     enable writes to FC
        #     this must send before WRTFC
        # """

        WRTGS = 1
        LATGS = 3
        WRTFC = 5
        LINERESET = 7
        READFC = 11
        TMGRST = 13
        FCWRTEN = 15

    ##########################################
    # 3.3.3 Function Control (FC) Register
    # BIT     NAME            default     description
    # 0-1     LODVTH          01          LED Open Detection Voltage
    # 2-3     SEL_TD0         01          TD0 select. SOUT hold time.
    # 4       SEL_GDLY        1           Group Delay. 0 = No Delay
    # 5       XREFRESH        0           auto data refresh mode.
    #                                     on LATGS/LINERESET → data copied
    #                                       from GS1 to GS2
    #                                     0 = enabled → GS-counter continues
    #                                     1 = disabled → GS-counter reset;
    #                                       OUTx forced off
    # 6       SEL_GCK_EDGE    0           GCLK edge select.
    #                                     0 = OUTx toggle only on
    #                                       rising edge of GLCK
    #                                     1 = OUTx toggle on
    #                                       rising & falling edge of GLCK
    # 7       SEL_PCHG        0           Pre-charge working mode select
    # 8       ESPWM           0           ESPWM mode enable bit.
    #                                       (0 = enabled, 1 = disabled)
    # 9       LGSE3           0           Compensation for Blue LED.
    #                                       (0 = disabled, 1 = enabled)
    # 10      SEL_SCK_EDGE    0           SCLK edge select
    #                                       (0 = rising edge, 1 = both edges)
    # 11-13   LGSE1           000         Low Gray Scale Enhancement for
    #                                       Red/Green/Blue color
    # 14-22   CCB             100000000   Color brightness control data Blue
    #                                       (000h-1FFh)
    # 23-31   CCG             100000000   Color brightness control data Green
    #                                       (000h-1FFh)
    # 32-40   CCR             100000000   Color brightness control data Red
    #                                       (000h-1FFh)
    # 41-43   BC              100         Global brightness control data
    #                                       (0h-7h)
    # 44      PokerTransMode  0           Poker trans mode enable bit.
    #                                       (0 = disabled, 1 = enabled)
    # 45-47   LGSE2           000         first line performance improvment
    # TODO(s-light): add function control options

    ##########################################

    def __init__(
            self,
            # *,    # this forces all following parameter to be named
            spi,
            spi_clock,
            spi_mosi,
            spi_miso,
            latch,
            gsclk,
            pixel_count=16):
        """Init."""
        # i don't see a better way to get all this initialised...
        # pylint: disable=too-many-arguments

        self._spi = spi
        self._spi_clock = spi_clock
        self._spi_mosi = spi_mosi
        self._spi_miso = spi_miso
        self._latch = latch
        self._gsclk = gsclk
        # how many pixels are there?
        self.pixel_count = pixel_count
        # print("pixel_count", self.pixel_count)
        # calculate how many chips are needed
        self.chip_count = self.pixel_count // self.CHIP_LED_COUNT
        if self.pixel_count % self.CHIP_LED_COUNT > 0:
            self.chip_count += 1
        # print("chip_count", self.chip_count)
        self.channel_count = self.pixel_count * self.COLORS_PER_PIXEL

        # data is stored in raw buffer
        self._buffer = bytearray(
            self.CHIP_GS_BUFFER_BYTE_COUNT * self.chip_count)
        # print("CHIP_GS_BUFFER_BYTE_COUNT", self.CHIP_GS_BUFFER_BYTE_COUNT)
        # print("_buffer", self._buffer)
        # write initial 0 values
        self.show()
        self.show()

    def _write_buffer(self):
        # Write out the current state to the shift register.
        buffer_start = 0
        write_count = (
            (self.CHIP_SHIFT_BUFFER_BYTE_COUNT * self.chip_count)
            - self.CHIP_FUNCTION_CMD_BYTE_COUNT)

        for index in range(self.CHIP_LED_COUNT):
            try:
                # wait untill we have access to / locked SPI bus
                while not self._spi.try_lock():
                    pass
                # configure
                # 10kHz
                # baudrate = (10 * 1000)
                # 1MHz
                # baudrate = (1000 * 1000)
                # 10MHz
                baudrate = (10 * 1000 * 1000)
                self._spi.configure(
                    baudrate=baudrate, polarity=0, phase=0, bits=8)

                # write data
                # self._spi.write(
                #     self._buffer, start=buffer_start, end=write_count)

                # workaround for bitbangio.SPI.write missing start & end
                buffer_in = bytearray(write_count)
                self._spi.write_readinto(
                    self._buffer,
                    buffer_in,
                    out_start=buffer_start,
                    out_end=buffer_start + write_count)

            finally:
                # Ensure the SPI bus is unlocked.
                self._spi.unlock()
            buffer_start += write_count
            # special
            if index == self.CHIP_LED_COUNT - 1:
                self._write_buffer_with_function_command(
                    self.Function_Command.LATGS, buffer_start)
            else:
                self._write_buffer_with_function_command(
                    self.Function_Command.WRTGS, buffer_start)
            buffer_start += 2

    def _write_buffer_with_function_command(
            self,
            function_command,
            buffer_start):
        """Bit-Banging SPI write to sync with latch pulse."""
        # combine two 8bit buffer parts to 16bit value
        value = (
            (self._buffer[buffer_start + 0] << 8) |
            self._buffer[buffer_start + 1]
        )

        self._spi_clock.value = 0
        self._spi_mosi.value = 0
        self._latch.value = 0
        latch_start_index = self.CHIP_LED_COUNT - function_command
        for index in range(self.CHIP_FUNCTION_CMD_BIT_COUNT):
            if latch_start_index == index:
                self._latch.value = 1

            # b1000000000000000
            if value & 0x8000:
                self._spi_mosi.value = 1
            else:
                self._spi_mosi.value = 0
            value <<= 1

            # CircuitPython needs 14us for this setting pin high and low again.
            self._spi_clock.value = 1
            # 1ms
            # time.sleep(0.001)
            # 100us
            # time.sleep(0.0001)
            # 10us
            # time.sleep(0.00001)
            self._spi_clock.value = 0

        self._latch.value = 0

    def show(self):
        """Write out Grayscale Values to chips."""
        self._write_buffer()

    def set_channel(self, channel_index, value):
        """
        Set the value for the provided channel.

        :param int channel_index: 0..(pixel_count * 3)
        :param int value: 0..65535
        """
        if 0 <= channel_index < (self.channel_count):
            # check if values are in range
            assert 0 <= value <= 65535
            # temp = channel_index
            # we change channel order here:
            # buffer channel order is blue, green, red
            pixel_index_offset = channel_index % self.COLORS_PER_PIXEL
            if pixel_index_offset == 0:
                channel_index += 2
            if pixel_index_offset == 2:
                channel_index -= 2
            # print("{:>2} → {:>2}".format(temp, channel_index))
            buffer_index = channel_index * self.BUFFER_BYTES_PER_COLORS
            self._set_16bit_value_in_buffer(buffer_index, value)
            # self._set_16bit_value_in_buffer(
            #     self.COLORS_PER_PIXEL - channel_index, value)
        else:
            raise IndexError(
                "channel_index {} out of range (0..{})".format(
                    channel_index,
                    self.channel_count
                )
            )

    def _get_16bit_value_from_buffer(self, buffer_start):
        return (
            (self._buffer[buffer_start + 0] << 8) |
            self._buffer[buffer_start + 1]
        )

    def _set_16bit_value_in_buffer(self, buffer_start, value):
        assert 0 <= value <= 65535
        # print("buffer_start", buffer_start, "value", value)
        self._buffer[buffer_start + 0] = (value >> 8) & 0xFF
        self._buffer[buffer_start + 1] = value & 0xFF

    @staticmethod
    def _convert_01_float_to_16bit_integer(value):
        """Convert 0..1 Float Value to 16bit (0..65535) Range."""
        # check if values are in range
        assert 0 <= value <= 1
        # convert to 16bit value
        return int(value * 65535)

    @classmethod
    def _convert_if_float(cls, value):
        """Convert if value is Float."""
        if isinstance(value, float):
            value = cls._convert_01_float_to_16bit_integer(value)
        return value

    # Define index and length properties to set and get each channel as
    # atomic RGB tuples.  This provides a similar feel as using neopixels.
    def __len__(self):
        """Retrieve TLC5975 the total number of Pixels available."""
        return self.pixel_count

    def __getitem__(self, key):
        """
        Retrieve the R, G, B values for the provided channel as a 3-tuple.

        Each value is a 16-bit number from 0-65535.
        """
        if 0 < key > (self.pixel_count-1):
            return (
                self._get_16bit_value_from_buffer(key + 0),
                self._get_16bit_value_from_buffer(key + 2),
                self._get_16bit_value_from_buffer(key + 4)
            )
        else:
            raise IndexError

    def __setitem__(self, key, value):
        """
        Set the R, G, B values for the provided channel.

        Specify a 3-tuple of R, G, B values that are each
        - 16-bit numbers (0-65535)
        - or 0..1 floats
        """
        if 0 <= key < self.pixel_count:
            # print("value", value)
            # convert to list
            value = list(value)
            # print("value", value)
            # print("rep:")
            # repr(value)
            # print("check length..")
            assert len(value) == 3
            # check if we have float values
            value[0] = self._convert_if_float(value[0])
            value[1] = self._convert_if_float(value[1])
            value[2] = self._convert_if_float(value[2])
            # print("value", value)

            # check if values are in range
            assert 0 <= value[0] <= 65535
            assert 0 <= value[1] <= 65535
            assert 0 <= value[2] <= 65535
            # update buffer
            # print("key", key, "value", value)
            # we change channel order here:
            # buffer channel order is blue, green, red
            buffer_pixel_start = key * self.BUFFER_BYTES_PER_PIXEL
            self._set_16bit_value_in_buffer(
                buffer_pixel_start + (0 * self.BUFFER_BYTES_PER_COLORS),
                value[2])
            self._set_16bit_value_in_buffer(
                buffer_pixel_start + (1 * self.BUFFER_BYTES_PER_COLORS),
                value[1])
            self._set_16bit_value_in_buffer(
                buffer_pixel_start + (2 * self.BUFFER_BYTES_PER_COLORS),
                value[0])
        else:
            raise IndexError("index {} out of range".format(key))

##########################################
