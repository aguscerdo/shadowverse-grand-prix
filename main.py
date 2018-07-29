import pandas as pd
import tools as t
from analysis import *
import os
import argparse

def main(folder, stages):
    stages = int(stages)
    # # Stage 1
    if stages in [0, 1]:
        df1 = t.r_csv(folder + "/stage1.csv")
        analyze_horizontal(df1, 1, folder, 1)

        dfv1 = t.verticalize(df1)
        analyze_vertical(dfv1, 1, folder, 1)

    # Stage 2
    if stages in [0, 2]:
        df2 = t.r_csv(folder + "/stage2.csv")
        analyze_horizontal(df2, 2, folder, 2)

        dfv2 = t.verticalize(df2)
        analyze_vertical(dfv2, 2, folder, 2)

if __name__ == '__main__':
    """
    Usage: 'python3 main.py FOLDER_NAME [-s {0|1|2}]
    
    - FOLDER_NAME is container where data is: e.g. BOTS_R_1
    - stage [-s] is which stages to analyze, 0 for all, 1 for stage 1 only, 2 for stage 2 only
    """


    parser = argparse.ArgumentParser()
    parser.add_argument('folder', nargs='?')
    parser.add_argument('-s', '--stage', default=0)
    args = parser.parse_args()

    # Check and create plot folders
    if not os.path.exists("{}/plots_stage1".format(args.folder)):
        os.mkdir("{}/plots_stage1".format(args.folder))
        print("Created plots_stage1 folder")

    if not os.path.exists("{}/plots_stage2".format(args.folder)):
        os.mkdir("{}/plots_stage2".format(args.folder))
        print("Created plots_stage2 folder")

    print("Analyzing {}".format(args.folder))
    main(args.folder, args.stage)
