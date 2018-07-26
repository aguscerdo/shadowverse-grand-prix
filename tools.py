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


def phead(df, n=25):
    print(df.head(n))

def has_first(df):
    return {'First1', 'First2', 'First3', 'First4', 'First5'}.issubset(df.columns) or {'First'}.issubset(df.columns)

# ------------------ DF works ------------------ #
def verticalize(df):

    if df is None:
        return 0
    data = []
    first_flag = has_first(df)
    for i in range(1, 6):
        if first_flag:
            d = df[["Timestamp", "Class", "Archetype", "Class{}".format(i), "Archetype{}".format(i),
                    "First{}".format(i),"Result{}".format(i)]]

            dict = {"Class{}".format(i):'Class_o', "Archetype{}".format(i):'Archetype_o',
                    "First{}".format(i):"First","Result{}".format(i):"Result"}
        else:
            d = df[["Timestamp", "Class", "Archetype", "Class{}".format(i), "Archetype{}".format(i),
                  "Result{}".format(i)]]

            dict = {"Class{}".format(i): 'Class_o', "Archetype{}".format(i): 'Archetype_o',
                    "Result{}".format(i): "Result"}

        data.append(d.rename(columns=dict))

    vertical = pd.concat(data)
    return vertical


def stack_match(df, c=None):
    if c:
        dfc0 = df[(df['Class'] == c) & (df['Class_o'] != c)]
        dfc1 = df[(df['Class_o'] == c) & (df['Class'] != c)].copy()

        # Switch order to account for both sides
        dfc1[['Class', 'Archetype', 'Class_o', 'Archetype_o']] = \
            dfc1[['Class_o', 'Archetype_o', 'Class', 'Archetype']]
        # Invert winning for adversarial
        dfc1.loc[:, 'Result'] = dfc1.loc[:, 'Result'].apply(lambda x: not x)
        # Invert start for adversarial
        if has_first(dfc1):
            dfc1.loc[:, 'First'] = dfc1.loc[:, 'First'].apply(lambda x: 1 if x == 2 else 2)

        return pd.concat([dfc0, dfc1])
    else:
        dfc1 = df.copy()
        dfc1[['Class', 'Archetype', 'Class_o', 'Archetype_o']] = dfc1[['Class_o', 'Archetype_o', 'Class', 'Archetype']]
        dfc1.loc[:, 'Result'] = dfc1.loc[:, 'Result'].apply(lambda x: not x)
        if has_first(dfc1):
            dfc1.loc[:, 'First'] = dfc1.loc[:, 'First'].apply(lambda x: 1 if x == 2 else 2)
        return pd.concat([df, dfc1])


def join(dfs, renames):
    return pd.concat([dfs[i].rename(renames[i]) for i in range(len(dfs))], axis=1)



def count_col(df, col): # TODO return one col instead of 2
    l = 1
    if isinstance(col, list):
        l = len(col)
    df2 = df.groupby(col)[col].count()
    if l > 1:
        return df2.iloc[:, 0]
    return df2



def mean_col(df, group, col):
    return df.groupby(group)[col].mean()


def std_col(df, group, col):
    return df.groupby(group)[col].std()


def most_popular_n(df, n=0):
    # Opponent single
    n = len(df.index) if not n else n

    df0 = df.copy()
    df0[['Class', 'Archetype', 'Class_o', 'Archetype_o']] = df0[['Class_o', 'Archetype_o', 'Class', 'Archetype']]

    # User Once Only
    df1 = df.copy().drop_duplicates(['Timestamp'])

    return count_col(pd.concat([df0, df1]), ['Class', 'Archetype']).nlargest(n)


def best_decks_n(df, n=10, mincount=10):
    df0 = stack_match(df)
    df0 = df0.groupby(['Class', 'Archetype']).agg({'Result':'mean', 'Archetype':'size'}).reset_index(level="count")
    df0 = df0[df0['count'] > mincount]

    return mean_col(df0, ['Class', 'Archetype'], 'Result').nlargest(n)


# ------------------ Plots ------------------ #
def plot_pie(df, title, filename, size=(6,6)):
    df.plot.pie(autopct='%.2f', figsize=size, title=title)#, labels=['' for _ in df])
    plt.xlabel('')
    plt.ylabel('')

    pplot(filename)


def plot_scatter(df, x, y,title, filename, c=None):
    if c:
        df.plot.scatter(x=x, y=y, c=c, title=title)
    else:
        df.plot.scatter(x=x, y=y, title=title)
    pplot(filename)


def plot_bar(df, title, filename, groupby=None, stack=True, h=False):
    if groupby is not None:
        df = df.unstack(groupby)
    if h:
        p = df.plot(kind='barh', stacked=stack, title=title)
    else:
        p = df.plot(kind='bar', stacked=stack, title=title)

    pplot(filename)


def pplot(path):
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.show()
    plt.close()




