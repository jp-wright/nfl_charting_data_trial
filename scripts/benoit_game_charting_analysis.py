import pandas as pd
import numpy as np
import datetime as dte
# import pickle


def load_data(filename):
    return pd.read_csv(filename)



def get_col_val_counts(df, col, kind='bool'):
    if kind == 'bool':
        dfy = df[df[col] == 1]
        dfn = df[df[col] == 0]
    # elif kind == 'categorical'

    print()


def group_and_summarize(dfg, group_by, game='both'):
    """Group and provide some analysis of the chosen DF.  Use 'game' to select both games or just one game (home teams of GB or OAK)
    INPUT:  group_by --> col to group on
            game --> 'both', 'GB', or 'OAK'
    OUTPUT:
    """

    if game != 'both':
        dfg = df[df['Team'] == game].copy()
    dfg = dfg.groupby(group_by)








    return dfg['Gain'].apply(lambda x: x - x.mean())




def group_v_game_mean(dfg):
    for group, data in dfg:



def group_v_combined_mean():




def plot_():
    pass


if __name__ == '__main__':
    # files = [
    #     '../data/film_charting_broncos_raiders_week_9_cleaned.csv', \
    #     '../data/film_charting_packers_bears_week_7_cleaned.csv', \
    #     '../data/combined_game_charts_cleaned.csv', \
    #     '../data/film_charting_seahawks_3x1_sets_cleaned.csv', \
    #     '../data/film_charting_stafford_2016_cleaned.csv'
    #     ]

    df = load_data('../data/combined_game_charts_cleaned.csv')



    dfg = df.groupby('Successful')


    gg = df[df['Team'] == 'GB']
    gg[gg['Successful_Play'] == 1, 'Gain']
    gg[gg['Successful_Play'] == 0, 'Gain']
    gg.groupby('Successful_Play')['Gain'].transform(lambda x: x - x.mean())


    gg.groupby('Successful_Play')[['Down', 'Distance']].mean()
    #                         Down  Distance
    #    Successful_Play
    #    0                1.723404  8.106383
    #    1                1.923077  7.717949
