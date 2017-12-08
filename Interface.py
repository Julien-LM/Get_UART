"""
    File name:  Interface
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    08/12/17
    
    Description:
    
"""

from DefaultsValues import choices

import os


class Interface:
    """
    Class which manage interface
    """

    def __init__(self, logger):
        self.logger = logger

    def interface_selection(self):
        """
        Function used to leave program or continue to main menu
        """
        self.logger.info("\nPress 'q' to exit, Enter to continue to main menu")
        choice = raw_input('>> ')
        if choice == 'q' or choice == 'exit':
            exit()

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

