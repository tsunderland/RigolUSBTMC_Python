#!/usr/bin/python

import os

class usbtmc:
    """ Simple implementation of USBTMC device driver """

    def __init__(self,device):
        self.device = device
        self.FILE = os.open(device, os.O_RDWR)

        # TODO : test that the file opened.
    def write(self,command):
        os.write(self.FILE,command)

    def read(self, length = 4000):
        return os.read(self.FILE, length)

    def getName(self):
        self.write("*IDN?")
        return self.read(300)

    def sendReset(self):
        self.write("*RST")


class RigolScope:
    """ Class to control the Rigol DS1000 series oscilloscope"""
    def __init__(self,device):
        self.meas = usbtmc(device)
        self.name = self.meas.getName()
        print self.name

    def write(self,command):
        """Send an arbitrary command directly to the scope"""
        self.meas.write(command)

    def read(self, command):
        """ Read an arbitary amount of data directly from the scope"""
        return self.meas.read(command)

    def reset(self):
        """ Reset the instrument"""
        self.meas.sendReset()

    def run(self):
        self.meas.write(":RUN")

    def stop(self):
        self.meas.write(":STOP")

    def auto(self):
        self.meas.write(":AUTO")

