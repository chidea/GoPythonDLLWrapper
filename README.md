# GoPythonDLLWrapper
A Go program that wraps python dll and scripts to ease up the python program distribution for windows.

### Target machine and package
  - 32bit, Python 3.4 (To be in compatable with Windows XP)
> This can be easily modified by replacing `python.exe`, `pythonXY.dll`, `libs` directory and files with any version of Python you want.

### Possible application
  - Go project which bootstraps Python without asking user to setup Python before.
  - Multiple Python interpreters running seperately by Go routines

### Note
> While everyone thinks it's able to, doing so is entirely burdened on the person who is awaken to.
