@ECHO off
COLOR 0A

setlocal enableextensions disabledelayedexpansion

rem ECHO Enter path to the file which you want to work on
rem SET /P TEXTFILE=
rem ECHO.

rem ECHO Enter word which you want to replace
rem SET /P SEARCH=
rem ECHO.

rem ECHO Enter word which will be used to replace the old word
rem SET /P REPLACE=
rem ECHO.
rem cd .\..\..\..\build\doxygen_output

@set SEARCH=\section
@set REPLACE=\coresubsection

@set SEARCH2=\subsection*
@set REPLACE2=\coresubsubsection

@set SEARCH3=\subsection
@set REPLACE3=\coresubsubsection

@set SEARCH4=\subsubsection[
@set REPLACE4=\coresubsubsubsectionTwo[

@set SEARCH5=\subsubsection
@set REPLACE5=\coresubsubsubsection

@set SEARCH6=\bf
@set REPLACE6=\textbf

@set SEARCH7=\tt
@set REPLACE7=\texttt

@set SEARCH8=\textttfamily
@set REPLACE8=\ttfamily


for %%t in (.\..\doxygen_output\latex\*.tex) do (

    IF NOT EXIST %%t GOTO ERROR

    ECHO Patch file %%t
    ECHO.

:PARSE
    for /f "delims=" %%i in ('type "%%t" ^| find /v /n "" ^& break ^> "%%t"') do (
        set "line=%%i"
        setlocal enabledelayedexpansion
        set "line=!line:*]=!"
        if defined line (
	        set "line=!line:%search%=%replace%!"
	        set "line=!line:%search2%=%replace2%!"
	        set "line=!line:%search3%=%replace3%!"
	        set "line=!line:%search4%=%replace4%!"
	        set "line=!line:%search5%=%replace5%!"
	        set "line=!line:%search6%=%replace6%!"
	        set "line=!line:%search7%=%replace7%!"
	        set "line=!line:%search8%=%replace8%!"
	    )
        >>"%%t" echo(!line!
        endlocal
    )
)

ECHO -----------------------------------------------------------------------
ECHO -                          Finish successful                          -
ECHO -----------------------------------------------------------------------
ECHO.

GOTO END


:ERROR
ECHO File not found
ECHO.

ECHO -----------------------------------------------------------------------
ECHO -                        Finish not successful                        -
ECHO -----------------------------------------------------------------------
ECHO.

:END
PAUSE