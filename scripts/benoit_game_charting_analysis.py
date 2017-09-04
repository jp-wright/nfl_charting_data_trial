import pandas as pd
import numpy as np
import datetime as dte
import matplotlib.pyplot as plt
import seaborn as sns
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



def get_percent_personnel_use(df, value, team='both', print_me=True):
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
    if print_me:
        print('Team: {t}'.format(t=team))
        print("Plays with {v}: {s} \nTotal plays: {t} \n{s}/{t} = {p:.2f}%".format(v=value, s=successes, t=total, p=perc*100))

    return perc


def get_percent_total_success_with_personnel(df, value, result='Successful', team='both', print_me=True):
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
    if print_me:
        print('Team: {t}'.format(t=team))
        print("Successful plays with {v}: {s} \nTotal successful plays: {t} \n{s}/{t} = {p:.2f}%".format(v=value, s=successes, t=total, p=perc*100))

    return perc


def get_percent_plays_with_personnel_that_succeeded(df, value, result='Successful', team='both', print_me=True):
    """Can pass in a formation for personnel, 'Successful' or 'Explosive' for result.  Must pass in as string representing the column name for that value. returns percent of all plays of a given formation/personnel that were successful"""

    value = value.lower()
    col = 'Formation' if value in ['singleback', 'shotgun', 'i-form', 'dual te', 'triple te'] else 'Personnel'
    if not team == 'both':
        team_mask = (df[result+'_Play'] == 1) & (df['Team'] == team)
        successes = df.loc[team_mask & (df[col].str.lower().str.contains(value))].shape[0]
        total = df[(df[col].str.lower().str.contains(value)) & (df['Team'] == team)].shape[0]
    else:
        successes = df.loc[(df[result+'_Play'] == 1) & (df[col].str.lower().str.contains(value))].shape[0]
        total = df[df[col].str.lower().str.contains(value)].shape[0]

    perc = successes / total if total > 0 else 0

    if print_me:
        print('Team: {t}'.format(t=team))
        print("Successful plays with {v}: {s} \nTotal plays with {v}: {t} \n{s}/{t} = {p:.2f}%".format(v=value, s=successes, t=total, p=perc*100))

    return perc



def plot_bars(vals_1, vals_2=None, labels=None, team=None):
    # if team == 'GB':
    #     color = 'green'
    # elif team == 'OAK':
    #     color = 'grey'
    # else:
    #     color = ''
    perc_axis = np.arange(0, .7, .1)
    fig = plt.figure(figsize=(8, 8))
    # plt.title("Formation Usage Comparison")
    if vals_2:
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)
        ax1.bar(range(len(vals_1)), vals_1, tick_label=labels, color='DarkGreen', edgecolor='#003300', linewidth=1.5, label='Green Bay', zorder=5)
        ax2.bar(range(len(vals_2)), vals_2, tick_label=labels, color='grey', edgecolor='black', linewidth=1.5, label='Oakland', zorder=5)
        ax1.set_ylim([0, .6])
        ax2.set_ylim([0, .6])
        ax1.set_yticks(perc_axis)
        ax2.set_yticks(perc_axis)
        ax1.set_yticklabels([str(int(n*100))+'%' for n in perc_axis])
        ax2.set_yticklabels([str(int(n*100))+'%' for n in perc_axis])
        ax1.set_title('Green Bay')
        ax2.set_title('Oakland')
        ax1.grid(axis='y', alpha=.6, zorder=0)
        ax2.grid(axis='y', alpha=.6, zorder=0)
    else:
        ax = fig.add_subplot(1, 1, 1)
        ax.bar(range(len(vals_1)), vals_1, tick_label=labels)

    fig.suptitle("Personnel Usage Comparison")
    # plt.ylim([0, 1])
    # plt.legend(loc='best')
    fig.tight_layout(pad=3)
    plt.show()
    plt.close()







if __name__ == '__main__':
    # files = [
    #     '../data/film_charting_broncos_raiders_week_9_cleaned.csv', \
    #     '../data/film_charting_packers_bears_week_7_cleaned.csv', \
    #     '../data/combined_game_charts_cleaned.csv', \
    #     '../data/film_charting_seahawks_3x1_sets_cleaned.csv', \
    #     '../data/film_charting_stafford_2016_cleaned.csv'
    #     ]

    df = load_data('../data/combined_game_charts_cleaned.csv')

    gb_percs, oak_percs = [], []
    for team in ['GB', 'OAK']:
        # for formation in ['singleback', 'shotgun', 'i-form']:#, 'dual te', 'triple te']:
        for formation in sorted(df['Personnel'].unique()):
            print(formation)
            # get_percent_total_success_with_personnel(df, formation, team=team)
            # get_percent_plays_with_personnel_that_succeeded(df, formation, team=team)
            val = get_percent_personnel_use(df, formation, team=team, print_me=False)
            if team == 'GB':
                gb_percs.append(val)
            else:
                oak_percs.append(val)

            print('')

    # plot_bars(gb_percs, oak_percs, ['Singleback', 'Shotgun', 'I-form'])
    plot_bars(gb_percs, oak_percs, sorted(df['Personnel'].unique()))


    """
    For each:
    situations, directions, margin, packages, shotgun/I-Form, motion, target dir, target align, rushers, yard line, what plays did they follow? follow penalties?

    1. explosive / success plays
    2. TD plays — same info
    3. Sacks — same info
    4. Packages — most common and in what situations, most successful, least successful, team character (6 OL v 3x1),
    5. Does shotgun = better passing?  Worse rushing? What about I-Form?
    6. Would certain QBs do better throwing to one side of the field?
    7. Do explosive plays come earlier or later in game?  Any correlation?  Do they happen more with certain players?
    8. Did Sacks kill drives?
    9. How did penalties affect drives?







    <BR><BR><BR><BR><BR><BR>

    cc = ['Team', 'Series', 'Play', 'Quarter', 'Time', 'Score_Margin', 'Down', 'Distance', 'LOS_to_Goal', 'Successful_Play', 'TD', 'Field_Goal']

    df.groupby(['Team', 'Series'], as_index=False)[cc].first()

    df.loc[(df['Successful_Play'] == 1) & (df['Down'] == 3), cc]




    df.groupby(['Successful_Play', 'Down'])['Down'].count().sort_values(ascending=False)
    ['Series', 'Play', 'Quarter', 'Time', 'Score_Margin', 'Down', 'Distance',
           'POS', 'Play_Type', 'Personnel', 'Formation', 'Motion', 'Runner',
           'Lead_Block', 'Target', 'Catch', 'Gain', 'Penalty', 'Play_Action',
           'Pass_Area', 'Pass_Depth', 'Run_Area', 'Def_Package', 'Def_Front',
           'Pass_Rushers', 'Team', 'Home/Road', 'Opponent', 'Goal_Line',
           'LOS_to_Goal', 'Net_Gain', 'Minute', 'Second', 'Num_RB', 'Num_TE',
           'Num_WR', '6_OL', 'Left_Split', 'Right_Split', 'Shotgun',
           'Shotgun_Offset', 'I-Form', 'I-Form_Offset', 'Motion_Bool',
           'Motion_Pos', 'Motion_Dir', 'Target_Pos', 'Target_Align', 'Pass_Dir',
           'TD', 'Explosive_Pass', 'Explosive_Pass_Yd', 'Explosive_Run',
           'Explosive_Run_Yd', 'Explosive_Play', 'Successful_Pass',
           'Successful_Run', 'Successful_Play', 'Sack_TFL', 'Sack_TFL_Yards',
           'Penalty_Team', 'Penalty_Type', 'Penalty_Yards']




    """





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
