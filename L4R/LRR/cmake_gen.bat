@echo off
REM ----------------------------------------------------------------------------
REM Usage: The file is used by both GUI and command line.
REM Current build targets are: rpu, apu, bootmanager, flashloader_uart, flashkernel
REM =============================================================================
REM   C O P Y R I G H T
REM -----------------------------------------------------------------------------
REM   Copyright (c) 2018 by Robert Bosch GmbH. All rights reserved.
REM
REM   This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
REM   distribution is an offensive act against international law and may be
REM   prosecuted under federal law. Its content is company confidential.
REM =============================================================================
REM  Author(s): Knueppel Rainer     CC/ESM3-Lr
REM             Goyal Ankit         CC/ESM3-Lr
REM             Hardikar Sandesh    RBEI/ESM2
REM ----------------------------------------------------------------------------

setlocal ENABLEDELAYEDEXPANSION

REM saving old path
set "OLDPATH=%PATH%"
set verbose=
set make_verbose=
set run_ccache=
set cmake_ccache=
set make_ccache=

REM set project directory
set project_dir=%~dp0
set "root_dir=%project_dir:\=/%"
REM parse command line arguments -----------------------------------------------------------------
:parseArgs
    if "%~1"=="" (
        goto start
    )

    if "%~1"=="-ut" (
		set run_unittest=YES
		set unittest_framework=%~2
	)

	if "%~1"=="--uttarget" (
		set unittest_target=%~2
	)

    if "%~1"=="-p" (
        echo Product is passed. Product: %2.
        set product=%~2
    )

    if "%~1"=="-ct" (
        echo Product is passed. Product: %2.
        set controller=%~2
    )

    if "%~1"=="-hw" (
        echo Hardware is passed. Hardware: %2.
        set hardware=%~2
    )

    if "%~1"=="-c" (
        set clean_build=YES
    )

    if "%~1"=="--clean" (
        set clean_build=YES
    )

    if "%~1"=="-btcdir" (
        set btc_dir=%~2
    )
    if "%~1"=="-toolsdir" (
        set tools_dir=%~2
    )
    if "%~1"=="-cb" (
        set customer_build=%~2
    )

    if "%~1"=="-m" (
        set execute_make=YES
    )

	if "%~1"=="--doxygen" (
        set execute_doxygen=YES
    )

    if "%~1"=="--env" (
        set creat_build_env=YES
    )

    if "%~1"=="-cfg" (
        echo Cmake config path is given. Look for a config file at: "%2".
        set cmake_cfg_folder=%~2
    )

    if "%~1"=="--config-path" (
        echo Cmake config path is given. Look for a config file at: "%2".
        set cmake_cfg_folder=%~2
    )

    if "%~1"=="-f" (
        echo Running in fast mode
        set fast_mode=YES
    )

    if "%~1"=="--a2l" (
        set run_a2l=YES
    )

    if "%~1"=="--cov" (
        set run_coverity=YES
    )

    if "%~1"=="--no-pause" (
        echo Build will exit once finished. User will not be able to see any success or error messages.
        set no_pause=YES
    )

    if "%~1"=="--verbose" (
        echo Enable verbose mode to get more verbose output from Makefile builds.
        set verbose=^-DCMAKE_VERBOSE_MAKEFILE^=1
        set make_verbose=VERBOSE^=1
    )

    if "%~1"=="--ccache" (
        echo Enable build with ccache
        set run_ccache=YES
    )

    if "%~1"=="--low" (
        echo Run make with LOW priority
        set low_mode=YES
    )
    
    if "%~1"=="--pdv_gen" (
        echo Run make mt pdv database generator
        set pdv_generator=YES
    )   

    if "%~1"=="-h" (
        echo.
        echo.
        echo ----------------------------------------------------------------------------------------------------------------------------
        echo.
        echo NOTE: Build and Test options are independent and cannot be combined together.
        echo If any 'test' option is provided, 'build' options will be ignored.
        echo.
        echo Full listing for building the variants including necessary -cfg parameters can be found in:
        echo.
        echo https://inside-docupedia.bosch.com/confluence/display/CCESM/Manual+for+PJIF+build
        echo.
        echo GENERAL
        echo ========================
        echo.
        echo "-c -----------------------> Clean the old build before running the build. (OPTIONAL)"
        echo "-s, --skip-tcc -----------> Skip to run TCC install script (OPTIONAL)"
        echo "-h -----------------------> Cmake_gen.bat help"
        echo "-p <product> -------------> Product name. DEFAULT: "Radar" (OPTIONAL). Allowed products are "DASY and Radar""
        echo "-hw <hardware> -----------> Hardware name. DEFAULT: "FR5CP_5NNN1_CAN_N_MX_2" (OPTIONAL).Eg: CR5CP_5NN21_CEN_N_MX_2,"
		echo " CR5CB_5NN21_CSN_N_SM_2, fault_inj_CR5CB_5NN21_CSN_N_SM_2, Radar_*_series (e.g. Radar_FR5CP_5NNN1_CAN_N_MX_2_series)"
        echo "-f -----------------------> Fast mode. Runs "make -j 16" to build the target after "cmake" is executed successfully. (OPTIONAL)"
        echo "--env --------------------> Setup build enviornment, which enables user to run available features of the build tool chain."
        echo "--cov --------------------> Run coverity for the project."
        echo "--verbose ----------------> Runs build in verbose mode. (OPTIONAL)"
        echo "-cfg, --config-path ------> Relative path from the project root directory to the folder where variant specific cmake"
        echo "                            config file is present. DEFAULT: "ad_radar_apl/tools/cmake/cfg" (OPTIONAL)"
	echo "--pdv_gen, ---------------> mt_pdv_database generator or pdv"
        echo.
        echo.
        echo BUILD
        echo ========================
        echo.
        echo "-m -----------------------> Run "make -j 8" to build the target after "cmake" is executed successfully. (OPTIONAL)"
        echo "--a2l --------------------> Run A2L. (OPTIONAL)"
        echo "--low --------------------> Run "make" with LOW priority. Useful for machines with limited ressources. (OPTIONAL)"
        echo.
        echo.
        echo TEST
        echo ========================
        echo.
        echo "-ut <test_framework> --------------> Cantata creates Cantata test environment for the passed target. User have to set --uttarget also if -ut is set. Eg :-ut cantata --uttarget simulator"
        echo "--uttarget <target> --------> Available targets are 'host, target, simulator"
        echo.
        echo ----------------------------------------------------------------------------------------------------------------------------
        exit /B
    )

    shift
    goto parseArgs
goto:eof

:start
REM set default variables ---------------------------------------------------------------------------------
if "!cmake_cfg_folder!"=="" (
    set cmake_cfg_folder=ad_radar_apl/tools/cmake/cfg
)
if "!product!"=="" (
    set product=Radar
)
if "!hardware!"=="" (
    set hardware=FR5CP_5NNN1_CAN_N_MX_2
)
if "!controller!"=="" (
    set controller=aurix
)
if "!customer_build!"=="" (
    set customer_build=""
)
if "!btc_dir!"=="" (
    set btc_dir=ip_if/btc_tools
)
if "!tools_dir!"=="" (
    set tools_dir=ip_if/tools
)
rem setting toolchain file ---------------------------------------------------------------------------------
if "!unittest_target!"=="host" (
    set toolchain_file=toolchains/rbmingw_x86
    set software_target=Cantata
) else (
    if "!unittest_target!"=="target" (
        set toolchain_file=toolchains/rbghs_tri
        set software_target=Cantata
    ) else (
        if "!unittest_target!"=="simulator" (
            set toolchain_file=toolchains/rbghs_tri
            set software_target=Cantata
        ) else (
            set toolchain_file=toolchains/rbghs_tri
            set software_target=generic
        )
    )
)

rem setting directory prefix ------------------------------------------------------------------------------
if "%run_unittest%"=="YES" (
	set dir_prefix=!unittest_framework!_!unittest_target!_
	if "!software_target!"=="" (
		echo "Error: Invalid unit test target: '!unittest_target!'"
        exit /b 101
    )
) else (
    set dir_prefix=
)

rem setting variables -------------------------------------------------------------------------------------
SETLOCAL
set build_dir_root=generatedFiles
set cmake_gen=-G "MinGW Makefiles"
set VARIANT=%dir_prefix%!product!_!hardware!
set BUILD_DIR=%project_dir%%build_dir_root%\%VARIANT%

set CMD_EXE=%SystemRoot%\system32\cmd.exe
set POWERSHELL_EXE=%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe
set /p TOOLCOLLECTION=<tcc_toolversion_itc2.txt

set error_file_name=%BUILD_DIR%\found.error

REM delete error file before running the build -----------------------------------------------------------
call :delete_found_error_file

REM print passed parameters ------------------------------------------------------------------------------
call :print_passed_param

rem create build environment only -----------------------------------------------------------------------
if "%creat_build_env%"=="YES" (
    call :setup_build_env
) else (

    if "%clean_build%"=="YES" (
        call :run_clean
    )

    call :run_install_tool_collection
    call :run_initialize_tools_env

    if "%run_a2l%"=="YES" (
        call :run_a2l
    ) else (
        call :run_cmake

        if "%run_coverity%"=="YES" (
            set coverity_tool_dir=%project_dir%%btc_dir%\coverity
            set coverity_config_dir=%project_dir%ad_radar_apl/tools/Coverity
            call :run_coverity
        ) else (
            if "%execute_make%"=="YES" (
                call :run_make
            )
			if "%execute_doxygen%"=="YES" (
                call :run_doxygen
            )

            call :run_after_build
        )
    )
)

rem check errors -----------------------------------------------------------------------------------------
if %ERRORLEVEL% neq 0 (
    popd
    echo "Build failure with error %ERRORLEVEL%"

    if not "%no_pause%"=="YES" (
        pause
    )

    set "PATH=%OLDPATH%"
    exit /B %ERRORLEVEL%
) else (
    cd %build_dir%
    echo ==================================================================================
    echo "Build configuration successful!"
    echo ==================================================================================
    if not "%no_pause%"=="YES" (
        goto end
    )

    set "PATH=%OLDPATH%"
    exit /B
)

rem functions --------------------------------------------------------------------------------------------
:run_install_tool_collection
    echo.
    echo Running InstallToolCollection to make sure we have all tools...
    echo.
    mkdir %BUILD_DIR%
    itc2 install %TOOLCOLLECTION% --tpdir %BUILD_DIR%
    call :check_error "Install tool collection failure"
goto:eof

:run_ccache_config
    set CCACHE_DIR=C:\ccache\%VARIANT%
    echo %CCACHE_DIR%
    set CCACHE_COMPRESS=1
    set CCACHE_DEPEND=1
    set CCACHE_MAXSIZE=10G
    %TCCPATH_ccache%\ccache -o log_file=%CCACHE_DIR%\ccache.log
    set cmake_ccache=^-DCMAKE_C_COMPILER_LAUNCHER=%TCCPATH_ccache%\ccache -DCMAKE_CXX_COMPILER_LAUNCHER=%TCCPATH_ccache%\ccache
    set make_ccache=%TCCPATH_ccache%\ccache
    call :check_error "Install tool collection failure"
goto:eof

:run_initialize_tools_env
    echo.
    echo Initializing tools environment...
    echo.
    call %BUILD_DIR%\TCC_ToolPaths.bat
    call :check_error "Tool's environment initialization failure"

    REM set test/build variables
    set "PATH="
    set PATH=%TCCPATH_cmake%\bin;%TCCPATH_mingw64%\bin;
goto:eof

:run_clean
    if %ERRORLEVEL% equ 0 (
        if exist %BUILD_DIR% (
            echo [-- Deleting build_cmake directory.. --]
            rmdir /s/q %BUILD_DIR%
        )
        call :check_error "Clean failure"
    )
goto:eof

:run_cmake
    if %ERRORLEVEL% equ 0 (
        echo Running CMAKE...
        if not exist %BUILD_DIR% (
            mkdir %BUILD_DIR%
        )

        if not exist %BUILD_DIR%\log (
            mkdir %BUILD_DIR%\log
        )

        pushd %BUILD_DIR%
        echo %rootDir%

        if "%run_ccache%"=="YES" (
            call :run_ccache_config

            echo  %CMAKE_EXE% %cmake_gen% -Wno-dev %verbose% !cmake_ccache! -DRB_SW_TARGET=%software_target% -DRB_PRODUCT=%product% -DCMAKE_TOOLCHAIN_FILE=%toolchain_file% -DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DCMAKE_SH=CMAKE_SH-NOTFOUND -DRB_UT_TARGET=%unittest_target% -DRB_CUSTOMER_CMAKE_DIR=%cmake_cfg_folder% -DRB_HARDWARE=%hardware% -DRB_PLATFORM=pjifuc -DRB_CUSTOMER_BUILD=%customer_build% -DRB_CONTROLLER=%controller% -DRB_ROOT_DIR=%root_dir% -DRB_BTC_DIR=%btc_dir%  -DRB_TOOLS_DIR=%tools_dir% -DRB_UNIT_TEST=%unittest_framework% %project_dir%%btc_dir%
            ( %CMAKE_EXE% %cmake_gen% -Wno-dev %verbose% !cmake_ccache! -DRB_SW_TARGET=%software_target% -DRB_PRODUCT=%product% -DCMAKE_TOOLCHAIN_FILE=%toolchain_file% -DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DCMAKE_SH=CMAKE_SH-NOTFOUND -DRB_UT_TARGET=%unittest_target% -DRB_CUSTOMER_CMAKE_DIR=%cmake_cfg_folder% -DRB_HARDWARE=%hardware% -DRB_PLATFORM=pjifuc -DRB_CUSTOMER_BUILD=%customer_build% -DRB_CONTROLLER=%controller% -DRB_ROOT_DIR=%root_dir% -DRB_BTC_DIR=%btc_dir%  -DRB_TOOLS_DIR=%tools_dir% -DRB_UNIT_TEST=%unittest_framework% %project_dir%%btc_dir% || echo "Error in cmake" > %error_file_name% ) 2>&1 | %TEE_EXE% %BUILD_DIR%\log\cmakeLog.txt

        ) else (
            echo  %CMAKE_EXE% %cmake_gen% -Wno-dev %verbose% -DRB_SW_TARGET=%software_target% -DRB_PRODUCT=%product% -DCMAKE_TOOLCHAIN_FILE=%toolchain_file% -DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DCMAKE_SH=CMAKE_SH-NOTFOUND -DRB_UT_TARGET=%unittest_target% -DRB_CUSTOMER_CMAKE_DIR=%cmake_cfg_folder% -DRB_HARDWARE=%hardware% -DRB_PLATFORM=pjifuc -DRB_CUSTOMER_BUILD=%customer_build% -DRB_CONTROLLER=%controller% -DRB_ROOT_DIR=%root_dir% -DRB_BTC_DIR=%btc_dir%  -DRB_TOOLS_DIR=%tools_dir% -DRB_UNIT_TEST=%unittest_framework% %project_dir%%btc_dir%
            ( %CMAKE_EXE% %cmake_gen% -Wno-dev %verbose% -DRB_SW_TARGET=%software_target% -DRB_PRODUCT=%product% -DCMAKE_TOOLCHAIN_FILE=%toolchain_file% -DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DCMAKE_SH=CMAKE_SH-NOTFOUND -DRB_UT_TARGET=%unittest_target% -DRB_CUSTOMER_CMAKE_DIR=%cmake_cfg_folder% -DRB_HARDWARE=%hardware% -DRB_PLATFORM=pjifuc -DRB_CUSTOMER_BUILD=%customer_build% -DRB_CONTROLLER=%controller% -DRB_ROOT_DIR=%root_dir% -DRB_BTC_DIR=%btc_dir%  -DRB_TOOLS_DIR=%tools_dir% -DRB_UNIT_TEST=%unittest_framework% %project_dir%%btc_dir% || echo "Error in cmake" > %error_file_name% ) 2>&1 | %TEE_EXE% %BUILD_DIR%\log\cmakeLog.txt
        )


        call :check_error "CMake failure"
    )
goto:eof

:run_a2l
    if %ERRORLEVEL% equ 0 (
        echo Running cmake for software...
        call :run_cmake

        echo Building software...
        call :run_make

        set BUILD_DIR=%BUILD_DIR%\A2L

        if not exist !BUILD_DIR! (
            mkdir !BUILD_DIR!
        )

        if not exist !BUILD_DIR!\log (
            mkdir !BUILD_DIR!\log
        )

        pushd !BUILD_DIR!

        echo Running A2L...
        ( %CMAKE_EXE% %cmake_gen% -Wno-dev %verbose% -DRB_SW_TARGET=A2L -DRB_PRODUCT=%product% -DCMAKE_TOOLCHAIN_FILE=%project_dir%%btc_dir%\cmake\toolchains\Radar_A2L_DINXVT_toolchain.cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DCMAKE_SH=CMAKE_SH-NOTFOUND -DRB_CUSTOMER_CMAKE_DIR=%cmake_cfg_folder% -DRB_HARDWARE=%hardware% -DRB_PLATFORM=pjifuc -DRB_CUSTOMER_BUILD=%customer_build% -DRB_ROOT_DIR=%root_dir% -DRB_CONTROLLER=%controller% -DRB_BTC_DIR=%btc_dir% -DRB_TOOLS_DIR=%tools_dir% %project_dir%%btc_dir% || echo "Error in A2l while running cmake" > %error_file_name% ) 2>&1 | %TEE_EXE% !BUILD_DIR!\log\cmakeLog.txt

        echo Building A2L...
        call :run_make_a2l

        call :check_error "A2L failure"
    )
goto:eof

:run_make
    if %ERRORLEVEL% equ 0 (
        echo.
        echo.
        echo [-- Running make.. --]

        if "%fast_mode%"=="YES" (
            set "make_options=-j 16 -k"
        ) else (
            set "make_options=-j 8 -k"
        )

        cd %BUILD_DIR%

        if "%run_ccache%"=="YES" (
            echo %TCCPATH_ccache%\ccache -c
            %TCCPATH_ccache%\ccache -c
            echo %TCCPATH_ccache%\ccache -z
            %TCCPATH_ccache%\ccache -z

            echo !make_ccache! "%MAKE_EXE%" !make_options! %make_verbose%
            ( !make_ccache! "%MAKE_EXE%" !make_options! %make_verbose% || echo "Error in make" > %error_file_name% ) 2>&1 | %TEE_EXE% !BUILD_DIR!\log\makeLog.txt

            echo %TCCPATH_ccache%\ccache -s
            %TCCPATH_ccache%\ccache -s
        ) else (
            echo "%MAKE_EXE%" !make_options! %make_verbose%
            if "%low_mode%"=="YES" (
                (start "-- MAKE --" /LOW /B "%MAKE_EXE%" !make_options! %make_verbose% || echo "Error in make" > %error_file_name% ) 2>&1 | %TEE_EXE% !BUILD_DIR!\log\makeLog.txt
            ) else (
                ("%MAKE_EXE%" !make_options! %make_verbose% || echo "Error in make" > %error_file_name% ) 2>&1 | %TEE_EXE% !BUILD_DIR!\log\makeLog.txt
            )
            if "%pdv_generator%"=="YES" (
                echo ===============================================================
                echo Running PDV database generator...
                echo ===============================================================
                echo "%MAKE_EXE%" !make_options! mt_pdv_database
                ("%MAKE_EXE%" !make_options! mt_pdv_database) 2>&1 | %TEE_EXE% !BUILD_DIR!\pdv\pdv_makeLog.txt
                    if not exist pdv\pdv_database.xml  echo "Error in make" > %error_file_name%
                    call :check_error "PDV database generator failure"
            )
        )


        echo %TCCPATH_python3%\python.exe %project_dir%%btc_dir%\python_scripts\logs\log_parser.py -i %BUILD_DIR%\log\makeLog.txt -c GHS -tcc %project_dir%/tcc_toolversion_itc2.txt -b "cmake_gen.bat %*" -p Radar
        %TCCPATH_python3%\python.exe %project_dir%%btc_dir%\python_scripts\logs\log_parser.py -i %BUILD_DIR%\log\makeLog.txt -c GHS -tcc %project_dir%/tcc_toolversion_itc2.txt -b "cmake_gen.bat %*" -p Radar

        call :check_error "Make failure"
    )
goto:eof

:run_doxygen
    if %ERRORLEVEL% equ 0 (
        echo.
        echo.
        echo [-- Running doxygen.. --]

        if "%fast_mode%"=="YES" (
            set "make_options=-j 16"
        ) else (
            set "make_options=-j 8"
        )

        cd %BUILD_DIR%

        echo "%MAKE_EXE%" doxygen !make_options! %make_verbose%
        ( "%MAKE_EXE%" doxygen !make_options! %make_verbose% || echo "Error in doxygen" > %error_file_name% ) 2>&1 | %TEE_EXE% !BUILD_DIR!\log\doxygenLog.txt

        call :check_error "Doxygen failure"
    )
goto:eof


:run_after_build
    if "!product!"=="DASY"  (
        set "MERGE_HEX_FILES_TOOL_HOME=%project_dir%dasy_int\tools\srecord\srec_cat.exe"
        set IMAGE_FILENAME=%dir_prefix%!product!_!hardware!

        if %ERRORLEVEL% equ 0 (
            if exist "%BUILD_DIR%\%IMAGE_FILENAME%.hex" (
                ECHO Generating Full Hex File...
                "%MERGE_HEX_FILES_TOOL_HOME%" %BUILD_DIR%\%IMAGE_FILENAME%.hex -intel %project_dir%dasy_int\tools\builder\bootbuilder\Platform_C0\Boot_Mgr\GHS_TC39X_BOOT_D02_V3_2_0.hex -intel %project_dir%dasy_int\tools\builder\bootbuilder\Platform_C0\BoschData\GHS_TC39X_DATA_BOSCH_V2.hex -intel %project_dir%dasy_int\tools\builder\bootbuilder\Platform_C0\FBL\TC39X_BLDR_Enhanced_BStep.hex -intel %project_dir%dasy_int\tools\builder\bootbuilder\ucbconfig\UCB_BMHD0_ORIG_DASy.hex -intel %project_dir%dasy_int\tools\builder\bootbuilder\ucbconfig\UCB_BMHD0_COPY_DASy.hex -intel %project_dir%dasy_int\tools\builder\bootbuilder\ucbconfig\UCB_DFLASH_complement_sensing.hex -intel -o %BUILD_DIR%\%IMAGE_FILENAME%_FULL.hex -intel
                call :check_error "Generating full Hex file failed"
            )
        )
    )
goto:eof

:run_make_a2l
    if %ERRORLEVEL% equ 0 (
        echo.
        echo.
        echo [-- Running make.. --]
        set BUILD_DIR=%BUILD_DIR%\A2L
        cd !BUILD_DIR!
        ( "%MAKE_EXE%" -j 8 || echo "Error in make" > %error_file_name% ) 2>&1 | %TEE_EXE% %BUILD_DIR%\log\makeLog.txt
        call :check_error "Make failure"
    )
goto:eof

:setup_build_env
    if %ERRORLEVEL% equ 0 (
        if not exist %BUILD_DIR% (
            set ERRORLEVEL=101
            call :check_error "Build directory does not exists. Please run cmake_gen.bat first."
        ) else (
            call :run_initialize_tools_env
            call :check_error "Error while setting up build environment"
        )
    )
goto:eof

:run_calcres
    if %ERRORLEVEL% equ 0 (
        cd %BUILD_DIR%
        %MAKE_EXE% calcres
        call :check_error "calcres failure"
    )
goto:eof

:run_coverity
    if %ERRORLEVEL% equ 0 (
        cd %BUILD_DIR%
        "%TCCPATH_python3%\python.exe" "%coverity_tool_dir%/CoverityEntry.py" --build_cmd "%MAKE_EXE% -j16" --config_file_path "%coverity_config_dir%/config/!product!Config.json" --coverity_path "%COVERITY_DIR%" --format_error "no" --commit_analysis "yes" --build_target !hardware! --product !product!
        call :check_error "coverity failure"
    )
goto:eof

:run_shadow_files
    if %ERRORLEVEL% equ 0 (
        cd %BUILD_DIR%
        %MAKE_EXE% shadow_files
        call :check_error "shadow_files failure"
    )
goto:eof

:run_qa_framework_proj_setup
    if %ERRORLEVEL% equ 0 (
        cd %BUILD_DIR%
        %MAKE_EXE% QAPROJECT
        call :check_error "Qa project setup failure"
    )
goto:eof

:check_error
    if exist %error_file_name% (
        echo %1
        exit /b 100
    )

    if %ERRORLEVEL% neq 0 (
        echo %1
        exit /b %ERRORLEVEL%
    )
goto:eof

:delete_found_error_file
    if exist %error_file_name% (
        del %error_file_name%
    )
goto:eof

:print_passed_param
    echo =========================================
    echo Params passed/used
    echo =========================================
    echo "PRODUCT---------------> !product!"
    echo "HARDWARE--------------> !hardware!"
    echo "SOFTWARE_TARGET-------> !software_target!"
    echo "CUSTOMER_CMAKE_DIR----> !cmake_cfg_folder!"
    echo "CMAKE_TOOLCHAIN_FILE--> !toolchain_file!"
goto:eof

rem have to open a new cmd to keep the cmd in build folder -----------------------------------------
:end
    if "%run_unittest%"=="YES" (
        %CMD_EXE%
	)
