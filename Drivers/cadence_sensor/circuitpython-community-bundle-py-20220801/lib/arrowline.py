# SPDX-FileCopyrightText: Copyright (c) 2021 Jose David
#
# SPDX-License-Identifier: MIT
"""
`arrowline`
================================================================================

Utility function to draw arrow lines using vectorio and tilegride to display it


* Author(s): Jose David M

Implementation Notes
--------------------

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# pylint: disable=too-many-lines, too-many-instance-attributes, too-many-arguments
# pylint: disable=too-many-locals, too-many-statements, invalid-name

import math
import displayio
from vectorio import VectorShape, Polygon, Circle

__version__ = "0.8.3"
__repo__ = "https://github.com/jposada202020/CircuitPython_ArrowLine.git"


def line_arrow(
    grid=None,
    x1=0,
    y1=0,
    x2=10,
    y2=10,
    arrow_length=10,
    palette=None,
    pal_index=1,
    line_width=1,
    pointer="A",
):
    """A Line Arrow utility.

    :param grid: Tilegrid object where the bitmap will be located, set to None for
     arbitrary placement of the `line_arrow` (default = None)

    :param int x1: line first point x coordinate
    :param int y1: line first point x coordinate
    :param int x2: line first point x coordinate
    :param int y2: line first point x coordinate

    :param int arrow_length: arrow length in pixels. Arrow width is half of the length

    :param `displayio.Palette` palette: palette object used to display the bitmap.
     This is used to utilize the same color for the arrow
    :param int pal_index: pallet color index used in the bitmap to give the arrow line the color
     property
    :param int line_width: the width of the arrow's line, in pixels (default = 1)

    :param str pointer: point type. Two pointers could be selected :const:`C` Circle
     or :const:`A` Arrow. Defaults to Arrow

    :return: `vectorio` VectorShape object to be added to the displayio group


    **Quickstart: Importing and using line_arrow**

        Here is one way of importing the `line_arrow` function so you can use:

        .. code-block:: python

            import displayio
            import board
            from CircuitPython_ArrowLine import line_arrow
            display = board.DISPLAY
            my_group = displayio.Group()
            bitmap = displayio.Bitmap(100, 100, 5)
            screen_palette = displayio.Palette(3)
            screen_palette[1] = 0x00AA00
            screen_tilegrid = displayio.TileGrid(
                bitmap,
                pixel_shader=screen_palette,
                x=50,
                y=50,
            )
            my_group.append(screen_tilegrid)

        Now you can create an arrowline starting at pixel position x=40, y=90 using:

        .. code-block:: python

            my_line = line_arrow(screen_tilegrid, bitmap, 40, 90, 90, 60, 12, screen_palette, 1)

        Once you setup your display, you can now add ``my_line`` to your display using:

        .. code-block:: python

            my_group.append(line)
            display.show(my_group)


    **Summary: `arrowline Features and input variables**

        The `line_arrow` widget has some options for controlling its position, visible appearance,
        and scale through a collection of input variables:

            - **position**: :const:`x1`, :const:`y1`, :const:`x2`, :const:`y2`

            - **size**: line length is given by two points. :const:`arrow_length`

            - **color**: :const:`pal_index`

            - **background color**: :const:`background_color` gfdgfd

    """

    if palette is None:
        raise Exception("Must provide a valid palette")

    my_group = displayio.Group()

    angle = math.atan2((y2 - y1), (x2 - x1))
    x0 = int(math.ceil(arrow_length * math.cos(angle)))
    y0 = int(math.ceil(arrow_length * math.sin(angle)))

    angle2 = math.pi / 2 - angle
    arrow_side_x = arrow_length // 2 * math.cos(angle2)
    arrow_side_y = arrow_length // 2 * math.sin(angle2)

    if grid is not None:
        x_reference = grid.x
        y_reference = grid.y
    else:
        x_reference = 0
        y_reference = 0

    start_x = x_reference + x2
    start_y = y_reference + y2

    arrow_base_x = start_x - x0
    arrow_base_y = start_y - y0

    end_line_x = x2 - x0
    end_line_y = y2 - y0
    line_draw = _angledrectangle(x1, y1, end_line_x, end_line_y, stroke=line_width)

    right_x = math.ceil(arrow_base_x + arrow_side_x)
    right_y = math.ceil(arrow_base_y - arrow_side_y)

    left_x = math.ceil(arrow_base_x - arrow_side_x)
    left_y = math.ceil(arrow_base_y + arrow_side_y)

    arrow_palette = displayio.Palette(2)
    arrow_palette.make_transparent(0)
    arrow_palette[1] = palette[pal_index]

    line_base = Polygon(
        points=[
            (x_reference + line_draw[0][0], y_reference + line_draw[0][1]),
            (x_reference + line_draw[1][0], y_reference + line_draw[1][1]),
            (x_reference + line_draw[2][0], y_reference + line_draw[2][1]),
            (x_reference + line_draw[3][0], y_reference + line_draw[3][1]),
        ]
    )
    line_vector_shape = VectorShape(
        shape=line_base,
        pixel_shader=arrow_palette,
        x=0,
        y=0,
    )
    my_group.append(line_vector_shape)

    if pointer == "A":
        arrow = Polygon(
            points=[(start_x, start_y), (right_x, right_y), (left_x, left_y)]
        )
        arrow_vector_shape = VectorShape(
            shape=arrow,
            pixel_shader=arrow_palette,
            x=0,
            y=0,
        )
        my_group.append(arrow_vector_shape)

    elif pointer == "C":
        circle_center_x = x_reference + line_draw[2][0]
        circle_center_y = y_reference + line_draw[2][1]

        circle_ending = Circle(3)
        circle_vector_shape = VectorShape(
            shape=circle_ending,
            pixel_shader=arrow_palette,
            x=circle_center_x,
            y=circle_center_y,
        )
        my_group.append(circle_vector_shape)

    return my_group


def _angledrectangle(x1, y1, x2, y2, stroke=1):
    # Code Source for this function by kmatch98 (R) 2021
    # https://github.com/adafruit/CircuitPython_Community_Bundle/pull/63
    if x2 - x1 == 0:
        xdiff1 = round(stroke / 2)
        xdiff2 = -round(stroke - xdiff1)
        ydiff1 = 0
        ydiff2 = 0

    elif y2 - y1 == 0:
        xdiff1 = 0
        xdiff2 = 0
        ydiff1 = round(stroke / 2)
        ydiff2 = -round(stroke - ydiff1)

    else:
        c_dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        xdiff = stroke * (y2 - y1) / c_dist
        xdiff1 = round(xdiff / 2)
        xdiff2 = -round(xdiff - xdiff1)

        ydiff = stroke * (x2 - x1) / c_dist
        ydiff1 = round(ydiff / 2)
        ydiff2 = -round(ydiff - ydiff1)

    return [
        (x1 + xdiff1, y1 + ydiff2),
        (x1 + xdiff2, y1 + ydiff1),
        (x2 + xdiff2, y2 + ydiff1),
        (x2 + xdiff1, y2 + ydiff2),
    ]
