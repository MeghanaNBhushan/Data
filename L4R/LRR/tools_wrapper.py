#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: UTF-8
import sys
import subprocess
import argparse
import os.path

script_dir = os.path.dirname(os.path.realpath(__file__))
tool_dir = "C:\TCC\itc2"


def parse_arguments():
    """Reads the input parameters"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--itc2_file", help='Provide itc2 version text file Ex: tcc_toolversion_itc2.txt ', default = 'tcc_toolversion_itc2.txt')
    args = parser.parse_args()
    return args


def main(args):
    print("Reading the itc2 file version :", args.itc2_file)
    if os.path.isfile(os.path.join(script_dir, args.itc2_file)):
        with open(os.path.join(script_dir, args.itc2_file), 'r') as file:
            BTC_version = file.read()
            file_len = len(BTC_version)
            if file_len == 0:
                print(f"{args.itc2_file} file is empty and no version available")
                sys.exit(1)
                
    else:
        print("Provide the itc2 file:", args.itc2_file)
        sys.exit(1)

    os.chdir(tool_dir)
    result = subprocess.call(['itc2', 'install', BTC_version, '-d', script_dir], shell=True) # To install itc2 version and generate TCC_Toolpaths.bat and TCC_Toolpaths.cmake
    
    if result:
        print(f"Warning: Installing itc2 version failed with exitcode '{result}'.")
        sys.exit(result)


if __name__ == '__main__':
    args = parse_arguments()
    main(args)