std::vector<std::string> get_directories(const std::string& s) {
    std::vector<std::string> r;
    for(auto& p : std::filesystem::recursive_directory_iterator(s))
        if (p.is_directory())
            r.push_back(p.path().string());
    return r;
}

void read_flat_table(){

    float fMass = 0;
    float fEta = 0;
    float fEta1 = 0;
    float fEta2 = 0;
    int fSign = 0;
    float fChi2MatchMCHMID1 = 0;
    float fChi2MatchMCHMID2 = 0;
    int fIsAmbig1 = 0;
    int fIsAmbig2 = 0;

    TH1F *hist_mass = new TH1F("hist_mass", "Dimuons", 250, 0, 5); hist_mass -> SetLineColor(kBlack);
    hist_mass -> SetMinimum(0.1);
    TH1F *hist_mass_ambiguous = new TH1F("hist_mass_ambiguous", "Ambiguous", 250, 0, 5); hist_mass_ambiguous -> SetLineColor(kRed+1);
    TH1F *hist_mass_non_ambiguous = new TH1F("hist_mass_non_ambiguous", "Unambiguous", 250, 0, 5); hist_mass_non_ambiguous -> SetLineColor(kGreen+1);
    TH1F *hist_eta = new TH1F("hist_eta", "", 250, -5, 5);
    TH1F *hist_eta1 = new TH1F("hist_eta1", "", 250, -5, 5);
    TH1F *hist_eta2 = new TH1F("hist_eta2", "", 250, -5, 5);
    TH1F *hist_chi2MatchMCHMID1 = new TH1F("hist_chi2MatchMCHMID1", "", 250, 0, 100);
    TH1F *hist_chi2MatchMCHMID2 = new TH1F("hist_chi2MatchMCHMID2", "", 250, 0, 100);

    string run_list[] = {"528602", "528781", "528783", "528617", "528798", "528801", "528604", "528784", "528782"};
    //string run_list[] = {"523141", "523142", "523148", "523669", "523897", "523182", "523186", "523559", "523671", "523728", "523779", "523783", "523786", "523788", "523789", "523792",
                         //"523298", "523306", "523308", "523309", "523397", "523399", "523401", "523677", "523441", "523541", "523797", "523821", "523731"};
    //string pathToFiles[] = {"data/LHC22m/001/AO2D.root", "data/LHC22m/002/AO2D.root", "data/LHC22m/003/AO2D.root", "data/LHC22m/004/AO2D.root", "data/LHC22m/005/AO2D.root"};
    //string pathToFiles[] = {"/Users/lucamicheletti/GITHUB/O2DQworkflows/dileptonAOD.root"};
    //string pathToFiles[] = {"/Users/lucamicheletti/GITHUB/O2DQworkflows/dileptonAOD_best_collisions.root"};
    //for (auto& pathToFile : pathToFiles) {
    for (auto& run : run_list) {
        std::vector<std::string> path_to_dir = get_directories(Form("data/LHC22p/%s", run.c_str()));
        for (auto& path : path_to_dir) {
            string path_to_file = Form("%s/AO2D.root", path.c_str());
            TFile *fIn = new TFile(path_to_file.c_str(), "READ");
            TIter next(fIn -> GetListOfKeys()); 
            TKey *key; 
            while ((key = (TKey*) next())) { 
                TString dirName = key -> GetName();
                if (!dirName.Contains("DF_")) {
                    continue;
                }
                //key -> Print(); 
                TTree *tree = (TTree*) fIn -> Get(Form("%s/O2rtdimuonall", dirName.Data()));
                tree -> SetBranchAddress("fMass", &fMass);
                tree -> SetBranchAddress("fEta", &fEta);
                tree -> SetBranchAddress("fEta1", &fEta1);
                tree -> SetBranchAddress("fEta2", &fEta2);
                tree -> SetBranchAddress("fSign", &fSign);
                tree -> SetBranchAddress("fChi2MatchMCHMID1", &fChi2MatchMCHMID1);
                tree -> SetBranchAddress("fChi2MatchMCHMID2", &fChi2MatchMCHMID2);
                tree -> SetBranchAddress("fIsAmbig1", &fIsAmbig1);
                tree -> SetBranchAddress("fIsAmbig2", &fIsAmbig2);
                
                std::cout << tree -> GetEntries() << std::endl;

                for (int iEntry = 0;iEntry < tree -> GetEntries();iEntry++) {
                    tree -> GetEntry(iEntry);
                    hist_eta -> Fill(fEta);
                    hist_eta1 -> Fill(fEta1);
                    hist_eta2 -> Fill(fEta2);
                    hist_chi2MatchMCHMID1 -> Fill(fChi2MatchMCHMID1);
                    hist_chi2MatchMCHMID1 -> Fill(fChi2MatchMCHMID2);
                    if (fSign != 0) continue;
                    if (TMath::Abs(fEta) > 2.5 && TMath::Abs(fEta) < 4) {
                        if (TMath::Abs(fEta1) > 2.5 && TMath::Abs(fEta1) < 4) {
                            if (TMath::Abs(fEta2) > 2.5 && TMath::Abs(fEta2) < 4) {
                                if (fChi2MatchMCHMID1 < 20 && fChi2MatchMCHMID2 < 20) {
                                    hist_mass -> Fill(fMass);
                                    if (fIsAmbig1 == 1 || fIsAmbig2 == 1) {
                                        hist_mass_ambiguous -> Fill(fMass);
                                    }
                                    if (fIsAmbig1 == 0 && fIsAmbig2 == 0) {
                                        hist_mass_non_ambiguous -> Fill(fMass);
                                    }
                                }
                            }
                        }
                    }
                }
            }
            fIn -> Close();
        }
    }
    

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
}