"""
A library class o interface to the McPherson Monochromator Scan Controller
through serial connection
https://pyserial.readthedocs.io/en/latest/shortintro.html

"""
import serial
import time

MAX_STEPS = 8388600

class mcpherson():
    """
    Models an  Serial connection
    """
# Defaults,
#bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE,
    def __init__(self, serial_port='/dev/ttyACM0', read_timeout=2.0):
        """
        Initializes the serial connection to the Arduino board
        """
        self.ser = serial.Serial(port=serial_port, baudrate=9600,
                                 xonxoff=True, timeout=read_timeout)
        #command = f' '.encode('utf-8')
        self.ser.write(b' ') # This commenda must be entered after power up
        #self.ser.timeout = read_timeout # Timeout for readline()

    def reset(self):
        """
        1) Stop Motion
        2) Sets counter to "0" ?
        3) Assumed "Idle" State
        """
        self.ser.write(b'\x03\r') # ^C

    def scanSteps(self, value):
        """
        Scan in Up/Down Direction
        36000 = 1 motor revolution
        Max 8388600
        Unicode strings must be encoded (e.g. 'hello'.encode('utf-8').
        """
        if value > MAX_STEPS:
            value = MAX_STEPS

        elif value < -MAX_STEPS:
            value = -MAX_STEPS

        if value >= 0:
            command = f'+{value:d}\r'.encode('utf-8')
        else:
            aval=abs(value)
            command = f'-{aval:d}\r'.encode('utf-8')

        print(command)
        self.ser.write(command)

    def findHome(self):
        """
        Find Home position
        """

        self.ser.write(b'A8\r') # Enable Home LED
        self.ser.write(b']\r') # Check Limit Status
        #x = self.ser.read() # 
        x = 10
        xi = int(x)
        print('x=' + str(xi))
        self.ser.write(b'M+23000\r') # Move at Constant Speed 23Khz
        homeNotFound = True
        while homeNotFound:
            try:
                print("Program is running")
                # Check Home
                self.ser.write(b']\r')
                #x = self.ser.read()
                #if x check bit 5

                time.sleep(0.8)
            except KeyboardInterrupt:
                print("Oh! you pressed CTRL + C.")

                self.ser.write(b'@\r') # Soft Stop
                homeNotFound = False

        self.ser.write(b'-108000\r') # Back 3 motor revs
        self.ser.write(b'+72000\r') # Up 2 motor revs
        self.ser.write(b'A24\r')    # Enable High Accuracy Circuit
        self.ser.write(b'F1000,0\r')    # Found edge Home Flag @ 1000 steps/s

        self.ser.write(b'A0\r') # Disable Home LED

    def moveStepsUp(self, value):
        """
        Writes the digital_value on pin_number
        Internally sends b'WD{pin_number}:{digital_value}' over the serial
        connection
        """
        #command = (''.join(('MX ', str(motor_number), ' ',
        #command = (''.join(('MX ', ' ',
        #    str(value)))).encode()
        #Unicode strings must be encoded (e.g. 'hello'.encode('utf-8').
        command = f'M{motor_number} {value}\r\n'.encode('utf-8')
        print(command)
        self.ser.write(command)
        line = self.ser.readline()   # read a '\n' terminated line
        print(line)

    def close(self):
        """
        To ensure we are properly closing our connection to the
        Arduino device.
        """
        self.ser.close()
        print('Connection to McPherson closed')

# vim: sta:et:sw=4:ts=4:sts=4
