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
destinationPath = os.path.join(projectPath, 'generatedFiles/TaskApplTests/Sw_int_test_Runnables_initialization.txt')
     
FunctionFound = False
InsideFunction = False

dsp_xR5yU_master_Found = False
dsp_xR5yU_slave_Found = False
locdataif_Runnable_Found = False
EgoVehDataIF_Runnable_Found = False 
EgoVehDataIF_Runnable_Slave_Found = False
netRunnable_Found = False
CInputHandlerRunnable_Found = False
MPM_Runnable_Found = False
MPM_Runnable_Slave_Found = False
runnableDia_Found = False
SysEvMRunnable_Found = False
SysEvMRunnable_Slave_Found = False
dspWorker1_master_Found = False
dspWorker1_slave_Found = False
dspWorker2_Found = False
DMP_Runnable_Found = False
SDM_Runnable_Found = False
SDM_Runnable_Slave_Found = False
SensorStateInfoRunnable_Found = False

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
            if("dsp_xR5yU_master.init();" in line.strip()):
                print(line.strip())
                dsp_xR5yU_master_Found=True
            if("dsp_xR5yU_slave.init();" in line.strip()):
                print(line.strip())
                dsp_xR5yU_slave_Found=True
            if("locdataif_Runnable.init();" in line.strip()):
                print(line.strip())
                locdataif_Runnable_Found=True
            if("EgoVehDataIF_Runnable.init();" in line.strip()):
                print(line.strip())
                EgoVehDataIF_Runnable_Found=True
            if("EgoVehDataIF_Runnable_Slave.init();" in line.strip()):
                print(line.strip())
                EgoVehDataIF_Runnable_Slave_Found=True    
            if("netRunnable.init();" in line.strip()):
                print(line.strip())
                netRunnable_Found=True
            if("CInputHandlerRunnable.init();" in line.strip()):
                print(line.strip())
                CInputHandlerRunnable_Found=True
            if("MPM_Runnable.init();" in line.strip()):
                print(line.strip())
                MPM_Runnable_Found=True
            if("MPM_Runnable_Slave.init();" in line.strip()):
                print(line.strip())
                MPM_Runnable_Slave_Found=True 
            if("runnableDia.init();" in line.strip()):
                print(line.strip())
                runnableDia_Found=True 
            if("SysEvMRunnable.init();" in line.strip()):
                print(line.strip())
                SysEvMRunnable_Found=True 
            if("SysEvMRunnable_Slave.init();" in line.strip()):
                print(line.strip())
                SysEvMRunnable_Slave_Found=True 
            if("dspWorker1_master.init();" in line.strip()):
                print(line.strip())
                dspWorker1_master_Found=True
            if("dspWorker1_slave.init();" in line.strip()):
                print(line.strip())
                dspWorker1_slave_Found=True
            if("dspWorker2.init();" in line.strip()):
                print(line.strip())
                dspWorker2_Found=True                 
            if("DMP_Runnable.init();" in line.strip()):
                print(line.strip())
                DMP_Runnable_Found=True
            if("SDM_Runnable.init();" in line.strip()):
                print(line.strip())
                SDM_Runnable_Found=True
            if("SDM_Runnable_Slave.init();" in line.strip()):
                print(line.strip())
                SDM_Runnable_Slave_Found=True
            if("SensorStateInfoRunnable.init();" in line.strip()):
                print(line.strip())
                SensorStateInfoRunnable_Found=True
            if line.strip() == "}":
                print("end of function")
                InsideFunction = False

# create report folder
Destination = os.path.realpath('../../../../generatedFiles/TaskApplTests')
if not os.path.exists(Destination):
    os.makedirs(Destination)
    #analysis
# create report
file1 = open(destinationPath, 'w')
message=""
if(dsp_xR5yU_master_Found ==True):
    message = "ID557532;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557532;FAILED\n"
    file1.writelines(message)
    
if(dsp_xR5yU_slave_Found ==True):
    message = "ID557532;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557532;FAILED\n"
    file1.writelines(message)

if(locdataif_Runnable_Found ==True):
    message = "ID557548;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557548;FAILED\n"
    file1.writelines(message)
    
if(EgoVehDataIF_Runnable_Found ==True):
    message = "ID557552;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557552;FAILED\n"
    file1.writelines(message)

if(EgoVehDataIF_Runnable_Slave_Found ==True):
    message = "ID557552;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557552;FAILED\n"
    file1.writelines(message)

if(netRunnable_Found ==True):
    message = "ID557547;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557547;FAILED\n"
    file1.writelines(message)
    
if(CInputHandlerRunnable_Found ==True):
    message = "ID598623;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID598623;FAILED\n"
    file1.writelines(message)
    
if(MPM_Runnable_Found ==True):
    message = "ID557551;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557551;FAILED\n"
    file1.writelines(message)

if(MPM_Runnable_Slave_Found ==True):
    message = "ID557551;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557551;FAILED\n"
    file1.writelines(message)

if(runnableDia_Found ==True):
    message = "ID557546;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557546;FAILED\n"
    file1.writelines(message)

if(SysEvMRunnable_Found ==True):
    message = "ID557529;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557529;FAILED\n"
    file1.writelines(message)

if(SysEvMRunnable_Slave_Found ==True):
    message = "ID557529;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557529;FAILED\n"
    file1.writelines(message)

if(dspWorker1_master_Found ==True):
    message = "ID557544;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557544;FAILED\n"
    file1.writelines(message)

if(dspWorker1_slave_Found ==True):
    message = "ID557544;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557544;FAILED\n"
    file1.writelines(message)
    
if(dspWorker2_Found ==True):
    message = "ID557549;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557549;FAILED\n"
    file1.writelines(message)

if(DMP_Runnable_Found ==True):
    message = "ID557550;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557550;FAILED\n"
    file1.writelines(message)

if(SDM_Runnable_Found ==True):
    message = "ID557545;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557545;FAILED\n"
    file1.writelines(message)

if(SDM_Runnable_Slave_Found ==True):
    message = "ID557545;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID557545;FAILED\n"
    file1.writelines(message)

if(SensorStateInfoRunnable_Found ==True):
    message = "ID578368;SUCCESS\n"
    file1.writelines(message)
else:
    message = "ID578368;FAILED\n"
    file1.writelines(message)

file1.close()
if (dsp_xR5yU_master_Found and dspWorker1_slave_Found and locdataif_Runnable_Found and EgoVehDataIF_Runnable_Found and EgoVehDataIF_Runnable_Slave_Found and netRunnable_Found and CInputHandlerRunnable_Found and MPM_Runnable_Found and MPM_Runnable_Slave_Found and runnableDia_Found and SysEvMRunnable_Found and SysEvMRunnable_Slave_Found and dspWorker1_master_Found and dspWorker1_slave_Found and dspWorker2_Found and DMP_Runnable_Found and SDM_Runnable_Found and SDM_Runnable_Slave_Found and SensorStateInfoRunnable_Found ) == True:
    exit(0)
else:
    exit(1)
