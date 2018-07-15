import pandas as pd
import tools as t
from analysis import *
import matplotlib.pyplot as plt
import argparse

def main(folder, stages, force):
    stages = int(stages)
    # # Stage 1
    if stages in [0, 1]:
        df1 = t.r_csv(folder + "/raw/stage1.csv")
        analyze_horizontal(df1, 1, folder, 1)

        dfv1 = t.verticalize(folder + "/vertical/stage1.csv", df1, force=force)
        analyze_vertical(dfv1, 1, folder, 1)

    # Stage 2
    if stages in [0, 2]:

        df2 = t.r_csv(folder + "/raw/stage2.csv")
        analyze_horizontal(df2, 2, folder, 2)

        dfv2 = t.verticalize(folder + "/vertical/stage2.csv", df2, force=force)
        analyze_vertical(dfv2, 2, folder, 2)

if __name__ == '__main__':
    """
    Usage: 'python3 main.py FOLDER_NAME [-s {0|1|2}] [-f]
    
    - FOLDER_NAME is container where data is: e.g. BOTS_R_1
    - stage [-s] is which stages to analyze, 0 for all, 1 for stage 1 only, 2 for stage 2 only
    - force [-f] is a binary to force re-verticalization.
        - Verticalized data is saved to a file, if not found it will be performed
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('folder', nargs='?')
    parser.add_argument('-f', '--force',action='store_true', default=False)
    parser.add_argument('-s', '--stage', default=0)
    args = parser.parse_args()
    main(args.folder, args.stage, args.force)
