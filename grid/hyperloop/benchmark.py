import matplotlib.pyplot as plt
import array as arr
import os
import sys
import argparse
import ROOT
from os import path
from ROOT import TCanvas, TF1, TFile, TPaveText
from ROOT import gROOT, gBenchmark, gPad, gStyle
from ctypes import cdll

def params():
    production = ['LHC15o_test', 'LHC18_pp_test', 'LHC18_pp_benchmark']

    # Derived data tables
    reduction_factor_fwd = arr.array('d', [2333, 299, 812])
    pss_memory_fwd = arr.array('d', [2.2, 2.3, 2.3]) # GB
    timing_fwd = arr.array('d', [2.62, 2.62, 2.6]) # min
    throughtput_fwd = arr.array('d', [34.5, 17.5, 32.2]) # MB/s
    procData_fwd = arr.array('d', [0 ,0 ,0])

    reduction_factor_barrel = arr.array('d', [805, 272, 621])
    pss_memory_barrel = arr.array('d', [3.3, 3.9, 3.6]) # GB
    timing_barrel = arr.array('d', [2.6, 2.96, 2.6]) # min
    throughtput_barrel = arr.array('d', [4.2, 3.9, 4.6]) # MB/s
    procData_barrel = arr.array('d', [0 ,0 ,0])

    print("Processed data")
    for iIndex in range(0, len(production)) :
        print("----> %s" % production[iIndex])
        procData_fwd[iIndex] = 3. *  throughtput_fwd[iIndex]
        print("fwd = %f" % procData_fwd[iIndex])
        procData_barrel[iIndex] = 3. *  throughtput_barrel[iIndex]
        print("barrel = %f" % procData_barrel[iIndex])


    figure, axis = plt.subplots(2, 2, figsize=(20, 8))

    axis[0, 0].plot(production, reduction_factor_fwd, 'r', marker = "o", label = "fwd")
    axis[0, 0].plot(production, reduction_factor_barrel, 'b', marker = "o", label = "barrel")
    axis[0, 0].set_title("Reduction factor")
    axis[0, 0].legend()

    axis[1, 0].plot(production, pss_memory_fwd, 'r', marker = "o", label = "fwd")
    axis[1, 0].plot(production, pss_memory_barrel, 'b', marker = "o", label = "barrel")
    axis[1, 0].set_title("PSS memory (GB)")
    axis[1, 0].legend()

    axis[0, 1].plot(production, procData_fwd, 'r', marker = "o", label = "fwd")
    axis[0, 1].plot(production, procData_barrel, 'b', marker = "o", label = "barrel")
    axis[0, 1].set_title("Processed data in 3 min (MB)")
    axis[0, 1].legend()

    axis[1, 1].plot(production, throughtput_fwd, 'r', marker = "o", label = "fwd")
    axis[1, 1].plot(production, throughtput_barrel, 'b', marker = "o", label = "barrel")
    axis[1, 1].set_title("Throughtput")
    axis[1, 1].legend()

    plt.show()

def fit():
    #lib = cdll.LoadLibrary('./../../../dq_fit_library/DQFitter_cxx.so')

    fIn_ee = TFile.Open("AnalysisResults_LHC18_dielectron.root")
    hlist_ee = fIn_ee.Get("analysis-same-event-pairing/output")
    list_ee = hlist_ee.FindObject("PairsBarrelSEPM_jpsiO2MCdebugCuts")
    histMass_ee = list_ee.FindObject("Mass")
    histMass_ee.GetXaxis().SetRangeUser(2, 5)
    histMass_ee.SetTitle("e^{+}e^{-} spectrum")

    #for i in range (0, 30):
        #histMass_ee.SetBinContent(histMass_ee.FindBin(2.5) + i, 0)
        #histMass_ee.SetBinError(histMass_ee.FindBin(2.5) + i, 0)

    funcMass_ee = TF1("funcMass_ee", "gaus(0)+pol2(3)", 2, 5)
    funcMass_ee.SetParameter(1, 3.1)
    funcMass_ee.SetParameter(2, 0.10)
    funcMass_ee.SetParameter(3, 1.1e4)
    funcMass_ee.SetParameter(4, -3.e3)
    funcMass_ee.SetParameter(5, 3.1e2)
    histMass_ee.Fit(funcMass_ee, "R")

    fIn_mumu = TFile.Open("AnalysisResults_LHC18_dimuon.root")
    hlist_mumu = fIn_mumu.Get("analysis-same-event-pairing/output")
    list_mumu = hlist_mumu.FindObject("PairsMuonSEPM_muonQualityCuts")
    histMass_mumu = list_mumu.FindObject("Mass")
    histMass_mumu.GetXaxis().SetRangeUser(2, 5)
    histMass_mumu.SetTitle("\mu^{+}\mu^{-} spectrum")

    #for i in range (0, 70):
        #histMass_mumu.SetBinContent(histMass_mumu.FindBin(2.5) + i, 0)
        #histMass_mumu.SetBinError(histMass_mumu.FindBin(2.5) + i, 0)
    
    funcMass_mumu = TF1("funcMass_mumu", "gaus(0)+pol4(3)", 2, 5)
    funcMass_mumu.SetParameter(1, 3.1)
    funcMass_mumu.SetParameter(2, 0.07)
    funcMass_mumu.SetParameter(3, 7.1e4)
    funcMass_mumu.SetParameter(4, 1.1e5)
    funcMass_mumu.SetParameter(5, -4.3e4)
    funcMass_mumu.SetParameter(6, 7.7e3)
    funcMass_mumu.SetParameter(7, -5.0e2)
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