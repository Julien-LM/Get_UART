"""
    File name:  Defaults_values.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    26/11/17
    
    Description:
    
"""

COM_PORT = '/dev/ttyUSB0'

# ASCII definition
END_OF_TRANSMIT         = '\x04'
START_OF_TEXT           = '\x02'
ACKNOWLEDGE             = '\x06'
LINE_FEED               = '\x0A'
CARRIAGE_RETURN         = '\x0D'
NEG_ACKNOWLEDGE         = '\x15'
BACKSPACE               = '\x08'

# Errors codes
WRONG_ARGUMENTS         = '\x41'
UNKNOWN_COMMAND         = '\x42'
BUFFER_OVERFLOW         = '\x43'
DEVICE_BUSY             = '\x44'
FRAMING_ERROR           = '\x45'
OVERRUN_ERROR           = '\x46'

# Communication Protocol
GET_TEMP                = '\x20'
GET_TIME                = '\x21'
SET_TIME                = '\x22'
CONFIGURE_SENSOR        = '\x30'
CLEAN_DATA              = '\x31'
GET_DATA_NUMBER         = '\x32'
PING                    = '\x33'

# Commands args size
GET_TEMP_SIZE           = 0
GET_TIME_SIZE           = 0
SET_TIME_SIZE           = 6
CONFIGURE_SENSOR_SIZE   = 2
CLEAN_DATA_SIZE         = 0
GET_DATA_NUMBER_SIZE    = 0

choices = [{'id': 0, 'text': 'Connect to PIC'},
           {'id': 1, 'text': 'Get temp'},
           {'id': 2, 'text': 'Get time'},
           {'id': 3, 'text': 'Set tme'},
           {'id': 4, 'text': 'Configure sensor'},
           {'id': 5, 'text': 'Clean data'},
           {'id': 6, 'text': 'Get data number'},
           {'id': 7, 'text': 'Export data current file'},
           {'id': 8, 'text': 'Export data new file'},
           {'id': 9, 'text': 'Log current time'},
           {'id': 'p', 'text': 'Ping device'}]
