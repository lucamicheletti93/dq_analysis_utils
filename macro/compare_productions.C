void DrawRatioPlot(TH1F *, TH1F *, TString , TString);
void LoadStyle();

Long_t *dummy1 = 0, *dummy2 = 0, *dummy3 = 0, *dummy4 = 0;
TString output_dir_name = "figures/qc";
TString name1;
TString name2;

// Available productions.q
// TM_LHC22c5_HL.root
// TM_LHC22c5_HL_apass3.root
// TM_LHC22c5_HL_apass4.root

void compare_productions(const char *name_fIn1 = "TM_OCT_apass3_HL.root", const char *name_fIn2 = "TM_OCT_apass4_HL.root"){
  //LoadStyle();
  const char *path_fIn = "/Users/lucamicheletti/GITHUB/dq_analysis_utils/o2/output";
  TString prod_pass = "/apass3_apass4";
  output_dir_name = output_dir_name + prod_pass;
  name1 = name_fIn1;
  name2 = name_fIn2;

  if(gSystem -> GetPathInfo(Form("%s", output_dir_name.Data()), dummy1, dummy2, dummy3, dummy4) != 0){
    gSystem -> Exec(Form("mkdir -p %s", output_dir_name.Data()));
  }

  TH1F *hist1dVar1[10][10], *hist1dVar2[10][10];
  TH2F *hist2dVar1[10][10], *hist2dVar2[10][10];
  TH1F *hist2dVar1Proj[10][10], *hist2dVar2Proj[10][10];
  std::vector<TString> dirName;
  std::vector<TString> hist1dName;
  std::vector<TString> hist2dName;
  int dirNum;
  int hist1dNum;
  int hist2dNum;

  TString initDirName[] = {"TrackBarrel_BeforeCuts", "TrackBarrel_jpsiO2MCdebugCuts"};
  TString initHist1dName[] = {"Pt", "Eta", "Phi", "DCAxy", "DCAz", "DCAsigXY", "DCAsigZ", "ITSncls", "ITSchi2", "TPCncls", "TPCchi2"};
  TString initHist2dName[] = {"TPCdedx_pIN", "TOFbeta_pIN", "TPCnSigEle_pIN", "TOFnSigEle_pIN", "Pt_DCAsigXY", "Pt_DCAsigZ"};
  dirNum = sizeof(initDirName)/sizeof(initDirName[0]);
  hist1dNum = sizeof(initHist1dName)/sizeof(initHist1dName[0]);
  hist2dNum = sizeof(initHist2dName)/sizeof(initHist2dName[0]);
  copy(initDirName,    initDirName+dirNum,       back_inserter(dirName));
  copy(initHist1dName, initHist1dName+hist1dNum, back_inserter(hist1dName));
  copy(initHist2dName, initHist2dName+hist2dNum, back_inserter(hist2dName));

  TFile *fIn1   = new TFile(Form("%s/AnalysisResults%s", path_fIn, name_fIn1), "READ");
  TString mainDirName1 = "table-maker";
  if(!name1.Contains("apass")){
    mainDirName1 += "-mc";
  }

  TFile *fIn2 = new TFile(Form("%s/AnalysisResults%s", path_fIn, name_fIn2), "READ");
  TString mainDirName2 = "table-maker";
  if(!name2.Contains("apass")){
    mainDirName2 += "-mc";
  }

  auto hlist1 = (THashList*) fIn1 -> Get(Form("%s/output", mainDirName1.Data()));
  auto hlist2 = (THashList*) fIn2 -> Get(Form("%s/output", mainDirName2.Data()));
  for(int iDir = 0;iDir < dirNum;iDir++){
    auto list1   = (TList*) hlist1 -> FindObject(dirName[iDir].Data());
    auto list2 = (TList*) hlist2 -> FindObject(dirName[iDir].Data());
    for(int iHist1d = 0;iHist1d < hist1dNum;iHist1d++){
      hist1dVar1[iDir][iHist1d] = (TH1F*) list1 -> FindObject(hist1dName[iHist1d].Data());
      hist1dVar1[iDir][iHist1d] -> SetName(dirName[iDir]);
      hist1dVar2[iDir][iHist1d] = (TH1F*) list2 -> FindObject(hist1dName[iHist1d].Data());
      hist1dVar2[iDir][iHist1d] -> SetName(dirName[iDir]);

      hist1dVar1[iDir][iHist1d] -> Scale(1. / hist1dVar1[iDir][iHist1d] -> Integral());
      hist1dVar1[iDir][iHist1d] -> SetMarkerStyle(20);
      hist1dVar1[iDir][iHist1d] -> SetMarkerSize(0.6);
      hist1dVar1[iDir][iHist1d] -> SetMarkerColor(kRed+1);
      hist1dVar1[iDir][iHist1d] -> SetLineColor(kRed+1);

      hist1dVar2[iDir][iHist1d] -> Scale(1. / hist1dVar2[iDir][iHist1d] -> Integral());
      hist1dVar2[iDir][iHist1d] -> SetMarkerStyle(24);
      hist1dVar2[iDir][iHist1d] -> SetMarkerSize(0.6);
      hist1dVar2[iDir][iHist1d] -> SetMarkerColor(kBlue+1);
      hist1dVar2[iDir][iHist1d] -> SetLineColor(kBlue+1);
    }
    for(int iHist2d = 0;iHist2d < hist2dNum;iHist2d++){
      hist2dVar1[iDir][iHist2d] = (TH2F*) list1 -> FindObject(hist2dName[iHist2d].Data());
      hist2dVar1[iDir][iHist2d] -> SetName(dirName[iDir]);
      hist2dVar2[iDir][iHist2d] = (TH2F*) list2 -> FindObject(hist2dName[iHist2d].Data());
      hist2dVar2[iDir][iHist2d] -> SetName(dirName[iDir]);

      // Save projections
      hist2dVar1Proj[iDir][iHist2d] = (TH1F*) hist2dVar1[iDir][iHist2d] -> ProjectionY();
      hist2dVar1Proj[iDir][iHist2d] -> SetName(Form("1_proj_%s", dirName[iDir].Data()));
      hist2dVar1Proj[iDir][iHist2d] -> Scale(1. / hist2dVar1Proj[iDir][iHist2d] -> Integral());
      hist2dVar1Proj[iDir][iHist2d] -> SetMarkerStyle(20);
      hist2dVar1Proj[iDir][iHist2d] -> SetMarkerSize(0.6);
      hist2dVar1Proj[iDir][iHist2d] -> SetMarkerColor(kRed+1);
      hist2dVar1Proj[iDir][iHist2d] -> SetLineColor(kRed+1);

      hist2dVar2Proj[iDir][iHist2d] = (TH1F*) hist2dVar2[iDir][iHist2d] -> ProjectionY();
      hist2dVar2Proj[iDir][iHist2d] -> SetName(Form("2_proj_%s", dirName[iDir].Data()));
      hist2dVar2Proj[iDir][iHist2d] -> Scale(1. / hist2dVar2Proj[iDir][iHist2d] -> Integral());
      hist2dVar2Proj[iDir][iHist2d] -> SetMarkerStyle(24);
      hist2dVar2Proj[iDir][iHist2d] -> SetMarkerSize(0.6);
      hist2dVar2Proj[iDir][iHist2d] -> SetMarkerColor(kBlue+1);
      hist2dVar2Proj[iDir][iHist2d] -> SetLineColor(kBlue+1);
    }
  }

  // dE/dx projections
  Double_t pinProj[] = {0, 0.6, 2, 10};
  Int_t    pinNum = sizeof(pinProj)/sizeof(pinProj[0]);
  Int_t    pinMin, pinMax;

  vector <TH1F*> histProj2[hist2dNum];
  vector <TH1F*> histProj1[hist2dNum];

  for(int iHist2d = 0;iHist2d < hist2dNum;iHist2d++){
    for(int iPin = 0;iPin < pinNum-1;iPin++){
      pinMin = hist2dVar2[0][iHist2d] -> GetXaxis() -> FindBin(pinProj[iPin]);
      pinMax = hist2dVar2[0][iHist2d] -> GetXaxis() -> FindBin(pinProj[iPin+1]);

      histProj2[iHist2d].push_back((TH1F*) hist2dVar2[0][iHist2d] -> ProjectionY(Form("hist_%s_2_Pt_%2.1f_%2.1f", hist2dName[iHist2d].Data(), pinProj[iPin], pinProj[iPin+1]), pinMin, pinMax));
      histProj2[iHist2d][iPin] -> SetTitle(Form("%2.1f < p_{in} < %2.1f GeV/c", pinProj[iPin], pinProj[iPin+1]));
      histProj2[iHist2d][iPin] -> Scale(1. / histProj2[iHist2d][iPin] -> Integral());
      histProj2[iHist2d][iPin] -> SetMarkerStyle(24);
      histProj2[iHist2d][iPin] -> SetMarkerSize(0.6);
      histProj2[iHist2d][iPin] -> SetMarkerColor(kBlue+1);
      histProj2[iHist2d][iPin] -> SetLineColor(kBlue+1);
      histProj2[iHist2d][iPin] -> Rebin(1);

      histProj1[iHist2d].push_back((TH1F*) hist2dVar1[0][iHist2d] -> ProjectionY(Form("hist_%s_1_Pt_%2.1f_%2.1f", hist2dName[iHist2d].Data(), pinProj[iPin], pinProj[iPin+1]), pinMin, pinMax));
      histProj1[iHist2d][iPin] -> SetTitle(Form("%2.1f < p_{in} < %2.1f GeV/c", pinProj[iPin], pinProj[iPin+1]));
      histProj1[iHist2d][iPin] -> Scale(1. / histProj1[iHist2d][iPin] -> Integral());
      histProj1[iHist2d][iPin] -> SetMarkerStyle(20);
      histProj1[iHist2d][iPin] -> SetMarkerSize(0.6);
      histProj1[iHist2d][iPin] -> SetMarkerColor(kRed+1);
      histProj1[iHist2d][iPin] -> SetLineColor(kRed+1);
      histProj1[iHist2d][iPin] -> Rebin(1);

      DrawRatioPlot(histProj1[iHist2d][iPin], histProj2[iHist2d][iPin], output_dir_name, Form("hist_%s_Pt_%2.1f_%2.1f", hist2dName[iHist2d].Data(), pinProj[iPin], pinProj[iPin+1]));
    }
  }


  for(int iHist2d = 0;iHist2d < hist2dNum;iHist2d++){
    auto canvasVar = new TCanvas("canvasVar", "",  600*dirNum, 600);
    canvasVar -> Divide(dirNum,1);
    for(int iDir = 0;iDir < dirNum;iDir++){
      canvasVar -> cd(iDir+1);
      if(hist2dName[iHist2d].Contains("TPCdedx") || hist2dName[iHist2d].Contains("TOFbeta")){
        gPad -> SetLogx(1);
      }
      hist2dVar1[iDir][iHist2d] -> Draw("COLZ");
    }
    canvasVar -> SaveAs(Form("%s/%s_1.pdf", output_dir_name.Data(), hist2dName[iHist2d].Data()));
    delete canvasVar;
  }

  for(int iHist2d = 0;iHist2d < hist2dNum;iHist2d++){
    auto canvasVar = new TCanvas("canvasVar", "",  600*dirNum, 600);
    canvasVar -> Divide(dirNum,1);
    for(int iDir = 0;iDir < dirNum;iDir++){
      canvasVar -> cd(iDir+1);
      if(hist2dName[iHist2d].Contains("TPCdedx") || hist2dName[iHist2d].Contains("TOFbeta")){
        gPad -> SetLogx(1);
      }
      hist2dVar2[iDir][iHist2d] -> Draw("COLZ");
    }
    canvasVar -> SaveAs(Form("%s/%s_2.pdf", output_dir_name.Data(), hist2dName[iHist2d].Data()));
    delete canvasVar;
  }


  // Ratio of projections
  for(int iDir = 0;iDir < dirNum;iDir++){
    for(int iHist2d = 0;iHist2d < hist2dNum;iHist2d++){
      DrawRatioPlot(hist2dVar1Proj[iDir][iHist2d], hist2dVar2Proj[iDir][iHist2d], output_dir_name, initHist2dName[iHist2d] + initDirName[iDir]);
    }
  }

  // Ratio of of 1D plots
  for(int iDir = 0;iDir < dirNum;iDir++){
    for(int iHist1d = 0;iHist1d < hist1dNum;iHist1d++){
      DrawRatioPlot(hist1dVar1[iDir][iHist1d], hist1dVar2[iDir][iHist1d], output_dir_name, initHist1dName[iHist1d] + initDirName[iDir]);
    }
  }

}
////////////////////////////////////////////////////////////////////////////////
void DrawRatioPlot(TH1F *hist1, TH1F *hist2, TString dirName, TString plotName){
  gStyle->SetOptStat(0);
  auto canvas = new TCanvas("canvas", "A ratio example");
  auto ratioPlot = new TRatioPlot(hist1, hist2);
  ratioPlot -> Draw();
  ratioPlot -> GetLowerRefYaxis() -> SetRangeUser(0.,2.);
  ratioPlot -> GetLowerRefYaxis() -> SetLabelSize(0.025);

  TPad *tmpPad = ratioPlot -> GetUpperPad();

  TLegend *legend = new TLegend(0.15, 0.75, 0.35, 0.89, " ", "brNDC");
  legend -> SetBorderSize(0);
  legend -> SetFillColor(10);
  legend -> SetFillStyle(1);
  legend -> SetLineStyle(0);
  legend -> SetLineColor(0);
  legend -> SetTextFont(42);
  legend -> SetTextSize(0.03);
  if(plotName.Contains("DCA")){
    legend -> AddEntry(hist1, Form("%s (mean = %3.2f)", name1.Data(), hist1 -> GetMean()), "PL");
    legend -> AddEntry(hist2, Form("%s (mean = %3.2f)", name2.Data(), hist2 -> GetMean()), "PL");
  } else {
    legend -> AddEntry(hist1, Form("%s", name1.Data()), "PL");
    legend -> AddEntry(hist2, Form("%s", name2.Data()), "PL");
  }
  legend -> Draw();

  tmpPad -> Modified(); 
  tmpPad -> Update(); 

  canvas -> Update();
  canvas -> SaveAs(Form("%s/ratio_%s.pdf", dirName.Data(), plotName.Data()));
  delete canvas;
  delete ratioPlot;
}
////////////////////////////////////////////////////////////////////////////////
void LoadStyle(){
  int font = 42;
  //TGaxis::SetMaxDigits(2);
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
  gStyle -> SetMarkerSize(0.5);
  gStyle -> SetOptStat(111111);
  gStyle -> SetEndErrorSize(0);
  gStyle -> SetCanvasPreferGL(kTRUE);
  gStyle -> SetHatchesSpacing(0.5);
  gStyle -> SetOptTitle(0);
  gStyle -> SetLineWidth(2);
  gStyle -> SetPadLeftMargin(0.15);
  gStyle -> SetPadBottomMargin(0.15);
  gStyle -> SetPadTopMargin(0.05);
  gStyle -> SetPadRightMargin(0.05);
  gStyle -> SetTitleSize(0.06);
  gStyle -> SetTitleSize(0.06,"Y");
  gStyle -> SetTitleOffset(1,"Y");
  gStyle -> SetTitleOffset(1,"X");
  gStyle -> SetLabelSize(0.05);
  gStyle -> SetLabelSize(0.05,"Y");
  gStyle -> SetFrameLineWidth(2);
  gStyle -> SetNdivisions(505,"X");
  gStyle -> SetNdivisions(505,"Y");
  gStyle -> SetPadTickX(1);
  gStyle -> SetPadTickY(1);
}
