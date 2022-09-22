# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Arofarn
#
# SPDX-License-Identifier: MIT
"""
`trellism4_extended`
================================================================================

CircuitPython library to extended Adafruit NeotrellisM4 board with two Neotrellis seesaw
boards (or more !).


* Author(s): arofarn

Implementation Notes
--------------------

**Hardware:**

* Adafruit NeoTrellis M4 Express: https://www.adafruit.com/product/3938
* Adafruit NeoTrellis RGB Driver PCB for 4x4 Keypad :https://www.adafruit.com/product/3954

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit CircuitPython bus_devices library (from Adafruit_CircuitPython_Bundle):
  https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases

"""

__version__ = "1.0.0"
__repo__ = "https://github.com/arofarn/CircuitPython_TrellisM4_extended.git"


import board
import digitalio
from micropython import const
from adafruit_seesaw.keypad import KeyEvent
from adafruit_matrixkeypad import Matrix_Keypad
from neopixel import NeoPixel


_NEO_TRELLIS_NUM_ROWS = const(4)
_NEO_TRELLIS_NUM_COLS = const(4)
_NEO_TRELLIS_NUM_KEYS = const(16)

# _NEO_TRELLIS_MAX_CALLBACKS = const(32)

_TRELLISM4_LEFT_PART = const(0)
_TRELLISM4_RIGHT_PART = const(4)


def _key(xval):
    return int(int(xval / 4) * 8 + (xval % 4))


def _seesaw_key(xval):
    return int(int(xval / 8) * 4 + (xval % 8))


def _to_seesaw_key(xval):
    return int(xval + (xval // 4) * 4)


class _TrellisNeoPixel:
    """Neopixel driver"""

    # Lots of stuff come from Adafruit_CircuitPython_seesaw/neopixel.py

    def __init__(
        self, auto_write=True, brightness=1.0, part=_TRELLISM4_LEFT_PART, left_part=None
    ):
        if part == _TRELLISM4_LEFT_PART:
            self.pix = NeoPixel(
                board.NEOPIXEL, 32, auto_write=False, brightness=brightness
            )
        elif part == _TRELLISM4_RIGHT_PART:
            self.pix = left_part.pix
        self.auto_write = auto_write
        self._offset = part

    def __setitem__(self, key, color):
        self.pix[_key(key) + self._offset] = color
        if self.auto_write:
            self.show()

    def __getitem__(self, key):
        return self.pix[_key(key) + self._offset]

    def fill(self, color):
        """Fill method wrapper"""
        # Suppress auto_write while filling.
        current_auto_write = self.auto_write
        self.auto_write = False
        for i in range(16):
            self[i] = color
        if current_auto_write:
            self.show()
        self.auto_write = current_auto_write

    def show(self):
        """Fill method wrapper"""
        self.pix.show()


class _TrellisKeypad:
    """Simple Keypad object for Trellis M4
    No pixel, no rotation
    Key numbers : 0 - 15"""

    def __init__(self, part=_TRELLISM4_LEFT_PART, row_pins=None):
        self._offset = part
        col_pins = []
        for x in range(self._offset, self._offset + _NEO_TRELLIS_NUM_COLS):
            col_pin = digitalio.DigitalInOut(getattr(board, "COL{}".format(x)))
            col_pins.append(col_pin)

        if part == _TRELLISM4_LEFT_PART:
            self.row_pins = []
            for y in range(_NEO_TRELLIS_NUM_ROWS):
                row_pin = digitalio.DigitalInOut(getattr(board, "ROW{}".format(y)))
                self.row_pins.append(row_pin)
        elif part == _TRELLISM4_RIGHT_PART:
            if row_pins is None:
                raise ValueError("Missing row_pins list for the right part")
            self.row_pins = row_pins
        else:
            raise ValueError("part arg should be 0 (left part) or 4 (right part)")

        key_names = []
        for y in range(4):
            row = []
            for x in range(4):
                row.append(4 * x + y)
            key_names.append(row)  # Keys of each halves is numbered from 0-15

        self._matrix = Matrix_Keypad(col_pins, self.row_pins, key_names)

    @property
    def pressed_keys(self):
        """A list of tuples of currently pressed button coordinates.

        .. code-block:: python

            import time
            import adafruit_trellism4

            trellis = adafruit_trellism4.TrellisM4Express()

            current_press = set()
            while True:
                pressed = set(trellis.pressed_keys)
                for press in pressed - current_press:
                    print("Pressed:", press)
                for release in current_press - pressed:
                    print("Released:", release)
                time.sleep(0.08)
                current_press = pressed
        """
        return self._matrix.pressed_keys


class NeoTrellisM4:
    """
    Driver for the Adafruit NeoTrellis.

    :param left_part: None (default) or left part object

    .. note:: if None (or ommitted) the class create a
      neotrellis.multitrellis-compatible object for the left half of the
      TrellisM4 board. Else the right part is created and the arguement should
      be the left part object.

    Example:

    .. code-block:: python

        from neotrellism4 import NeoTrellisM4
        trellis_left = NeoTrellisM4()
        trellis_right = NeoTrellisM4(left_part=trellis_left)
    """

    EDGE_HIGH = const(0)
    EDGE_LOW = const(1)
    EDGE_FALLING = const(2)
    EDGE_RISING = const(3)

    def __init__(self, left_part=None):
        if left_part is None:
            self._offset = _TRELLISM4_LEFT_PART
            self.pixels = _TrellisNeoPixel()
            self.keypad = _TrellisKeypad()
        else:
            self._offset = _TRELLISM4_RIGHT_PART
            self.pixels = _TrellisNeoPixel(
                32, part=_TRELLISM4_RIGHT_PART, left_part=left_part.pixels
            )
            self.keypad = _TrellisKeypad(
                part=_TRELLISM4_RIGHT_PART, row_pins=left_part.keypad.row_pins
            )

        self._events = [0] * _NEO_TRELLIS_NUM_KEYS
        self._current_press = set()
        self._key_edges = [self.EDGE_HIGH] * _NEO_TRELLIS_NUM_KEYS  # Keys edges
        self._current_events = bytearray()
        self.callbacks = [None] * 16

    @property
    def interrupt_enabled(self):
        """Only for compatibility with neotrellis module:
        Interrupts are disable on trellis M4 keypad"""
        return False

    # pylint: disable=unused-argument, no-self-use
    @interrupt_enabled.setter
    def interrupt_enabled(self, value):
        """Only for compatibility with neotrellis module:
        Interrupts are disable on trellis M4 keypad
        """
        print("Warning: no interrupt with Trellis M4 keypad (method does nothing)")

    # pylint: enable=unused-argument, no-self-use

    @property
    def count(self):
        """Return the pressed keys count"""
        self._read_keypad()
        return len(self._current_events)

    # pylint: disable=unused-argument, no-self-use
    @count.setter
    def count(self, value):
        """Only for compatibility with neotrellis module"""
        raise AttributeError("count is read only")

    # pylint: enable=unused-argument, no-self-use

    def set_event(self, key, edge, enable):
        """
        Control which kinds of events are set

        :param int key: the key number
        :param int edge: the type of event
        :param bool enable: True to enable the event, False to disable it
        """

        if enable not in (True, False):
            raise ValueError("event enable must be True or False")
        if edge > 3 or edge < 0:
            raise ValueError("invalid edge")

        # Pas besoin de l'écriture sur I2C mais de l'enregistrer dans self._events
        if enable:
            self._events[key] = self._events[key] | (1 << edge)
        else:
            self._events[key] = self._events[key] & (0xF ^ (1 << edge))

    def read_keypad(self, num):
        """
        Read data from the keypad

        :param int num: The number of bytes to read
        """

        while num > len(self._current_events):
            self._current_events.append(0xFF)
        return self._current_events[:num]

    def _read_keypad(self):
        """Read keypad and update _key_edges and _current_events"""
        pressed = set(self.keypad.pressed_keys)
        # default : not pressed => EDGE_HIGH
        self._key_edges = [self.EDGE_HIGH] * _NEO_TRELLIS_NUM_KEYS
        for k in pressed:
            self._key_edges[k] = self.EDGE_LOW
        for k in pressed - self._current_press:
            self._key_edges[k] = self.EDGE_RISING
        for k in self._current_press - pressed:
            self._key_edges[k] = self.EDGE_FALLING

        self._current_press = pressed
        self._current_events = bytearray()

        for k in range(_NEO_TRELLIS_NUM_KEYS):
            if (self._events[k] >> self._key_edges[k]) & 0x1:
                raw_evt = (_to_seesaw_key(k) << 2) | self._key_edges[k]
                self._current_events.append(raw_evt)

    def activate_key(self, key, edge, enable=True):
        """
        Activate or deactivate a key on the trellis

        :param int key : key number from 0 to 16.
        :param int edge : specifies what edge to register an event on and can be
        NeoTrellis.EDGE_FALLING or NeoTrellis.EDGE_RISING.
        :param bool enable : should be set to True if the event is to be enabled,
        or False if the event is to be disabled.
        """
        self.set_event(key, edge, enable)

    def sync(self):
        """
        Read any events from the Trellis hardware and call associated callbacks.
        """
        available = self.count
        if available > 0:
            available = available + 2
            buf = self.read_keypad(available)
            for raw in buf:
                evt = KeyEvent(_seesaw_key((raw >> 2) & 0x3F), raw & 0x3)
                if (
                    evt.number < _NEO_TRELLIS_NUM_KEYS
                    and self.callbacks[evt.number] is not None
                ):
                    self.callbacks[evt.number](evt)
