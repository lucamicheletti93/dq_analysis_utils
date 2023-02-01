void run2_comparison(){
    gStyle -> SetOptStat(0);
    gStyle -> SetPadLeftMargin(0.15);
    gStyle -> SetPadBottomMargin(0.15);
    gStyle -> SetPadTopMargin(0.05);
    gStyle -> SetPadRightMargin(0.05);
    gStyle -> SetEndErrorSize(0.0);

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

    double pt_centr_run3[] = {1, 4, 18};
    double pt_width_run3[] = {1, 2, 12};

    double run3_Jpsi_reso_LHC22m_pass1[] = {0.172, 0.199, 0.250};
    double err_run3_Jpsi_reso_LHC22m_pass1[] = {0.003, 0.003, 0.010};

    double run3_Jpsi_mass_LHC22m_pass1[] = {3.095, 3.120, 3.196};
    double err_run3_Jpsi_mass_LHC22m_pass1[] = {0.002, 0.003, 0.009};

    TGraphErrors *gra_Jpsi_reso_run3_LHC22m_pass1 = new TGraphErrors(3, pt_centr_run3, run3_Jpsi_reso_LHC22m_pass1, pt_width_run3, err_run3_Jpsi_reso_LHC22m_pass1);
    gra_Jpsi_reso_run3_LHC22m_pass1 -> SetMarkerStyle(24);
    gra_Jpsi_reso_run3_LHC22m_pass1 -> SetMarkerColor(kAzure+2);
    gra_Jpsi_reso_run3_LHC22m_pass1 -> SetLineColor(kAzure+2);
    gra_Jpsi_reso_run3_LHC22m_pass1 -> SetLineWidth(2);

    TGraphErrors *gra_Jpsi_mass_run3_LHC22m_pass1 = new TGraphErrors(3, pt_centr_run3, run3_Jpsi_mass_LHC22m_pass1, pt_width_run3, err_run3_Jpsi_mass_LHC22m_pass1);
    gra_Jpsi_mass_run3_LHC22m_pass1 -> SetMarkerStyle(24);
    gra_Jpsi_mass_run3_LHC22m_pass1 -> SetMarkerColor(kAzure+2);
    gra_Jpsi_mass_run3_LHC22m_pass1 -> SetLineColor(kAzure+2);
    gra_Jpsi_mass_run3_LHC22m_pass1 -> SetLineWidth(2);

    double run3_Jpsi_reso_LHC22m_pass2[] = {0.083, 0.095, 0.099};
    double err_run3_Jpsi_reso_LHC22m_pass2[] = {0.002, 0.002, 0.005};

    double run3_Jpsi_mass_LHC22m_pass2[] = {3.079, 3.073, 3.090};
    double err_run3_Jpsi_mass_LHC22m_pass2[] = {0.002, 0.002, 0.005};

    TGraphErrors *gra_Jpsi_reso_run3_LHC22m_pass2 = new TGraphErrors(3, pt_centr_run3, run3_Jpsi_reso_LHC22m_pass2, pt_width_run3, err_run3_Jpsi_reso_LHC22m_pass2);
    gra_Jpsi_reso_run3_LHC22m_pass2 -> SetMarkerStyle(20);
    gra_Jpsi_reso_run3_LHC22m_pass2 -> SetMarkerColor(kAzure+2);
    gra_Jpsi_reso_run3_LHC22m_pass2 -> SetLineColor(kAzure+2);
    gra_Jpsi_reso_run3_LHC22m_pass2 -> SetLineWidth(2);

    TGraphErrors *gra_Jpsi_mass_run3_LHC22m_pass2 = new TGraphErrors(3, pt_centr_run3, run3_Jpsi_mass_LHC22m_pass2, pt_width_run3, err_run3_Jpsi_mass_LHC22m_pass2);
    gra_Jpsi_mass_run3_LHC22m_pass2 -> SetMarkerStyle(20);
    gra_Jpsi_mass_run3_LHC22m_pass2 -> SetMarkerColor(kAzure+2);
    gra_Jpsi_mass_run3_LHC22m_pass2 -> SetLineColor(kAzure+2);
    gra_Jpsi_mass_run3_LHC22m_pass2 -> SetLineWidth(2);

    double run3_Jpsi_reso_LHC22o_pass2[] = {0.090, 0.116, 0.143};
    double err_run3_Jpsi_reso_LHC22o_pass2[] = {0.001, 0.000, 0.026};

    double run3_Jpsi_mass_LHC22o_pass2[] = {3.083, 3.080, 3.084};
    double err_run3_Jpsi_mass_LHC22o_pass2[] = {0.000, 0.000, 0.003};

    TGraphErrors *gra_Jpsi_reso_run3_LHC22o_pass2 = new TGraphErrors(3, pt_centr_run3, run3_Jpsi_reso_LHC22o_pass2, pt_width_run3, err_run3_Jpsi_reso_LHC22o_pass2);
    gra_Jpsi_reso_run3_LHC22o_pass2 -> SetMarkerStyle(20);
    gra_Jpsi_reso_run3_LHC22o_pass2 -> SetMarkerColor(kGreen+1);
    gra_Jpsi_reso_run3_LHC22o_pass2 -> SetLineColor(kGreen+1);
    gra_Jpsi_reso_run3_LHC22o_pass2 -> SetLineWidth(2);

    TGraphErrors *gra_Jpsi_mass_run3_LHC22o_pass2 = new TGraphErrors(3, pt_centr_run3, run3_Jpsi_mass_LHC22o_pass2, pt_width_run3, err_run3_Jpsi_mass_LHC22o_pass2);
    gra_Jpsi_mass_run3_LHC22o_pass2 -> SetMarkerStyle(20);
    gra_Jpsi_mass_run3_LHC22o_pass2 -> SetMarkerColor(kGreen+1);
    gra_Jpsi_mass_run3_LHC22o_pass2 -> SetLineColor(kGreen+1);
    gra_Jpsi_mass_run3_LHC22o_pass2 -> SetLineWidth(2);

    double run3_reso_mc_prompt[] = {0.075, 0.079, 0.091};
    double err_run3_reso_mc_prompt[] = {0.001, 0.004, 0.003};

    TGraphErrors *gra_run3_mc_prompt = new TGraphErrors(3, pt_centr_run3, run3_reso_mc_prompt, pt_width_run3, err_run3_reso_mc_prompt);
    gra_run3_mc_prompt -> SetMarkerStyle(24);
    gra_run3_mc_prompt -> SetMarkerColor(kAzure+2);
    gra_run3_mc_prompt -> SetLineColor(kAzure+2);
    gra_run3_mc_prompt -> SetLineWidth(2);

    double run3_reso_mc_non_prompt[] = {0.076, 0.079, 0.091};
    double err_run3_reso_mc_non_prompt[] = {0.002, 0.001, 0.002};

    TGraphErrors *gra_run3_mc_non_prompt = new TGraphErrors(3, pt_centr_run3, run3_reso_mc_non_prompt, pt_width_run3, err_run3_reso_mc_non_prompt);
    gra_run3_mc_non_prompt -> SetMarkerStyle(24);
    gra_run3_mc_non_prompt -> SetMarkerColor(kOrange+2);
    gra_run3_mc_non_prompt -> SetLineColor(kOrange+2);
    gra_run3_mc_non_prompt -> SetLineWidth(2);

    TH2D *hist_grid_reso = new TH2D("hist_grid_reso", "", 100, 0, 30, 100, 0.02, 0.35);
    hist_grid_reso -> SetTitleSize(0.05,"X");
    hist_grid_reso -> SetTitleSize(0.045,"Y");
    hist_grid_reso -> SetLabelSize(0.045,"X");
    hist_grid_reso -> SetLabelSize(0.045,"Y");
    hist_grid_reso -> SetTitleOffset(1.2,"X");
    hist_grid_reso -> SetTitleOffset(1.35,"Y");
    hist_grid_reso -> GetXaxis() -> SetTitle("#it{p}_{T} (GeV/#it{c})");
    hist_grid_reso -> GetYaxis() -> SetTitle("#sigma_{J/#psi} (GeV/#it{c}^{2})");

    TH2D *hist_grid_mass = new TH2D("hist_grid_mass", "", 100, 0, 30, 100, 2.9, 3.3);
    hist_grid_mass -> SetTitleSize(0.05,"X");
    hist_grid_mass -> SetTitleSize(0.045,"Y");
    hist_grid_mass -> SetLabelSize(0.045,"X");
    hist_grid_mass -> SetLabelSize(0.045,"Y");
    hist_grid_mass -> SetTitleOffset(1.2,"X");
    hist_grid_mass -> SetTitleOffset(1.35,"Y");
    hist_grid_mass -> GetXaxis() -> SetTitle("#it{p}_{T} (GeV/#it{c})");
    hist_grid_mass -> GetYaxis() -> SetTitle("#it{m}_{J/#psi} (GeV/#it{c}^{2})");

    TLegend *legend = new TLegend(0.55, 0.20, 0.75, 0.50, " ", "brNDC");
    legend -> SetBorderSize(0);
    legend -> SetFillColor(10);
    legend -> SetFillStyle(1);
    legend -> SetLineStyle(0);
    legend -> SetLineColor(0);
    legend -> SetTextFont(42);
    legend -> SetTextSize(0.04);
    legend -> AddEntry(gra_run2, "Run2 Data", "PL");
    legend -> AddEntry(gra_Jpsi_reso_run3_LHC22m_pass1, "Run3 Data - pass1", "PL");
    legend -> AddEntry(gra_Jpsi_reso_run3_LHC22m_pass2, "Run3 Data - pass2", "PL");
    legend -> AddEntry(gra_run3_mc_prompt, "Run3 MC prompt", "PL");
    legend -> AddEntry(gra_run3_mc_non_prompt, "Run3 MC non-prompt", "PL");

    TCanvas *canvas_comp_Jpsi_reso = new TCanvas("canvas_comp_Jpsi_reso", "", 800, 600);
    canvas_comp_Jpsi_reso -> SetLeftMargin(0.15);
    gPad -> SetLogy();
    hist_grid_reso -> Draw();
    gra_run2 -> Draw("EPsame");
    gra_Jpsi_reso_run3_LHC22m_pass1 -> Draw("EPsame");
    gra_Jpsi_reso_run3_LHC22m_pass2 -> Draw("EPsame");
    gra_run3_mc_prompt -> Draw("EPsame");
    gra_run3_mc_non_prompt -> Draw("EPsame");
    legend -> Draw("same");

    canvas_comp_Jpsi_reso -> SaveAs("run2_comparison.pdf");

    TLegend *legend_data = new TLegend(0.55, 0.20, 0.75, 0.50, " ", "brNDC");
    legend_data -> SetBorderSize(0);
    legend_data -> SetFillColor(10);
    legend_data -> SetFillStyle(1);
    legend_data -> SetLineStyle(0);
    legend_data -> SetLineColor(0);
    legend_data -> SetTextFont(42);
    legend_data -> SetTextSize(0.04);
    legend_data -> AddEntry(gra_run2, "Run2 Data", "PL");
    legend_data -> AddEntry(gra_Jpsi_reso_run3_LHC22m_pass1, "LHC22m apass1", "PL");
    legend_data -> AddEntry(gra_Jpsi_reso_run3_LHC22m_pass2, "LHC22m apass2", "PL");

    TCanvas *canvas_compt_Jpsi_reso_data = new TCanvas("canvas_compt_Jpsi_reso_data", "", 800, 600);
    canvas_compt_Jpsi_reso_data -> SetLeftMargin(0.15);
    gPad -> SetLogy();
    hist_grid_reso -> Draw();
    gra_run2 -> Draw("EPsame");
    gra_Jpsi_reso_run3_LHC22m_pass1 -> Draw("EPsame");
    gra_Jpsi_reso_run3_LHC22m_pass2 -> Draw("EPsame");
    legend_data -> Draw("same");

    TLegend *legend_data2_noRun2 = new TLegend(0.55, 0.20, 0.75, 0.50, " ", "brNDC");
    legend_data2_noRun2 -> SetBorderSize(0);
    legend_data2_noRun2 -> SetFillColor(10);
    legend_data2_noRun2 -> SetFillStyle(1);
    legend_data2_noRun2 -> SetLineStyle(0);
    legend_data2_noRun2 -> SetLineColor(0);
    legend_data2_noRun2 -> SetTextFont(42);
    legend_data2_noRun2 -> SetTextSize(0.04);
    legend_data2_noRun2 -> AddEntry(gra_run2, "Run2 Data", "PL");
    legend_data2_noRun2 -> AddEntry(gra_Jpsi_reso_run3_LHC22m_pass2, "LHC22m apass2", "PL");
    legend_data2_noRun2 -> AddEntry(gra_Jpsi_reso_run3_LHC22o_pass2, "LHC22o apass2", "PL");

    TCanvas *canvas_compt_Jpsi_reso_data2 = new TCanvas("canvas_compt_Jpsi_reso_data2", "", 800, 600);
    canvas_compt_Jpsi_reso_data2 -> SetLeftMargin(0.15);
    gPad -> SetLogy();
    hist_grid_reso -> Draw();
    gra_run2 -> Draw("EPsame");
    gra_Jpsi_reso_run3_LHC22m_pass2 -> Draw("EPsame");
    gra_Jpsi_reso_run3_LHC22o_pass2 -> Draw("EPsame");
    legend_data2_noRun2 -> Draw("same");

    TLegend *legend_data_noRun2 = new TLegend(0.55, 0.20, 0.75, 0.50, " ", "brNDC");
    legend_data_noRun2 -> SetBorderSize(0);
    legend_data_noRun2 -> SetFillColor(10);
    legend_data_noRun2 -> SetFillStyle(1);
    legend_data_noRun2 -> SetLineStyle(0);
    legend_data_noRun2 -> SetLineColor(0);
    legend_data_noRun2 -> SetTextFont(42);
    legend_data_noRun2 -> SetTextSize(0.04);
    legend_data_noRun2 -> AddEntry(gra_Jpsi_reso_run3_LHC22m_pass1, "LHC22m apass1", "PL");
    legend_data_noRun2 -> AddEntry(gra_Jpsi_reso_run3_LHC22m_pass2, "LHC22m apass2", "PL");
    legend_data_noRun2 -> AddEntry(gra_Jpsi_mass_PDG, "PDG", "F");

    TCanvas *canvas_compt_Jpsi_mass_data = new TCanvas("canvas_compt_Jpsi_mass_data", "", 800, 600);
    canvas_compt_Jpsi_mass_data -> SetLeftMargin(0.15);
    //gPad -> SetLogy();
    hist_grid_mass -> Draw();
    gra_Jpsi_mass_PDG -> Draw("E2same");
    gra_Jpsi_mass_run3_LHC22m_pass1 -> Draw("EPsame");
    gra_Jpsi_mass_run3_LHC22m_pass2 -> Draw("EPsame");
    legend_data_noRun2 -> Draw("same");

    canvas_comp_Jpsi_reso -> SaveAs("Jpsi_reso_comparison.pdf");
    canvas_compt_Jpsi_reso_data -> SaveAs("Jpsi_reso_comparison_data.pdf");
    canvas_compt_Jpsi_mass_data -> SaveAs("Jpsi_mass_comparison_data.pdf");
    canvas_compt_Jpsi_reso_data2 -> SaveAs("Jpsi_reso_comparison_LHC22m_LHC22o.pdf");

    // RESOLUTIONS vs ASYMMERTRY
    double pAsym[6] = {10, -10, 30, -30, 70, -70};
    double err_pAsym[6] = {10, 10, 10, 10, 30, 30};

    //string period = "LHC22m";
    //int run_list[] = {523142, 523182, 523186, 523306, 523308, 523309, 523401, 523779};

    string period = "LHC22o";
    int run_list[] = {526463, 526486, 526606, 527237, 527523, 527850, 527864, 527895, 527902, 527979, 528036, 528105,526465, 526505, 526612, 527345, 527826, 527852, 527869, 527898, 527976, 528021, 528094,526467, 526525, 526638, 527518, 527828, 527863, 527871, 527899, 527978, 528026, 528097};

    for (auto& iRun : run_list) {
        string fIn_path = Form("/Users/lucamicheletti/GITHUB/dq_fit_library/validation/output/trending_%s_apass2/CB2_VWG", period.c_str());
        const int nAsymBins = 6;
        string asymBins[] = {"0_Reso_20_1", "0_Reso_20_2", "20_Reso_40_1", "20_Reso_40_2", "40_Reso_100_1", "40_Reso_100_2"};
        double mean_Jpsi[6];
        double err_mean_Jpsi[6];

        for (int i = 0;i < nAsymBins;i++) {
            TFile *fIn = new TFile(Form("%s_%i/PairsMuonSEPM_muonLowPt_Mass_DeltaPtotTracks_Proj_%s.root", fIn_path.c_str(), iRun, asymBins[i].c_str()));
            TH1F *hist = (TH1F*) fIn -> Get("fit_results_CB2_VWG__2_5");
            for (int iBin = 0;iBin < hist -> GetNbinsX();iBin++) {
                if (strcmp(hist -> GetXaxis() -> GetBinLabel(iBin+1), "mean_Jpsi") == 0) {
                    mean_Jpsi[i] = hist -> GetBinContent(iBin+1);
                    err_mean_Jpsi[i] = hist -> GetBinError(iBin+1);
                }
            }
        }

        double integrated_mean_Jpsi = 0;
        TFile *fIn = new TFile(Form("%s_%i/Mass_PairsMuonSEPM_muonLowPt.root", fIn_path.c_str(), iRun));
        TH1F *hist_integrated = (TH1F*) fIn -> Get("fit_results_CB2_VWG__2_5");
        for (int iBin = 0;iBin < hist_integrated -> GetNbinsX();iBin++) {
            if (strcmp(hist_integrated -> GetXaxis() -> GetBinLabel(iBin+1), "mean_Jpsi") == 0) {
                integrated_mean_Jpsi = hist_integrated -> GetBinContent(iBin+1);
            }
        }

        TLine *line_integrated_mean_Jpsi = new TLine(-100, integrated_mean_Jpsi, 100, integrated_mean_Jpsi);
        line_integrated_mean_Jpsi -> SetLineColor(kRed+1);
        line_integrated_mean_Jpsi -> SetLineWidth(2);

        TH2D *hist_grid_mean_Jpsi_vs_pAsym = new TH2D("hist_grid_mean_Jpsi_vs_pAsym", "", 100, -100, 100, 100, 2.9, 3.3);
        hist_grid_mean_Jpsi_vs_pAsym -> SetTitleSize(0.05,"X");
        hist_grid_mean_Jpsi_vs_pAsym -> SetTitleSize(0.045,"Y");
        hist_grid_mean_Jpsi_vs_pAsym -> SetLabelSize(0.045,"X");
        hist_grid_mean_Jpsi_vs_pAsym -> SetLabelSize(0.045,"Y");
        hist_grid_mean_Jpsi_vs_pAsym -> SetTitleOffset(1.2,"X");
        hist_grid_mean_Jpsi_vs_pAsym -> SetTitleOffset(1.35,"Y");
        hist_grid_mean_Jpsi_vs_pAsym -> GetXaxis() -> SetTitle("#it{p}^{#mu+} - #it{p}^{#mu-}");
        hist_grid_mean_Jpsi_vs_pAsym -> GetYaxis() -> SetTitle("#it{m}_{J/#psi} (GeV/#it{c}^{2})");

        TGraphErrors *gra_mean_Jpsi_vs_pAsym = new TGraphErrors(6, pAsym, mean_Jpsi, err_pAsym, err_mean_Jpsi);
        gra_mean_Jpsi_vs_pAsym -> SetMarkerStyle(24);
        gra_mean_Jpsi_vs_pAsym -> SetMarkerColor(kBlack);
        gra_mean_Jpsi_vs_pAsym -> SetLineColor(kBlack);
        gra_mean_Jpsi_vs_pAsym -> SetLineWidth(2);

        TLatex *letexText = new TLatex();
        letexText -> SetTextSize(0.045);
        letexText -> SetNDC();
        letexText -> SetTextFont(42);

        TCanvas *canvas_mean_Jpsi_vs_pAsym = new TCanvas("canvas_mean_Jpsi_vs_pAsym", "", 800, 600);
        hist_grid_mean_Jpsi_vs_pAsym -> Draw();
        line_integrated_mean_Jpsi -> Draw("same");
        gra_mean_Jpsi_vs_pAsym -> Draw("EPsame");
        letexText -> DrawLatex(0.20, 0.85, Form("%s, run %i", period.c_str(), iRun));
        
        canvas_mean_Jpsi_vs_pAsym -> SaveAs(Form("%s/mean_Jpsi_vs_pAsym_%i.pdf", period.c_str(), iRun));
        delete canvas_mean_Jpsi_vs_pAsym;
    }
}