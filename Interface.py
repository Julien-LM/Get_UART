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
        self.log = logger

    def interface_selection(self):
        """
        Function used to leave program or continue to main menu
        """
        self.log.info("\nPress 'q' to exit, Enter to continue to main menu")
        choice = raw_input('>> ')
        if choice == 'q' or choice == 'exit':
            exit()

    def log_main_page(self):
        """
        Log choices, related to choices list
        """
        os.system('clear')
        self.log.info("##################################################################")
        self.log.info("                Welcome to PIC interface Main page                ")
        self.log.info("##################################################################")
        self.log.info("\nSelect one of the following action:")

        for choice in choices:
            self.log.info("{id}) {text}".format(id=choice.get('id'), text=choice.get('text')))

