#!/usr/bin/env python3
# coding=utf-8

# SPDX-FileCopyrightText: Copyright (c) 2022 Stefan Krüger s-light.eu
#
# SPDX-License-Identifier: MIT
"""
`ansi_escape_code`
================================================================================

simple helper library for common ANSI escape codes

inspired / based on information from
    - https://en.wikipedia.org/wiki/ANSI_escape_code
    - https://www.geeksforgeeks.org/print-colors-python-terminal/


* Author(s): Stefan Krüger

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware
    `>= 7.0.0 for the supported boards. <https://github.com/adafruit/circuitpython/releases>`_
* Python3
* terminal with support for escape codes / sequences
    (tested with `GTKTerm <https://github.com/Jeija/gtkterm>`_)
"""

# pylint: disable=invalid-name, too-few-public-methods

# how to document on class attributes:
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-autoattribute

import re
import time

##########################################
# helper functions


def create_seq(control, esc="\033["):
    r"""
    Control sequences function generator.

    :param string control: control characters.
    :param string esc: escape character. Default: ``\033[``
    :return lambda: function generator with predefined control sequences.
    """
    return lambda value="": "{esc}{value}{control}".format(
        esc=esc, value=value, control=control
    )


def create_color(color):
    """
    Create color sequences.

    :param string color: color number (as string).
    :return string: ready to use color control character string.
    """
    return create_seq("m")(color)


def get_flat_list(obj_dict):
    """Get a flattend list of all control characters in dict."""
    result = []
    # print("*"*42)
    # print("obj_dict", obj_dict)
    # print("*"*42)
    for attr_name, attr_value in obj_dict.items():
        if not attr_name.startswith("__"):
            # if type(attr_value) is str:
            #     value_str = attr_value.replace("\x1b", "\\x1b")
            # else:
            #     value_str = attr_value
            # print(
            #     "'{}' '{}': {}  "
            #     "".format(
            #         attr_name,
            #         type(attr_value),
            #         value_str,
            #     ),
            #     end=""
            # )
            if isinstance(attr_value, str):
                # print(" STRING ")
                result.append(attr_value)
            elif isinstance(attr_value, type):
                # print(" TYPE ")
                result.extend(get_flat_list(attr_value.__dict__))
            else:
                # print(" UNKNOWN ")
                pass
    # print("*"*42)
    return result


##########################################
# ANSIControllsBase Class


class ANSIControllsBase:
    """Base Class for ANSI color and control sequences."""

    esc = "\033["  #:

    # @staticmethod
    # def create_seq(control, esc=esc):
    #     return lambda value: "{esc}{value}{control}".format(
    #         esc=esc, value=value, control=control
    #     )

    @classmethod
    def get_flat_list(cls):
        """Get a flattend list of all control characters in dict."""
        result = get_flat_list(cls.__dict__)
        return result


class ANSIColors(ANSIControllsBase):
    """
    ANSI Color and Font-Effect control sequences.

    usage:

    .. code-block:: python

        # colors
        ANSIColors.fg.red
        ANSIColors.bg.green

        # font effect
        ANSIColors.bold

        # reste
        ANSIColors.reset

    """

    # reset = ANSIControllsBase.esc + "0m"
    reset = create_color("0")  #:
    bold = create_color("01")  #:
    disable = create_color("02")  #:
    underline = create_color("04")  #:
    reverse = create_color("07")  #:
    strikethrough = create_color("09")  #:
    invisible = create_color("08")  #:

    # class fg:
    #     """Forderground Colors."""
    #
    #     black = create_color("30m")
    #     red = create_color("31m")
    #     green = create_color("32m")
    #     orange = create_color("33m")
    #     blue = create_color("34m")
    #     purple = create_color("35m")
    #     cyan = create_color("36m")
    #     lightgrey = create_color("37m")
    #     darkgrey = create_color("90m")
    #     lightred = create_color("91m")
    #     lightgreen = create_color("92m")
    #     yellow = create_color("93m")
    #     lightblue = create_color("94m")
    #     pink = create_color("95m")
    #     lightcyan = create_color("96m")
    #
    # class bg:
    #     """Background Colors."""
    #
    #     black = create_color("40m")
    #     red = create_color("41m")
    #     green = create_color("42m")
    #     orange = create_color("43m")
    #     blue = create_color("44m")
    #     purple = create_color("45m")
    #     cyan = create_color("46m")
    #     lightgrey = create_color("47m")

    class fg:
        """Forderground Colors."""

        black = ANSIControllsBase.esc + "30m"  #:
        red = ANSIControllsBase.esc + "31m"  #:
        green = ANSIControllsBase.esc + "32m"  #:
        orange = ANSIControllsBase.esc + "33m"  #:
        blue = ANSIControllsBase.esc + "34m"  #:
        purple = ANSIControllsBase.esc + "35m"  #:
        cyan = ANSIControllsBase.esc + "36m"  #:
        lightgrey = ANSIControllsBase.esc + "37m"  #:
        darkgrey = ANSIControllsBase.esc + "90m"  #:
        lightred = ANSIControllsBase.esc + "91m"  #:
        lightgreen = ANSIControllsBase.esc + "92m"  #:
        yellow = ANSIControllsBase.esc + "93m"  #:
        lightblue = ANSIControllsBase.esc + "94m"  #:
        pink = ANSIControllsBase.esc + "95m"  #:
        lightcyan = ANSIControllsBase.esc + "96m"  #:

    class bg:
        """Background Colors."""

        black = ANSIControllsBase.esc + "40m"  #:
        red = ANSIControllsBase.esc + "41m"  #:
        green = ANSIControllsBase.esc + "42m"  #:
        orange = ANSIControllsBase.esc + "43m"  #:
        blue = ANSIControllsBase.esc + "44m"  #:
        purple = ANSIControllsBase.esc + "45m"  #:
        cyan = ANSIControllsBase.esc + "46m"  #:
        lightgrey = ANSIControllsBase.esc + "47m"  #:


class ANSIControl(ANSIControllsBase):
    """
    ANSI Cursor movement.

    please make sure your terminal supports these control sequences.
    tested with `GTKTerm:
    <https://circuitpython.readthedocs.io/en/latest/shared-bindings/usb_cdc/index.html>`_

    usage:

    .. code-block:: python

        ANSIControl.erease_line()
        ANSIControl.cursor.up(5)
    """

    # ED =
    erase_display = create_seq("J")
    """
    erase display (ED)

    clear part of screen.

    :param string value:

        * ``0`` (=default): clear from cursor to end of screen.
        * ``1`` : clear from cursor to beginning of screen.
        * ``2`` : clear entire screen. move cursor to 1;1.
        * ``3`` : as 2 and delete all lines in scrollback buffer.
    """

    # EL =
    erase_line = create_seq("K")
    """
    erase line (EL)

    erease part of line.

    :param string value:

        * ``0`` (=default): clear from cursor to end of line.
        * ``1`` : clear from cursor to beginning of line.
        * ``2`` : clear entire line. cursor position does not change.
    """

    # SU =
    scroll_up = create_seq("S")
    """
    scroll up (SU)

    scroll hole page up by n lines. (new lines added at bottom)

    :param string value: lines to scroll up
    """

    # SD =
    scroll_down = create_seq("T")
    """
    scroll down (SD)

    scroll hole page down by n lines. (new lines added at top)

    :param string value: lines to scroll down
    """

    # DSR =
    device_status_report = create_seq("n")("6")
    """
    device status report (DSR)

    request Cursor Position Report (CPR).

    terminal answers / transmitts report:
    ``"ESC[n;mR"``
    ``n`` = row
    ``m`` = column
    """

    # device_status_report_regex = re.compile(r"XXX\[(?P<row>\d*);(?P<column>\d*)R")
    # device_status_report_regex = re.compile(r"\033\[" + r"(\d*);(\d*)R")
    device_status_report_regex = re.compile(r".\[(\d*);(\d*)R")

    @classmethod
    def device_status_report_parse(cls, input_string):
        """
        Parse Device Status Report. (Cursor Position Report / CPR)

        ``"ESC[n;mR"``
        ``n`` = row
        ``m`` = column

        :param string input_string: raw report
        :return (int row, int column): cursor position.
        """
        result = (None, None)
        match = cls.device_status_report_regex.match(input_string)
        if match:
            row, col = match.groups()
            result = (row, col)
        return result

    class cursor:
        """Cursor Movement."""

        # CUU =
        up = create_seq("A")
        """
        cursor up (CUU)

        move cursor n cells up.

        :param string value: cells to move (default: 1)
        """

        # CUD =
        down = create_seq("B")
        """
        cursor down (CUD)

        move cursor n cells down.

        :param string value: cells to move (default: 1)
        """

        # CUF =
        forward = create_seq("C")
        """
        cursor forward (CUF)

        move cursor n cells forward.

        :param string value: cells to move (default: 1)
        """

        back = create_seq("D")
        """
        cursor back (CUB)

        move cursor n cells back.

        :param string value: cells to move (default: 1)
        """

        next_line = create_seq("E")
        """
        cursor next line (CNL)

        move cursor n lines up and to beginning of the line.

        :param string value: lines to move (default: 1)
        """

        previous_line = create_seq("F")
        """
        cursor previous line (CPL)

        move cursor n lines down and to beginning of the line.

        :param string value: lines to move (default: 1)
        """

        horizontal_absolute = create_seq("G")
        """
        cursor horizontal absolute (CHA)

        moves cursor to column n.

        :param string value: column to move to. (default: 1)
        """

        position = create_seq("H")
        """
        cursor position (CUP)

        set cursor position absolute.
        Format: ``"n;m"``
        moves cursor to row n, column m.
        omitted n or m default to 1.

        :param string value: position to move to. (default: "1;1" = top left)
        """


##########################################
# tests


def filter_ansi_controlls(data):
    """
    Remove ANSI controll characters.

    :param string data: input data to filter.
    :return string: filtered result.
    """
    code_list = []
    code_list.extend(ANSIColors.get_flat_list())
    code_list.extend(ANSIControl.get_flat_list())
    for list_entry in code_list:
        data = data.replace(list_entry, "")
    return data


def test_filtering():
    """
    Test for filter_ansi_controlls.

    print some test cases.
    """
    test_string = (
        ANSIColors.fg.lightblue
        + "Hello "
        + ANSIColors.fg.green
        + "World "
        + ANSIColors.fg.orange
        + ":-)"
        + ANSIColors.reset
    )
    print("test_string", test_string)
    test_filtered = filter_ansi_controlls(test_string)
    print("test_filtered", test_filtered)


def test_control():
    """
    Test for control sequences.

    print some test cases.
    """

    test_string = (
        ANSIColors.fg.lightblue
        + "Hello "
        + ANSIColors.fg.green
        + "World "
        + ANSIColors.fg.orange
        + ":-)"
        + ANSIColors.reset
    )
    print("test_string", test_string)
    print("test_string", test_string)
    print("test_string", test_string)
    time.sleep(1)
    test_string = (
        ANSIControl.cursor.previous_line(2)
        + "WOOO"
        + ANSIControl.cursor.next_line(1)
        + ANSIControl.erase_line()
        + ":-)"
    )
    print(test_string)
