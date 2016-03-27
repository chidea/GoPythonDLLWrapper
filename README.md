# GoPythonDLLWrapper
A Go program that wraps python dll and scripts to make it stand-alone for Windows.

### Target machine and package
  - 32bit Windows, Python 3.4.4 (To be in compatable with Windows XP)
    - Which means if you're on 64bit Windows, you must set `$env:GOARCH = 386` on PowerShell or `set GOARCH=386` before `go build` or change contents of `lib` directory to 64 bit ones.

> This can be easily modified by replacing files and directories like `python.exe`, `pythonXY.dll`, `msvcrXXX.dll`, `lib` under `bin` directory with any version of Python you want. They're usually in Python installation directory or `%WINDIR%\System32\`.

### Possible application
  - Instantly runnable Go & Python program packages without asking user to setup Python before.
  - Multiple Python interpreters running seperately by Go routines

### Usage
  1. Build with `go build`.
  2. Put built `GoPythonDLLWrapper.exe` in `bin` directory to let it get along with other dependent files.
  3. Just think built `GoPythonDLLWrapper.exe` as the same as `python.exe`. Which means you can just `./GoPythonDLLWrapper` to open python REPL or `./GoPythonDLLWrapper main.py hello` to run `main.py` script with argument `hello` in PowerShell. (or just `GoPythonDLLWrapper` and `GoPythonDLLWrapper main.py hello` in CMD)
  4. Feel free to modify `main.go` on your need. ([Related docs](https://docs.python.org/3/c-api/index.html)) You can also rename `GoPythonDLLWrapper.exe` to anything you want.
  5. There's a batch file named `main.bat` in `bin` directory which redirects all additional arguments to another binary pointed by `CMD`. You can easily make shortcuts with this batch file in case of having multiple startpoint scripts for your project.
  
### Note
> While everyone thinks it's able to, doing so is entirely burdened on the person who is awaken to.
