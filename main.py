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
        analyze_horizontal(df1, 1, folder)

        dfv1 = t.verticalize(folder + "/vertical/stage1.csv", df1, force=force)
        analyze_vertical(dfv1, 1, folder)

    # Stage 2
    if stages in [0, 2]:

        df2 = t.r_csv(folder + "/raw/stage2.csv")
        analyze_horizontal(df2, 2, folder)

        dfv2 = t.verticalize(folder + "/vertical/stage2.csv", df2, force=force)
        analyze_vertical(dfv2, 2, folder)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', nargs='?')
    parser.add_argument('-f', '--force',action='store_true', default=False)
    parser.add_argument('-s', '--stage', default=0)
    args = parser.parse_args()
    main(args.folder, args.stage, args.force)

