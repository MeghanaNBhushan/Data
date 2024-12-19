@echo off
set SCRIPTLOCATION=%~dp0

SET TARGET=0
IF [%1]==[] (
	echo "No commandline for 1st arg given, please choose:"
	echo "Options:"
	echo "0: latest version (Python 3.8.3 WIN64)"
	echo "1: Python 3.6.5-14 WIN64"
	echo "2: Python 3.8.3 WIN64"
	echo "3: Python 3.9.1 WIN64"
	SET /P TARGET="Choose: "
) ELSE (
	SET TARGET=%1
)

SET CACHE_FOLDER=%SCRIPTLOCATION%tcc_path_cache
IF [%2]==[] (
	echo "Using default tcc cache folder"
) ELSE (
	SET CACHE_FOLDER=%2
)
echo tcc cache folder is: %CACHE_FOLDER%


IF "%TARGET%"=="0" SET INSTALL_VERSION=_TCC_python_3.8.3_WIN64.xml
IF "%TARGET%"=="1" SET INSTALL_VERSION=_TCC_python_3.6.5-14_WIN64.xml
IF "%TARGET%"=="2" SET INSTALL_VERSION=_TCC_python_3.8.3_WIN64.xml
IF "%TARGET%"=="3" SET INSTALL_VERSION=_TCC_python_3.9.1_WIN64.xml

set "TCC_COMMAND=%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe -file C:\TCC\Base\InstallToolCollection\InstallToolCollection.ps1"

::must match folder
SET TOOLNAME=python

set "TCC_COMMAND=%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe -file C:\TCC\Base\InstallToolCollection\InstallToolCollection.ps1"
echo "#### Installing %TOOLNAME% ####"
echo Environment variable SCA_SKIP_TCC_INSTALL ...
IF "%SCA_SKIP_TCC_INSTALL%"=="" (
	echo ... not found, installing...
	echo %TCC_COMMAND% %SCRIPTLOCATION%%TOOLNAME%\%INSTALL_VERSION%
	%TCC_COMMAND% %SCRIPTLOCATION%%TOOLNAME%\%INSTALL_VERSION%
	echo Generating TCC ToolPaths bat file
	echo %TCC_COMMAND% %SCRIPTLOCATION%%TOOLNAME%\%INSTALL_VERSION% -GenerateToolPathBat %CACHE_FOLDER%\TCC_ToolPaths_%TOOLNAME%.bat
	%TCC_COMMAND% %SCRIPTLOCATION%%TOOLNAME%\%INSTALL_VERSION% -GenerateToolPathBat %CACHE_FOLDER%\TCC_ToolPaths_%TOOLNAME%.bat
) ELSE (
	echo ... found, skipping TCC install.
)
