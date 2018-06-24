import pandas as pd
from tools import *



def analyze_horizontal(df):
    # ---- Single column distributions -----
    rank_count = count_col(df, "Rank")
    plot_pie(rank_count, "Rank Distribution", "rank_count")
    class_count = count_col(df, "Class")
    plot_pie(class_count, "Class Distribution", "class_count")


    # Rank Statistics
    rank_class = count_col(df, ['Rank', 'Class'])
    plot_bar(rank_class, "Ranks by Class", "rank_vs_class", groupby="Rank")

    rank_wins = count_col(df, ['Rank', 'Wins'])
    plot_bar(rank_wins, "Wins per Rank", "rank_vs_win", groupby='Rank')

    class_wins = count_col(df, ['Class', 'Wins'])
    plot_bar(class_wins, "Wins per Class", 'class_vs_win', groupby='Class')


    # Class Statistics
    classes = ['Shadowcraft', 'Runecraft', 'Forestcraft', 'Swordcraft', 'Dragoncraft', 'Havencraft', 'Portalcraft', 'Bloodcraft']

    for c in classes:
        dfc = df[df['Class'] == c]

        # Class Archetypes
        class_archetype = count_col(dfc, ['Class', 'Archetype'])
        plot_pie(class_archetype, "Archetype Distribution for {} - Users".format(c), "{}_arch_pie".format(c))


def analyze_vertical(df):
    classes = ['Shadowcraft', 'Runecraft', 'Forestcraft', 'Swordcraft', 'Dragoncraft', 'Havencraft', 'Portalcraft', 'Bloodcraft']


    for c in classes:
        dfc = stack_match(df, c)   # Full

        # Avg Winrate
        df_mean = mean_col(dfc, ['Class', 'Class_o'], 'Result')
        plot_bar(df_mean, 'Class vs Class Winrate for {} - All'.format(c), 'class_vs_class_win_{}'.format(c))


        # Archetypes
        class_archetype = count_col(dfc, ['Class', 'Archetype'])
        plot_pie(class_archetype, "Archetype Distribution for {} - All".format(c), "{}_full_arch_pie".format(c))


    # Most popular decks
    popular_decks = most_popular_n(df, 10)
    plot_bar(popular_decks, "Most used decks - All", 'most_used_all')

    # Highest Winrate Decks
    # best_decks = best_decks_n(df, 10)
    # plot_bar(best_decks, 'Highest Winrate Decks - All', 'best_deck_all')


