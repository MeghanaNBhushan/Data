echo off
setlocal EnableDelayedExpansion

REM By default 'testmode' is disabled
set testmode=0

REM ----------------------
REM Get HW
REM ----------------------
:parseArgs
    if "%~1"=="" (
        goto start
    )
	if "%~1"=="-hw" (
		echo Hardware passed is: %2
		set hardware=%~2
	)
	if "%~1"=="-st" (
		echo Setup passed is: %2
		set setup=%~2
	)
	if "%~1"=="-filter" (
		echo Filter passed is: %2
		set filter=%~2
	)
	if "%~1"=="-testmode" (
		echo 'testmode' is enabled
		set testmode="1"
	)		
    shift
    goto parseArgs
goto:eof
:start
IF "%hardware%"=="fr5cu" (
	IF "%setup%"=="6501" (
		python framework/main/atf_main.py -t32c1 -t32c2 -t32s -hp1 -hp2 -ep1 -ep2 -r -hw fr5cu -tp -filter "%filter%" -testmode "%testmode%"
		IF not errorlevel 1 (
			exit /b 0
		) ELSE (
			exit /b -1
		)
	) ELSE IF "%setup%"=="9528" (
		python framework/main/atf_main.py -t32c1 "framework/config/lauterbach_cfg/cfg_z9528/config_uC1.t32" -t32c2 "framework/config/lauterbach_cfg/cfg_z9528/config_uC2.t32" -t32s -hp1 "./unarchive/plant_C1_uC1/C1_UC1/_init/INIT_4_LAB_TEST/*_ATR_V*_Complete.hex" -hp2 "./unarchive/plant_C1_uC2/C1_UC2/_init/INIT_4_LAB_TEST/*_ATR_V*_Complete.hex" -ep1 -ep2 -r -hw fr5cu -tp "4" -filter "%filter%" -testmode "%testmode%"
		IF not errorlevel 1 (
			exit /b 0
		) ELSE (
			exit /b -1
		)
	) ELSE IF "%setup%"=="001f2" (
		python framework/main/atf_main.py -t32c1 "framework/config/lauterbach_cfg/cfg_c001f2/config_uC1.t32" -t32c2 "framework/config/lauterbach_cfg/cfg_c001f2/config_uC2.t32" -t32s -hp1 "./unarchive/plant_C1_uC1/C1_UC1/_init/INIT_4_LAB_TEST/*_ATR_V*_Complete.hex" -hp2 "./unarchive/plant_C1_uC2/C1_UC2/_init/INIT_4_LAB_TEST/*_ATR_V*_Complete.hex" -ep1 -ep2 -r -hw fr5cu -tp "4" -filter "%filter%" -testmode "%testmode%"
		IF not errorlevel 1 (
			exit /b 0
		) ELSE (
			exit /b -1
		)
	) ELSE IF "%setup%"=="001et" (
		python framework/main/atf_main.py -t32c1 "framework/config/lauterbach_cfg/cfg_c001et/config_uC1.t32" -t32c2 "framework/config/lauterbach_cfg/cfg_c001et/config_uC2.t32" -t32s -hp1 -hp2 -ep1 -ep2 -r -hw fr5cu -tp "4" -filter "%filter%" -testmode "%testmode%"
		IF not errorlevel 1 (
			exit /b 0
		) ELSE (
			exit /b -1
		)
	) ELSE IF "%setup%"=="9168" (
		python framework/main/atf_main.py -t32c1 "framework/config/lauterbach_cfg/cfg_z9168/config_uC1.t32" -t32c2 "framework/config/lauterbach_cfg/cfg_z9168/config_uC2.t32" -t32s -hp1 "./unarchive/plant_C1_uC1/C1_UC1/_init/INIT_4_LAB_TEST/*_ATR_V*_Complete.hex" -hp2 "./unarchive/plant_C1_uC2/C1_UC2/_init/INIT_4_LAB_TEST/*_ATR_V*_Complete.hex" -ep1 -ep2 -r -hw fr5cu -tp "5" -filter "%filter%" -testmode "%testmode%"
		IF not errorlevel 1 (
			exit /b 0
		) ELSE (
			exit /b -1
		)	
	) ELSE IF "%setup%"=="7409" (
		python framework/main/atf_main.py -t32c1 "framework/config/lauterbach_cfg/cfg_z7409/config_uC1.t32" -t32c2 "framework/config/lauterbach_cfg/cfg_z7409/config_uC2.t32" -t32s -hp1 "./unarchive/plant_C1_uC1/C1_UC1/_init/INIT_4_LAB_TEST/*_ATR_V*_Complete.hex" -hp2 "./unarchive/plant_C1_uC2/C1_UC2/_init/INIT_4_LAB_TEST/*_ATR_V*_Complete.hex" -ep1 -ep2 -r -hw fr5cu -tp "4" -filter "%filter%" -testmode "%testmode%"
		IF not errorlevel 1 (
			exit /b 0
		) ELSE (
			exit /b -1
		)				
	) ELSE (
		echo Setup does not exist
		exit /b -1
	)
) ELSE (
	echo HW not supported
	exit -1
)


