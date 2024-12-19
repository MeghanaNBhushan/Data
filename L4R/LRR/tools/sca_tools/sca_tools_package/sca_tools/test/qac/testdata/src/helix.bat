:: ----------------------------------------------------------------------------
:: Usage: Example script to use the prqa_helper.py
:: =============================================================================
::   C O P Y R I G H T
:: -----------------------------------------------------------------------------
::   Copyright (c) 2018 by Robert Bosch GmbH. All rights reserved.
:: 
::   This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
::   distribution is an offensive act against international law and may be
::   prosecuted under federal law. Its content is company confidential.
:: =============================================================================
::  Filename: prqa_helper.bat
::  Author(s): Ingo Jauch CC-AD/ESW3 (Maintainer)
:: # ----------------------------------------------------------------------------
@echo on
set SCRIPTLOCATION=%~dp0

SET PROJECT_ROOT=%SCRIPTLOCATION%..\..
pushd %PROJECT_ROOT%
SET PROJECT_ROOT=%CD%
popd

echo "PRQA_HELPER BATCH"
echo "PROJECT_ROOT: " %PROJECT_ROOT%
:: Setup path to support run qt,qnx,cmake,cygwin and boost
SET PATH=C:\TCC\Tools\python3\3.6.5-6_WIN64;%PATH%	
SET PRQA_PATH="C:/Perforce/Helix-QAC-2019.1/common/bin"

C:\TCC\Tools\python3\3.6.5-6_WIN64\python.exe %PROJECT_ROOT%\qac_helper\qac_helper.py --datastore_path %PROJECT_ROOT%\qac_helper\test\test_monitor.json --prqa_path C:/Perforce/Helix-QAC-2019.1/common/bin --project_root %PROJECT_ROOT%\qac_helper\test_src --datastore_target test_1_5 --helper_target create  --build_shell True
