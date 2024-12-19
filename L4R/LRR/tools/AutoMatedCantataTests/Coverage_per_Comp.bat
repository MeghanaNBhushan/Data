@echo on


if "%~1"=="-c" (
	echo Cantata Build Option is passed. Build Option is: %2.
	set CantataBuildOption=%~2
) else (
	set CantataBuildOption=FR5CU_DENN1_CEN_N_XX_2_uC2
)



set BATCH_DIR=%~dp0
cd /D %BATCH_DIR%

call python Coverage_per_Comp.py %CantataBuildOption%

exit %ERRORLEVEL%