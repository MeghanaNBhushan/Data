@echo off

set MSVS_HOME=C:\Program Files (x86)\Microsoft Visual Studio 14.0
call "%MSVS_HOME%\VC\vcvarsall.bat" amd64

set RLM_LICENSE="5062@rb-lic-lauterbach-cc.de.bosch.com"
set T32_HOME=C:\TCC\Tools\trace32\bosch_201807
set ARMCLANG_HOME=C:\TCC\Tools\armcompiler6\6.6.1_WIN64
set AC6_HOME=%ARMCLANG_HOME%
set ARMLMD_LICENSE_FILE="8224@rb-lic-armlmd-ccda-video.de.bosch.com"
set CLANG_HOME=C:\TCC\Tools\llvm\7.0.1_WIN64
set MINGW64_HOME=C:\TCC\Tools\mingw64\5.4.0_WIN64
set LSFORCEHOST=FE0VMC0829.de.bosch.com
set TCC_CANTATA_HOME=C:\TCC\Tools\cantata\9.0.0_WIN64
set CMAKE_HOME=C:\TCC\Tools\cmake\3.12.1_WIN32
set GHS_HOME=C:\TCC\Tools\greenhills_ifx\comp_201815_1fp_WIN64
set GHS_INCLUDES="-I%GHS_HOME%\scxx -I%GHS_HOME%\include\tri -I%GHS_HOME%\ansi"
set PYTHON_PATH=C:\TCC\Tools\python\2.7.13_WIN64;C:\TCC\Tools\python\2.7.13_WIN64\Scripts;C:\TCC:\TCC\Tools\python\3.7.4-2_WIN64

set PATH=%PYTHON_PATH%;%CMAKE_HOME%\bin;%MINGW64_HOME%\bin;%PATH%
