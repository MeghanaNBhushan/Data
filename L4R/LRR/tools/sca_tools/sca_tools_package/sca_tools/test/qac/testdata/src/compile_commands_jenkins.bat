@echo on
set SCRIPTLOCATION=%~dp0

SET PROJECT_ROOT=%SCRIPTLOCATION%
pushd %PROJECT_ROOT%
SET PROJECT_ROOT=%CD%
popd

CALL %SCRIPTLOCATION%TCC_ToolPaths.bat

set ENVNOTCONFIGURED=
IF NOT DEFINED TCCPATH_python3 (
    echo '[ERROR] TCCPATH_python3 environment variable is not defined'
    SET ENVNOTCONFIGURED=1
)
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

echo %PROJECT_ROOT%
cd %PROJECT_ROOT%

RMDIR /Q/S build_commands
MKDIR build_commands
cd build_commands
cmake.exe -G "MinGW Makefiles" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON ..
cd ..

%TCCPATH_python3%\python.exe %PROJECT_ROOT%/../../../../fix_json/fix_json.py -in build_commands/compile_commands.json