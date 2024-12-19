# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 17:15:01 2019

@author: YAH3KOR
"""
import numpy as np
import pandas as pd
import subprocess
import sys

def get_grp(x, df, col_name, my_list):
    for c in my_list:
       if c in df.loc[x][col_name]:
            return c

variant = sys.argv[1]
subprocess.run(["genLOC.bat"])
raw_data = pd.read_csv("LOC_ATR.csv",names=["raw_data"] )
stripped_data = raw_data['raw_data'].str.strip()
stripped_data.replace(to_replace=r'^.*total.*$|^.*\.txt.*$|^.*\.flux.*$|^.*Invalid.*$|^.*ip_if.*$|^.*rc_fw.*$|^.*cubas/gen.*$|^.*directory.*$|^.*ip_dc.*$|^.*Ethernet_LRR.*$',value=np.NaN, regex=True, inplace=True)
stripped_data.dropna(inplace=True)
clean_data = stripped_data.str.split(expand=True)
clean_data.columns = ['Loc','File']
clean_data['Loc'] = clean_data['Loc'].astype(int)
total_loc = clean_data.Loc.sum()
components = clean_data.File.str.extract('^.*ad_radar_apl/component/(\w*)/.*$', expand = True)
components.dropna(inplace=True)
components.drop_duplicates(inplace=True)
components_generic = pd.DataFrame(["tools", "btc_tools", "athena_mt", "main", "stubs", "Vector", "if_prem_addons"])
components = components.append(components_generic)
components.columns = ['Name']
grouped_data = clean_data.groupby(lambda x : get_grp(x, clean_data, 'File', components.Name))

print("------------------------------------------------------------------------------------")
print("Summary of lines of code per component:")
print(grouped_data.sum())
print("------------------------------------------------------------------------------------")
print("Total lines of code in project : " ,total_loc)
print("\n\n")

clean_data_c = clean_data.copy()
clean_data_c.columns = ['Loc_c','File']
clean_data_c.File = clean_data_c.File.str.extract('^(.*\.c)$', expand = True)
clean_data_c.dropna(inplace=True)
grouped_data_c = clean_data_c.groupby(lambda x : get_grp(x, clean_data_c, 'File', components.Name))
total_loc_c = clean_data_c.Loc_c.sum()

clean_data_h = clean_data.copy()
clean_data_h.columns = ['Loc_h','File']
clean_data_h.File = clean_data_h.File.str.extract('^(.*\.h)$', expand = True)
clean_data_h.dropna(inplace=True)
grouped_data_h = clean_data_h.groupby(lambda x : get_grp(x, clean_data_h, 'File', components.Name))
total_loc_h = clean_data_h.Loc_h.sum()

grouped_data_c_df = pd.concat([pd.DataFrame(grouped_data_c.sum()), pd.DataFrame(grouped_data_h.sum())], axis = 1)
grouped_data_c_df.loc['Total'] = [total_loc_c,total_loc_h]
grouped_data_c_df.fillna(0,inplace = True)
grouped_data_c_df.Loc_c = grouped_data_c_df.Loc_c.astype(int) 
grouped_data_c_df.Loc_h = grouped_data_c_df.Loc_h.astype(int) 

print("------------------------------------------------------------------------------------")
print("Summary of lines of code for all C files per component:")
print("------------------------------------------------------------------------------------")
print(grouped_data_c_df)
print("------------------------------------------------------------------------------------")
print("Total lines of C code in project : " ,total_loc_c+total_loc_h)
print("\n\n")

clean_data_cpp = clean_data.copy()
clean_data_cpp.columns = ['Loc_cpp','File']
clean_data_cpp.File = clean_data_cpp.File.str.extract('^(.*\.cpp)$', expand = True)
clean_data_cpp.dropna(inplace=True)
grouped_data_cpp = clean_data_cpp.groupby(lambda x : get_grp(x, clean_data_cpp, 'File', components.Name))
total_loc_cpp = clean_data_cpp.Loc_cpp.sum()

clean_data_hpp = clean_data.copy()
clean_data_hpp.columns = ['Loc_hpp','File']
clean_data_hpp.File = clean_data_hpp.File.str.extract('^(.*\.hpp)$', expand = True)
clean_data_hpp.dropna(inplace=True)
grouped_data_hpp = clean_data_hpp.groupby(lambda x : get_grp(x, clean_data_hpp, 'File', components.Name))
total_loc_hpp = clean_data_hpp.Loc_hpp.sum()

grouped_data_cpp_df = pd.concat([pd.DataFrame(grouped_data_cpp.sum()), pd.DataFrame(grouped_data_hpp.sum())], axis = 1)
grouped_data_cpp_df.loc['Total'] = [total_loc_cpp,total_loc_hpp]
grouped_data_cpp_df.fillna(0,inplace = True)
grouped_data_cpp_df.Loc_cpp = grouped_data_cpp_df.Loc_cpp.astype(int)
grouped_data_cpp_df.Loc_hpp = grouped_data_cpp_df.Loc_hpp.astype(int)

print("------------------------------------------------------------------------------------")
print("Summary of lines of code for all C++ files per component:")
print("------------------------------------------------------------------------------------")
print(grouped_data_cpp_df)
print("------------------------------------------------------------------------------------")
print("Total lines of C++ code in the project :", total_loc_cpp+total_loc_hpp)
print("\n\n")


with open("LinesofCode.txt", "w") as text_file:

    print("------------------------------------------------------------------------------------", file = text_file)
    print("Summary of lines of code per component:", file = text_file)
    print(grouped_data.sum(), file = text_file)
    print("------------------------------------------------------------------------------------", file = text_file)
    print("Total lines of code in project : " ,total_loc, file = text_file)
    print("\n\n", file = text_file)

    print("------------------------------------------------------------------------------------", file = text_file)
    print("Summary of lines of code for all C files per component:", file = text_file)
    print("------------------------------------------------------------------------------------", file = text_file)
    print(grouped_data_c_df, file = text_file)
    print("------------------------------------------------------------------------------------", file = text_file)
    print("Total lines of C code in project : " ,total_loc_c+total_loc_h, file = text_file)
    print("\n\n", file = text_file)

    print("------------------------------------------------------------------------------------", file = text_file)
    print("Summary of lines of code for all C++ files per component:", file = text_file)
    print("------------------------------------------------------------------------------------", file = text_file)
    print(grouped_data_cpp_df, file = text_file)
    print("------------------------------------------------------------------------------------",  file = text_file)
    print("Total lines of C++ code in the project :", total_loc_cpp+total_loc_hpp , file = text_file)
    print("\n\n", file = text_file)

subprocess.run(["copy_loc.bat", "-hw", variant])