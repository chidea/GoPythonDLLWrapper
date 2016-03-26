@set CMD="GoPythonDLLWrapper"

@set params=%1
@:loop
@shift
@if [%1]==[] goto afterloop
@set params=%params% %1
@goto loop
@:afterloop

@%CMD% "main.py" %params%
