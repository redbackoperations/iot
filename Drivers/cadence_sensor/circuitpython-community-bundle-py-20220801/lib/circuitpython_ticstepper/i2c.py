# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`circuitpython_ticstepper.i2c`
================================================================================

TIC Motor over I2C control


* Author(s): Alec Delaney

"""

import struct
from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_struct import Struct
from circuitpython_ticstepper import TicMotor
from circuitpython_ticstepper.constants import StepMode, OperationMode

try:
    from typing import Optional, Type, List
    from circuitpython_typing import ReadableBuffer
    from busio import I2C
    from circuitpython_ticstepper.constants import (  # pylint: disable=ungrouped-imports
        StepModeValues,
    )
except ImportError:
    pass

_CMD_STEP_MODE = const(0x94)
_CMD_RESET = const(0xB0)
_CMD_CLEAR_ERROR = const(0x8A)
_CMD_MAX_SPEED = const(0xE6)
_CMD_HALT_SET = const(0xEC)
_CMD_MOVE = const(0xE0)
_CMD_DRIVE = const(0xE3)
_CMD_GET_VAR = const(0xA1)
_CMD_MAX_ACCEL = const(0xEA)
_CMD_MAX_DECEL = const(0xE9)
_CMD_CURRENT_LIMIT = const(0x91)
_CMD_ENERGIZE = const(0x85)
_CMD_DEENERGIZE = const(0x86)

_OFFSET_CURRENT_VELOCITY = const(0x26)
_OFFSET_STEP_MODE = const(0x49)
_OFFSET_UPTIME = const(0x35)
_OFFSET_MAX_SPEED = const(0x47)
_OFFSET_MAX_ACCEL = const(0x4F)
_OFFSET_MAX_DECEL = const(0x4B)
_OFFSET_CURRENT_LIMIT = const(0x40)
_OFFSET_ENERGIZED = const(0x00)


class ClearMSBByteStruct:
    """
    Arbitrary structure register that is readable and writeable.
    Values are tuples that map to the values in the defined struct.  See struct
    module documentation for struct format string and its possible value types.

    :param int register_address: The register address to read the bit from
    """

    def __init__(self, register_address: int) -> None:
        self.format = "<b"
        self.buffer = bytearray(1 + struct.calcsize(self.format))
        self.buffer[0] = register_address

    def __get__(
        self, obj: "TicMotorI2C", objtype: Optional[Type["TicMotorI2C"]] = None
    ) -> List[int]:
        with obj.i2c_device as i2c:
            i2c.write_then_readinto(self.buffer, self.buffer, out_end=1, in_start=1)
        return struct.unpack_from(self.format, memoryview(self.buffer)[1:])

    def __set__(self, obj: "TicMotorI2C", value: ReadableBuffer) -> None:
        struct.pack_into(self.format, self.buffer, 1, *value)
        with obj.i2c_device as i2c:
            i2c.write(self.buffer)


# pylint: disable=too-many-instance-attributes
class TicMotorI2C(TicMotor):
    """Generic TIC motor driver contolled via I2C, this class is not intended
    to be instanced directly due to various differences between motor controllers
    - you should use a specific one instead (like ``TIC36v4``)

    :param I2C i2c: The I2C bus object
    :param int address: The I2C address of the motor driver
    :param StepModeValues step_mode: The step mode to use
    """

    _get_var_32bit_signed_reg = Struct(_CMD_GET_VAR, "<i")
    _get_var_32bit_unsigned_reg = Struct(_CMD_GET_VAR, "<I")
    _get_var_8bit_unsigned_reg = Struct(_CMD_GET_VAR, "<B")

    _step_mode_reg = ClearMSBByteStruct(_CMD_STEP_MODE)
    _max_speed_reg = Struct(_CMD_MAX_SPEED, "<I")
    _halt_set_reg = Struct(_CMD_HALT_SET, "<i")
    _move_reg = Struct(_CMD_MOVE, "<i")
    _drive_reg = Struct(_CMD_DRIVE, "<i")
    _max_accel_reg = Struct(_CMD_MAX_ACCEL, "<I")
    _max_decel_reg = Struct(_CMD_MAX_DECEL, "<I")
    _current_limit_reg = ClearMSBByteStruct(_CMD_CURRENT_LIMIT)

    _get_var_32bit_signed_reg = Struct(_CMD_GET_VAR, "<i")
    _get_var_32bit_unsigned_reg = Struct(_CMD_GET_VAR, "<I")
    _get_var_8bit_unsigned_reg = Struct(_CMD_GET_VAR, "<B")

    def __init__(
        self, i2c: I2C, address: int = 0x0E, step_mode: StepModeValues = StepMode.FULL
    ) -> None:

        self.i2c_device = I2CDevice(i2c, address)
        super().__init__(step_mode)
        self.clear()

    @property
    def step_mode(self) -> StepModeValues:
        """Gets and sets the stepper step mode"""
        self._get_var_8bit_unsigned_reg = [_OFFSET_STEP_MODE]
        return StepMode.get_by_enum(self._get_var_8bit_unsigned_reg[0])

    @step_mode.setter
    def step_mode(self, mode: StepModeValues) -> None:
        self._step_mode = mode
        self._step_mode_reg = [mode.value]

    def clear(self) -> None:
        """Clears and reinits the stepper motor"""
        self.reset()

    def _quick_write(self, cmd: int) -> None:
        packed_cmd = struct.pack("<B", cmd)
        with self.i2c_device as i2c:
            i2c.write(packed_cmd)

    def reset(self) -> None:
        """Resets the motor driver"""
        self._quick_write(_CMD_RESET)

    def reinit(self) -> None:
        """Reinitializes the motor driver"""
        self.step_mode = self._step_mode

    def clear_error(self) -> None:
        """Clears errors for the motor driver"""
        self._quick_write(_CMD_CLEAR_ERROR)

    @property
    def operation_mode(self) -> int:
        """Get the current operation mode"""
        self._get_var_8bit_unsigned_reg = [_OFFSET_ENERGIZED]
        return self._get_var_8bit_unsigned_reg[0]

    @property
    def energized(self) -> bool:
        """Whether the motor coils are energized"""
        state = self.operation_mode
        if state == OperationMode.DEENERGIZED:
            return False
        if state in (OperationMode.STARTING_UP, OperationMode.NORMAL):
            return True
        raise RuntimeError("Some other operation mode was detected")

    @energized.setter
    def energized(self, setting: bool) -> None:
        cmd = _CMD_ENERGIZE if setting else _CMD_DEENERGIZE
        self._quick_write(cmd)

    @property
    def max_speed(self) -> float:
        """Gets and sets the maximum speed for the motor"""
        self._get_var_32bit_unsigned_reg = [_OFFSET_MAX_SPEED]
        pps = self._get_var_32bit_unsigned_reg[0]
        return self._pps_to_rpm(pps)

    @max_speed.setter
    def max_speed(self, rpm: float) -> None:
        # if not -self.MAX_RPM <= rpm <= self.MAX_RPM:
        #    raise ValueError("Given speed is over the RPM threshold")
        pulse_speed = self._rpm_to_pps(rpm)
        self._max_speed_reg = [pulse_speed]

    @property
    def max_accel(self) -> float:
        """The maximum acceleration the motor can experience in rpm/s"""
        self._get_var_32bit_unsigned_reg = [_OFFSET_MAX_ACCEL]
        pps2 = self._get_var_32bit_unsigned_reg[0]
        return self._pps_to_rpm(pps2)

    @max_accel.setter
    def max_accel(self, rpms: float) -> None:
        pulse_accel = self._rpm_to_pps(rpms)
        self._max_accel_reg = [pulse_accel]

    @property
    def max_decel(self) -> float:
        """The maximum deceleration the motor can experience in rpm/s"""
        self._get_var_32bit_unsigned_reg = [_OFFSET_MAX_DECEL]
        pps2 = self._get_var_32bit_unsigned_reg[0]
        return self._pps_to_rpm(pps2)

    @max_decel.setter
    def max_decel(self, rpms: float) -> None:
        pulse_decel = self._rpm_to_pps(rpms)
        self._max_decel_reg = [pulse_decel]

    def halt_and_set_position(self, position: int = 0) -> None:
        """Stops the motor and keeps coils energized"""
        self._halt_set_reg = [position]
        self.step_mode = self._step_mode
        self._rpm = 0

    def move(self, units: int) -> None:
        """Moves the given number of steps/microsteps

        :param int units: The number of steps/microsteps to move
        """
        self._move_reg = [units]

    def drive(self, rpm: float) -> None:
        """Drives the motor at a given speed

        :param float rpm: The speed to move the motor in RPM
        """

        # if not -self.MAX_RPM <= rpm <= self.MAX_RPM:
        #    raise ValueError("Cannot set speed above {} RPM".format(self.MAX_RPM))

        self._drive_reg = [self._rpm_to_pps(rpm)]
        self._rpm = rpm

    @property
    def is_moving(self) -> bool:
        """Whether the stepper motor is actively moving"""

        self._get_var_32bit_signed_reg = [_OFFSET_CURRENT_VELOCITY]
        return self._get_var_32bit_signed_reg[0] != 0

    @property
    def uptime(self) -> float:
        """The number of seconds the motor controller has been up.  This is
        not affected by a reset command
        """

        self._get_var_32bit_unsigned_reg = [_OFFSET_UPTIME]
        return self._get_var_32bit_unsigned_reg[0] / 1000

    @property
    def current_limit(self) -> None:
        """Sets the current limit for the I2C device in Amps"""
        self._get_var_8bit_unsigned_reg = [_OFFSET_CURRENT_LIMIT]
        response = self._get_var_8bit_unsigned_reg[0]
        return self.convert_current_enum(response)

    @current_limit.setter
    def current_limit(self, current: float) -> None:
        self._current_limit_reg = [self.convert_current_value(current)]

    def convert_current_value(self, current: float) -> int:
        """Converts the desired current into the TIC value, rounds down
        to nearest acceptable value
        """

        raise NotImplementedError("Must be implemented in a TIC motor subclass")

    def convert_current_enum(self, enum_value: int) -> float:
        """Converts the desired TIC enumeration into the corresponding
        current limit
        """

        raise NotImplementedError("Must be implemented in a TIC motor subclass")
