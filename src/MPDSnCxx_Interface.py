import sys
import serial as pyserial
from serial.tools.list_ports import comports

class MPDSnCxx_Interface:
    def __init__(self, vid, pid, serial):

        self.VID = vid
        self.PID = pid
        self.SERIALNUM = serial

        self.device_found = False

        for port in comports():
            if self.VID and self.PID and self.SERIALNUM in port.hwid:
                print("Device found")
                print("PID: " + str(self.PID))
                print("VID: " + str(self.VID))
                print("Serial Number: " + str(self.SERIALNUM))
                print("Port Name:" + port.name)
                self.PORT = port.name
                self.device_found = True
                break

        self.BAUDRATE = 9600                    # integer
        self.BYTESIZE = pyserial.EIGHTBITS      # possible values are five, six, seven, eight
        self.PARITY = pyserial.PARITY_NONE      # possible values are none, even, odd, mark, space
        self.STOPBITS = pyserial.STOPBITS_ONE   # possible values are one, one_point_five, two
        self.TIMEOUT = None                     # float, CAN BE NONE
        self.XONXOFF = False                    # boolean
        self.RTSCTS = False                     # boolean
        self.DSRDTR = False                     # boolean
        self.WRITE_TIMEOUT = None               # float, CAN BE NONE
        self.INTER_BYTE_TIMEOUT = None          # float, CAN BE NONE
        self.EXCLUSIVE = None                   # boolean, CAN BE NONE
        self.num_channels = 0
        
        #check if device is found, if not return
        if not self.device_found:
            self.__device_not_found()
            raise RuntimeError("Device not found")

    def __del__(self):
        if self.device_found:
            self.disconnect_device()

    def __device_not_found(self):
        print("\nDevice not found")
        print("PID: " + str(self.PID))
        print("VID: " + str(self.VID))
        print("Serial Number: " + str(self.SERIALNUM))      

    def connect_device(self, baudrate=9600, bytesize=pyserial.EIGHTBITS, parity=pyserial.PARITY_NONE, 
                      stopbits=pyserial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, 
                      dsrdtr=False, write_timeout=None, inter_byte_timeout=None, exclusive=None):
        """ Connect to the MPDSnCxx Interface.

        Parameters
        ----------
        baudrate : int, optional
            baudrate, by default 9600
        bytesize : _type_, optional
            bytesize, by default pyserial.EIGHTBITS
        parity : _type_, optional
            parity, by default pyserial.PARITY_NONE
        stopbits : _type_, optional
            stopbits, by default pyserial.STOPBITS_ONE, 
        timeout : float, optional
            timeout, by default None
        xonxoff : bool, optional
            xonxoff, by default False
        rtscts : bool, optional
            rtscts, by default False
        dsrdtr : bool, optional
            dsrdtr, by default False
        write_timeout : float, optional
            write_timeout, by default None
        inter_byte_timeout : float, optional
            inter_byte_timeout, by default None
        exclusive : boolean, optional
            exclusive, by default None
        """
        
        self.BAUDRATE = baudrate                        # integer
        self.BYTESIZE = bytesize                        # possible values are five, six, seven, eight
        self.PARITY = parity                            # possible values are none, even, odd, mark, space
        self.STOPBITS = stopbits                        # possible values are one, one_point_five, two
        self.TIMEOUT = timeout                          # float, CAN BE NONE
        self.XONXOFF = xonxoff                          # boolean
        self.RTSCTS = rtscts                            # boolean
        self.DSRDTR = dsrdtr                            # boolean
        self.WRITE_TIMEOUT = write_timeout              # float, CAN BE NONE
        self.INTER_BYTE_TIMEOUT = inter_byte_timeout    # float, CAN BE NONE
        self.EXCLUSIVE = exclusive                      # boolean, CAN BE NONE


        self.SER = pyserial.Serial(port=self.PORT, baudrate=baudrate, bytesize=bytesize, parity=parity,
                                 stopbits=stopbits, timeout=timeout, xonxoff=xonxoff, rtscts=rtscts,
                                 dsrdtr=dsrdtr, write_timeout=write_timeout, 
                                 inter_byte_timeout=inter_byte_timeout, exclusive=exclusive)
    
    def disconnect_device(self):
        """Disconnect from the MPDSnCxx Radio Frequency Driver
        """
        self.SER.close()
        print("\nPort Closed")
        
        self.device_found = False

    def print_self(self):
        """Print to terminal the settings for the USB connection
        """
        print("\nPort:" + str(self.PORT))
        print("Baudrate: "+ str(self.BAUDRATE))
        print("Bytesize: "+ str(self.BYTESIZE))
        print("Parity: "+ str(self.PARITY))
        print("Stopbits: "+ str(self.STOPBITS))
        print("Timeout: "+ str(self.TIMEOUT))   
        print("XONXOFF: "+ str(self.XONXOFF))
        print("RTSCTS: "+ str(self.RTSCTS))
        print("DSRDT: "+ str(self.DSRDTR))
        print("Inter Byte Timeout: "+ str(self.INTER_BYTE_TIMEOUT))
        print("Write Timeout: "+ str(self.WRITE_TIMEOUT))
        print("Exclusive: "+ str(self.EXCLUSIVE))

    def create_fast_command(self, channel=None, frequency=None, powerP=None, powerD=None,
                  switch=None, internal=None, store=None):
        """Create formatted quick command to set the MPDSnCxx Radio Frequency Driver in normal mode \n
        FULL Command: LxFfff.ffPppppDdd.ddOoIiE

        Parameters
        ----------
        channel : int,
            Channel selection (x= 1 to 8 for channels, 0 for BLK selection[Oo, Ii, only] )
        frequency : float, optional
            Frequency adjustment (fff.ff = frequency value ex-142.26 - MHz, by default None
        powerP : int, optional
            Power adjustment (pppp = 0 to 1023), by default None
        powerD : float, optional
            Power adjustment (dBm, ex dd.dd=17.45), by default None
        switch : int, optional
            Switch ON/OFF (o=1/0), by default None
        internal : int, optional
            Internal mode ON/OFF (i=1/0), by default None
        store : int, optional
            Immediate store, by default None

        Returns
        -------
        String
            normal operation command to be sent to MPDSnCxx Radio Frequency Driver
        """
    
        command = "L"
        if channel is None:
            raise Exception("The channel parameter must be set.")
        if not(isinstance(channel, int)):
            raise Exception(f"The channel parameter must be an integer. ({channel=})")
        if (channel > self.num_channels or channel < 0):
            raise Exception(f"The channel parameter must be between 0 and {self.num_channels} inclusive. ({channel=})")
        command = command+str(channel)


        if ((frequency is not None) and channel !=0):
            if not(isinstance(frequency,float)):
                raise Exception(f"The frequency parameter must be a float. ({frequency=})")
            freq = f"F{frequency:07.3f}"
            command = command + freq


        if ((powerP is not None) and (powerD is not None)):
            raise Exception(f"Both powerP and powerD cannot be set. ({powerP=}, {powerD=})")
        
        if ((powerP is not None) and channel !=0):
            if not(isinstance(powerP,int)):
                raise Exception(f"The powerP parameter must be an integer. ({powerP=})")
            if (powerP>=0 and powerP<=1023):
                power = f"P{powerP:04d}"
                command = command + power
            else:
                raise Exception(f"powerP must be in the range of 0-1023 inclusive. ({powerP=})")
            
        if ((powerD is not None) and channel !=0):
            if not(isinstance(powerD,float)):
                raise Exception(f"The powerD parameter must be a float. ({powerD=})")
            power = f"D{powerD:05.2f}"
            command = command + power

        if switch is not None:
            if not(isinstance(switch,int)):
                raise Exception("Switch must be of type integer")
            if switch == 0 or switch == 1:
                command = command + "O" +str(switch)
            else:
                raise Exception(f"Switch must be 0 or 1({switch=})")

        if internal is not None:
            if not(isinstance(internal,int)):
                raise Exception("Internal must be of type integer")
            if internal == 0 or internal == 1:
                command = command + "I" + str(internal)
            else:
                raise Exception(f"Internal must be 0 or 1({internal=})")
            
        if ((store is not None) and channel != 0):
            if isinstance(store,bool):
                if store:
                    command = command + "E"
            else:
                raise Exception("Store parameter must be type of boolean")
            
        return command

    def create_sweeping_command(self, sweeping = None, frequency_start=None, frequency_stop=None, sweeping_time=None, store=None):
        """Create formatted quick command to set the MPDSnCxx Radio Frequency Driver in sweeping mode \n
        FULL Command: GgAfff.fffOfff.fffUuuuuE (applies on channel 1 only)

        Parameters
        ----------
        sweeping : int
            Sweeping mode - OFF/ON - g=0/1, by default None
        frequencyStart : float, optional
            Start frequency (fff.ff = frequency value ex-75.206 – MHz), by default None
        frequencyStop : float, optional
            Stop frequency (fff.ff = frequency value ex-84.260 – MHz), by default None
        SweepingTime : int, optional
            Sweeping time in microseconds by steps of 1μs from 1 to 5000, by default None
        store : bool, optional
            Immediate store, by default None

        Returns
        -------
        String
            sweeping command to be sent to MPDSnCxx Radio Frequency Driver
        """
        command = "G"
        if sweeping is None:
            raise Exception("The sweeping parameter must be set.")
        if not(isinstance(sweeping,int)):
            raise Exception(f"The sweeping parameter must be an integer. ({sweeping=})")
        if (sweeping == 0 or sweeping == 1):
            command = command+str(sweeping)
        else:
            raise Exception(f"The sweeping parameter must be 0 or 1. ({sweeping=})")


        if (frequency_start is not None):
            if not(isinstance(frequency_start,float)):
                raise Exception(f"The frequencyStart parameter must be a float. ({frequency_start=})")
            freqstart = f"A{frequency_start:07.3f}"
            command = command + freqstart

        if (frequency_stop is not None):
            if not(isinstance(frequency_stop,float)):
                raise Exception(f"The frequencyStop parameter must be a float. ({frequency_stop=})")
            freqstop = f"O{frequency_stop:07.3f}"
            command = command + freqstop

        
        if (sweeping_time is not None):
            if not(isinstance(sweeping_time,int)):
                raise Exception(f"The SweepingTime parameter must be an integer. ({sweeping_time=})")
            if (sweeping_time>=1 and sweeping_time<=5000):
                time = f"U{sweeping_time:04d}"
                command = command + time
            else:
                raise Exception(f"SweepingTime must be in the range of 1-5000 inclusive. ({sweeping_time=})")

        if (store is not None):
            if isinstance(store,bool):
                if store:
                    command = command + "E"
            else:
                raise Exception("Store parameter must be type of boolean")
            
        return command

    def __write_to_device(self, command):
        command = command + "\n\r"
        self.SER.write(command.encode())

    def read_status(self, long_form=False):
        """Read the status of MPDSnCxx Radio Frequency Driver
        
        Parameters
        ----------
        long_form : bool
            Display all the status, by default False
        """
        self.__write_to_device("S")
        self.SER.read_until("\n\r".encode())
        line = self.SER.read_until("\n\r".encode())

        count = 0
        num_chan_set = False
        bPassed = False

        print("Status:\n", end = " ")
        while line != b"":
            
            if not bPassed:
                print(line)
            elif long_form:
                print(line)
                
            count += 1
            if b"?" in line:
                bPassed = True
                if not num_chan_set: 
                    self.num_channels = count - 2
                    num_chan_set = True
                self.__write_to_device("")

            line = self.SER.read_until("\n\r".encode())

        print("")

        if (not num_chan_set): 
            self.num_channels = count - 3

    def send_quick_command(self, command):
        """Sends a command to MPDSnCxx Radio Frequency Driver

        Parameters
        ----------
        command : String
            Formated command to be sent
        """
        command = command + "\n\r"
        self.SER.write(command.encode())

        self.SER.read_until("\n\r".encode())

