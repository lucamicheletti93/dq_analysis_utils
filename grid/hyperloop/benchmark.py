import matplotlib.pyplot as plt
import array as arr
import numpy as np
import os
import sys
import argparse
import ROOT
from os import path
from ROOT import TCanvas, TF1, TFile, TPaveText, TMath
from ROOT import gROOT, gBenchmark, gPad, gStyle
from ctypes import cdll
sys.path.append('../../utils/')
from plot_library import Load_Style, Draw_Ratio_Plot
from function_library import Func_Tot_ee, Func_Tot_mumu

def params():
    production = ['LHC15o_test', 'LHC18_pp_test', 'LHC18_pp_benchmark']

    # Derived data tables
    reduction_factor_fwd_TM = arr.array('d', [2347, 298, 810])
    pss_memory_fwd_TM = arr.array('d', [2.2, 2.3, 2.3]) # GB
    throughtput_fwd_TM = arr.array('d', [42.8, 23.7, 32.9]) # MB/s
    events_fwd_TM = arr.array('d', [67356, 449384, 207607]) # Number of events in 3 minutes
    procData_fwd_TM = arr.array('d', [0 ,0 ,0])

    reduction_factor_barrel_TM = arr.array('d', [837, 271, 637])
    pss_memory_barrel_TM = arr.array('d', [3.6, 3.1, 2.9]) # GB
    throughtput_barrel_TM = arr.array('d', [4.9, 5.0, 5.3]) # MB/s
    events_barrel_TM = arr.array('d', [8672, 110937, 37597]) # Number of events in 3 minutes
    procData_barrel_TM = arr.array('d', [0 ,0 ,0])

    reduction_factor_fwd_TR = arr.array('d', [1980, 294, 764])
    pss_memory_fwd_TR = arr.array('d', [2.8, 2.8, 2.8]) # GB
    throughtput_fwd_TR = arr.array('d', [25.6, 16.2, 22.9]) # MB/s
    events_fwd_TR = arr.array('d', [43877, 317666, 153007]) # Number of events in 3 minutes
    procData_fwd_TR = arr.array('d', [0 ,0 ,0])

    reduction_factor_barrel_TR = arr.array('d', [634, 256, 558])
    pss_memory_barrel_TR = arr.array('d', [3.9, 4.6, 4.2]) # GB
    throughtput_barrel_TR = arr.array('d', [3.9, 3.4, 4.2]) # MB/s
    events_barrel_TR = arr.array('d', [7266, 73050, 31691]) # Number of events in 3 minutes
    procData_barrel_TR = arr.array('d', [0 ,0 ,0])

    print("Processed data")
    for iIndex in range(0, len(production)) :
        print("----> %s" % production[iIndex])
        procData_fwd_TM[iIndex] = events_fwd_TM[iIndex]/180
        print("fwd skimming = %f" % procData_fwd_TM[iIndex])
        procData_barrel_TM[iIndex] = events_barrel_TM[iIndex]/180
        print("barrel skimming = %f" % procData_barrel_TM[iIndex])
        print("----> %s" % production[iIndex])
        procData_fwd_TR[iIndex] = events_fwd_TR[iIndex]/180
        print("fwd analysis = %f" % procData_fwd_TR[iIndex])
        procData_barrel_TR[iIndex] = events_barrel_TR[iIndex]/180
        print("barrel analysis = %f" % procData_barrel_TR[iIndex])


    figure, axis = plt.subplots(2, 2, figsize=(20, 8))

    axis[0, 0].plot(production, reduction_factor_fwd_TM, 'ro-', label = "fwd skim")
    axis[0, 0].plot(production, reduction_factor_barrel_TM, 'bo-', label = "barrel skim")
    axis[0, 0].plot(production, reduction_factor_fwd_TR, 'rs--', label = "fwd analysis")
    axis[0, 0].plot(production, reduction_factor_barrel_TR, 'bs--', label = "barrel analysis")
    axis[0, 0].set_title("Reduction factor")
    axis[0, 0].legend()

    axis[1, 0].plot(production, pss_memory_fwd_TM, 'ro-', label = "fwd skim")
    axis[1, 0].plot(production, pss_memory_barrel_TM, 'bo-', label = "barrel skim")
    axis[1, 0].plot(production, pss_memory_fwd_TR, 'rs--', label = "fwd analysis")
    axis[1, 0].plot(production, pss_memory_barrel_TR, 'bs--', label = "barrel analysis")
    axis[1, 0].set_title("PSS memory (GB)")
    axis[1, 0].legend()

    axis[0, 1].plot(production, procData_fwd_TM, 'ro-', label = "fwd skim")
    axis[0, 1].plot(production, procData_barrel_TM, 'bo-', label = "barrel skim")
    axis[0, 1].plot(production, procData_fwd_TR, 'rs--', label = "fwd analysis")
    axis[0, 1].plot(production, procData_barrel_TR, 'bs--', label = "barrel analysis")
    axis[0, 1].set_title("Events/s")
    axis[0, 1].legend()

    axis[1, 1].plot(production, throughtput_fwd_TM, 'ro-', label = "fwd skim")
    axis[1, 1].plot(production, throughtput_barrel_TM, 'bo-', label = "barrel skim")
    axis[1, 1].plot(production, throughtput_fwd_TR, 'rs--', label = "fwd analysis")
    axis[1, 1].plot(production, throughtput_barrel_TR, 'bs--', label = "barrel analysis")
    axis[1, 1].set_title("Throughtput (MB/s)")
    axis[1, 1].legend()

    plt.show()


def fit():
    fIn_ee = TFile.Open("../../o2/output/AnalysisResults_LHC18_dielectron.root")
    hlist_ee = fIn_ee.Get("analysis-same-event-pairing/output")
    list_ee = hlist_ee.FindObject("PairsBarrelSEPM_jpsiO2MCdebugCuts")
    histMass_ee = list_ee.FindObject("Mass")
    histMass_ee.GetXaxis().SetRangeUser(2, 5)
    histMass_ee.SetTitle("e^{+}e^{-} spectrum")

    #for i in range (0, 30):
        #histMass_ee.SetBinContent(histMass_ee.FindBin(2.5) + i, 0)
        #histMass_ee.SetBinError(histMass_ee.FindBin(2.5) + i, 0)

    # Input parameters for the fit to the e+e- spectrum
    par_signal_ee = [100.,3.096,7.0e-02,0.089,10.393]

    funcMass_ee = TF1("funcMass_ee", Func_Tot_ee, 2, 5, 7)
    funcMass_ee.SetNpx(1000)
    funcMass_ee.SetParameter(0,100.)
    funcMass_ee.SetParameter(1,1.)
    funcMass_ee.SetParameter(2,par_signal_ee[0])
    funcMass_ee.SetParameter(3,par_signal_ee[1])
    funcMass_ee.SetParName(3, "#mu_{J/#psi}")
    funcMass_ee.SetParameter(4,par_signal_ee[2])
    funcMass_ee.SetParName(4, "#sigma_{J/#psi}")
    funcMass_ee.FixParameter(5,par_signal_ee[3])
    funcMass_ee.FixParameter(6,par_signal_ee[4])
    histMass_ee.Fit(funcMass_ee, "R")

    fIn_mumu = TFile.Open("../../o2/output/AnalysisResults_LHC18_dimuon.root")
    hlist_mumu = fIn_mumu.Get("analysis-same-event-pairing/output")
    list_mumu = hlist_mumu.FindObject("PairsMuonSEPM_muonQualityCuts")
    histMass_mumu = list_mumu.FindObject("Mass")
    histMass_mumu.GetXaxis().SetRangeUser(2, 5)
    histMass_mumu.SetTitle("\mu^{+}\mu^{-} spectrum")

    #for i in range (0, 70):
        #histMass_mumu.SetBinContent(histMass_mumu.FindBin(2.5) + i, 0)
        #histMass_mumu.SetBinError(histMass_mumu.FindBin(2.5) + i, 0)
    
    # Input parameters for the fit to the mu+mu- spectrum
    par_signal_mumu = [100.,3.096,7.0e-02,1.089,3.393,2.097,8.694,0.01]

    funcMass_mumu = TF1("funcMass_mumu", Func_Tot_mumu, 2.3, 4.5, 12)
    funcMass_mumu.SetNpx(1000)
    funcMass_mumu.FixParameter(0, 3.82888e+06)
    funcMass_mumu.FixParameter(1, -1.92923e+03)
    funcMass_mumu.FixParameter(2, 6.02176e+04)
    funcMass_mumu.FixParameter(3, 5.96033e+04)
    funcMass_mumu.SetParameter(4, 50000.)
    funcMass_mumu.SetParameter(5, par_signal_mumu[1]) 
    funcMass_mumu.SetParName(5, "#mu_{J/#psi}")
    funcMass_mumu.SetParameter(6, par_signal_mumu[2])
    funcMass_mumu.SetParName(6, "#sigma_{J/#psi}")
    funcMass_mumu.FixParameter(7, par_signal_mumu[3])
    funcMass_mumu.FixParameter(8, par_signal_mumu[4])
    funcMass_mumu.FixParameter(9, par_signal_mumu[5])
    funcMass_mumu.FixParameter(10, par_signal_mumu[6])
    funcMass_mumu.SetParameter(11, par_signal_mumu[7])
    funcMass_mumu.SetParName(11, "#psi(2S)/J/#psi")
    histMass_mumu.Fit(funcMass_mumu, "R")

    canvas = TCanvas("canvas", "canvas", 1200, 600)
    canvas.Divide(2, 1)

    canvas.cd(1)
    gPad.SetLogy(1)
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(1)
    histMass_ee.Draw("EPsame")

    canvas.cd(2)
    gPad.SetLogy(1)
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(1)
    histMass_mumu.Draw("EPsame")
    funcMass_mumu.Draw("same")

    canvas.Update() 
    input()


def main():
    parser = argparse.ArgumentParser(description='Arguments to pass')
    parser.add_argument("--params", help="plot parameters", action="store_true")
    parser.add_argument("--fit", help="plot and fit the dilepton distribution", action="store_true")
    args = parser.parse_args()

    if args.params:
        params()
    if args.fit:
        fit()

main()