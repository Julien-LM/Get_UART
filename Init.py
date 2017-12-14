# coding=utf-8
"""
    File name:  Init.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    26/11/17

    Description: Initialization class

"""

import logging
import sys
import getopt
import DefaultsValues
from SpecialFormatter import SpecialFormatter
from Interface import Interface


class Init(object):
    """
    Class Init
    """

    def __init__(self, argv):
        """Constructor for Init"""
        # Logger managing
        fmt = SpecialFormatter()
        stream_handler = logging.StreamHandler(sys.stdout)

        stream_handler.setFormatter(fmt)

        self.log = logging.getLogger('get_UART')
        self.log.setLevel(logging.INFO)
        self.log.addHandler(stream_handler)

        # Interface
        interface = Interface()
        interface.log_init_info()

        self.serial_port = DefaultsValues.COM_PORT
        self.init_UART_bit = False

        try:
            opts, args = getopt.getopt(argv, "hdus:", ["serial=", "debug", "uart"])
        except getopt.GetoptError:
            self.usage()
            sys.exit(1)
        for opt, arg in opts:
            if opt == '-h' or opt == '--help':
                self.usage()
                sys.exit(0)
            elif opt in ("-s", "--serial"):
                self.serial_port = arg
                self.log.info("Com port selected: {}".format(arg))
            elif opt in ("-d", "--debug"):
                self.log.setLevel(logging.DEBUG)
                self.log.info("Logging level set to DEBUG")
            elif opt in ("-u", "--uart"):
                self.init_UART_bit = True
                self.log.info("UART will be automatically initialized")

    def get_serial_port(self):
        """
        serial_port getter
        :return: serial port
        :rtype: String
        """
        return self.serial_port

    def get_init_UART_bit(self):
        """
        uart init bit getter
        :return: uart init
        :rtype: bool
        """
        return self.init_UART_bit

    def usage(self):
        """
        Script usage information
        """
        self.log.info('getUART version TODO')
        self.log.info('Usage: getUART')
        self.log.info('   or: getUART [arguments]')

        self.log.info('Arguments:')
        self.log.info('  -d or --debug:     Set logger into debug mode')
        self.log.info('  -s or --serial:    Set serial port com')
        self.log.info('  -u or --uart:      Open UART com port during init')
