# shadowverse-grand-prix
Shadowverse analysis tools for Grand Prix Surveys

Python files:
  - main.py: runs analysis scripts. Use `main.py FOLDER_NAME [-s {0|1|2}] [-f]`
    * FOLDER_NAME: path to folder containing folders
      + raw: contains cleaned csv files
      + vertical: folder to store verticalized csv files
      + plots_stage1: folder to save plots for stage 1
      + plots_stage2: folder to save plots for stage 2
    * stage (-s): 0 is to analyze both stages, 1 or 2 for the respective stage
    * force (-f): force re-verticalization of the data
  
  - analysis.py: streamlines analysis of csv files. Contains horizontal analysis for default csv and vertical analysis for verticalized csv
  - tools.py: plotting and pandas function to use for analysis
  - cleaning_iterations: used to check for anomalies in naming. Up to user to manually change names afterward (TODO: streamline this process). Use `clean_iterations.py FOLDER_NAME [-s {0|1|2}]`
    * FOLDER_NAME: path to folder which contains inside "raw" folder with the csv files. Same as FOLDER_NAME for main.py
    * stage (-s): 0 is to analyze both stages, 1 or 2 for the respective stage
      
