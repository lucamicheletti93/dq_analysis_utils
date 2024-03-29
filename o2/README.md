# Useful info
- tableReader configuration: the cuts have to be the same in "analysis-muon-selection" and "analysis-same-event-pairing"

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
  
- ### New!
  ```ruby
  python runTableMaker_new.py configTableMakerDataRun3_QC.json -runData table-maker:processMuonOnlyWithCov:true --add_track_prop
  ```
  
  ```ruby
  o2-analysis-dq-table-reader --configuration json://configAnalysisDataRun3_HL.json -b
  ```
  
- if it complains about fdd run this command:
  ```ruby
  python runTableMaker_QC_fddconverter.py configTableMakerDataRun3_QC.json runData table-maker:processBarrelOnlyWithCov:true
  ```
  
- ### MFT ambiguous tracks
- Run this framework to re-assaign the tracks to the best collision according to the DCA
  ```ruby
  o2-analysis-mm-vertexing-fwd --configuration json://config.json -b
  ```
- ### link to the latest command from tutorial
https://indico.cern.ch/event/1220887/contributions/5168721/attachments/2565795/4423412/IArsene_DQO2analysis_2022December13.pdf

- For ambiguous tracks studies
  - Data w/o collision re-association
  ```ruby
  python runTableMaker.py configTableMakerDataRun3.json -runData --arg table-maker:processAmbiguousMuonOnlyWithCov:true --add_track_prop --add_col_conv
  ```
  - Data with collision re-association
  ```ruby
  python runTableMaker.py configTableMakerDataRun3.json -runData --arg table-maker:processAmbiguousMuonOnlyWithCovBestCollision:true --add_track_prop --add_col_conv --add_best_coll
  ```
  
  ```ruby
  python3 runAnalysis.py configAnalysisData.json -runData --aod-writer-json writerConfiguration_dileptons.json
  ```
  
  - MC w/o collision re-association
  ```ruby
  python runTableMaker.py configTableMakerMCRun3.json -runMC --arg table-maker-m-c:processAmbiguousMuonOnlyWithCov:true --add_track_prop --add_col_conv
  ```
  - MC with collision re-association
  ```ruby
  python runTableMaker.py configTableMakerMCRun3.json -runMC --arg table-maker-m-c:processAmbiguousMuonOnlyWithCovBestCollision:true --add_track_prop --add_col_conv --add_best_coll
  ```
