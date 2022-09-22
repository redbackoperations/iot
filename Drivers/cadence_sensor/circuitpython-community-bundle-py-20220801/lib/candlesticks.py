# SPDX-FileCopyrightText: Copyright (c) 2021 Jose David
#
# SPDX-License-Identifier: MIT
"""
`candlesticks`
================================================================================

Graphical representation of the stock movement in candlestick form


* Author(s): Jose David

Implementation Notes
--------------------

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# pylint: disable=too-many-lines, too-many-instance-attributes, too-many-arguments
# pylint: disable=too-many-locals, too-many-statements, invalid-name, too-few-public-methods

import math
import displayio
from vectorio import VectorShape, Rectangle

__version__ = "0.6.2"
__repo__ = "https://github.com/jposada202020/CircuitPython_Candlesticks.git"


class Candlestick:
    """A graphical candlestick representation

    :param int dist_x: number of segments in each bar

    :param int openp: Stock open price
    :param int close: Stock close price
    :param int high: Stock high price
    :param int low: Stock low price

    :param int color_green: When stock close price is higher thant the price opening
     candlestick are representing by a green color. This allows the selection of the
     color of your choice
    :param int color_red: When stock close price is lower thant the price opening
     candlestick are representing by a red color. This allows the selection of the
     color of your choice

    :param int screen_ref: Distance in pixels from the left to the screem to locate
     the candlestick. This allows to present different candlesticks in the same screen


    **Quickstart: Importing and using Candlestick**

    Here is one way of importing the `Candlestick` class so you can use it as
    the name ``my_candle``:

    .. code-block:: python

        from CircuitPython_Candlesticks.candlesticks import Candlestick as Candlestick

    Now you can create a plane at pixel position x=100, open price=60 close price=30
    high price=80 low price=5 using:

    .. code-block:: python

        my_candle = Candlestick(100, 60, 30, 80, 5)

    Once you setup your display, you can now add ``my_candle`` to your display using:

    .. code-block:: python

        display.show(my_plane) # add the group to the display

    If you want to have multiple display elements, you can create a group and then
    append the plane and the other elements to the group.  Then, you can add the full
    group to the display as in this example:

    .. code-block:: python

        my_candle = Candlestick(100, 60, 30, 80, 5)
        my_group = displayio.Group() # make a group
        my_group.append(my_plane) # Add my_plane to the group

        #
        # Append other display elements to the group
        #

        display.show(my_group) # add the group to the display


    **Summary: Cartesian Features and input variables**

    The `Candlestick` class has some options for controlling its position, appearance,
    through a collection of input variables:

        - **position**: ``x``

        - **color**: ``color_green``, ``color_red``


    .. figure:: candlestick.png
      :scale: 90 %
      :alt: Diagram of layout coordinates

      Diagram showing 5 different candlesticks.

    """

    def __init__(
        self,
        dist_x: int,
        openp: int,
        close: int,
        high: int,
        low: int,
        color_green: int = 0x00FF00,
        color_red: int = 0xFF0000,
        screen_ref: int = 180,
    ) -> None:

        self._my_group = displayio.Group()
        self._dist_x = dist_x
        self.bitmap = displayio.Bitmap(high - low, 12, 5)
        self._candlestick_palette = displayio.Palette(2)
        self._candlestick_palette.make_transparent(0)

        self.body_palette = displayio.Palette(2)
        self.body_palette.make_transparent(0)
        if openp > close:
            self.body_palette[1] = color_red
            self._candlestick_palette[1] = color_red
        else:
            self.body_palette[1] = color_green
            self._candlestick_palette[1] = color_green

        if openp > close:
            self._top = openp
            self._bottom = close
        else:
            self._top = close
            self._bottom = openp

        self._high = high
        self._low = low

        self.screen_ref = screen_ref

        self._draw_lines()

    def _draw_lines(self):
        top_line_height = int(math.fabs(self._high - self._top))
        if top_line_height == 0:
            top_line_height = 1

        top_line = VectorShape(
            shape=Rectangle(1, top_line_height),
            pixel_shader=self.body_palette,
            x=self._dist_x,
            y=self.screen_ref - self._high,
        )

        body_height = int(math.fabs(self._top - self._bottom))
        body = VectorShape(
            shape=Rectangle(10, body_height),
            pixel_shader=self.body_palette,
            x=self._dist_x - 5,
            y=self.screen_ref - self._top,
        )

        bottom_line_height = int(math.fabs(self._bottom - self._low))
        if bottom_line_height == 0:
            bottom_line_height = 1

        bottom_line = VectorShape(
            shape=Rectangle(1, bottom_line_height),
            pixel_shader=self.body_palette,
            x=self._dist_x,
            y=self.screen_ref - self._bottom,
        )

        self._my_group.append(top_line)
        self._my_group.append(body)
        self._my_group.append(bottom_line)

        self.my_rep = self._my_group
