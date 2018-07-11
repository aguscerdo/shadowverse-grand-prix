import pandas as pd
from tools import *



def analyze_horizontal(df, n, folder):
    path = folder + '/plots/'
    # ---- Single column distributions -----
    rank_count = count_col(df, "Rank")
    plot_pie(rank_count, "Rank Distribution - Stage {}".format(n), path+"pie_rank_count_s{}.png".format(n))
    class_count = count_col(df, "Class")
    plot_pie(class_count, "Class Distribution - Stage {}".format(n), path+"pie_class_count_s{}.png".format(n))


    # Rank Statistics
    rank_class = count_col(df, ['Rank', 'Class'])
    plot_bar(rank_class, "Ranks by Class - Stage {}".format(n), path+"bar_rank_vs_class_s{}.png".format(n), groupby="Rank")

    rank_wins = count_col(df, ['Rank', 'Wins'])
    plot_bar(rank_wins, "Wins per Rank - Stage {}".format(n), path+"bar_rank_vs_win_s{}.png".format(n), groupby='Rank')

    class_wins = count_col(df, ['Class', 'Wins'])
    plot_bar(class_wins, "Wins per Class - Stage {}".format(n), path+'bar_class_vs_win_s{}.png'.format(n), groupby='Class')


    # Class Statistics
    classes = ['Shadowcraft', 'Runecraft', 'Forestcraft', 'Swordcraft', 'Dragoncraft', 'Havencraft', 'Portalcraft', 'Bloodcraft']

    for c in classes:
        dfc = df[df['Class'] == c]

        # Class Archetypes
        class_archetype = count_col(dfc, ['Class', 'Archetype'])
        plot_pie(class_archetype, "Archetype Distribution for {} - Users - Stage {}".format(c, n), path+"pie-{}_arch_pie_s{}.png".format(c, n))


def analyze_vertical(df, n, folder):
    classes = ['Shadowcraft', 'Runecraft', 'Forestcraft', 'Swordcraft', 'Dragoncraft', 'Havencraft', 'Portalcraft', 'Bloodcraft']
    path = folder + '/plots/'
    for c in classes:
        dfc = stack_match(df, c)   # Full

        # Avg Winrate
        df_mean = mean_col(dfc, ['Class', 'Class_o'], 'Result')
        plot_bar(df_mean, 'Class vs Class Winrate for {} - All - Stage {}'.format(c, n), path+'bar_{}_vs_class_s{}.png'.format(c, n))


        # Archetypes
        class_archetype = count_col(dfc, ['Class', 'Archetype'])
        plot_pie(class_archetype, "Archetype Distribution for {} - All - Stage {}".format(c, n), path+"pie_{}_full_arch_pie_s{}.png".format(c, n))


    # Most popular decks
    popular_decks = most_popular_n(df, 10)
    plot_bar(popular_decks, "Most used decks - All - Stage {}".format(n), path+'bar_most_used_all_s{}.png'.format(n))

    # Highest Winrate Decks
    # best_decks = best_decks_n(df, 10)
    # plot_bar(best_decks, 'Highest Winrate Decks - All - Stage {}'.format(n), 'best_deck_all_s{}'.format(n))


