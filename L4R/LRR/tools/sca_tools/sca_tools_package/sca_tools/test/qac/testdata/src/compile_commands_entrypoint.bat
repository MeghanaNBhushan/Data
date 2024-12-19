:: Entrypoint file to distinguish test build on local development environment
:: using MSVC compiler and on Jenkins Build Agent using MinGW.
:: Jenkins sets BUILD_URL environment variables.

set SCRIPTLOCATION=%~dp0

IF DEFINED BUILD_URL (
    call %SCRIPTLOCATION%compile_commands_jenkins.bat
) ELSE (
    call %SCRIPTLOCATION%compile_commands_msvc14.bat
)
