"""
UART connection class.
(i hate rs232.. all my homies hate rs232)
"""
import struct
from threading import Thread
from typing import List, Optional, Union
import time

import serial

from gbrpi.constants.uart import BAUD_RATE, DEFAULT_ALGO, DOUBLE_SIZE


# noinspection PyUnusedClass
class UART:
    """
    UART connection class.
    """

    def __init__(self, dev_name: str, algo_list: List[str], baud_rate: int = BAUD_RATE):
        self.conn: serial.Serial = serial.Serial(dev_name, baudrate=baud_rate)
        time.sleep(1)
        self.algo: str = DEFAULT_ALGO
        self.latest_data: Optional[List[int]] = None
        self.algo_list: List[str] = algo_list
        ping_size: int = 5
        self.handler_map = {
            0: (self.ping_handler, ping_size),
            1: (self.get_handler, 0),
            2: (self.set_algo_handler, 1)
        }
        self.handler_thread: Optional[Thread] = None

    def send_success(self):
        """
        Send byte 0x01.
        """
        self.__write(bytes("\x01", encoding="ascii"))

    def send_fail(self):
        """
        Send byte 0x00.
        """
        self.__write(bytes("\x00", encoding="ascii"))

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
        print("[UART_CONN] Started thread object")

    def handler(self):
        """
        The handler method which is run asynchronously (on a new thread).
        """
        print("[UART_CONN] Handler function started (listener)")
        while True:
            # Read byte
            req = self.__read()
            # If we have a command that matches this byte
            print(f"[UART_CONN] Received data: {req}")
            if req in self.handler_map:
                # Get the matching (command, size) tuple
                curr_handler = self.handler_map[req]
                print(f"[UART_CONN] Identified data as: {curr_handler}")
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
        print(f"[UART_CONN] Pinged with: {data}")
        self.__write(data)

    def set_algo_handler(self, data: bytes):
        """
        Set the current algorithm.

        :param data: The index of the algorithm in the algorithm list to update to.
        """
        algo_index: int = data[0]
        if algo_index >= len(self.algo_list):
            self.send_fail()
            return
        self.algo = self.algo_list[algo_index]
        self.send_success()

    def get_handler(self, data: bytes):
        """
        Writes our latest data to the stream.
        "GET" request.
        """
        # If there are NOT coordinates
        if self.latest_data is None \
                or not isinstance(self.latest_data, list) \
                or len(self.latest_data) != 3:
            # Send a bunch of 0s instead
            self.__write(bytes("\x00" * (1 + DOUBLE_SIZE * 3), encoding="ascii"))
        else:
            # If there ARE coordinates
            # Send success
            self.send_success()
            # For each data point to send
            for coord in self.latest_data:
                # Send it via UART
                self.__write(bytearray(struct.pack(">d", coord)))
                
    def __write(self, data: Union[bytes, bytearray]) -> None:
        """
        Writes data to the serial buffer.
        Wrapper function for writing.
        
        :param data: The data to write to the serial buffer.
        """
        self.conn.flushOutput()
        self.conn.write(data)
    
    def __read(self) -> int:
        """
        Reads 1 byte from the serial buffer and returns the data.
        This is a wrapper function for reading data (for example, to prevent constant buffer flushing).
         
        :return: The data on the buffer.
        """
        self.conn.flushInput()
        return self.conn.read()[0]
