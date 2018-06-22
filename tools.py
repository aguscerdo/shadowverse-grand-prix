import pandas as pd
import matplotlib.pyplot as plt
import csv

def r_csv(path):
    return pd.read_csv(path)


def w_csv(df, path):
    df.to_csv(path)


def r_df(path):
    return pd.read_parquet(path)


def w_df(df, path):
    df.to_parquet(path)


def count_col(df, col): # TODO return one col instead of 2
    return df.groupby(col)[col].count()


def mean_col(df, group, col):
    return df.groupby(group).mean()[col]

def phead(df):
    print(df.head)

# ------------------ DF works ------------------ #
def verticalize(path_csv_out, df=None, force=False):
    try:
        if force:
            i = 1/0
        vertical = pd.read_csv(path_csv_out)
    except:
        if df is None:
            return 0
        data = []
        for i in range(1, 6):
            d = df[["Timestamp", "Class", "Archetype", "Class{}".format(i), "Archetype{}".format(i), "Result{}".format(i)]]
            dict = {"Class{}".format(i):'Class_o', "Archetype{}".format(i):'Archetype_o', "Result{}".format(i):"Result"}
            data.append(d.rename(columns=dict))

        vertical = pd.concat(data)
        vertical.to_csv(path_csv_out)
    return vertical




# ------------------ Plots ------------------ #
def plot_pie(df):
    return df.plot.pie(autopct='%.2f', figsize=(5,5))   #


def plot_scatter(df, x, y, c=None):
    if c:
        p = df.plot.scatter(x=x, y=y, c=c)
    else:
        p = df.plot.scatter(x=x, y=y)

    return p

def plot_bar(df, stack=False, h=False):
    if h:
        p = df.plot.barh(stack=stack)
    else:
        p = df.plot.bar(stack=stack)
    return p


def show_plots(plot, title):
    plot.title(title)
    plot.show()


def save_plot(plot, title, loc="plots"):
    plot.title(title)
    plot.savefig("{}/{}.png".format(loc, title))
