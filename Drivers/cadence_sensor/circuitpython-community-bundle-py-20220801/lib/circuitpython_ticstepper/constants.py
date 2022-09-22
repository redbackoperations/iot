# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`circuitpython_ticstepper.constants`
================================================================================

Constants need to TIC stepper motor driver operation


* Author(s): Alec Delaney

"""

from collections import namedtuple

StepModeValues = namedtuple("StepModeValues", ["value", "multiplier"])


class StepMode:
    """Step mode constants"""

    FULL = StepModeValues(0, 1)
    HALF = StepModeValues(1, 2)
    QUARTER = StepModeValues(2, 4)
    EIGHTH = StepModeValues(3, 8)
    SIXTEENTH = StepModeValues(4, 16)
    THIRTY_SECONDTH = StepModeValues(5, 32)
    SIXTY_FOURTH = StepModeValues(7, 64)
    ONE_TWENTY_EIGTH = StepModeValues(8, 128)
    TWO_FIFTY_SIXTH = StepModeValues(9, 256)

    @classmethod
    def get_by_factor(cls, factor: int):
        """Gets a StepMode constant by the TIC param value

        :param int value: The TIC param value
        """

        for attr_value in cls.__dict__.values():
            if (
                isinstance(attr_value, StepModeValues)
                and attr_value.multiplier == factor
            ):
                return attr_value
        raise ValueError("Could not find the requested step mode")

    @classmethod
    def get_by_enum(cls, enum: int):
        """Gets a StepMode by the Tic enum value

        :param int enum: The Tic enum value
        """

        for attr_value in cls.__dict__.values():
            if isinstance(attr_value, StepModeValues) and attr_value.value == enum:
                return attr_value
        raise ValueError("Could not find the requested step mode")


# pylint: disable=too-few-public-methods
class OperationMode:
    """The operation modes of the TIC stepper motor driver"""

    RESET = 0
    DEENERGIZED = 2
    SOFT_ERROR = 4
    WAITING_FOR_ERR_LINE = 6
    STARTING_UP = 8
    NORMAL = 10
