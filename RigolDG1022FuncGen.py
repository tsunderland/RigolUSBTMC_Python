#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Rigol DG1022 Function Generator Interface

This application will allow the user to control the Rigol DG1022
Function generator through the Qt interface or through the command
line interface. The benefit of this being that the inbuilt ability
to control two channels frequency and voltage in a linked format.

author: Tsunderland@wabtec.com
last edited: November 2014
"""

import sys

from PyQt4.QtGui import *

class RigolDG():
    def __init__(self):
        pass

class RigolGui(QWidget):
    def __init__(self):
        super(RigolGui,self).__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300,300,250,150)
        self.setWindowTitle("Rigol DG1022DG Interface")
        self.setWindowIcon(QIcon('./Wabtec_icon.ico'))

        self.show()


def main():

    app = QApplication(sys.argv)
    fg = RigolGui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
