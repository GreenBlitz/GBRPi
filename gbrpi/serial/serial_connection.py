import abc
import struct

from gbrpi.constants.types import SerialData, Primitive, FixedSizePrimitive
import numpy as np


class SerialConnection(abc.ABC):
    class _Message:
        BIG_ENDIAN = '>'
        LITTLE_ENDIAN = '<'

        def __init__(self):
            self.message = bytearray()

        def finalize(self) -> bytes:
            return bytes(self.message)

        def append_raw(self, data: SerialData) -> 'SerialConnection._Message':
            self.message += data
            return self

        def append_string(self, string: str, encoding: str = "ascii"):
            return self.append_raw(bytearray(string, encoding=encoding))

        def append_ascii_string(self, string: str):
            return self.append_string(string)

        def append_primitive(self, value: FixedSizePrimitive, format_type: str, is_big_endian: bool = True):
            if is_big_endian:
                endian_str = SerialConnection._Message.BIG_ENDIAN
            else:
                endian_str = SerialConnection._Message.LITTLE_ENDIAN
            return self.append_raw(bytearray(struct.pack(endian_str + format_type, value)))

        def append_double(self, double: float, is_big_endian: bool = True):
            return self.append_primitive(double, 'd', is_big_endian)

        def append_float(self, fl: float, is_big_endian: bool = True):
            return self.append_primitive(fl, 'f', is_big_endian)

        def append_integer(self, integer: int, is_big_endian: bool = True):
            return self.append_primitive(integer, 'i', is_big_endian)

        def append_byte(self, byte: int, is_big_endian: bool = True):
            return self.append_primitive(byte, 'b', is_big_endian)

        def append_boolean(self, boolean: bool, is_big_endian: bool = True):
            if boolean:
                return self.append_byte(1, is_big_endian)
            return self.append_byte(0, is_big_endian)

        def append_long(self, long: int, is_big_endian: bool = True):
            return self.append_primitive(long, 'l', is_big_endian)

        def append(self, data, is_big_endian: bool = True):
            data_type = type(data)
            if data_type is str:
                return self.append_string(data)
            if data_type is bytearray or data_type is bytes:
                return self.append_raw(data)
            if data_type is np.float32:
                return self.append_float(data.value, is_big_endian=is_big_endian)
            if data_type is np.float64:
                return self.append_double(data.value, is_big_endian=is_big_endian)
            if data_type is float:
                return self.append_double(data, is_big_endian=is_big_endian)
            if data_type is int:
                return self.append_integer(data, is_big_endian=is_big_endian)
            if data_type is np.int32:
                return self.append_integer(data.value, is_big_endian=is_big_endian)
            if data_type is np.int64:
                return self.append_long(data.value, is_big_endian=is_big_endian)
            raise TypeError(f'Unable to convert type `{data_type}` to raw format')

    @abc.abstractmethod
    def receive(self, amount: int, timeout: int = None) -> bytes:
        """
        reads `amount` bytes from the serial port and returns them in raw format
        :param amount: amount of bytes
        :param timeout: timeout in millis, None is no timeout
        :return:
        """

    @abc.abstractmethod
    def _send(self, data: bytes):
        pass

    def send(self, data):
        """
        sends the data to the serial port
        :param data:
        :return:
        """
        self._send(self._Message().append(data).finalize())
