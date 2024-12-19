@echo off
set SCRIPTLOCATION=%~dp0

set MSVS_HOME="C:\Program Files (x86)\Microsoft Visual Studio 14.0"
call %MSVS_HOME%\VC\vcvarsall.bat amd64

RMDIR /Q/S %SCRIPTLOCATION%build
MKDIR %SCRIPTLOCATION%build
cd %SCRIPTLOCATION%build
cmake -G "NMake Makefiles" -DCMAKE_EXPORT_COMPILE_COMMANDS=1 .. 
