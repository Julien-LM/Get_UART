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
import time

import DefaultsValues


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

        for choice in DefaultsValues.choices:
            self.log.info("{id}) {text}".format(id=choice.get('id'), text=choice.get('text')))

    def log_init_info(self):
        """
        Log basic welcome screen
        """
        os.system('clear')
        self.log.info("##################################################################")
        self.log.info("                getUART initialization information                ")
        self.log.info("##################################################################\n")

    def configure_sensor_interface(self):
        """
        Send getting temp rate
        First 6 bits, value: from 0 to 63
        Last 2 bits, unit: see DefaultsValues
        return 0 if error detected
        """
        unit = -1
        self.log.info("Enter time unit (seconds, minutes, hours)")
        keyboard_input = self.get_input_char
        for time_unit in DefaultsValues.TimeUnitValues:
            if keyboard_input in time_unit:
                self.log.info("Correct input, selected value: {}".format(time_unit))
                unit = DefaultsValues.TimeUnitValues.get(time_unit)
                break
        if unit == -1:
            self.log.warning("Wrong input... Back to main menu")
            return 0

        self.log.info("Enter time value, from 1 to 60")
        keyboard_input = self.get_input_int()
        if 1 <= keyboard_input <= 60:
            self.log.info("Correct input, selected value: {}".format(keyboard_input))
            self.log.debug("Arg: {arg:08b}, hex: {arg:02x}".format(arg=keyboard_input + (unit << 6)))
            return [keyboard_input + (unit << 6)]
        else:
            self.log.warning("Wrong input... Back to main menu")
            return 0


class System(object):
    """
    Class PICom
    """

    def __init__(self):
        self.log = logging.getLogger('get_UART')

    def log_time(self):
        """
        Log time
        """
        self.log.info("Actual time")
        self.log.info("{day:02d}/{month:02d}/{year} {hour:02d}:{minute:02d}:{seconds:02d}\n".format(
            day=time.localtime().tm_mday, month=time.localtime().tm_mon,
            year=time.localtime().tm_year, hour=time.localtime().tm_hour,
            minute=time.localtime().tm_min, seconds=time.localtime().tm_sec))