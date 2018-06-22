import pandas as pd
import tools as t
import analysis as A
import matplotlib.pyplot as plt

df = t.r_csv("raw/stage1.csv")

t.plot_pie(t.count_col(df, "Class"))
plt.show()