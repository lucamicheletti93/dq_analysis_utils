TH1D *histMass;
TH1D *histMass_sig;
TH1D *histMass_bkg;
TH1D *histTauz;
TH1D *histTauz_sig;
TH1D *histTauz_bkg;

void LoadStyle();
void BookHistograms();
void read_dilepton_table(const char *fileName = "dileptons_NonPromptJpsi.root", Bool_t cross_check = kFALSE){

  LoadStyle();
  BookHistograms();

  // Set paths and plot configurations
  const char *pathIn = "/home/luca/GITHUB/dq_analysis_utils/macro/data";
  const int rebin = 2;

  TFile *fIn = new TFile(Form("%s/%s", pathIn, fileName), "READ");
  TIter keyList(fIn->GetListOfKeys());
  TKey *key;
  Int_t dirCounter = 0;
  Int_t LSCounter = 0;
  Int_t OSCounter = 0;

  while ((key = (TKey*)keyList())) {
    TClass *cl = gROOT->GetClass(key->GetClassName());
    if (!cl->InheritsFrom("TDirectory")) continue;
    TDirectory *dir = (TDirectory*)key->ReadObj();

    TTreeReader treeReaderDileptons("Dileptons", dir);
    TTreeReaderValue<Float_t>   fMass(treeReaderDileptons, "fMass");
    TTreeReaderValue<Float_t>   fPt(treeReaderDileptons, "fPt");
    TTreeReaderValue<Int_t>     fSign(treeReaderDileptons, "fSign");
    TTreeReaderValue<uint32_t>  fFilterMap(treeReaderDileptons, "fFilterMap");

    TTreeReader treeReaderDileptonsExtra("DileptonsExtra", dir);
    TTreeReaderValue<Float_t> fTauz(treeReaderDileptonsExtra, "fTauz");

    while (treeReaderDileptons.Next() && treeReaderDileptonsExtra.Next()) {
       (*fSign != 0) ? LSCounter++ : OSCounter++;
       if (*fSign != 0) continue;
       histMass -> Fill(*fMass);
       histTauz -> Fill(*fTauz);
       (*fFilterMap > 0) ? histMass_sig -> Fill(*fMass) : histMass_bkg -> Fill(*fMass);
       (*fFilterMap > 0) ? histTauz_sig -> Fill(*fTauz) : histTauz_bkg -> Fill(*fTauz);
    }
    dirCounter++;
    cout << "OS: " << OSCounter << " - LS: " << LSCounter << endl;
  }

  // Histogram rebin
  histMass -> Rebin(rebin);
  histMass_sig -> Rebin(rebin);
  histMass_bkg -> Rebin(rebin);
  histTauz -> Rebin(rebin);
  histTauz_sig -> Rebin(rebin);
  histTauz_bkg -> Rebin(rebin);

  // Draw results
  TCanvas *canvasMassTauz = new TCanvas("canvasMassTauz", "", 1200, 600);
  canvasMassTauz -> Divide(2,1);

  canvasMassTauz -> cd(1);
  histMass -> Draw("EP");
  histMass_sig -> Draw("Hsame");
  histMass_bkg -> Draw("Hsame");

  TLegend *legendMassTauz = new TLegend(0.70,0.65,0.80,0.85," ","brNDC");
  legendMassTauz -> SetBorderSize(0);
  legendMassTauz -> SetFillColor(10);
  legendMassTauz -> SetFillStyle(1);
  legendMassTauz -> SetLineStyle(0);
  legendMassTauz -> SetLineColor(0);
  legendMassTauz -> SetTextFont(42);
  legendMassTauz -> SetTextSize(0.043);
  legendMassTauz -> AddEntry(histMass,"Data","PE");
  legendMassTauz -> AddEntry(histMass_sig,"Sig.","L");
  legendMassTauz -> AddEntry(histMass_bkg,"Bkg.","L");
  legendMassTauz -> Draw("same");

  canvasMassTauz -> cd(2);
  gPad -> SetLogy();
  histTauz -> Draw("EP");
  histTauz_sig -> Draw("Hsame");
  histTauz_bkg -> Draw("Hsame");


  if (cross_check){
    TFile *fIn_test = new TFile(Form("%s/AnalysisResults_test.root", pathIn), "READ");
    auto hlist_test = (THashList*) fIn_test -> Get("analysis-same-event-pairing/output");
    auto list_test = (TList*) hlist_test -> FindObject("PairsMuonSEPM_matchedGlobal");
    auto histMass_test = (TH1F*) list_test -> FindObject("Mass");
    histMass_test -> SetLineColor(kRed);
    auto histTauz_test = (TH1F*) list_test -> FindObject("Tauz");
    histTauz_test -> SetLineColor(kRed);

    TCanvas *canvasMassTauz_test = new TCanvas("canvasMassTauz_test", "", 1200, 600);
    canvasMassTauz_test -> Divide(2,1);

    canvasMassTauz_test -> cd(1);
    histMass -> Draw("EP");
    histMass_test -> Draw("Hsame");

    canvasMassTauz_test -> cd(2);
    gPad -> SetLogy();
    histTauz -> Draw("EP");
    histTauz_test -> Draw("Hsame");
  }

}
////////////////////////////////////////////////////////////////////////////////
void BookHistograms(){
  histMass = new TH1D("histMass", "", 120, 0., 5.);
  histMass -> GetXaxis() -> SetTitle("#it{M} (GeV/c^{2})");
  histMass -> SetMarkerStyle(20);
  histMass -> SetMarkerColor(kBlack);
  histMass -> SetLineColor(kBlack);
  histMass_sig = new TH1D("histMass_sig", "", 120, 0., 5.);
  histMass_sig -> GetXaxis() -> SetTitle("#it{M} (GeV/c^{2})");
  histMass_sig -> SetLineColor(kRed);
  histMass_sig -> SetLineWidth(2);
  histMass_sig -> SetFillColorAlpha(kRed, 0.3);
  histMass_bkg = new TH1D("histMass_bkg", "", 120, 0., 5.);
  histMass_bkg -> GetXaxis() -> SetTitle("#it{M} (GeV/c^{2})");
  histMass_bkg -> SetLineColor(kBlue);
  histMass_bkg -> SetLineWidth(2);

  histTauz = new TH1D("histTauz", "", 100, -0.01, 0.01);
  histTauz -> GetXaxis() -> SetTitle("#it{#tau}_{z}");
  histTauz -> SetMarkerStyle(20);
  histTauz -> SetMarkerColor(kBlack);
  histTauz -> SetLineColor(kBlack);
  histTauz_sig = new TH1D("histTauz_sig", "", 100, -0.01, 0.01);
  histTauz_sig -> GetXaxis() -> SetTitle("#it{#tau}_{z}");
  histTauz_sig -> SetLineColor(kRed);
  histTauz_sig -> SetLineWidth(2);
  histTauz_sig -> SetFillColorAlpha(kRed, 0.3);
  histTauz_bkg = new TH1D("histTauz_bkg", "", 100, -0.01, 0.01);
  histTauz_bkg -> GetXaxis() -> SetTitle("#it{#tau}_{z}");
  histTauz_bkg -> SetLineColor(kBlue);
  histTauz_bkg -> SetLineWidth(2);
}
////////////////////////////////////////////////////////////////////////////////
void LoadStyle(){
    int font = 42;
    TGaxis::SetMaxDigits(2);
    gStyle -> SetFrameBorderMode(0);
    gStyle -> SetFrameFillColor(0);
    gStyle -> SetCanvasBorderMode(0);
    gStyle -> SetPadBorderMode(0);
    gStyle -> SetPadColor(10);
    gStyle -> SetCanvasColor(10);
    gStyle -> SetTitleFillColor(10);
    gStyle -> SetTitleBorderSize(1);
    gStyle -> SetStatColor(10);
    gStyle -> SetStatBorderSize(1);
    gStyle -> SetLegendBorderSize(1);
    gStyle -> SetDrawBorder(0);
    gStyle -> SetTextFont(font);
    gStyle -> SetStatFontSize(0.05);
    gStyle -> SetStatX(0.97);
    gStyle -> SetStatY(0.98);
    gStyle -> SetStatH(0.03);
    gStyle -> SetStatW(0.3);
    gStyle -> SetTickLength(0.02,"y");
    gStyle -> SetEndErrorSize(3);
    gStyle -> SetLabelSize(0.04,"xyz");
    gStyle -> SetLabelFont(font,"xyz");
    gStyle -> SetLabelOffset(0.01,"xyz");
    gStyle -> SetTitleFont(font,"xyz");
    gStyle -> SetTitleOffset(0.9,"x");
    gStyle -> SetTitleOffset(1.02,"y");
    gStyle -> SetTitleSize(0.04,"xyz");
    gStyle -> SetMarkerSize(0.8);
    gStyle -> SetOptStat(0);
    gStyle -> SetEndErrorSize(0);
    gStyle -> SetCanvasPreferGL(kTRUE);
    gStyle -> SetHatchesSpacing(0.5);
}
