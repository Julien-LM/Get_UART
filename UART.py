"""
    File name:  UART.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    25/11/17

    Description: UART library

"""
import serial

import DefaultsValues
from Interface import Interface


class UART:
    """
    Class UART
    """

    def __init__(self, logger, port, baud_rate=9600, parity=serial.PARITY_NONE, stop_bits=serial.STOPBITS_ONE,
                 byte_size=serial.EIGHTBITS, timeout=1, write_timeout=1):

        # get logger
        self.log = logger

        # get interface
        self.interface = Interface(self.log)

        self.serial_com = None

        self.port = port
        self.baud_rate = baud_rate
        self.parity = parity
        self.stop_bits = stop_bits
        self.byte_size = byte_size
        self.timeout = timeout
        self.write_timeout = write_timeout

    def open_UART(self, log_interface=True):
        """
        UART class declaration and ping PIC
        """
        if self.serial_com is None:
            # Open serial port com
            try:
                self.open_serial_com()
            except serial.serialutil.SerialException as e:
                self.log.error("Serial error({0}): {1}".format(e.errno, e.strerror))
                if log_interface:
                    self.interface.interface_selection()
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
                self.log.info("Device is offline...")
                self.log.info("Run a diagnostic for more information")
                if log_interface:
                    self.interface.interface_selection()
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
        return self.serial_com.isOpen()

    def parse_answer(self):
        """
        Parse answer from PIC
        :return: data from PIC
        :rtype: int
        """
        received_thread = self.read()
        if received_thread == '':
            self.log.error("No value read on serial port")
            return 0
        # Parse each value received from PIC
        for val in received_thread:
            if val == DefaultsValues.ACKNOWLEDGE:
                self.log.debug("Acknowledge received")
            self.log.debug("0x{:02x}".format(ord(val)))

        # Check for Acknowledge
        if received_thread[0] == DefaultsValues.ACKNOWLEDGE:
            self.log.debug("Acknowledge received")
        elif received_thread[0] == DefaultsValues.NEG_ACKNOWLEDGE:
            self.log.error("Neg Acknowledge received...")
            self.log.error("Relative command: 0x{:02x}".format(ord(received_thread[1])))
            self.log.error("Error code: 0x{:02x}".format(ord(received_thread[2])))
            return 0
        else:
            self.log.error("Acknowledge have not been received...")
            return 0

        # Check for line feed
        if received_thread[-1] == DefaultsValues.LINE_FEED:
            self.log.debug("Line feed received")
        else:
            self.log.error("Line feed have not been received...")
            return 0

        # Check for command
        self.log.debug("Received command: 0x{:02x}".format(ord(received_thread[1])))
        if received_thread[1] == DefaultsValues.GET_TEMP:
            return received_thread[2:4]
        elif received_thread[1] == DefaultsValues.GET_TIME:
            return received_thread[2:8]
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
            return 0

    def read(self):
        """
        fd
        """
        try:
            read_data = self.serial_com.readline()
        except serial.SerialException as e:
            self.log.error("Serial error({0}): {1}".format(e.errno, e.strerror))
            return -1

        if read_data == '':
            self.log.error("Timeout occurred, device did not send anything for 1sec")

        return read_data

    def write(self, data):
        """

        :param data: Data to send
        :type data: String
        :return: number of bytes written
        :rtype: int
        """
        return self.serial_com.write(data)

    def ping_device(self):
        """
        Send command to device and check if it is answering well

        :return: return 1 si device answer, 0 if not
        :rtype: bool
        """

        if not self.send_UART_command(DefaultsValues.PING):
            return 0
        return True if self.parse_answer() == DefaultsValues.PING else False

    def send_UART_command(self, command, args=None):
        """

        :param command: command ref
        :type command: int
        :param args: args relative to command
        :type args: list
        """
        if args is None:
            args = []
        if self.serial_com is None:
            self.log.error("Com port is not open, do it before sending any command")
            return 0

        data_send_count = self.write(command)
        for arg in args:
            data_send_count += self.write(arg)
        data_send_count += self.write(DefaultsValues.LINE_FEED)

        if data_send_count > 20:
            self.log.warning("Data send > 20, PIC will probably turn to overflow")

        self.log.debug("Data send: {}".format(data_send_count))
        return 1

    def close_com_port(self):
        """
        Close port com
        """
        self.serial_com.close()
