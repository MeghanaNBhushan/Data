@echo off
set SCRIPTLOCATION=%~dp0

CALL %SCRIPTLOCATION%TCC_ToolPaths.bat

set ENVNOTCONFIGURED=
IF NOT DEFINED TCCPATH_cmake (
    echo '[ERROR] TCCPATH_cmake environment variable is not defined'
    SET ENVNOTCONFIGURED=1
)
IF NOT DEFINED TCCPATH_mingw64 (
    echo '[ERROR] TCCPATH_mingw64 environment variable is not defined'
    SET ENVNOTCONFIGURED=1
)

IF DEFINED ENVNOTCONFIGURED exit 1

SET CMAKE_HOME=%TCCPATH_cmake%\bin
SET MINGW_HOME=%TCCPATH_mingw64%\bin

:: Adding Python, CMake and MinGW to PATH
set PATH=%TCCPATH_python3%;%CMAKE_HOME%;%MINGW_HOME%;%PATH%

RMDIR /Q/S %SCRIPTLOCATION%build
MKDIR %SCRIPTLOCATION%build
cd %SCRIPTLOCATION%build
cmake -G "MinGW Makefiles" -DCMAKE_EXPORT_COMPILE_COMMANDS=1 .. 
