TH1D *histMass;
TH1D *histMassJpsi_sig;
TH1D *histMassPsi2S_sig;
TH1D *histMassPromptJpsi_sig;
TH1D *histMassNonPromptJpsi_sig;
TH1D *histMass_bkg;
TH1D *histTauz;
TH1D *histTauzJpsi_sig;
TH1D *histTauzPsi2S_sig;
TH1D *histTauzPromptJpsi_sig;
TH1D *histTauzNonPromptJpsi_sig;
TH1D *histTauz_bkg;
TH1D *histPt;
TH1D *histPtJpsi_sig;
TH1D *histPtPsi2S_sig;
TH1D *histPtPromptJpsi_sig;
TH1D *histPtNonPromptJpsi_sig;
TH1D *histPt_bkg;

TH2D *histMassPt;

void LoadStyle();
void BookHistograms();
void read_dilepton_table(const char *fileSuffix = "NonPromptJpsi",const char *fOutName = "NonPromptJpsi", Bool_t cross_check = kFALSE){

  LoadStyle();
  BookHistograms();

  // Set paths and plot configurations
  const char *pathIn = "/home/luca/GITHUB/dq_analysis_utils/macro/data";
  const int rebin = 1;

  TFile *fOut = new TFile(fOutName, "RECREATE");
  // Tree variables
  Float_t mass, pt, tauz;

  TTree *tree_sig = new TTree("tree_sig", "tree_sig");
  tree_sig -> Branch("fMass", &mass, "mass/F");
  tree_sig -> Branch("fPt", &pt, "pt/F");
  tree_sig -> Branch("fTauz", &tauz, "tauz/F");

  TTree *tree_bkg = new TTree("tree_bkg", "tree_bkg");
  tree_bkg -> Branch("fMass", &mass, "mass/F");
  tree_bkg -> Branch("fPt", &pt, "pt/F");
  tree_bkg -> Branch("fTauz", &tauz, "tauz/F");

  TFile *fIn = new TFile(Form("%s/dileptons_%s.root", pathIn, fileSuffix), "READ");
  TIter keyList(fIn->GetListOfKeys());
  TKey *key;
  Int_t dirCounter = 0;

  while ((key = (TKey*)keyList())) {
    TClass *cl = gROOT->GetClass(key->GetClassName());
    if (!cl->InheritsFrom("TDirectory")) continue;
    TDirectory *dir = (TDirectory*)key->ReadObj();

    TTreeReader treeReaderDileptons("Dileptons", dir);
    TTreeReaderValue<Float_t>   fMass(treeReaderDileptons, "fMass");
    TTreeReaderValue<Float_t>   fPt(treeReaderDileptons, "fPt");
    TTreeReaderValue<Float_t>   fEta(treeReaderDileptons, "fEta");
    TTreeReaderValue<Int_t>     fSign(treeReaderDileptons, "fSign");
    TTreeReaderValue<uint32_t>  fFilterMap(treeReaderDileptons, "fFilterMap");
    TTreeReaderValue<uint32_t>  fMcDecision(treeReaderDileptons, "fMcDecision");

    TTreeReader treeReaderDileptonsExtra("DileptonsExtra", dir);
    TTreeReaderValue<Float_t> fTauz(treeReaderDileptonsExtra, "fTauz");

    while (treeReaderDileptons.Next() && treeReaderDileptonsExtra.Next()) {
      if (*fSign != 0) continue;
      //if (TMath::Abs(*fEta) > 2.5 && TMath::Abs(*fEta) < 4.) continue;

      mass = *fMass;
      pt = *fPt;
      tauz = *fTauz;

      histMass -> Fill(*fMass);
      histTauz -> Fill(*fTauz);
      histPt -> Fill(*fPt);

      if (*fMcDecision == 0) {
        histMass_bkg -> Fill(*fMass);
        histTauz_bkg -> Fill(*fTauz);
        histPt_bkg -> Fill(*fPt);
        tree_bkg -> Fill();
        histMassPt -> Fill(*fMass, *fPt);
      }

      if (*fMcDecision == 1) {
        histMassJpsi_sig -> Fill(*fMass);
        histTauzJpsi_sig -> Fill(*fTauz);
        histPtJpsi_sig -> Fill(*fPt);
        tree_sig -> Fill();
        histMassPt -> Fill(*fMass, *fPt);
      }

      if (*fMcDecision == 2) {
        histMassPsi2S_sig -> Fill(*fMass);
        histTauzPsi2S_sig -> Fill(*fTauz);
        histPtPsi2S_sig -> Fill(*fPt);
      }
    }
    dirCounter++;
  }

  fOut -> cd();
  tree_sig -> Write();
  tree_bkg -> Write();
  fOut -> Close();

  // Histogram rebin
  histMass -> Rebin(rebin);
  histMassJpsi_sig -> Rebin(rebin);
  histMass_bkg -> Rebin(rebin);
  histTauz -> Rebin(rebin);
  histTauzJpsi_sig -> Rebin(rebin);
  histTauz_bkg -> Rebin(rebin);

  // Draw results
  TCanvas *canvasMassTauzPt = new TCanvas("canvasMassTauzPt", "", 1800, 600);
  canvasMassTauzPt -> Divide(3,1);

  canvasMassTauzPt -> cd(1);
  gPad -> SetLogy();
  histMass -> GetXaxis() -> SetRangeUser(2., 5.);
  histMass -> Draw("EP");
  histMassJpsi_sig -> Draw("Hsame");
  histMassPsi2S_sig -> Draw("Hsame");
  histMass_bkg -> Draw("Hsame");

  TLegend *legendMassTauz = new TLegend(0.70,0.60,0.85,0.85," ","brNDC");
  legendMassTauz -> SetBorderSize(0);
  legendMassTauz -> SetFillColor(10);
  legendMassTauz -> SetFillStyle(1);
  legendMassTauz -> SetLineStyle(0);
  legendMassTauz -> SetLineColor(0);
  legendMassTauz -> SetTextFont(42);
  legendMassTauz -> SetTextSize(0.043);
  legendMassTauz -> AddEntry(histMass,"Data","PE");
  legendMassTauz -> AddEntry(histMassJpsi_sig,"J/#psi","F");
  legendMassTauz -> AddEntry(histMassPsi2S_sig,"#psi(2S)","F");
  legendMassTauz -> AddEntry(histMass_bkg,"Bkg.","L");
  legendMassTauz -> Draw("same");

  canvasMassTauzPt -> cd(2);
  gPad -> SetLogy();
  histTauz -> Draw("EP");
  histTauzJpsi_sig -> Draw("Hsame");
  histTauzPsi2S_sig -> Draw("Hsame");
  histTauz_bkg -> Draw("Hsame");

  canvasMassTauzPt -> cd(3);
  gPad -> SetLogy();
  histPt -> Draw("EP");
  histPtJpsi_sig -> Draw("Hsame");
  histPtPsi2S_sig -> Draw("Hsame");
  histPt_bkg -> Draw("Hsame");


  TCanvas *canvasMassPt = new TCanvas("canvasMassPt", "", 600, 600);
  histMassPt -> Draw("COLZ");

  if (cross_check){
    TFile *fIn_test = new TFile(Form("%s/AnalysisResults_%s.root", pathIn, fileSuffix), "READ");
    auto hlist_test = (THashList*) fIn_test -> Get("analysis-same-event-pairing/output");
    auto list_test = (TList*) hlist_test -> FindObject("PairsMuonSEPM_matchedGlobal_mumuFromJpsi");
    auto histMass_test = (TH1F*) list_test -> FindObject("Mass");
    histMass_test -> SetLineColor(kBlack);
    histMass_test -> SetLineWidth(2);
    histMass_test -> SetMarkerColor(kBlack);
    auto histTauz_test = (TH1F*) list_test -> FindObject("Tauz");
    histTauz_test -> SetLineColor(kBlack);
    histTauz_test -> SetLineWidth(2);
    histTauz_test -> SetMarkerColor(kBlack);

    TLegend *legendMassTauz_test = new TLegend(0.20,0.65,0.40,0.85," ","brNDC");
    legendMassTauz_test -> SetBorderSize(0);
    legendMassTauz_test -> SetFillColor(10);
    legendMassTauz_test -> SetFillStyle(1);
    legendMassTauz_test -> SetLineStyle(0);
    legendMassTauz_test -> SetLineColor(0);
    legendMassTauz_test -> SetTextFont(42);
    legendMassTauz_test -> SetTextSize(0.033);
    legendMassTauz_test -> AddEntry(histMassJpsi_sig,"Dilepton table","F");
    legendMassTauz_test -> AddEntry(histMass_test,"Analysis results","PE");

    auto canvasRpMass = new TCanvas("canvasRpMass", "canvasRpMass");
    canvasRpMass -> cd();
    auto rpMass = new TRatioPlot(histMassJpsi_sig, histMass_test);
    canvasRpMass -> SetTicks(0, 1);
    rpMass -> Draw();
    legendMassTauz_test -> Draw("same");
    canvasRpMass -> Update();

    auto canvasRpTauz = new TCanvas("canvasRpTauz", "canvasRpTauz");
    canvasRpTauz -> cd();
    auto rpTauz = new TRatioPlot(histTauzJpsi_sig, histTauz_test);
    canvasRpTauz -> SetTicks(0, 1);
    rpTauz -> Draw();
    legendMassTauz_test -> Draw("same");
    canvasRpTauz -> Update();
  }

}
////////////////////////////////////////////////////////////////////////////////
void combine_datasets(){
  LoadStyle();
  BookHistograms();

  TFile *fInPromptJpsi = new TFile("promptJpsi.root", "READ");

  TTreeReader treeReaderPromptJpsi_sig("tree_sig", fInPromptJpsi);
  TTreeReaderValue<Float_t>   fMassPromptJpsi_sig(treeReaderPromptJpsi_sig, "fMass");
  TTreeReaderValue<Float_t>   fPtPromptJpsi_sig(treeReaderPromptJpsi_sig, "fPt");
  TTreeReaderValue<Float_t>   fTauzPromptJpsi_sig(treeReaderPromptJpsi_sig, "fTauz");

  while (treeReaderPromptJpsi_sig.Next()) {
    histMassPromptJpsi_sig -> Fill(*fMassPromptJpsi_sig);
    histPtPromptJpsi_sig -> Fill(*fPtPromptJpsi_sig);
    histTauzPromptJpsi_sig -> Fill(*fTauzPromptJpsi_sig);
    histMass -> Fill(*fMassPromptJpsi_sig);
    histPt -> Fill(*fPtPromptJpsi_sig);
    histTauz -> Fill(*fTauzPromptJpsi_sig);
  }

  TTreeReader treeReaderPromptJpsi_bkg("tree_bkg", fInPromptJpsi);
  TTreeReaderValue<Float_t>   fMassPromptJpsi_bkg(treeReaderPromptJpsi_bkg, "fMass");
  TTreeReaderValue<Float_t>   fPtPromptJpsi_bkg(treeReaderPromptJpsi_bkg, "fPt");
  TTreeReaderValue<Float_t>   fTauzPromptJpsi_bkg(treeReaderPromptJpsi_bkg, "fTauz");

  while (treeReaderPromptJpsi_bkg.Next()) {
    histMass_bkg -> Fill(*fMassPromptJpsi_bkg);
    histPt_bkg -> Fill(*fPtPromptJpsi_bkg);
    histTauz_bkg -> Fill(*fTauzPromptJpsi_bkg);
    histMass -> Fill(*fMassPromptJpsi_bkg);
    histPt -> Fill(*fPtPromptJpsi_bkg);
    histTauz -> Fill(*fTauzPromptJpsi_bkg);
  }

  TFile *fInNonPromptJpsi = new TFile("nonPromptJpsi.root", "READ");

  TTreeReader treeReaderNonPromptJpsi_sig("tree_sig", fInNonPromptJpsi);
  TTreeReaderValue<Float_t>   fMassNonPromptJpsi_sig(treeReaderNonPromptJpsi_sig, "fMass");
  TTreeReaderValue<Float_t>   fPtNonPromptJpsi_sig(treeReaderNonPromptJpsi_sig, "fPt");
  TTreeReaderValue<Float_t>   fTauzNonPromptJpsi_sig(treeReaderNonPromptJpsi_sig, "fTauz");

  while (treeReaderNonPromptJpsi_sig.Next()) {
    histMassNonPromptJpsi_sig -> Fill(*fMassNonPromptJpsi_sig);
    histPtNonPromptJpsi_sig -> Fill(*fPtNonPromptJpsi_sig);
    histTauzNonPromptJpsi_sig -> Fill(*fTauzNonPromptJpsi_sig);
    histMass -> Fill(*fMassNonPromptJpsi_sig);
    histPt -> Fill(*fPtNonPromptJpsi_sig);
    histTauz -> Fill(*fTauzNonPromptJpsi_sig);
  }

  TTreeReader treeReaderNonPromptJpsi_bkg("tree_bkg", fInNonPromptJpsi);
  TTreeReaderValue<Float_t>   fMassNonPromptJpsi_bkg(treeReaderNonPromptJpsi_bkg, "fMass");
  TTreeReaderValue<Float_t>   fPtNonPromptJpsi_bkg(treeReaderNonPromptJpsi_bkg, "fPt");
  TTreeReaderValue<Float_t>   fTauzNonPromptJpsi_bkg(treeReaderNonPromptJpsi_bkg, "fTauz");

  while (treeReaderNonPromptJpsi_bkg.Next()) {
    histMass_bkg -> Fill(*fMassNonPromptJpsi_bkg);
    histPt_bkg -> Fill(*fPtNonPromptJpsi_bkg);
    histTauz_bkg -> Fill(*fTauzNonPromptJpsi_bkg);
    histMass -> Fill(*fMassNonPromptJpsi_bkg);
    histPt -> Fill(*fPtNonPromptJpsi_bkg);
    histTauz -> Fill(*fTauzNonPromptJpsi_bkg);
  }


  // Draw results
  TCanvas *canvasMassTauzPt = new TCanvas("canvasMassTauzPt", "", 1800, 600);
  canvasMassTauzPt -> Divide(3,1);

  canvasMassTauzPt -> cd(1);
  gPad -> SetLogy();
  histMass -> Draw("EP");
  histMassPromptJpsi_sig -> Draw("Hsame");
  histMassNonPromptJpsi_sig -> Draw("Hsame");
  histMass_bkg -> Draw("Hsame");

  TLegend *legendMassTauz = new TLegend(0.20,0.65,0.40,0.85," ","brNDC");
  legendMassTauz -> SetBorderSize(0);
  legendMassTauz -> SetFillColor(10);
  legendMassTauz -> SetFillStyle(1);
  legendMassTauz -> SetLineStyle(0);
  legendMassTauz -> SetLineColor(0);
  legendMassTauz -> SetTextFont(42);
  legendMassTauz -> SetTextSize(0.033);
  legendMassTauz -> AddEntry(histMass,"Data","PE");
  legendMassTauz -> AddEntry(histMassPromptJpsi_sig,"J/#psi prompt","F");
  legendMassTauz -> AddEntry(histMassNonPromptJpsi_sig,"J/#psi from B","F");
  legendMassTauz -> AddEntry(histMass_bkg,"Bakground","L");
  legendMassTauz -> Draw("same");

  canvasMassTauzPt -> cd(2);
  gPad -> SetLogy();
  histTauz -> Draw("EP");
  histTauzPromptJpsi_sig -> Draw("Hsame");
  histTauzNonPromptJpsi_sig -> Draw("Hsame");
  histTauz_bkg -> Draw("Hsame");

  canvasMassTauzPt -> cd(3);
  gPad -> SetLogy();
  histPt -> Draw("EP");
  histPtPromptJpsi_sig -> Draw("Hsame");
  histPtNonPromptJpsi_sig -> Draw("Hsame");
  histPt_bkg -> Draw("Hsame");

}
////////////////////////////////////////////////////////////////////////////////
void BookHistograms(){
  const float ptBins[]   = {0., 1., 2., 3., 4., 5., 7., 10., 15., 20.};

  histMass = new TH1D("histMass", "", 125, 0., 5.);
  histMass -> GetXaxis() -> SetTitle("#it{M} (GeV/c^{2})");
  histMass -> SetMarkerStyle(20);
  histMass -> SetMarkerColor(kBlack);
  histMass -> SetLineColor(kBlack);
  histMassJpsi_sig = new TH1D("histMassJpsi_sig", "", 125, 0., 5.);
  histMassJpsi_sig -> GetXaxis() -> SetTitle("#it{M} (GeV/c^{2})");
  histMassJpsi_sig -> SetLineColor(kOrange+7);
  histMassJpsi_sig -> SetLineWidth(2);
  histMassJpsi_sig -> SetFillColorAlpha(kOrange+7, 0.3);
  histMassPsi2S_sig = new TH1D("histMassPsi2S_sig", "", 125, 0., 5.);
  histMassPsi2S_sig -> GetXaxis() -> SetTitle("#it{M} (GeV/c^{2})");
  histMassPsi2S_sig -> SetLineColor(kGreen+1);
  histMassPsi2S_sig -> SetLineWidth(2);
  histMassPsi2S_sig -> SetFillColorAlpha(kGreen+1, 0.3);
  histMassPromptJpsi_sig = new TH1D("histMassPromptJpsi_sig", "", 125, 0., 5.);
  histMassPromptJpsi_sig -> GetXaxis() -> SetTitle("#it{M} (GeV/c^{2})");
  histMassPromptJpsi_sig -> SetLineColor(kOrange+7);
  histMassPromptJpsi_sig -> SetLineWidth(2);
  histMassPromptJpsi_sig -> SetFillColorAlpha(kOrange+7, 0.3);
  histMassNonPromptJpsi_sig = new TH1D("histMassNonPromptJpsi_sig", "", 125, 0., 5.);
  histMassNonPromptJpsi_sig -> GetXaxis() -> SetTitle("#it{M} (GeV/c^{2})");
  histMassNonPromptJpsi_sig -> SetLineColor(kAzure+7);
  histMassNonPromptJpsi_sig -> SetLineWidth(2);
  histMassNonPromptJpsi_sig -> SetFillColorAlpha(kAzure+7, 0.3);
  histMass_bkg = new TH1D("histMass_bkg", "", 125, 0., 5.);
  histMass_bkg -> GetXaxis() -> SetTitle("#it{M} (GeV/c^{2})");
  histMass_bkg -> SetLineColor(kRed);
  histMass_bkg -> SetLineWidth(2);

  histTauz = new TH1D("histTauz", "", 100, -0.01, 0.01);
  histTauz -> GetXaxis() -> SetTitle("#it{#tau}_{z} (ps)");
  histTauz -> SetMarkerStyle(20);
  histTauz -> SetMarkerColor(kBlack);
  histTauz -> SetLineColor(kBlack);
  histTauz -> GetYaxis() -> SetRangeUser(1., 2e5);
  histTauzJpsi_sig = new TH1D("histTauzJpsi_sig", "", 100, -0.01, 0.01);
  histTauzJpsi_sig -> GetXaxis() -> SetTitle("#it{#tau}_{z} (ps)");
  histTauzJpsi_sig -> SetLineColor(kOrange+7);
  histTauzJpsi_sig -> SetLineWidth(2);
  histTauzJpsi_sig -> SetFillColorAlpha(kOrange+7, 0.3);
  histTauzPsi2S_sig = new TH1D("histTauzPsi2S_sig", "", 100, -0.01, 0.01);
  histTauzPsi2S_sig -> GetXaxis() -> SetTitle("#it{#tau}_{z} (ps)");
  histTauzPsi2S_sig -> SetLineColor(kGreen+1);
  histTauzPsi2S_sig -> SetLineWidth(2);
  histTauzPsi2S_sig -> SetFillColorAlpha(kGreen+1, 0.3);
  histTauzPromptJpsi_sig = new TH1D("histTauzPromptJpsi_sig", "", 100, -0.01, 0.01);
  histTauzPromptJpsi_sig -> GetXaxis() -> SetTitle("#it{#tau}_{z} (ps)");
  histTauzPromptJpsi_sig -> SetLineColor(kOrange+7);
  histTauzPromptJpsi_sig -> SetLineWidth(2);
  histTauzPromptJpsi_sig -> SetFillColorAlpha(kOrange+7, 0.3);
  histTauzNonPromptJpsi_sig = new TH1D("histTauzNonPromptJpsi_sig", "", 100, -0.01, 0.01);
  histTauzNonPromptJpsi_sig -> GetXaxis() -> SetTitle("#it{#tau}_{z} (ps)");
  histTauzNonPromptJpsi_sig -> SetLineColor(kAzure+7);
  histTauzNonPromptJpsi_sig -> SetLineWidth(2);
  histTauzNonPromptJpsi_sig -> SetFillColorAlpha(kAzure+7, 0.3);
  histTauz_bkg = new TH1D("histTauz_bkg", "", 100, -0.01, 0.01);
  histTauz_bkg -> GetXaxis() -> SetTitle("#it{#tau}_{z} (ps)");
  histTauz_bkg -> SetLineColor(kRed);
  histTauz_bkg -> SetLineWidth(2);

  histPt = new TH1D("histPt", "", 200, 0., 20.);
  histPt -> GetXaxis() -> SetTitle("#it{p}_{T} (GeV/#it{c})");
  histPt -> SetMarkerStyle(20);
  histPt -> SetMarkerColor(kBlack);
  histPt -> SetLineColor(kBlack);
  histPtJpsi_sig = new TH1D("histPtJpsi_sig", "", 200, 0., 20.);
  histPtJpsi_sig -> GetXaxis() -> SetTitle("#it{p}_{T} (GeV/#it{c})");
  histPtJpsi_sig -> SetLineColor(kOrange+7);
  histPtJpsi_sig -> SetLineWidth(2);
  histPtJpsi_sig -> SetFillColorAlpha(kOrange+7, 0.3);
  histPtPsi2S_sig = new TH1D("histPtPsi2S_sig", "", 200, 0., 20.);
  histPtPsi2S_sig -> GetXaxis() -> SetTitle("#it{p}_{T} (GeV/#it{c})");
  histPtPsi2S_sig -> SetLineColor(kGreen+1);
  histPtPsi2S_sig -> SetLineWidth(2);
  histPtPsi2S_sig -> SetFillColorAlpha(kGreen+1, 0.3);
  histPtPromptJpsi_sig = new TH1D("histPtPromptJpsi_sig", "", 200, 0., 20.);
  histPtPromptJpsi_sig -> GetXaxis() -> SetTitle("#it{p}_{T} (GeV/#it{c})");
  histPtPromptJpsi_sig -> SetLineColor(kOrange+7);
  histPtPromptJpsi_sig -> SetLineWidth(2);
  histPtPromptJpsi_sig -> SetFillColorAlpha(kOrange+7, 0.3);
  histPtNonPromptJpsi_sig = new TH1D("histPtNonPromptJpsi_sig", "", 200, 0., 20.);
  histPtNonPromptJpsi_sig -> GetXaxis() -> SetTitle("#it{p}_{T} (GeV/#it{c})");
  histPtNonPromptJpsi_sig -> SetLineColor(kAzure+7);
  histPtNonPromptJpsi_sig -> SetLineWidth(2);
  histPtNonPromptJpsi_sig -> SetFillColorAlpha(kAzure+7, 0.3);
  histPt_bkg = new TH1D("histPt_bkg", "", 200, 0., 20.);
  histPt_bkg -> GetXaxis() -> SetTitle("#it{p}_{T} (GeV/#it{c})");
  histPt_bkg -> SetLineColor(kRed);
  histPt_bkg -> SetLineWidth(2);

  histMassPt = new TH2D("histMassPt", "", 125, 0., 5., 20, 0., 20.);
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
