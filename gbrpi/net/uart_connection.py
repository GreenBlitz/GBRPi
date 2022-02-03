"""
UART connection class.
(i hate rs232.. all my homies hate rs232)
"""
import struct
from threading import Thread
from typing import List, Optional
import time

import serial

from gbrpi.constants.uart import BAUD_RATE, DEFAULT_ALGO, DOUBLE_SIZE


# noinspection PyUnusedClass
class UART:
    """
    UART connection class.
    """

    def __init__(self, dev_name: str, algo_list: List[str], ping_size: int, baud_rate: int = BAUD_RATE):
        self.conn: serial.Serial = serial.Serial(dev_name, baudrate=baud_rate)
        time.sleep(1)
        self.algo: str = DEFAULT_ALGO
        self.latest_data: Optional[List[int]] = None
        self.algo_list: List[str] = algo_list
        self.handler_map = {
            0: (self.ping_handler, ping_size),
            1: (self.get_handler, 0),
            2: (self.set_algo_handler, 1)
        }
        self.handler_thread: Optional[Thread] = None

    def send_success(self):
        self.conn.write(bytes("\x01", encoding="ascii"))

    def send_fail(self):
        self.conn.write(bytes("\x00", encoding="ascii"))

    # noinspection PyUnusedFunction
    def start_handler_thread(self):
        """
        Starts an asychronous thread which will
        constantly listen to data sent.

        Whenever received data triggers an event,
        the proper function will run.
        """
        self.handler_thread = Thread(target=self.handler)
        self.conn.flushInput()
        self.handler_thread.setName("UART_Listener")
        self.handler_thread.setDaemon(True)
        time.sleep(1)
        self.send_success()
        self.handler_thread.start()
        print("Started listener")

    def handler(self):
        """
        The handler method which is run asynchronously (on a new thread).
        """
        while True:
            # Read byte
            req = self.conn.read()[0]
            # If we have a command that matches this byte
            if req in self.handler_map:
                # Get the matching (command, size) tuple
                curr_handler = self.handler_map[req]
                # If we need to read (the 'size' is not 0)
                if curr_handler[1] != 0:
                    # Then read the data
                    data = self.conn.read(curr_handler[1])
                else:
                    # Otherwise, no bytes
                    data = bytes()
                # Pass the data to the matching function
                curr_handler[0](data)

    def ping_handler(self, data: bytes):
        """
        Send back the data that was received.
        Our ping is a heartbeat packet.

        That means that Motion will send us some random data, and
        we need to send it back to them. They will make a check that
        validates that the same data that was sent, was received.
        That means that we are still alive.

        :param data: The data that we got, and need send back to Motion.
        """
        self.conn.write(data)

    def set_algo_handler(self, data: bytes):
        algo_index: int = data[0]
        if algo_index >= len(self.algo_list):
            self.send_fail()
            return
        self.algo = self.algo_list[algo_index]
        self.send_success()

    def get_handler(self, data: bytes):
        if self.latest_data is None \
                or not isinstance(self.latest_data, list) \
                or len(self.latest_data) != 3:
            self.conn.write(bytes("\x00" * (1 + DOUBLE_SIZE * 3), encoding="ascii"))
            return
        self.send_success()
        for coord in self.latest_data:
            self.conn.write(bytearray(struct.pack(">d", coord)))
