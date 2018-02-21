# coding=utf-8
"""
    File name:  PICom.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    18/12/17
    
    Description:
    
"""

import logging
import DefaultsValues
from Interface import System


class PICom(object):
    """
    Class PICom
    """

    def __init__(self):
        self.log = logging.getLogger('get_UART')

        # System class
        self.system = System()

        self.data_number = 0

    def get_real_time_info(self, received_data):
        """
        Get every real time info
        """
        self.log.info("temp = {},{}".format(received_data[0], int(received_data[1] / 25.6)))
        return True

    def config_sensor_parsing(self, received_data):
        """
        log config sensor infos
        :param received_data: Data from PIC
        :type received_data: list
        """
        self.log.info("Sample rate config in sec: {}:{}".format(received_data[1], received_data[0]))
        return True

    def ping_parsing(self, answered_command):
        """
        Ping
        :return: Is device answer
        :rtype: bool
        :param answered_command: Command answered
        :type answered_command: char
        """
        if answered_command == DefaultsValues.PING:
            self.log.info("Device is right answering")
            return True
        else:
            self.log.error("Device is offline...")
            return False

    def get_data_number_parsing(self, received_data):
        """
        get data number
        :return: Number of data
        :rtype: int
        """
        self.log.debug("Value: {}:{}".format(received_data[1], received_data[0]))
        temp_data_number = received_data[0] + (received_data[1] << 8)
        self.log.info("temp_data_number = {}".format(temp_data_number))
        self.data_number = temp_data_number
        return temp_data_number

    def set_time_parsing(self):
        """
        Log info message
        """
        self.log.info("Time set successfully")
        return True

    def get_time_parsing(self, received_data):
        """
        get time
        """
        self.log.info("Time from PIC")
        self.log.info("{day:02d}/{month:02d}/{century}{year} {hour:02d}:{minute:02d}:{seconds:02d}\n".format(
            day=received_data[3], month=received_data[2], year=received_data[1],
            hour=received_data[4], minute=received_data[5], seconds=received_data[6],
            century=received_data[0]))

        self.system.log_time()
        return True

    def get_temp_parsing(self, received_data):
        """
        Log data
        :param received_data: data from pic
        :type received_data: list
        """
        if self.data_number == len(received_data):
            self.log.info("Data received OK!!")
            # for data in received_data:
            #     self.log.info("data = 0x{:02x}".format(data))
        else:
            self.log.warning("Number of read data does not match with expected value")
        return True

    def clean_data_parsing(self):
        """
        Clean data
        """
        self.log.info("Data cleaned")
        return True

    def get_debug_value_parsing(self, received_data):
        """
        Log debug data from PIC
        :param received_data: data from pic
        :type received_data: list
        """

        self.log.info("Debug data:")
        for data in received_data:
            self.log.info("{}".format(data))

        return True
