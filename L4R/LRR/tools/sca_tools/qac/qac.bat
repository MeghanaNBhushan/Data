:: ----------------------------------------------------------------------------
:: Usage: Example script to use the sca_tools.py qac
:: =============================================================================
::   C O P Y R I G H T
:: -----------------------------------------------------------------------------
::   Copyright (c) 202X (TODO) by Robert Bosch GmbH. All rights reserved.
:: 
::   This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
::   distribution is an offensive act against international law and may be
::   prosecuted under federal law. Its content is company confidential.
:: =============================================================================
::  Filename: qac.bat
::  Author(s): TODO HERE THE INTEGRATOR NAME (MY BOSCH DEPARTMENT)
:: # ----------------------------------------------------------------------------
@echo off
set SCRIPTLOCATION=%~dp0

SET PROJECT_ROOT=%SCRIPTLOCATION%..\..\..\..
pushd %PROJECT_ROOT%
set PROJECT_ROOT=%CD%

echo "PROJECT_ROOT" %PROJECT_ROOT%
echo "SCA QAC BATCH"
echo "Arguments order: target helper_option json_config_path changed_files_file_path enable_quality_gate"

:: Setup path to support run qt,qnx,cmake,cygwin and boost
SET PYTHON_EXE=C:\TCC\Tools\python3\3.9.1-1_WIN64\python.exe
SET GHS_IFX_HOME=C:\TCC\Tools\greenhills_ifx\comp_201815_9fp_WIN64
SET DATASTORE_TARGET=default
echo.
IF [%1]==[] (
   echo "No commandline for 1st arg given, please choose a target from the datastore (e.g. qac.json)"
   echo "Options:"
   echo "FR5CU_DNNN1_NNN_N_XX_2_uC1"
   echo "FR5CU_DENN1_CEN_N_XX_2_uC2"
   echo "Total_FR5CU"

   SET /P DATASTORE_TARGET="Choose: "
) ELSE (
   SET DATASTORE_TARGET=%1
)
echo "using datastore target: %DATASTORE_TARGET%"

SET OPTION=default
echo.
IF [%2]==[] (
   echo "No commandline for 2nd arg given, please choose a helper target:"
   echo "Options:"
   echo "1: create          (This option will create a new PRQA project for you (based on the aurix build))"
   echo "2: analyze         (This option will analyze an existing project (with all files in it))"
   echo "3: state           (This option will export an exsiting analysis to a spreadsheet with map team)"
   echo "4: gui             (This option will start the gui for you and load the selected ruleset/project)"
   echo "5: list            (This option will require an existing PRQA project (from step 1.)"
   echo "6: pr              (This option will require an existing PRQA project (from step 1.) and will analyze filles acording to the content of changed_files_file_path file has to be inside project root)"
   echo "7: baseline_create (This option will require an existing PRQA project (from step 1.) and analyze (from step 2.) and creates a baseline)"
   echo "8: Splunk copy    (This option will copy the output csv to Splunk export directory)"
   echo "9: merge fr5cu reports and splunk copy    (This option will merge uc1 and uc2 reports to generate Total_FR5CU report)"

   SET /P OPTION="Choose: "
) ELSE (
   SET OPTION=%2
)

IF [%3] NEQ [] (
   SET QAC_DATASTORE_PATH=%SCRIPTLOCATION%%3
) ELSE (
   SET QAC_DATASTORE_PATH=%SCRIPTLOCATION%qac.json )
echo "QAC_DATASTORE_PATH:" %QAC_DATASTORE_PATH%

SET CHANGED_FILES_PATH=default
IF [%4] NEQ [] (
   SET CHANGED_FILES_PATH=%4 )
echo "changed files path: %CHANGED_FILES_PATH%"

SET ENABLE_QUALITY_GATE=FALSE
IF [%5] NEQ [] (
   SET ENABLE_QUALITY_GATE=TRUE )
echo "Enable quality gate for pull request check: %ENABLE_QUALITY_GATE%"


IF "%DATASTORE_TARGET%"=="FR5CU_DNNN1_NNN_N_XX_2_uC1" SET DATASTORE_TARGET_DIR=generatedFiles/qac_report/FR5CU_DNNN1_NNN_N_XX_2_uC1
IF "%DATASTORE_TARGET%"=="FR5CU_DENN1_CEN_N_XX_2_uC2" SET DATASTORE_TARGET_DIR=generatedFiles/qac_report/FR5CU_DENN1_CEN_N_XX_2_uC2
IF "%DATASTORE_TARGET%"=="Total_FR5CU" mkdir %PROJECT_ROOT%\generatedFiles\qac_report\Total_FR5CU\ && SET DATASTORE_TARGET_DIR=generatedFiles/qac_report/Total_FR5CU
echo "parameters:" %*
SET QAC_COMMAND=%PYTHON_EXE% %SCRIPTLOCATION%..\sca_tools_package\sca_tools\sca_tools.py qac
SET QAC_COMMON_ARGS=-dp %QAC_DATASTORE_PATH% -qap %DATASTORE_TARGET_DIR%  -dt %DATASTORE_TARGET% -pr %PROJECT_ROOT% 
SET COMMON_ARGS=-dp %QAC_DATASTORE_PATH% -dt %DATASTORE_TARGET% -pr %PROJECT_ROOT% 
SET DATASTORE_TARGET_REPORT=%PROJECT_ROOT%\%DATASTORE_TARGET_DIR%\sca_tools\export\qacli-view.csv
REM SET HIS_METRICS_REPORT=%PROJECT_ROOT%\%DATASTORE_TARGET_DIR%\sca_tools\export\report-metrics.csv


IF "%OPTION%"=="1" echo "1 selected" & CALL :create
IF "%OPTION%"=="2" echo "2 selected" & CALL :analyze
IF "%OPTION%"=="3" echo "3 selected" & CALL :state
IF "%OPTION%"=="4" echo "4 selected" & CALL :gui
IF "%OPTION%"=="5" echo "5 selected" & CALL :list
IF "%OPTION%"=="6" echo "6 selected" & CALL :pr
IF "%OPTION%"=="7" echo "7 selected" & CALL :baseline_create
IF "%OPTION%"=="8" echo "8 selected" & CALL :Splunk copy
IF "%OPTION%"=="9" echo "9 selected" & CALL :merge fr5cu reports and splunk copy
echo "Error: Unknown option. %OPTION%"
pause >nul
set ERRORLEVEL=1
call :done


:create
echo "create function"
echo %QAC_COMMAND% create %QAC_COMMON_ARGS%
%QAC_COMMAND% create %QAC_COMMON_ARGS%
call :done

:analyze
echo "analyze function"
echo %QAC_COMMAND% analyze %QAC_COMMON_ARGS%
%QAC_COMMAND% analyze %QAC_COMMON_ARGS%
call :done


:state
echo "State"
echo %QAC_COMMAND% state %QAC_COMMON_ARGS% --with_metrics -ef csv html xlsx
%QAC_COMMAND% state %QAC_COMMON_ARGS% --with_metrics -ef csv html

echo %PYTHON_EXE% %SCRIPTLOCATION%..\sca_tools_package\sca_tools\sca_tools.py map_teams %COMMON_ARGS% --input_warnings_report %DATASTORE_TARGET_REPORT% --teams_report %DATASTORE_TARGET_REPORT%
%PYTHON_EXE% %SCRIPTLOCATION%..\sca_tools_package\sca_tools\sca_tools.py map_teams %COMMON_ARGS% -iwr %DATASTORE_TARGET_REPORT% -tr %DATASTORE_TARGET_REPORT%
call :done

:gui
echo "gui function"
echo %QAC_COMMAND% gui %QAC_COMMON_ARGS%
%QAC_COMMAND% gui %QAC_COMMON_ARGS%
call :done

:: the purpose of this list function is to analyze all files coming from a file.
:list
echo "list function"
echo %QAC_COMMAND% analyze %QAC_COMMON_ARGS% --analyze_list %SCRIPTLOCATION%sca_tools_file_list.txt 
%QAC_COMMAND% analyze %QAC_COMMON_ARGS% --analyze_list %SCRIPTLOCATION%sca_tools_file_list.txt
call :done

:pr
echo "---pr function---"
rem main variables
%FIND_INCLUDES_COMMAND%
set FIND_INCLUDES_DATASTORE_PATH=%SCRIPTLOCATION%find_includes.json

IF %CHANGED_FILES_PATH%==default (
   echo "Localy delta check on pc"
   git diff --diff-filter=d --name-only > %SCRIPTLOCATION%/deltas_list.txt
   set FIND_INCLUDES_COMMAND=%PYTHON_EXE% %SCRIPTLOCATION%..\sca_tools_package\sca_tools\sca_tools.py find_includes -dp %FIND_INCLUDES_DATASTORE_PATH% --datastore_target local
) ELSE (
   echo "Jenkins delta check on server"
   set FIND_INCLUDES_COMMAND=%PYTHON_EXE% %SCRIPTLOCATION%..\sca_tools_package\sca_tools\sca_tools.py find_includes -dp %FIND_INCLUDES_DATASTORE_PATH% --datastore_target jenkins -fl %PROJECT_ROOT%/%CHANGED_FILES_PATH%
)

echo "Copy baseline \\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\Athena_Radar\CI\QAC_baseline\%DATASTORE_TARGET%\files.sup to ad_radar_apl\tools\sca_tools\qac\baseline\%DATASTORE_TARGET% "
copy \\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\Athena_Radar\CI\QAC_baseline\%DATASTORE_TARGET%\files.sup %PROJECT_ROOT%\ad_radar_apl\tools\sca_tools\qac\baseline\%DATASTORE_TARGET%

echo "%FIND_INCLUDES_COMMAND%"
%FIND_INCLUDES_COMMAND%

echo "create function"
echo %QAC_COMMAND% create %QAC_COMMON_ARGS% 
%QAC_COMMAND% create %QAC_COMMON_ARGS% 

echo %QAC_COMMAND% analyze %QAC_COMMON_ARGS% --analyze_list %SCRIPTLOCATION%PR_changes_list.txt
%QAC_COMMAND% analyze %QAC_COMMON_ARGS% --analyze_list %SCRIPTLOCATION%PR_changes_list.txt

echo "State"
echo %QAC_COMMAND% state %QAC_COMMON_ARGS% --with_metrics -ef csv html
%QAC_COMMAND% state %QAC_COMMON_ARGS% --with_metrics -ef csv html


if %ENABLE_QUALITY_GATE%==TRUE (
%QAC_COMMAND% filter_qaview %QAC_COMMON_ARGS% --qaview_csv %PROJECT_ROOT%\%DATASTORE_TARGET_DIR%\sca_tools\export\qacli-view.csv --severity_level_fail_threshold_for_level_7 0 --severity_level_fail_threshold_for_level_8 0 --severity_level_fail_threshold_for_level_9 0)

echo "---END---"
call :done

:baseline_create
echo "baseline_create function"
echo %QAC_COMMAND% analyze %QAC_COMMON_ARGS% --helper_create_baseline yes
%QAC_COMMAND% analyze %QAC_COMMON_ARGS% --helper_create_baseline yes
call :done

:Splunk copy
echo "Copy output to Splunk export directory function"
echo copy "%PROJECT_ROOT%\%DATASTORE_TARGET_DIR%\sca_tools\export\qacli-view.csv" \\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\Athena_Radar\CI\Splunk\QAC_output\%DATASTORE_TARGET%
copy "%PROJECT_ROOT%\%DATASTORE_TARGET_DIR%\sca_tools\export\qacli-view.csv" \\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\Athena_Radar\CI\Splunk\QAC_output\%DATASTORE_TARGET%
call :done

:merge fr5cu reports and splunk copy
echo "merge uc1 and uc2 reports to generate Total_FR5CU report"
echo generatedFiles\qac_report\FR5CU_DNNN1_NNN_N_XX_2_uC1\sca_tools\export\qacli-view.csv>%DATASTORE_TARGET_DIR%\input_file.txt
echo generatedFiles\qac_report\FR5CU_DENN1_CEN_N_XX_2_uC2\sca_tools\export\qacli-view.csv>>%DATASTORE_TARGET_DIR%\input_file.txt
%PYTHON_EXE% %SCRIPTLOCATION%..\sca_tools_package\sca_tools\sca_tools.py unify_reports -pr %PROJECT_ROOT% --unify_report_type qac --unify_report_variant_input %DATASTORE_TARGET_DIR%\input_file.txt --unify_report_output %DATASTORE_TARGET_DIR%\qacli-view.csv
echo copy "%DATASTORE_TARGET_DIR%\qacli-view.csv" \\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\Athena_Radar\CI\Splunk\QAC_output\%DATASTORE_TARGET%
copy "%DATASTORE_TARGET_DIR%\qacli-view.csv" \\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\Athena_Radar\CI\Splunk\QAC_output\%DATASTORE_TARGET%
call :done

:done
IF ERRORLEVEL 1 (
    ECHO "Helper command execution failed"
    exit 1
)
call :end

:end
exit 0
