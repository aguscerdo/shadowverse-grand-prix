import pandas as pd
from tools import *


def analyze_horizontal(df, stage_number, folder):
	path, tag, plot_tag = __separate_tags(stage_number, folder)

	# ---- Single column distributions -----
	rank_count = count_col(df, "Rank")
	plot_pie(rank_count, "User Rank Distribution - {}".format(tag),
	         path+"pie_rank_count_{}.png".format(plot_tag))
	class_count = count_col(df, "Class")
	plot_pie(class_count, "User Class Distribution - {}".format(tag),
	         path+"pie_class_count_{}.png".format(plot_tag))

	# Rank by Class
	rank_class = count_col(df, ['Rank', 'Class'])
	plot_bar(rank_class, "Ranks by Class - {}".format(tag),
	         path+"bar_rank_vs_class_{}.png".format(plot_tag), groupby="Rank")

	# Wins per Rank
	rank_wins = count_col(df, ['Rank', 'Wins'])
	plot_bar(rank_wins, "Wins per Rank - {}".format(tag),
	         path+"bar_rank_vs_win_{}.png".format(plot_tag), groupby='Rank')

	# Wins per class
	class_wins = count_col(df, ['Class', 'Wins'])
	plot_bar(class_wins, "Wins per Class - {}".format(tag),
	         path+'bar_class_vs_win_{}.png'.format(plot_tag), groupby='Class')

	# # Wins vs First or second
	# if has_first(df):
	# 	first_wins = count_col(df, ['Wins', 'First'])
	# 	plot_bar(first_wins, "Times going First vs Wins - {}".format(tag),
	# 	         path+'bar_first_vs_win_{}.png'.format(plot_tag), groupby='Wins', stack=False)

	# Get Links of good Decks
	if 'Link' in df.columns:
		link_df = df[df.Link.notna()][['Class', 'Archetype', 'Wins', 'Link']].\
			sort_values(['Wins', 'Class', 'Archetype'], ascending=False)
		format_reddit_table(link_df, folder, stage_number)


def analyze_vertical(df, stage_number, folder):
	classes = ['Shadowcraft', 'Runecraft', 'Forestcraft', 'Swordcraft', 'Dragoncraft', 'Havencraft', 'Portalcraft', 'Bloodcraft']
	
	path, tag, plot_tag = __separate_tags(stage_number, folder)
	
	# Pie of total Usage
	class_count = stack_and_count(df, ['Class', 'Class_o'])
	plot_pie(class_count, "Total Class Distribution - {}".format(stage_number),
	         path + "pie_total_class_count_s{}.png".format(plot_tag))
	
	for c in classes:
		dfc = stack_match(df, c)   # Full
		
		# Avg Winrate
		df_mean = mean_col(dfc, ['Class', 'Class_o'], 'Result')
		if not has_first(dfc):
			plot_bar(df_mean, 'Class vs Class Winrate for {} - {}'.format(c, tag),
					 path + 'bar_{}_vs_class_{}.png'.format(c, plot_tag))
		else:
			df_mean_first = mean_col(dfc[dfc['First'] == 1], ['Class', 'Class_o'], 'Result')
			df_mean_second = mean_col(dfc[dfc['First'] == 2], ['Class', 'Class_o'], 'Result')

			df_joint = join([df_mean, df_mean_first, df_mean_second], ['Mean', 'First', 'Second'])
			plot_bar(df_joint, 'Class vs Class Winrate for {} - {}'.format(c, tag),
					 path + 'bar_{}_vs_class_{}.png'.format(c, plot_tag), stack=False)

		# Archetypes
		class_archetype = count_col(dfc, ['Class', 'Archetype'])
		plot_pie(class_archetype, "Archetype Distribution for {} - {}".format(c, tag),
				 path + "pie_{}_arch_pie_{}.png".format(c, plot_tag))

	# Most popular decks
	popular_decks = most_popular_n(df, 10)
	plot_bar(popular_decks, "Most used decks - {}".format(tag),
	         path + 'bar_most_used_{}.png'.format(plot_tag))


def __separate_tags(stage_number, folder):
	if stage_number == 1:
		tag = 'Stage 1'
		path = 'Data/{}/plots_stage1/'.format(folder)
		plot_tag = 's1'
	elif stage_number == 2:
		tag = 'Stage 2'
		path = 'Data/{}/plots_stage2/'.format(folder)
		plot_tag = 's2'
	elif stage_number == 3:
		tag = 'Finals A'
		path = 'Data/{}/plots_finals_a/'.format(folder)
		plot_tag = 'fA'
	else:
		tag = 'Finals B'
		path = 'Data/{}/plots_finals_b/'.format(folder)
		plot_tag = 'fB'
	
	return path, tag, plot_tag