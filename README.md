#Rigol TMC Based Scripts#

###Description###

These scripts allow you to read/write data to the Rigol DG1000 series function generators, and the DS1000 series oscilloscopes. Please contribute any additional functionality you may add. 

The DG1022_UI.py provides a pc application that allows the user to control the function generator. It has been noted that there is a quirk in the Rigol unit, where the voltage of channel two is not updated without changing the function type. 

The UI's are developed using PyQt 4.8. Once the application has been developed you can create a stand alone binary using the python installer program (See developement below).

###Development###

For development, you will need 
- Python 2.7
- PyQt 4.8
- Rigol DG1000 or DS1000 unit
- git
- (optional) PyInstaller (www.pyinstaller.org)

On Linux,
If you're wanting to use these scripts on a linux machine, please follow the instructions in the 97-RigolUSBTMC.rules header to enable read write access for the python scripts.

On Windows, 
The NI VISA runtime libraries will be needed. This process is currently being developed and this will be updated when available. 

###Issues###

The main quirk at present is that Channel 2 of the DG1022 series Function Generator requires the user to change the output function to notice any commanded change in voltage. No alternative work around has been developed yet. 

###Usage###

The gui can be called using the command
> python DG1022_UI.py

for a basic command line version of the USBTMC based interface, start python and within python 
> from DG1022 import *

> dg1022 = GetDG1022Device()

###Version History###

#### Version 0.1 ####
Initial draft. Still need to add windows support.

###ToDo Items###
- Resolve windows support
- Resolve OSX support
- Improve DS1000 series support for python command line
- Create DS1000 series GUI.

