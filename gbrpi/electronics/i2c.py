from typing import List

from smbus2 import SMBus, i2c_msg

class I2C:
    @staticmethod
    def __prep_data(data: List[int]) -> List[int]:
        ln = len(data)
        arr = [0, 0, 0, 0]
        for i in range(4):
            arr[3 - i] = ln & 0xFF
            ln >>= 8
        return arr + data

    @staticmethod
    def __get_read_length(bytelength: List[int]) -> int:
        result = 0
        for i in range(4):
            result <<= 8
            result |= bytelength[i]
        return result

    def __init__(self, input_addr: int, output_addr: int, bus=1, force=False):
        self.force = force
        self.bus = bus
        self.input_addr = input_addr
        self.output_addr = output_addr

    def send(self, data: List[int]):
        """

        """
        data = self.__prep_data(data)
        with SMBus(self.bus, force=self.force) as bus:
            msg = i2c_msg.write(self.output_addr, data)
            bus.i2c_rdwr(msg)

    def receive(self) -> List[int]:
        """

        """
        with SMBus(self.bus, force=self.force) as bus:
            msg = i2c_msg.read(self.input_addr, 4)
            bus.i2c_rdwr(msg)
            length = list(bytes(msg))
            msg_len = self.__get_read_length(list(bytes(msg)))
            msg = i2c_msg.read(self.input_addr, msg_len)
            bus.i2c_rdwr(msg)
            return list(bytes(msg))
