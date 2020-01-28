from gbrpi.electronics.gpio_device import GPIODevice
import board
import neopixel
from gbrpi.constants import led_strip

class LedStrip(object):

    def __init__(self):
        self.pixels = neopixel.NeoPixel(led_strip.port, led_strip.amount)
        self.pixels.auto_write = True


    def color_range(self, ports: tuple[int, int], color: tuple[int, int, int]):
        """
        turns the LEDs from index low to high on led strip in color
        """
        low = min(ports[0], led_strip.amount - 1)
        high = min(ports[1], led_strip.amount - 1)
        for i in range(low, high):
            self.color_pixel(i, color)

    def color_pixel(self, loc: int, color: tuple[int, int, int]):
        self.pixels[loc] = color

    def color_jump(self, init_loc: int, jump: int, color: tuple[int, int, int], batch: int = 1):
        while init_loc < led_strip.amount:
            self.color_range((init_loc, init_loc + batch - 1), (color))
            init_loc += jump + batch


    def off(self):
        '''
        turns the led strip off
        '''
        self.color_range((0, led_strip.amount - 1), (0, 0, 0))
