from typing import Tuple

from gbrpi.electronics.gpio_device import GPIODevice


class LedStrip:

    def __init__(self, port, amount):
        self.port = port
        self.amount = amount
        try:
            import board
            import neopixel
        except ImportError:
            import sys
            print("You do not have the neopixel module installed, please install it in order to use the led strip",
                  file=sys.stderr)
            return
        self.pixels = neopixel.NeoPixel(port, amount)
        self.pixels.auto_write = True

    def color_range(self, low: int, high: int, color: Tuple[int, int, int]):
        """
        turns the LEDs from index low to high on led strip in color
        """
        low = min(low, self.amount - 1)
        high = min(high, self.amount - 1)
        for i in range(low, high):
            self.color_pixel(i, color)

    def color_pixel(self, loc: int, color: Tuple[int, int, int]):
        self.pixels[loc] = color

    def color_jump(self, init_loc: int, jump: int, color: Tuple[int, int, int], batch: int = 1):
        while init_loc < self.amount:
            self.color_range(init_loc, init_loc + batch - 1, color)
            init_loc += jump + batch

    def off(self):
        """
        turns the led strip off
        """
        self.color_range(0, self.amount - 1, (0, 0, 0))
