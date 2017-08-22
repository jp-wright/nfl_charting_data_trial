import pandas as pd
import numpy as np

def load_data():
    return pd.read_csv('film_charting_broncos_raiders_week_9.csv', usecols=tuple([col for col in range(25)]))


def add_col_team(df):
    df['Team'] = 'Raiders'
    return df


def add_col_LOS(df):
    """Convert Point of Scrimmage to absolute Line of Scrimmage, in yards from target goal line (e.g. 1 = 1 yard from scoring, 67 = 67 yards from scoring)."""
    df['abs_LOS'] = df['POS'].where(df['POS'] > 0, df['POS'] + 100)
    return df


def add_col_goalline(df):
    df['Goal_Line'] = [1 if 'G' in dist else 0 for dist in df['Distance']]
    return df


def clean_col_distance(df):
    df['Distance'] = df['Distance'].str.extract('(\d+)')
    return df


def clean_col_score(df):
    # score_dict = {'Tied': 0}
    # df['Temp_Score'] = ['']
    # df['Score'] =

    for idx in df.index:
        if df.loc[idx, 'Score'].contains('Tied'):
            df.loc[idx, 'Score'] = 0
        elif df.loc[idx, 'Score'].contains('Up'):
            df.loc[idx, 'Score'] = df.loc[idx, 'Score'].extract('(\d+)')
        elif df.loc[idx, 'Score'].contains('Down'):
            df.loc[idx, 'Score'] = '-' + df.loc[idx, 'Score'].extract('(\d+)')

    return df
# def calc_net_gain(start, end):
#     if (start < 0 and end > 0):
#         net_yards = 50 - abs(start) + 50 - abs(end)
#     elif (start > 0 and end < 0):
#         net_yards = (50 - abs(start) + 50 - abs(end)) * -1
#     elif start < 0 and end < 0:
#         net_yards = (abs(start) - abs(end)) * -1
#     else:
#         net_yards = abs(start) - abs(end)
#
#     return net_yards



if __name__ == '__main__':
    df = load_data()
    df = add_col_LOS(df)
    df = add_col_goalline(df)
    df = clean_col_distance(df)
    df = clean_col_score(df)
    dfg = df.groupby('Series #')




    for s in df['Series #'].unique():
        series_mask = df['Series #'] == s
        dfs = df[series_mask]
        df.loc[series_mask, 'true_gain'] = df.loc[series_mask, 'abs_LOS'] - df.loc[series_mask, 'abs_LOS'].shift(-1)
        df.loc[dfs.index[-1], 'true_gain'] = df.loc[dfs.index[-1], 'Gain']

    # penalty_mask = pd.notnull(df['Penalty'])
    # df.loc[penalty_mask, 'true_ga']


    ## Works but makes the final row in each group a NaN...  bad
    # df['calc_gain'] = dfg['abs_LOS'].shift(0) - dfg['abs_LOS'].shift(-1)




    ## Want to calculate net gain on a play, but must group it by series since last play of one series and first play of next series are unrelated/discontinuous
    ## So, groupby series.  Function used is calc_net_gain.  Want to do an all at once approach.
    ## Here is a very bad way of doing it line by line (bad)
    # for group, data in dfg:
    #     df.loc[data.index, 'calc_gain'] = calc_net_gain(data['Gain'], data['Gain'].shift(-1))
    #
    # df['calc_gain'] = calc_net_gain(dfg['Gain'], dfg['Gain'].shift(-1))
    #
    #
    #
    # for group, data in dfg:
    #
    # df['calc_gain'] = [calc_net_gain(g['Gain'], g['Gain'].shift(-1)) for g in [dfg.get_group(n) for n in dfg.groups]]
    #
    # dfg['Gain'].transform(lambda x: calc_net_gain(x, x.shift(-1)))

    # dfg['calc_gain'] = dfg.apply(get_play_yardage(dfg['POS'], dfg['POS'].shift(-1)))
    # for group, data in dfg:
    #     data['calc_gain'] =
    #     print(data['calc_gain'])

    # dfg['calc_gain'] = dfg['Gain'] - dfg['Gain'].shift(-1)
