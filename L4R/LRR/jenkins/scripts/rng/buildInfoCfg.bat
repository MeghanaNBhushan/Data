@echo off
setlocal EnableDelayedExpansion
REM ----------------------
REM Get HW
REM ----------------------

set hardware=%~1
IF not defined hardware (
	set hardware=FR5CU
)

IF "%hardware%"=="FR5CU" (
	python buildInfoCfg.py -uC1 -uC2
	IF not errorlevel 1 (
		exit /b 0
	) ELSE (
		exit /b -1
	)
) ELSE (
	echo HW not supported
	exit -1
)

