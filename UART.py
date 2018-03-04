# coding=utf-8
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
from PICom import PICom


class UART(object):
    """
    Class UART
    """

    def __init__(self, port, baud_rate=19200, parity=serial.PARITY_NONE, stop_bits=serial.STOPBITS_ONE,
                 byte_size=serial.EIGHTBITS, timeout=1, write_timeout=5):

        # get logger
        self.log = logging.getLogger('get_UART')

        # get interface
        self.interface = Interface()

        # Get PICom
        self.pic_com = PICom()

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
                self.ping_device()
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

    def parse_answer(self, command, first_read):
        """
        Parse answer from PIC
        :return: data from PIC
        :rtype: list
        """

        received_thread, received_error = self.read(first_read)
        if received_error:
            self.log.error("Issue occurred during serial com read...")
            return []

        if not received_thread:
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
            first_read = False
        else:
            self.log.error("End of transmit chard have not been received...")
            return []

        # Check right command received
        if command != DefaultsValues.GET_REAL_TIME_INFO:
            # Get real time info send many data, as time, temp, nb value...
            if command != DefaultsValues.GET_TEMP:
                # Get temp also send nb data
                if command != received_thread[1]:
                    self.log.error("Received command doesn't match with sent one")
                    return []

        # Check for command
        self.log.debug("Received command: 0x{:02x}".format(received_thread[1]))

        # Extract data from received thread
        received_data = received_thread[2:(len(received_thread)-1)]

        # If GET_TEMP
        if received_thread[1] == DefaultsValues.GET_TEMP:
            return self.pic_com.get_temp_parsing(received_data)
        # If GET_TIME
        elif received_thread[1] == DefaultsValues.GET_TIME:
            return self.pic_com.get_time_parsing(received_data)
        # If SET_TIME
        elif received_thread[1] == DefaultsValues.SET_TIME:
            return self.pic_com.set_time_parsing()
        # If CONFIGURE_SENSOR
        elif received_thread[1] == DefaultsValues.CONFIGURE_SENSOR:
            return self.pic_com.config_sensor_parsing(received_data)
        # If CLEAN_DATA
        elif received_thread[1] == DefaultsValues.CLEAN_DATA:
            return self.pic_com.clean_data_parsing()
        # If GET_DATA_NUMBER
        elif received_thread[1] == DefaultsValues.GET_DATA_NUMBER:
            return self.pic_com.get_data_number_parsing(received_data)
        # If PING
        elif received_thread[1] == DefaultsValues.PING:
            return received_data[0]
        # If GET_REAL_TIME_INFO
        elif received_thread[1] == DefaultsValues.GET_REAL_TIME_INFO:
            return self.pic_com.get_real_time_info(received_data)
        # If GET_DEBUG_VALUES
        elif received_thread[1] == DefaultsValues.GET_DEBUG_VALUES:
            return self.pic_com.get_debug_value_parsing(received_data)
        # Unknown command...
        else:
            self.log.error("Unknown command received...")
            return []

    def read(self, first_read=True):
        """
        read serial port since getting end of transmit char
        :rtype: list, bool
        :return: data, error
        """
        read_data = []
        index = 0
        if first_read:
            self.log.debug("Start read data:")
        while True:
            try:
                read_data.append(ord(self.serial_com.read()))
                self.log.debug("nb: {}  0x{:02x}".format(index, read_data[index]))
            except serial.SerialException as e:
                self.log.exception("Serial error({0}): {1}".format(e.errno, e.strerror))
                return read_data, True
            except TypeError:
                if first_read:
                    self.log.error("Timeout occurred, device did not send anything for 1sec")
                    return read_data, True
                else:
                    return [], False
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
        return self.pic_com.ping_parsing(self.send_UART_command(DefaultsValues.PING))

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

        self.log.debug("Data sent: {}".format(data_send_count))
        return self.parse_multi_answer(command)

    def parse_multi_answer(self, command):
        """
        Check multi thread from PIC
        :param command:
        :type command:
        :return:
        :rtype:
        """
        return_list = [self.parse_answer(command, True)]

        while True:
            return_list.append(self.parse_answer(command, False))
            if not return_list[-1]:
                break
        if len(return_list) == 2:
            return return_list[0]
        else:
            return return_list

    def close_com_port(self):
        """
        Close port com
        """
        self.serial_com.close()
