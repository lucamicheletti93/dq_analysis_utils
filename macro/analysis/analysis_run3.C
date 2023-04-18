void analysis_run3(){
    gStyle -> SetOptStat(0);
    gStyle -> SetPadLeftMargin(0.15);
    gStyle -> SetPadBottomMargin(0.15);
    gStyle -> SetPadTopMargin(0.05);
    gStyle -> SetPadRightMargin(0.05);
    gStyle -> SetEndErrorSize(0.0);
    gStyle -> SetPalette(kBlueRedYellow);

    double pt_centr_PDG[] = {15};
    double pt_width_PDG[] = {15};
    double PDG_Jpsi_mass[] = {3.096};
    double err_PDG_Jpsi_mass[1];
    err_PDG_Jpsi_mass[0] = TMath::Sqrt(0.002 * 0.002 + 0.006 * 0.006);

    TGraphErrors *gra_Jpsi_mass_PDG = new TGraphErrors(1, pt_centr_PDG, PDG_Jpsi_mass, pt_width_PDG, err_PDG_Jpsi_mass);
    gra_Jpsi_mass_PDG -> SetLineWidth(3);
    gra_Jpsi_mass_PDG -> SetLineColor(kGray+1);
    gra_Jpsi_mass_PDG -> SetFillColorAlpha(kGray+1, 0.3);


    double pt_centr_run2[] = {0.25, 0.75, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 9, 11, 13, 15, 17, 19, 21, 24, 28};
    double pt_width_run2[] = {0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1, 1, 1, 1, 2, 2};
    double run2_reso[] = {0.067, 0.069, 0.068, 0.069, 0.069, 0.070, 0.071, 0.072, 0.074, 0.075, 0.079, 0.080, 0.087, 0.083, 0.098, 0.083, 0.112, 0.121};
    double err_run2_reso[] = {0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.002, 0.003, 0.005, 0.007, 0.010, 0.011, 0.019, 0.031};

    TGraphErrors *gra_run2 = new TGraphErrors(18, pt_centr_run2, run2_reso, pt_width_run2, err_run2_reso);
    gra_run2 -> SetMarkerStyle(20);
    gra_run2 -> SetMarkerColor(kRed+1);
    gra_run2 -> SetLineColor(kRed+1);
    gra_run2 -> SetLineWidth(2);

    /*string fIn_list[] = {
        "/Users/lucamicheletti/GITHUB/dq_fit_library/validation/output/analysis/LHC22m_apass3/myAnalysis.root",
        "/Users/lucamicheletti/GITHUB/dq_fit_library/validation/output/analysis/LHC22p_apass3/myAnalysis.root",
        "/Users/lucamicheletti/GITHUB/dq_fit_library/validation/output/analysis/LHC22q_apass3/myAnalysis.root",
        "/Users/lucamicheletti/GITHUB/dq_fit_library/validation/output/analysis/LHC22o_apass3/myAnalysis.root"
    };*/

    string fIn_list[] = {
        "/Users/lucamicheletti/GITHUB/dq_fit_library/validation/output/analysis/LHC22o_medium_apass3/myAnalysis.root"
    };

    const int size_fIn_list = sizeof(fIn_list) / sizeof(string);
    TGraphErrors *gra_width_jpsi[size_fIn_list];
    TGraphErrors *gra_mean_jpsi[size_fIn_list];

    for (int i = 0;i < size_fIn_list;i++) {
        TFile *fIn = new TFile(fIn_list[i].c_str(), "READ");
        gra_width_jpsi[i] = (TGraphErrors*) fIn -> Get("gra_width_Jpsi");
        gra_mean_jpsi[i] = (TGraphErrors*) fIn -> Get("gra_mean_Jpsi");
    }

    TH2D *hist_grid_reso = new TH2D("hist_grid_reso", "", 100, 0, 30, 100, 0.02, 0.15);
    hist_grid_reso -> SetTitleSize(0.05,"X");
    hist_grid_reso -> SetTitleSize(0.045,"Y");
    hist_grid_reso -> SetLabelSize(0.045,"X");
    hist_grid_reso -> SetLabelSize(0.045,"Y");
    hist_grid_reso -> SetTitleOffset(1.2,"X");
    hist_grid_reso -> SetTitleOffset(1.35,"Y");
    hist_grid_reso -> GetXaxis() -> SetTitle("#it{p}_{T} (GeV/#it{c})");
    hist_grid_reso -> GetYaxis() -> SetTitle("#sigma_{J/#psi} (GeV/#it{c}^{2})");

    TCanvas *canvas_comp_Jpsi_reso = new TCanvas("canvas_comp_Jpsi_reso", "", 800, 600);
    canvas_comp_Jpsi_reso -> SetLeftMargin(0.15);
    //gPad -> SetLogy();
    hist_grid_reso -> Draw();
    gra_run2 -> Draw("EP SAME");
    for (int i = 0;i < size_fIn_list;i++) {
        gra_width_jpsi[i] -> Draw("EP PLC SAME");
    }

    // Ratio Psi(2S) / J/Psi
    double pt_bin_limits_run2[] = {0, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14};
    double pt_bin_centr_run2[] = {0.25, 0.75, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 9, 11, 13};
    double width_pt_bin_run2[] = {0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 1};

    double sig_jpsi_run2[] = {12896, 30703, 71984, 62544, 48123, 35498, 24109, 15957, 10366, 10457, 4487, 2006};
    double stat_sig_jpsi_run2[] = {188, 295, 435, 391, 328, 268, 206, 173, 134, 139, 93, 62};
    double syst_sig_jpsi_run2[] = {333, 752, 1853, 1883, 1474, 970, 578, 337, 232, 239, 104, 56};

    double sig_psi2s_run2[] = {547, 1922, 1755, 1072, 829, 615, 384, 288, 281, 123, 88, 45};
    double stat_sig_psi2s_run2[] = {116, 162, 137, 105, 81, 63, 48, 40, 41, 29, 19, 16};
    double syst_sig_psi2s_run2[] = {44, 95, 111, 64, 52, 34, 27, 20, 43, 17, 9, 4};

    TH1F *hist_sig_jpsi_run2 = new TH1F("hist_sig_jpsi_run2", "", 12, pt_bin_limits_run2);
    hist_sig_jpsi_run2 -> SetLineWidth(2);
    hist_sig_jpsi_run2 -> SetLineColor(kRed+1);
    hist_sig_jpsi_run2 -> SetMarkerStyle(20);
    hist_sig_jpsi_run2 -> SetMarkerColor(kRed+1);

    TH1F *hist_sig_psi2s_run2 = new TH1F("hist_sig_psi2s_run2", "", 12, pt_bin_limits_run2);
    hist_sig_psi2s_run2 -> SetLineWidth(2);
    hist_sig_psi2s_run2 -> SetLineColor(kRed+1);
    hist_sig_psi2s_run2 -> SetMarkerStyle(20);
    hist_sig_psi2s_run2 -> SetMarkerColor(kRed+1);

    for (int i = 0;i < 12;i++) {
        hist_sig_jpsi_run2 -> SetBinContent(i+1, sig_jpsi_run2[i]);
        hist_sig_jpsi_run2 -> SetBinError(i+1, TMath::Sqrt(stat_sig_jpsi_run2[i] * stat_sig_jpsi_run2[i] + syst_sig_jpsi_run2[i] * syst_sig_jpsi_run2[i]));
        hist_sig_psi2s_run2 -> SetBinContent(i+1, sig_psi2s_run2[i]);
        hist_sig_psi2s_run2 -> SetBinError(i+1, TMath::Sqrt(stat_sig_psi2s_run2[i] * stat_sig_psi2s_run2[i] + syst_sig_psi2s_run2[i] * syst_sig_psi2s_run2[i]));
    }

    TH1F *hist_psi2s_over_jpsi_run2 = (TH1F*) hist_sig_psi2s_run2 -> Clone("hist_psi2s_over_jpsi_run2");
    hist_psi2s_over_jpsi_run2 -> Divide(hist_sig_jpsi_run2);

    TH1F *hist_sig_jpsi_run3[size_fIn_list];
    TH1F *hist_sig_psi2s_run3[size_fIn_list];
    TH1F *hist_psi2s_over_jpsi_run3[size_fIn_list];
    for (int i = 0;i < size_fIn_list;i++) {
        TFile *fIn = new TFile(fIn_list[i].c_str(), "READ");
        hist_sig_jpsi_run3[i] = (TH1F*) fIn -> Get("hist_sig_Jpsi");
        hist_sig_psi2s_run3[i] = (TH1F*) fIn -> Get("hist_sig_Psi2s");
        hist_psi2s_over_jpsi_run3[i] = (TH1F*) hist_sig_psi2s_run3[i] -> Clone(Form("hist_psi2s_over_jpsi_run3_%i", i));
        hist_psi2s_over_jpsi_run3[i] -> Divide(hist_sig_jpsi_run3[i]);
        hist_psi2s_over_jpsi_run3[i] -> SetMarkerStyle(24);
    }

    TH2D *hist_grid_psi2s_over_jpsi = new TH2D("hist_grid_psi2s_over_jpsi", "", 100, 0, 20, 100, 0, 0.08);
    hist_grid_psi2s_over_jpsi -> SetTitleSize(0.05,"X");
    hist_grid_psi2s_over_jpsi -> SetTitleSize(0.045,"Y");
    hist_grid_psi2s_over_jpsi -> SetLabelSize(0.045,"X");
    hist_grid_psi2s_over_jpsi -> SetLabelSize(0.045,"Y");
    hist_grid_psi2s_over_jpsi -> SetTitleOffset(1.2,"X");
    hist_grid_psi2s_over_jpsi -> SetTitleOffset(1.35,"Y");
    hist_grid_psi2s_over_jpsi -> GetXaxis() -> SetTitle("#it{p}_{T} (GeV/#it{c})");
    hist_grid_psi2s_over_jpsi -> GetYaxis() -> SetTitle("#psi(2S) / J/#psi");

    TCanvas *canvas_comp_psi2s_over_jpsi = new TCanvas("canvas_comp_psi2s_over_jpsi", "", 800, 600);
    canvas_comp_psi2s_over_jpsi -> SetLeftMargin(0.15);
    hist_grid_psi2s_over_jpsi -> Draw();
    hist_psi2s_over_jpsi_run2 -> Draw("EP SAME");
    for (int i = 0;i < size_fIn_list;i++) {
        hist_psi2s_over_jpsi_run3[i] -> Draw("EP PLC SAME");
    }
}


void remove_combinatorial_background() {
    int min_pt[] = {0, 1, 2, 3, 5, 7, 10};
    int max_pt[] = {1, 2, 3, 5, 7, 10, 20};

    TFile *fIn = new TFile("/Users/lucamicheletti/cernbox/JPSI/Run3/2022/apass3/LHC22o/histograms.root", "READ");

    TH1F *hist_mass[7];
    TH1F *hist_mass_sig[7];
    TH1F *hist_mass_bkg[7];

    for (int i = 0;i < 7;i++) {
        hist_mass[i] = (TH1F*) fIn -> Get(Form("hist_mass_pt_%i_%i", min_pt[i], max_pt[i]));
        TH1F *hist_mass_PP = (TH1F*) fIn -> Get(Form("hist_mass_pt_%i_%i_PP", min_pt[i], max_pt[i]));
        TH1F *hist_mass_MM = (TH1F*) fIn -> Get(Form("hist_mass_pt_%i_%i_MM", min_pt[i], max_pt[i]));
        hist_mass_sig[i] = new TH1F(Form("hist_mass_pt_%i_%i_sig", min_pt[i], max_pt[i]), "", 100, 2, 5); 
        hist_mass_bkg[i] = new TH1F(Form("hist_mass_pt_%i_%i_bkg", min_pt[i], max_pt[i]), "", 100, 2, 5);

        hist_mass[i] -> SetLineColor(kBlack);
        hist_mass[i] -> SetMarkerColor(kBlack);
        hist_mass[i] -> SetMarkerStyle(20);
        hist_mass[i] -> SetMarkerSize(0.5);
        hist_mass_sig[i] -> SetLineColor(kRed+1);
        hist_mass_sig[i] -> SetLineWidth(2);
        hist_mass_sig[i] -> SetFillColorAlpha(kRed+1, 0.5);
        hist_mass_bkg[i] -> SetLineColor(kAzure+2);
        hist_mass_bkg[i] -> SetLineWidth(2); 

        for (int j = 0;j < hist_mass[i] -> GetNbinsX();j++) {
            double OS = hist_mass[i] -> GetBinContent(j+1);
            double PP = hist_mass_PP -> GetBinContent(j+1);
            double MM = hist_mass_MM -> GetBinContent(j+1);
            hist_mass_bkg[i] -> SetBinContent(j+1, 2 * TMath::Sqrt(PP * MM));
            hist_mass_sig[i] -> SetBinContent(j+1, OS - 2 * TMath::Sqrt(PP * MM));
        }
    }

    

    TCanvas *canvas = new TCanvas("canvas", "", 2400, 1200);
    canvas -> Divide(4, 2);

    for (int i = 0;i < 7;i++) {
        canvas -> cd(i+1);
        hist_mass[i] -> Draw("EP");
        //hist_mass_PP -> Draw("H SAME");
        //hist_mass_MM -> Draw("H SAME");
        hist_mass_bkg[i] -> Draw("H SAME");
        hist_mass_sig[i] -> Draw("H SAME");
    }
}