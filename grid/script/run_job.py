import os
import sys
import argparse
import yaml

def run_on_grid(inputCfg, mode):
    if not os.path.isdir(inputCfg["output"]["output_dir"]) :
        print("the directory does not exist, creating %s" % (inputCfg["output"]["output_dir"]))
        os.system("mkdir -p %s" % (inputCfg["output"]["output_dir"]))

    if mode == "full" :
        fIn  = open(inputCfg["input"]["run_list_file"], "r")
        fOut = open("%s/%s" % (inputCfg["output"]["output_dir"], inputCfg["output"]["submitted_output_file"]), "w")

    if mode == "terminate" :
        if not os.path.isfile("%s/%s" % (inputCfg["output"]["output_dir"], inputCfg["output"]["submitted_output_file"])) :
            print('Submitted job file does not exist! Do --full before')
            return
        fIn  = open("%s/%s" % (inputCfg["output"]["output_dir"], inputCfg["output"]["submitted_output_file"]), "r")
        fOut = open("%s/%s" % (inputCfg["output"]["output_dir"], inputCfg["output"]["terminated_output_file"]), "w")

    for run in fIn:
        print(fr"aliroot -b -q ReadMCJPsi_Grid.C\(\"%s\",%i\)" % (mode, int(run)))
        #os.system(fr"aliroot -b -q ReadMCJPsi_Grid.C\(\"%s\",%i\)" % (mode, int(run))) // enable if you want to run on grid
        fOut.write(run)



def main():
    parser = argparse.ArgumentParser(description='Arguments to pass')
    parser.add_argument('cfgFileName', metavar='text', default='config.yml', help='config file name')
    parser.add_argument("--full", help="submit your task in full mode", action="store_true")
    parser.add_argument("--terminate", help="terminate your task", action="store_true")
    args = parser.parse_args()

    print('Loading task configuration: ...', end='\r')
    with open(args.cfgFileName, 'r') as ymlCfgFile:
        inputCfg = yaml.load(ymlCfgFile, yaml.FullLoader)
    print('Loading task configuration: Done!')
    if args.full:
        run_on_grid(inputCfg, "full")
    if args.terminate:
        run_on_grid(inputCfg, "terminate")

main()
