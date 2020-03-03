import abc
import struct
from typing import List

import serial

from gbrpi.serial.serial_connection import SerialConnection


class UARTConnection(SerialConnection):
    DEFAULT_BAUD_RATE = 115200

    def __init__(self, dev_name: str, baud_rate: int = DEFAULT_BAUD_RATE):
        self.conn: serial.Serial = serial.Serial(dev_name, baudrate=baud_rate)
