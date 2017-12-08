"""
    File name:  UART.py
    Author:     Julien LE MELLEC
    Mail:       julien.lemellec@gmail.com
    Created:    25/11/17

    Description: UART library

"""
import serial
import time

import DefaultsValues
from Interface import Interface


class UART:
    """
    Class UART
    """

    def __init__(self, logger, port, baud_rate=9600, parity=serial.PARITY_NONE, stop_bits=serial.STOPBITS_ONE,
                 byte_size=serial.EIGHTBITS):

        # get logger
        self.log = logger

        # get interface
        self.interface = Interface(self.log)

        self.serial_com = None

        self.port = port
        self.baud_rate = baud_rate
        self.parity = parity
        self.stop_bits = stop_bits
        self.byte_size = byte_size

    def open_UART(self):
        """
        UART class declaration and ping PIC
        """
        if self.serial_com is None:
            # Open serial port com
            try:
                self.open_serial_com()
            except serial.serialutil.SerialException as e:
                self.log.error("Serial error({0}): {1}".format(e.errno, e.strerror))
                self.interface.interface_selection()
            else:
                self.log.info("Serial com port have been initialized successfully")
                if self.is_open():
                    self.log.info("Serial com port is open")

            # Ping device
            if self.ping_device():
                self.log.info("Device is right answering")
            else:
                self.log.info("Device is offline...")
                self.log.info("Run a diagnostic for more information")
                self.interface.interface_selection()
        else:
            self.log.warning("\n!!!! Serial com have already be declared !!!!")

    def open_serial_com(self):
        """
        Open serial com
        """
        self.serial_com = serial.Serial(
            port=self.port,
            baudrate=self.baud_rate,
            parity=self.parity,
            stopbits=self.stop_bits,
            bytesize=self.byte_size
        )

    def is_open(self):
        """

        :return: Get the state of the serial port, whether it's open.
        :rtype: bool
        """
        return self.serial_com.isOpen()

    def parse_answer(self):
        """
        Parse answer from PIC
        :return: data from PIC
        :rtype: int
        """
        received_thread = self.read()

        # Check for Acknowledge
        if received_thread[0] == DefaultsValues.ACKNOWLEDGE:
            self.log.info("Acknowledge received")
        else:
            self.log.error("Acknowledge have not been received...")
            return -1

        # Check for line feed
        if received_thread[-1] == DefaultsValues.LINE_FEED:
            self.log.info("Line feed received")
        else:
            self.log.error("Line feed have not been received...")
            return -1

        # Check for command
        if received_thread[1] == DefaultsValues.GET_TEMP:
            return received_thread[2:4]
        elif received_thread[1] == DefaultsValues.GET_TIME:
            return received_thread[2:8]
        elif received_thread[1] == DefaultsValues.SET_TIME:
            return True
        elif received_thread[1] == DefaultsValues.CONFIGURE_SENSOR:
            return True
        elif received_thread[1] == DefaultsValues.CLEAN_DATA:
            return True
        elif received_thread[1] == DefaultsValues.GET_DATA_NUMBER:
            return received_thread[2]
        else:
            self.log.error("Unknown command received...")

        # Parse each value received from PIC
        for val in received_thread:
            if val == DefaultsValues.ACKNOWLEDGE:
                self.log.info("Acknowledge received")
            print("{:02x}".format(ord(val)))

        data = 0
        return data

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

    def ping_device(self):
        """
        Send command to device and check if it is answering well

        :return: return 1 si device answer, 0 if not
        :rtype: int
        """
        return 1

    def send_UART_command(self, command, args=0):
        """

        :param command: command ref
        :type command: int
        :param args: args relative to command
        :type args: list
        """
        self.write(command)
        self.write(args)
        self.write(DefaultsValues.LINE_FEED)

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
