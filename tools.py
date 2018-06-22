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



# ------------------ DF works ------------------ #
def verticalize(path_in, path_out):
    index = 0
    header = ["mid", "deck_u", "arch_u", "deck_o", "arch_o", "win", "gnum"]

    file_in = open(path_in, 'rb')
    csv_in = csv.reader(file_in, delimiter=',')

    df = pd.DataFrame(columns=["mid", "deck_u", "arch_u", "deck_o", "arch_o", "win", "gnum"])
    data = []

    for row in csv_in:
        index += 1
        for i in range(1,6):





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






# TODO plot functions, Pies, bar, scatter
