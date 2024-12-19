@echo off
set SCRIPTLOCATION=%~dp0

::must match folder
set TOOLNAME=coverity

SET TARGET=0
IF [%1]==[] (
	echo "No commandline for 1st arg given, please choose:"
	echo "Options:"
	echo "0: latest (Coverity 2021.12_WIN64)"
	echo "1: Coverity 2017.07.SP1_WIN64"
	echo "2: Coverity 2018.03-2_WIN64"
	echo "3: Coverity 2019.06_WIN64"
	echo "4: Coverity 2019.12_WIN64"
	echo "5: Coverity 2020.03_WIN64"
	echo "6: Coverity 2020.06_WIN64"
	echo "7: Coverity 2020.09_WIN64"
	echo "8: Coverity 2020.12_WIN64"
	echo "9: Coverity 2021.03_WIN64"
	echo "10: Coverity 2021.06_WIN64"
	echo "11: Coverity 2021.09_WIN64"
	echo "12: Coverity 2021.12_WIN64"
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

IF "%TARGET%"=="0" SET INSTALL_VERSION=_TCC_Coverity_2021.12_WIN64.xml
IF "%TARGET%"=="1" SET INSTALL_VERSION=_TCC_Coverity_2017.07.SP1_WIN64.xml
IF "%TARGET%"=="2" SET INSTALL_VERSION=_TCC_Coverity_2018.03-2_WIN64.xml
IF "%TARGET%"=="3" SET INSTALL_VERSION=_TCC_Coverity_2019.06_WIN64.xml
IF "%TARGET%"=="4" SET INSTALL_VERSION=_TCC_Coverity_2019.12_WIN64.xml
IF "%TARGET%"=="5" SET INSTALL_VERSION=_TCC_Coverity_2020.03_WIN64.xml
IF "%TARGET%"=="6" SET INSTALL_VERSION=_TCC_Coverity_2020.06_WIN64.xml
IF "%TARGET%"=="7" SET INSTALL_VERSION=_TCC_Coverity_2020.09_WIN64.xml
IF "%TARGET%"=="8" SET INSTALL_VERSION=_TCC_Coverity_2020.12_WIN64.xml
IF "%TARGET%"=="9" SET INSTALL_VERSION=_TCC_Coverity_2021.03_WIN64.xml
IF "%TARGET%"=="10" SET INSTALL_VERSION=_TCC_Coverity_2021.06_WIN64.xml
IF "%TARGET%"=="11" SET INSTALL_VERSION=_TCC_Coverity_2021.09_WIN64.xml
IF "%TARGET%"=="12" SET INSTALL_VERSION=_TCC_Coverity_2021.12_WIN64.xml

set "TCC_COMMAND=%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe -file C:\TCC\Base\InstallToolCollection\InstallToolCollection.ps1"

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
