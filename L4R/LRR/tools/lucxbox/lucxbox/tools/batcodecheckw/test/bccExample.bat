REM Faulty Code to test BatCodeCheck
for /f "usebackq delims==" %%i in (%VARIABLE%) do (
  set VARIABLE=%%i
)