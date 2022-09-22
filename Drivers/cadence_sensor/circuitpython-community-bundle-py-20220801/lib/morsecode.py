# SPDX-FileCopyrightText: Copyright (c) 2021 Jose David M.
#
# SPDX-License-Identifier: MIT
"""
`morsecode`
================================================================================

Circuitpython library to crete Morse code


* Author(s): Jose David M.

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import time
from random import randint
import digitalio

try:
    from typing import List
except ImportError:
    pass


__version__ = "0.2.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_MorseCode.git"


class Emitter:
    """
    Creates a Receiver object
    ex: sreceptor = Emmiter('D13')


    **Quickstart: Importing and using the Emitter**

        Here is an example of using the :class:`Emitter` class.
        First you will need to import the libraries to use it

        .. code-block:: python

            from mc_emitter import Emitter
            import board

        Once this is done you can define your morse code Emitter

        .. code-block:: python

            internal_led = Emitter(board.D13)


        Now you could send phrases to the emitter like so:

        .. code-block:: python

            internal_led.outmorse("Hugo AKA the Architect")

    """

    def __init__(self, pin):
        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.OUTPUT
        self.id = pin  # pylint: disable=invalid-name

    def turnoff(self, pausa: float = 0.1):
        """
        Turns off the Emitter

        :param float pausa: time in seconds for the Emitter to be OFF
        :return: None

        """
        self.pin.value = False
        time.sleep(pausa)

    def turnon(self, pausa: float = 0.1):
        """
        Turns on the Emitter
        :param float pausa: time in seconds for the Emitter to be ON
        :return: None

        """

        self.pin.value = True
        time.sleep(pausa)

    def flashing(self, ontime: float, offtime: float, repeat: int):
        """
        Flash the led according to given parameters

        :param float ontime: time in seconds for the Emitter to be ON
        :param float offtime: time in seconds for the Emitter to be OFF
        :param int repeat: number of repetitions
        :return: None

        """

        for _ in range(repeat):
            self.turnon(ontime)
            self.turnoff(offtime)

    def blinking(self, blinktime: int):
        """

        :param int blinktime: duration in seconds
        :return: None

        """
        self.turnon(blinktime)
        self.turnoff(blinktime)

    def pattern(self, patternl: List[int]) -> None:
        """
        Converts a list of values [0 or 1] to an output in the Emitter

        :param list patternl: list of [0-1] values
        :return: None

        .. code-block:: python

            led = Emitter('D2')
            codigo = [1,1,0,1,0,0,1,1,1,0,0,1,1,1,1,1,0,0,0,1]
            led.pattern(codigo)

        """

        for item in patternl:
            if item == 1:
                self.turnon()
            elif item == 0:
                self.turnoff()
            else:
                continue

    def randomblink(self, iterl: int) -> None:
        """
        Emits a random output to the Emitter

        :param int iterl: number of values to be randomly generated
        :return: None

        """

        self.pattern([randint(0, 1) for _ in range(iterl)])
        self.turnoff()

    @staticmethod
    def convletter(letter: str, final: str) -> str:
        """
        Converts a letter to its representation in morse code

        :param str letter: Letter to be converted
        :param str final: Final character encoding
        :return: string representation in morse code

        """

        morsetabs = {
            "A": ".-",
            "a": ".-",
            "B": "-...",
            "b": "-...",
            "C": "-.-.",
            "c": "-.-.",
            "D": "-..",
            "d": "-..",
            "E": ".",
            "e": ".",
            "F": "..-.",
            "f": "..-.",
            "G": "--.",
            "g": "--.",
            "H": "....",
            "h": "....",
            "I": "..",
            "i": "..",
            "J": ".---",
            "j": ".---",
            "K": "-.-",
            "k": "-.-",
            "L": ".-..",
            "l": ".-..",
            "M": "--",
            "m": "--",
            "N": "-.",
            "n": "-.",
            "O": "---",
            "o": "---",
            "P": ".--.",
            "p": ".--.",
            "Q": "--.-",
            "q": "--.-",
            "R": ".-.",
            "r": ".-.",
            "S": "...",
            "s": "...",
            "T": "-",
            "t": "-",
            "U": "..-",
            "u": "..-",
            "V": "...-",
            "v": "...-",
            "W": ".--",
            "w": ".--",
            "X": "-..-",
            "x": "-..-",
            "Y": "-.--",
            "y": "-.--",
            "Z": "--..",
            "z": "--..",
            "0": "-----",
            ",": "--..--",
            "1": ".----",
            ".": ".-.-.-",
            "2": "..---",
            "?": "..--..",
            "3": "...--",
            ";": "-.-.-.",
            "4": "....-",
            ":": "---...",
            "5": ".....",
            "'": ".----.",
            "6": "-....",
            "-": "-....-",
            "7": "--...",
            "/": "-..-.",
            "8": "---..",
            "(": "-.--.-",
            "9": "----.",
            ")": "-.--.-",
            " ": " ",
            "_": "..--.-",
            "!": "-·-·--",
        }

        convletter = morsetabs[letter]
        convertedletter = ""
        fin = len(convletter) - 1
        for ind, symbol in enumerate(convletter):
            if ind == fin:
                convertedletter = convertedletter + symbol + final
            else:
                convertedletter = convertedletter + symbol + "*"

        return convertedletter

    def convertword(self, word: str) -> str:
        """
        Convert a word to its representation in morse code

        :param word: word string
        :return: string of morse code

        """

        worklist = ""
        fin = len(word) - 1
        for ile, letter in enumerate(word):
            if ile == fin:
                worklist = worklist + self.convletter(letter, "#")
            else:
                worklist = worklist + self.convletter(letter, "|")
        return worklist

    def convertphrase(self, phrase: str) -> List[str]:
        """
        Convert a phrase to a list of words converted to morse code.
        We use a list to allow the library
        do some threading methods

        :param phrase: string to be converted to morse code
        :return: list of words converted to morse code

        """

        phrase = phrase.split(" ")
        phraselist = []
        for word in phrase:
            phraselist.append(self.convertword(word))
        return phraselist

    def outmorse(self, phrase: str, duration: float = 0.1) -> None:
        """
        Plays the morse code

        :param str phrase:
        :param float duration: This value hods the logic of the morse code wpm(words per minute)
         In this case we use 0.1 that means that we use 120/0.12
        :return: None

        """

        codes = self.convertphrase(phrase)
        for word in codes:
            for symbol in word:
                if symbol == "*":
                    self.turnoff(duration)
                elif symbol == ".":
                    self.turnon(duration)
                elif symbol == "-":
                    self.turnon(duration * 3)
                elif symbol == "|":
                    self.turnoff(duration * 3)
                elif symbol == "#":
                    self.turnoff(duration * 7)

    def convertbpm(self, bpm):
        """
        Converts beats per minute in light output

        :param int bpm: Beats per minute
        :return: None

        """

        divider = 60 / bpm
        for _ in range(150):
            self.blinking(divider / 2)
        self.turnoff()

    def __str__(self):
        return r"Sensor is using IO number: {}".format(self.id)
