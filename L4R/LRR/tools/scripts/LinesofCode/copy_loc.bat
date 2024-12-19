@echo off

setlocal ENABLEDELAYEDEXPANSION

if "%~1"=="-hw" (
	echo Hardware is passed. Hardware: %2.
	set hardware=%~2
)

set BATCH_DIR=%~dp0
cd /D %BATCH_DIR%

SET "project_dir=%BATCH_DIR%..\..\..\..\"
cd /D %project_dir%
set build_dir_root=generatedFiles

SET product=Radar
set "dest_dir=%project_dir%%build_dir_root%\%product%_%hardware%\log"
		
PUSHD %BATCH_DIR%
COPY "*.txt" %dest_dir% /Y
POPD