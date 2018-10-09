# shadowverse-grand-prix
Shadowverse analysis tools for Grand Prix Surveys

Python files:
  - main.py: runs analysis scripts. Use `main.py FOLDER_NAME [-s {0|1|2}] [-f]`
    * FOLDER_NAME: path to folder containing csv files
    * stage (-s): 0 is to analyze both stages, 1 or 2 for the respective stage, 3 is for finals
  
  - analysis.py: streamlines analysis of csv files. Contains horizontal analysis for default csv and vertical analysis for verticalized dataframes
  - tools.py: plotting and pandas function to use for analysis
  - file_pre_process: adds wins and first count. Points out anomalies to replace. Use `file_pre_process.py FOLDER_NAME [-s {0|1|2|3}]`
    * FOLDER_NAME: path to folder which contains csv files. Same as FOLDER_NAME for main.py
    * stage (-s): 0 is to analyze both stages, 1 or 2 for the respective stage, 3 is for finals
