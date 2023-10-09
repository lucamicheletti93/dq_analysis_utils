import os
import sys
import yaml
import numpy as np
import argparse
import ROOT
from ROOT import *
sys.path.append('../../dq_fit_library/utils')
from plot_library import LoadStyle, SetGraStat, SetGraSyst, SetLegend

def qc(inputCfg):
    #gStyle.SetPalette(ROOT.kRainBow)

    fInNames = inputCfg["inputs"]["data"]
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

    for i_fInName, fInName in enumerate(fInNames):
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

    for i_selName, selName in enumerate(selNames):
        for i_varName, varName in enumerate(varNames):
            canvas = TCanvas(f'canvas_{selName}_{varName}', f'canvas_{selName}_{varName}', 600, 600)
            gPad.SetLogy(1)
            for i_fInName, fInName in enumerate(fInNames):
                histsMS[i_fInName][i_selName][i_varName].Draw("H SAME")
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
                    sigmaJpsi = ROOT.RooRealVar("sigmaJpsi", "sigmaJpsi", 0.095)
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

                    legendFit = ROOT.TLegend(0.65, 0.55, 0.85, 0.65)
                    SetLegend(legendFit)
                    legendFit.AddEntry(mJpsiframe.findObject("Sig"), "J/#psi", "L")
                    legendFit.AddEntry(mJpsiframe.findObject("Bkg"), "Bkg", "L")
                    legendFit.Draw()

                    letexTitle.DrawLatex(0.35, 0.88, "ALICE, Pb#minusPb, #sqrt{#it{s}_{NN}} = 5.36 TeV")
                    letexTitle.DrawLatex(0.35, 0.81, "Inclusive J/#psi #rightarrow #mu^{+}#mu^{-}, 2.5 < #it{y} < 4")
                    letexTitle.DrawLatex(0.55, 0.74, "#it{N}_{J/#psi} = %1.0f #pm %1.0f" % (nSigJpsi.getVal(), nSigJpsi.getError()))
                    letexTitle.DrawLatex(0.55, 0.68, "#it{#mu}_{J/#psi} = %4.3f #pm %4.3f" % (meanJpsi.getVal(), meanJpsi.getError()))
                    canvasFit.SaveAs(f'plots/analysis/fit_{dataset}_{selName}.pdf')

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
                          
                canvasCombBkg.SaveAs(f'plots/analysis/combBkg_{dataset}_{selName}.pdf')

def main():
    parser = argparse.ArgumentParser(description='Arguments to pass')
    parser.add_argument('cfgFileName', metavar='text', default='config.yml', help='config file name')
    parser.add_argument("--do_qc", help="Do simple QC", action="store_true")
    parser.add_argument("--do_analysis", help="Do simple anaysis", action="store_true")
    args = parser.parse_args()

    print('Loading task configuration: ...', end='\r')
    with open(args.cfgFileName, 'r') as ymlCfgFile:
        inputCfg = yaml.load(ymlCfgFile, yaml.FullLoader)
    print('Loading task configuration: Done!')

    if args.do_qc:
        qc(inputCfg)

    if args.do_analysis:
        analysis(inputCfg)

main()