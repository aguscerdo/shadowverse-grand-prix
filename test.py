import pandas as pd
import tools as t
from analysis import *
import matplotlib.pyplot as plt
import argparse


def main(folder, stages, force):

    df1 = t.r_csv(folder + "/raw/stage1.csv")

    df = t.verticalize(folder + "/vertical/stage1.csv", df1, force=force)

    dfc = stack_match(df, 'Swordcraft')
    df_std = t.std_col(dfc, ['Class', 'Class_o'], 'Result')
    df_mean = t.mean_col(dfc, ['Class', 'Class_o'], 'Result')
    phead(df_std)
    phead(df_mean)



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
    parser.add_argument('-f', '--force', action='store_true', default=False)
    parser.add_argument('-s', '--stage', default=0)
    args = parser.parse_args()
    main(args.folder, args.stage, args.force)
