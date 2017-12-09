#!/usr/bin/env python
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


class Main:
    """
    Class Main
    """

    def __init__(self, argv):

        # init, initialization class
        self.init = Init(argv)

        # Get logger from Init class
        self.log = logging.getLogger('get_UART')

        # Serial com variable definition
        self.serial_com = UART(port=self.init.get_serial_port(),
                               baud_rate=9600)

        # Is UART init a program beginning
        self.init_UART_bit = self.init.get_init_UART_bit()

        # Define interface class
        self.interface = Interface()

    def main(self):
        """
        Main script function
        """
        if self.init_UART_bit:
            self.serial_com.open_UART(True)

        while True:
            self.interface.log_main_page()

            # get keyboard input
            try:
                keyboard_input = raw_input(">> ")
            except KeyboardInterrupt:
                self.log.info("KeyboardInterrupt, this program is ending...")
                exit(0)
            if keyboard_input == '0' or keyboard_input == 'connect':
                self.serial_com.open_UART(False)
                self.interface.interface_selection()
            elif keyboard_input == '1' or keyboard_input == 'get_temp':
                self.get_temp()
            elif keyboard_input == '2' or keyboard_input == 'get_time':
                self.get_time()
            elif keyboard_input == '3' or keyboard_input == 'set_time':
                self.set_time()
            elif keyboard_input == '9' or keyboard_input == 'log_time':
                self.log_time()
            elif keyboard_input == 'p' or keyboard_input == 'ping':
                self.ping()
            elif keyboard_input == 'exit' or keyboard_input == 'q':
                exit(0)
            else:
                self.log.info("\nNo matching founded with {}".format(keyboard_input))
                time.sleep(1)
                self.log.info("Back to main page")
                time.sleep(1)

    def ping(self):
        """
        Ping device
        """
        if self.serial_com.ping_device():
            self.log.info("Device is right answering")
        else:
            self.log.error("Device is offline...")
        self.interface.interface_selection()

    def get_temp(self):
        """
        Get temp
        """
        if self.serial_com.send_UART_command(DefaultsValues.GET_TEMP):
            received_data = self.serial_com.parse_answer()
            if received_data != 0:
                self.log.info("temp = {},{}".format(ord(received_data[0]), ord(received_data[1])))

        self.interface.interface_selection()

    def get_time(self):
        """
        Get time
        """
        self.log.info("Would you like to also compare time with local one? (y/n)")
        binary_choice = raw_input('>> ')
        if self.serial_com.send_UART_command(DefaultsValues.GET_TIME):
            received_data = self.serial_com.parse_answer()
            if received_data != 0:
                self.log.info("Time from PIC")
                self.log.info("years = {}".format(ord(received_data[0])))
                self.log.info("months = {}".format(ord(received_data[1])))
                self.log.info("days = {}".format(ord(received_data[2])))
                self.log.info("hours = {}".format(ord(received_data[3])))
                self.log.info("minutes = {}".format(ord(received_data[4])))
                self.log.info("secondes = {}".format(ord(received_data[5])))

        if binary_choice:
            self.log_time()

    def set_time(self):
        """
        Set time
        """
        if self.serial_com.send_UART_command(DefaultsValues.SET_TIME,
                                             [time.localtime().tm_year,
                                              time.localtime().tm_mon,
                                              time.localtime().tm_mday,
                                              time.localtime().tm_hour,
                                              time.localtime().tm_min,
                                              time.localtime().tm_sec]):
            if self.serial_com.parse_answer():
                self.log.info("Time set successfully")

        self.interface.interface_selection()

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
        self.log.info("Actual time")
        # self.log.info(time.localtime())
        self.log.info("year = {}".format(time.localtime().tm_year))
        self.log.info("month = {}".format(time.localtime().tm_mon))
        self.log.info("day = {}".format(time.localtime().tm_mday))
        self.log.info("hour = {}".format(time.localtime().tm_hour))
        self.log.info("minute = {}".format(time.localtime().tm_min))
        self.log.info("second = {}".format(time.localtime().tm_sec))
        self.interface.interface_selection()

    def __del__(self):
        if not self.serial_com.is_open():
            self.log.info("Com port is not open")
        else:
            self.serial_com.close_com_port()
            self.log.info("Serial port com have been closed")


if __name__ == "__main__":
    Main(sys.argv[1:]).main()
