# GoPythonDLLWrapper
A Go program that wraps python dll and scripts to ease up the python program distribution for windows.

### Target machine and package
  - 32bit, Python 3.4 (To be in compatable with Windows XP)

> This can be easily modified by replacing `python.exe`, `pythonXY.dll`, `libs` directory and files with any version of Python you want. They're usually in Python installation directory or `%WINDIR%\System32\`.

### Possible application
  - Go project which bootstraps Python without asking user to setup Python before.
  - Multiple Python interpreters running seperately by Go routines

### Usage
  1. Build with `go build main.go`
  2. Just think `main.exe` the same as `python.exe`. Which means you can just `./main` to open python REPL or `./main main.py hello` to run `main.py` script with argument `hello`.
  3. Feel free modify main.go for your need.

### Note
> While everyone thinks it's able to, doing so is entirely burdened on the person who is awaken to.
