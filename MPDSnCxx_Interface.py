import serial as pyserial
from serial.tools.list_ports import comports

class MPDSnCxx_Interface:
   
    def __init__(self, vid, pid, serial):

        self.VID = vid
        self.PID = pid
        self.SERIALNUM = serial

        self.deviceFound = False


        for port in comports():
            if self.VID and self.PID and self.SERIALNUM in port.hwid:
                print("Device found")
                print("PID: " + str(self.PID))
                print("VID: " + str(self.VID))
                print("Serial Number: " + str(self.SERIALNUM))
                print("Port Name:" + port.name)
                self.PORT = port.name
                self.deviceFound = True
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

        self.numChannels = 0

    def __del__(self):
        if(self.deviceFound):
            self.disconnectDevice()

    def deviceNotFound(self):
        
        print("\nDevice not found")
        print("PID: " + str(self.PID))
        print("VID: " + str(self.VID))
        print("Serial Number: " + str(self.SERIALNUM))      

    def connectDevice(self, baudrate=9600, bytesize=pyserial.EIGHTBITS, parity=pyserial.PARITY_NONE, 
                      stopbits=pyserial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, 
                      dsrdtr=False, write_timeout=None, inter_byte_timeout=None, exclusive=None):
        
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
        #self.SER.open()
        
    def disconnectDevice(self):
        self.SER.close()
        print("\nPort Closed")

    def printSelf(self):
        #print("")
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

    def createFastCommand(self, channel=None, frequency=None, powerP=None, powerD=None,
                  switch=None, internal=None, store=None):
    
        command = "L"
        if channel == None:
            raise Exception("The channel parameter must be set.")
        if type(channel) != int:
            raise Exception(f"The channel parameter must be an integer. ({channel=})")
        if (channel > self.numChannels or channel < 0):
            raise Exception(f"The channel parameter must be between 0 and {self.numChannels} inclusive. ({channel=})")
        command = command+str(channel)


        if (frequency != None and channel !=0):
            if (type(frequency) != float):
                raise Exception(f"The frequency parameter must be a float. ({frequency=})")
            freq = "F{0:07.3f}".format(frequency)
            command = command + freq


        if (powerP != None and powerD != None):
            raise Exception(f"Both powerP and powerD cannot be set. ({powerP=}, {powerD=})")
        
        if (powerP != None and channel !=0):
            if (type(powerP) != int):
                raise Exception(f"The powerP parameter must be an integer. ({powerP=})")
            if (powerP>=0 and powerP<=1023):
                power = "P{0:04d}".format(powerP)
                command = command + power
            else:
                raise Exception(f"powerP must be in the range of 0-1023 inclusive. ({powerP=})")
            
        if (powerD != None and channel !=0):
            if (type(powerD) != float):
                raise Exception(f"The powerD parameter must be a float. ({powerD=})")
            power = "D{0:05.2f}".format(powerD)
            command = command + power
            

        if switch != None:
            if(type(switch) != int):
                raise Exception("Switch must be of type integer")
            if switch == 0 or switch == 1:
                command = command + "O" +str(switch)
            else:
                raise Exception(f"Switch must be 0 or 1({switch=})")

        if internal != None:
            if(type(internal) != int):
                raise Exception("Internal must be of type integer")
            if internal == 0 or internal == 1:
                command = command + "I" + str(internal)
            else:
                raise Exception(f"Internal must be 0 or 1({internal=})")
            
        if (store != None and channel != 0):
            if type(store) == bool:
                if store:
                    command = command + "E"
            else:
                raise Exception("Store parameter must be type of boolean")
            
        return command

    def createSweepingCommand(self, sweeping = None, frequencyStart=None, frequencyStop=None, SweepingTime=None, store=None):
        
        command = "G"
        if sweeping == None:
            raise Exception("The sweeping parameter must be set.")
        if type(sweeping) != int:
            raise Exception(f"The sweeping parameter must be an integer. ({sweeping=})")
        if (sweeping == 0 or sweeping == 1):
            command = command+str(sweeping)
        else:
            raise Exception(f"The sweeping parameter must be 0 or 1. ({sweeping=})")


        if (frequencyStart != None):
            if (type(frequencyStart) != float):
                raise Exception(f"The frequencyStart parameter must be a float. ({frequencyStart=})")
            freqstart = "A{0:07.3f}".format(frequencyStart)
            command = command + freqstart

        if (frequencyStop != None):
            if (type(frequencyStop) != float):
                raise Exception(f"The frequencyStop parameter must be a float. ({frequencyStop=})")
            freqstop = "O{0:07.3f}".format(frequencyStop)
            command = command + freqstop

        
        if (SweepingTime != None):
            if (type(SweepingTime) != int):
                raise Exception(f"The SweepingTime parameter must be an integer. ({SweepingTime=})")
            if (SweepingTime>=1 and SweepingTime<=5000):
                time = "U{0:04d}".format(SweepingTime)
                command = command + time
            else:
                raise Exception(f"SweepingTime must be in the range of 1-5000 inclusive. ({SweepingTime=})")

        if (store != None):
            if type(store) == bool:
                if store:
                    command = command + "E"
            else:
                raise Exception("Store parameter must be type of boolean")
            
        return command

    def writeToDevice(self, command):
        command = command + "\n\r"
        self.SER.write(command.encode())

    def readStatus(self):

        self.writeToDevice("S")
        self.SER.read_until("\n\r".encode())
        line = self.SER.read_until("\n\r".encode())

        count = 0
        numChanSet = False

        print(self.SER.in_waiting)

        print("Status:", end = " ")
        while line != b"":
            print(line)
            count += 1
            if b"?" in line:

                if (not numChanSet): 
                    self.numChannels = count - 2
                    numChanSet = True
                    print(count - 2)

                self.writeToDevice("")

            line = self.SER.read_until("\n\r".encode())

        print("")

        if (not numChanSet): 
            self.numChannels = count - 3
            print(count)

    def sendQuickCommand(self, command):
        command = command + "\n\r"
        self.SER.write(command.encode())

        self.SER.read_until("\n\r".encode())


