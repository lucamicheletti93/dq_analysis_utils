import os
import sys
import yaml
import numpy as np
import argparse
import ROOT
from ROOT import *


def qc(inputCfg):
    #gStyle.SetPalette(ROOT.kRainBow)

    fInNames = inputCfg["inputs"]["data"]
    labels = inputCfg["inputs"]["labels"]
    colors = inputCfg["inputs"]["colors"]
    colCounter = []

    # Table Maker
    dirNames = inputCfg["table_maker"]["directory"]
    selNames = inputCfg["table_maker"]["selections"]
    varNames = inputCfg["table_maker"]["vars"]
    rebins = inputCfg["table_maker"]["rebins"]
    minRanges = inputCfg["table_maker"]["minRanges"]
    maxRanges = inputCfg["table_maker"]["maxRanges"]

    histsTM = [[[[None for _ in range(10)] for _ in range(10)] for _ in range(10)] for _ in range(10)]

    for i_fInName, fInName in enumerate(fInNames):
        fIn = TFile(fInName, "READ")
        histEvCount = fIn.Get("event-selection-task/hColCounterAcc")
        colCounter.append(histEvCount.GetBinContent(1))
        for i_dirName, dirName in enumerate(dirNames):
            hlistIn = fIn.Get(dirName)
            for i_selName, selName in enumerate(selNames):
                listIn = hlistIn.FindObject(selName)
                for i_varName, varName in enumerate(varNames):
                    histsTM[i_fInName][i_dirName][i_selName][i_varName] = listIn.FindObject(varName)
                    histsTM[i_fInName][i_dirName][i_selName][i_varName].SetTitle(labels[i_fInName])
                    histsTM[i_fInName][i_dirName][i_selName][i_varName].SetLineColor(colors[i_fInName])
                    histsTM[i_fInName][i_dirName][i_selName][i_varName].SetLineWidth(2)
                    histsTM[i_fInName][i_dirName][i_selName][i_varName].Rebin(rebins[i_fInName])
                    histsTM[i_fInName][i_dirName][i_selName][i_varName].GetXaxis().SetRangeUser(minRanges[i_varName], maxRanges[i_varName])
                    if inputCfg["inputs"]["normToColls"]: histsTM[i_fInName][i_dirName][i_selName][i_varName].Scale(1. / colCounter[i_fInName])

    for i_dirName, dirName in enumerate(dirNames):
        for i_selName, selName in enumerate(selNames):
            for i_varName, varName in enumerate(varNames):
                canvas = TCanvas(f'canvas_{selName}_{varName}', f'canvas_{selName}_{varName}', 600, 600)
                gPad.SetLogy(1)
                for i_fInName, fInName in enumerate(fInNames):
                    histsTM[i_fInName][i_dirName][i_selName][i_varName].Draw("H SAME")
                gPad.BuildLegend(0.78, 0.75, 0.980, 0.935,"","L")
                canvas.Update()
                canvas.SaveAs(f'plots/{selName}_{varName}.pdf')


    # Table Reader
    dirNames = inputCfg["table_reader"]["directory"]
    selNames = inputCfg["table_reader"]["selections"]
    varNames = inputCfg["table_reader"]["vars"]
    rebins = inputCfg["table_reader"]["rebins"]
    minRanges = inputCfg["table_reader"]["minRanges"]
    maxRanges = inputCfg["table_reader"]["maxRanges"]
    histsTR = [[[[None for _ in range(10)] for _ in range(10)] for _ in range(10)] for _ in range(10)]

    for i_fInName, fInName in enumerate(fInNames):
        fIn = TFile(fInName, "READ")
        for i_dirName, dirName in enumerate(dirNames):
            hlistIn = fIn.Get(dirName)
            for i_selName, selName in enumerate(selNames):
                listIn = hlistIn.FindObject(selName)
                for i_varName, varName in enumerate(varNames):
                    histsTR[i_fInName][i_dirName][i_selName][i_varName] = listIn.FindObject(varName)
                    histsTR[i_fInName][i_dirName][i_selName][i_varName].SetTitle(labels[i_fInName])
                    histsTR[i_fInName][i_dirName][i_selName][i_varName].SetLineColor(colors[i_fInName])
                    histsTR[i_fInName][i_dirName][i_selName][i_varName].SetLineWidth(2)
                    histsTR[i_fInName][i_dirName][i_selName][i_varName].Rebin(rebins[i_varName])
                    histsTR[i_fInName][i_dirName][i_selName][i_varName].GetXaxis().SetRangeUser(minRanges[i_varName], maxRanges[i_varName])
                    if inputCfg["inputs"]["normToColls"]: histsTR[i_fInName][i_dirName][i_selName][i_varName].Scale(1. / colCounter[i_fInName])

    for i_dirName, dirName in enumerate(dirNames):
        for i_selName, selName in enumerate(selNames):
            for i_varName, varName in enumerate(varNames):
                canvas = TCanvas(f'canvas_{selName}_{varName}', f'canvas_{selName}_{varName}', 600, 600)
                gPad.SetLogy(1)
                for i_fInName, fInName in enumerate(fInNames):
                    histsTR[i_fInName][i_dirName][i_selName][i_varName].Draw("H SAME")
                gPad.BuildLegend(0.78, 0.75, 0.980, 0.935,"","L")
                canvas.Update()
                canvas.SaveAs(f'plots/{selName}_{varName}.pdf')



def main():
    parser = argparse.ArgumentParser(description='Arguments to pass')
    parser.add_argument('cfgFileName', metavar='text', default='config.yml', help='config file name')
    parser.add_argument("--do_qc", help="Do simple QC", action="store_true")
    args = parser.parse_args()

    print('Loading task configuration: ...', end='\r')
    with open(args.cfgFileName, 'r') as ymlCfgFile:
        inputCfg = yaml.load(ymlCfgFile, yaml.FullLoader)
    print('Loading task configuration: Done!')

    if args.do_qc:
        qc(inputCfg)

main()