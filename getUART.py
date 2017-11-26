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


class Main:
    """
    Class Main
    """

    def __init__(self, argv):

        # init, initialization class
        init = Init(argv)

        # Get logger from Init class
        self.logger = init.get_logger()

    def main(self):
        """
        Main script function
        """
        self.logger.info('I am the Main!!!!')


if __name__ == "__main__":
    Main(sys.argv[1:]).main()
