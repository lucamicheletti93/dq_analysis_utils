# List of commands to run

- To produce control histograms:
  ```ruby
  o2-analysis-timestamp --configuration json://configData.json -b | o2-analysis-collision-converter --configuration json://configData.json -b | o2-analysis-mm-vertexing-fwd --aod-file AO2D_mc.root -b
  ```

- To produce tables to process:
  ```ruby
  o2-analysis-mm-track-propagation --configuration json://configData.json -b | o2-analysis-timestamp --configuration json://configData.json -b | o2-analysis-collision-converter --configuration json://configData.json -b
  ```
