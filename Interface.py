# coding=utf-8
"""
    File name:  Interface.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    08/12/17
    
    Description:
    
"""

import logging
import os

from DefaultsValues import choices


class Interface(object):
    """
    Class which manage interface
    """

    def __init__(self):
        self.log = logging.getLogger('get_UART')
        self.first_screen = True

    @property
    def get_input_char(self):
        """
        :return: Data coming from keyboard
        :rtype: String
        """
        input_data = 0
        try:
            input_data = raw_input('>> ')
        except KeyboardInterrupt:
            self.log.info("KeyboardInterrupt, this program is ending...")
            exit(0)
        return input_data

    def get_input_int(self):
        """
        :return: Data coming from keyboard
        :rtype: String
        """
        input_data = self.get_input_char
        try:
            return int(input_data)
        except ValueError:
            self.log.error("Input value is not an integer... ")
            return -1

    def interface_selection(self):
        """
        Function used to leave program or continue to main menu
        """
        self.log.info("\nPress 'q' to exit, Enter to continue to main menu")
        choice = self.get_input_char
        if choice == 'q' or choice == 'exit':
            exit(0)

    def log_main_page(self):
        """
        Log choices, related to choices list
        """

        if self.first_screen:
            self.first_screen = False
            self.log.info("")
        else:
            os.system('clear')

        self.log.info("##################################################################")
        self.log.info("                Welcome to PIC interface Main page                ")
        self.log.info("##################################################################")
        self.log.info("\nSelect one of the following action:")

        for choice in choices:
            self.log.info("{id}) {text}".format(id=choice.get('id'), text=choice.get('text')))

    def log_init_info(self):
        """
        Log basic welcome screen
        """
        os.system('clear')
        self.log.info("##################################################################")
        self.log.info("                getUART initialization information                ")
        self.log.info("##################################################################\n")
