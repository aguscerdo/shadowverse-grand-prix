from tools import *
import argparse
import pandas

def main(folder, stages):
    stages = int(stages)
    # # Stage 1
    if stages in [0, 1]:
        print(folder + "/raw/stage1.csv")
        df1 = r_csv(folder + "/raw/stage1.csv")
        dfv1 = verticalize(folder + "/vertical/stage1.csv", df1, force=True)
        df = most_popular_n(dfv1, 100)
        phead(df)


    # Stage 2
    if stages in [0, 2]:

        df2 = r_csv(folder + "/raw/stage2.csv")
        dfv2 = verticalize(folder + "/vertical/stage2.csv", df2, force=True)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder')
    parser.add_argument('-s', '--stage')
    args = parser.parse_args()
    main(args.folder, args.stage if args.stage is not None else 0)
