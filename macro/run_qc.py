import matplotlib.pyplot as plt
import array as arr
import numpy as np
import os
import sys
import argparse
import yaml
import ROOT
from os import path
from ROOT import TCanvas, TF1, TFile, TPaveText, TMath
from ROOT import gROOT, gBenchmark, gPad, gStyle, kBlack
from ctypes import cdll
sys.path.append('../utils/')
from plot_library import Load_Style, Draw_Ratio_Plot
from function_library import Func_Exp, Func_Tot_ee

def comp():
    name_fInMC = "AnalysisResultsTM_LHC22c5_HL.root"
    name_fInData = "AnalysisResultsTM_OCT_apass3_HL.root"
    path_fIn = "/Users/lucamicheletti/GITHUB/dq_analysis_utils/o2/output"

def fit(inputCfg, mode):
    Load_Style()
    #fIn = TFile.Open("../grid/hyperloop/AnalysisResults_LHC18_dielectron.root")    # run2 converted data
    #fIn = TFile.Open("../o2/output/AnalysisResultsTR_OCT_apass3.root")             # apass3 pilot run
    fIn = TFile.Open(inputCfg["input"]["input_file_name"])
    hlist = fIn.Get("analysis-same-event-pairing/output")
    list = hlist.FindObject("PairsBarrelSEPM_jpsiO2MCdebugCuts")
    histMass = list.FindObject("Mass")
    histMass.GetXaxis().SetRangeUser(2., 5.)
    histMass.SetMarkerStyle(24)
    histMass.SetMarkerColor(kBlack)
    histMass.SetLineColor(kBlack)
    histMass.GetXaxis().SetTitle("#it{m} (Gev/#it{c}^{2})")
    histMass.GetXaxis().SetTitleSize(0.05)
    histMass.GetYaxis().SetTitle("dN / d#it{m} (Gev/#it{c}^{2})^{-1}")
    histMass.GetYaxis().SetTitleSize(0.05)
    histMass.GetXaxis().SetLabelSize(0.05)
    histMass.GetYaxis().SetLabelSize(0.05)
    
    if (mode == "bkg_only"):
        funcMass = TF1("funcMass", Func_Exp, 2, 5, 2)
        funcMass.SetNpx(1000)
        funcMass.SetParameter(0,100.)
        funcMass.SetParameter(1,1.)
        histMass.Fit(funcMass, "RL")

    if (mode == "full"):
        par_signal = [100.,3.096,7.0e-02,0.089,10.393]
        funcMass = TF1("funcMass", Func_Tot_ee, 2, 5, 7)
        funcMass.SetNpx(1000)
        funcMass.SetParameter(0,100.)
        funcMass.SetParameter(1,1.)
        funcMass.SetParameter(2,par_signal[0])
        funcMass.SetParameter(3,par_signal[1])
        funcMass.SetParName(3, "#mu_{J/#psi}")
        funcMass.SetParameter(4,par_signal[2])
        funcMass.SetParName(4, "#sigma_{J/#psi}")
        funcMass.FixParameter(5,par_signal[3])
        funcMass.FixParameter(6,par_signal[4])
        histMass.Fit(funcMass, "R")

    canvasMass = TCanvas("canvasMass", "canvasMass", 600, 600)

    gStyle.SetOptFit(1)
    histMass.Draw("EPsame")
    funcMass.Draw("same")

    canvasMass.Update() 
    input()
    canvasMass.SaveAs(inputCfg["output"]["output_plot_neme"])

def main():
    parser = argparse.ArgumentParser(description='Arguments to pass')
    parser.add_argument('cfgFileName', metavar='text', default='config.yml', help='config file name')
    parser.add_argument("--comp", help="compare data to mc", action="store_true")
    parser.add_argument("--fit_bkg_only", help="plot and fit the dilepton distribution background only", action="store_true")
    parser.add_argument("--fit_full", help="plot and fit the dilepton distribution", action="store_true")
    args = parser.parse_args()

    print('Loading task configuration: ...', end='\r')
    with open(args.cfgFileName, 'r') as ymlCfgFile:
        inputCfg = yaml.load(ymlCfgFile, yaml.FullLoader)
    print('Loading task configuration: Done!')

    if args.comp:
        comp()
    if args.fit_bkg_only:
        fit(inputCfg, "bkg_only")
    if args.fit_full:
        fit(inputCfg, "full")

main()