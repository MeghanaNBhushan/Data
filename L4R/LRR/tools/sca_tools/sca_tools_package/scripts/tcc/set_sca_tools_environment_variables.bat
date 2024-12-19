:: ----------------------------------------------------------------------------
:: This script is meant as a common way to share environment variables between
:: the different SCA scripts.
:: =============================================================================
::   C O P Y R I G H T
:: -----------------------------------------------------------------------------
::   Copyright (c) 2021 by Robert Bosch GmbH. All rights reserved.
:: 
::   This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
::   distribution is an offensive act against international law and may be
::   prosecuted under federal law. Its content is company confidential.
:: =============================================================================
::  Filename: set_env.bat
::  Author(s): Ingo Jauch XC-AD/ESW4
::             Andre Silva XC-AD/ESW4
:: # ----------------------------------------------------------------------------
set SCRIPTLOCATION=%~dp0

:: install the windows tool chain via TCC
call %SCRIPTLOCATION%\_install_TCC_qac.bat 0
call %SCRIPTLOCATION%\_install_TCC_coverity.bat 0
call %SCRIPTLOCATION%\_install_TCC_python.bat 0
call %SCRIPTLOCATION%\_install_TCC_jq.bat 0

call %SCRIPTLOCATION%\tcc_path_cache\TCC_ToolPaths_qac.bat
call %SCRIPTLOCATION%\tcc_path_cache\TCC_ToolPaths_coverity.bat
call %SCRIPTLOCATION%\tcc_path_cache\TCC_ToolPaths_python.bat
call %SCRIPTLOCATION%\tcc_path_cache\TCC_ToolPaths_jq.bat

IF DEFINED TCCPATH_helix_qac (
    echo Using TCCPATH_helix_qac variable to set QAC_BIN_PATH
    SET QAC_BIN_PATH=%TCCPATH_helix_qac%\common\bin
) ELSE (
    echo Skip QAC_BIN_PATH configuration. Left unchanged.
)

IF DEFINED TCCPATH_coverity (
    echo Using TCCPATH_coverity variable to set COVERITY_BIN_PATH
    SET COVERITY_BIN_PATH=%TCCPATH_coverity%\bin
) ELSE (
    echo Skip COVERITY_BIN_PATH configuration. Left unchanged.
)