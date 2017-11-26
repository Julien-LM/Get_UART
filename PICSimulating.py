#!/usr/bin/env python
"""
    File name:  PICSimulating
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    26/11/17
    
    Description:
    
"""

from UART import UART
import logging
import time

logging.basicConfig(format='%(message)s', level=logging.INFO)
serial_com = UART(logger=logging.getLogger(''),
                  port='/dev/ttyS1')
while 1:
    received_data = serial_com.read
    print received_data
    time.sleep(1)
    if '02' in received_data:
        print '02 received'
        serial_com.write('copy Roger!!')
