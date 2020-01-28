from gbrpi.electronics.gpio_device import GPIODevice


class LedStrip(object):

    def __init__(self, r_port, g_port, b_port):
        self.r = GPIODevice(r_port)
        self.g = GPIODevice(g_port)
        self.b = GPIODevice(b_port)


    def on(self, power):
        """
        turns the led strip on in white
        """
        self.r.set_power(power)
        self.g.set_power(power)
        self.b.set_power(power)

    def onRGB(self, color: (int, int, int)):
        '''
        turns the led strip in a specific color
        :param color: RGB of color wanted
        '''

        self.r.set_power(color[0])
        self.g.set_power(color[1])
        self.b.set_power(color[2])


    def off(self):
        '''
        turns the led strip off
        '''
        self.r.set_power(0)
        self.g.set_power(0)
        self.b.set_power(0)
