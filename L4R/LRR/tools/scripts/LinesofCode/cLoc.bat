@echo off
setlocal
setlocal enabledelayedexpansion
del /s /q ".\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\*.*"
del /s /q ".\..\..\..\..\generatedFiles\LinesofCode\*.*"
set Files=
set PathToExe="C:\tools\cloc\cloc-1.84.exe"
rem set PathToExe="cloc-1.84.exe"
SET /A counter =0

FOR /D %%G in (".\..\..\..\component\*") DO (
!PathToExe! --exclude-dir=test --by-file-by-lang --include-lang=C,C++ --report-file=.\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\component\%%~nxG  %%G 
echo(serach %%G
set feld[!counter!]=%%G 
set /a counter+=1
if exist .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\component\%%~nxG set "Files=!Files! .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\component\%%~nxG
)
)


FOR /D %%G in (".\..\..\..\cubas\gen\*") DO (
!PathToExe! --exclude-dir=test --by-file-by-lang --include-lang=C,C++ --report-file=.\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\cubas\gen\%%~nxG  %%G 
echo(serach %%G
set feld[!counter!]=%%G 
set /a counter+=1
if exist .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\cubas\gen\%%~nxG set "Files=!Files! .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\cubas\gen\%%~nxG
)
)

FOR /F %%G in (".\..\..\..\cubas\stubs\*") DO (
!PathToExe! --exclude-dir=test --by-file-by-lang --include-lang=C,C++ --report-file=.\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\cubas\stubs\%%~nxG  %%G 
echo(serach %%G
set feld[!counter!]=%%G 
set /a counter+=1
if exist .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\cubas\stubs\%%~nxG set "Files=!Files! .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\cubas\stubs\%%~nxG
)
)

FOR /F %%G in (".\..\..\..\cubas\stubs_premium_uC1\*") DO (
!PathToExe! --exclude-dir=test --by-file-by-lang --include-lang=C,C++ --report-file=.\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\cubas\stubs_premium_uC1\%%~nxG  %%G 
echo(serach %%G
set feld[!counter!]=%%G 
set /a counter+=1
if exist .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\cubas\stubs_premium_uC1\%%~nxG set "Files=!Files! .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\cubas\stubs_premium_uC1\%%~nxG
)
)

FOR /D %%G in (".\..\..\..\cubas\cfg\*") DO (
!PathToExe! --exclude-dir=test --by-file-by-lang --include-lang=C,C++ --report-file=.\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\cubas\cfg\%%~nxG  %%G 
echo(serach %%G
set feld[!counter!]=%%G 
set /a counter+=1
if exist .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\cubas\cfg\%%~nxG set "Files=!Files! .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\cubas\cfg\%%~nxG
)
)

FOR /F %%G in (".\..\..\..\ToBeCleanUp\*") DO (
!PathToExe! --exclude-dir=test --by-file-by-lang --include-lang=C,C++ --report-file=.\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\ToBeCleanUp\%%~nxG  %%G 
echo(serach %%G
set feld[!counter!]=%%G 
set /a counter+=1
if exist .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\ToBeCleanUp\%%~nxG set "Files=!Files! .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\ToBeCleanUp\%%~nxG
)
)

FOR /D %%G in (".\..\..\..\cfg\*") DO (
!PathToExe! --exclude-dir=test --by-file-by-lang --include-lang=C,C++ --report-file=.\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\cfg\%%~nxG  %%G 
echo(serach %%G
set feld[!counter!]=%%G 
set /a counter+=1
if exist .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\cfg\%%~nxG set "Files=!Files! .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\cfg\%%~nxG
)
)


FOR /D %%G in (".\..\..\..\..\ip_dc\*") DO (
!PathToExe! --exclude-dir=test --by-file-by-lang --include-lang=C,C++ --report-file=.\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\ip_dc\%%~nxG  %%G 
echo(serach %%G
set feld[!counter!]=%%G 
set /a counter+=1
if exist .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\ip_dc\%%~nxG set "Files=!Files! .\..\..\..\..\generatedFiles\LinesofCode\cloc_Details\ip_dc\%%~nxG
)
)

echo %Files%
!PathToExe! --sum-reports --report_file=.\..\..\..\..\generatedFiles\LinesofCode\TotalText_Report  !Files!
!PathToExe! --sum-reports --csv --report_file=.\..\..\..\..\generatedFiles\LinesofCode\Management_Report !Files!
rename .\..\..\..\..\generatedFiles\LinesofCode\TotalText_Report.lang TotalText_Report_Lang.txt
rename .\..\..\..\..\generatedFiles\LinesofCode\TotalText_Report.file TotalText_Report_File.txt
rename .\..\..\..\..\generatedFiles\LinesofCode\Management_Report.lang Management_Report_Lang.csv
rename .\..\..\..\..\generatedFiles\LinesofCode\Management_Report.file Management_Report_File.csv

mkdir .\..\..\..\..\generatedFiles\SWQualityReports\CountLinesofCode_report
copy .\..\..\..\..\generatedFiles\LinesofCode\*.* .\..\..\..\..\generatedFiles\SWQualityReports\CountLinesofCode_report
python cLocToExcel.py

endlocal