package main

import (
	"fmt"
	"os"
	"syscall"
	"time"
	"unsafe"
)

var (
	py          = syscall.NewLazyDLL("Python35.dll")
	Init        = py.NewProc("Py_Initialize")
	Finalize    = py.NewProc("Py_Finalize")
	SetPath     = py.NewProc("Py_SetPath")
	SetProgName = py.NewProc("Py_SetProgramName")
	SetArgvEx   = py.NewProc("PySys_SetArgvEx")
	SetArgv     = py.NewProc("PySys_SetArgv")
	Run         = py.NewProc("PyRun_SimpleString")
	Main        = py.NewProc("Py_Main")
	Free        = py.NewProc("PyMem_RawFree")
)

func main() {
	//r, _, _ := SetPath.Call(
	//uintptr(unsafe.Pointer(syscall.StringToUTF16Ptr(""))))
	prog := uintptr(unsafe.Pointer(syscall.StringToUTF16Ptr("python")))
	Call(SetProgName, prog)
	//uintptr(unsafe.Pointer(syscall.StringToUTF16Ptr(path))))
	Call(Init)
	argc := len(os.Args) - 1
	argv := make([]*uint16, argc+1)
	for i, v := range os.Args[1:] {
		argv[i] = syscall.StringToUTF16Ptr(v)
	}
	argv[argc] = nil
	//Call(Main, uintptr(argc), uintptr(unsafe.Pointer(&argv)))
	Call(SetArgvEx, uintptr(unsafe.Pointer(&argv[0])), uintptr(argc), uintptr(0))
	//Call(SetArgv, uintptr(unsafe.Pointer(&argv[0])), uintptr(unsafe.Pointer(&argc)))
	//updatepath := 0
	//fmt.Println("Running", os.Args[1])
	script := syscall.StringByteSlice(`from sys import argv; print(argv)`)
	//script := syscall.StringByteSlice(`import sys; sys.argv=['idea.sh']; from imp import load_module, PY_SOURCE; f='main.py'; load_module('__main__', open(f), f, ('.py', 'r', PY_SOURCE))`)
	Call(Run, uintptr(unsafe.Pointer(&script[0])))
	Call(Finalize)
	time.Sleep(1 * time.Microsecond)
	Call(Free, prog)
}

func Call(proc *syscall.LazyProc, args ...uintptr) {
	r1, r2, le := proc.Call(args...)
	fmt.Println(r1, r2, le)
}
