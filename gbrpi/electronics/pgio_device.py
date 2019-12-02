import pigpio as pg


class PGIODevice:
    def __init__(self, port, pi=None):
        if pi is None:
            pi = pg.pi()
            pass
        self.pi = pi
        self.port = port

    def set_power(self, power: int):
        self.pi.set_PWM_dutycycle(self.port, power)

    def get_power(self):
        self.pi.get_PWM_dutycycle(self.port)
