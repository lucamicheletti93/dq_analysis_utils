import os
import sys
import argparse
import yaml

def run_on_grid(inputCfg, mode):
    '''
    function for run jobs on alien grid
    '''
    if not os.path.isdir(inputCfg["output"]["output_dir"]) :
        print("the directory does not exist, creating %s" % (inputCfg["output"]["output_dir"]))
        os.system("mkdir -p %s" % (inputCfg["output"]["output_dir"]))

    if mode == "full" :
        fIn  = open(inputCfg["input"]["run_list_file"], "r")
        fOut = open("%s/%s" % (inputCfg["output"]["output_dir"], inputCfg["output"]["submitted_output_file"]), "w")

    if mode == "terminate" :
        if not os.path.isfile("%s/%s" % (inputCfg["output"]["output_dir"], inputCfg["output"]["submitted_output_file"])) :
            print('Submitted jobs file does not exist! Do --full before')
            return
        fIn  = open("%s/%s" % (inputCfg["output"]["output_dir"], inputCfg["output"]["submitted_output_file"]), "r")
        fOut = open("%s/%s" % (inputCfg["output"]["output_dir"], inputCfg["output"]["terminated_output_file"]), "w")

    for run in fIn:
        print(fr"aliroot -b -q ReadMCJPsi_Grid.C\(\"%s\",%i\)" % (mode, int(run)))
        #os.system(fr"aliroot -b -q ReadMCJPsi_Grid.C\(\"%s\",%i\)" % (mode, int(run))) // enable if you want to run on grid
        fOut.write(run)

def copy_from_grid(inputCfg):
    '''
    function for downloading files from alien grid
    '''
    if not os.path.isfile("%s/%s" % (inputCfg["output"]["output_dir"], inputCfg["output"]["terminated_output_file"])) :
        print('Terminated jobs file does not exist! Do --terminate before')
        return
    fIn  = open("%s/%s" % (inputCfg["output"]["output_dir"], inputCfg["output"]["terminated_output_file"]), "r")
    for run in fIn:
        print("alien_cp alien://%s/AO2D.root file:%s" % (inputCfg["input"]["alien_input_path"], inputCfg["output"]["alien_output_path"]))
        #os.system("alien_cp alien://%s/AO2D.root file:%s" % (inputCfg["input"]["alien_input_path"], inputCfg["output"]["alien_output_path"])) // enable if you want to run on grid

def merge_files(inputCfg):
    '''
    function for merging files
    '''
    if not os.path.isfile("%s/%s" % (inputCfg["output"]["output_dir"], inputCfg["output"]["terminated_output_file"])) :
        print('Terminated jobs file does not exist! Do --terminate before')
        return
    mergeCommand = "hadd -f %s.root " % (inputCfg["merging"]["output_file_prefix"])
    fIn  = open("%s/%s" % (inputCfg["output"]["output_dir"], inputCfg["output"]["terminated_output_file"]), "r")
    for run in fIn:
        mergeCommand += "%s/%s%i.root " % (inputCfg["merging"]["output_path"], inputCfg["merging"]["input_file_prefix"], int(run))
    print(mergeCommand)
    print('Proceed with the merging? (true / false)')
    merge_exec = input()
    if merge_exec == 'true' :
        os.system(mergeCommand)


def main():
    parser = argparse.ArgumentParser(description='Arguments to pass')
    parser.add_argument('cfgFileName', metavar='text', default='config.yml', help='config file name')
    parser.add_argument("--full", help="submit your task in full mode", action="store_true")
    parser.add_argument("--terminate", help="terminate your task", action="store_true")
    parser.add_argument("--copy", help="download files from alien grid", action="store_true")
    parser.add_argument("--merge", help="merge output files", action="store_true")
    args = parser.parse_args()

    print('Loading task configuration: ...', end='\r')
    with open(args.cfgFileName, 'r') as ymlCfgFile:
        inputCfg = yaml.load(ymlCfgFile, yaml.FullLoader)
    print('Loading task configuration: Done!')
    if args.full:
        run_on_grid(inputCfg, "full")
    if args.terminate:
        run_on_grid(inputCfg, "terminate")
    if args.copy:
        copy_from_grid(inputCfg)
    if args.merge:
        merge_files(inputCfg)

main()
