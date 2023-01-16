void run2_comparison(){
    gStyle -> SetOptStat(0);
    gStyle -> SetPadLeftMargin(0.15);
    gStyle -> SetPadBottomMargin(0.15);
    gStyle -> SetPadTopMargin(0.05);
    gStyle -> SetPadRightMargin(0.05);
    gStyle -> SetEndErrorSize(0.0);

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

    double run3_reso_pass1[] = {0.172, 0.199, 0.250};
    double err_run3_reso_pass1[] = {0.003, 0.003, 0.010};

    TGraphErrors *gra_run3_pass1 = new TGraphErrors(3, pt_centr_run3, run3_reso_pass1, pt_width_run3, err_run3_reso_pass1);
    gra_run3_pass1 -> SetMarkerStyle(24);
    gra_run3_pass1 -> SetMarkerColor(kAzure+2);
    gra_run3_pass1 -> SetLineColor(kAzure+2);
    gra_run3_pass1 -> SetLineWidth(2);

    double run3_reso_pass2[] = {0.083, 0.095, 0.099};
    double err_run3_reso_pass2[] = {0.002, 0.002, 0.005};

    TGraphErrors *gra_run3_pass2 = new TGraphErrors(3, pt_centr_run3, run3_reso_pass2, pt_width_run3, err_run3_reso_pass2);
    gra_run3_pass2 -> SetMarkerStyle(20);
    gra_run3_pass2 -> SetMarkerColor(kAzure+2);
    gra_run3_pass2 -> SetLineColor(kAzure+2);
    gra_run3_pass2 -> SetLineWidth(2);

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

    TH2D *histGrid = new TH2D("histGrid", "", 100, 0, 30, 100, 0.02, 0.35);
    histGrid -> SetTitleSize(0.05,"X");
    histGrid -> SetTitleSize(0.045,"Y");
    histGrid -> SetLabelSize(0.045,"X");
    histGrid -> SetLabelSize(0.045,"Y");
    histGrid -> SetTitleOffset(1.2,"X");
    histGrid -> SetTitleOffset(1.35,"Y");
    histGrid -> GetXaxis() -> SetTitle("#it{p}_{T} (GeV/#it{c})");
    histGrid -> GetYaxis() -> SetTitle("#sigma_{J/#psi} (GeV/#it{c}^{2})");

    TLegend *legend = new TLegend(0.55, 0.20, 0.75, 0.50, " ", "brNDC");
    legend -> SetBorderSize(0);
    legend -> SetFillColor(10);
    legend -> SetFillStyle(1);
    legend -> SetLineStyle(0);
    legend -> SetLineColor(0);
    legend -> SetTextFont(42);
    legend -> SetTextSize(0.04);
    legend -> AddEntry(gra_run2, "Run2 Data", "PL");
    legend -> AddEntry(gra_run3_pass1, "Run3 Data - pass1", "PL");
    legend -> AddEntry(gra_run3_pass2, "Run3 Data - pass2", "PL");
    legend -> AddEntry(gra_run3_mc_prompt, "Run3 MC prompt", "PL");
    legend -> AddEntry(gra_run3_mc_non_prompt, "Run3 MC non-prompt", "PL");

    TCanvas *canvas = new TCanvas("canvas", "", 800, 600);
    canvas -> SetLeftMargin(0.15);
    gPad -> SetLogy();
    histGrid -> Draw();
    gra_run2 -> Draw("EPsame");
    gra_run3_pass1 -> Draw("EPsame");
    gra_run3_pass2 -> Draw("EPsame");
    gra_run3_mc_prompt -> Draw("EPsame");
    gra_run3_mc_non_prompt -> Draw("EPsame");
    legend -> Draw("same");

    canvas -> SaveAs("run2_comparison.pdf");

    TLegend *legend_data = new TLegend(0.55, 0.20, 0.75, 0.50, " ", "brNDC");
    legend_data -> SetBorderSize(0);
    legend_data -> SetFillColor(10);
    legend_data -> SetFillStyle(1);
    legend_data -> SetLineStyle(0);
    legend_data -> SetLineColor(0);
    legend_data -> SetTextFont(42);
    legend_data -> SetTextSize(0.04);
    legend_data -> AddEntry(gra_run2, "Run2 Data", "PL");
    legend_data -> AddEntry(gra_run3_pass1, "Run3 Data - pass1", "PL");
    legend_data -> AddEntry(gra_run3_pass2, "Run3 Data - pass2", "PL");

    TCanvas *canvas_data = new TCanvas("canvas_data", "", 800, 600);
    canvas_data -> SetLeftMargin(0.15);
    gPad -> SetLogy();
    histGrid -> Draw();
    gra_run2 -> Draw("EPsame");
    gra_run3_pass1 -> Draw("EPsame");
    gra_run3_pass2 -> Draw("EPsame");
    legend_data -> Draw("same");

    canvas_data -> SaveAs("run2_comparison_data.pdf");
}