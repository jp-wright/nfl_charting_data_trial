import pandas as pd
import numpy as np
import datetime as dte
# import pickle


def load_data(filename):
    return pd.read_csv(filename)



#
# def get_val_counts(dfv, group_col, target_col, game='both'):
#     if game != 'both':
#         dfv = dv[dv['Team'] == game].copy()
#
#     for cat in df[group_col].dropna().unique():
#         print(cat)
#         print(df.loc[df[group_col] == cat, target_col].value_counts())

    # print()


def group_and_summarize(dfg, group_by, target_col, game='both', method='mean'):
    """Group and provide some analysis of the chosen DF.  Use 'game' to select both games or just one game (home teams of GB or OAK)
    INPUT:  group_by --> col to group on
            game --> 'both', 'GB', or 'OAK'
    OUTPUT:
    """

    if game != 'both':
        dfg = df[df['Team'] == game].copy()
    dfg = dfg.groupby(group_by)
    # dfg[]


    # return dfg[target_col].apply(lambda x: x - x.mean())
    return dfg[target_col].value_counts()




def group_v_game_mean(dfg):
    pass
    # for group, data in dfg:



def group_v_combined_mean():
    pass



def get_percent_personnel_use(df, value, team='both'):
    """Can choose 'Formation' or 'Personnel' col.  Must pass in as string representing the column name for that value"""

    value = value.lower()
    col = 'Formation' if value in ['singleback', 'shotgun', 'i-form', 'dual te', 'triple te'] else 'Personnel'
    if not team == 'both':
        successes = df[(df[col].str.lower().str.contains(value)) & (df['Team'] == team)].shape[0]
        total = df[df['Team'] == team].shape[0]
    else:
        successes = df[df[col].str.lower().str.contains(value)].shape[0]
        total = df.shape[0]

    perc = successes / total if total > 0 else 0
    print("Plays with {v}: {s} \nTotal plays: {t} \n{s}/{t} = {p:.2f}%".format(v=value, s=successes, t=total, p=perc*100))

    return None


def get_percent_total_success_with_personnel(df, value, result='Successful', team='both'):
    """Can pass in a formation for personnel, 'Successful' or 'Explosive' for result.  Must pass in as string representing the column name for that value.  Returns percent of all successful plays that happened to be from this formation/personnel"""

    value = value.lower()
    col = 'Formation' if value in ['singleback', 'shotgun', 'i-form', 'dual te', 'triple te'] else 'Personnel'
    if not team == 'both':
        print('Team: {t}'.format(t=team))
        team_mask = (df[result+'_Play'] == 1) & (df['Team'] == team)
        successes = df.loc[team_mask & (df[col].str.lower().str.contains(value))].shape[0]
        total = df[team_mask].shape[0]
    else:
        print("All teams")
        successes = df.loc[(df[result+'_Play'] == 1) & (df[col].str.lower().str.contains(value))].shape[0]
        total = df[df[result+'_Play'] == 1].shape[0]

    perc = successes / total if total > 0 else 0
    print("Successful plays with {v}: {s} \nTotal successful plays: {t} \n{s}/{t} = {p:.2f}%".format(v=value, s=successes, t=total, p=perc*100))

    return None


def get_percent_plays_with_personnel_that_succeeded(df, value, result='Successful', team='both'):
    """Can pass in a formation for personnel, 'Successful' or 'Explosive' for result.  Must pass in as string representing the column name for that value. returns percent of all plays of a given formation/personnel that were successful"""

    value = value.lower()
    col = 'Formation' if value in ['singleback', 'shotgun', 'i-form', 'dual te', 'triple te'] else 'Personnel'
    if not team == 'both':
        print('Team: {t}'.format(t=team))
        team_mask = (df[result+'_Play'] == 1) & (df['Team'] == team)
        successes = df.loc[team_mask & (df[col].str.lower().str.contains(value))].shape[0]
        total = df[(df[col].str.lower().str.contains(value)) & (df['Team'] == team)].shape[0]
    else:
        print("All teams")
        successes = df.loc[(df[result+'_Play'] == 1) & (df[col].str.lower().str.contains(value))].shape[0]
        total = df[df[col].str.lower().str.contains(value)].shape[0]

    perc = successes / total if total > 0 else 0

    print("Successful plays with {v}: {s} \nTotal plays with {v}: {t} \n{s}/{t} = {p:.2f}%".format(v=value, s=successes, t=total, p=perc*100))

    return None



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

    for team in ['GB', 'OAK']:
        for formation in ['singleback', 'shotgun', 'i-form', 'dual te', 'triple te']:
            print(formation)
            get_percent_total_success_with_personnel(df, formation, team=team)
            print('')
            get_percent_plays_with_personnel_that_succeeded(df, formation, team=team)
            print('')









    #
    # dfg = df.groupby('Successful')
    #
    #
    # gg = df[df['Team'] == 'GB']
    # gg[gg['Successful_Play'] == 1, 'Gain']
    # gg[gg['Successful_Play'] == 0, 'Gain']
    # gg.groupby('Successful_Play')['Gain'].transform(lambda x: x - x.mean())
    #
    #
    # gg.groupby('Successful_Play')[['Down', 'Distance']].mean()
    #                         Down  Distance
    #    Successful_Play
    #    0                1.723404  8.106383
    #    1                1.923077  7.717949
