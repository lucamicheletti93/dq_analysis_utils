import os
import sys
import yaml
import math
import numpy as np
import argparse
import ROOT
from ROOT import *
sys.path.append('../../dq_fit_library/utils')
from plot_library import LoadStyle, SetLegend

def qc(inputCfg):
    fInNames = inputCfg["inputs"]["histos"]
    labels = inputCfg["inputs"]["labels"]
    colors = inputCfg["inputs"]["colors"]
    colCounter = []

    fOutName = inputCfg["output"]["name"]

    # Table Maker
    dirName = inputCfg["table_maker"]["directory"]
    selNames = inputCfg["table_maker"]["selections"]
    varNames = inputCfg["table_maker"]["vars"]
    rebins = inputCfg["table_maker"]["rebins"]
    minRanges = inputCfg["table_maker"]["minRanges"]
    maxRanges = inputCfg["table_maker"]["maxRanges"]
    outputDirName = inputCfg["table_maker"]["outputDir"]

    if os.path.exists(outputDirName):
        print(f'{outputDirName} already exists!')
    else:
        os.mkdir(outputDirName)

    histsTM = [[[None for _ in range(len(varNames))] for _ in range(len(selNames))] for _ in range(len(fInNames))]

    for i_fInName, fInName in enumerate(fInNames):
        fIn = TFile(fInName, "READ")
        fIn.ls()
        histEvCount = fIn.Get("event-selection-task/hColCounterAcc")
        colCounter.append(histEvCount.GetEntries())
        print(f'{labels[i_fInName]} - N collision accepted = {histEvCount.GetEntries()}')
        hlistIn = fIn.Get(dirName)
        for i_selName, selName in enumerate(selNames):
            listIn = hlistIn.FindObject(selName)
            for i_varName, varName in enumerate(varNames):
                histsTM[i_fInName][i_selName][i_varName] = listIn.FindObject(varName)
                histsTM[i_fInName][i_selName][i_varName].SetTitle(labels[i_fInName])
                histsTM[i_fInName][i_selName][i_varName].SetLineColor(colors[i_fInName])
                histsTM[i_fInName][i_selName][i_varName].SetLineWidth(2)
                histsTM[i_fInName][i_selName][i_varName].Rebin(rebins[i_varName])
                histsTM[i_fInName][i_selName][i_varName].GetXaxis().SetRangeUser(minRanges[i_varName], maxRanges[i_varName])
                if inputCfg["table_maker"]["normToColls"]: histsTM[i_fInName][i_selName][i_varName].Scale(1. / colCounter[i_fInName])
                if inputCfg["table_maker"]["normToInt"]: histsTM[i_fInName][i_selName][i_varName].Scale(1. / histsTM[i_fInName][i_selName][i_varName].Integral())
        fIn.Close()

    for i_selName, selName in enumerate(selNames):
        for i_varName, varName in enumerate(varNames):
            canvas = TCanvas(f'canvas_{selName}_{varName}', f'canvas_{selName}_{varName}', 600, 600)
            gPad.SetLogy(1)
            for i_fInName, fInName in enumerate(fInNames):
                histsTM[i_fInName][i_selName][i_varName].Draw("H SAME")
            gPad.BuildLegend(0.78, 0.75, 0.980, 0.935,"","L")
            canvas.Update()
            canvas.SaveAs(f'{outputDirName}/{selName}_{varName}.pdf')


    # Muon Selection
    dirName = inputCfg["muon_selection"]["directory"]
    selNames = inputCfg["muon_selection"]["selections"]
    varNames = inputCfg["muon_selection"]["vars"]
    rebins = inputCfg["muon_selection"]["rebins"]
    minRanges = inputCfg["muon_selection"]["minRanges"]
    maxRanges = inputCfg["muon_selection"]["maxRanges"]
    outputDirName = inputCfg["muon_selection"]["outputDir"]

    if os.path.exists(outputDirName):
        print(f'{outputDirName} already exists!')
    else:
        os.mkdir(outputDirName)

    histsMS = [[[None for _ in range(len(varNames))] for _ in range(len(selNames))] for _ in range(len(fInNames))]
    histsRatioMS = [[[None for _ in range(len(varNames))] for _ in range(len(selNames))] for _ in range(len(fInNames))]

    for i_fInName, fInName in enumerate(fInNames):
        print(f'[muon-selection] Processing {fInName} ...')
        fIn = TFile(fInName, "READ")
        histEvCount = fIn.Get("event-selection-task/hColCounterAcc")
        colCounter.append(histEvCount.GetEntries())
        print(f'{labels[i_fInName]} - N collision accepted = {histEvCount.GetEntries()}')
        hlistIn = fIn.Get(dirName)
        for i_selName, selName in enumerate(selNames):
            listIn = hlistIn.FindObject(selName)
            for i_varName, varName in enumerate(varNames):
                histsMS[i_fInName][i_selName][i_varName] = listIn.FindObject(varName)
                histsMS[i_fInName][i_selName][i_varName].SetTitle(labels[i_fInName])
                histsMS[i_fInName][i_selName][i_varName].SetLineColor(colors[i_fInName])
                histsMS[i_fInName][i_selName][i_varName].SetLineWidth(2)
                histsMS[i_fInName][i_selName][i_varName].Rebin(rebins[i_varName])
                histsMS[i_fInName][i_selName][i_varName].GetXaxis().SetRangeUser(minRanges[i_varName], maxRanges[i_varName])
                if inputCfg["muon_selection"]["normToColls"]: histsMS[i_fInName][i_selName][i_varName].Scale(1. / colCounter[i_fInName])
                if inputCfg["muon_selection"]["normToInt"]: histsMS[i_fInName][i_selName][i_varName].Scale(1. / histsMS[i_fInName][i_selName][i_varName].Integral())
        fIn.Close()

    for i_fInName, fInName in enumerate(fInNames):
        for i_selName, selName in enumerate(selNames):
            for i_varName, varName in enumerate(varNames):
                histsRatioMS[i_fInName][i_selName][i_varName] = histsMS[i_fInName][i_selName][i_varName].Clone(f'{histsMS[i_fInName][i_selName][i_varName].GetName()}_Ratio')
                histsRatioMS[i_fInName][i_selName][i_varName].Divide(histsMS[0][i_selName][i_varName])

    for i_selName, selName in enumerate(selNames):
        for i_varName, varName in enumerate(varNames):
            canvas = TCanvas(f'canvas_{selName}_{varName}', f'canvas_{selName}_{varName}', 1200, 600)
            canvas.Divide(2, 1)
            canvas.cd(1)
            gPad.SetLogy(1)
            for i_fInName, fInName in enumerate(fInNames):
                histsMS[i_fInName][i_selName][i_varName].Draw("H SAME")
            gPad.BuildLegend(0.78, 0.75, 0.980, 0.935,"","L")
            canvas.Update()
            canvas.cd(2)
            gPad.SetLogy(0)
            for i_fInName, fInName in enumerate(fInNames):
                histsRatioMS[i_fInName][i_selName][i_varName].GetYaxis().SetRangeUser(0, 2)
                histsRatioMS[i_fInName][i_selName][i_varName].GetYaxis().SetTitle("Ratio")
                histsRatioMS[i_fInName][i_selName][i_varName].Draw("H SAME")
            gPad.BuildLegend(0.78, 0.75, 0.980, 0.935,"","L")
            canvas.Update()
            canvas.SaveAs(f'{outputDirName}/{selName}_{varName}.pdf')



    # Table Reader
    dirName = inputCfg["table_reader"]["directory"]
    selNames = inputCfg["table_reader"]["selections"]
    varNames = inputCfg["table_reader"]["vars"]
    rebins = inputCfg["table_reader"]["rebins"]
    minRanges = inputCfg["table_reader"]["minRanges"]
    maxRanges = inputCfg["table_reader"]["maxRanges"]
    var2dNames = inputCfg["table_reader"]["vars2D"]
    outputDirName = inputCfg["table_reader"]["outputDir"]

    if os.path.exists(outputDirName):
        print(f'{outputDirName} already exists!')
    else:
        os.mkdir(outputDirName)

    histsTR = [[[None for _ in range(len(varNames))] for _ in range(len(selNames))] for _ in range(len(fInNames))]
    hists2dTR = [[[None for _ in range(len(var2dNames))] for _ in range(len(selNames))] for _ in range(len(fInNames))]

    for i_fInName, fInName in enumerate(fInNames):
        fIn = TFile(fInName, "READ")
        hlistIn = fIn.Get(dirName)
        for i_selName, selName in enumerate(selNames):
            listIn = hlistIn.FindObject(selName)
            for i_varName, varName in enumerate(varNames):
                histsTR[i_fInName][i_selName][i_varName] = listIn.FindObject(varName)
                histsTR[i_fInName][i_selName][i_varName].SetTitle(labels[i_fInName])
                histsTR[i_fInName][i_selName][i_varName].SetName(f'{labels[i_fInName]}_{selName}_{varName}')
                histsTR[i_fInName][i_selName][i_varName].SetLineColor(colors[i_fInName])
                histsTR[i_fInName][i_selName][i_varName].SetLineWidth(2)
                histsTR[i_fInName][i_selName][i_varName].Rebin(rebins[i_varName])
                histsTR[i_fInName][i_selName][i_varName].GetXaxis().SetRangeUser(minRanges[i_varName], maxRanges[i_varName])
                if inputCfg["table_reader"]["normToColls"]: histsTR[i_fInName][i_selName][i_varName].Scale(1. / colCounter[i_fInName])
                if inputCfg["table_reader"]["normToInt"]: histsTR[i_fInName][i_selName][i_varName].Scale(1. / histsTR[i_fInName][i_selName][i_varName].Integral())
            
            for i_var2dName, var2dName in enumerate(var2dNames):
                hists2dTR[i_fInName][i_selName][i_var2dName] = listIn.FindObject(var2dName)
                if inputCfg["table_reader"]["normToColls"]: histsTR[i_fInName][i_selName][i_var2dName].Scale(1. / colCounter[i_fInName])
                if inputCfg["table_reader"]["normToInt"]: histsTR[i_fInName][i_selName][i_var2dName].Scale(1. / histsTR[i_fInName][i_selName][i_var2dName].Integral())
        fIn.Close()

    fOut = TFile(fOutName, "RECREATE")
    for i_selName, selName in enumerate(selNames):
        for i_varName, varName in enumerate(varNames):
            canvas = TCanvas(f'canvas_{selName}_{varName}', f'canvas_{selName}_{varName}', 600, 600)
            gPad.SetLogy(1)
            for i_fInName, fInName in enumerate(fInNames):
                histsTR[i_fInName][i_selName][i_varName].Draw("H SAME")
                histsTR[i_fInName][i_selName][i_varName].Write()
            gPad.BuildLegend(0.78, 0.75, 0.980, 0.935,"","L")
            canvas.Update()
            canvas.SaveAs(f'{outputDirName}/{selName}_{varName}.pdf')

        for i_fInName, fInName in enumerate(fInNames):
            for i_var2dName, var2dName in enumerate(var2dNames):
                minCuts = inputCfg["table_reader"]["minCuts"]
                maxCuts = inputCfg["table_reader"]["maxCuts"]
                for i_cut in range(0, len(minCuts[i_var2dName])):
                    hist2d = hists2dTR[i_fInName][i_selName][i_var2dName]
                    binWidth = hist2d.GetYaxis().GetBinWidth(1)
                    minCut = minCuts[i_var2dName][i_cut]
                    maxCut = maxCuts[i_var2dName][i_cut]
                    if i_cut == 0:
                        minBinCut = hist2d.GetYaxis().FindBin(minCut)
                        maxBinCut = hist2d.GetYaxis().FindBin(maxCut)
                    else:
                        minBinCut = hist2d.GetYaxis().FindBin(minCut+binWidth)
                        maxBinCut = hist2d.GetYaxis().FindBin(maxCut)
                    histProj = hist2d.ProjectionX(f'{labels[i_fInName]}_projMass_{var2dName}_{selName}_{minBinCut}_{maxBinCut}', minBinCut, maxBinCut)
                    histProj.Write()
    fOut.Close()

def analysis(inputCfg):
    LoadStyle()
    letexTitle = ROOT.TLatex()
    letexTitle.SetTextSize(0.040)
    letexTitle.SetNDC()
    letexTitle.SetTextFont(42)
    
    rebins = inputCfg["analysis"]["rebins"]
    minRanges = inputCfg["analysis"]["minRanges"]
    maxRanges = inputCfg["analysis"]["maxRanges"]
    outputDirName = inputCfg["analysis"]["outputDir"]

    if os.path.exists(outputDirName):
        print(f'{outputDirName} already exists!')
    else:
        os.mkdir(outputDirName)

    fInName = inputCfg["analysis"]["input"]
    fIn = TFile(fInName, "READ")

    for i_dataset, dataset in enumerate(inputCfg["analysis"]["datasets"]):
        for i_selName, selName in enumerate(inputCfg["analysis"]["selections"]):
            for i_varName, varName in enumerate(inputCfg["analysis"]["vars"]):
                histMassSEPM = fIn.Get(f'{dataset}_PairsMuonSEPM_{selName}_{varName}')
                histMassSEPP = fIn.Get(f'{dataset}_PairsMuonSEPP_{selName}_{varName}')
                histMassSEMM = fIn.Get(f'{dataset}_PairsMuonSEMM_{selName}_{varName}')

                nBins = histMassSEPM.GetNbinsX()
                minBin = histMassSEPM.GetBinLowEdge(1)
                maxBin = histMassSEPM.GetBinLowEdge(nBins+1)

                histSig = TH1F(f'histSig_{dataset}_{selName}', "", nBins, minBin, maxBin); histSig.SetLineColor(kRed+1); histSig.SetLineWidth(2)
                histBkg = TH1F(f'histBkg_{dataset}_{selName}', "", nBins, minBin, maxBin); histBkg.SetLineColor(kAzure+4); histBkg.SetLineWidth(2)
                histSigBkg = TH1F(f'histSigBkg_{dataset}_{selName}', "", nBins, minBin, maxBin); histSigBkg.SetLineColor(kBlack); histSigBkg.SetLineWidth(2); histSigBkg.SetMarkerStyle(20)

                for iBin in range(0, histMassSEPM.GetNbinsX()):
                    SEPM = histMassSEPM.GetBinContent(iBin+1)
                    SEPP = histMassSEPP.GetBinContent(iBin+1)
                    SEMM = histMassSEMM.GetBinContent(iBin+1)
                    histSigBkg.SetBinContent(iBin+1, SEPM)
                    histSigBkg.SetBinError(iBin+1, TMath.Sqrt(SEPM))
                    histBkg.SetBinContent(iBin+1, 2 * TMath.Sqrt(SEPP * SEMM))
                    #histBkg.SetBinError(iBin+1, TMath.Sqrt(2 * TMath.Sqrt(SEPP * SEMM))) #WARNING!
                    histSig.SetBinContent(iBin+1, SEPM - 2 * TMath.Sqrt(SEPP * SEMM))
                    #histSig.SetBinError(iBin+1, 0.2 * (SEPM - 2 * TMath.Sqrt(SEPP * SEMM))) #WARNING!

                histSigBkg.Rebin(rebins[i_varName])
                histBkg.Rebin(rebins[i_varName])
                histSig.Rebin(rebins[i_varName])

                if (dataset in inputCfg["analysis"]["datasetsForFit"]) and (selName in inputCfg["analysis"]["selectionsForFit"]):
                    mJpsi = ROOT.RooRealVar("Dimuon mass", "#it{m}_{#mu#mu} (GeV/#it{c}^{2})", 2.60, 4.00)

                    dataHistSigBkg = ROOT.RooDataHist("dataHistSigBkg", "dataHistSigBkg", [mJpsi], Import=histSigBkg)

                    meanJpsi  = ROOT.RooRealVar("meanJpsi", "meanJpsi", 3.096, 2.9, 3.3)
                    sigmaJpsi = ROOT.RooRealVar("sigmaJpsi", "sigmaJpsi", 0.095, 0.060, 0.120)
                    gausPdfJpsi = ROOT.RooGaussian("gausPdfJpsi", "Gaus J/psi", mJpsi, meanJpsi, sigmaJpsi)

                    chebyParsJpsi = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.00, -100, 100) for i in range(3)]
                    chebyPdfJpsi = ROOT.RooChebychev("chebyPdfJpsi", "Cheby for Bkg1", mJpsi, ROOT.RooArgList(*chebyParsJpsi))

                    nSigJpsi  = ROOT.RooRealVar("nSigJpsi", "Jpsi signal", 1e2, 0., 1e5)
                    nBkgJpsi  = ROOT.RooRealVar("nBkgJpsi", "Jpsi background", 5e3, 0., 1e6)
                    modelJpsi = ROOT.RooAddPdf("modelJpsi", "sigJpsi + bkgJpsi", ROOT.RooArgList(gausPdfJpsi, chebyPdfJpsi), ROOT.RooArgList(nSigJpsi, nBkgJpsi))

                    fitResultJpsi = modelJpsi.fitTo(dataHistSigBkg, ROOT.RooFit.PrintLevel(3), ROOT.RooFit.Optimize(1), ROOT.RooFit.Hesse(1), ROOT.RooFit.Minos(1), ROOT.RooFit.Strategy(2), ROOT.RooFit.Save(1))

                    mJpsiframe = mJpsi.frame(Title=" ")
                    dataHistSigBkg.plotOn(mJpsiframe)
                    modelJpsi.plotOn(mJpsiframe)
                    modelJpsi.plotOn(mJpsiframe, Name={"Sig"}, Components={gausPdfJpsi}, LineStyle="--", LineColor=ROOT.kRed+1)
                    modelJpsi.plotOn(mJpsiframe, Name={"Bkg"}, Components={chebyPdfJpsi}, LineStyle="--", LineColor=ROOT.kAzure+4)

                    canvasFit = ROOT.TCanvas("canvasFit", f'canvasFit_{dataset}_{selName}', 600, 600)
                    canvasFit.SetTickx(1)
                    canvasFit.SetTicky(1)

                    mJpsiframe.GetYaxis().SetTitleOffset(1.4)
                    mJpsiframe.Draw()

                    legendFit = ROOT.TLegend(0.65, 0.45, 0.85, 0.55)
                    SetLegend(legendFit)
                    legendFit.AddEntry(mJpsiframe.findObject("Sig"), "J/#psi", "L")
                    legendFit.AddEntry(mJpsiframe.findObject("Bkg"), "Bkg", "L")
                    legendFit.Draw()

                    letexTitle.DrawLatex(0.35, 0.88, "ALICE, Pb#minusPb, #sqrt{#it{s}_{NN}} = 5.36 TeV")
                    letexTitle.DrawLatex(0.35, 0.81, "Inclusive J/#psi #rightarrow #mu^{+}#mu^{-}, 2.5 < #it{y} < 4")
                    letexTitle.DrawLatex(0.55, 0.74, "#it{N}_{J/#psi} = %1.0f #pm %1.0f" % (nSigJpsi.getVal(), nSigJpsi.getError()))
                    letexTitle.DrawLatex(0.55, 0.68, "#it{#mu}_{J/#psi} = %4.3f #pm %4.3f" % (meanJpsi.getVal(), meanJpsi.getError()))
                    letexTitle.DrawLatex(0.55, 0.62, "#it{#sigma}_{J/#psi} = %4.3f #pm %4.3f" % (sigmaJpsi.getVal(), sigmaJpsi.getError()))
                    canvasFit.SaveAs(f'{outputDirName}/fit_{dataset}_{selName}.pdf')

                gStyle.SetOptStat(0)
                canvasCombBkg = ROOT.TCanvas("canvasCombBkg", f'canvasCombBkg_{dataset}_{selName}', 600, 600)
                histSigBkg.GetXaxis().SetRangeUser(minRanges[i_varName], maxRanges[i_varName])
                histSigBkg.GetXaxis().SetTitle("#it{m}_{#mu#mu} (GeV/#it{c}^{2})")
                histSigBkg.SetTitle("")
                histSigBkg.Draw("EP")
                histBkg.Draw("H SAME")
                histSig.Draw("H SAME")

                legendFit = ROOT.TLegend(0.60, 0.55, 0.85, 0.75)
                SetLegend(legendFit)
                legendFit.AddEntry(histSigBkg, "Data", "EP")
                legendFit.AddEntry(histSig, "Sig", "L")
                legendFit.AddEntry(histBkg, "LS Bkg", "L")
                legendFit.Draw("SAME")

                letexTitle.DrawLatex(0.35, 0.88, "ALICE, Pb#minusPb, #sqrt{#it{s}_{NN}} = 5.36 TeV")
                letexTitle.DrawLatex(0.35, 0.81, "Inclusive J/#psi #rightarrow #mu^{+}#mu^{-}, 2.5 < #it{y} < 4")
                          
                canvasCombBkg.SaveAs(f'{outputDirName}/combBkg_{dataset}_{selName}.pdf')


def process_tree(inputCfg):
    fInNames = inputCfg["inputs"]["trees"]
    labels = inputCfg["inputs"]["labels"]
    fOutName = inputCfg["dimuonall"]["output"]
    print(fOutName)
    cuts = (inputCfg["dimuonall"]["cuts"])
    gPi = math.pi
    gPi2 = gPi / 2.

    hMassFullPM = ROOT.TH1F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Mass","Dimuon mass SEPM ;m (GeV/#it{c}^{2});#", 100, 2, 5)
    hMassFullPP = ROOT.TH1F("LHC23_full_PairsMuonSEPP_matchedQualityCuts_Mass","Dimuon mass SEPP ;m (GeV/#it{c}^{2});#", 100, 2, 5)
    hMassFullMM = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Mass","Dimuon mass SEMM ;m (GeV/#it{c}^{2});#", 100, 2, 5)
    hTauzFullPM = ROOT.TH1F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Tauz","Dimuon tauz SEPM ;#tau_{z};#", 1000, -0.1, 0.1)
    hTauzFullPP = ROOT.TH1F("LHC23_full_PairsMuonSEPP_matchedQualityCuts_Tauz","Dimuon tauz SEPM ;#tau_{z};#", 1000, -0.1, 0.1)
    hTauzFullMM = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Tauz","Dimuon tauz SEPM ;#tau_{z};#", 1000, -0.1, 0.1)
    hTauxyFullPM = ROOT.TH1F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Tauxy","Dimuon tauxy SEPM ;#tau_{xy};#", 1000, 0, 0.02)
    hTauxyFullPP = ROOT.TH1F("LHC23_full_PairsMuonSEPP_matchedQualityCuts_Tauxy","Dimuon tauxy SEPM ;#tau_{xy};#", 1000, 0, 0.02)
    hTauxyFullMM = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Tauxy","Dimuon tauxy SEPM ;#tau_{xy};#", 1000, 0, 0.02)
    hEtaPhiFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_EtaPhi","Dimuon #eta - #varphi SEPM ;#eta;#varphi", 500, -4.5, -2., 500, -4, 4)
    hMassPtFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_MassPt","Dimuon mass - pT SEPM ;m (GeV/#it{c}^{2});#it{p}_{T} (GeV/#it{c})", 100, 2, 5, 500, 0, 20)

    hDcax1Dcax2FullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcax1Dcax2","Dimuon Dca x1 - Dca x2 SEPM ;DCA X1;DCA X2", 500, -1, 1, 500, -1, 1)
    hDcay1Dcay2FullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcay1Dcay2","Dimuon Dca y1 - Dca y2 SEPM ;DCA Y1;DCA Y2", 500, -1, 1, 500, -1, 1)
    hDcax1Dcax2FullPP = ROOT.TH2F("LHC23_full_PairsMuonSEPP_matchedQualityCuts_Dcax1Dcax2","Dimuon Dca x1 - Dca x2 SEPP ;DCA X1;DCA X2", 500, -1, 1, 500, -1, 1)
    hDcay1Dcay2FullPP = ROOT.TH2F("LHC23_full_PairsMuonSEPP_matchedQualityCuts_Dcay1Dcay2","Dimuon Dca y1 - Dca y2 SEPP ;DCA Y1;DCA Y2", 500, -1, 1, 500, -1, 1)
    hDcax1Dcax2FullMM = ROOT.TH2F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcax1Dcax2","Dimuon Dca x1 - Dca x2 SEMM ;DCA X1;DCA X2", 500, -1, 1, 500, -1, 1)
    hDcay1Dcay2FullMM = ROOT.TH2F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcay1Dcay2","Dimuon Dca y1 - Dca y2 SEMM ;DCA Y1;DCA Y2", 500, -1, 1, 500, -1, 1)
    hDcax1Dcay1FullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcax1Dcay1","Dimuon Dca x1 - Dca y1 SEPM ;DCA X1;DCA Y1", 500, -1, 1, 500, -1, 1)
    hDcax2Dcay2FullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcay2Dcay2","Dimuon Dca x2 - Dca y2 SEPM ;DCA X2;DCA Y2", 500, -1, 1, 500, -1, 1)

    hDcax1PhiFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcax1Phi","Dimuon Dca x1 - #varphi SEPM ;DCA X1;#varphi", 500, -1, 1, 500, -4, 4)
    hDcay1PhiFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcay1Phi","Dimuon Dca y1 - #varphi SEPM ;DCA Y1;#varphi", 500, -1, 1, 500, -4, 4)

    hDcax1Chi2MatchMCHMFTFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcax1Chi2MatchMCHMFT","Dimuon Dca x1 - #chi^{2}_{MCH-MFT} SEPM ;DCA X1;#chi^{2}_{MCH-MFT}", 500, -1, 1, 500, 0, 100)
    hDcay1Chi2MatchMCHMFTFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcay1Chi2MatchMCHMFT","Dimuon Dca y1 - #chi^{2}_{MCH-MFT} SEPM ;DCA Y1;#chi^{2}_{MCH-MFT}", 500, -1, 1, 500, 0, 100)

    hDcax1EtaFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcax1Eta","Dimuon Dca x1 - #eta SEPM ;DCA X1;#eta", 500, -1, 1, 500, -4.5, -2.)
    hDcay1EtaFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcay1Eta","Dimuon Dca y1 - #eta SEPM ;DCA Y1;#eta", 500, -1, 1, 500, -4.5, -2.)

    hDcax1MassFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcax1Mass","Dimuon Dca x1 - mass SEPM ;DCA X1;m (GeV/#it{c}^{2})", 500, -1, 1, 100, 2, 5)
    hDcax2MassFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcax2Mass","Dimuon Dca x2 - mass SEPM ;DCA X2;m (GeV/#it{c}^{2})", 500, -1, 1, 100, 2, 5)
    hDcay1MassFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcay1Mass","Dimuon Dca y1 - mass SEPM ;DCA Y1;m (GeV/#it{c}^{2})", 500, -1, 1, 100, 2, 5)
    hDcay2MassFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcay2Mass","Dimuon Dca y2 - mass SEPM ;DCA Y2;m (GeV/#it{c}^{2})", 500, -1, 1, 100, 2, 5)

    hDcax1Pt1FullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcax1Pt1","Dimuon Dca x1 - Pt1 SEPM ;DCA X1;#it{p}_{T} (GeV/#it{c})", 500, -1, 1, 500, 0, 20)
    hDcax2Pt2FullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcax2Pt2","Dimuon Dca x2 - Pt2 SEPM ;DCA X2;#it{p}_{T} (GeV/#it{c})", 500, -1, 1, 500, 0, 20)
    hDcay1Pt1FullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcay1Pt1","Dimuon Dca y1 - Pt1 SEPM ;DCA Y1;#it{p}_{T} (GeV/#it{c})", 500, -1, 1, 500, 0, 20)
    hDcay2Pt2FullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcay2Pt2","Dimuon Dca y2 - Pt2 SEPM ;DCA Y2;#it{p}_{T} (GeV/#it{c})", 500, -1, 1, 500, 0, 20)

    hDcax1PosxFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcax1Posx","Dimuon Dca x1 - Pos X SEPM ;DCA X1;Pos X", 500, -1, 1, 1000, -0.1, 0.1)
    hDcax1PosyFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcax1Posy","Dimuon Dca x1 - Pos Y SEPM ;DCA X1;Pos Y", 500, -1, 1, 1000, -0.1, 0.1)
    hDcax1PoszFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcax1Posz","Dimuon Dca x1 - Pos Z SEPM ;DCA X1;Pos Z", 500, -1, 1, 1000, -10, 10)

    hDcay1PosxFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcay1Posx","Dimuon Dca x1 - Pos X SEPM ;DCA X1;Pos X", 500, -1, 1, 1000, -0.1, 0.1)
    hDcay1PosyFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcay1Posy","Dimuon Dca x1 - Pos Y SEPM ;DCA X1;Pos Y", 500, -1, 1, 1000, -0.1, 0.1)
    hDcay1PoszFullPM = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcay1Posz","Dimuon Dca x1 - Pos Z SEPM ;DCA X1;Pos Z", 500, -1, 1, 1000, -10, 10)

    hDcax1FullPlus = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcax1_plus","Dimuon Dca x1 Plus ;DCA X1;#", 500, -1, 1)
    hDcax1FullMinus = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcax1_minus","Dimuon Dca x1 Minus ;DCA X1;#", 500, -1, 1)
    hDcax2FullPlus = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcax2_plus","Dimuon Dca x2 Plus ;DCA X2;#", 500, -1, 1)
    hDcax2FullMinus = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcax2_minus","Dimuon Dca x2 Minus ;DCA X2;#", 500, -1, 1)

    hDcay1FullPlus = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcay1_plus","Dimuon Dca y1 Plus ;DCA Y1;#", 500, -1, 1)
    hDcay1FullMinus = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcay1_minus","Dimuon Dca y1 Minus ;DCA Y1;#", 500, -1, 1)
    hDcay2FullPlus = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcay2_plus","Dimuon Dca y2 Plus ;DCA Y2;#", 500, -1, 1)
    hDcay2FullMinus = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcay2_minus","Dimuon Dca y2 Minus ;DCA Y2;#", 500, -1, 1)

    hDcaxy1FullPM = ROOT.TH1F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcaxy1","Dimuon DCA xy1 SEPM ;DCA_{xy};#", 1000, 0, 5)
    hDcaxy2FullPM = ROOT.TH1F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_Dcaxy2","Dimuon DCA xy2 SEPM ;DCA_{xy};#", 1000, 0, 5)

    hDcax1FullPhiR1 = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcax1_phiR1","Dimuon Dca x1 phi R1 ;DCA X1;#", 500, -1, 1)
    hDcax1FullPhiR2 = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcax1_phiR2","Dimuon Dca x1 phi R2 ;DCA X1;#", 500, -1, 1)
    hDcax1FullPhiR3 = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcax1_phiR3","Dimuon Dca x1 phi R3 ;DCA X1;#", 500, -1, 1)
    hDcax1FullPhiR4 = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcax1_phiR4","Dimuon Dca x1 phi R4 ;DCA X1;#", 500, -1, 1)

    hDcay1FullPhiR1 = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcay1_phiR1","Dimuon Dca y1 phi R1 ;DCA Y1;#", 500, -1, 1)
    hDcay1FullPhiR2 = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcay1_phiR2","Dimuon Dca y1 phi R2 ;DCA Y1;#", 500, -1, 1)
    hDcay1FullPhiR3 = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcay1_phiR3","Dimuon Dca y1 phi R3 ;DCA Y1;#", 500, -1, 1)
    hDcay1FullPhiR4 = ROOT.TH1F("LHC23_full_PairsMuonSEMM_matchedQualityCuts_Dcay1_phiR4","Dimuon Dca y1 phi R4 ;DCA Y1;#", 500, -1, 1)

    hDiskMap1 = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_DiskMap1","-#pi < #varphi < -#pi/2 ;X (cm);Y (cm)", 200, -20, 20, 200, -20, 20)
    hDiskMap2 = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_DiskMap2","-#pi/2 < #varphi < 0 ;X (cm);Y (cm)", 200, -20, 20, 200, -20, 20)
    hDiskMap3 = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_DiskMap3","0 < #varphi < #pi/2 ;X (cm);Y (cm)", 200, -20, 20, 200, -20, 20)
    hDiskMap4 = ROOT.TH2F("LHC23_full_PairsMuonSEPM_matchedQualityCuts_DiskMap4","#pi/2 < #varphi < #pi ;X (cm);Y (cm)", 200, -20, 20, 200, -20, 20)

    fOut = TFile(fOutName, "RECREATE")
    for i_fInName, fInName in enumerate(fInNames):
        print(f'Processing {fInName} ...')
        fIn = ROOT.TFile.Open(fInName)
        
        # Prepare histograms
        hMassPM = ROOT.TH1F(f'{labels[i_fInName]}_PairsMuonSEPM_matchedQualityCuts_Mass',"Dimuon mass SEPM ;m (GeV/c^2);#", 100, 2, 5)
        hMassPP = ROOT.TH1F(f'{labels[i_fInName]}_PairsMuonSEPP_matchedQualityCuts_Mass',"Dimuon mass SEPP ;m (GeV/c^2);#", 100, 2, 5)
        hMassMM = ROOT.TH1F(f'{labels[i_fInName]}_PairsMuonSEMM_matchedQualityCuts_Mass',"Dimuon mass SEMM ;m (GeV/c^2);#", 100, 2, 5)
        hTauzPM = ROOT.TH1F(f'{labels[i_fInName]}_PairsMuonSEPM_matchedQualityCuts_Tauz',"Dimuon tauz SEPM ;m (GeV/c^2);#", 1000, -0.1, 0.1)
        hTauzPP = ROOT.TH1F(f'{labels[i_fInName]}_PairsMuonSEPP_matchedQualityCuts_Tauz',"Dimuon tauz SEPM ;m (GeV/c^2);#", 1000, -0.1, 0.1)
        hTauzMM = ROOT.TH1F(f'{labels[i_fInName]}_PairsMuonSEMM_matchedQualityCuts_Tauz',"Dimuon tauz SEPM ;m (GeV/c^2);#", 1000, -0.1, 0.1)

        accumulatedData = {
            'fPosX': [],
            'fPosY': [],
            'fPosZ': [],
            'fMass': [],
            'fTauz': [],
            'fTauxy': [],
            'fSign': [],
            'fSign1': [],
            'fSign2': [],
            'fEta': [],
            'fEta1': [],
            'fEta2': [],
            'fPhi': [],
            'fPhi1': [],
            'fPhi2': [],
            'fPt': [],
            'fPt1': [],
            'fPt2': [],
            'fFwdDcaX1': [],
            'fFwdDcaX2': [],
            'fFwdDcaY1': [],
            'fFwdDcaY2': [],
            'fChi2MatchMCHMFT1': [],
            'fChi2MatchMCHMFT2': [],
        }

        for key in fIn.GetListOfKeys():
            dirName = key.GetName()
            if dirName == "parentFiles":
                continue
            if key.IsFolder():
                print(dirName)
                tree = fIn.Get(f'{dirName}/O2rtdimuonall')
                rdf = ROOT.RDataFrame(tree).Filter(cuts)

                data = rdf.AsNumpy(columns=["fPosX", "fPosY", "fPosZ", "fMass", "fTauz", "fTauxy", "fSign", "fSign1", "fSign2", "fEta", "fEta1", "fEta2", "fPhi", "fPhi1", "fPhi2", "fPt", "fPt1", "fPt2", "fFwdDcaX1", "fFwdDcaX2", "fFwdDcaY1", "fFwdDcaY2", "fChi2MatchMCHMFT1", "fChi2MatchMCHMFT2"])
                accumulatedData['fPosX'].extend(data["fPosX"])
                accumulatedData['fPosY'].extend(data["fPosY"])
                accumulatedData['fPosZ'].extend(data["fPosZ"])
                accumulatedData['fMass'].extend(data["fMass"])
                accumulatedData['fTauz'].extend(data["fTauz"])
                accumulatedData['fTauxy'].extend(data["fTauxy"])
                accumulatedData['fSign'].extend(data["fSign"])
                accumulatedData['fSign1'].extend(data["fSign1"])
                accumulatedData['fSign2'].extend(data["fSign2"])
                accumulatedData['fEta'].extend(data["fEta"])
                accumulatedData['fEta1'].extend(data["fEta1"])
                accumulatedData['fEta2'].extend(data["fEta2"])
                accumulatedData['fPhi'].extend(data["fPhi"])
                accumulatedData['fPhi1'].extend(data["fPhi1"])
                accumulatedData['fPhi2'].extend(data["fPhi2"])
                accumulatedData['fPt'].extend(data["fPt"])
                accumulatedData['fPt1'].extend(data["fPt1"])
                accumulatedData['fPt2'].extend(data["fPt2"])
                accumulatedData['fFwdDcaX1'].extend(data["fFwdDcaX1"])
                accumulatedData['fFwdDcaX2'].extend(data["fFwdDcaX2"])
                accumulatedData['fFwdDcaY1'].extend(data["fFwdDcaY1"])
                accumulatedData['fFwdDcaY2'].extend(data["fFwdDcaY2"])
                accumulatedData['fChi2MatchMCHMFT1'].extend(data["fChi2MatchMCHMFT1"])
                accumulatedData['fChi2MatchMCHMFT2'].extend(data["fChi2MatchMCHMFT2"])

        for posx, posy, posz, mass, tauz, tauxy, sign, sign1, sign2, eta, eta1, eta2, phi, phi1, phi2, pt, pt1, pt2, dcax1, dcax2, dcay1, dcay2, chi2mchmft1, chi2mchmft2 in zip(
            accumulatedData['fPosX'], 
            accumulatedData['fPosY'], 
            accumulatedData['fPosZ'], 
            accumulatedData['fMass'], 
            accumulatedData['fTauz'], 
            accumulatedData['fTauxy'], 
            accumulatedData['fSign'], 
            accumulatedData['fSign1'], 
            accumulatedData['fSign2'], 
            accumulatedData['fEta'], 
            accumulatedData['fEta1'], 
            accumulatedData['fEta2'], 
            accumulatedData['fPhi'], 
            accumulatedData['fPhi1'], 
            accumulatedData['fPhi2'], 
            accumulatedData['fPt'], 
            accumulatedData['fPt1'], 
            accumulatedData['fPt2'], 
            accumulatedData['fFwdDcaX1'], 
            accumulatedData['fFwdDcaX2'], 
            accumulatedData['fFwdDcaY1'], 
            accumulatedData['fFwdDcaY2'],
            accumulatedData['fChi2MatchMCHMFT1'], 
            accumulatedData['fChi2MatchMCHMFT2']):
                if sign == 0:
                    hMassPM.Fill(mass)
                    hTauzPM.Fill(tauz)
                    hMassFullPM.Fill(mass)
                    hTauzFullPM.Fill(tauz)
                    hTauxyFullPM.Fill(tauxy)
                    hEtaPhiFullPM.Fill(eta, phi)
                    hMassPtFullPM.Fill(mass, pt)
                    hDcax1Dcax2FullPM.Fill(dcax1, dcax2)
                    hDcay1Dcay2FullPM.Fill(dcay1, dcay2)
                    hDcax1Dcay1FullPM.Fill(dcax1, dcay1)
                    hDcax2Dcay2FullPM.Fill(dcax2, dcay2)
                    hDcaxy1FullPM.Fill(math.sqrt(dcax1 * dcax1 + dcay1 * dcay1))
                    hDcaxy2FullPM.Fill(math.sqrt(dcax2 * dcax2 + dcay2 * dcay2))
                    if sign1 > 0: 
                        hDcax1FullPlus.Fill(dcax1)
                        hDcay1FullPlus.Fill(dcay1)
                    if sign2 > 0:
                        hDcax2FullPlus.Fill(dcax2)
                        hDcay2FullPlus.Fill(dcay2)
                    if sign1 < 0: 
                        hDcax1FullMinus.Fill(dcax1)
                        hDcay1FullMinus.Fill(dcay1)
                    if sign2 < 0:
                        hDcax2FullMinus.Fill(dcax2)
                        hDcay2FullMinus.Fill(dcay2)
                    hDcax1MassFullPM.Fill(dcax1, mass)
                    hDcax2MassFullPM.Fill(dcax2, mass)
                    hDcay1MassFullPM.Fill(dcay1, mass)
                    hDcay2MassFullPM.Fill(dcay2, mass)

                    hDcax1Pt1FullPM.Fill(dcax1, pt1)
                    hDcax2Pt2FullPM.Fill(dcax2, pt2)
                    hDcay1Pt1FullPM.Fill(dcay1, pt1)
                    hDcay2Pt2FullPM.Fill(dcay2, pt2)

                    hDcax1PosxFullPM.Fill(dcax1, posx)
                    hDcax1PosyFullPM.Fill(dcax1, posy)
                    hDcax1PoszFullPM.Fill(dcax1, posz)
                    hDcay1PosxFullPM.Fill(dcay1, posx)
                    hDcay1PosyFullPM.Fill(dcay1, posy)
                    hDcay1PoszFullPM.Fill(dcay1, posz)

                    hDcax1PhiFullPM.Fill(dcax1, phi1)
                    hDcay1PhiFullPM.Fill(dcay1, phi1)
                    hDcax1Chi2MatchMCHMFTFullPM.Fill(dcax1, chi2mchmft1)
                    hDcay1Chi2MatchMCHMFTFullPM.Fill(dcay1, chi2mchmft1)
                    hDcax1EtaFullPM.Fill(dcax1, eta1)
                    hDcay1EtaFullPM.Fill(dcay1, eta1)

                    if (phi1 >= -gPi and phi1 < -gPi2):
                        hDcax1FullPhiR1.Fill(dcax1)
                        hDcay1FullPhiR1.Fill(dcay1)
                        hDiskMap1.Fill(math.cos(phi1), math.sin(phi1))
                    if (phi1 >= -gPi2 and phi1 < 0):
                        hDcax1FullPhiR2.Fill(dcax1)
                        hDcay1FullPhiR2.Fill(dcay1)
                        hDiskMap2.Fill(math.cos(phi1), math.sin(phi1))
                    if (phi1 >= 0 and phi1 < gPi2):
                        hDcax1FullPhiR3.Fill(dcax1)
                        hDcay1FullPhiR3.Fill(dcay1)
                        hDiskMap3.Fill(math.cos(phi1), math.sin(phi1))
                    if (phi1 >= gPi2 and phi1 < gPi):
                        hDcax1FullPhiR4.Fill(dcax1)
                        hDcay1FullPhiR4.Fill(dcay1)
                        hDiskMap4.Fill(math.cos(phi1), math.sin(phi1))


                if sign > 0:
                    hMassPP.Fill(mass)
                    hTauzPP.Fill(tauz)
                    hMassFullPP.Fill(mass)
                    hTauzFullPP.Fill(tauz)
                    hTauxyFullPP.Fill(tauxy)
                    hDcax1Dcax2FullPP.Fill(dcax1, dcax2)
                    hDcay1Dcay2FullPP.Fill(dcay1, dcay2)
                if sign < 0:
                    hMassMM.Fill(mass)
                    hTauzMM.Fill(tauz)
                    hMassFullMM.Fill(mass)
                    hTauzFullMM.Fill(tauz)
                    hTauxyFullMM.Fill(tauxy)
                    hDcax1Dcax2FullMM.Fill(dcax1, dcax2)
                    hDcay1Dcay2FullMM.Fill(dcay1, dcay2)

        fOut.cd()
        hMassPM.Write()
        hTauzPM.Write()
        hMassPP.Write()
        hTauzPP.Write()
        hMassMM.Write()
        hTauzMM.Write()

        fIn.Close()

    fOut.cd()
    hMassFullPM.Write()
    hTauzFullPM.Write()
    hMassFullPP.Write()
    hTauzFullPP.Write()
    hMassFullMM.Write()
    hTauzFullMM.Write()
    hTauxyFullPM.Write()
    hTauxyFullPP.Write()
    hTauxyFullMM.Write()
    hEtaPhiFullPM.Write()
    hMassPtFullPM.Write()
    hDcax1Dcax2FullPM.Write()
    hDcay1Dcay2FullPM.Write()
    hDcax1Dcax2FullPP.Write()
    hDcay1Dcay2FullPP.Write()
    hDcax1Dcax2FullMM.Write()
    hDcay1Dcay2FullMM.Write()
    hDcax1Dcay1FullPM.Write()
    hDcax2Dcay2FullPM.Write()
    hDcaxy1FullPM.Write()
    hDcaxy2FullPM.Write()
    hDcax1FullPlus.Write()
    hDcay1FullPlus.Write()
    hDcax2FullPlus.Write()
    hDcay2FullPlus.Write()
    hDcax1FullMinus.Write()
    hDcay1FullMinus.Write()
    hDcax2FullMinus.Write()
    hDcay2FullMinus.Write()
    hDcax1MassFullPM.Write()
    hDcax2MassFullPM.Write()
    hDcay1MassFullPM.Write()
    hDcay2MassFullPM.Write()
    hDcax1Pt1FullPM.Write()
    hDcax2Pt2FullPM.Write()
    hDcay1Pt1FullPM.Write()
    hDcay2Pt2FullPM.Write()
    hDcax1PosxFullPM.Write()
    hDcax1PosyFullPM.Write()
    hDcax1PoszFullPM.Write()
    hDcay1PosxFullPM.Write()
    hDcay1PosyFullPM.Write()
    hDcay1PoszFullPM.Write()
    hDcax1PhiFullPM.Write()
    hDcay1PhiFullPM.Write()
    hDcax1EtaFullPM.Write()
    hDcay1EtaFullPM.Write()
    hDcax1FullPhiR1.Write()
    hDcay1FullPhiR1.Write()
    hDcax1FullPhiR2.Write()
    hDcay1FullPhiR2.Write()
    hDcax1FullPhiR3.Write()
    hDcay1FullPhiR3.Write()
    hDcax1FullPhiR4.Write()
    hDcay1FullPhiR4.Write()
    hDiskMap1.Write()
    hDiskMap2.Write()
    hDiskMap3.Write()
    hDiskMap4.Write()
    hDcax1Chi2MatchMCHMFTFullPM.Write()
    hDcay1Chi2MatchMCHMFTFullPM.Write()
    fOut.Close()



def main():
    parser = argparse.ArgumentParser(description='Arguments to pass')
    parser.add_argument('cfgFileName', metavar='text', default='config.yml', help='config file name')
    parser.add_argument("--do_qc", help="Do simple QC", action="store_true")
    parser.add_argument("--do_analysis", help="Do simple anaysis", action="store_true")
    parser.add_argument("--do_process_tree", help="Process the AO2D tree with dimuon flat tables", action="store_true")
    args = parser.parse_args()

    print('Loading task configuration: ...', end='\r')
    with open(args.cfgFileName, 'r') as ymlCfgFile:
        inputCfg = yaml.load(ymlCfgFile, yaml.FullLoader)
    print('Loading task configuration: Done!')

    if args.do_qc:
        qc(inputCfg)

    if args.do_analysis:
        analysis(inputCfg)

    if args.do_process_tree:
        process_tree(inputCfg)

main()