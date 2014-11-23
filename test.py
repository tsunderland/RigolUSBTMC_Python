#!/usr/bin/python

import sys
from DG1022 import *

r = RigolDG('/dev/usbtmc0')

c = raw_input("Press any key to query IDN...")
r.meas.write('*IDN?')
c = raw_input("Press any key to read IDN response...")
r.meas.read()
c=raw_input("Press enter to enable Channel 1")
r.enableChan1()

c=raw_input("Press enter to enable Channel 2")
r.enableChan2()

c = raw_input("Press any key to set sync Voltages...")
r.setFunc(function=RigolDG.SQUARE,channel=RigolDG.CH1)
r.setFunc(function=RigolDG.SQUARE,channel=RigolDG.CH2)

r.syncVoltages(sync=True,ratio_CH1=2,ratio_CH2=1)
r.setVoltage(5)
c = raw_input("Press any key to set sync Frequencies...")
r.syncFrequency(sync=True,ratio_CH1=1,ratio_CH2=10)
r.setFreqHz(10000)



c = raw_input("Press any key to continue...")

r.setFreqHz(2000)
r.setVoltage(10)

r.enableChan1(False)
r.enableChan2(False)
r.setVoltage(value=5)
r.setVoltage(channel = RigolDG.CH2,value=5)
