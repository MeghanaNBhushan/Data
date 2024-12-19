#this script copies togetter the Splunk upload files for LRR 5000 and LRR 60000
#!/usr/bin/env python
# -*- coding: utf-8 -*- import os
import xml.etree.ElementTree as ET
import shutil
import re
import sys, os
import difflib



# count the arguments
arguments = len(sys.argv) - 1  

print ("the script is called with %i arguments" % (arguments))  

# read commandline arguments, first
fullCmdArguments = sys.argv

# - further arguments
argumentList = fullCmdArguments[1:]

#print ("List of arguments %s" %(argumentList))


if (arguments > 0) or (arguments < 0):
     print("The python arguments are too much!")
     
cwd = os.getcwd()
projectPath = os.path.join(cwd, '../../../../')

sourcePath = os.path.join(projectPath, 'athena_prem_apl/main/callouts_interrupts/Task_ApplCpp.cpp')
destinationPath = os.path.join(projectPath, 'generatedFiles/TaskApplTests/Sw_int_test_Port_initialization.txt')

FunctionFound = False
InsideFunction = False
ConnectFound = False
InitBeforConnect = False
#C:\Users\SOT1ER\Desktop\NeuAthena\athena_frr_11316\athena_prem_apl\main\callouts_interrupts
#open file
with open(sourcePath,'r') as file:
    for line in file:
        #check Task_C0_Init_CppApplCbk 
        if line.strip() == "void Task_C0_Init_CppApplCbk(void)":
            print(line.strip())
            FunctionFound=True
        #check {
        elif line.strip() == "{" and FunctionFound == True :
            InsideFunction=True
            FunctionFound=False
        elif InsideFunction == True: 
            #check if there is an init(); funktion befor the scom::connect();
            if (".init();" in line.strip() and ConnectFound == False):
                InitBeforConnect = True           
#check scom::connect()
            if line.strip() == "scom::connect();":
                print(line.strip())
                ConnectFound = True;
            # check }
            elif line.strip() == "}" and ConnectFound == False:
                print("ERROR, scom::connect() not in void Task_C0_Init_CppApplCbk(void)")
                InsideFunction = False
            elif line.strip() == "}" and ConnectFound == True and InitBeforConnect== True:
                print("Error, scom::connect() in void Task_C0_Init_CppApplCbk(void), but a .init(); befor SCOM::connect()")
                InsideFunction = False
            elif line.strip() == "}" and ConnectFound == True and InitBeforConnect== False:
                print("SUCCESS, scom::connect() in void Task_C0_Init_CppApplCbk(void)")
                InsideFunction = False
        else:
            #just read
            pass

# create report folder
Destination = os.path.realpath('../../../../generatedFiles/TaskApplTests')
if not os.path.exists(Destination):
    os.makedirs(Destination)

file1 = open(destinationPath, 'w')
message=""
if(ConnectFound == True and InitBeforConnect == False):
    message = "ID557652;SUCCESS"
    file1.writelines(message)
    file1.close()
    exit(0)
elif (ConnectFound == True and InitBeforConnect == True):
    print("Found .Init(); befor scom::connect();, please correct this error")
    message = "ID557652;FAILED"
    file1.writelines(message)
    file1.close()
    exit(1)
else:
    message = "ID557652;FAILED"
    file1.writelines(message)
    file1.close()
    exit(1)



