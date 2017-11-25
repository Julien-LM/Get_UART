#!/usr/bin/env python

import sys
import getopt
import logging


class Main:
    def __init__(self, argv):

        # create logger
        logging.basicConfig(format='%(message)s', level=logging.INFO)
        self.logger = logging.getLogger('')

        serial_port = 'ttyUSB0'

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
                serial_port = arg
            elif opt in ("-d", "--debug"):
                self.logger.setLevel(logging.DEBUG)
                self.logger.info("Logging level set to DEBUG")

    def main(self):
        self.logger.info('I am the Main!!!!')

    def usage(self):
        self.logger.info('getUART version TODO')
        self.logger.info('Usage: getUART')
        self.logger.info('   or: getUART [arguments]')

        self.logger.info('Arguments:')
        self.logger.info('  -d or --debug:    Set logger into debug mode')
        self.logger.info('  -s or --serial:   Set serial port com')


if __name__ == "__main__":
    main = Main(sys.argv[1:])
    main.main()

