import pandas as pd
import tools as t
from analysis import *
import matplotlib.pyplot as plt


# # Stage 1
df1 = t.r_csv("raw/stage1.csv")
analyze_horizontal(df1, 1)

dfv1 = t.verticalize("vertical/stage1.csv", df1, force=True)
analyze_vertical(dfv1, 1)

# Stage 2
df2 = t.r_csv("raw/stage2.csv")
analyze_horizontal(df2, 2)

dfv2 = t.verticalize("vertical/stage2.csv", df2, force=True)
analyze_vertical(dfv2, 2)