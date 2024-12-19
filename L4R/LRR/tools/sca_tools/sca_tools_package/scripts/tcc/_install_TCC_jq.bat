@echo off
set SCRIPTLOCATION=%~dp0

SET TARGET=0
IF [%1]==[] (
	echo "No commandline for 1st arg given, please choose:"
	echo "Options:"
	echo "0: latest version"
	echo "1: jq 1.6"
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

IF "%TARGET%"=="0" SET INSTALL_VERSION=_TCC_jq_1.6_WIN64.xml
IF "%TARGET%"=="1" SET INSTALL_VERSION=_TCC_jq_1.6_WIN64.xml

set "TCC_COMMAND=%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe -file C:\TCC\Base\InstallToolCollection\InstallToolCollection.ps1"

::must match folder
SET TOOLNAME=jq

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