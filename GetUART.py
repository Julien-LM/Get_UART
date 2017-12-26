#!/usr/bin/env python
# coding=utf-8
"""
    File name:  getUART.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    25/11/17

    Description: Script to get data through UART

    UART thread from python scipt:
    |CMD|ARGS or not|LINE_FEED

    Regular answer from PIC
    |ACK|CMD|DATA|LINE_FEED

    Error answer from PIC
    |nACK|CMD|Error_code|LINE_FEED

"""

import sys
import time
import logging

import DefaultsValues
from Init import Init
from Interface import Interface
from UART import UART
from Interface import System


class Main(object):
    """
    Class Main
    """

    def __init__(self, argv):

        # init, initialization class
        self.init = Init(argv)

        # Get logger from Init class
        self.log = logging.getLogger('get_UART')

        # Serial com variable definition
        self.serial_com = UART(port=self.init.get_serial_port())

        # System class
        self.system = System()

        # Is UART init a program beginning
        self.init_UART_bit = self.init.get_init_UART_bit()

        # Define interface class
        self.interface = Interface()

    def main(self):
        """
        Main script function
        """
        if self.init_UART_bit:
            self.serial_com.open_UART()

        while True:
            self.interface.log_main_page()

            # get keyboard input
            keyboard_input = self.interface.get_input_char
            if keyboard_input == '0' or keyboard_input == 'connect':
                self.serial_com.open_UART()
            elif keyboard_input == '1' or keyboard_input == 'temp':
                self.get_temp()
            elif keyboard_input == '2' or keyboard_input == 'time':
                self.get_time()
            elif keyboard_input == '3' or keyboard_input == 'set_time':
                self.set_time()
            elif keyboard_input == '4' or keyboard_input == 'configure':
                self.config_sensor()
            elif keyboard_input == '5' or keyboard_input == 'clean':
                self.clean_data()
            elif keyboard_input == '9' or keyboard_input == 'log_time':
                self.system.log_time()
            elif keyboard_input == 'p' or keyboard_input == 'ping':
                self.serial_com.send_UART_command(DefaultsValues.PING)
            elif keyboard_input == 'r' or keyboard_input == 'recover':
                self.recover_overflow()
            elif keyboard_input == 'i' or keyboard_input == 'info':
                self.serial_com.send_UART_command(DefaultsValues.GET_REAL_TIME_INFO)
            elif keyboard_input == 'exit' or keyboard_input == 'q':
                exit(0)
            else:
                self.log.info("\nNo matching founded with {}".format(keyboard_input))

            self.interface.interface_selection()

    def config_sensor(self):
        """
        Config sensor
        """
        sensor_rate = self.interface.configure_sensor_interface()
        if sensor_rate != 0:
            self.serial_com.send_UART_command(DefaultsValues.CONFIGURE_SENSOR, sensor_rate)

    def ping(self):
        """
        Ping device
        """
        self.serial_com.ping_device()

    def get_temp(self):
        """
        Get temp storage
        """
        # First get number of data into the storage
        data_number = self.get_data_number()
        if data_number:
            self.serial_com.send_UART_command(DefaultsValues.GET_TEMP)
        else:
            self.log.warning("Storage empty... No data to read!")

    def get_time(self):
        """
        Get time
        """
        self.serial_com.send_UART_command(DefaultsValues.GET_TIME)

    def set_time(self):
        """
        Set time
        """
        self.serial_com.send_UART_command(DefaultsValues.SET_TIME,
                                          [20,
                                           17,
                                           time.localtime().tm_mon,
                                           time.localtime().tm_mday,
                                           time.localtime().tm_hour,
                                           time.localtime().tm_min,
                                           time.localtime().tm_sec])

    def clean_data(self):
        """
        Clean data
        """
        self.serial_com.send_UART_command(DefaultsValues.CLEAN_DATA)

    def get_data_number(self):
        """
        Get data number
        """
        return self.serial_com.send_UART_command(DefaultsValues.GET_DATA_NUMBER)

    def export_data_current_file(self):
        """
        Export data current file
        """
        print("export_data_current_file")

    def export_data_new_file(self):
        """
        Export data new file
        """
        print("export_data_new_file")

    def recover_overflow(self):
        """
        Send command to PIC to put in a good state after UART overflow
        """
        self.serial_com.write(DefaultsValues.START_OF_TEXT)
        if self.serial_com.ping_device():
            self.log.info("Device have been recover successfully")
        else:
            self.log.error("Device is still stuck since overflow....")

    def __del__(self):
        if not self.serial_com.is_open():
            self.log.info("Com port is not open")
        else:
            self.serial_com.close_com_port()
            self.log.info("Serial port com have been closed")


if __name__ == "__main__":
    Main(sys.argv[1:]).main()
