#!/usr/bin/python
# The MIT License (MIT)
#
# Copyright (c) 2014 Trevor Sunderland
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#     The above copyright notice and this permission notice shall be included in all
#     copies or substantial portions of the Software.
#
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#     SOFTWARE.
#
#

import os
from time import sleep
import  threading
import Queue
import platform
from PyQt4.QtGui import *

if platform.system() =='Windows':
    import visa


debug_mode = True

def debugPrint(message):
    if debug_mode:
        print datetime.datetime.utcnow(),' ',message

DEVICE = '/dev/usbtmc0'

class usbtmc:
    """ Simple implementation of USBTMC device driver """
    def __init__(self,device):
        self.device = device
        try:
            self.FILE = os.open(device, os.O_RDWR)
        except Exception:
            QMessageBox.about(None,'ERROR','Unable to find requried device\n' +device)
            exit()

    def ask(self, message=""):
        """ Send a query to the unit and read the response."""
        self.write(message)
        return self.read()


    def write(self,command):
        """Send an arbitrary command directly to the device"""
        os.write(self.FILE,command)
        sleep(0.1)

    def read(self, length = 4000):
        """ Read an arbitary amount of data directly from the device"""
        return os.read(self.FILE, length)

    def getName(self):
        """ Return the unique identifier based on the *IDN? query"""
        seljf.write("*IDN?")
        sleep(0.10)
        return self.read(300)

    def sendReset(self):
        self.write("*RST")

    def close(self):
        """ Returns the ability for the user to press buttons"""
        self.write("SYST:LOC")


SINE,SQUARE,RAMP,PULSE,NOISE,ARB = range(0,6)
CH1, CH2 = range(6,8)
VPP,VRMS,DBM = range(8,11)

class RigolDG:
    """ Class to control the Rigol DS1000 series oscilloscope"""
    def __init__(self,device):
        self.meas = None
        if platform.system() =='Windows':
            rm = visa.ResourceManager()
            self.meas = rm.open_resource(device)
        else:
            self.meas = usbtmc(device)
        self.syncVoltage=False
        self.syncFreq=False
        self.syncFreqRatio1_2=1.0
        self.syncVoltageRatio1_2=1.0
        self.reset()


    def getName(self):
        self.write("*IDN?")
        sleep(0.01)
        return self.read()

    def reset(self):
        """ Reset the instrument"""
        self.write("*RST")


    def setFunc(self, function = None, channel = None):
        """ This sets the current function of the generator, SINE, SQUARE, NOISE, RAMP"""
        if channel == None:
            channel = CH1
        if channel == CH1:
            if function == None:
                function = SINE
            msg = "FUNC "
            if(function == SINE):
                msg+="SIN"
            elif(function == SQUARE):
                msg += "SQU"
            elif(function == RAMP):
                msg += "RAMP"
            elif(function == NOISE):
                msg += "NOIS"

            if len(msg) > 6:
                self.write(msg)

        elif channel == CH2:
            if function == None:
                function = SINE
            msg = "FUNC:CH2 "
            if(function == SINE):
                msg+="SIN"
            elif(function == SQUARE):
                msg += "SQU"
            elif(function == RAMP):
                msg += "RAMP"
            elif(function == NOISE):
                msg += "NOIS"

            if len(msg) > 9:
                self.write(msg)


    def enableChan1(self, en = True):
        """ This function enables and checks the output of the channel. Ocassionally the screen will time out and the program would have to resend the command to ensure complience. This function only needs to be called once and will retry several times if needed"""
        msg = "OUTP "
        if en:
            msg += "ON"
        else:
            msg += "OFF"
        self.write(msg)
        attempts = 1
        if en:
            while (self.ask("OUTP?") == "OFF\n\r") and en:
                self.write(msg)
                attempts += 1
                if attempts >= 5:
                    raise ValueException("Unable to Enable Channel 1!")

        else:
            while (self.ask("OUTP?") == "ON\n\r") and not en:
                self.write(msg)
                attempts +=1
                if attempts >= 5:
                    raise ValueException("Unable to Disable Channel 1!")


    def enableChan2(self, en=True):
        """ This function enables and checks the output of the channel. Ocassionally the screen will time out and the program would have to resend the command to ensure complience. This function only needs to be called once and will retry several times if needed"""
        msg = "OUTP:CH2 "
        if en:
            msg += "ON"
        else:
            msg += "OFF"
        self.write(msg)
        self.Chan2_ON = en
        attempts = 1
        if en:
            while (self.ask("OUTP:CH2?") == "OFF\n\r") and en:
                self.write(msg)
                attempts += 1
                if attempts >= 5:
                    raise ValueException("Unable to Enable Channel 2!")

        else:
            while (self.ask("OUTP:CH2?") == "ON\n\r") and not en:
                self.write(msg)
                attempts +=1
                if attempts >= 5:
                    raise ValueException("Unable to Disable Channel 2!")

    def isChan1Enabled(self):
        """ Check if we've got the ouput enabled"""
        ans = self.ask("OUTP?")
        if ans == 'ON\n\r':
            return True
        else:
            return False

    def isChan2Enabled(self):
        """ Check if we've got the ouput enabled"""
        ans = self.ask("OUTP:CH2?")
        if ans == 'ON\n\r':
            return True
        else:
            return False


    def setFreqHz(self, value=10000.0 ,channel =None):
        """ Set the frequency of the channel. Must provide frequency as a Hz value, ie 0.01Hz or 100000000Hz"""
        if(channel == None):
            if self.syncFreq:
                msg="FREQ "+str(value)
                self.write(msg)
                msg="FREQ:CH2 "+str(value * self.syncFreqRatio1_2)
                self.write(msg)
                return
            else:
                channel = CH1
        if channel == CH1:
            msg = "FREQ "+str(value)

            self.write(msg)
        elif channel == CH2:
            msg = "FREQ:CH2 " + str(value)
            self.write(msg)
        else:
            print("Unsupported channel selection")

    def write(self, message=""):
        """ send the message using the low level control"""
        self.meas.write(message)

    def read(self):
        """ read the message using the low level control"""
        return self.meas.read()

    def ask(self, message=""):
        """ request a response using the low level control"""
        self.write(message)
        sleep(0.1)
        return self.read()

    def setVoltageUnits(self,unit="VPP",channel = None):
        """ Provide string representation of voltage units"""
        if channel == None:
            if self.syncVoltage:
                msg="VOLT:UNIT "+unit
                self.write(msg)
                msg="VOLT:UNIT:CH2 " + unit
                self.write(msg)
                return

            else:
                channel = CH1

        if channel == CH1:
            msg = "VOLT:UNIT " + unit
            self.write(msg)
            msg = "VOLT "+ str(value)
            self.write(msg)
        elif channel == CH2:
            msg = "VOLT:UNIT:CH2 " + unit
            self.write(msg)
            msg = "VOLT:CH2 "+ str(value)
            self.write(msg)

        else:
            print("Unsupported channel selection")


    def setVoltage(self, value = 1.0, channel = None , offset=None):
        """ Set the current voltage and offset for the given channel. If no Channel specified, channel one is used by default"""
        if channel == None:
            if self.syncVoltage:
                msg="VOLT " + str(value)
                self.write(msg)

                msg="VOLT:CH2 "+str((float(value * self.syncVoltageRatio1_2)))
                sleep(0.1)
                self.write(msg)
                if offset is not None:
                    msg = "VOLT:OFFS " + offset
                    self.write(msg)
                if offset is not None:
                    msg = "VOLT:OFFS:CH2 " + str(offset)
                    self.write(msg)
                return

            else:
                channel = CH1

        if channel == CH1:
            msg = "VOLT "+ str(value)
            self.write(msg)
            if offset is not None:
                msg = "VOLT:OFFS " + offset
                self.write(msg)

        elif channel == CH2:
            msg = "VOLT:CH2 "+ str(value)
            self.write(msg)
            if offset is not None:
                msg = "VOLT:OFFS:CH2 " + str(offset)
                self.write(msg)
        else:
            print("Unsupported channel selection")

    def disconnect(self):
        """ Call this when you're done using the unit"""
        self.meas.close()


    def readVoltage(self, channel=None):
        """Read the current value, Channel one used when no channel specified"""
        if channel == None:
            channel = CH1
        volt = 0.0
        if channel == CH1:
            v1 = self.ask("VOLT?")
            end = len(v1)
            volt = float(v1[:end-1])
        elif channel == CH2:
            v2= self.ask("VOLT:CH2?")
            end = len (v2)
            volt = float(v2[4:end-1])
        return volt

    def readFreq(self, channel=None):
        """Read the current value, Channel one used when no channel specified"""
        if channel == None:
            channel = CH1
        freq = 0.0;
        if channel == CH1:
            f1 = self.ask("FREQ?")
            end = len(f1)
            freq = float(f1[:end-1])
        elif channel == CH2:
            f2 = self.ask("FREQ:CH2?")
            end = len(f2)
            freq = float(f2[4:end-1])
        return freq

    def readFunc(self,channel=None):
        """Read the current value, Channel one used when no channel specified"""
        if channel == None:
            channel = CH1
        func =""
        retValue = None
        if channel == CH1:
            func = self.ask("FUNC?")
        elif channel == CH2:
            func = self.ask("FUNC:CH2?")
        if "SIN" in func:
            retValue = SINE
        elif "SQU" in func:
            retValue = SQUARE
        elif "RAMP" in func:
            retValue = RAMP
        elif "NOIS" in func:
            retValue = NOISE
        return retValue

    def syncVoltages(self, sync=True, ratio_CH1 = 1.0, ratio_CH2=1.0):
        """ Handle the sincronisation of the channels here"""
        if sync:
            self.syncVoltage = True
            self.syncVoltageRatio1_2 = ratio_CH2 / ratio_CH1
        else:
            self.syncVoltage = False

    def syncFrequency(self,sync=True, ratio_CH1 = 1.0, ratio_CH2 = 1.0):
        """ Handle the sincronisation of the channels here"""
        if sync:
            self.syncFreq=True
            self.syncFreqRatio1_2 = ratio_CH2 / ratio_CH1
        else:
            self.syncFreq = False


def GetDG1022Device():
    """ Call this function to get cross platform access for the function generator"""
    if platform.system() == 'Linux':
        return RigolDG('/dev/usbtmc0')
    elif platform.system() =='Windows':
        rm = visa.ResourceManager()
        usb = filter(lambda x: 'USB' in x, rm.list_resources())
        if len(usb) != 1:
            print 'Unable to specify instruments. Please check connection and try again.'
            sys.exit(-1)
        return RigolDG(usb[0])


