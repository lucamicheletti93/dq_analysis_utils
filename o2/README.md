# List of commands to run

## General MC processing
- TableMaker:
  ```ruby
  python runTableMaker.py configTableMakerMCRun3.json runMC table-maker-m-c:processMuonOnlyWithCov:true
  ```
- TableMaker with converter (if mcparticles_001 not found)
  ```ruby
  python runTableMaker2.py configTableMakerMCRun3.json runMCwithConverter table-maker-m-c:processMuonOnlyWithCov:true
  ```

- TableReader:
  ```ruby
  o2-analysis-dq-efficiency --configuration json://configAnalysisMC.json --aod-writer-json writerConfiguration_dileptons.json -b
  ```
  
## QC MC processing
- Load O2 via cvmfs (temporary issue with fdd):
  ```ruby
  /cvmfs/alice.cern.ch/bin/alienv enter VO_ALICE@O2Physics::nightly-20220421-1
  ```
  
- Run table maker without converter (specific for GP MC pp@900GeV):
  ```ruby
  python runTableMaker_QC.py configTableMakerMCRun3_QC.json runMC table-maker-m-c:processBarrelOnlyWithCov:true
  ```
  
- ### New!
  ```ruby
  python runTableMaker_new.py configTableMakerMCRun3_QC.json -runMC table-maker-m-c:processMuonOnlyWithCov:true --add_track_prop
  ```
  
- Run dq Efficiency:
  ```ruby
  o2-analysis-dq-efficiency --configuration json://configAnalysisMC_QC.json -b
  ```
  
## QC Data processing
- Load O2 via cvmfs (temporary issue with fdd):
  ```ruby
  /cvmfs/alice.cern.ch/bin/alienv enter VO_ALICE@O2Physics::nightly-20220421-1
  ```
  
- Run table maker on pilot beam data (until apass3)
  ```ruby
  python runTableMaker_QC.py configTableMakerDataRun3_QC.json runData table-maker:processBarrelOnlyWithCov:true
  ```
- Run table maker on pilot beam data (**apass4**, WIP: issue with cov)
  ```ruby
  python runTableMaker_QC2.py configTableMakerDataRun3_QC.json runData table-maker:processBarrelOnly:true
  ```
  
- Run table reader:
  ```ruby
  o2-analysis-dq-table-reader --configuration json://configAnalysisData_QC.json -b
  ```
  
- <mark style="background-color: #FFFF00">Highlighted text</mark>  Run pp@13TeV as HL:  <mark >Highlighted text</mark>  
  ```ruby
  o2-analysis-dq-table-reader --configuration json://configAnalysisDataRun3_HL.json -b
  ```
  
- if it complains about fdd run this command:
  ```ruby
  python runTableMaker_QC_fddconverter.py configTableMakerDataRun3_QC.json runData table-maker:processBarrelOnlyWithCov:true
  ```
