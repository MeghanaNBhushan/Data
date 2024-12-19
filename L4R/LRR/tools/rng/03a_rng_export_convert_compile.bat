@echo off


call conda activate 

REM ********************************************
REM Execut Release Note Generation COMPILE Stage
REM ********************************************
cd src
python rng.py export -c ../rn_TestProject/rng_cfg.json
if %errorlevel% neq 0 GOTO ERROREXIT
python rng.py convert -c ../rn_TestProject/rng_cfg.json
if %errorlevel% neq 0 GOTO ERROREXIT
python rng.py compile -c ../rn_TestProject/rng_cfg.json
if %errorlevel% neq 0 GOTO ERROREXIT
cd..

REM normal exit
REM ******************************************
REM normal exit: close window after 3 seconds
REM ******************************************
:NORMALEXIT
echo.
echo ******** SUCCESSFULLY FINISHED! ********
timeout 3 
exit 0

REM ******************************************
REM exit with ERROR indication, let window open
REM ******************************************
:ERROREXIT
echo ******** GENERATION FAILED! ********
exit -1
   
