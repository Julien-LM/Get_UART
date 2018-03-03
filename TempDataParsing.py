# coding=utf-8
"""
    File name:  TempDataParsing.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    22/02/18
    
    Description:
    
"""

import calendar
import datetime
import logging

import DefaultsValues


class TempParsing(object):
    """
    Class TempParsing
    """

    def __init__(self):
        self.log = logging.getLogger('get_UART')

    def store_temp_data_to_readable_table(self, brut_data_from_pic):
        """
        Get data from pic, move it to a easy parsing table
        output format:
        Time | Temp
        :return:
        :rtype:
        """

        output_tab = []
        reference_time = 0
        reference_step = 5
        i = 0

        while i < len(brut_data_from_pic):
            if brut_data_from_pic[i] == DefaultsValues.TIME_TRANSFERT_IND:
                i += DefaultsValues.TIME_TRANSFERT_IND_S + 1
                reference_time = self.get_reference_time(
                    brut_data_from_pic[(i - DefaultsValues.TIME_TRANSFERT_IND_S):i])

            elif brut_data_from_pic[i] == DefaultsValues.S_RATE_TRANSFERT_IND:
                i += DefaultsValues.S_RATE_TRANSFERT_IND_S + 1
                reference_step = self.get_reference_step(brut_data_from_pic[(i - DefaultsValues.S_RATE_TRANSFERT_IND_S):i])
            else:
                output_tab.append((reference_time, self.get_temp_value(brut_data_from_pic[i:i+2])))
                reference_time = reference_time + reference_step
                i += 2

        return output_tab

    def get_reference_time(self, time_tab):

        if len(time_tab) == DefaultsValues.TIME_TRANSFERT_IND_S:
            year = time_tab[0]*100 + time_tab[1]

            date = datetime.datetime(year, time_tab[2], time_tab[3], time_tab[4], time_tab[5], time_tab[6])
            universal_time = calendar.timegm(date.timetuple())
            return universal_time
        else:
            self.log.error("Get reference time, wrong arg size")
            return 0

    def get_reference_step(self, step_tab):
        if len(step_tab) == DefaultsValues.S_RATE_TRANSFERT_IND_S:
            reference_step = step_tab[3] + (step_tab[2] << 8) + (step_tab[1] << 16) + (step_tab[0] << 24)
            return reference_step
        else:
            self.log.error("Get reference step, wrong arg size")
            return 0

    def get_temp_value(self, temp_tab):
        """
        Get 2 Byte, build a real temperature value
        :param temp_tab: temp
        :type temp_tab: list
        :return: temp
        :rtype: float
        """
        if len(temp_tab) != 2:
            self.log.error("Table do not contains 2 elements")
            self.log.warning("Table size is: {}".format(len(temp_tab)))
            if len(temp_tab) == 1:
                self.log.warning("tab[0] = {}".format(temp_tab[0]))
            return 0
        else:
            real_part = temp_tab[1]/25.6
            res = temp_tab[0] + real_part*0.1
            return round(res, 2)
