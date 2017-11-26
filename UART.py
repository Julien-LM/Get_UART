"""
    File name:  UART.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    25/11/17

    Description: UART library

"""
import serial
import time


class UART:
    """
    Class UART
    """

    def __init__(self, logger, port, baud_rate=9600, parity=serial.PARITY_NONE, stop_bits=serial.STOPBITS_ONE,
                 byte_size=serial.EIGHTBITS):

        # get logger
        self.logger = logger

        # configure the serial connections (the parameters differs on the device you are connecting to)
        self.serial_com = serial.Serial(
                     port=port,
                     baudrate=baud_rate,
                     parity=parity,
                     stopbits=stop_bits,
                     bytesize=byte_size
        )

        if self.serial_com.isOpen():
            self.logger.info("Serial port {}, is open".format(port))

    def read(self):
        """
        fd
        """
        return self.serial_com.readline()

    def write(self, data):
        """

        :param data: Data to send
        :type data: String
        :return: number of bytes written
        :rtype: int
        """
        return self.serial_com.write(data)

    def playUART(self):
        """
        Not define
        """
        print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

        while 1:
            # get keyboard input
            input = raw_input(">> ")
            # Python 3 users
            # input = input(">> ")
            if input == 'exit':
                self.serial_com.close()
                exit()
            else:
                # send the character to the device
                # (note that I happend a \r\n carriage return and line feed to the characters
                # this is requested by my device)
                self.serial_com.write(input + '\r\n')
                out = ''
                # let's wait one second before reading output (let's give device time to answer)
                time.sleep(2)
                while self.serial_com.inWaiting() > 0:
                    out += self.serial_com.read(1)

                if out != '':
                    print ">>" + out
