@echo off

call conda activate 

REM ******************************************
REM Execut Release Note Generation signature Stage
REM ******************************************
cd src
python rng.py sign -c ../rn_TestProject/rng_cfg.json
cd..

if %errorlevel% neq 0 GOTO ERROREXIT

REM normal exit
REM ******************************************
REM normal exit: close window after 3 seconds
REM ******************************************
:NORMALEXIT
echo.
echo ******** SUCCESSFULLY FINISHED! ********
rem timeout 3  
exit /b 0

REM ******************************************
REM exit with ERROR indication, let window open
REM ******************************************
:ERROREXIT
echo ******** GENERATION FAILED! ********
exit /b -1   
