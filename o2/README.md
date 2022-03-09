## List of commands to run

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