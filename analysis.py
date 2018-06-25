import pandas as pd
from tools import *



def analyze_horizontal(df, n):
    # ---- Single column distributions -----
    rank_count = count_col(df, "Rank")
    plot_pie(rank_count, "Rank Distribution - Stage {}".format(n), "rank_count_s{}".format(n))
    class_count = count_col(df, "Class")
    plot_pie(class_count, "Class Distribution - Stage {}".format(n), "class_count_s{}".format(n))


    # Rank Statistics
    rank_class = count_col(df, ['Rank', 'Class'])
    plot_bar(rank_class, "Ranks by Class - Stage {}".format(n), "rank_vs_class_s{}".format(n), groupby="Rank")

    rank_wins = count_col(df, ['Rank', 'Wins'])
    plot_bar(rank_wins, "Wins per Rank - Stage {}".format(n), "rank_vs_win_s{}".format(n), groupby='Rank')

    class_wins = count_col(df, ['Class', 'Wins'])
    plot_bar(class_wins, "Wins per Class - Stage {}".format(n), 'class_vs_win_s{}'.format(n), groupby='Class')


    # Class Statistics
    classes = ['Shadowcraft', 'Runecraft', 'Forestcraft', 'Swordcraft', 'Dragoncraft', 'Havencraft', 'Portalcraft', 'Bloodcraft']

    for c in classes:
        dfc = df[df['Class'] == c]

        # Class Archetypes
        class_archetype = count_col(dfc, ['Class', 'Archetype'])
        plot_pie(class_archetype, "Archetype Distribution for {} - Users - Stage {}".format(c, n), "{}_arch_pie_s{}".format(c, n))


def analyze_vertical(df, n):
    classes = ['Shadowcraft', 'Runecraft', 'Forestcraft', 'Swordcraft', 'Dragoncraft', 'Havencraft', 'Portalcraft', 'Bloodcraft']

    for c in classes:
        dfc = stack_match(df, c)   # Full

        # Avg Winrate
        df_mean = mean_col(dfc, ['Class', 'Class_o'], 'Result')
        plot_bar(df_mean, 'Class vs Class Winrate for {} - All - Stage {}'.format(c, n), '{}_vs_class_s{}'.format(c, n))


        # Archetypes
        class_archetype = count_col(dfc, ['Class', 'Archetype'])
        plot_pie(class_archetype, "Archetype Distribution for {} - All - Stage {}".format(c, n), "{}_full_arch_pie_s{}".format(c, n))


    # Most popular decks
    popular_decks = most_popular_n(df, 10)
    plot_bar(popular_decks, "Most used decks - All - Stage {}".format(n), 'most_used_all_s{}'.format(n))

    # Highest Winrate Decks
    # best_decks = best_decks_n(df, 10)
    # plot_bar(best_decks, 'Highest Winrate Decks - All - Stage {}'.format(n), 'best_deck_all_s{}'.format(n))


