import pandas as pd
import tools as t
from analysis import *
import matplotlib.pyplot as plt

df = t.r_csv("raw/stage1.csv")
analyze_horizontal(df)


dfv = t.verticalize("vertical/stage1.csv", df, force=True)
analyze_vertical(dfv)
