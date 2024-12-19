:: ----------------------------------------------------------------------------
:: Usage: Example script to use the coverity_helper.py
:: =============================================================================
::   C O P Y R I G H T
:: -----------------------------------------------------------------------------
::   Copyright (c) 2018 by Robert Bosch GmbH. All rights reserved.
:: 
::   This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
::   distribution is an offensive act against international law and may be
::   prosecuted under federal law. Its content is company confidential.
:: =============================================================================
::  Filename: coverity.bat
::  Author(s): Ingo Jauch CC-AD/ESW4 (Maintainer)
:: # ----------------------------------------------------------------------------

@echo off
set SCRIPTLOCATION=%~dp0
@rem call %SCRIPTLOCATION%\set_env.bat

SET PROJECT_ROOT=%SCRIPTLOCATION%..\..\..\..
pushd %PROJECT_ROOT%
SET PROJECT_ROOT=%CD%
popd

SET SCA_TOOL_PACKAGE_ROOT=%SCRIPTLOCATION%..\sca_tools_package
pushd %SCA_TOOL_PACKAGE_ROOT%
SET SCA_TOOL_PACKAGE_ROOT=%CD%
popd

SET PYTHON_BIN=C:\TCC\Tools\python3\3.7.4-29_WIN64\python.exe

echo -----------------------------------------------------
echo PROJECT_ROOT: %PROJECT_ROOT%
echo SCA_TOOL_PACKAGE_ROOT: %SCA_TOOL_PACKAGE_ROOT%
echo PYTHON_BIN: %PYTHON_BIN%
@rem echo COVERITY_BIN_PATH: %COVERITY_BIN_PATH%
echo -----------------------------------------------------

echo "COVERITY BATCH"
echo PROJECT_ROOT: %PROJECT_ROOT%
echo SCA_TOOL_PACKAGE_ROOT: %SCA_TOOL_PACKAGE_ROOT%

REM EnableDelayedExpansion is required for the whole script for error treatment
setlocal EnableDelayedExpansion

SET HELPER_PY=%SCA_TOOL_PACKAGE_ROOT%\sca_tools\sca_tools.py
SET DATASTORE_PATH=%SCRIPTLOCATION%coverity.json
SET DATASTORE_PATH=%SCRIPTLOCATION%coverity.json
echo HELPER_PY: %HELPER_PY%
echo DATASTORE_PATH: %DATASTORE_PATH%

SET DATASTORE_TARGET=1

setlocal EnableDelayedExpansion
echo.
IF [%1]==[] (
	:: if no args are passed, we read from a menu for input
	echo "No commandline arguments given for %~nx0"
	echo "-------------------------------------------------------"
	echo "1: FR5CU_DNNN1_NNN_N_XX_2_uC1"
	echo "2: FR5CU_DENN1_CEN_N_XX_2_uC2"
	echo "-------------------------------------------------------"
	SET /P KEYBOARD_TARGET_INPUT="Please enter input (Number or String) for TARGET: "
	echo KEYBOARD_TARGET_INPUT input was !KEYBOARD_TARGET_INPUT!

	echo.
	echo "-------------------------------------------------------"
	echo "1: create"
	echo "2: analyze"
	echo "3: export"
	echo "4: upload"
	echo "5: preview_report"
	echo "6: webapi_export"
	echo "-------------------------------------------------------"	
	SET /P KEYBOARD_OPTIONS_INPUT="Please enter input numbers for OPTIONS: "
	echo KEYBOARD_OPTIONS_INPUT input was !KEYBOARD_OPTIONS_INPUT!

	SET KEYBOARD_INPUTS=!KEYBOARD_TARGET_INPUT! !KEYBOARD_OPTIONS_INPUT!
	call :main_function !KEYBOARD_INPUTS!
) ELSE (
	:: if args were given, pass to main function
	echo calling main funtion %*
	call :main_function %*
)
goto:eof

:main_function
echo main_function
echo main args: %*

:: per default we asume the 1st is the datastore target
SET DATASTORE_TARGET=%~1
:: for developer convienience we "map" numbers to our datastore targets
IF "!DATASTORE_TARGET!"=="1" SET DATASTORE_TARGET=FR5CU_DNNN1_NNN_N_XX_2_uC1
IF "!DATASTORE_TARGET!"=="2" SET DATASTORE_TARGET=FR5CU_DENN1_CEN_N_XX_2_uC2

echo datastore target: !DATASTORE_TARGET!

SET COVERITY_COMMAND=%PYTHON_BIN% %HELPER_PY% coverity
SET COVERITY_COMMON_ARGS=-dp %DATASTORE_PATH% --datastore_target %DATASTORE_TARGET% --project_root %PROJECT_ROOT%

echo # start of option stack
shift
SET DATASTORE_TARGET_SHIFTED=false
call :loop %*
echo # end of option stack

call :pause_function
goto:eof

:loop
:: check if there is input at all
if "%~1" neq "" (
  ::first time we need to check and remeber that the 1st arg is the datastore target
  IF "!DATASTORE_TARGET_SHIFTED!"=="true" (
	echo in the loop with: %~1
	IF "%~1"=="1"	CALL :create
	IF "%~1"=="2"	CALL :analyze
	IF "%~1"=="3"	CALL :export
	IF "%~1"=="4"	CALL :upload
	IF "%~1"=="5"	CALL :preview_report
	IF "%~1"=="6"	CALL :webapi_export
	IF "%~1"=="7"	CALL :check_buildlog

	shift
  ) ELSE (
	  echo First iteration, removing target input %~1
	  SET DATASTORE_TARGET_SHIFTED=true
	  shift
  )
  goto :loop
)
goto:eof


:create
echo "create function"
echo %COVERITY_COMMAND% create %COVERITY_COMMON_ARGS% 
%COVERITY_COMMAND% create %COVERITY_COMMON_ARGS%
if not !errorlevel! equ 0 (
	goto:function_exit_gracefully
) else (
	goto :eof
)

:check_buildlog
echo "check_buildlog"
echo %COVERITY_COMMAND% check_buildlog %COVERITY_COMMON_ARGS% 
%COVERITY_COMMAND% check_buildlog %COVERITY_COMMON_ARGS% 
if not !errorlevel! equ 0 (
	goto:function_exit_gracefully
) else (
	goto :eof
)

:analyze
echo "analyze function"
echo %COVERITY_COMMAND% analyze %COVERITY_COMMON_ARGS% 
%COVERITY_COMMAND% analyze %COVERITY_COMMON_ARGS% 
if not !errorlevel! equ 0 (
	goto:function_exit_gracefully
) else (
	goto :eof
)

:export
echo "export function"
echo %COVERITY_COMMAND% export %COVERITY_COMMON_ARGS% 
%COVERITY_COMMAND% export %COVERITY_COMMON_ARGS% 
if not !errorlevel! equ 0 (
	goto:function_exit_gracefully
) else (
	goto :eof
)

:upload
echo "upload function"
echo %COVERITY_COMMAND% upload %COVERITY_COMMON_ARGS% 
%COVERITY_COMMAND% upload %COVERITY_COMMON_ARGS% 
if not !errorlevel! equ 0 (
	goto:function_exit_gracefully
) else (
	goto :eof
)

:preview_report
echo "preview_report function"
echo %COVERITY_COMMAND% preview_report %COVERITY_COMMON_ARGS% 
%COVERITY_COMMAND% preview_report %COVERITY_COMMON_ARGS% 
if not !errorlevel! equ 0 (
	goto:function_exit_gracefully
) else (
	goto :eof
)

:webapi_export
echo "preview_report function"
echo %COVERITY_COMMAND% webapi_export %COVERITY_COMMON_ARGS% 
%COVERITY_COMMAND% webapi_export %COVERITY_COMMON_ARGS% 
if not !errorlevel! equ 0 (
	goto:function_exit_gracefully
) else (
	goto :eof
)

echo "### %~nx0 end ###"
goto :eof
:function_exit_gracefully
echo ERROR: Function called from %~nx0 returned errorlevel !errorlevel!
echo "### %~nx0 end ###"
EXIT /B !errorlevel!
goto:eof

:pause_function
pause >nul
goto:eof