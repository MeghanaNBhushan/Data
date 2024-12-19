@echo off

setlocal EnableDelayedExpansion

REM ----------------------
REM Get Product
REM ----------------------



set var_sel=%~1
IF not defined var_sel (
set hardware=FR5CU_DENN1_CEN_N_XX_2_uC2
)

IF "%var_sel%"=="FR5CU_DNNN1_NNN_N_XX_2_uC1" (
set hardware=FR5CU_DNNN1_NNN_N_XX_2_uC1
)

IF "%var_sel%"=="FR5CU_DENN1_CEN_N_XX_2_uC2" (
set hardware=FR5CU_DENN1_CEN_N_XX_2_uC2 
)

REM ----------------------
REM Install TCC?
REM ----------------------

set "ut_target=target"

set "ut_framework=CANTATA"
set customer_cfg_folder=ad_radar_apl/tools/cmake/cfg

set "LSFORCEHOST=FE0VMC0829.de.bosch.com"

SET "project_dir=%BATCH_DIR%..\..\..\"
PUSHD %project_dir%
call cmake_gen.bat -cfg %customer_cfg_folder% -hw %hardware% -ut %ut_framework% --uttarget %ut_target% -f -c -s
exit /b