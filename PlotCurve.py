# coding=utf-8
"""
    File name:  PlotCurve.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    02/03/18
    
    Description:
    
"""

import logging

import matplotlib.pyplot as plt
import matplotlib.dates as mat_dates
import DefaultsValues


class PlotCurve(object):
    """
    Class TempParsing
    """

    def __init__(self):
        self.log = logging.getLogger('get_UART')

    def plot_first_curve(self, data_tab):
        x_array = []
        y_array = []

        for data in data_tab:
            x_array.append(data[0])
            y_array.append(data[1])

        x_array = mat_dates.epoch2num(x_array)

        fig, ax = plt.subplots()
        ax.plot(x_array, y_array)

        myFmt = mat_dates.DateFormatter("%m/%d %H:%M")
        ax.xaxis.set_major_formatter(myFmt)

        # Rotate date labels automatically
        fig.autofmt_xdate()
        plt.show()
