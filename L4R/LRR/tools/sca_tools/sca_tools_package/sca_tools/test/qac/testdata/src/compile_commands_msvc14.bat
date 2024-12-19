@echo on
set SCRIPTLOCATION=%~dp0

SET PROJECT_ROOT=%SCRIPTLOCATION%
pushd %PROJECT_ROOT%
SET PROJECT_ROOT=%CD%
popd

set PATH=C:\TCC\Tools\python3\3.6.5-1_WIN64;%PATH%
set PYTHON2_EXECUTABLE=C:/TCC/Tools/python/2.7.13-9_WIN64/python.exe
set PYTHON_EXECUTABLE=C:/TCC/Tools/python3/3.6.5-6_WIN64/python.exe

set MSVS_HOME="C:\Program Files (x86)\Microsoft Visual Studio 14.0"
call %MSVS_HOME%\VC\vcvarsall.bat amd64


SET CMAKE_HOME=C:\TCC\Tools\cmake\3.11.2_WIN32\bin
echo %path% | find /i "%CMAKE_HOME%" > nul 2>&1  || set path=%CMAKE_HOME%;%path%

echo %PROJECT_ROOT%
cd %PROJECT_ROOT%

RMDIR /Q/S build_commands
MKDIR build_commands
cd build_commands
cmake.exe -G "NMake Makefiles" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON ..
cd ..

C:/TCC/Tools/python3/3.6.5-6_WIN64/python.exe %PROJECT_ROOT%/../../../../fix_json/fix_json.py -in build_commands/compile_commands.json