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
  TString initHist1dName[] = {"Pt", "Eta", "Phi", "DCAxy", "DCAz"};
  TString initHist2dName[] = {"TPCdedx_pIN"};
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
      hist1dVarMC[iDir][iHist1d] -> SetMarkerSize(0.8);
      hist1dVarMC[iDir][iHist1d] -> SetMarkerColor(kRed);
      hist1dVarMC[iDir][iHist1d] -> SetLineColor(kRed);

      //hist1dVarData[iDir][iHist1d] -> Rebin(2);
      hist1dVarData[iDir][iHist1d] -> Scale(1. / hist1dVarData[iDir][iHist1d] -> Integral());
      hist1dVarData[iDir][iHist1d] -> SetMarkerStyle(20);
      hist1dVarData[iDir][iHist1d] -> SetMarkerSize(0.8);
      hist1dVarData[iDir][iHist1d] -> SetMarkerColor(kBlue);
      hist1dVarData[iDir][iHist1d] -> SetLineColor(kBlue);
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
      hist2dVarMCProj[iDir][iHist2d] -> SetMarkerSize(0.8);
      hist2dVarMCProj[iDir][iHist2d] -> SetMarkerColor(kRed);
      hist2dVarMCProj[iDir][iHist2d] -> SetLineColor(kRed);

      hist2dVarDataProj[iDir][iHist2d] = (TH1F*) hist2dVarData[iDir][iHist2d] -> ProjectionY();
      hist2dVarDataProj[iDir][iHist2d] -> SetName(Form("Data_proj_%s", dirName[iDir].Data()));
      hist2dVarDataProj[iDir][iHist2d] -> Scale(1. / hist2dVarDataProj[iDir][iHist2d] -> Integral());
      hist2dVarDataProj[iDir][iHist2d] -> SetMarkerStyle(20);
      hist2dVarDataProj[iDir][iHist2d] -> SetMarkerSize(0.8);
      hist2dVarDataProj[iDir][iHist2d] -> SetMarkerColor(kBlue);
      hist2dVarDataProj[iDir][iHist2d] -> SetLineColor(kBlue);
    }
  }

  // dE/dx projections
  Double_t pinProj[] = {0, 0.6, 2, 10};
  TH1F *hist_dEdx_Data[3];
  TH1F *hist_dEdx_MC[3];

  for(int iPt = 0;iPt < 3;iPt++){
    hist_dEdx_Data[iPt] = (TH1F*) hist2dVarData[0][0] -> ProjectionY(Form("hist_dEdx_Data_Pt_%2.1f_%2.1f", pinProj[iPt], pinProj[iPt+1]), hist2dVarData[0][0] -> GetXaxis() -> FindBin(pinProj[iPt]), hist2dVarData[0][0] -> GetXaxis() -> FindBin(pinProj[iPt+1]));
    hist_dEdx_Data[iPt] -> SetTitle(Form("%2.1f < p_{in} < %2.1f GeV/c", pinProj[iPt], pinProj[iPt+1]));
    hist_dEdx_Data[iPt] -> Scale(1. / hist_dEdx_Data[iPt] -> Integral());
    hist_dEdx_Data[iPt] -> SetMarkerStyle(20);
    hist_dEdx_Data[iPt] -> SetMarkerSize(0.8);
    hist_dEdx_Data[iPt] -> SetMarkerColor(kRed);
    hist_dEdx_Data[iPt] -> SetLineColor(kRed);
    //hist_dEdx_Data[iPt] -> Rebin(2);

    hist_dEdx_MC[iPt] = (TH1F*) hist2dVarMC[0][0] -> ProjectionY(Form("hist_dEdx_MC_Pt_%2.1f_%2.1f", pinProj[iPt], pinProj[iPt+1]), hist2dVarMC[0][0] -> GetXaxis() -> FindBin(pinProj[iPt]), hist2dVarMC[0][0] -> GetXaxis() -> FindBin(pinProj[iPt+1]));
    hist_dEdx_MC[iPt] -> SetTitle(Form("%2.1f < p_{in} < %2.1f GeV/c", pinProj[iPt], pinProj[iPt+1]));
    hist_dEdx_MC[iPt] -> Scale(1. / hist_dEdx_MC[iPt] -> Integral());
    hist_dEdx_MC[iPt] -> SetMarkerStyle(20);
    hist_dEdx_MC[iPt] -> SetMarkerSize(0.8);
    hist_dEdx_MC[iPt] -> SetMarkerColor(kBlue);
    hist_dEdx_MC[iPt] -> SetLineColor(kBlue);
    //hist_dEdx_MC[iPt] -> Rebin(2);

    DrawRatioPlot(hist_dEdx_Data[iPt], hist_dEdx_MC[iPt], output_dir_name, Form("hist_dEdx_Pt_%2.1f_%2.1f", pinProj[iPt], pinProj[iPt+1]));
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
  if(plotName.Contains("Pt")){
    ratioPlot -> GetLowerRefYaxis() -> SetRangeUser(0.,2.);
  }
  canvas -> Update();
  canvas -> SaveAs(Form("%s/ratio_%s.pdf", dirName.Data(), plotName.Data()));
  //canvas -> SaveAs(Form("%s/ratio_%s.png", dirName.Data(), plotName.Data()));
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
