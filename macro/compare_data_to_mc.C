void DrawRatioPlot(TH1F *, TH1F *, TString , TString);
void LoadStyle();

Long_t *dummy1 = 0, *dummy2 = 0, *dummy3 = 0, *dummy4 = 0;
TString output_dir_name = "figures/qc";

void compare_data_to_mc(const char *name_fInMC = "AnalysisResultsTM_LHC22c5_HL.root", const char *name_fInData = "AnalysisResultsTM_OCT_apass3_HL.root"){
  //LoadStyle();
  const char *path_fIn = "/Users/lucamicheletti/GITHUB/dq_analysis_utils/o2/output";

  if(gSystem -> GetPathInfo(Form("%s",output_dir_name.Data()),dummy1,dummy2,dummy3,dummy4) != 0){
    gSystem -> Exec(Form("mkdir -p %s",output_dir_name.Data()));
  }

  TH1F *hist1dVarMC[10][10], *hist1dVarData[10][10];
  TH2F *hist2dVarMC[10][10], *hist2dVarData[10][10];
  TH1F *hist2dVarMCProj[10][10], *hist2dVarDataProj[10][10];
  std::vector<TString> dirName;
  std::vector<TString> hist1dName;
  std::vector<TString> hist2dName;
  int dirNum;
  int hist1dNum;
  int hist2dNum;

  TString initDirName[] = {"TrackBarrel_jpsiO2MCdebugCuts"};
  TString initHist1dName[] = {"Pt", "Eta", "Phi", "DCAxy", "DCAz", "DCAsigXY", "DCAsigZ", "ITSncls", "ITSchi2", "TPCncls", "TPCchi2"};
  TString initHist2dName[] = {"TPCdedx_pIN", "TOFbeta_pIN"};
  dirNum = sizeof(initDirName)/sizeof(initDirName[0]);
  hist1dNum = sizeof(initHist1dName)/sizeof(initHist1dName[0]);
  hist2dNum = sizeof(initHist2dName)/sizeof(initHist2dName[0]);
  copy(initDirName,    initDirName+dirNum,       back_inserter(dirName));
  copy(initHist1dName, initHist1dName+hist1dNum, back_inserter(hist1dName));
  copy(initHist2dName, initHist2dName+hist2dNum, back_inserter(hist2dName));

  TFile *fInMC   = new TFile(Form("%s/%s", path_fIn, name_fInMC),   "READ");
  TString mainDirNameMC = "table-maker-m-c";

  TFile *fInData = new TFile(Form("%s/%s", path_fIn, name_fInData), "READ");
  TString mainDirNameData = "table-maker";

  auto hlistMC = (THashList*) fInMC -> Get(Form("%s/output", mainDirNameMC.Data()));
  auto hlistData = (THashList*) fInData -> Get(Form("%s/output", mainDirNameData.Data()));
  for(int iDir = 0;iDir < dirNum;iDir++){
    auto listMC   = (TList*) hlistMC -> FindObject(dirName[iDir].Data());
    auto listData = (TList*) hlistData -> FindObject(dirName[iDir].Data());
    for(int iHist1d = 0;iHist1d < hist1dNum;iHist1d++){
      hist1dVarMC[iDir][iHist1d] = (TH1F*) listMC -> FindObject(hist1dName[iHist1d].Data());
      hist1dVarMC[iDir][iHist1d] -> SetName(dirName[iDir]);
      hist1dVarData[iDir][iHist1d] = (TH1F*) listData -> FindObject(hist1dName[iHist1d].Data());
      hist1dVarData[iDir][iHist1d] -> SetName(dirName[iDir]);

      //hist1dVarMC[iDir][iHist1d] -> Rebin(2);
      hist1dVarMC[iDir][iHist1d] -> Scale(1. / hist1dVarMC[iDir][iHist1d] -> Integral());
      hist1dVarMC[iDir][iHist1d] -> SetMarkerStyle(20);
      hist1dVarMC[iDir][iHist1d] -> SetMarkerSize(0.6);
      hist1dVarMC[iDir][iHist1d] -> SetMarkerColor(kRed+1);
      hist1dVarMC[iDir][iHist1d] -> SetLineColor(kRed+1);

      //hist1dVarData[iDir][iHist1d] -> Rebin(2);
      hist1dVarData[iDir][iHist1d] -> Scale(1. / hist1dVarData[iDir][iHist1d] -> Integral());
      hist1dVarData[iDir][iHist1d] -> SetMarkerStyle(24);
      hist1dVarData[iDir][iHist1d] -> SetMarkerSize(0.6);
      hist1dVarData[iDir][iHist1d] -> SetMarkerColor(kBlue+1);
      hist1dVarData[iDir][iHist1d] -> SetLineColor(kBlue+1);
    }
    for(int iHist2d = 0;iHist2d < hist2dNum;iHist2d++){
      hist2dVarMC[iDir][iHist2d] = (TH2F*) listMC -> FindObject(hist2dName[iHist2d].Data());
      hist2dVarMC[iDir][iHist2d] -> SetName(dirName[iDir]);
      hist2dVarData[iDir][iHist2d] = (TH2F*) listData -> FindObject(hist2dName[iHist2d].Data());
      hist2dVarData[iDir][iHist2d] -> SetName(dirName[iDir]);

      // Save projections
      hist2dVarMCProj[iDir][iHist2d] = (TH1F*) hist2dVarMC[iDir][iHist2d] -> ProjectionY();
      hist2dVarMCProj[iDir][iHist2d] -> SetName(Form("MC_proj_%s", dirName[iDir].Data()));
      hist2dVarMCProj[iDir][iHist2d] -> Scale(1. / hist2dVarMCProj[iDir][iHist2d] -> Integral());
      hist2dVarMCProj[iDir][iHist2d] -> SetMarkerStyle(20);
      hist2dVarMCProj[iDir][iHist2d] -> SetMarkerSize(0.6);
      hist2dVarMCProj[iDir][iHist2d] -> SetMarkerColor(kRed+1);
      hist2dVarMCProj[iDir][iHist2d] -> SetLineColor(kRed+1);

      hist2dVarDataProj[iDir][iHist2d] = (TH1F*) hist2dVarData[iDir][iHist2d] -> ProjectionY();
      hist2dVarDataProj[iDir][iHist2d] -> SetName(Form("Data_proj_%s", dirName[iDir].Data()));
      hist2dVarDataProj[iDir][iHist2d] -> Scale(1. / hist2dVarDataProj[iDir][iHist2d] -> Integral());
      hist2dVarDataProj[iDir][iHist2d] -> SetMarkerStyle(24);
      hist2dVarDataProj[iDir][iHist2d] -> SetMarkerSize(0.6);
      hist2dVarDataProj[iDir][iHist2d] -> SetMarkerColor(kBlue+1);
      hist2dVarDataProj[iDir][iHist2d] -> SetLineColor(kBlue+1);
    }
  }

  // dE/dx projections
  Double_t pinProj[] = {0, 0.6, 2, 10};
  Int_t    pinNum = sizeof(pinProj)/sizeof(pinProj[0]);
  Int_t    pinMin, pinMax;

  vector <TH1F*> histProjData[hist2dNum];
  vector <TH1F*> histProjMC[hist2dNum];

  for(int iHist2d = 0;iHist2d < hist2dNum;iHist2d++){
    for(int iPin = 0;iPin < pinNum-1;iPin++){
      pinMin = hist2dVarData[0][iHist2d] -> GetXaxis() -> FindBin(pinProj[iPin]);
      pinMax = hist2dVarData[0][iHist2d] -> GetXaxis() -> FindBin(pinProj[iPin+1]);

      histProjData[iHist2d].push_back((TH1F*) hist2dVarData[0][iHist2d] -> ProjectionY(Form("hist_%s_Data_Pt_%2.1f_%2.1f", hist2dName[iHist2d].Data(), pinProj[iPin], pinProj[iPin+1]), pinMin, pinMax));
      histProjData[iHist2d][iPin] -> SetTitle(Form("%2.1f < p_{in} < %2.1f GeV/c", pinProj[iPin], pinProj[iPin+1]));
      histProjData[iHist2d][iPin] -> Scale(1. / histProjData[iHist2d][iPin] -> Integral());
      histProjData[iHist2d][iPin] -> SetMarkerStyle(20);
      histProjData[iHist2d][iPin] -> SetMarkerSize(0.6);
      histProjData[iHist2d][iPin] -> SetMarkerColor(kRed+1);
      histProjData[iHist2d][iPin] -> SetLineColor(kRed+1);
      histProjData[iHist2d][iPin] -> Rebin(1);

      histProjMC[iHist2d].push_back((TH1F*) hist2dVarMC[0][iHist2d] -> ProjectionY(Form("hist_%s_MC_Pt_%2.1f_%2.1f", hist2dName[iHist2d].Data(), pinProj[iPin], pinProj[iPin+1]), pinMin, pinMax));
      histProjMC[iHist2d][iPin] -> SetTitle(Form("%2.1f < p_{in} < %2.1f GeV/c", pinProj[iPin], pinProj[iPin+1]));
      histProjMC[iHist2d][iPin] -> Scale(1. / histProjMC[iHist2d][iPin] -> Integral());
      histProjMC[iHist2d][iPin] -> SetMarkerStyle(24);
      histProjMC[iHist2d][iPin] -> SetMarkerSize(0.6);
      histProjMC[iHist2d][iPin] -> SetMarkerColor(kBlue+1);
      histProjMC[iHist2d][iPin] -> SetLineColor(kBlue+1);
      histProjMC[iHist2d][iPin] -> Rebin(1);

      DrawRatioPlot(histProjData[iHist2d][iPin], histProjMC[iHist2d][iPin], output_dir_name, Form("hist_%s_Pt_%2.1f_%2.1f", hist2dName[iHist2d].Data(), pinProj[iPin], pinProj[iPin+1]));
    }
  }


  for(int iHist2d = 0;iHist2d < hist2dNum;iHist2d++){
    auto canvasVar = new TCanvas("canvasVar", "",  600*dirNum, 600);
    canvasVar -> Divide(dirNum,1);
    for(int iDir = 0;iDir < dirNum;iDir++){
      canvasVar -> cd(iDir+1);
      if(hist2dName[iHist2d].Contains("dedx")){
        gPad -> SetLogx(1);
      }
      hist2dVarMC[iDir][iHist2d] -> Draw("COLZ");
    }
    canvasVar -> SaveAs(Form("%s/%s_MC.pdf", output_dir_name.Data(), hist2dName[iHist2d].Data()));
    delete canvasVar;
  }

  for(int iHist2d = 0;iHist2d < hist2dNum;iHist2d++){
    auto canvasVar = new TCanvas("canvasVar", "",  600*dirNum, 600);
    canvasVar -> Divide(dirNum,1);
    for(int iDir = 0;iDir < dirNum;iDir++){
      canvasVar -> cd(iDir+1);
      if(hist2dName[iHist2d].Contains("dedx")){
        gPad -> SetLogx(1);
      }
      hist2dVarData[iDir][iHist2d] -> Draw("COLZ");
    }
    canvasVar -> SaveAs(Form("%s/%s_Data.pdf", output_dir_name.Data(), hist2dName[iHist2d].Data()));
    delete canvasVar;
  }


  // Ratio of projections
  for(int iDir = 0;iDir < dirNum;iDir++){
    for(int iHist2d = 0;iHist2d < hist2dNum;iHist2d++){
      DrawRatioPlot(hist2dVarMCProj[iDir][iHist2d], hist2dVarDataProj[iDir][iHist2d], output_dir_name, initHist2dName[iHist2d] + initDirName[iDir]);
    }
  }

  // Ratio of of 1D plots
  for(int iDir = 0;iDir < dirNum;iDir++){
    for(int iHist1d = 0;iHist1d < hist1dNum;iHist1d++){
      DrawRatioPlot(hist1dVarMC[iDir][iHist1d], hist1dVarData[iDir][iHist1d], output_dir_name, initHist1dName[iHist1d] + initDirName[iDir]);
    }
  }

}
////////////////////////////////////////////////////////////////////////////////
void DrawRatioPlot(TH1F *hist1, TH1F *hist2, TString dirName, TString plotName){
  gStyle->SetOptStat(0);
  auto canvas = new TCanvas("canvas", "A ratio example");
  auto ratioPlot = new TRatioPlot(hist1, hist2);
  if(plotName.Contains("Pt")){
    gPad -> SetLogy(1);
  }
  ratioPlot -> Draw();
  ratioPlot -> GetLowerRefYaxis() -> SetRangeUser(0.,2.);
  ratioPlot -> GetLowerRefYaxis() -> SetLabelSize(0.025);

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
