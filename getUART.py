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

from Init import Init
from UART import UART


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
        os.system('clear')
        self.logger.info("#################################################################")
        self.logger.info("                    Welcome to PIC interface                     ")
        self.logger.info("#################################################################")

        self.logger.info("\nSelect one of the following action:")
        self.logger.info("1) Get temp")
        self.logger.info("2) Get time")
        self.logger.info("3) Set time")
        self.logger.info("4) Configure sensor")
        self.logger.info("5) Clean data")
        self.logger.info("6) Get data number")

        self.logger.info("7) Export data current file")
        self.logger.info("8) Export data new file")

        while 1:
            # get keyboard input
            input = raw_input(">> ")
            print input
            if input == 'exit':
                exit()


        # serial_com = UART(logger=self.logger, port=self.init.get_serial_port())
        # serial_com.playUART()


if __name__ == "__main__":
    Main(sys.argv[1:]).main()
