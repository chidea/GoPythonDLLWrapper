package main

import (
	"fmt"
	"os"
	"runtime"
	"syscall"
	"time"
	"unsafe"
)

var (
	py          = syscall.NewLazyDLL("Python34.dll")
	Init        = py.NewProc("Py_Initialize")
	Finalize    = py.NewProc("Py_Finalize")
	SetPath     = py.NewProc("Py_SetPath")
	SetProgName = py.NewProc("Py_SetProgramName")
	SetArgvEx   = py.NewProc("PySys_SetArgvEx")
	SetArgv     = py.NewProc("PySys_SetArgv")
	Run         = py.NewProc("PyRun_SimpleString")
	Main        = py.NewProc("Py_Main")
	Free        = py.NewProc("PyMem_RawFree")
	RawMalloc   = py.NewProc("PyMem_RawMalloc")
	Decode      = py.NewProc("Py_DecodeLocale")
)

func main() {
	runtime.GOMAXPROCS(runtime.NumCPU()) // use all physical cores. for in your case of using go routines

	//prog := uintptr(unsafe.Pointer(syscall.StringToUTF16Ptr("python")))
	//Call(SetProgName, prog)

	/*  Example : Imply target script and pass every argument to there */
	/*argc := len(os.Args) + 1
	argv := make([]uintptr, argc+1)
	argv[1] = uintptr(unsafe.Pointer(syscall.StringToUTF16Ptr("main.py")))
	for i, v := range os.Args[1:] {
		argv[i+2] = uintptr(unsafe.Pointer(syscall.StringToUTF16Ptr(v)))
	}*/

	/*  Example : Simplest wrapper */
	argc := len(os.Args)
	argv := make([]uintptr, argc)
	for i, v := range os.Args[1:] {
		argv[i+1] = uintptr(unsafe.Pointer(syscall.StringToUTF16Ptr(v)))
	}

	Call(Init)
	s := time.Now()
	Call(Main, uintptr(argc), uintptr(unsafe.Pointer(&argv[0])))
	//updatepath := 0
	e := time.Since(s)
	fmt.Println("Execution time :", e)
	/* Example : inline script instead of external script execution */
	//script := syscall.StringByteSlice(`from sys import argv; print(argv)`)
	//script := syscall.StringByteSlice(`import sys; sys.argv=['idea.sh']; from imp import load_module, PY_SOURCE; f='main.py'; load_module('__main__', open(f), f, ('.py', 'r', PY_SOURCE))`)
	//Call(Run, uintptr(unsafe.Pointer(&script[0])))

	Call(Finalize)
	time.Sleep(1 * time.Microsecond)
}

func Call(proc *syscall.LazyProc, args ...uintptr) uintptr {
	r1, r2, le := proc.Call(args...)
	//fmt.Println(r1, r2, le) // Debug purpose
	_, _ = r2, le
	return r1
}
