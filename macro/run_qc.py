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

    fOut = TFile.Open("%s/%s" % (inputCfg["output"]["output_dir_name"], inputCfg["output"]["output_file_name"]), "RECREATE")
    fInTM = TFile.Open(inputCfg["input"]["input_table_maker_file_name"])
    fInTM.ls()
    fInTR = TFile.Open(inputCfg["input"]["input_table_reader_file_name"])
    fInTR.ls()

    # Table Maker
    hlistTM = fInTM.Get(inputCfg["input"]["table_maker"])
    for cut in inputCfg["input"]["table_maker_dir"]:
        print("---------->", cut)
        listTM = hlistTM.FindObject(cut)
        for var in inputCfg["input"]["table_maker_obj"]:
            print("---------->", var)
            hist = listTM.FindObject(var)
            hist.SetDirectory(0)
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

    # Table Reader
    pt_min = inputCfg["input"]["table_reader_pt_min"]
    pt_max = inputCfg["input"]["table_reader_pt_max"]
    rap_min = inputCfg["input"]["table_reader_rap_min"]
    rap_max = inputCfg["input"]["table_reader_rap_max"]
    reso_min = inputCfg["input"]["table_reader_reso_min"]
    reso_max = inputCfg["input"]["table_reader_reso_max"]
    hlistTR = fInTR.Get(inputCfg["input"]["table_reader"])
    for cut in inputCfg["input"]["table_reader_dir"]:
        print("---------->", cut)
        listTR = hlistTR.FindObject(cut)
        for var in inputCfg["input"]["table_reader_obj"]:
            print("---------->", var)
            hist = listTR.FindObject(var)
            hist.SetDirectory(0)
            canvas = TCanvas("canvas", "canvas", 600, 600)
            hist.SetMarkerStyle(20)
            hist.SetMarkerSize(0.5)
            hist.SetMarkerColor(kBlack)
            hist.SetLineColor(kBlack)
            hist.GetXaxis().SetRangeUser(0, 5)
            hist.GetXaxis().SetTitleSize(0.05)
            #if "Mass" in var:
                #hist.GetXaxis().SetRangeUser(2, 5)
                #hist.GetXaxis().SetTitle("#it{m} (Gev/#it{c}^{2})")
                #hist.GetYaxis().SetTitle("dN / d#it{m} (GeV/#it{c}^{2})^{-1}")
                #print("Entering in the mass plot")
                #fOut.cd()
                #hist.Write("Mass_{}".format(cut))
            hist.GetYaxis().SetTitleSize(0.05)
            hist.GetXaxis().SetLabelSize(0.05)
            hist.GetYaxis().SetLabelSize(0.05)
            gPad.SetLogy(1)

            #if not var == "Mass_Pt":
                #hist.Draw("EPsame")
            #else:
                #hist.Draw("COLZ")
                # Project histogram
                #for iPt in range(0, len(pt_min)):
                    #pt_bin_min = hist.GetYaxis().FindBin(pt_min[iPt])
                    #pt_bin_max = hist.GetYaxis().FindBin(pt_max[iPt])
                    #histProj = hist.ProjectionX("{}_{}_Proj_{}_Pt_{}".format(cut, var, pt_min[iPt], pt_max[iPt]), pt_bin_min, pt_bin_max)
                    #canvasProj = TCanvas("canvasProj", "canvasProj", 600, 600)
                    #histProj.Draw("EP")
                    #canvasProj.SaveAs("{}/{}_{}_Proj_{}_Pt_{}.pdf".format(inputCfg["output"]["output_fig_name"], cut, var, pt_min[iPt], pt_max[iPt]))
                    #fOut.cd()
                    #histProj.Write("{}_{}_Proj_{}_Pt_{}".format(cut, var, pt_min[iPt], pt_max[iPt]))

            if var == "Mass_Pt":
                hist.Draw("COLZ")
                # Project histogram
                for iPt in range(0, len(pt_min)):
                    pt_bin_min = hist.GetYaxis().FindBin(pt_min[iPt])
                    pt_bin_max = hist.GetYaxis().FindBin(pt_max[iPt])
                    histProj = hist.ProjectionX("{}_{}_Proj_{}_Pt_{}".format(cut, var, pt_min[iPt], pt_max[iPt]), pt_bin_min, pt_bin_max)
                    canvasProj = TCanvas("canvasProj", "canvasProj", 600, 600)
                    histProj.Draw("EP")
                    canvasProj.SaveAs("{}/{}_{}_Proj_{}_Pt_{}.pdf".format(inputCfg["output"]["output_fig_name"], cut, var, pt_min[iPt], pt_max[iPt]))
                    fOut.cd()
                    histProj.Write("{}_{}_Proj_{}_Pt_{}".format(cut, var, pt_min[iPt], pt_max[iPt]))
            elif var == "Mass_Rapidity":
                hist.Draw("COLZ")
                # Project histogram
                for iRap in range(0, len(rap_min)):
                    rap_bin_min = hist.GetYaxis().FindBin(rap_min[iRap])
                    rap_bin_max = hist.GetYaxis().FindBin(rap_max[iRap])
                    histProj = hist.ProjectionX("{}_{}_Proj_{}_Y_{}".format(cut, var, rap_min[iRap], rap_max[iRap]), rap_bin_min, rap_bin_max)
                    canvasProj = TCanvas("canvasProj", "canvasProj", 600, 600)
                    histProj.Draw("EP")
                    canvasProj.SaveAs("{}/{}_{}_Proj_{}_Y_{}.pdf".format(inputCfg["output"]["output_fig_name"], cut, var, rap_min[iRap], rap_max[iRap]))
                    fOut.cd()
                    histProj.Write("{}_{}_Proj_{}_Y_{}".format(cut, var, rap_min[iRap], rap_max[iRap]))
            elif var == "Mass_DeltaPtotTracks":
                    hist.Draw("COLZ")
                    # Project histogram
                    for iReso in range(0, len(reso_min)):
                        reso_bin_min_1 = hist.GetYaxis().FindBin(+reso_min[iReso])
                        reso_bin_max_1 = hist.GetYaxis().FindBin(+reso_max[iReso])
                        reso_bin_min_2 = hist.GetYaxis().FindBin(-reso_max[iReso])
                        reso_bin_max_2 = hist.GetYaxis().FindBin(-reso_min[iReso])
                        histProj1 = hist.ProjectionX("{}_{}_Proj_{}_Reso_{}_1".format(cut, var, reso_min[iReso], reso_max[iReso]), reso_bin_min_1, reso_bin_max_1)
                        histProj2 = hist.ProjectionX("{}_{}_Proj_{}_Reso_{}_2".format(cut, var, reso_min[iReso], reso_max[iReso]), reso_bin_min_2, reso_bin_max_2)
                        histProj = histProj1.Clone("{}_{}_Proj_{}_Reso_{}".format(cut, var, reso_min[iReso], reso_max[iReso]))
                        histProj.Add(histProj2)
                        fOut.cd()
                        histProj1.Write("{}_{}_Proj_{}_Reso_{}_1".format(cut, var, reso_min[iReso], reso_max[iReso]))
                        histProj2.Write("{}_{}_Proj_{}_Reso_{}_2".format(cut, var, reso_min[iReso], reso_max[iReso]))
                        histProj.Write("{}_{}_Proj_{}_Reso_{}".format(cut, var, reso_min[iReso], reso_max[iReso]))
            else:
                hist.Draw("EPsame")
                
            canvas.Update()
            canvas.SaveAs("{}/{}_{}.pdf".format(inputCfg["output"]["output_fig_name"], cut, var))
            # Save the invariant mass spectra for fitting
            if "Mass" in var:
                print("Entering in the mass plot")
                fOut.cd()
                hist.Write("{}_{}".format(var, cut))

    input()
    fOut.Close()

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
        for var in inputCfg["input"]["table_reader_gen_obj"]:
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
        for var in inputCfg["input"]["table_reader_gen_obj"]:
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

    fOut = TFile.Open("%s/%s" % (inputCfg["output"]["output_dir_name"], inputCfg["output"]["output_file_name_acceff"]), "RECREATE")
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
    
def bkg_subtr():
    fIn = TFile.Open("output/Data/LHC22m_apass1_trigger_electrons.root")
    histSEPM = fIn.Get("Mass_PairsBarrelSEPM_jpsiO2MCdebugCuts")
    histSEPM.Rebin(2)
    histSEPP = fIn.Get("Mass_PairsBarrelSEPP_jpsiO2MCdebugCuts")
    histSEPP.Rebin(2)
    histSEMM = fIn.Get("Mass_PairsBarrelSEMM_jpsiO2MCdebugCuts")
    histSEMM.Rebin(2)

    #minBin = histSEPP.GetXaxis().FindBin(2)
    #maxBin = histSEPP.GetXaxis().FindBin(5)

    #histBkg = ROOT.TH1D("histBkg", "", maxBin - minBin, 2, 5)
    histBkg = ROOT.TH1D("histBkg", "", histSEPM.GetNbinsX(), 0, 5)
    histBkg.SetMarkerColor(kBlue)
    histBkg.SetLineColor(kBlue)
    #histSig = ROOT.TH1D("histSig", "", maxBin - minBin, 2, 5)
    histSig = ROOT.TH1D("histSig", "", histSEPM.GetNbinsX(), 0, 5)
    histSig.SetMarkerColor(kRed)
    histSig.SetLineColor(kRed)

    #print(minBin, maxBin)

    #for i in range(minBin, maxBin):
        #histBkg.SetBinContent(i-minBin, 2 * TMath.Sqrt(histSEPP.GetBinContent(i) * histSEMM.GetBinContent(i)))
        #histSig.SetBinContent(i-minBin, histSEPM.GetBinContent(i) - histBkg.GetBinContent(i-minBin))

    for i in range(0, histSEPM.GetNbinsX()):
        histBkg.SetBinContent(i+1, 2 * TMath.Sqrt(histSEPP.GetBinContent(i+1) * histSEMM.GetBinContent(i+1)))
        histSig.SetBinContent(i+1, histSEPM.GetBinContent(i+1) - histBkg.GetBinContent(i+1))

    canvas = TCanvas("canvas", "canvas", 600, 600)
    gPad.SetLogy(1)
    histSEPM.GetYaxis().SetRangeUser(10, 1e8)
    histSEPM.Draw("EP")
    histBkg.Draw("EPsame")
    histSig.Draw("EPsame")
    canvas.Update()
    input()

###
def qa(inputCfg):
    Load_Style()

    #//prods = ["LHC22m_apass1_bis", "LHC22f_apass1_bis", "LHC22o_apass1_bis"]
    #//prods = ["LHC22m_apass1_tris", "LHC22f_apass2", "LHC22o_apass1_tris", "LHC22s_apass1"]
    #//prods = ["LHC22f_apass2", "LHC22o_apass1_tris", "LHC22s_apass1", "LHC22s_apass3"]
    #//prodNames = ["LHC22f_apass2", "LHC22o_apass1", "LHC22s_apass1", "LHC22s_apass3"]
    prods = ["LHC22p_apass1", "LHC22q_apass1", "LHC22r_apass1"]
    prodNames = ["LHC22p_apass1", "LHC22q_apass1", "LHC22r_apass1"]
    colors = [ROOT.kRed +1, ROOT.kAzure+2, ROOT.kGreen+1, ROOT.kMagenta+1]
    #dirs_tm = [
        #"analysis-muon-selection/output",
        #"analysis-muon-selection/output",
        #"analysis-muon-selection/output",
        #"d-q-muons-selection/output"
    #]
    dirs_tm = [
        "table-maker/output",
        "table-maker/output",
        "table-maker/output"
    ]
    #//ref = "Muons_matchedMchMid"
    # Table maker
    #//cuts_tm = ["Muons_muonQualityCuts"]
    #//cuts_tm = ["Muons_mchTrack"]
    #//cuts_tm = ["Muons_muonLowPt"]
    # Muon selection
    #//cuts_tm = ["TrackMuon_muonQualityCuts"]
    #//cuts_tm = ["TrackMuon_muonLowPt"]

    #cuts_tm = ["Muons_muonLowPt"]
    #cuts_tm = ["Muons_muonQualityCuts"]
    cuts_tm = ["Muons_matchedGlobal"]

    #vars_tm = ["Pt", "Eta", "Phi", "Chi2MCHMID", "pdca", "RAtAbsorberEnd"]
    #labels_tm = ["#it{p}_{T} (GeV/#it{c})", "#eta", "#phi", "#chi^{2}_{MCH-MID}", "p #times DCA", "R_{Abs}"]
    vars_tm = ["Pt", "Eta", "Phi"]
    labels_tm = ["#it{p}_{T} (GeV/#it{c})", "#eta", "#phi"]
    lepton = "muons"

    ##---------------------------------------##
    #prods = ["LHC22s_apass1", "LHC22s_apass2"]
    #prodNames = ["LHC22s_apass1", "LHC22s_apass2"]
    #colors = [ROOT.kRed +1, ROOT.kAzure+2]
    #dir = "analysis-track-selection/output"
    # Muon selection
    #cuts_tm = ["TrackBarrel_BeforeCuts"]
    #vars_tm = ["Pt", "Eta", "Phi", "TPCnSigEle_pIN"]
    #labels_tm = ["#it{p}_{T} (GeV/#it{c})", "#eta", "#phi", "TPC n. #sigma e"]
    #lepton = "electrons"


    histVar_tm = []
    for prod in prods:
        fIn = TFile.Open("../o2/output/AnalysisResults_TR_{}_HL_{}.root".format(prod, lepton))
        fIn.ls()
        # Table Maker
        dir = dirs_tm[prods.index(prod)]
        hlistTM = fIn.Get(dir)
        #hlistTM.ls()
        for cut in cuts_tm:
            if dir == "d-q-muons-selection/output":
                cut = cut.replace("Track", "")
            print(prod, dir, cut)
            listTM = hlistTM.FindObject(cut)
            #listTM.ls()
            for var in vars_tm:
                if "TPC" in var:
                    hist2D = listTM.FindObject(var)
                    hist = hist2D.ProjectionX()
                else:
                    hist = listTM.FindObject(var)
                hist.SetDirectory(0)
                hist.SetLineColor(colors[prods.index(prod)])
                hist.SetMarkerColor(colors[prods.index(prod)])
                hist.SetTitle("")
                hist.SetLineWidth(1)
                hist.SetTitleSize(0.05,"X")
                hist.SetTitleSize(0.045,"Y")
                hist.SetLabelSize(0.045,"X")
                hist.SetLabelSize(0.045,"Y")
                hist.SetTitleOffset(1.2,"X")
                hist.SetTitleOffset(1.35,"Y")
                if var == "Pt":
                    if not hist.GetNbinsX() == 200:
                        hist.Rebin(20)
                #hist.Rebin(5)
                if var == "Eta":
                    if lepton == "muons":
                        hist.GetXaxis().SetRangeUser(-4.2, -1)
                    else:
                        hist.GetXaxis().SetRangeUser(-2, 2)
                if var == "Phi":
                    hist.Rebin(2)
                    #hist.GetXaxis().SetRangeUser(-2*ROOT.TMath.Pi(), 2*ROOT.TMath.Pi())
                    hist.GetXaxis().SetRangeUser(-ROOT.TMath.Pi(), ROOT.TMath.Pi())
                    hist.GetYaxis().SetRangeUser(1e-7, 100)
                if "Chi2" in var:
                    hist.GetXaxis().SetRangeUser(0, 16)
                hist.Scale(1. / hist.Integral())
                hist.SetName("{}_{}".format(prod, var))
                hist.GetXaxis().SetTitle(labels_tm[vars_tm.index(var)])
                histVar_tm.append(hist)

    legend = ROOT.TLegend(0.25, 0.20, 0.45, 0.49, " ", "brNDC")
    legend.SetBorderSize(0)
    legend.SetFillColor(10)
    legend.SetFillStyle(1)
    legend.SetLineStyle(0)
    legend.SetLineColor(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)

    for prodName in prodNames:
        for hist in histVar_tm:
            if prodName in hist.GetName():
                legend.AddEntry(hist, prodName, "L")
                break

    for var in vars_tm:
        canvas = TCanvas("canvas", "canvas", 800, 600)
        canvas.SetLeftMargin(0.15)
        if not "TPC" in var:
            gPad.SetLogy(1)
        for hist in histVar_tm:
            if var in hist.GetName():
                hist.Draw("same")
        legend.Draw("same")
        canvas.Update()
        canvas.SaveAs("figures/qc/summary/{}_{}_{}_distrib_comparison.pdf".format(var, lepton, cuts_tm[0]))

    dirs_tr = [
        "analysis-same-event-pairing/output",
        "analysis-same-event-pairing/output",
        "analysis-same-event-pairing/output"
    ]

    #cuts_tr = ["PairsMuonSEPM_muonLowPt"]
    #cuts_tr = ["PairsMuonSEPM_muonQualityCuts"]
    cuts_tr = ["PairsMuonSEPM_matchedGlobal"]

    vars_tr = ["Mass", "Pt", "Rapidity"]
    labels_tr = ["#it{M} (GeV/#it{c}^{2})", "#it{p}_{T} (GeV/#it{c})", "#it{y}"]

    histVar_tr = []
    for prod in prods:
        fIn = TFile.Open("../o2/output/AnalysisResults_TR_{}_HL_{}.root".format(prod, lepton))
        # Table Maker
        dir = dirs_tr[prods.index(prod)]
        hlistTR = fIn.Get(dir)
        for cut in cuts_tr:
            print(prod, dir, cut)
            listTR = hlistTR.FindObject(cut)
            for var in vars_tr:
                hist = listTR.FindObject(var)
                hist.SetDirectory(0)
                hist.SetLineColor(colors[prods.index(prod)])
                hist.SetMarkerColor(colors[prods.index(prod)])
                hist.SetMarkerStyle(20)
                hist.SetMarkerSize(0.3)
                hist.SetTitle("")
                hist.SetLineWidth(1)
                hist.SetTitleSize(0.05,"X")
                hist.SetTitleSize(0.045,"Y")
                hist.SetLabelSize(0.045,"X")
                hist.SetLabelSize(0.045,"Y")
                hist.SetTitleOffset(1.2,"X")
                hist.SetTitleOffset(1.35,"Y")

                hist.Scale(1. / hist.Integral())
                hist.SetName("{}_{}".format(prod, var))
                hist.GetXaxis().SetTitle(labels_tr[vars_tr.index(var)])
                histVar_tr.append(hist)

    for var in vars_tr:
        canvas = TCanvas("canvas", "canvas", 800, 600)
        canvas.SetLeftMargin(0.15)
        gPad.SetLogy(1)
        for hist in histVar_tr:
            if var in hist.GetName():
                if var == "Mass":
                    hist.GetXaxis().SetRangeUser(2,5)
                hist.Draw("EPsame")
        legend.Draw("same")
        canvas.Update()
        canvas.SaveAs("figures/qc/summary/{}_di{}_{}_distrib_comparison.pdf".format(var, lepton, cuts_tr[0]))

    exit()
    fIn = TFile.Open("../o2/output/AnalysisResults_TR_LHC22f_apass1_bis_HL_muons.root")

    hlistTMAmbi = fIn.Get(inputCfg["input"]["table_maker"])
    listTMAmbi = hlistTMAmbi.FindObject("Ambiguous_{}".format(cuts[0]))
    histAmbi = listTMAmbi.FindObject("Pt")
    histAmbi.Rebin(10)
    histAmbi.Rebin(5)
    histAmbi.SetDirectory(0)

    hlistTMAll = fIn.Get(inputCfg["input"]["table_maker"])
    listTMAll = hlistTMAll.FindObject("{}".format(cuts[0]))
    histAll = listTMAll.FindObject("Pt")
    histAll.Rebin(10)
    histAll.Rebin(5)
    histAll.SetDirectory(0)

    histRatioAmbi = histAmbi.Clone("histRatioAmbi")
    histRatioAmbi.Divide(histAll)
    histRatioAmbi.SetTitle("")
    histRatioAmbi.SetLineWidth(2)
    histRatioAmbi.SetTitleSize(0.05,"X")
    histRatioAmbi.SetTitleSize(0.045,"Y")
    histRatioAmbi.SetLabelSize(0.045,"X")
    histRatioAmbi.SetLabelSize(0.045,"Y")
    histRatioAmbi.SetTitleOffset(1.2,"X")
    histRatioAmbi.SetTitleOffset(1.35,"Y")
    histRatioAmbi.GetXaxis().SetTitle("#it{p}_{T} (GeV/#it{c})")
    histRatioAmbi.GetYaxis().SetTitle("Ambiguous / All")

    letexText = ROOT.TLatex()
    letexText.SetTextSize(0.045)
    letexText.SetNDC()
    letexText.SetTextFont(42)

    canvasRatioAmbi = TCanvas("canvasRatioAmbi", "canvasRatioAmbi", 800, 600)
    canvasRatioAmbi.SetLeftMargin(0.15)
    gPad.SetLogy(1)
    histRatioAmbi.Draw()
    letexText.DrawLatex(0.20, 0.85, "pp #sqrt{s} = 13 TeV, LHC22f")
    letexText.DrawLatex(0.20, 0.78, "MCH + MID matched tracks")
    canvasRatioAmbi.Update()
    canvasRatioAmbi.SaveAs("figures/qc/summary/Pt_ratio_ambiguous.pdf")

    input()

def init_trending(inputCfg):
    print("----- Download and save files in %s -----" % (inputCfg["input"]["output_dir_name"]))
    os.system("mkdir -p {}".format(inputCfg["input"]["output_dir_name"]))
    for iRun in range(0, len(inputCfg["input"]["run_list"])):
        os.system("alien_cp alien://%s/AnalysisResults.root file:%s/AnalysisResults_%i.root" % (inputCfg["input"]["alien_input_path"][iRun], inputCfg["input"]["output_dir_name"], inputCfg["input"]["run_list"][iRun]))
        #print("alien_cp alien://%s/AnalysisResults.root file:%s/AnalysisResults_%i.root" % (inputCfg["input"]["alien_input_path"][iRun], inputCfg["input"]["output_dir_name"], inputCfg["input"]["run_list"][iRun]))

    print("----- Process downloaded files -----")
    os.system("mkdir -p {}".format(inputCfg["output"]["output_dir_name"]))
    for iRun in range(0, len(inputCfg["input"]["run_list"])):
        deleteOutput = False
        if not os.path.isfile("%s/AnalysisResults_%i.root" % (inputCfg["input"]["output_dir_name"], inputCfg["input"]["run_list"][iRun])):
            continue
        
        fIn = TFile.Open("%s/AnalysisResults_%i.root" % (inputCfg["input"]["output_dir_name"], inputCfg["input"]["run_list"][iRun]), "READ")
        fOut = TFile.Open("%s/%s_%i.root" % (inputCfg["output"]["output_dir_name"], inputCfg["output"]["output_file_name"], inputCfg["input"]["run_list"][iRun]), "RECREATE")
        print("%s/%s_%i.root" % (inputCfg["output"]["output_dir_name"], inputCfg["output"]["output_file_name"], inputCfg["input"]["run_list"][iRun]))

        hlistTM = fIn.Get(inputCfg["input"]["table_maker"])
        for cut in inputCfg["input"]["table_maker_dir"]:
            listTM = hlistTM.FindObject(cut)
            for var in inputCfg["input"]["table_maker_obj"]:
                hist = listTM.FindObject(var)
                hist.SetDirectory(0)
                hist.Write("{}_{}".format(var, cut))

        pt_min = inputCfg["input"]["table_reader_pt_min"]
        pt_max = inputCfg["input"]["table_reader_pt_max"]
        rap_min = inputCfg["input"]["table_reader_rap_min"]
        rap_max = inputCfg["input"]["table_reader_rap_max"]
        reso_min = inputCfg["input"]["table_reader_reso_min"]
        reso_max = inputCfg["input"]["table_reader_reso_max"]
        hlistTR = fIn.Get(inputCfg["input"]["table_reader"])
        for cut in inputCfg["input"]["table_reader_dir"]:
            listTR = hlistTR.FindObject(cut)
            for var in inputCfg["input"]["table_reader_obj"]:
                hist = listTR.FindObject(var)
                hist.SetDirectory(0)
                if hist.GetEntries() == 0:
                    deleteOutput = True
                if var == "Mass_Pt":
                    for iPt in range(0, len(pt_min)):
                        pt_bin_min = hist.GetYaxis().FindBin(pt_min[iPt])
                        pt_bin_max = hist.GetYaxis().FindBin(pt_max[iPt])
                        histProj = hist.ProjectionX("{}_{}_Proj_{}_Pt_{}".format(cut, var, pt_min[iPt], pt_max[iPt]), pt_bin_min, pt_bin_max)
                        fOut.cd()
                        histProj.Write("{}_{}_Proj_{}_Pt_{}".format(cut, var, pt_min[iPt], pt_max[iPt]))
                elif var == "Mass_Rapidity":
                    for iRap in range(0, len(rap_min)):
                        rap_bin_min = hist.GetYaxis().FindBin(rap_min[iRap])
                        rap_bin_max = hist.GetYaxis().FindBin(rap_max[iRap])
                        histProj = hist.ProjectionX("{}_{}_Proj_{}_Y_{}".format(cut, var, rap_min[iRap], rap_max[iRap]), rap_bin_min, rap_bin_max)
                        fOut.cd()
                        histProj.Write("{}_{}_Proj_{}_Y_{}".format(cut, var, rap_min[iRap], rap_max[iRap]))
                elif var == "Mass_DeltaPtotTracks":
                    for iReso in range(0, len(reso_min)):
                        reso_bin_min_1 = hist.GetYaxis().FindBin(+reso_min[iReso])
                        reso_bin_max_1 = hist.GetYaxis().FindBin(+reso_max[iReso])
                        reso_bin_min_2 = hist.GetYaxis().FindBin(-reso_max[iReso])
                        reso_bin_max_2 = hist.GetYaxis().FindBin(-reso_min[iReso])
                        histProj1 = hist.ProjectionX("{}_{}_Proj_{}_Reso_{}_1".format(cut, var, reso_min[iReso], reso_max[iReso]), reso_bin_min_1, reso_bin_max_1)
                        histProj2 = hist.ProjectionX("{}_{}_Proj_{}_Reso_{}_2".format(cut, var, reso_min[iReso], reso_max[iReso]), reso_bin_min_2, reso_bin_max_2)
                        histProj = histProj1.Clone("{}_{}_Proj_{}_Reso_{}".format(cut, var, reso_min[iReso], reso_max[iReso]))
                        histProj.Add(histProj2)
                        fOut.cd()
                        histProj1.Write("{}_{}_Proj_{}_Reso_{}_1".format(cut, var, reso_min[iReso], reso_max[iReso]))
                        histProj2.Write("{}_{}_Proj_{}_Reso_{}_2".format(cut, var, reso_min[iReso], reso_max[iReso]))
                        histProj.Write("{}_{}_Proj_{}_Reso_{}".format(cut, var, reso_min[iReso], reso_max[iReso]))
                else:
                    fOut.cd()
                    hist.Write("{}_{}".format(var, cut))
        fOut.Close()
        if deleteOutput:
            os.system("rm %s/%s_%i.root" % (inputCfg["output"]["output_dir_name"], inputCfg["output"]["output_file_name"], inputCfg["input"]["run_list"][iRun]))

def do_trending(inputCfg):
    Load_Style()
    gStyle.SetPalette(ROOT.kBlueRedYellow)

    #period = "LHC22m"
    #run_list = [523142, 523182, 523186, 523306, 523308, 523309, 523401, 523779]
    period = "LHC22o"
    run_list = [526463, 526486, 526606, 527237, 527523, 527850, 527864, 527895, 527902, 527979, 528036, 528105,526465, 526505, 526612, 527345, 527826, 527852, 527869, 527898, 527976, 528021, 528094,526467, 526525, 526638, 527518, 527828, 527863, 527871, 527899, 527978, 528026, 528097]

    fIn_path_qa = "/Users/lucamicheletti/GITHUB/dq_analysis_utils/macro/output/Data/trending_{}".format(period)

    hist_chi2 = []
    hist_chi2MCHMID = []

    hist_mean_chi2 = ROOT.TH1F("hist_mean_chi2", "", len(run_list), 0, len(run_list))
    hist_mean_chi2.GetYaxis().SetRangeUser(0.01, 50)
    hist_mean_chi2.GetYaxis().SetTitle("#chi^{2}")
    hist_mean_chi2.SetMarkerStyle(24)
    hist_mean_chi2.SetMarkerColor(ROOT.kAzure+2)
    hist_mean_chi2.SetLineColor(ROOT.kAzure+2)
    hist_mean_chi2.SetLineWidth(2)

    for iRun in range(0, len(run_list)):
        fIn_qa = TFile.Open("{}/{}_apass2_muons_{}.root".format(fIn_path_qa, period, run_list[iRun]))
        
        tmp_hist_chi2 = fIn_qa.Get("Chi2_Muons_muonLowPt")
        tmp_hist_chi2.Scale(1. / tmp_hist_chi2.Integral())
        #tmp_hist_chi2.SetLineColor(iRun+1)
        tmp_hist_chi2.SetLineWidth(2)
        tmp_hist_chi2.SetDirectory(0)
        tmp_hist_chi2.SetTitle("{}".format(run_list[iRun]))
        hist_chi2.append(tmp_hist_chi2)

        hist_mean_chi2.SetBinContent(iRun+1, tmp_hist_chi2.GetMean())
        hist_mean_chi2.SetBinError(iRun+1, 0)
        hist_mean_chi2.GetXaxis().SetBinLabel(iRun+1, str(run_list[iRun]))

        tmp_hist_chi2MCHMID = fIn_qa.Get("Chi2MCHMID_Muons_muonLowPt")
        tmp_hist_chi2MCHMID.Scale(1. / tmp_hist_chi2MCHMID.Integral())
        #tmp_hist_chi2MCHMID.SetLineColor(iRun+1)
        tmp_hist_chi2MCHMID.SetLineWidth(2)
        tmp_hist_chi2MCHMID.SetDirectory(0)
        tmp_hist_chi2MCHMID.SetTitle("{}".format(run_list[iRun]))
        hist_chi2MCHMID.append(tmp_hist_chi2MCHMID)


    canvas_chi2 = ROOT.TCanvas("canvas_chi2", "", 800, 600)
    gPad.SetLogy(1)
    gPad.SetTitle("")
    for iRun in range(0, len(run_list)):
        hist_chi2[iRun].Draw("H SAME PLC")
    gPad.BuildLegend(0.78,0.35,0.980,0.935,"","L")
    canvas_chi2.Update()
    canvas_chi2.SaveAs("trending_track_chi2_{}.pdf".format(period))


    canvas_chi2MCHMID = ROOT.TCanvas("canvas_chi2MCHMID", "", 800, 600)
    gPad.SetLogy(1)
    for iRun in range(0, len(run_list)):
        hist_chi2MCHMID[iRun].Draw("H SAME PLC")
    gPad.BuildLegend(0.78,0.35,0.980,0.935,"","L")
    canvas_chi2MCHMID.Update()
    canvas_chi2MCHMID.SaveAs("trending_track_chi2MCHMID_{}.pdf".format(period))

    fIn_path_fit = "/Users/lucamicheletti/GITHUB/dq_fit_library/validation/output/trending_{}_apass2/CB2_VWG".format(period)

    hist_mean_Jpsi_PDG = ROOT.TH1F("hist_mean_Jpsi_PDG", "", len(run_list), 0, len(run_list))
    hist_mean_Jpsi_PDG.SetLineWidth(3)
    hist_mean_Jpsi_PDG.SetLineColor(kGray+1)
    hist_mean_Jpsi_PDG.SetFillColorAlpha(kGray+1, 0.3)

    hist_mean_Jpsi = ROOT.TH1F("hist_mean_Jpsi", "", len(run_list), 0, len(run_list))
    hist_mean_Jpsi.GetYaxis().SetRangeUser(2.9, 3.3)
    hist_mean_Jpsi.GetYaxis().SetTitle("#it{m}_{J/#psi} (GeV/#it{c}^{2})")
    hist_mean_Jpsi.SetMarkerStyle(24)
    hist_mean_Jpsi.SetMarkerColor(ROOT.kAzure+2)
    hist_mean_Jpsi.SetLineColor(ROOT.kAzure+2)
    hist_mean_Jpsi.SetLineWidth(2)

    hist_width_Jpsi = ROOT.TH1F("hist_mean_Jpsi", "", len(run_list), 0, len(run_list))
    hist_width_Jpsi.GetYaxis().SetRangeUser(0.06, 0.12)
    hist_width_Jpsi.GetYaxis().SetTitle("#it{#sigma}_{J/#psi} (GeV/#it{c}^{2})")
    hist_width_Jpsi.SetMarkerStyle(24)
    hist_width_Jpsi.SetMarkerColor(ROOT.kAzure+2)
    hist_width_Jpsi.SetLineColor(ROOT.kAzure+2)
    hist_width_Jpsi.SetLineWidth(2)

    for iRun in range(0, len(run_list)):
        fIn_fit = TFile.Open("{}_{}/Mass_PairsMuonSEPM_muonLowPt.root".format(fIn_path_fit, run_list[iRun]))
        hist = fIn_fit.Get("fit_results_CB2_VWG__2_5")
        for iBin in range(0, hist.GetNbinsX()):
            if hist.GetXaxis().GetBinLabel(iBin+1) == "mean_Jpsi":
                hist_mean_Jpsi.SetBinContent(iRun+1, hist.GetBinContent(iBin+1))
                hist_mean_Jpsi.SetBinError(iRun+1, hist.GetBinError(iBin+1))
                hist_mean_Jpsi.GetXaxis().SetBinLabel(iRun+1, str(run_list[iRun]))

                hist_mean_Jpsi_PDG.SetBinContent(iRun+1, 3.096)
                hist_mean_Jpsi_PDG.SetBinError(iRun+1, ROOT.TMath.Sqrt(0.002 * 0.002 + 0.006 * 0.006))

            if hist.GetXaxis().GetBinLabel(iBin+1) == "width_Jpsi":
                print(run_list[iRun], ") ", hist.GetBinContent(iBin+1), " +/- ", hist.GetBinError(iBin+1))
                hist_width_Jpsi.SetBinContent(iRun+1, hist.GetBinContent(iBin+1))
                hist_width_Jpsi.SetBinError(iRun+1, hist.GetBinError(iBin+1))
                hist_width_Jpsi.GetXaxis().SetBinLabel(iRun+1, str(run_list[iRun]))


    legend = ROOT.TLegend(0.7, 0.30, 0.9, 0.50, " ", "brNDC")
    legend.SetBorderSize(0)
    legend.SetFillColor(10)
    legend.SetFillStyle(1)
    legend.SetLineStyle(0)
    legend.SetLineColor(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)
    legend.AddEntry(hist_mean_Jpsi, "Data", "PL")
    legend.AddEntry(hist_mean_Jpsi_PDG, "PDG", "F")

    canvas_mean_Jpsi = ROOT.TCanvas("canvas_mean_Jpsi", "", 1200, 600)
    hist_mean_Jpsi.Draw("EP")
    hist_mean_Jpsi_PDG.Draw("E2same")
    legend.Draw("same")
    canvas_mean_Jpsi.Update()
    canvas_mean_Jpsi.SaveAs("trending_mean_Jpsi_{}.pdf".format(period))

    canvas_width_Jpsi = ROOT.TCanvas("canvas_width_Jpsi", "", 1200, 600)
    hist_width_Jpsi.Draw("EP")
    canvas_width_Jpsi.Update()
    canvas_width_Jpsi.SaveAs("trending_width_Jpsi_{}.pdf".format(period))

    canvas_mean_chi2 = ROOT.TCanvas("canvas_mean_chi2_{}".format(period), "", 1200, 600)
    gPad.SetLogy()
    hist_mean_chi2.Draw("EP")
    canvas_mean_chi2.Update()
    canvas_mean_chi2.SaveAs("trending_mean_chi2_{}.pdf".format(period))

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
    parser.add_argument("--bkg_subtr", help="Subtract bkg", action="store_true")
    parser.add_argument("--qa", help="Quality assurance", action="store_true")
    parser.add_argument("--init_trending", help="Enable trending vs run number", action="store_true")
    parser.add_argument("--do_trending", help="Do trending vs run number", action="store_true")
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
    if args.bkg_subtr:
        bkg_subtr()
    if args.qa:
        qa(inputCfg)
    if args.init_trending:
        init_trending(inputCfg)
    if args.do_trending:
        do_trending(inputCfg)

main()