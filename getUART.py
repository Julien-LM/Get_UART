#!/usr/bin/env python
"""
    File name:  getUART.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    25/11/17

    Description: Script to get data through UART

"""

import sys
import os
import time

from Init import Init
from UART import UART

from DefaultsValues import choices


class Main:
    """
    Class Main
    """

    def __init__(self, argv):

        # init, initialization class
        self.init = Init(argv)

        # Get logger from Init class
        self.logger = self.init.get_logger()

    def main(self):
        """
        Main script function
        """

        while 1:
            self.log_main_page()

            # get keyboard input
            keyboard_input = raw_input(">> ")

            if keyboard_input == '1' or keyboard_input == 'get_temp':
                self.get_temp()
            if keyboard_input == '2' or keyboard_input == 'get_time':
                self.get_time()
            if keyboard_input == '3' or keyboard_input == 'set_time':
                self.set_time()
            if keyboard_input == '9' or keyboard_input == 'log_time':
                self.log_time()
            elif keyboard_input == 'exit':
                exit()
            else:
                self.logger.info("\nNo matching founded with {}".format(keyboard_input))
                time.sleep(1)
                self.logger.info("Back to main page")
                time.sleep(1)

                # serial_com = UART(logger=self.logger, port=self.init.get_serial_port())
        # serial_com.playUART()

    def log_main_page(self):
        """
        Log choices, related to choices list
        """
        os.system('clear')
        self.logger.info("##################################################################")
        self.logger.info("                Welcome to PIC interface Main page                ")
        self.logger.info("##################################################################")
        self.logger.info("\nSelect one of the following action:")

        for choice in choices:
            self.logger.info("{id}) {text}".format(id=choice.get('id'), text=choice.get('text')))

    def get_temp(self):
        """
        Get temp
        """
        print "get_temp"

    def get_time(self):
        """
        Get time
        """
        print "get_time"

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
        print "log_time"


if __name__ == "__main__":
    Main(sys.argv[1:]).main()
