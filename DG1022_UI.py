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
#import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from DG1022 import *


class DG1022_UI(QWidget):
    def __init__(self):
        super(DG1022_UI,self).__init__()
        self.dg1022 = GetDG1022Device()
        self.layoutScreen()
        self.curr_syncFRatio_2=1
        self.curr_syncFRatio_1=1
        self.curr_syncVRatio_2=1
        self.curr_syncVRatio_1=1
        self.prev_chan1VLCD="9.000"
        self.prev_chan2VLCD="9.000"
        self.prev_chan1FLCD="10000.00"
        self.prev_chan2FLCD="10000.00"
        self.syncFreq = False
        self.syncVolt = False

    def layoutScreen(self):
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)


        self.setStyleSheet("QGroupBox { border: 1px solid black; } ")
        self.channel1Group = QGroupBox("Channel 1:")
        self.channel2Group = QGroupBox("Channel 2:")
        self.ch1Layout = QGridLayout()
        self.ch2Layout = QGridLayout()
        self.chan1VLabel = QLabel("Voltage (V):")
        self.chan1FLabel = QLabel("Frequency (Hz):")
        self.chan1VLCD  = QLineEdit()
        self.chan1FLCD  = QLineEdit()

        self.chan1EnButton = QPushButton("Enable Output")
        self.chan1EnButton.setCheckable(True)

        self.chan1LCDLayout = QGridLayout()
        self.chan1LCDLayout.addWidget(self.chan1VLabel,0,0)
        self.chan1LCDLayout.addWidget(self.chan1VLCD,0,2)
        self.chan1LCDLayout.addWidget(self.chan1FLabel,1,0)
        self.chan1LCDLayout.addWidget(self.chan1FLCD,1,2)


        self.funcGroup1 = QGroupBox("Function:")
        #self.funcGroup1.setStyleSheet("QGroupBox { background-color: rgb(255,255,255); border:1px solid rgb (255,170,255); } ")

        self.sineRadio1 = QRadioButton("SINE")
        self.squareRadio1=QRadioButton("SQUARE")
        self.rampRadio1 = QRadioButton("RAMP")
        self.noiseRadio1= QRadioButton("NOISE")
        #self.dutyText1  = QLineEdit()
        #self.dutyLabel1 = QLabel("Duty (%)")
        self.funcGridLayout1 = QGridLayout()
        #self.dutyLayout1 = QHBoxLayout()
        #self.dutyLayout1.addWidget(self.dutyLabel1)
        #self.dutyLayout1.addWidget(self.dutyText1)

        self.funcGridLayout1.addWidget(self.sineRadio1,0,0)
        self.funcGridLayout1.addWidget(self.squareRadio1,0,1)
        self.funcGridLayout1.addWidget(self.rampRadio1,1,0)
        self.funcGridLayout1.addWidget(self.noiseRadio1,1,1)
        #self.funcGridLayout1.addLayout(self.dutyLayout1,2,1)

        self.funcGroup1.setLayout(self.funcGridLayout1)
        #self.mainLayout.addWidget(self.funcGroup1,0,0)
        #self.dutyText1.setText("50")
        #self.dutyText1.setEnabled(False)

        self.ch1Layout.addLayout(self.chan1LCDLayout,0,0,2,1)
        self.ch1Layout.addWidget(self.funcGroup1,2,0,3,1)
        self.ch1Layout.addWidget(self.chan1EnButton,5,0,1,1)
        self.channel1Group.setLayout(self.ch1Layout)
        self.mainLayout.addWidget(self.channel1Group,0,0,4,1)


        self.chan2VLabel = QLabel("Voltage (V):")
        self.chan2FLabel = QLabel("Frequency (Hz):")
        self.chan2VLCD  = QLineEdit()
        self.chan2FLCD  = QLineEdit()
        #self.chan1VLCD.setValue(9.0000)
        #self.chan1FLCD.setValue(10000.00)
        self.chan2EnButton = QPushButton("Enable Output")
        self.chan2EnButton.setCheckable(True)

        self.chan2VLayout = QHBoxLayout()
        self.chan2LCDLayout = QGridLayout()
        self.chan2LCDLayout.addWidget(self.chan2VLabel,0,0)
        self.chan2LCDLayout.addWidget(self.chan2VLCD,0,2)
        self.chan2LCDLayout.addWidget(self.chan2FLabel,1,0)
        self.chan2LCDLayout.addWidget(self.chan2FLCD,1,2)
        self.funcGroup2 = QGroupBox("Function:")

        self.sineRadio2 = QRadioButton("SINE")
        self.squareRadio2=QRadioButton("SQUARE")
        self.rampRadio2 = QRadioButton("RAMP")
        self.noiseRadio2= QRadioButton("NOISE")

        #self.dutyText2  = QLineEdit()
        #self.dutyLabel2 = QLabel("Duty (%)")
        self.funcGridLayout2 = QGridLayout()
        #self.dutyLayout2 = QHBoxLayout()
        #self.dutyLayout2.addWidget(self.dutyLabel2)
        #self.dutyLayout2.addWidget(self.dutyText2)

        self.funcGridLayout2.addWidget(self.sineRadio2,0,0)
        self.funcGridLayout2.addWidget(self.squareRadio2,0,1)
        self.funcGridLayout2.addWidget(self.rampRadio2,1,0)
        self.funcGridLayout2.addWidget(self.noiseRadio2,1,1)
        #self.funcGridLayout2.addLayout(self.dutyLayout2,2,1)

        self.funcGroup2.setLayout(self.funcGridLayout2)
        #self.dutyText2.setText("50")
        #self.dutyText2.setEnabled(False)


        self.ch2Layout.addLayout(self.chan2LCDLayout,0,0,2,1)
        self.ch2Layout.addWidget(self.funcGroup2,2,0,3,1)
        self.ch2Layout.addWidget(self.chan2EnButton,5,0,1,1)
        self.channel2Group.setLayout(self.ch2Layout)
        self.mainLayout.addWidget(self.channel2Group,0,1,4,1)

        #Sync events
        self.syncGroup = QGroupBox("Channel Sync Settings:")
        self.syncLayout = QGridLayout()
        self.syncCH1Label = QLabel("CH1")
        self.syncCH2Label = QLabel("CH2")
        self.syncVCheck     = QCheckBox("Voltage")
        self.syncFCheck     = QCheckBox("Frequency")
        self.syncVRatio_1   = QLineEdit()
        self.syncVRatio_2   = QLineEdit()
        self.syncVRatioCol  = QLabel(":")
        self.syncFRatioCol  = QLabel(":")
        self.syncFRatio_1   = QLineEdit()
        self.syncFRatio_2   = QLineEdit()
        self.syncLayout.addWidget(self.syncCH1Label,0,2,Qt.AlignCenter)
        self.syncLayout.addWidget(self.syncCH2Label,0,4,Qt.AlignCenter)
        self.syncLayout.addWidget(self.syncVCheck,1,1)
        self.syncLayout.addWidget(self.syncVRatio_1,1,2)
        self.syncLayout.addWidget(self.syncVRatioCol,1,3)
        self.syncLayout.addWidget(self.syncVRatio_2,1,4)
        self.syncLayout.addWidget(self.syncFCheck,2,1)
        self.syncLayout.addWidget(self.syncFRatio_1,2,2)
        self.syncLayout.addWidget(self.syncFRatioCol,2,3)
        self.syncLayout.addWidget(self.syncFRatio_2,2,4)
        self.syncGroup.setLayout(self.syncLayout)
        self.mainLayout.addWidget(self.syncGroup,4,0,1,2)

        self.syncFRatio_1.setText("1")
        self.syncFRatio_2.setText("1")
        self.syncVRatio_1.setText("1")
        self.syncVRatio_2.setText("1")

        func1 = self.dg1022.readFunc(CH1)
        func2 = self.dg1022.readFunc(CH2)

        self.sineRadio1.setChecked(func1 == SINE)
        self.squareRadio1.setChecked(func1 == SQUARE)
        self.rampRadio1.setChecked(func1 == RAMP)
        self.noiseRadio1.setChecked(func1 == NOISE)

        self.sineRadio2.setChecked(func2 == SINE)
        self.squareRadio2.setChecked(func2 == SQUARE)
        self.rampRadio2.setChecked(func2 == RAMP)
        self.noiseRadio2.setChecked(func2 == NOISE)

        self.chan1VLCD.setText(str(self.dg1022.readVoltage(CH1)))
        self.chan2VLCD.setText(str(self.dg1022.readVoltage(CH2)))
        self.chan1FLCD.setText(str(self.dg1022.readFreq(CH1)))
        self.chan2FLCD.setText(str(self.dg1022.readFreq(CH2)))


        self.syncFRatio_1.setAlignment(Qt.AlignRight)
        self.syncFRatio_2.setAlignment(Qt.AlignRight)
        self.syncVRatio_1.setAlignment(Qt.AlignRight)
        self.syncVRatio_2.setAlignment(Qt.AlignRight)
        self.chan1VLCD.setAlignment(Qt.AlignRight)
        self.chan2VLCD.setAlignment(Qt.AlignRight)
        self.chan1FLCD.setAlignment(Qt.AlignRight)
        self.chan2FLCD.setAlignment(Qt.AlignRight)

        #Handle the events
        self.chan1VLCD.editingFinished.connect(self.chan1VChanged)
        self.chan1FLCD.editingFinished.connect(self.chan1FChanged)
        self.chan2VLCD.editingFinished.connect(self.chan2VChanged)
        self.chan2FLCD.editingFinished.connect(self.chan2FChanged)
        self.syncVCheck.stateChanged.connect(self.syncVoltage)
        self.syncFCheck.stateChanged.connect(self.syncFrequency)
        self.chan1EnButton.clicked[bool].connect(self.chan1Enable)
        self.chan2EnButton.clicked[bool].connect(self.chan2Enable)
        self.syncVRatio_1.editingFinished.connect(self.syncVRatio1Changed)
        self.syncVRatio_2.editingFinished.connect(self.syncVRatio2Changed)
        self.syncFRatio_1.editingFinished.connect(self.syncFRatio1Changed)
        self.syncFRatio_2.editingFinished.connect(self.syncFRatio2Changed)
        self.sineRadio1.toggled.connect(self.setChan1Sine)
        self.sineRadio2.toggled.connect(self.setChan2Sine)
        self.squareRadio1.toggled.connect(self.setChan1Square)
        self.squareRadio2.toggled.connect(self.setChan2Square)
        self.rampRadio1.toggled.connect(self.setChan1Ramp)
        self.rampRadio2.toggled.connect(self.setChan2Ramp)
        self.noiseRadio1.toggled.connect(self.setChan1Noise)
        self.noiseRadio2.toggled.connect(self.setChan2Noise)


        self.chan1EnButton.setChecked(self.dg1022.isChan1Enabled())
        self.chan2EnButton.setChecked(self.dg1022.isChan2Enabled())

        #Setup Main Display
        self.setGeometry(300,300,300,350)
        self.setWindowTitle('Rigol Function Generator')
        self.show()

    def closeEvent(self,event):
        self.dg1022.disconnect()
        super(DG1022_UI,self).closeEvent(event)

    def chan1Enable(self,checked):
        self.dg1022.enableChan1(checked)

    def chan2Enable(self,checked):
        self.dg1022.enableChan2(checked)

    def setChan1Sine(self):
        self.dg1022.setFunc(SINE,CH1)
    def setChan2Sine(self):
        self.dg1022.setFunc(SINE,CH2)
    def setChan1Square(self):
        self.dg1022.setFunc(SQUARE,CH1)
    def setChan2Square(self):
        self.dg1022.setFunc(SQUARE,CH2)
    def setChan1Ramp(self):
        self.dg1022.setFunc(RAMP,CH1)
    def setChan2Ramp(self):
        self.dg1022.setFunc(RAMP,CH2)
    def setChan1Noise(self):
        self.dg1022.setFunc(NOISE,CH1)
    def setChan2Noise(self):
        self.dg1022.setFunc(NOISE,CH2)

    def syncVoltage(self):
        self.syncVolt = self.syncVCheck.isChecked()
        if self.syncVCheck.isChecked():
            self.chan2VLCD.setEnabled(False)
            self.dg1022.syncVoltages(True, float(self.syncVRatio_1.text()), float(self.syncVRatio_2.text()))
        else:
            self.chan2VLCD.setEnabled(True)
            self.dg1022.syncVoltages(False)


    def syncFrequency(self):
        self.syncFreq = self.syncFCheck.isChecked()
        if self.syncFCheck.isChecked():

            self.chan2FLCD.setEnabled(False)
            self.dg1022.syncFrequency(True, float(self.syncFRatio_1.text()), float(self.syncFRatio_2.text()))
        else:
            self.chan2FLCD.setEnabled(True)
            self.dg1022.syncFrequency(False)

    def checkVRatio(self):
        chan1 = float(self.chan1VLCD.text())
        chan2 = float(self.chan2VLCD.text())
        rat1 = float(self.syncVRatio_1.text())
        rat2 = float(self.syncVRatio_2.text())

        return True

    def checkFRatio(self):
        return True

    def chan1VChanged(self):
        if self.chan1VLCD.text() == self.prev_chan1VLCD:
            return
        try:
            txt = self.chan1VLCD.text()
            number = float(txt)

            if (number < 0.0):
                raise ValueError("Number is lower than MIN allowed voltage (0)")
            if number > 20.0:
                raise ValueError("Number is greater than MAX allowed voltage (20V)")

            if self.syncVolt:
                if not self.checkVRatio():
                    raise ValueError("Voltage ration not in range")
                ch2 = number * float(self.curr_syncVRatio_1) / float(self.curr_syncVRatio_2)
                self.chan2VLCD.setText(str(ch2))
            self.prev_chan1VLCD = str(number)
            self.dg1022.setVoltage(value=number,channel = CH1)
            if self.syncVolt:
                self.dg1022.setVoltage(value = ch2,channel=CH2)
        except ValueError,e:
            QMessageBox.about(self,'Error','Value Error')
            self.chan1VLCD.setText(self.prev_chan1VLCD)
        except:
            QMessageBox.about(self,'Error','Unable to handle input')
            self.chan1VLCD.setText(self.prev_chan1VLCD)

    def chan1FChanged(self):
        number = self.chan1FLCD.text()
        if number == self.prev_chan1FLCD:
            return
        try:
            number = float(number)
            if number < 0:
                raise Exception


            if self.syncFreq:
                if not self.checkFRatio():
                    raise ValueError("Frequency not in ratio Range")
                ch2 = number * self.curr_syncFRatio_1 / self.curr_syncFRatio_2
                self.chan2FLCD.setText(str(ch2))
            print("Setting freq")
            self.dg1022.setFreqHz(value = number, channel = CH1)
            print("Checking Sync settings")
            if self.syncFreq:
                self.dg1022.setFreqHz(value = ch2,channel = CH2)
            self.prev_chan1FLCD = str(number)
        except ValueError,e:
            QMessageBox.about(self,'Error',e)
            self.chan1FLCD.setText(self.prev_chan1FLCD)
        except Exception:
            QMessageBox.about(self,'Error','Input can only be a number greater than 0')
            self.chan1FLCD.setText(self.prev_chan1FLCD)


    def chan2VChanged(self):
        number = self.chan2VLCD.text()
        if number == self.prev_chan2VLCD:
            return
        try:
            number = float(number)
            if number < 0:
                raise Exception
            if number > 20:
                raise Exception
            self.prev_chan2VLCD = str(number)
            self.dg1022.setVoltage(value = number,channel=CH2)
        except Exception:
            QMessageBox.about(self,'Error','Input can only be a number greater than 0')
            self.chan2VLCD.setText(self.prev_chan2VLCD)

    def chan2FChanged(self):
        number = self.chan2FLCD.text()
        if number == self.prev_chan2FLCD:
            return
        try:
            number = float(number)
            if number < 0:
                raise Exception


            self.dg1022.setFreqHz(value = number, channel = CH2)
            self.prev_chan2FLCD = str(number)
        except ValueError,e:
            QMessageBox.about(self,'Error',e)
            self.chan2FLCD.setText(self.prev_chan2FLCD)
        except Exception:
            QMessageBox.about(self,'Error','Input can only be a number greater than 0')
            self.chan2FLCD.setText(self.prev_chan2FLCD)

    def syncVRatio1Changed(self):
        number = self.syncVRatio_1.text()
        if number == self.curr_syncVRatio_1:
            return
        try:
            number = float(number)
            if number < 0:
                raise Exception
            if self.syncVolt:
                self.checkVRatio()

            self.curr_syncVRatio_1 = self.syncVRatio_1.text()

            self.dg1022.syncVoltages(True, float(self.syncVRatio_1.text()), float(self.syncVRatio_2.text()))
        except Exception:
            QMessageBox.about(self,'Error','Input can only be a number greater than 0')
            self.syncVRatio_1.setText(str(self.curr_syncVRatio_1))


    def syncVRatio2Changed(self):
        number = self.syncVRatio_2.text()
        if number == self.curr_syncVRatio_2:
            return
        try:
            number = float(number)
            if number < 0:
                raise Exception
            if self.syncVolt:
                self.checkVRatio()
            self.curr_syncVRatio_2 = self.syncVRatio_2.text()
            self.dg1022.syncVoltages(True, float(self.syncVRatio_1.text()), float(self.syncVRatio_2.text()))
        except Exception:
            QMessageBox.about(self,'Error','Input can only be a number greater than 0')
            self.syncVRatio_2.setText(str(self.curr_syncVRatio_2))


    def syncFRatio1Changed(self):
        number = self.syncFRatio_1.text()
        if number == self.curr_syncFRatio_2:
            return
        try:
            number = float(number)
            if number < 0:
                raise Exception
            if self.syncFreq:
                self.checkFRatio()
            self.curr_syncFRatio_1 = self.syncFRatio_1.text()
            self.dg1022.syncFrequency(True, float(self.syncFRatio_1.text()), float(self.syncFRatio_2.text()))
        except Exception:
            QMessageBox.about(self,'Error','Input can only be a number greater than 0')
            self.syncFRatio_1.setText(str(self.curr_syncFRatio_1))

    def syncFRatio2Changed(self):
        number = self.syncFRatio_2.text()
        if number == self.curr_syncFRatio_2:
            return
        try:
            number = float(number)
            if number < 0:
                raise Exception
            if self.syncFreq:
                self.checkFRatio()
            self.curr_syncFRatio_2 = self.syncFRatio_2.text()
            self.dg1022.syncFrequency(True, float(self.syncFRatio_1.text()), float(self.syncFRatio_2.text()))
        except Exception:
            QMessageBox.about(self,'Error','Input can only be a number greater than 0')
            self.syncFRatio_2.setText(str(self.curr_syncFRatio_2))



def main():
    app = QApplication(sys.argv)
    dg = DG1022_UI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
