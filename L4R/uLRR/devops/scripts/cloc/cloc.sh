#!/bin/bash
# This script generates a Lines of code reports for the given directory.
ROOT_DIR=$1
LOC_dir=("${@:2}")
Files=""

echo "Root directory is $ROOT_DIR"

for subdir in "${LOC_dir[@]}"; 
do
  echo "Selected subdirectory is $subdir"
  dir="$ROOT_DIR/software/$subdir"

  if [ -d "$dir" ]; then
    report_file="$ROOT_DIR/TestResults/LinesofCode/cloc_Reports/component/$subdir"
    cloc --include-ext=cpp,hpp --report-file="$report_file" "$dir"

    if [ -e "$report_file" ]; then
      Files="$Files $(ls -1d $report_file)"
    fi
  fi
done

echo $Files

cloc --quiet --sum-reports --report_file="$ROOT_DIR/TestResults/LinesofCode/TotalText_Report" $Files
cloc --quiet --sum-reports --csv --report_file="$ROOT_DIR/TestResults/LinesofCode/Management_Report" $Files

mv "$ROOT_DIR/TestResults/LinesofCode/TotalText_Report.lang" "$ROOT_DIR/TestResults/LinesofCode/TotalText_Report_Lang.txt"
mv "$ROOT_DIR/TestResults/LinesofCode/TotalText_Report.file" "$ROOT_DIR/TestResults/LinesofCode/TotalText_Report_File.txt"
mv "$ROOT_DIR/TestResults/LinesofCode/Management_Report.lang" "$ROOT_DIR/TestResults/LinesofCode/Management_Report_Lang.csv"
mv "$ROOT_DIR/TestResults/LinesofCode/Management_Report.file" "$ROOT_DIR/TestResults/LinesofCode/Management_Report_File.csv"