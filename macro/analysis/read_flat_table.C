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

#endif

std::vector<std::string> get_directories(const std::string& s) {
    std::vector<std::string> r;
    for(auto& p : std::filesystem::recursive_directory_iterator(s))
        if (p.is_directory())
            r.push_back(p.path().string());
    return r;
}

string path_to_data = "/Users/lucamicheletti/cernbox/JPSI/Run3/2022/apass3";

void read_flat_table(string period = "LHC22o_medium"){

    float fMass = 0;
    float fPt = 0;
    float fPt1 = 0;
    float fPt2 = 0;
    float fEta = 0;
    float fEta1 = 0;
    float fEta2 = 0;
    int fSign = 0;
    float fChi2MatchMCHMID1 = 0;
    float fChi2MatchMCHMID2 = 0;
    float fChi2MatchMCHMFT1 = 0;
    float fChi2MatchMCHMFT2 = 0;
    float fTauz = 0;
    float fTauxy = 0;
    int fIsAmbig1 = 0;
    int fIsAmbig2 = 0;

    double min_pt[] = {0, 1, 2, 3, 4, 5, 6, 7, 10};
    double max_pt[] = {1, 2, 3, 4, 5, 6, 7, 10, 20};

    const int size_pt = sizeof(min_pt) / sizeof(double);
    TH1F *hist_mass_vs_pt_PM[size_pt];
    TH1F *hist_mass_vs_pt_PP[size_pt];
    TH1F *hist_mass_vs_pt_MM[size_pt];
    for (int i = 0;i < size_pt;i++) {
        hist_mass_vs_pt_PM[i] = new TH1F(Form("hist_mass_pt_%1.0f_%1.0f", min_pt[i], max_pt[i]), Form("hist_mass_pt_%1.0f_%1.0f", min_pt[i], max_pt[i]), 100, 2, 5);
        hist_mass_vs_pt_PP[i] = new TH1F(Form("hist_mass_pt_%1.0f_%1.0f_PP", min_pt[i], max_pt[i]), Form("hist_mass_pt_%1.0f_%1.0f_PP", min_pt[i], max_pt[i]), 100, 2, 5);
        hist_mass_vs_pt_MM[i] = new TH1F(Form("hist_mass_pt_%1.0f_%1.0f_MM", min_pt[i], max_pt[i]), Form("hist_mass_pt_%1.0f_%1.0f_MM", min_pt[i], max_pt[i]), 100, 2, 5);
    }

    TH1F *hist_events = new TH1F("hist_events", "", 2, 0, 2);
    hist_events -> GetXaxis() -> SetBinLabel(1, "N ev. all.");
    hist_events -> GetXaxis() -> SetBinLabel(2, "N ev. acc.");

    TH1F *hist_mass = new TH1F("hist_mass", "Dimuons", 100, 2, 5); hist_mass -> SetLineColor(kBlack); hist_mass -> SetMinimum(0.1);
    TH1F *hist_full_mass = new TH1F("hist_full_mass", "Dimuons full mass", 500, 2, 12); hist_mass -> SetLineColor(kBlack); hist_mass -> SetMinimum(0.1);
    TH1F *hist_tauz = new TH1F("hist_tauz", "Dimuons tauz", 200, -1, 1); hist_tauz -> SetLineColor(kBlack); hist_tauz -> SetMinimum(0.1);
    TH1F *hist_tauxy = new TH1F("hist_tauxy", "Dimuons tauxy", 200, -1, 1); hist_tauxy -> SetLineColor(kBlack); hist_tauxy -> SetMinimum(0.1);
    TH1F *hist_mass_all_histo = new TH1F("hist_mass_all_histo", "Dimuons all histo", 750, 0, 15);
    TH1F *hist_mass_ambiguous = new TH1F("hist_mass_ambiguous", "Ambiguous", 100, 2, 5); hist_mass_ambiguous -> SetLineColor(kRed+1);
    TH1F *hist_mass_non_ambiguous = new TH1F("hist_mass_non_ambiguous", "Unambiguous", 100, 2, 5); hist_mass_non_ambiguous -> SetLineColor(kAzure+4);
    TH1F *hist_pt = new TH1F("hist_pt", "", 300, 0, 30);
    TH1F *hist_pt1 = new TH1F("hist_pt1", "", 300, 0, 30);
    TH1F *hist_pt2 = new TH1F("hist_pt2", "", 300, 0, 30);
    TH1F *hist_eta = new TH1F("hist_eta", "", 250, -5, 5);
    TH1F *hist_eta1 = new TH1F("hist_eta1", "", 250, -5, 5);
    TH1F *hist_eta2 = new TH1F("hist_eta2", "", 250, -5, 5);
    TH1F *hist_chi2MatchMCHMID1 = new TH1F("hist_chi2MatchMCHMID1", "", 250, 0, 100);
    TH1F *hist_chi2MatchMCHMID2 = new TH1F("hist_chi2MatchMCHMID2", "", 250, 0, 100);
    TH1F *hist_chi2MatchMCHMFT1 = new TH1F("hist_chi2MatchMCHMFT1", "", 250, 0, 100);
    TH1F *hist_chi2MatchMCHMFT2 = new TH1F("hist_chi2MatchMCHMFT2", "", 250, 0, 100);

    ifstream inFile;
    inFile.open(Form("/Users/lucamicheletti/cernbox/JPSI/Run3/2022/apass3/%s/run_list.txt", period.c_str()));

    vector <string> run_list;
    string tmp_run;
    while (inFile >> tmp_run) {
        run_list.push_back(tmp_run);
    }
    
    const int size_run_list = run_list.size();
    TH1F *hist_mass_run_by_run[size_run_list];

    int run_counter = 0;
    double coll_acc_counter = 0;
    double coll_all_counter = 0;
    for (auto& run : run_list) {
        std::cout << "Run = " << run << std::endl;
        std::vector<std::string> path_to_dir = get_directories(Form("%s/%s/%s", path_to_data.c_str(), period.c_str(), run.c_str()));
        hist_mass_run_by_run[run_counter] = new TH1F(Form("hist_mass_%s", run.c_str()), Form("hist_mass_%s", run.c_str()), 100, 2, 5); 
        hist_mass_run_by_run[run_counter] -> SetLineColor(kBlack);
        for (auto& path : path_to_dir) {

            string path_to_histo = Form("%s/AnalysisResults.root", path.c_str());
            TFile *fIn_histo = new TFile(path_to_histo.c_str(), "READ");
            TH1F *hist_coll_acc = (TH1F*) fIn_histo -> Get("event-selection-task/hColCounterAcc");
            coll_acc_counter += hist_coll_acc -> GetBinContent(1);
            std::cout << "N collisions = " << hist_coll_acc -> GetBinContent(1) << std::endl;
            TH1F *hist_coll_all = (TH1F*) fIn_histo -> Get("event-selection-task/hColCounterAll");
            coll_all_counter += hist_coll_all -> GetBinContent(1);
            THashList *hlist = (THashList*) fIn_histo -> Get("analysis-same-event-pairing/output");
            TList *list = (TList*) hlist -> FindObject("PairsMuonSEPM_matchedQualityCuts");
            TH1F *hist_mass_tmp = (TH1F*) list -> FindObject("Mass");
            hist_mass_all_histo -> Add(hist_mass_tmp);
            fIn_histo -> Close();

            string path_to_tree = Form("%s/AO2D.root", path.c_str());
            TFile *fIn_tree = new TFile(path_to_tree.c_str(), "READ");
            TIter next(fIn_tree -> GetListOfKeys()); 
            TKey *key; 
            while ((key = (TKey*) next())) { 
                TString dirName = key -> GetName();
                if (!dirName.Contains("DF_")) {
                    continue;
                }
                //key -> Print(); 
                TTree *tree = (TTree*) fIn_tree -> Get(Form("%s/O2rtdimuonall", dirName.Data()));
                tree -> SetBranchAddress("fMass", &fMass);
                tree -> SetBranchAddress("fPt", &fPt);
                tree -> SetBranchAddress("fPt1", &fPt1);
                tree -> SetBranchAddress("fPt2", &fPt2);
                tree -> SetBranchAddress("fEta", &fEta);
                tree -> SetBranchAddress("fEta1", &fEta1);
                tree -> SetBranchAddress("fEta2", &fEta2);
                tree -> SetBranchAddress("fSign", &fSign);
                tree -> SetBranchAddress("fTauz", &fTauz);
                tree -> SetBranchAddress("fTauxy", &fTauxy);
                tree -> SetBranchAddress("fChi2MatchMCHMID1", &fChi2MatchMCHMID1);
                tree -> SetBranchAddress("fChi2MatchMCHMID2", &fChi2MatchMCHMID2);
                tree -> SetBranchAddress("fChi2MatchMCHMFT1", &fChi2MatchMCHMFT1);
                tree -> SetBranchAddress("fChi2MatchMCHMFT2", &fChi2MatchMCHMFT2);
                tree -> SetBranchAddress("fIsAmbig1", &fIsAmbig1);
                tree -> SetBranchAddress("fIsAmbig2", &fIsAmbig2);
                
                //std::cout << tree -> GetEntries() << std::endl;

                for (int iEntry = 0;iEntry < tree -> GetEntries();iEntry++) {
                    tree -> GetEntry(iEntry);
                    //std::cout << fEta << " , " << fEta1 << " , " <<  fEta2 << " , " << fMass << std::endl;
                    //if (fPt < 1 || fPt > 3) continue;

                    if (fPt1 < 0.5 || fPt2 < 0.5) continue;
                    if (TMath::Abs(fEta) < 2.5 || TMath::Abs(fEta) > 4) continue;
                    if (TMath::Abs(fEta1) < 2.5 || TMath::Abs(fEta1) > 4) continue;
                    if (TMath::Abs(fEta2) < 2.5 || TMath::Abs(fEta2) > 4) continue;
                    if (fChi2MatchMCHMID1 > 15 || fChi2MatchMCHMID2 > 15) continue;
                    hist_full_mass -> Fill(fMass);
                    if (fChi2MatchMCHMFT1 > 45 || fChi2MatchMCHMFT2 > 45) continue;
                    if (fSign == 0) {
                        hist_mass_run_by_run[run_counter] -> Fill(fMass);
                        hist_mass -> Fill(fMass);
                        if (fMass > 2.9 && fMass < 3.3) {
                            hist_tauz -> Fill(fTauz);
                            hist_tauxy -> Fill(fTauxy);
                        }
                        hist_pt -> Fill(fPt);
                        hist_pt1 -> Fill(fPt1);
                        hist_pt2 -> Fill(fPt2);
                        hist_eta -> Fill(fEta);
                        hist_eta1 -> Fill(fEta1);
                        hist_eta2 -> Fill(fEta2);
                        hist_chi2MatchMCHMID1 -> Fill(fChi2MatchMCHMID1);
                        hist_chi2MatchMCHMID1 -> Fill(fChi2MatchMCHMID2);
                        if (fIsAmbig1 == 1 || fIsAmbig2 == 1) {
                            hist_mass_ambiguous -> Fill(fMass);
                        }
                        if (fIsAmbig1 == 0 && fIsAmbig2 == 0) {
                            hist_mass_non_ambiguous -> Fill(fMass);
                        }

                        for (int iPt = 0;iPt < size_pt;iPt++) {
                            if (fPt > min_pt[iPt] && fPt < max_pt[iPt]) {
                                hist_mass_vs_pt_PM[iPt] -> Fill(fMass);
                                break;
                            }
                        }
                    } 
                    if (fSign > 0) {
                        for (int iPt = 0;iPt < size_pt;iPt++) {
                            if (fPt > min_pt[iPt] && fPt < max_pt[iPt]) {
                                hist_mass_vs_pt_PP[iPt] -> Fill(fMass);
                                break;
                            }
                        }
                    }
                    if (fSign < 0) {
                        for (int iPt = 0;iPt < size_pt;iPt++) {
                            if (fPt > min_pt[iPt] && fPt < max_pt[iPt]) {
                                hist_mass_vs_pt_MM[iPt] -> Fill(fMass);
                                break;
                            }
                        }
                    }
                    
                }
            }
            fIn_tree -> Close();
        }
        run_counter++;
    }
    
    TCanvas *canvas_run_by_run = new TCanvas("canvas_run_by_run", "", 800, 600);
    gPad -> SetLogy(1);
    hist_mass -> Draw("H");
    for (int i = 0;i < size_run_list;i++) {
        hist_mass_run_by_run[i] -> Draw("H SAME PLC");
    }
    gPad -> BuildLegend(0.78, 0.65, 0.980, 0.935, "", "L");

    TCanvas *canvas_var = new TCanvas("canvas_var", "", 1800, 1200);
    canvas_var -> Divide(3, 2);
    canvas_var -> cd(1); hist_eta -> Draw("H");
    canvas_var -> cd(2); hist_eta1 -> Draw("H");
    canvas_var -> cd(3); hist_eta2 -> Draw("H");
    canvas_var -> cd(4); gPad -> SetLogy(1); hist_chi2MatchMCHMID1 -> Draw("H");
    canvas_var -> cd(5); gPad -> SetLogy(1); hist_chi2MatchMCHMID1 -> Draw("H");

    TCanvas *canvas_mass = new TCanvas("canvas_mass", "", 800, 600);
    gPad -> SetLogy(1);
    hist_mass -> Draw("EP");
    hist_mass_ambiguous -> Draw("EPsame");
    hist_mass_non_ambiguous -> Draw("EPsame");
    gPad -> BuildLegend(0.78, 0.65, 0.980, 0.935, "", "L");

    std::cout << "Total number of events (Acc) = " << coll_acc_counter << std::endl;
    std::cout << "Total number of events (All) = " << coll_all_counter << std::endl;
    hist_events -> SetBinContent(1, coll_all_counter);
    hist_events -> SetBinContent(2, coll_acc_counter);

    TFile *fOut = new TFile(Form("%s/%s/histograms.root", path_to_data.c_str(), period.c_str()), "RECREATE");
    fOut -> cd();
    hist_events -> Write();
    hist_full_mass -> Write();
    hist_mass -> Write();
    hist_tauz -> Write();
    hist_tauxy -> Write();
    hist_mass_all_histo -> Write();
    for (int i = 0;i < size_run_list;i++) {
        hist_mass_run_by_run[i] -> Write();
    }
    for (int i = 0;i < size_pt;i++) {
        hist_mass_vs_pt_PM[i] -> Write();
        hist_mass_vs_pt_PP[i] -> Write();
        hist_mass_vs_pt_MM[i] -> Write();
    }
    fOut -> Close();
    inFile.close();
}


void read_analysis_results(string period = "LHC22o_medium") {
    const int n_cuts = 2;
    string cuts[] = {"PairsMuonSEPM_matchedMchMid", "PairsMuonSEPM_matchedQualityCuts"};
    const int n_pt_bins = 7;
    double pt_bin_min[] = {0, 1, 2, 3, 5, 7, 10};
    double pt_bin_max[] = {1, 2, 3, 5, 7, 10, 20};

    TH1F *hist_mass_all_histo[n_cuts];
    TH2F *hist_mass_pt_all_histo[n_cuts];

    for (int i = 0;i < n_cuts;i++) {
        hist_mass_all_histo[i] = new TH1F(Form("hist_mass_all_histo_%s", cuts[i].c_str()), Form("hist_mass_all_histo_%s", cuts[i].c_str()), 750, 0, 15);
        hist_mass_pt_all_histo[i] = new TH2F(Form("hist_mass_pt_all_histo_%s", cuts[i].c_str()), Form("hist_mass_pt_all_histo_%s", cuts[i].c_str()), 750, 0, 15, 120, 0, 30);
    }

    ifstream inFile;
    inFile.open(Form("/Users/lucamicheletti/cernbox/JPSI/Run3/2022/apass3/%s/run_list.txt", period.c_str()));

    vector <string> run_list;
    string tmp_run;
    while (inFile >> tmp_run) {
        run_list.push_back(tmp_run);
    }
    
    const int size_run_list = run_list.size();

    int run_counter = 0;
    double coll_acc_counter = 0;
    double coll_all_counter = 0;
    for (auto& run : run_list) {
        std::cout << "Run = " << run << std::endl;
        std::vector<std::string> path_to_dir = get_directories(Form("%s/%s/%s", path_to_data.c_str(), period.c_str(), run.c_str()));
        for (auto& path : path_to_dir) {
            string path_to_histo = Form("%s/AnalysisResults.root", path.c_str());
            TFile *fIn_histo = new TFile(path_to_histo.c_str(), "READ");
            TH1F *hist_coll_acc = (TH1F*) fIn_histo -> Get("event-selection-task/hColCounterAcc");
            coll_acc_counter += hist_coll_acc -> GetBinContent(1);
            std::cout << "N collisions = " << hist_coll_acc -> GetBinContent(1) << std::endl;
            TH1F *hist_coll_all = (TH1F*) fIn_histo -> Get("event-selection-task/hColCounterAll");
            coll_all_counter += hist_coll_all -> GetBinContent(1);
            THashList *hlist = (THashList*) fIn_histo -> Get("analysis-same-event-pairing/output");

            int index = 0;
            for (auto& cut : cuts) {
                TList *list = (TList*) hlist -> FindObject(cut.c_str());
                TH1F *hist_mass_tmp = (TH1F*) list -> FindObject("Mass");
                hist_mass_all_histo[index] -> Add(hist_mass_tmp);
                TH2F *hist_mass_pt_tmp = (TH2F*) list -> FindObject("Mass_Pt");
                hist_mass_pt_all_histo[index] -> Add(hist_mass_pt_tmp);
                index++;
            }
            
            fIn_histo -> Close();
        }
    }

    // pt cuts for differential studies
    TH1F *hist_mass_pt_all_histo_proj[n_cuts][n_pt_bins];

    for (int i = 0;i < n_cuts;i++) {
        for (int j = 0;j < n_pt_bins;j++) {
            int tmp_pt_bin_min = hist_mass_pt_all_histo[i] -> GetYaxis() -> FindBin(pt_bin_min[j]);
            int tmp_pt_bin_max = hist_mass_pt_all_histo[i] -> GetYaxis() -> FindBin(pt_bin_max[j]);
            if (tmp_pt_bin_max > 1) {
                tmp_pt_bin_max = tmp_pt_bin_max - 1;
            }
            hist_mass_pt_all_histo_proj[i][j] = (TH1F*) hist_mass_pt_all_histo[i] -> ProjectionX(Form("hist_mass_pt_all_histo_%s_pt_%1.0f_%1.0f", cuts[i].c_str(), pt_bin_min[j], pt_bin_max[j]), tmp_pt_bin_min, tmp_pt_bin_max);
        }
    }

    TFile *fOut = new TFile(Form("%s/%s/AnalysisResultsHistograms.root", path_to_data.c_str(), period.c_str()), "RECREATE");
    for (int i = 0;i < n_cuts;i++) {
        hist_mass_all_histo[i] -> Write();
        hist_mass_pt_all_histo[i] -> Write();
        for (int j = 0;j < n_pt_bins;j++) {
            hist_mass_pt_all_histo_proj[i][j] -> Write();
        }
    }
    fOut -> ls();
    fOut -> Close();
}


void read_reduced_data_table(string period = "LHC22o_medium"){

    gStyle -> SetPalette(kBlueRedYellow);
    if (std::filesystem::exists("chi2_studies.root")) {
        TFile *fIn = new TFile("chi2_studies.root", "READ");
        TH2F *hist_chi2_chi2MatchMCHMFT = (TH2F*) fIn -> Get("hist_chi2_chi2MatchMCHMFT");

        TH1F *histProj_chi2 = (TH1F*) hist_chi2_chi2MatchMCHMFT -> ProjectionX("histProj_chi2", 0, -1);
        TH1F *histProj_chi2MatchMCHMFT = (TH1F*) hist_chi2_chi2MatchMCHMFT -> ProjectionY("histProj_chi2MatchMCHMFT", 0, -1);

        vector <float> cuts_chi2MatchMCHMFT = {1, 2, 10, 45};
        int index = 0;
        TH1F *histProj_chi2_cuts[cuts_chi2MatchMCHMFT.size()];
        for (auto& cut : cuts_chi2MatchMCHMFT) {
            int cut_bin = (hist_chi2_chi2MatchMCHMFT -> GetYaxis() -> FindBin(cut)) - 1;
            histProj_chi2_cuts[index] = (TH1F*) hist_chi2_chi2MatchMCHMFT -> ProjectionX(Form("cuts_chi2MatchMCHMFT_cut_0_%1.0f", cut), 0, cut_bin);
            index++;
        }

        TCanvas *canvasProj = new TCanvas("canvasProj", "", 1200, 600);
        canvasProj -> Divide(2, 1);

        canvasProj -> cd(1);
        gPad -> SetLogy();
        histProj_chi2 -> GetXaxis() -> SetRangeUser(0, 200);
        histProj_chi2 -> Draw("PLC");
        for (int i = 0;i < (int) cuts_chi2MatchMCHMFT.size();i++) {
            histProj_chi2_cuts[i] -> Draw("PLC SAME");
        }
        gPad -> BuildLegend(0.5, 0.65, 0.980, 0.935, "", "L");

        canvasProj -> cd(2);
        gPad -> SetLogy();
        histProj_chi2MatchMCHMFT -> GetXaxis() -> SetRangeUser(0, 200);
        histProj_chi2MatchMCHMFT -> Draw();
    } else {
        float fPt = 0;
        float fEta = 0;
        float fPhi = 0;
        int fSign = 0;
        int fIsAmbiguous = 0;
        float fChi2 = 0;
        float fChi2MatchMCHMID = 0;
        float fChi2MatchMCHMFT = 0;

        double min_pt[] = {0, 1, 2, 3, 4, 5, 6, 7, 10};
        double max_pt[] = {1, 2, 3, 4, 5, 6, 7, 10, 20};

        const int size_pt = sizeof(min_pt) / sizeof(double);

        ifstream inFile;
        inFile.open(Form("/Users/lucamicheletti/cernbox/JPSI/Run3/2022/apass3/%s/run_list.txt", period.c_str()));

        //vector <string> run_list;
        //string tmp_run;
        //while (inFile >> tmp_run) {
            //run_list.push_back(tmp_run);
        //}
        
        vector <string> run_list = {"528093"};
        const int size_run_list = run_list.size();

        TH2F *hist_chi2_chi2MatchMCHMID = new TH2F("hist_chi2_chi2MatchMCHMID", "", 1000, 0, 1000, 1000, 0, 1000); 
        TH2F *hist_chi2_chi2MatchMCHMFT = new TH2F("hist_chi2_chi2MatchMCHMFT", "", 1000, 0, 1000, 1000, 0, 1000); 

        int run_counter = 0;
        double coll_acc_counter = 0;
        double coll_all_counter = 0;
        for (auto& run : run_list) {
            std::cout << "Run = " << run << std::endl;
            std::vector<std::string> path_to_dir = get_directories(Form("%s/%s/%s", path_to_data.c_str(), period.c_str(), run.c_str()));
            for (auto& path : path_to_dir) {
                string path_to_tree = Form("%s/AO2D.root", path.c_str());
                TFile *fIn_tree = new TFile(path_to_tree.c_str(), "READ");
                TIter next(fIn_tree -> GetListOfKeys()); 
                TKey *key; 
                while ((key = (TKey*) next())) { 
                    TString dirName = key -> GetName();
                    if (!dirName.Contains("DF_")) {
                        continue;
                    }

                    TTree *tree_rtmuon = (TTree*) fIn_tree -> Get(Form("%s/O2rtmuon", dirName.Data()));
                    tree_rtmuon -> SetBranchAddress("fPt", &fPt);
                    tree_rtmuon -> SetBranchAddress("fEta", &fEta);
                    tree_rtmuon -> SetBranchAddress("fSign", &fSign);
                    tree_rtmuon -> SetBranchAddress("fIsAmbiguous", &fIsAmbiguous);

                    TTree *tree_rtmuonextra = (TTree*) fIn_tree -> Get(Form("%s/O2rtmuonextra", dirName.Data()));
                    tree_rtmuonextra -> SetBranchAddress("fChi2", &fChi2);
                    tree_rtmuonextra -> SetBranchAddress("fChi2MatchMCHMID", &fChi2MatchMCHMID);
                    tree_rtmuonextra -> SetBranchAddress("fChi2MatchMCHMFT", &fChi2MatchMCHMFT);
                    
                    std::cout << tree_rtmuon -> GetEntries() << std::endl;

                    for (int iEntry = 0;iEntry < tree_rtmuon -> GetEntries();iEntry++) {
                        tree_rtmuon -> GetEntry(iEntry);
                        tree_rtmuonextra -> GetEntry(iEntry);

                        hist_chi2_chi2MatchMCHMID -> Fill(fChi2, fChi2MatchMCHMID);
                        hist_chi2_chi2MatchMCHMFT -> Fill(fChi2, fChi2MatchMCHMFT);
                    }
                }
                fIn_tree -> Close();
            }
            run_counter++;
        }
        inFile.close();

        TCanvas *canvas_chi2 = new TCanvas("canvas_chi2", "", 800, 600);

        TCanvas *canvas_chi2_chi2MatchMCHMID = new TCanvas("canvas_chi2_chi2MatchMCHMID", "", 800, 600);
        hist_chi2_chi2MatchMCHMID -> Draw("COLZ");

        TCanvas *canvas_chi2MatchMCHMFT = new TCanvas("canvas_chi2MatchMCHMFT", "", 800, 600);
        hist_chi2_chi2MatchMCHMFT -> Draw("COLZ");

        TFile *fOut = new TFile("chi2_studies.root", "RECREATE");
        hist_chi2_chi2MatchMCHMID -> Write();
        hist_chi2_chi2MatchMCHMFT -> Write();
        fOut -> Close(); 
    }
}