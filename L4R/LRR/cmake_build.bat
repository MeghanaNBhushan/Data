@echo off
setlocal EnableDelayedExpansion

REM ----------------------
REM Get Product
REM ----------------------

set BATCH_DIR=%~dp0
set root_dir=%BATCH_DIR%

echo Following product can be build:
echo 0 - Radar_uc1 
echo 1 - Radar_uc2 (default)
echo 2 - Radar_uc1_series
echo 3 - Radar_uc2_series



set /P var_sel="Select number of product (Enter for default)"
IF not defined var_sel (
set product=Radar
set hardware=FR5CU_DENN1_CEN_N_XX_2_uC2
)

IF "%var_sel%"=="0" (
set product=Radar
set hardware=FR5CU_DNNN1_NNN_N_XX_2_uC1
)

IF "%var_sel%"=="1" (
set product=Radar
set hardware=FR5CU_DENN1_CEN_N_XX_2_uC2 
)

IF "%var_sel%"=="2" (
set product=Radar
set hardware=FR5CU_DNNN1_NNN_N_XX_2_uC1_series
)

IF "%var_sel%"=="3" (
set product=Radar
set hardware=FR5CU_DENN1_CEN_N_XX_2_uC2_series
)

REM ----------------------
REM Run Unit Test?
REM ----------------------

set /p ut_sel="Run Unit Test (y/N)? "
IF "%ut_sel%"=="y" set use_ut=-ut
IF "%ut_sel%"=="n" set use_ut=

IF not defined ut_sel (
    set ut_sel=n
	set use_ut=
) 

IF not defined use_ut (
	set customer_cfg_folder=ad_radar_apl/tools/cmake/cfg
	set ut_framework=
	set ut_target=
	set use_ut=
) 

IF defined use_ut (
	echo ============================================
	echo Select 0 for Google Test and 1 for Cantata
	echo ============================================
	set /p ut_framework_sel="Select Unit Test framework (0/1)? "
	
	IF !ut_framework_sel!==0 (
	set ut_framework=GTEST
	)
	
    IF !ut_framework_sel!==1 (
	set ut_framework=CANTATA
	)

	IF !ut_framework_sel!==0 (
		set /p ut_cc_sel="Enable Cantata code coverage (y/N)? "
		IF "!ut_cc_sel!"=="y" (
			set "ut_cc=--cc CANTATA"
			set LSFORCEHOST=FE0VMC0829.de.bosch.com
		) 
		IF "!ut_cc_sel!"=="n" (
			set ut_cc=
		)
	)
	echo ====================================
	echo Select 0 for host build
	echo Select 1 for target build
	echo Select 2 for simulator build
	echo ====================================
	set /p ut_target_sel="Select Unit Test target (0/1/2)? "
	IF !ut_target_sel!==0 set "ut_target=--uttarget host"
	IF !ut_target_sel!==1 set "ut_target=--uttarget target"
	IF !ut_target_sel!==2 set "ut_target=--uttarget simulator"
	
	set customer_cfg_folder=ad_radar_apl/tools/cmake/cfg/utf
)

REM ----------------------
REM Run Make?
REM ----------------------

set /p make_sel="Run Make (Y/n)? "
IF "%make_sel%"=="y" set "use_make=-m"
IF "%make_sel%"=="n" set use_make=
IF not defined make_sel (
	set use_make=-m
	set make_sel=y
)

REM ----------------------
REM Clean Build?
REM ----------------------

set /p clean_sel="Clean old build (y/N)? "
IF "%clean_sel%"=="y" set use_clean=-c
IF "%clean_sel%"=="n" set use_clean=
IF not defined clean_sel (
	set use_clean=
	set clean_sel=n
)

REM ----------------------
REM Build CustomerDataBlock?
REM ----------------------

 set /p cdb_sel="Build CustomerDataBlock (y/N)? "
 IF "%cdb_sel%"=="y" set use_cdb=-d
 IF "%cdb_sel%"=="n" set use_cdb=
 IF not defined cdb_sel (
	set use_cdb=
	set cdb_sel=n
)

echo.
echo -------------------------------
echo Following options are selected:
echo ------------------------------- 
echo Product:        %product%
echo Hardware:       %hardware%
echo Run Unit Test:  %ut_sel%
echo Run Make:       %make_sel%
echo Clean Build:    %clean_sel%
echo Build CustomerDataBlock %cdb_sel%
echo.

set /p user_confirmation="Is this configuration right? (Y/n) "
IF "%user_confirmation%"=="n" exit

echo call python script to generate rbBuild_Version_Cfg.h
cd %root_dir%/ad_radar_apl/cfg
call python generate_h_file.py --creator cis9lr
cd %root_dir%

cd %root_dir%/ad_radar_apl/component/rbPdm/insert
python ExecuteInsert.py --link -v %hardware%
cd %root_dir%

echo cmake_gen.bat -hw %hardware% -p %product% -cfg %customer_cfg_folder% %use_make% %use_clean% -f %use_cdb% %use_ut% %ut_framework% %ut_target% %ut_cc%
cmake_gen.bat -hw %hardware% -p %product% -cfg %customer_cfg_folder% %use_make% %use_clean% -f %use_cdb% %use_ut% %ut_framework% %ut_target% %ut_cc%