#!/usr/bin/env python
"""
    File name:  getUART.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    25/11/17

    Description: Script to get data through UART

"""

import sys

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
        self.logger.info("Let's try UART!!!")
        serial_com = UART(logger=self.logger, port=self.init.get_serial_port())
        serial_com.playUART()


if __name__ == "__main__":
    Main(sys.argv[1:]).main()
