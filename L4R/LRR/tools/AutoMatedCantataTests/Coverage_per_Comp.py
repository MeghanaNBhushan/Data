#!/usr/bin/env python
# -*- coding: utf-8 -*- import os
"""
Created on Wed Oct 28 10:05:38 2020

@author: GMB5KOR
"""
from bs4 import BeautifulSoup
import requests
import shutil
import re
import sys, os
import xlsxwriter

# count the arguments
arguments = len(sys.argv) - 1  

print ("the script is called with %i arguments" % (arguments))  

# read commandline arguments, first
fullCmdArguments = sys.argv

# - further arguments
argumentList = fullCmdArguments[1:]

#print ("List of arguments %s" %(argumentList))


if (arguments > 1) or (arguments < 1):
     print("The python arguments are too much!")
     
else:
     LRR_HW_Variant = argumentList[0]




#Get the path of the input file
cwd = os.getcwd()
projectPath = os.path.join(cwd, '../../../')
SourceFile = os.path.join(projectPath, 'generatedFiles/SWQualityReports/Cantata/'+'Host_Radar_'+LRR_HW_Variant)
CompPath1 = os.path.join(projectPath, 'ad_radar_apl/component')
Destination = os.path.realpath('../../../generatedFiles/SWQualityReports/Coverage_report')
if not os.path.exists(Destination):
    os.makedirs(Destination)

workbook = xlsxwriter.Workbook('../../../generatedFiles/SWQualityReports/Coverage_report/'+'CoveragePerComp_'+LRR_HW_Variant+'.xlsx')
worksheet = workbook.add_worksheet("Coverage_report")
worksheet.set_column('A:Z', 20)
worksheet.set_column('B1:Z1', 15)

cell_format1 = workbook.add_format()
cell_format1 = workbook.add_format({'bold': True, 'font_color': 'blue', 'font_size': 14, 'align': 'centre', 'center_across': True})
cell_format2 = workbook.add_format({'bold': True, 'font_color': 'red', 'font_size': 14, 'align': 'centre', 'fg_color': 'yellow'})
cell_format3 = workbook.add_format({'bold': True, 'font_color': 'black', 'font_size': 12, 'align': 'centre'})

worksheet.write('A1', 'Component', cell_format1)
worksheet.write('B1', 'C0 Coverage[%]', cell_format1)
worksheet.write('C1', 'C1 Coverage[%]', cell_format1)
worksheet.write('D1', 'MCDC Coverage[%]', cell_format1)


components = []
Component1 = []
Comp1 = os.listdir(CompPath1)
for ele in Comp1:
    if ele not in ("doc", "Hotfix"):
        Component1.append(ele)
Component2 = ["arch", "ToBeCleanUp"]
Components=Component1+Component2

number=0
row=1
column=0
comp_count=0
for name in Components:
    worksheet.write(row, column, name, cell_format3)
    row+=1
    comp_count+=1
row=1
column=1

Cantata_Components= os.listdir(SourceFile)
for name in Components:
    C0_Coverage=0
    C1_Coverage=0
    MCDC_Coverage=0
    for comp in Cantata_Components:
        if name == comp:
            url = os.path.join(SourceFile,comp+"/Cantata Output/test_report.html")
            soup = BeautifulSoup(open(url), "lxml")
            table = soup.find("table", attrs={"class":"projectsummary"})
            headings = [td.get_text() for td in table.find("tr").find_all("td")]
            del headings[0]
            value = []
            value=["Statement", "Decision", "Boolean Operand Effectiveness (Masking)", "Total number of test cases","Test cases passed"]
            heading = []
            for ele in headings:
                heading.append(str(ele))
            i=0,
            for i in range(0,len(heading)):
                if heading[i] == value[0]:
                    Statement=heading[i+2]
                if heading[i] == value[1]:
                    Decision=heading[i+2]
                if heading[i] == value[2]:
                    Boolean_masking_effectiveness=heading[i+2]
                if heading[i] == value[3]:
                    total_testcases=heading[i+1]
                if heading[i] == value[4]:
                    tests_passed=heading[i+1]
            C0_Coverage = ((int(Statement.strip('%'))*int(tests_passed))/int(total_testcases))
            C1_Coverage = ((int(Decision.strip('%'))*int(tests_passed))/int(total_testcases))
            MCDC_Coverage = ((int(Boolean_masking_effectiveness.strip('%'))*int(tests_passed))/int(total_testcases))
    worksheet.write(row, column, round(C0_Coverage,2), cell_format3)
    worksheet.write(row, column+1, round(C1_Coverage,2), cell_format3)
    worksheet.write(row, column+2, round(MCDC_Coverage,2), cell_format3)
    row=row+1
print("Coverage report generated succesfully")
workbook.close()