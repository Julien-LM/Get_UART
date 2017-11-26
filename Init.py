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
        self.logger = logging.getLogger('')

        self.serial_port = DefaultsValues.COM_PORT

        try:
            opts, args = getopt.getopt(argv, "hds:", ["serial=", "debug"])
        except getopt.GetoptError:
            self.usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h' or opt == '--help':
                self.usage()
                sys.exit()
            elif opt in ("-s", "--serial"):
                self.serial_port = arg
                self.logger.info("Com port selected: {}".format(arg))
            elif opt in ("-d", "--debug"):
                self.logger.setLevel(logging.DEBUG)
                self.logger.info("Logging level set to DEBUG")

    def get_logger(self):
        """
        logger getter
        :return: logger
        :rtype: object
        """
        return self.logger

    def get_serial_port(self):
        """
        serial_port getter
        :return: serial port
        :rtype: String
        """
        return self.serial_port

    def usage(self):
        """
        Script usage information
        """
        self.logger.info('getUART version TODO')
        self.logger.info('Usage: getUART')
        self.logger.info('   or: getUART [arguments]')

        self.logger.info('Arguments:')
        self.logger.info('  -d or --debug:    Set logger into debug mode')
        self.logger.info('  -s or --serial:   Set serial port com')
