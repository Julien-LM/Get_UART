"""
    File name:  Defaults_values.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    26/11/17
    
    Description:
    
"""

COM_PORT = '/dev/ttyUSB0'

# ASCII definition
END_OF_TRANSMIT         = 0xFE
START_OF_TEXT           = 0x02
ACKNOWLEDGE             = 0x06
LINE_FEED               = 0x0A
CARRIAGE_RETURN         = 0x0D
NEG_ACKNOWLEDGE         = 0x15
BACKSPACE               = 0x08

# Errors codes
WRONG_ARGUMENTS         = 0x41
UNKNOWN_COMMAND         = 0x42
BUFFER_OVERFLOW         = 0x43
DEVICE_BUSY             = 0x44
FRAMING_ERROR           = 0x45
OVERRUN_ERROR           = 0x46

# Communication Protocol
GET_TEMP                = 0x20
GET_TIME                = 0x21
SET_TIME                = 0x22
CONFIGURE_SENSOR        = 0x30
CLEAN_DATA              = 0x31
GET_DATA_NUMBER         = 0x32
PING                    = 0x33

# Commands answer args size
GET_TEMP_SIZE           = 2
GET_TIME_SIZE           = 7
SET_TIME_SIZE           = 0
CONFIGURE_SENSOR_SIZE   = 0
CLEAN_DATA_SIZE         = 0
GET_DATA_NUMBER_SIZE    = 0

#Config Sensor Unit
SECONDS                 = 0
MINUTES                 = 1
HOURS                   = 2

TimeUnitValues = {'seconds': 0,
                  'minutes': 1,
                  'hours': 2}

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
           {'id': 'p', 'text': 'Ping device'},
           {'id': 'r', 'text': 'Recover overflow'}]

# term log format
normal = "\033[0m"
black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
purple = "\033[35m"
cyan = "\033[36m"
grey = "\033[37m"

bold = "\033[1m"
uline = "\033[4m"
blink = "\033[5m"
invert = "\033[7m"
