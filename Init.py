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


class Init:
    """
    Class Init
    """

    def __init__(self, argv):
        """Constructor for Init"""
        logging.basicConfig(format='%(message)s', level=logging.INFO)
        self.log = logging.getLogger('')

        self.serial_port = DefaultsValues.COM_PORT
        self.init_UART_bit = False

        try:
            opts, args = getopt.getopt(argv, "hdus:", ["serial=", "debug", "uart"])
        except getopt.GetoptError:
            self.usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h' or opt == '--help':
                self.usage()
                sys.exit()
            elif opt in ("-s", "--serial"):
                self.serial_port = arg
                self.log.info("Com port selected: {}".format(arg))
            elif opt in ("-d", "--debug"):
                self.log.setLevel(logging.DEBUG)
                self.log.info("Logging level set to DEBUG")
            elif opt in ("-u", "--uart"):
                self.init_UART_bit = True
                self.log.info("UART will be automatically initialized")

    def get_logger(self):
        """
        logger getter
        :return: logger
        :rtype: object
        """
        return self.log

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
        self.log.info('  -d or --debug:    Set logger into debug mode')
        self.log.info('  -s or --serial:   Set serial port com')
