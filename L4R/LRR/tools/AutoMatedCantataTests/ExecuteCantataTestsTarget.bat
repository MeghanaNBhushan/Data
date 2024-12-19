@echo on


if "%~1"=="-c" (
	echo Cantata Build Option is passed. Build Option is: %2.
	set CantataBuildOption=%~2
) else (
	set CantataBuildOption=FR5CU_DENN1_CEN_N_XX_2_uC2
)

IF %CantataBuildOption%==FR5CU_DENN1_CEN_N_XX_2_uC2 (
set variant=Radar_FR5CU_DENN1_CEN_N_XX_2_uC2 
set hardware=FR5CU_DENN1_CEN_N_XX_2_uC2
)

IF %CantataBuildOption%==FR5CU_DNNN1_NNN_N_XX_2_uC1 (
set variant=Radar_FR5CU_DNNN1_NNN_N_XX_2_uC1 
set hardware=FR5CU_DNNN1_NNN_N_XX_2_uC1 
)


set BATCH_DIR=%~dp0
cd /D %BATCH_DIR%

call python AutomaticCantataTargetExec.py -c %CantataBuildOption% -v %variant% 

set errorValue=%ERRORLEVEL%
if %errorValue% equ 1 (
	exit 0
) else (
	if %errorValue% neq 0 (
		exit -1
	)
)
SET project_dir=%BATCH_DIR%..\..\..\
cd /D %project_dir%
set build_dir_root=generatedFiles

SET cantata_product=CANTATA_target_Radar_%hardware%
set dest_dir=%project_dir%%build_dir_root%\SWQualityReports\Cantata\
		
set source_file=%project_dir%ad_radar_apl\tools\AutoMatedCantataTests\
PUSHD %source_file%
COPY "*.txt" %dest_dir% /Y
exit %ERRORLEVEL%