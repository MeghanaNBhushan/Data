@echo off
set SCRIPTLOCATION=%~dp0

SET TOOLNAME=qac

SET TARGET=0
IF [%1]==[] (
	echo "No commandline for 1st arg given, please choose:"
	echo "Options:"
	echo "0: Latest (HELIX2021.3)"
	echo "1: PRQA2.4.0"
	echo "2: HELIX2019.1"
  echo "3: HELIX2019.2"
  echo "4: HELIX2020.1"
  echo "5: HELIX2020.2"
  echo "6: HELIX2021.1"
  echo "7: HELIX2021.2"
  echo "8: HELIX2021.3"
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

IF "%TARGET%"=="0" SET INSTALL_VERSION=_TCC_Helix2021.3_WIN64.xml
IF "%TARGET%"=="1" SET INSTALL_VERSION=_TCC_PRQA2.4.0_WIN64.xml
IF "%TARGET%"=="2" SET INSTALL_VERSION=_TCC_Helix2019.1_WIN64.xml
IF "%TARGET%"=="3" SET INSTALL_VERSION=_TCC_Helix2019.2_WIN64.xml
IF "%TARGET%"=="4" SET INSTALL_VERSION=_TCC_Helix2020.1_WIN64.xml
IF "%TARGET%"=="5" SET INSTALL_VERSION=_TCC_Helix2020.2_WIN64.xml
IF "%TARGET%"=="6" SET INSTALL_VERSION=_TCC_Helix2021.1_WIN64.xml
IF "%TARGET%"=="7" SET INSTALL_VERSION=_TCC_Helix2021.2_WIN64.xml
IF "%TARGET%"=="8" SET INSTALL_VERSION=_TCC_Helix2021.3_WIN64.xml

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
