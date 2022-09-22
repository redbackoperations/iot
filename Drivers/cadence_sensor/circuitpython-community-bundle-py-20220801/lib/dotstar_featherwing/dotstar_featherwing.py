# The MIT License (MIT)
#
# Copyright (c) 2017 Dave Astels
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
"""
`dotstar_featherwing` - CircuitPython support for the 6x12 DotStar FeatherWing
====================================================

Provides a simple way to use the DotStar Feather Wing to display text, images, and animation.

* Author(s): Dave Astels
"""

import board
import adafruit_dotstar
import time

class DotstarFeatherwing(object):
	"""Test, Image, and Animation support for the DotStar featherwing"""

	blank_stripe = [(0, 0, 0),
					(0, 0, 0),
					(0, 0, 0),
					(0, 0, 0),
					(0, 0, 0),
					(0, 0, 0)]
	"""A blank stripe, used internally to separate characters as they are shifted onto the display."""
	
	def __init__(self, clock, data, brightness=1.0):
		"""Create an interface for the display.

		   :param pin clock: The clock pin for the featherwing
		   :param pin data: The data pin for the featherwing
		   :param float brightness: Optional brightness (0.0-1.0) that defaults to 1.0
		"""
		self.rows = 6
		self.columns = 12
		self.display = adafruit_dotstar.DotStar(clock, data, self.rows * self.columns, brightness, False)
			  

	def clear(self):
		"""Clear the display.
		   Does NOT update the LEDs
		"""
		self.display.fill((0,0,0))


	def fill(self, color):
		"""Fills the wing with a color.
		   Does NOT update the LEDs.

		   :param (int, int, int) color: the color to fill with
		"""
		self.display.fill(color)


	def show(self):
		"""Update the LEDs.
		"""
		self.display.show()


	def set_color(self, row, column, color):
		"""Set the color of the specified pixel.

		   :param int row: The row (0-5) of the pixel to set
		   :param int column: The column (0-11) of the pixel to set
		   :param (int, int, int) color: The color to set the pixel to
		"""
		self.display[row * self.columns + column] = color
		
		
	def shift_into_left(self, stripe):
		""" Shift a column of pixels into the left side of the display.

			:param [(int, int, int)] stripe: A column of pixel colors. The first at the top.
		"""
		for r in range(self.rows):
			rightmost = r * self.columns
			for c in range(self.columns - 1):
				self.display[rightmost + c] = self.display[rightmost + c + 1]
			self.display[rightmost + self.columns - 1] = stripe[r]


	def shift_into_right(self, stripe):
		""" Shift a column of pixels into the rightside of the display.

			:param [(int, int, int)] stripe: A column of pixel colors. The first at the top.
		"""
		for r in range(self.rows):
			leftmost = ((r + 1) * self.columns) - 1
			for c in range(self.columns - 1):
				self.display[leftmost - c] = self.display[(leftmost - c) -1]
			self.display[(leftmost - self.columns) + 1] = stripe[r]
				

	def number_to_pixels(self, x, color):
		"""Convert an integer (0..63) into an array of 6 pixels.

		   :param int x: integer to convert into binary pixel values; LSB is topmost.
		   :param (int, int, int) color: the color to set "on" pixels to
		"""
		val = x
		pixels = []
		for b in range(self.rows):
			if val & 1 == 0:
				pixels.append((0, 0, 0))
			else:
				pixels.append(color)
			val = val >> 1
		return pixels
			

	def character_to_numbers(self, font, char):
		"""Convert a letter to the sequence of column values to display.

		   :param {char -> [int]} font: the font to use to convert characters to glyphs
		   :param char letter: the char to convert
		"""
		return font[char]


	def shift_in_character(self, font, c, color=(0x00, 0x40, 0x00), delay=0.2):
		"""Shifts a single character onto the display from the right edge.

		   :param {char -> [int]} font: the font to use to convert characters to glyphs
		   :param char c: the char to convert
		   :param (int, int, int) color: the color to use for each pixel turned on
		   :param float delay: the time to wait between shifting in columns
		"""
		if c.upper() in font:
			matrix = self.character_to_numbers(font, c.upper())
		else:
			matrix = self.character_to_numbers(font, 'UNKNOWN')
		for stripe in matrix:
			self.shift_into_right(self.number_to_pixels(stripe, color))
			self.show()
			time.sleep(delay)
		self.shift_into_right(self.blank_stripe)
		self.show()
		time.sleep(delay)


	def shift_in_string(self, font, s, color=(0x00, 0x40, 0x00), delay=0.2):
		"""Shifts a string onto the display from the right edge.

		   :param {char -> [int]} font: the font to use to convert characters to glyphs
		   :param string s: the char to convert
		   :param (int, int, int)) color: the color to use for each pixel turned on
		   :param float delay: the time to wait between shifting in columns
		"""
		for c in s:
			self.shift_in_character(font, c, color, delay)

		
	# Display an image
	def display_image(self, image, color):
		"""Display an mono-colored image.

		   :param [string] image: the textual bitmap, 'X' for set pixels, anything else for others
		   :param (int) color: the color to set "on" pixels to
		"""
		self.display_colored_image(image, {'X': color})
							

	def display_colored_image(self, image, colors):
		"""Display an multi-colored image.

		   :param [string] image: the textual bitmap, character are looked up in colors for the 
				  corresponding pixel color, anything not in the map is off
		   :param {char -> (int, int, int)} colors: a map of characters in the image data to colors to use
		"""
		for r in range(self.rows):
			for c in range(self.columns):
				index = r * self.columns + ((self.columns - 1) - c)
				key = image[r][c]
				if key in colors:
					self.display[index] = colors[key]
				else:
					self.display[index] = (0, 0, 0)
		self.display.show()
							

	def display_animation(self, animation, colors, count=1, delay=0.1):
		"""Display a multi-colored animation.

		   :param [[string]] animation: a list of textual bitmaps, each as described in display_colored_image
		   :param {char -> (int, int, int)} colors: a map of characters in the image data to colors to use
		   :param int count: the number of times to play the animation
		   :param float delay: the amount of time (seconds) to wait between frames
		"""
		self.clear()
		first_frame = True
		while count > 0:
			for frame in animation:
				if not first_frame:
					time.sleep(delay)
				first_frame = False
				self.display_colored_image(frame, colors)
			count = count - 1
					




