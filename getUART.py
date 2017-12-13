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
            keyboard_input = self.interface.get_input_char()
            if keyboard_input == '0' or keyboard_input == 'connect':
                self.serial_com.open_UART()
            elif keyboard_input == '1' or keyboard_input == 'get_temp':
                self.get_temp()
            elif keyboard_input == '2' or keyboard_input == 'get_time':
                self.get_time()
            elif keyboard_input == '3' or keyboard_input == 'set_time':
                self.set_time()
            elif keyboard_input == '4' or keyboard_input == 'configure':
                self.configure_sensor()
            elif keyboard_input == '9' or keyboard_input == 'log_time':
                self.log_time()
            elif keyboard_input == 'p' or keyboard_input == 'ping':
                self.ping()
            elif keyboard_input == 'r' or keyboard_input == 'recover':
                self.recover_overflow()
            elif keyboard_input == 'exit' or keyboard_input == 'q':
                exit(0)
            else:
                self.log.info("\nNo matching founded with {}".format(keyboard_input))

            self.interface.interface_selection()

    def ping(self):
        """
        Ping device
        """
        if self.serial_com.ping_device():
            self.log.info("Device is right answering")
        else:
            self.log.error("Device is offline...")

    def get_temp(self):
        """
        Get temp
        """
        if self.serial_com.send_UART_command(DefaultsValues.GET_TEMP):
            received_data = self.serial_com.parse_answer()
            if received_data:
                self.log.info("temp = {},{}".format(received_data[0], int(received_data[1] / 25.6)))

    def get_time(self):
        """
        Get time
        """
        # self.log.info("Wouaw_input('>> ')
        if self.serial_com.send_UART_command(DefaultsValues.GET_TIME):
            received_data = self.serial_com.parse_answer()
            if received_data:
                self.log.info("Time from PIC")
                self.log.info("{day:02d}/{month:02d}/{century}{year} {hour:02d}:{minute:02d}:{seconds:02d}\n".format(
                    day=received_data[3], month=received_data[2], year=received_data[1],
                    hour=received_data[4], minute=received_data[5], seconds=received_data[6],
                    century=received_data[0]))

                self.log_time()

    def set_time(self):
        """
        Set time
        """
        if self.serial_com.send_UART_command(DefaultsValues.SET_TIME,
                                             [20,
                                              17,
                                              time.localtime().tm_mon,
                                              time.localtime().tm_mday,
                                              time.localtime().tm_hour,
                                              time.localtime().tm_min,
                                              time.localtime().tm_sec]):
            if self.serial_com.parse_answer():
                self.log.info("Time set successfully")

    def configure_sensor(self):
        """
        Send getting temp rate
        First 6 bits, value: from 0 to 63
        Last 2 bits, unit: see DefaultsValues
        return 0 if error detected
        """
        unit = -1
        self.log.info("Enter time unit (seconds, minutes, hours)")
        keyboard_input = self.interface.get_input_char()
        for time_unit in DefaultsValues.TimeUnitValues:
            if keyboard_input in time_unit:
                self.log.info("Correct input, selected value: {}".format(time_unit))
                unit = DefaultsValues.TimeUnitValues.get(time_unit)
                break
        if unit == -1:
            self.log.warning("Wrong input... Back to main menu")
            return 0

        self.log.info("Enter time value, from 1 to 60")
        keyboard_input = self.interface.get_input_int()
        if 1 <= keyboard_input <= 60:
            self.log.info("Correct input, selected value: {}".format(keyboard_input))
        else:
            self.log.warning("Wrong input... Back to main menu")
            return 0

        if self.serial_com.send_UART_command(DefaultsValues.CONFIGURE_SENSOR,
                                             [keyboard_input + (unit << 6)]):
            self.log.debug("Arg: {arg:08b}, hex: {arg:02x}".format(arg=keyboard_input + (unit << 6)))
            received_data = self.serial_com.parse_answer()
            if received_data:
                self.log.info("Sensor configured successfully")
                self.log.debug("Value in sec: {}:{}".format(received_data[1], received_data[0]))

    def clean_data(self):
        """
        Clean data
        """
        print 'clean_data'

    def get_data_number(self):
        """
        Get data number
        """
        print "get_data_number"

    def export_data_current_file(self):
        """
        Export data current file
        """
        print "export_data_current_file"

    def export_data_new_file(self):
        """
        Export data new file
        """
        print "export_data_new_file"

    def log_time(self):
        """
        Log time
        """
        self.log.info("Actual time")
        self.log.info("{day:02d}/{month:02d}/{year} {hour:02d}:{minute:02d}:{seconds:02d}\n".format(
            day=time.localtime().tm_mday, month=time.localtime().tm_mon,
            year=time.localtime().tm_year, hour=time.localtime().tm_hour,
            minute=time.localtime().tm_min, seconds=time.localtime().tm_sec))

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
