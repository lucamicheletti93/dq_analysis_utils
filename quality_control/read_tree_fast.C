#if !defined(CLING) || defined(ROOTCLING)

#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>

#include "TSystemDirectory.h"
#include <TLorentzVector.h>
#include "TCanvas.h"
#include "TFile.h"
#include "TH1F.h"
#include "TH2D.h"
#include "TH1D.h"
#include "TF1.h"
#include "TMath.h"
#include "TFile.h"
#include "TString.h"
#include "TTree.h"
#include "TLegend.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TKey.h"
#include "THashList.h"
#include "TProfile.h"
#include "TTreeReader.h"
#include "TLine.h"
#include <ROOT/RDataFrame.hxx>

#endif

void read_tree_fast() {
    float fMass, fPt, fEta, fTauz, fTauxy, fU2Q2, fCos2DeltaPhi, fR2EP, fR2SP = -99999;
    int fSign = -99999;

    const int nMassBins = 100;
    const double minMassRange = 0;
    const double maxMassRange = 5;

    TLine *lineJpsi = new TLine(3.096, 1, 3.096, 1e5);
    lineJpsi -> SetLineStyle(kDashed);
    lineJpsi -> SetLineColor(kRed+1);
    lineJpsi -> SetLineWidth(2);

    TH1F *histMass = new TH1F("histMass", "", nMassBins, minMassRange, maxMassRange);
    TH1F *histU2Q2 = new TH1F("histU2Q2", "", nMassBins, minMassRange, maxMassRange);
    TH1F *histR2SP = new TH1F("histR2SP", "", nMassBins, minMassRange, maxMassRange);

    TH2F *histMassU2Q2 = new TH2F("histMassU2Q2", "", nMassBins, minMassRange, maxMassRange, 30, -10, 10);
    TH2F *histMassR2EP = new TH2F("histMassR2EP", "", nMassBins, minMassRange, maxMassRange, 30, -10, 10);
    TH2F *histMassC2DP = new TH2F("histMassC2DP", "", nMassBins, minMassRange, maxMassRange, 30, -10, 10);
    TH2F *histMassR2SP = new TH2F("histMassR2SP", "", nMassBins, minMassRange, maxMassRange, 30, -10, 10);

    string pathToFile = "/Users/lucamicheletti/cernbox/JPSI/Run3/2023/PbPb/pass1/AO2D_reduced_with_flow.root";
    TFile *fIn = new TFile(pathToFile.c_str(), "READ");
    TIter next(fIn -> GetListOfKeys()); 
    TKey *key; 
    while ((key = (TKey*) next())) { 
        TString dirName = key -> GetName();
        if (!dirName.Contains("DF_")) {
            continue;
        }

        TTree *tree = (TTree*) fIn -> Get(Form("%s/O2rtdimuonall", dirName.Data()));
        tree -> SetBranchAddress("fMass", &fMass);
        tree -> SetBranchAddress("fPt", &fPt);
        tree -> SetBranchAddress("fEta", &fEta);
        tree -> SetBranchAddress("fSign", &fSign);
        tree -> SetBranchAddress("fTauz", &fTauz);
        tree -> SetBranchAddress("fTauxy", &fTauxy);
        tree -> SetBranchAddress("fU2Q2", &fU2Q2);
        tree -> SetBranchAddress("fCos2DeltaPhi", &fCos2DeltaPhi);
        tree -> SetBranchAddress("fR2EP", &fR2EP);
        tree -> SetBranchAddress("fR2SP", &fR2SP);


        for (int iEntry = 0;iEntry < tree -> GetEntries();iEntry++) {
            tree -> GetEntry(iEntry);
            if (fSign == 0 && TMath::Abs(fEta) > 2.5 && TMath::Abs(fEta) < 4) {
                histMassU2Q2 -> Fill(fMass, fU2Q2);
                histMassR2EP -> Fill(fMass, fR2EP);
                histMassC2DP -> Fill(fMass, fCos2DeltaPhi);
                histMassR2SP -> Fill(fMass, fR2SP);
            }
        }
    }
    fIn -> Close();

    TCanvas *canvasMassU2Q2 = new TCanvas("canvasMassU2Q2", "", 600, 600);
    histMassU2Q2 -> Draw("COLZ");

    TCanvas *canvasMassR2EP = new TCanvas("canvasMassR2EP", "", 600, 600);
    histMassR2EP -> Draw("COLZ");

    TCanvas *canvasMassC2DP = new TCanvas("canvasMassC2DP", "", 600, 600);
    histMassC2DP -> Draw("COLZ");

    TCanvas *canvasMassR2SP = new TCanvas("canvasMassR2SP", "", 600, 600);
    histMassR2SP -> Draw("COLZ");

    TH1F *histProjMass  = (TH1F*) histMassU2Q2 -> ProjectionX("histProjMass");

    TProfile *histProjU2Q2  = (TProfile*) histMassU2Q2 -> ProfileX("histProjU2Q2");
    TProfile *histProjR2SP  = (TProfile*) histMassR2SP -> ProfileX("histProjR2SP");

    TProfile *histProjC2DP  = (TProfile*) histMassC2DP -> ProfileX("histProjC2DP");
    TProfile *histProjR2EP  = (TProfile*) histMassR2EP -> ProfileX("histProjR2EP");

    // Compute v2 with SP
    TH1F *histV2SP = new TH1F("histV2SP", "", nMassBins, minMassRange, maxMassRange);
    TH1F *histV2EP = new TH1F("histV2EP", "", nMassBins, minMassRange, maxMassRange);
    for (int i = 0;i < nMassBins;i++) {
        // SP
        float u2q2 = histProjU2Q2 -> GetBinContent(i+1);
        float errU2q2 = histProjU2Q2 -> GetBinError(i+1);
        float r2sp = histProjR2SP -> GetBinContent(i+1);
        float errR2sp = histProjR2SP -> GetBinError(i+1);
        // EP
        float c2dp = histProjC2DP -> GetBinContent(i+1);
        float errC2dp = histProjC2DP -> GetBinError(i+1);
        float r2ep = histProjR2EP -> GetBinContent(i+1);
        float errR2ep = histProjR2EP -> GetBinError(i+1);

        if (r2sp == 0) {
            histV2SP -> SetBinContent(i+1, -999.);
            histV2SP -> SetBinError(i+1, -999.);
        } else {
            histV2SP -> SetBinContent(i+1, u2q2/r2sp);
            histV2SP -> SetBinError(i+1, TMath::Sqrt((errU2q2/u2q2)*(errU2q2/u2q2) + (errR2sp/r2sp)*(errR2sp/r2sp)));
        }

        if (r2ep == 0) {
            histV2EP -> SetBinContent(i+1, -999.);
            histV2EP -> SetBinError(i+1, -999.);
        } else {
            histV2EP -> SetBinContent(i+1, c2dp/r2ep);
            histV2EP -> SetBinError(i+1, TMath::Sqrt((errC2dp/c2dp)*(errC2dp/c2dp) + (errR2ep/r2ep)*(errR2ep/r2ep)));
        }  
    }

    TCanvas *canvasProfMassV2SP = new TCanvas("canvasProfMassV2SP", "", 1200, 1200);
    canvasProfMassV2SP -> Divide(2, 2);
    canvasProfMassV2SP -> cd(1);
    gPad -> SetLogy(1);
    histProjMass -> Draw("EP");
    lineJpsi -> Draw("SAME");
    canvasProfMassV2SP -> cd(2);
    histProjU2Q2 -> Draw("EP");
    canvasProfMassV2SP -> cd(3);
    histV2SP -> GetYaxis() -> SetRangeUser(-10, 10);
    histV2SP -> Draw("EP");
    lineJpsi -> Draw("SAME");
    canvasProfMassV2SP -> cd(4);
    histProjR2SP -> Draw("EP");

    TCanvas *canvasProfMassV2EP = new TCanvas("canvasProfMassV2EP", "", 1200, 1200);
    canvasProfMassV2EP -> Divide(2, 2);
    canvasProfMassV2EP -> cd(1);
    gPad -> SetLogy(1);
    histProjMass -> Draw("EP");
    lineJpsi -> Draw("SAME");
    canvasProfMassV2EP -> cd(2);
    histProjC2DP -> Draw("EP");
    canvasProfMassV2EP -> cd(3);
    histV2EP -> GetYaxis() -> SetRangeUser(-10, 10);
    histV2EP -> Draw("EP");
    lineJpsi -> Draw("SAME");
    canvasProfMassV2EP -> cd(4);
    histProjR2EP -> Draw("EP");


}