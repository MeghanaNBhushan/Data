@echo off

setlocal EnableDelayedExpansion

REM ----------------------
REM Get Product
REM ----------------------

echo Following product can be build:
echo 0 - Radar_C0_uc1 
echo 1 - Radar_C0_uc2 (default)


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

REM ----------------------
REM Install TCC?
REM ----------------------

set /p tcc_sel="Install TCC (y/N)? "
IF "%tcc_sel%"=="y" set tcc_install=
IF "%tcc_sel%"=="n" set tcc_install=-s
IF not defined tcc_sel (
	set tcc_install=-s
	set tcc_sel=n
)


echo Select target:
echo 0 - host
echo 1 - target

if %1.==. (
    :: missing parameter -> prompt
    set /P var_sel="Select target "
    ) else (
    set "var_sel=%1"
)

IF "%var_sel%"=="0" (
set ut_target=host
)

IF "%var_sel%"=="1" (
set ut_target=target
)

set ut_framework=CANTATA

set LSFORCEHOST=FE0VMC0829.de.bosch.com
set customer_cfg_folder=ad_radar_apl/tools/cmake/cfg

cmake_gen.bat -cfg %customer_cfg_folder% -hw %hardware% -ut %ut_framework% --uttarget %ut_target% -s -f -c
