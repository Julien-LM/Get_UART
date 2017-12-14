# coding=utf-8
"""
    File name:  SpecialFormatter.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    09/12/17
    
    Description:
    
"""

import logging
from DefaultsValues import red, yellow, green, normal


class SpecialFormatter(logging.Formatter):
    """
    Special format file for logging
    """

    err_format = red+"ERROR: %(msg)s"+normal
    warn_format = yellow+"!!!WARNING!!! %(msg)s"+normal
    dbg_format = green+"%(lineno)d:%(module)s:DBG: %(msg)s"+normal
    info_format = "%(msg)s"

    def __init__(self, fmt="%(levelno)s: %(msg)s"):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        """

        :param record: record format
        :type record: Object
        :return: record format
        :rtype: Object
        """
        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._fmt = SpecialFormatter.dbg_format

        elif record.levelno == logging.INFO:
            self._fmt = SpecialFormatter.info_format

        elif record.levelno == logging.WARNING:
            self._fmt = SpecialFormatter.warn_format

        elif record.levelno == logging.ERROR:
            self._fmt = SpecialFormatter.err_format

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._fmt = format_orig

        return result
