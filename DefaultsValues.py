"""
    File name:  Defaults_values
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    26/11/17
    
    Description:
    
"""

COM_PORT = '/dev/ttyUSB0'

# ASCII definition
END_OF_TRANSMIT         = 0x04
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

# Commands args size
GET_TEMP_SIZE           = 0x00
GET_TIME_SIZE           = 0x00
SET_TIME_SIZE           = 0x06
CONFIGURE_SENSOR_SIZE   = 0x02
CLEAN_DATA_SIZE         = 0x00
GET_DATA_NUMBER_SIZE    = 0x00
