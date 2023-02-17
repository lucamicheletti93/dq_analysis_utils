from telnetlib import Telnet
import matplotlib.pyplot as plt
import array as arr
import numpy as np
import os
import sys
import argparse
import yaml
import ROOT
from os import path

def download(inputCfg):
    print("----- Download and save files in %s -----" % (inputCfg["input"]["output_dir_name"]))
    for iRun in range(0, len(inputCfg["input"]["run_list"])):

        file_type = inputCfg["input"]["file_type"]
        run = inputCfg["input"]["run_list"][iRun]
        alien_path = inputCfg["input"]["alien_input_path"][iRun]
        output_dir = inputCfg["input"]["output_dir_name"]
        
        os.system("mkdir -p %s/%s" % (output_dir, run))
        os.system("alien_cp alien://%s/%s file:%s/%s/." % (alien_path, file_type, output_dir, run))


### ### ###
def main():
    parser = argparse.ArgumentParser(description='Arguments to pass')
    parser.add_argument('cfgFileName', metavar='text', default='config.yml', help='config file name')
    parser.add_argument("--download", help="Enable trending vs run number", action="store_true")
    args = parser.parse_args()

    print('Loading task configuration: ...', end='\r')
    with open(args.cfgFileName, 'r') as ymlCfgFile:
        inputCfg = yaml.load(ymlCfgFile, yaml.FullLoader)
    print('Loading task configuration: Done!')

    if args.download:
        download(inputCfg)

main()