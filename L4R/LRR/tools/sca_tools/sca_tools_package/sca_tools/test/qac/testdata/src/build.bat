:: Entrypoint file to distinguish test build on local development environment
:: using MSVC compiler and on Jenkins Build Agent using MinGW.
:: Jenkins sets BUILD_URL environment variables.

set SCRIPTLOCATION=%~dp0

IF DEFINED BUILD_URL (
    call %SCRIPTLOCATION%jenkins_build.bat
) ELSE (
    call %SCRIPTLOCATION%msvc_build.bat
)