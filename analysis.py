import pandas as pd
from tools import *


def analyze_horizontal(df, n, folder, stage_number):
	path = 'Data/{}/plots_stage{}/'.format(folder, stage_number)
	# ---- Single column distributions -----
	rank_count = count_col(df, "Rank")
	plot_pie(rank_count, "User Rank Distribution - Stage {}".format(n), path+"pie_rank_count_s{}.png".format(n))
	class_count = count_col(df, "Class")
	plot_pie(class_count, "User Class Distribution - Stage {}".format(n), path+"pie_class_count_s{}.png".format(n))

	# Rank by Class
	rank_class = count_col(df, ['Rank', 'Class'])
	plot_bar(rank_class, "Ranks by Class - Stage {}".format(n), path+"bar_rank_vs_class_s{}.png".format(n), groupby="Rank")

	# Wins per Rank
	rank_wins = count_col(df, ['Rank', 'Wins'])
	plot_bar(rank_wins, "Wins per Rank - Stage {}".format(n), path+"bar_rank_vs_win_s{}.png".format(n), groupby='Rank')

	# Wins per class
	class_wins = count_col(df, ['Class', 'Wins'])
	plot_bar(class_wins, "Wins per Class - Stage {}".format(n), path+'bar_class_vs_win_s{}.png'.format(n), groupby='Class')

	# # Wins vs First or second
	# if has_first(df):
	# 	first_wins = count_col(df, ['Wins', 'First'])
	# 	plot_bar(first_wins, "Times going First vs Wins - Stage {}".format(n), path+'bar_first_vs_win_s{}.png'.format(n), groupby='Wins', stack=False)

	# Get Links of good Decks
	if 'Link' in df.columns:
		link_df = df[df.Link.notna()][['Class', 'Archetype', 'Wins', 'Link']].\
			sort_values(['Wins', 'Class', 'Archetype'], ascending=False)
		format_reddit_table(link_df, folder, stage_number)


def analyze_vertical(df, n, folder, stage_number):
	classes = ['Shadowcraft', 'Runecraft', 'Forestcraft', 'Swordcraft', 'Dragoncraft', 'Havencraft', 'Portalcraft', 'Bloodcraft']
	path = 'Data/{}/plots_stage{}/'.format(folder, stage_number)
	
	# Pie of total Usage
	class_count = stack_and_count(df, ['Class', 'Class_o'])
	plot_pie(class_count, "Total Class Distribution - Stage {}".format(n), path+"pie_total_class_count_s{}.png".format(n))
	
	for c in classes:
		dfc = stack_match(df, c)   # Full
		
		# Avg Winrate
		df_mean = mean_col(dfc, ['Class', 'Class_o'], 'Result')
		if not has_first(dfc):
			plot_bar(df_mean, 'Class vs Class Winrate for {} - Stage {}'.format(c, n),
					 path + 'bar_{}_vs_class_s{}.png'.format(c, n))
		else:
			df_mean_first = mean_col(dfc[dfc['First'] == 1], ['Class', 'Class_o'], 'Result')
			df_mean_second = mean_col(dfc[dfc['First'] == 2], ['Class', 'Class_o'], 'Result')

			df_joint = join([df_mean, df_mean_first, df_mean_second], ['Mean', 'First', 'Second'])
			plot_bar(df_joint, 'Class vs Class Winrate for {} - Stage {}'.format(c, n),
					 path + 'bar_{}_vs_class_s{}.png'.format(c, n), stack=False)

		# Archetypes
		class_archetype = count_col(dfc, ['Class', 'Archetype'])
		plot_pie(class_archetype, "Archetype Distribution for {} - Stage {}".format(c, n),
				 path+"pie_{}_arch_pie_s{}.png".format(c, n))

	# Most popular decks
	popular_decks = most_popular_n(df, 10)
	plot_bar(popular_decks, "Most used decks - Stage {}".format(n), path+'bar_most_used_s{}.png'.format(n))
