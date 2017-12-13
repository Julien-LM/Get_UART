"""
    File name:  UART.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    25/11/17

    Description: UART library

"""
import serial
import logging

import DefaultsValues
from Interface import Interface


def convert_to_int(data):
    """

    :param data: data from UART
    :type data: unichar
    :return: data converted to int
    :rtype: list of int
    """
    out = []
    for val in data:
        out.append(ord(val))
    return out


class UART:
    """
    Class UART
    """

    def __init__(self, port, baud_rate=19200, parity=serial.PARITY_NONE, stop_bits=serial.STOPBITS_ONE,
                 byte_size=serial.EIGHTBITS, timeout=1, write_timeout=5):

        # get logger
        self.log = logging.getLogger('get_UART')

        # get interface
        self.interface = Interface()

        self.serial_com = None

        self.port = port
        self.baud_rate = baud_rate
        self.parity = parity
        self.stop_bits = stop_bits
        self.byte_size = byte_size
        self.timeout = timeout
        self.write_timeout = write_timeout

    def open_UART(self):
        """
        UART class declaration and ping PIC
        """
        if self.serial_com is None:
            # Open serial port com
            try:
                self.open_serial_com()
            except serial.serialutil.SerialException as e:
                self.log.error("Serial error({0}): {1}".format(e.errno, e.strerror))
            else:
                self.log.info("Serial com port have been initialized successfully")
                if self.is_open():
                    self.log.info("Serial com port is open")
                else:
                    self.log.error("!!! Com port not open !!!")

                # Ping device
                if self.ping_device():
                    self.log.info("Device is right answering")
                else:
                    self.log.warning("Device is offline...")
                    self.log.info("Run a diagnostic for more information")
        else:
            self.log.warning("\n!!!! Serial com have already be declared !!!!")

    def open_serial_com(self):
        """
        Open serial com
        """
        self.serial_com = serial.Serial(
            port=self.port,
            baudrate=self.baud_rate,
            parity=self.parity,
            stopbits=self.stop_bits,
            bytesize=self.byte_size,
            timeout=self.timeout,
            write_timeout=self.write_timeout
        )

    def is_open(self):
        """

        :return: Get the state of the serial port, whether it's open.
        :rtype: bool
        """
        if self.serial_com is not None:
            return self.serial_com.isOpen()
        return False

    def parse_answer(self):
        """
        Parse answer from PIC
        :return: data from PIC
        :rtype: list
        """
        received_thread, received_error = self.read()
        if received_error:
            self.log.error("Issue occurred during serial com read...")
            return []

        # Parse each value received from PIC
        if len(received_thread) > 2:

            # Check for Acknowledge
            if received_thread[0] == DefaultsValues.ACKNOWLEDGE:
                self.log.debug("Acknowledge received")
            elif received_thread[0] == DefaultsValues.NEG_ACKNOWLEDGE:
                self.log.error("Neg Acknowledge received...")
                self.log.error("Relative command: 0x{:02x}".format(received_thread[1]))
                self.log.error("Error code: 0x{:02x}".format(received_thread[2]))
                return []
            else:
                self.log.error("Acknowledge have not been received...")
                return []
        else:
            self.log.error("Received data is not long enough...")
            self.log.error("Required: <=2 obtained: {}".format(len(received_thread)))
            return []

        # Check for line feed
        if received_thread[-1] == DefaultsValues.END_OF_TRANSMIT:
            self.log.debug("End of transmit char received")
        else:
            self.log.error("End of transmit chard have not been received...")
            return []

        # Check for command
        self.log.debug("Received command: 0x{:02x}".format(received_thread[1]))
        if received_thread[1] == DefaultsValues.GET_TEMP:
            if len(received_thread) > DefaultsValues.GET_TEMP_SIZE+2:
                return received_thread[2:4]
            else:
                self.log.error("Get time args to short...")
                return []
        elif received_thread[1] == DefaultsValues.GET_TIME:
            if len(received_thread) > DefaultsValues.GET_TIME_SIZE + 2:
                return received_thread[2:9]
            else:
                self.log.error("Get time args to short...")
                return []
        elif received_thread[1] == DefaultsValues.SET_TIME:
            return True
        elif received_thread[1] == DefaultsValues.CONFIGURE_SENSOR:
            return True
        elif received_thread[1] == DefaultsValues.CLEAN_DATA:
            return True
        elif received_thread[1] == DefaultsValues.GET_DATA_NUMBER:
            return received_thread[2]
        elif received_thread[1] == DefaultsValues.PING:
            return received_thread[2]
        else:
            self.log.error("Unknown command received...")
            return []

    def read(self):
        """
        read serial port since getting end of transmit char
        :return: data, error
        :rtype: list, bool
        """
        read_data = []
        index = 0
        self.log.debug("Start read data:")
        while True:
            try:
                read_data.append(ord(self.serial_com.read()))
                self.log.debug("0x{:02x}".format(read_data[index]))
            except serial.SerialException as e:
                self.log.exception("Serial error({0}): {1}".format(e.errno, e.strerror))
                return read_data, True
            except TypeError:
                self.log.error("Timeout occurred, device did not send anything for 1sec")
                return read_data, True
            if read_data[index] == DefaultsValues.END_OF_TRANSMIT:
                self.log.debug("Number of data received: {}".format(len(read_data)))
                return read_data, False

            index += 1

    def write(self, data):
        """

        :param data: Data to send
        :type data: byte
        :return: number of bytes written
        :rtype: int
        """
        self.log.debug("0x{:02x}".format(data))
        return self.serial_com.write(bytearray.fromhex("{0:02x}".format(data)))

    def ping_device(self):
        """
        Send command to device and check if it is answering well

        :return: return 1 si device answer, 0 if not
        :rtype: bool
        """
        self.log.debug("Ping device")
        if not self.send_UART_command(DefaultsValues.PING):
            return 0
        return True if self.parse_answer() == DefaultsValues.PING else False

    def send_UART_command(self, command, args=None):
        """

        :param command: command ref
        :type command: int
        :param args: to complete command, list of int
        :type args: list
        """
        if args is None:
            args = []
        if self.serial_com is None:
            self.log.error("Com port is not open, do it before sending any command")
            return 0

        self.log.debug("Write data:")
        data_send_count = self.write(command)
        for arg in args:
            data_send_count += self.write(arg)
        data_send_count += self.write(DefaultsValues.END_OF_TRANSMIT)

        if data_send_count > 20:
            self.log.warning("Data send > 20, PIC will probably turn to overflow")

        self.log.debug("Data send: {}".format(data_send_count))
        return 1

    def close_com_port(self):
        """
        Close port com
        """
        self.serial_com.close()
