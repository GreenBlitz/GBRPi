"""
UART connection class.
(i hate rs232.. all my homies hate rs232)
"""
import serial
import struct
import time
from inspect import stack
from threading import Thread
from typing import List, Optional, Union, Iterable

from gbrpi.constants.uart import BAUD_RATE, DEFAULT_ALGO, DOUBLE_SIZE, PING_SIZE


# noinspection PyUnusedClass
class UART:
    """
    UART connection class.
    """

    def __init__(self, dev_name: str, algo_list: List[str], baud_rate: int = BAUD_RATE):
        self.__conn: serial.Serial = serial.Serial(dev_name, baudrate=baud_rate)
        time.sleep(1)
        self.__latest_data: Optional[Iterable[int]] = None
        self.algo: str = DEFAULT_ALGO
        self.algo_list: List[str] = algo_list
        self.__handler_map = {
            0: (self.__ping_handler, PING_SIZE),
            1: (self.__get_handler, 0),
            2: (self.__set_algo_handler, 1)
        }
        self.__handler_thread: Optional[Thread] = None

    # API function
    # noinspection PyUnusedFunction,PySameParameterValue
    def update_data(self, updated_data: Optional[Iterable[int]]) -> None:
        """
        Update the last data sent.

        The way that our system works is that the data is cached here on the RPI.
        Only if the RoboRIO requests this data, then it is sent to it.
        If there is a surplus of information, then we update the information with
        the most updated data to send.
        """
        self.__latest_data = updated_data

    # API function
    # noinspection PyUnusedFunction
    def send_fail(self) -> None:
        """
        Sends a fail status code via UART.
        External API wrapper.
        """
        # Send the fail
        self.__send_fail()
        # Update the last data
        self.update_data(None)

    def __send_success(self):
        """
        Send byte 0x01.
        """
        self.__write(bytes("\x01", encoding="ascii"))

    def __send_fail(self):
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
        self.__handler_thread = Thread(target=self.__handler)
        self.__conn.reset_input_buffer()
        self.__conn.reset_output_buffer()
        self.__handler_thread.setName("UART_Listener")
        self.__handler_thread.setDaemon(True)
        time.sleep(1)
        self.__handler_thread.start()
        print("[UART_CONN] Started thread object")

    def __handler(self):
        """
        The handler method which is run asynchronously (on a new thread).
        """
        print("[UART_CONN] Handler function started (listener)")
        while True:
            # Read single byte
            req = self.__read()[0]
            # If we have a command that matches this byte
            print(f"[UART_CONN] Received command: {req}")
            if req in self.__handler_map:
                # Get the matching (command, size) tuple
                curr_handler = self.__handler_map[req]
                print(f"[UART_CONN] Identified command as: {curr_handler[0]}")
                # If we need to read (the 'size' is not 0)
                if curr_handler[1] != 0:
                    # Then read the data
                    data = self.__read(curr_handler[1])
                else:
                    # Otherwise, no bytes
                    data = bytes()
                # Pass the data to the matching function
                curr_handler[0](data)

    def __ping_handler(self, data: bytes):
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

    def __set_algo_handler(self, data: bytes):
        """
        Set the current algorithm.

        :param data: The index of the algorithm in the algorithm list to update to.
        """
        algo_index: int = data[0]
        if algo_index >= len(self.algo_list):
            self.__send_fail()
            return
        self.algo = self.algo_list[algo_index]
        self.__send_success()

    # noinspection PyUnusedLocal
    def __get_handler(self, data: bytes):
        """
        Writes our latest data to the stream.
        "GET" request.
        """
        # If there are NOT coordinates
        if self.__latest_data is None \
                or not isinstance(self.__latest_data, Iterable) \
                or len(self.__latest_data) != 3:
            # Send a bunch of 0s instead
            self.__write(bytes("\x00" * (1 + DOUBLE_SIZE * 3), encoding="ascii"))
        else:
            # If there ARE coordinates
            # Send success
            self.__send_success()
            # For each data point to send
            for coord in self.__latest_data:
                # Send it via UART
                self.__write(bytearray(struct.pack(">d", coord)))
                
    def __write(self, data: Union[bytes, bytearray]) -> None:
        """
        Writes data to the serial buffer.
        Wrapper function for writing.
        
        :param data: The data to write to the serial buffer.
        """
        # Debugging info
        debug_stack = stack()
        print(f"[UART_CONN] Wrote the following data (from "
              f"{' -> '.join([debug_stack[i][3] for i in range(len(debug_stack))])}): {data}")
        # Flush and write
        self.__conn.reset_output_buffer()
        self.__conn.write(data)
    
    def __read(self, read_size: int = 1) -> Optional[bytes]:
        """
        Reads 1 byte from the serial buffer and returns the data.
        This is a wrapper function for reading data (for example, to prevent constant buffer flushing).
         
        :return: The data on the buffer.
        """
        # Read the data
        read_data = self.__conn.read(read_size)
        # Debug stuff
        debug_stack = stack()
        print(f"[UART_CONN] Read the following data of size {read_size} "
              f"(from {' -> '.join([debug_stack[i][3] for i in range(len(debug_stack))])}): {read_data}")
        # Return the data
        return read_data
