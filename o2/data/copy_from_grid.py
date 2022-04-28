import os
import sys

def copy_from_grid():
        '''
        function for downloading files from alien grid
        '''
        # Path of the alien directory
        alienPrefix = "/alice/sim/2022";
        # Path of the local directory
        alienDirName = "LHC22c5/505548/AOD"
        # working directory
        workDir = os.getcwd()
        # output file name
        fOutName = "LHC22c5_505548.txt"
        # Number of files to download
        nFiles = 23

        fOut = open("%s" % (fOutName), "w")

        for iter in range(1, nFiles):
            if iter < 10 :
                if not os.path.isfile("%s/00%d/AO2D.root" % (alienDirName, iter)) :
                        print("alien_cp alien://%s/%s/00%d/AO2D.root file:%s/00%d/AO2D.root" % (alienPrefix, alienDirName, iter, alienDirName, iter))
                        os.system("alien_cp alien://%s/%s/00%d/AO2D.root file:%s/00%d/AO2D.root" % (alienPrefix, alienDirName, iter, alienDirName, iter))
                if os.path.isfile("%s/00%d/AO2D.root" % (alienDirName, iter)) :
                        fOut.write("%s/%s/00%d/AO2D.root\n" % (workDir, alienDirName, iter))
            if iter >= 10 :
                if not os.path.isfile("%s/0%d/AO2D.root" % (alienDirName, iter)) :
                        print("alien_cp alien://%s/%s/0%d/AO2D.root file:%s/0%d/AO2D.root" % (alienPrefix, alienDirName, iter, alienDirName, iter))
                        os.system("alien_cp alien://%s/%s/0%d/AO2D.root file:%s/0%d/AO2D.root" % (alienPrefix, alienDirName, iter, alienDirName, iter))
                if os.path.isfile("%s/0%d/AO2D.root" % (alienDirName, iter)) :
                        fOut.write("%s/%s/0%d/AO2D.root\n" % (workDir, alienDirName, iter))

def main():
    copy_from_grid()

main()
