@echo on

:parseArgs
    if "%~1"=="" (
        goto start
    )
	if "%~1"=="-c" (
		echo Cantata Build Option is passed. Build Option is: %2.
		set CantataBuildOption=%~2
	)
	if "%~1"=="-bt" (
		echo Build Type. Partial or Full is: %2.
		set BuildType=%~2
	)
    shift
    goto parseArgs
goto:eof
:start

if not defined CantataBuildOption (
	set CantataBuildOption=FR5CU_DENN1_CEN_N_XX_2_uC2
)
if not defined BuildType (
	set BuildType=full
)
IF %CantataBuildOption%==FR5CU_DENN1_CEN_N_XX_2_uC2 (
set variant=Radar_FR5CU_DENN1_CEN_N_XX_2_uC2 
set hardware=FR5CU_DENN1_CEN_N_XX_2_uC2
)

IF %CantataBuildOption%==FR5CU_DNNN1_NNN_N_XX_2_uC1 (
set variant=Radar_FR5CU_DNNN1_NNN_N_XX_2_uC1 
set hardware=FR5CU_DNNN1_NNN_N_XX_2_uC1 
)


set BATCH_DIR=%~dp0
cd /D %BATCH_DIR%

echo Cantata build option .......... %CantataBuildOption%
echo Build Type           .......... %BuildType%
call python AutomaticCantataHostExec.py -c %CantataBuildOption% -v %variant% -bt %BuildType%

set errorValue=%ERRORLEVEL%
if %errorValue% equ 1 (
	exit 0
) else (
	if %errorValue% neq 0 (
		exit -1
	) else (
		exit 0
	)
)
