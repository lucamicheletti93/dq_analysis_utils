import os
import sys
import argparse
import json
import random

def run_sim(inputCfg, mode):
    '''
    create simulation list for running in parallel
    '''
    if not os.path.isdir(inputCfg["output"]["output_dir"]) :
        print("the directory does not exist, creating %s" % (inputCfg["output"]["output_dir"]))
        os.system("mkdir -p %s" % (inputCfg["output"]["output_dir"]))

    fOut = open("%s/%s" % (inputCfg["output"]["output_dir"], inputCfg["output"]["output_file"]), "w")

    if mode == "config" :
        for id in range(0, inputCfg["input"]["n_sim"]) :
            print("$ALIDPG_ROOT/bin/aliroot_dpgsim.sh --debug --run 289971 --mode %s --uid %d --seed %d --generator Custom --nevents %d" % (inputCfg["input"]["mode"], id, id, inputCfg["input"]["n_events"]))
            fOut.write("$ALIDPG_ROOT/bin/aliroot_dpgsim.sh --debug --run 289971 --mode %s --uid %d --seed %d --generator Custom --nevents %d \n" % (inputCfg["input"]["mode"], id, id, inputCfg["input"]["n_events"]))

    if mode == "run" :
        print("parallel -j %d --timeout %d < %s/%s" % (inputCfg["parallel"]["n_jobs"], inputCfg["parallel"]["timeout"], inputCfg["output"]["output_dir"], inputCfg["output"]["output_file"]))
        os.system("parallel -j %d --timeout %d < %s/%s" % (inputCfg["parallel"]["n_jobs"], inputCfg["parallel"]["timeout"], inputCfg["output"]["output_dir"], inputCfg["output"]["output_file"]))

def main():
    parser = argparse.ArgumentParser(description='Arguments to pass')
    parser.add_argument('cfgFileName', metavar='text', default='config.yml', help='config file name')
    parser.add_argument("--config", help="config your simulation", action="store_true")
    parser.add_argument("--run", help="run simulations", action="store_true")
    args = parser.parse_args()

    print('Loading task configuration: ...', end='\r')
    with open(args.cfgFileName, 'r') as jsonCfgFile:
        inputCfg = json.load(jsonCfgFile)
    print('Loading task configuration: Done!')
    if args.config:
        run_sim(inputCfg, "config")
    if args.run:
        run_sim(inputCfg, "run")

main()
