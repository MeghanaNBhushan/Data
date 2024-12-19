@echo off
SET SCRIPTLOCATION=%~dp0
SET CURRENT_DIR=%CD%
SET PROJECT_ROOT=%SCRIPTLOCATION%..\..\..\..
pushd %PROJECT_ROOT%
set PROJECT_ROOT=%CD%
popd

echo "PROJECT_ROOT" %PROJECT_ROOT%

IF [%1]==[] (
   echo "No commandline for 1st arg given, please choose a target:"
   echo "Options:"
   echo "1: FR5CU_DNNN1_NNN_N_XX_2_uC1"
   echo "2: FR5CU_DENN1_CEN_N_XX_2_uC2"
   SET /P OPTION="Choose: "
) ELSE (
   SET OPTION=%1
)

IF [%2]==[] (
   echo "No commandline for 2nd arg given, please choose:"
   echo "Options:"
   echo "1: Create new environment"
   echo "2: Use existing qac environment"
   echo "3: Generate csv report for analyzed files"
   echo "For option 2nd, csv report files will be available at repo\generatedFiles\qac\"variant"\sca_tools\export"
   SET /P CHOICE="Choose: "
) ELSE (
   SET CHOICE=%2
)


IF "%OPTION%"=="1" (
   SET VARIANT=FR5CU_DNNN1_NNN_N_XX_2_uC1 
   )

IF "%OPTION%"=="2" (
   SET VARIANT=FR5CU_DENN1_CEN_N_XX_2_uC2
   )


IF "%CHOICE%"=="1" (
   pushd %SCRIPTLOCATION%
   call start_qac_build_env.bat %VARIANT%
   popd
   start /b /wait %SCRIPTLOCATION%qac.bat %VARIANT% 1
   start /b /wait %SCRIPTLOCATION%qac.bat %VARIANT% 4 )

IF "%CHOICE%"=="2" (
   start /b /wait %SCRIPTLOCATION%qac.bat %VARIANT% 4 )

IF "%CHOICE%"=="3" (
   start /b /wait %SCRIPTLOCATION%qac.bat %VARIANT% 3 )

CD /D %CURRENT_DIR%