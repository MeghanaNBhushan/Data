@echo off
set BATCH_DIR=%~dp0
cd /D %BATCH_DIR%
SET "project_dir=%BATCH_DIR%..\..\..\..\"
cd /D %project_dir%
git ls-files | xargs wc -l 2>&1 | tee  %BATCH_DIR%LOC_ATR.csv
cd /D %BATCH_DIR%