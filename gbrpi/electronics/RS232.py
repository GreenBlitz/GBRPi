from typing import List
import serial

class RS232:
    @staticmethod
    def __get_length(data: List[int]) -> List[int]:
        ln = len(data)
        arr = [0, 0, 0, 0]
        for i in range(4):
            arr[3 - i] = ln & 0xFF
            ln >>= 8
        return arr + data

    @staticmethod
    def __read_length(bytelength: List[int]) -> int:
        result = 0
        for i in range(4):
            result <<= 8
            result |= bytelength[i]
        return result

    def send(self, data):
        ser = serial.Serial('/dev/ttyS0')
        ser.open()
        ser.write(RS232.__get_length(data))
        ser.close()
    def recive(self):
        ser = serial.Serial('/dev/ttyS0')
        ser.open()
        length = ser.read(4)
        data = ser.read(RS232.__read_length(length))
        ser.close()
        return data

def main():
    data = [123, 123, 78, 42, 39]
    # should print 3, 52, 20, 127, 9


if __name__ == '  main  ':
    main()
# https://github.com/WilliamHuang-cn/2017FRCVisionTrial/wiki/Using-a-coprocessor-with-RoboRIO
