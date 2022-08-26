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
from ROOT import TCanvas, TF1, TFile, TPaveText, TMath, TLegend, TLine
from ROOT import gROOT, gBenchmark, gPad, gStyle, kBlack, kRed, kGreen, kBlue, kGray, kDashed
from ctypes import cdll
sys.path.append('../utils/')
from plot_library import Load_Style, SetLegend, Draw_Ratio_Plot
from function_library import Func_Exp, Func_Tot_ee

###
def trigger(inputCfg):
    fIn = TFile.Open(inputCfg["input"]["input_trigger_file_name"])
    histStats = fIn.Get("d-q-filter-p-p-task/Statistics")

    canvasStats = TCanvas("canvasStats", "canvasStats", 1000, 700)
    gPad.SetLogy(1)
    histStats.Draw("Hsame")
    canvasStats.Update() 
    input()

###
def plot(inputCfg):
    Load_Style()

    fIn = TFile.Open(inputCfg["input"]["input_file_name"])
    hlistTM = fIn.Get(inputCfg["input"]["table_maker"])

    for cut in inputCfg["input"]["table_maker_dir"]:
        listTM = hlistTM.FindObject(cut)
        for var in inputCfg["input"]["table_maker_obj"]:
            hist = listTM.FindObject(var)
            print(var)
            canvas = TCanvas("canvas", "canvas", 600, 600)
            if "TPC" in var:
                hist.Draw("COLZ")
            elif "TOF" in var:
                hist.Draw("COLZ")
            else:
                hist.SetMarkerStyle(20)
                hist.SetMarkerSize(0.4)
                hist.SetMarkerColor(kBlack)
                hist.SetLineColor(kBlack)
                gPad.SetLogy(1)
                hist.Draw("EPsame")

            canvas.Update()
            canvas.SaveAs("{}/{}_{}.pdf".format(inputCfg["output"]["output_fig_name"], cut, var))

    hlistTR = fIn.Get(inputCfg["input"]["table_reader"])
    for cut in inputCfg["input"]["table_reader_dir"]:
        listTR = hlistTR.FindObject(cut)
        for var in inputCfg["input"]["table_reader_obj"]:
            hist = listTR.FindObject(var)
            canvas = TCanvas("canvas", "canvas", 600, 600)
            hist.SetMarkerStyle(24)
            hist.SetMarkerSize(0.8)
            hist.SetMarkerColor(kBlack)
            hist.SetLineColor(kBlack)
            hist.GetXaxis().SetRangeUser(0, 5)
            hist.GetXaxis().SetTitleSize(0.05)
            if "Mass" in var:
                hist.GetXaxis().SetTitle("#it{m} (Gev/#it{c}^{2})")
                hist.GetYaxis().SetTitle("dN / d#it{m} (GeV/#it{c}^{2})^{-1}")
            hist.GetYaxis().SetTitleSize(0.05)
            hist.GetXaxis().SetLabelSize(0.05)
            hist.GetYaxis().SetLabelSize(0.05)
            gPad.SetLogy(1)
            hist.Draw("EPsame")
            canvas.Update()
            canvas.SaveAs("{}/{}_{}.pdf".format(inputCfg["output"]["output_fig_name"], cut, var))

    input()

###
def comparison(inputCfg):
    fIn = TFile.Open(inputCfg["input"]["input_file_name"])
    hlistTM = fIn.Get(inputCfg["input"]["table_maker"])
    hist_dedx = []
    hist_Pt = []
    listOfCuts = []

    for cut in inputCfg["input"]["table_maker_dir"]:
        listTM = hlistTM.FindObject(cut)
        listOfCuts.append(cut)
        for var in inputCfg["input"]["table_maker_obj"]:
            hist = listTM.FindObject(var)
            if "TPC" in var:
                hist.GetXaxis().SetRangeUser(1, 10)
                hist_dedx.append(hist.ProjectionY("Proj_{}_{}".format(cut, var)))
            if "Pt" in var:
                hist_Pt.append(hist)

    colors = [kBlack, kRed+1, kBlue+1, kGreen+1]

    canvasDeDxNoCuts = TCanvas("canvasDeDxNoCuts", "", 600, 600)
    gPad.SetLogy(1)
    gStyle.SetOptStat(0)
    hist_dedx[0].SetTitle(" ")
    hist_dedx[0].SetLineColor(colors[0])
    hist_dedx[0].Draw("H")
    canvasDeDxNoCuts.Update()
    
    legend = TLegend(0.35, 0.7, 0.75, 0.85)
    SetLegend(legend)

    canvasDeDxCuts = TCanvas("canvasDeDxCuts", "", 600, 600)
    gPad.SetLogy(1)
    gStyle.SetOptStat(0)
    hist_dedx[1].SetTitle(" ")
    hist_dedx[1].SetLineColor(colors[1])
    hist_dedx[1].GetXaxis().SetRangeUser(60, 120)
    hist_dedx[1].Draw("H")
    legend.AddEntry(hist_dedx[1], listOfCuts[1])
    for i in range(2, len(hist_dedx)):
        hist_dedx[i].SetLineColor(colors[i])
        hist_dedx[i].Draw("Hsame")
        legend.AddEntry(hist_dedx[i], listOfCuts[i])
    legend.Draw("same")
    canvasDeDxCuts.Update()

    canvasPtCuts = TCanvas("canvasPtCuts", "", 600, 600)
    gPad.SetLogy(1)
    gStyle.SetOptStat(0)
    hist_Pt[1].SetTitle(" ")
    hist_Pt[1].SetLineColor(colors[1])
    hist_Pt[1].Draw("H")
    for i in range(2, len(hist_Pt)):
        hist_Pt[i].SetLineColor(colors[i])
        hist_Pt[i].Draw("Hsame")
    legend.Draw("same")
    canvasPtCuts.Update()
    input()

    canvasDeDxNoCuts.SaveAs("{}/comparison_TPCdedx_nocuts.pdf".format(inputCfg["output"]["output_fig_name"], cut, var))
    canvasDeDxCuts.SaveAs("{}/comparison_TPCdedx_cuts.pdf".format(inputCfg["output"]["output_fig_name"], cut, var))
    canvasPtCuts.SaveAs("{}/comparison_Pt_cuts.pdf".format(inputCfg["output"]["output_fig_name"], cut, var))

###
def fit(inputCfg, mode):
    Load_Style()
    fIn = TFile.Open(inputCfg["input"]["input_file_name"])
    hlist = fIn.Get("analysis-same-event-pairing/output")
    #list = hlist.FindObject("PairsBarrelSEPM_jpsiO2MCdebugCuts")
    list = hlist.FindObject("PairsMuonSEPM_mchTrack")
    histMass = list.FindObject("Mass")
    histMass.GetXaxis().SetRangeUser(0., 5.)
    histMass.SetMarkerStyle(24)
    histMass.SetMarkerColor(kBlack)
    histMass.SetLineColor(kBlack)
    histMass.GetXaxis().SetTitle("#it{m} (Gev/#it{c}^{2})")
    histMass.GetXaxis().SetTitleSize(0.05)
    histMass.GetYaxis().SetTitle("dN / d#it{m} (GeV/#it{c}^{2})^{-1}")
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
    gPad.SetLogy(1)
    gStyle.SetOptFit(1)
    histMass.Draw("EPsame")
    funcMass.Draw("same")

    canvasMass.Update() 
    input()
    canvasMass.SaveAs(inputCfg["output"]["output_plot_neme"])

###
def eval_eff(inputCfg):
    Load_Style()

    hist_gen_tm = []
    hist_rec_tm = []
    hist_eff_tm = []

    hist_gen_tr = []
    hist_rec_tr = []
    hist_eff_tr = []

    fInTM = TFile.Open(inputCfg["input"]["input_table_maker_file_name"])
    hlistTM = fInTM.Get(inputCfg["input"]["table_maker"])

    fInTR = TFile.Open(inputCfg["input"]["input_table_reader_file_name"])
    fInTR.ls()
    hlistTR = fInTR.Get(inputCfg["input"]["table_reader"])
    hlistTR.ls()

    # Loop over generated
    for cut in inputCfg["input"]["table_maker_gen_dir"]:
        listTM = hlistTM.FindObject(cut)
        for var in inputCfg["input"]["table_maker_obj"]:
            hist = listTM.FindObject("{}MC".format(var))
            hist.Rebin(5)
            hist_gen_tm.append(hist)
    
    for cut in inputCfg["input"]["table_reader_gen_dir"]:
        listTR = hlistTR.FindObject(cut)
        for var in inputCfg["input"]["table_reader_obj"]:
            hist = listTR.FindObject("{}MC".format(var))
            hist.Rebin(5)
            hist_gen_tr.append(hist)

    # Loop over reconstructed
    for cut in inputCfg["input"]["table_maker_rec_dir"]:
        listTM = hlistTM.FindObject(cut)
        for var in inputCfg["input"]["table_maker_obj"]:
            hist = listTM.FindObject("{}".format(var))
            hist.Rebin(5)
            hist_rec_tm.append(hist)

    for cut in inputCfg["input"]["table_reader_rec_dir"]:
        listTR = hlistTR.FindObject(cut)
        for var in inputCfg["input"]["table_reader_obj"]:
            hist = listTR.FindObject("{}".format(var))
            hist.Rebin(5)
            hist_rec_tr.append(hist)
    
    var_tm = inputCfg["input"]["table_maker_obj"]

    for i in range(0, len(var_tm)):
        hist_tmp_tm = hist_rec_tm[i].Clone("hist_tmp_tm")
        hist_tmp_tm.Divide(hist_gen_tm[i])
        hist_eff_tm.append(hist_tmp_tm)

        # Rename the histograms
        hist_gen_tm[i].SetName("hist_gen_tm_Pt".format(var_tm[i]))
        hist_rec_tm[i].SetName("hist_rec_tm_Pt".format(var_tm[i]))
        hist_eff_tm[i].SetName("hist_eff_tm_Pt".format(var_tm[i]))

    var_tr = inputCfg["input"]["table_maker_obj"]

    for i in range(0, len(var_tr)):
        hist_tmp_tr = hist_rec_tr[i].Clone("hist_tmp_tr")
        hist_tmp_tr.Divide(hist_gen_tr[i])
        hist_eff_tr.append(hist_tmp_tr)

        # Rename the histograms
        hist_gen_tr[i].SetName("hist_gen_tr_Pt".format(var_tr[i]))
        hist_rec_tr[i].SetName("hist_rec_tr_Pt".format(var_tr[i]))
        hist_eff_tr[i].SetName("hist_eff_tr_Pt".format(var_tr[i]))

    fOut = TFile.Open("%s/%s" % (inputCfg["output"]["output_dir_name"], inputCfg["output"]["output_file_name"]), "RECREATE")
    for i in range(0, len(hist_eff_tm)):
        hist_gen_tm[i].Write("hist_gen_tm_Pt".format(var_tm[i]))
        hist_rec_tm[i].Write("hist_rec_tm_Pt".format(var_tm[i]))
        hist_eff_tm[i].Write("hist_eff_tm_Pt".format(var_tm[i]))

    for i in range(0, len(hist_eff_tr)):
        hist_gen_tr[i].Write("hist_gen_tr_Pt".format(var_tr[i]))
        hist_rec_tr[i].Write("hist_rec_tr_Pt".format(var_tr[i]))
        hist_eff_tr[i].Write("hist_eff_tr_Pt".format(var_tr[i]))
    fOut.Close()

###
def comp_eff():
    Load_Style()

    fIn1 = TFile.Open("output/MC/LHC21i3d2.root") # Prompt charmonia fwd
    hist_eff_tm1 = fIn1.Get("hist_eff_tm_Pt")
    hist_eff_tm1.SetMarkerStyle(20)
    hist_eff_tm1.SetMarkerSize(0.8)
    hist_eff_tm1.SetMarkerColor(kRed)
    hist_eff_tm1.SetLineColor(kRed)
    hist_eff_tm1.GetXaxis().SetRangeUser(0, 20)
    hist_eff_tm1.GetYaxis().SetRangeUser(0.01, 2)
    hist_eff_tm1.GetXaxis().SetTitleSize(0.05)
    hist_eff_tm1.GetYaxis().SetTitleSize(0.05)
    hist_eff_tm1.GetXaxis().SetLabelSize(0.05)
    hist_eff_tm1.GetYaxis().SetLabelSize(0.05)
    hist_eff_tm1.GetXaxis().SetTitle("#it{p}_{T} (GeV/c)")
    hist_eff_tm1.GetYaxis().SetTitle("A #times #varepsilon")

    hist_eff_tr1 = fIn1.Get("hist_eff_tr_Pt")
    hist_eff_tr1.SetMarkerStyle(20)
    hist_eff_tr1.SetMarkerSize(0.8)
    hist_eff_tr1.SetMarkerColor(kRed)
    hist_eff_tr1.SetLineColor(kRed)
    hist_eff_tr1.GetXaxis().SetRangeUser(0, 20)
    hist_eff_tr1.GetYaxis().SetRangeUser(0.01, 100)
    hist_eff_tr1.GetXaxis().SetTitleSize(0.05)
    hist_eff_tr1.GetYaxis().SetTitleSize(0.05)
    hist_eff_tr1.GetXaxis().SetLabelSize(0.05)
    hist_eff_tr1.GetYaxis().SetLabelSize(0.05)
    hist_eff_tr1.GetXaxis().SetTitle("#it{p}_{T} (GeV/c)")
    hist_eff_tr1.GetYaxis().SetTitle("A #times #varepsilon")

    fIn2 = TFile.Open("output/MC/LHC21i3g2.root") # Non-Prompt charmonia fwd
    hist_eff_tm2 = fIn2.Get("hist_eff_tm_Pt")
    hist_eff_tm2.SetMarkerStyle(20)
    hist_eff_tm2.SetMarkerSize(0.8)
    hist_eff_tm2.SetMarkerColor(kBlue)
    hist_eff_tm2.SetLineColor(kBlue)
    hist_eff_tm2.GetXaxis().SetRangeUser(0, 20)
    hist_eff_tm2.GetYaxis().SetRangeUser(0.01, 2)
    hist_eff_tm2.GetXaxis().SetTitleSize(0.05)
    hist_eff_tm2.GetYaxis().SetTitleSize(0.05)
    hist_eff_tm2.GetXaxis().SetLabelSize(0.05)
    hist_eff_tm2.GetYaxis().SetLabelSize(0.05)

    hist_eff_tr2 = fIn2.Get("hist_eff_tr_Pt")
    hist_eff_tr2.SetMarkerStyle(20)
    hist_eff_tr2.SetMarkerSize(0.8)
    hist_eff_tr2.SetMarkerColor(kBlue)
    hist_eff_tr2.SetLineColor(kBlue)
    hist_eff_tr2.GetXaxis().SetRangeUser(0, 20)
    hist_eff_tr2.GetYaxis().SetRangeUser(0.01, 100)
    hist_eff_tr2.GetXaxis().SetTitleSize(0.05)
    hist_eff_tr2.GetYaxis().SetTitleSize(0.05)
    hist_eff_tr2.GetXaxis().SetLabelSize(0.05)
    hist_eff_tr2.GetYaxis().SetLabelSize(0.05)

    lineUnity = TLine(0, 1, 20, 1)
    lineUnity.SetLineStyle(kDashed)
    lineUnity.SetLineColor(kGray)

    legend = TLegend(0.2, 0.75, 0.3, 0.85)
    SetLegend(legend)
    legend.AddEntry(hist_eff_tm1, "prompt charmonia", "P")
    legend.AddEntry(hist_eff_tm2, "non-prompt charmonia", "P")

    canvas_tm = TCanvas("canvas_tm", "canvas_tm", 800, 600)
    gStyle.SetOptStat(0)
    gPad.SetLogy(1)
    hist_eff_tm1.Draw("EP")
    hist_eff_tm2.Draw("EPsame")
    lineUnity.Draw("same")
    legend.Draw("same")

    canvas_tm.Update()

    canvas_tr = TCanvas("canvas_tr", "canvas_tr", 800, 600)
    gStyle.SetOptStat(0)
    gPad.SetLogy(1)
    hist_eff_tr1.Draw("EP")
    hist_eff_tr2.Draw("EPsame")
    lineUnity.Draw("same")
    legend.Draw("same")

    canvas_tr.Update()
    input()

    canvas_tm.SaveAs("eff_comparison_tm.pdf")
    canvas_tr.SaveAs("eff_comparison_tr.pdf")

###
def ambi_tracks(inputCfg):
    #Load_Style()
    file_list = ["AnalysisResults_LHC21i3d2_ambiguous.root", "AnalysisResults_LHC21i3g2_ambiguous.root", "AnalysisResults_LHC21k6_ambiguous.root"]
    #file_list = ["AnalysisResults_LHC21i3d2_ambiguous.root", "AnalysisResults_LHC21i3g2_ambiguous.root"]
    color_list = [ROOT.kRed+1, ROOT.kBlue+1, ROOT.kGreen+1]
    #color_list = [ROOT.kRed+1, ROOT.kBlue+1]
    var_list = ["XvtxPos", "YvtxPos", "ZvtxPos", "TracksDCAX", "TracksDCAY", "NumberOfContributors", "CollisionsSize", "BcSize", "Chi2MatchMCHMID", "Chi2MatchMCHMFT", "RMSZvtx"]
    var_label = ["X_{vtx}^{reco} (cm)", "Y_{vtx}^{reco} (cm)", "Z_{vtx}^{reco} (cm)", "DCA_{X} (cm)", "DCA_{Y} (cm)", "number of contributors", "number of collisions", "number of BCs", "#chi^{2} MCH-MID", "#chi^{2} MCH-MFT", "RMS (Z_{vtx}^{reco})"]
    hist_list_prompt = []
    hist_list_nonprompt = []
    hist_list_gp_mc = []

    for i in range(0, len(file_list)):
        fIn = TFile.Open("/Users/lucamicheletti/GITHUB/dq_analysis_utils/o2/output/{}".format(file_list[i]))
        for j in range(0, len(var_list)):
            hist = fIn.Get("table-maker-m-c/{}".format(var_list[j]))
            if not "CollisionsSize" == var_list[j]:
                hist.Rebin(2)
            if "Chi2MatchMCHMID" == var_list[j]:
                hist.GetXaxis().SetRangeUser(-2, 20)
            if "LHC21i3d2" in fIn.GetName():
                hist_list_prompt.append(hist)
                hist_list_prompt[j].SetDirectory(0)
                hist_list_prompt[j].SetLineColor(color_list[i])
                hist_list_prompt[j].SetLineWidth(2)
                hist_list_prompt[j].Scale(1. / hist_list_prompt[j].Integral())
            if "LHC21i3g2" in fIn.GetName():
                hist_list_nonprompt.append(hist)
                hist_list_nonprompt[j].SetDirectory(0)
                hist_list_nonprompt[j].SetLineColor(color_list[i])
                hist_list_nonprompt[j].SetLineWidth(2)
                hist_list_nonprompt[j].Scale(1. / hist_list_nonprompt[j].Integral())
            if "LHC21k6" in fIn.GetName():
                hist_list_gp_mc.append(hist)
                hist_list_gp_mc[j].SetDirectory(0)
                hist_list_gp_mc[j].SetLineColor(color_list[i])
                hist_list_gp_mc[j].SetLineWidth(2)
                hist_list_gp_mc[j].Scale(1. / hist_list_gp_mc[j].Integral())

    legend = TLegend(0.4, 0.7, 0.7, 0.85)
    SetLegend(legend)
    legend.AddEntry(hist_list_prompt[0], "LHC21i3d2 (prompt J/#psi fwd)", "L")
    legend.AddEntry(hist_list_nonprompt[0], "LHC21i3g2 (non-prompt J/#psi fwd)", "L")
    legend.AddEntry(hist_list_gp_mc[0], "LHC21k6 (general purpose MC)", "L")

    for i in range(0, len(var_list)):
        canvas = TCanvas("compt_{}".format(var_list[i]), "", 600, 600)
        gPad.SetLogy()
        gStyle.SetOptStat(0)
        hist_list_prompt[i].GetYaxis().SetRangeUser(1e-5, 1e2)
        hist_list_prompt[i].GetXaxis().SetTitle(var_label[i])
        hist_list_prompt[i].Draw("H")
        hist_list_nonprompt[i].Draw("Hsame")
        print("{} - Prompt = {}, Non-Prompt = {}".format(var_list[i], hist_list_prompt[i].GetMean(), hist_list_nonprompt[i]))
        hist_list_gp_mc[i].Draw("Hsame")
        legend.Draw("same")
        canvas.Update()
        canvas.SaveAs("compt_{}.pdf".format(var_list[i]))

    input()
    

### ### ###
def main():
    parser = argparse.ArgumentParser(description='Arguments to pass')
    parser.add_argument('cfgFileName', metavar='text', default='config.yml', help='config file name')
    parser.add_argument("--trigger", help="plot the trigger statistics", action="store_true")
    parser.add_argument("--fit_bkg_only", help="plot and fit the dilepton distribution background only", action="store_true")
    parser.add_argument("--fit_full", help="plot and fit the dilepton distribution", action="store_true")
    parser.add_argument("--plot", help="plot the dilepton distribution", action="store_true")
    parser.add_argument("--comparison", help="comparison of the dilepton distribution", action="store_true")
    parser.add_argument("--eval_eff", help="evaluate efficiency", action="store_true")
    parser.add_argument("--comp_eff", help="compare efficiency", action="store_true")
    parser.add_argument("--ambi_tracks", help="Study ambiguous tracks", action="store_true")
    args = parser.parse_args()

    print('Loading task configuration: ...', end='\r')
    with open(args.cfgFileName, 'r') as ymlCfgFile:
        inputCfg = yaml.load(ymlCfgFile, yaml.FullLoader)
    print('Loading task configuration: Done!')

    if args.trigger:
        trigger(inputCfg)
    if args.fit_bkg_only:
        fit(inputCfg, "bkg_only")
    if args.fit_full:
        fit(inputCfg, "full")
    if args.plot:
        plot(inputCfg)
    if args.comparison:
        comparison(inputCfg)
    if args.eval_eff:
        eval_eff(inputCfg)
    if args.comp_eff:
        comp_eff()
    if args.ambi_tracks:
        ambi_tracks(inputCfg)

main()