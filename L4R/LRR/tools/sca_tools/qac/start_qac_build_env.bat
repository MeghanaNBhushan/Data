@echo off
echo "Start the build of the QAC Environment "
rem set "COPY_PATH=%~1"
rem set "HASH=%~2"

SET PROJECT_ROOT=%~dp0..\..\..\..\
echo %PROJECT_ROOT%
pushd %PROJECT_ROOT%
cmake_gen.bat -hw %1 -p Radar -cfg ad_radar_apl/tools/cmake/cfg -c -tcc -f
popd