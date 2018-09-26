import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import re

do_print_plot = False

def r_csv(path):
	return pd.read_csv(str(path))


def w_csv(df, path):
	df.to_csv(path, index=False)


def r_df(path):
	return pd.read_parquet(path)


def w_df(df, path):
	df.to_parquet(path)


def phead(df, n=25):
	print(df.head(n))


def has_first(df):
	return {'First'}.issubset(df.columns) or {'First1', 'First2', 'First3', 'First4', 'First5'}.issubset(df.columns)


def format_reddit_table(df, base_folder, stage_number):
	# Get unique links
	df = df.drop_duplicates(['Link'])
	reddit_table = df.to_csv(sep='|', index=False)

	separator = '|'.join([':-' for _ in range(len(df.columns))])
	if reddit_table[0] == '|':
		reddit_table = 'Index|%s' % reddit_table
		separator += '|:--'
	reddit_table = '|%s' % reddit_table

	reddit_table = reddit_table.replace('\n', '\n%s\n' % separator, 1)
	reddit_table = reddit_table.replace('\n', '|\n|')[:-2]
	
	reddit_table = re.sub(r'\|(http[^|]*)\|', r'|[Deck Link](\1)|', reddit_table)
	reddit_table = re.sub(r'\|(\d)\.\d\|', r'|\1|', reddit_table)

	path = 'Data/{}/reddit_table_{}.txt'.format(base_folder, stage_number)
	with open(path, 'w') as file:
		file.write(reddit_table)
	print('\t\tReddit table saved'.format(stage_number))

# ------------------ DF works ------------------ #
def verticalize(df):
	if df is None:
		return 0
	data = []
	first_flag = has_first(df)
	for i in range(1, 6):
		arch_key = 'Archetype{}'.format(i)
		if arch_key not in df.columns: continue
		
		class_key = "Class{}".format(i)
		first_key = "First{}".format(i)
		result_key = "Result{}".format(i)
		if first_flag:
			d = df[["Timestamp", "Class", "Archetype", class_key, arch_key,
					"First{}".format(i), result_key]]

			feed_dict = {class_key: 'Class_o', arch_key:'Archetype_o',
						 first_key: "First", result_key:"Result"}
		else:
			d = df[["Timestamp", "Class", "Archetype", class_key, arch_key,
					result_key]]

			feed_dict = {class_key: 'Class_o', arch_key: 'Archetype_o',
						 result_key: "Result"}

		data.append(d.rename(columns=feed_dict))

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


def count_col(df, col):
	count = 1
	if isinstance(col, list):
		count = len(col)
	df2 = df.groupby(col)[col].count()
	if count > 1:
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


def stack_and_count(df, to_stack):
	if not isinstance(to_stack, list):
		to_stack = [to_stack]
	
	stack_list = [df[col] for col in to_stack]
	stacked = pd.concat(stack_list, 0)
	count = pd.value_counts(stacked)
	return count
	

# ------------------ Plots ------------------ #
def plot_pie(df, title, filename, size=(6, 6)):
	font = FontProperties()
	font.set_weight('bold')
	df.plot.pie(autopct='%.2f', figsize=size, title=title)  #, labels=['' for _ in df])
	count = df.sum()
	
	font = FontProperties()
	font.set_style('italic')
	font.set_weight('light')
	font.set_size('medium')
	plt.annotate('Total Count: {}'.format(count), xy=(0.01, 0.96), xycoords='axes fraction', fontproperties=font)
	
	plt.xlabel('')
	plt.ylabel('')

	pplot(filename)


def plot_scatter(df, x, y, title, filename, c=None):
	if c:
		df.plot.scatter(x=x, y=y, c=c, title=title)
	else:
		df.plot.scatter(x=x, y=y, title=title)
	pplot(filename)


def plot_bar(df, title, filename, groupby=None, stack=True, h=False):
	if groupby is not None:
		df = df.unstack(groupby)
	if h:
		df.plot(kind='barh', stacked=stack, title=title)
	else:
		df.plot(kind='bar', stacked=stack, title=title)
	pplot(filename)


def pplot(path):
	plt.tight_layout()
	plt.savefig(path, bbox_inches='tight')
	if do_print_plot:
		plt.show()
	plt.close()


def _change_do_plot(new_val):
	global do_print_plot
	do_print_plot = new_val