import shutil
import re
import sys, os
import xlsxwriter
import openpyxl 


cwd = os.getcwd()
projectPath = os.path.join(cwd, '../../../../')
Destination = os.path.realpath('../../../../generatedFiles/SWQualityReports/CountLinesofCode_report')
SourceFile = os.path.join(projectPath, 'generatedFiles/'+'LinesofCode'+'/Management_Report_File.csv')

CompPath1 = os.path.join(projectPath, 'ad_radar_apl/component')
if not os.path.exists(Destination):
    os.makedirs(Destination)
DestinationFile = os.path.realpath('../../../../generatedFiles/SWQualityReports/CountLinesofCode_report/'+'CLOC.txt')

workbook = xlsxwriter.Workbook('../../../../generatedFiles/SWQualityReports/CountLinesofCode_report/'+'CLOC.xlsx')
worksheet = workbook.add_worksheet()
worksheet.set_column('A:Z', 20)
worksheet.set_column('B1:Z1', 15)

cell_format1 = workbook.add_format()
cell_format1 = workbook.add_format({'bold': True, 'font_color': 'blue', 'font_size': 14, 'align': 'centre', 'center_across': True})
cell_format2 = workbook.add_format({'bold': True, 'font_color': 'red', 'font_size': 14, 'align': 'centre', 'fg_color': 'yellow'})
cell_format3 = workbook.add_format({'bold': True, 'font_color': 'black', 'font_size': 12, 'align': 'centre'})
cell_format4 = workbook.add_format({'bold': True, 'font_color': 'blue', 'font_size': 14, 'align': 'left', 'center_across': True})

worksheet.write('A1', 'Components', cell_format1)

worksheet.write('B1', 'Lines of Code', cell_format1)



components = []
Component1 = []
Comp1 = os.listdir(CompPath1)
for ele in Comp1:
    if ele not in ("doc", "Hotfix"):
        Component1.append(ele)
Component2 = ["arch", "ToBeCleanUp"]
Components=Component1+Component2

row=1
column=0
comp_count=0
for name in Components:
    worksheet.write(row, column, name, cell_format3)
    row+=1
    comp_count+=1
row=1
column=0
comp_count=0
row=1
column=1
with open(SourceFile, 'r') as f:
    datafile = f.readline() # Ignore header line
    datafile = f.readlines()
    for name in Components:
        sum = 0
        for line in datafile:
            #print(line)
            word=line.split(",")
            list=word[1]
            #print(list)                
            splitList1= list.split('\\')
            if 'cloc_Details' in splitList1:
                index = splitList1.index('cloc_Details')
                splitList = splitList1[index:]
                RelPath = splitList[0]
                i = 1;
                while (i) < (len(splitList)):
                    RelPath += '\\' + splitList[i]
                    i +=1
                if name in RelPath:
                    sum = sum + int(word[4])
        worksheet.write(row, column, sum, cell_format3)
        row+=1
workbook.close()
