#!/usr/bin/env python
"""
    File name:  getUART.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    25/11/17

    Description: Script to get data through UART

"""

import sys
import time

import DefaultsValues
from Init import Init
from Interface import Interface
from UART import UART


class Main:
    """
    Class Main
    """

    def __init__(self, argv):

        # init, initialization class
        self.init = Init(argv)

        # Get logger from Init class
        self.log = self.init.get_logger()

        # Serial com variable definition
        self.serial_com = UART(logger=self.log,
                               port=self.init.get_serial_port(),
                               baud_rate=9600)

        # Is UART init a program beginning
        self.init_UART_bit = self.init.get_init_UART_bit()

        # Define interface class
        self.interface = Interface(self.log)

    def main(self):
        """
        Main script function
        """
        if self.init_UART_bit:
            self.serial_com.open_UART()

        while True:
            self.interface.log_main_page()

            # get keyboard input
            keyboard_input = raw_input(">> ")
            if keyboard_input == '0' or keyboard_input == 'connect':
                self.serial_com.open_UART()
                self.interface.interface_selection()
            elif keyboard_input == '1' or keyboard_input == 'get_temp':
                self.get_temp()
            elif keyboard_input == '2' or keyboard_input == 'get_time':
                self.get_time()
            elif keyboard_input == '3' or keyboard_input == 'set_time':
                self.set_time()
            elif keyboard_input == '9' or keyboard_input == 'log_time':
                self.log_time()
            elif keyboard_input == 'exit' or keyboard_input == 'q':
                exit()
            else:
                self.log.info("\nNo matching founded with {}".format(keyboard_input))
                time.sleep(1)
                self.log.info("Back to main page")
                time.sleep(1)

    def get_temp(self):
        """
        Get temp
        """
        self.serial_com.send_UART_command(DefaultsValues.GET_TEMP)
        received_data = self.serial_com.parse_answer()

        # hex_value = read_values.encode('hex')
        # print " : ".join("{:02x}".format(ord(c))for c in read_values)
        # #print "serial reception: {}".format(hex_value)

        self.interface.interface_selection()

    def get_time(self):
        """
        Get time
        """
        self.log.info("Would you like to also compare time with local one? (y/n)")

    def set_time(self):
        """
        Set time
        """
        print "set_time"

    def configure_sensor(self):
        """
        Configure sensor
        """
        print "configure_sensor"

    def clean_data(self):
        """
        Clean data
        """
        print "clean_data"

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
        self.log.info(time.localtime())
        self.log.info("year = {}".format(time.localtime().tm_year))
        self.log.info("month = {}".format(time.localtime().tm_mon))
        self.log.info("day = {}".format(time.localtime().tm_mday))
        self.log.info("hour = {}".format(time.localtime().tm_hour))
        self.log.info("minute = {}".format(time.localtime().tm_min))
        self.log.info("second = {}".format(time.localtime().tm_sec))
        self.interface.interface_selection()


if __name__ == "__main__":
    Main(sys.argv[1:]).main()
