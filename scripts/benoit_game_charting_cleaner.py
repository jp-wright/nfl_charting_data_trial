import pandas as pd
import numpy as np
import datetime as dte
# import pickle


def load_data(filename):
    """There is extraneous data after column 25"""
    def clean_col_names(df):
        if 'Gain' and 'Catch' not in df.columns:
            df.columns = df.loc[0].values
            df.drop(0, axis=0, inplace=True)

        df.rename(columns={'Series #': 'Series', 'Qtr': 'Quarter', 'Play #': 'Play', 'Play Description': 'Play_Type', 'Score': 'Score_Margin', 'Area': 'Pass_Area', 'Depth': 'Pass_Depth'}, inplace=True)

        df.columns = [col.replace(' ', '_') for col in df.columns]
        return df

    def drop_empty_rows(df):
        df.dropna(axis=0, thresh=12, inplace=True)
        return df

    def add_col_name_loc_opp(df, filename):
        if 'packers' in filename:
            df['Team'] = 'GB'
            df['Home/Road'] = 'Home'
            df['Opponent'] = 'CHI'
        elif 'raiders' in filename:
            df['Team'] = 'OAK'
            df['Home/Road'] = 'Home'
            df['Opponent'] = 'DEN'
        return df


    df = pd.read_csv(filename, usecols=tuple([col for col in range(25)]))
    df = clean_col_names(df)
    df = drop_empty_rows(df)
    df = add_col_name_loc_opp(df, filename)
    df = fix_nans_dtypes(df)
    return df


def fix_nans_dtypes(df):
    def fill_col_nans(df):
        """Certain cols required to have a string instead of np.nan, which is a float, in order to do string parsing in later functions."""

        ## Change NaN into str='N/A' b/c can't index in with NaN (float)
        for col in ['Formation', 'Personnel', 'Target', 'Runner', 'Catch']:
            df[col].fillna('N/A', inplace=True)
        return df

    def fix_dtypes(df):
        """Other cols that need to be numeric must be converted after some parsing in their own functions"""
        for col in ['Series', 'Play', 'Quarter', 'Down', 'POS', 'Gain']:
            ## OT is str, set = 5 for 5th quarter
            if 'OT' in df['Quarter'].unique().tolist():
                df.loc[df['Quarter'] == 'OT', 'Quarter'] = '5'

            ## 2-pt Conv are 'undowned', set = 0 for int dtype
            # if pd.isnull(df['Down']).any():
            #     df.loc[pd.isnull(df['Down']), 'Down'] = 0

            try:
                df[col] = pd.to_numeric(df[col])
            except KeyError:
                print("{c} is not in columns; bypassing.".format(c=col))
        return df

    df = fill_col_nans(df)
    df = fix_dtypes(df)
    return df


def parse_data_into_new_cols(df):
    def add_col_goalline(df):
        df['Goal_Line'] = [1 if 'G' in str(dist) else 0 for dist in df['Distance']]
        return df


    def clean_col_distance(df):
        df['Distance'] = df['Distance'].str.extract('(\d+)', expand=False)
        df['Distance'] = df['Distance'].astype(float)
        return df


    def clean_col_score(df):
        up_mask = df['Score_Margin'].str.contains('Up')
        down_mask = df['Score_Margin'].str.contains('Down')
        tie_mask = df['Score_Margin'].str.contains('Tied')

        df.loc[up_mask, 'Score_Margin'] = df.loc[up_mask, 'Score_Margin'].str.extract('(\d+)', expand=False)
        df.loc[down_mask, 'Score_Margin'] = '-' + df.loc[down_mask, 'Score_Margin'].str.extract('(\d+)', expand=False)
        df.loc[tie_mask, 'Score_Margin'] = 0

        df['Score_Margin'] = df['Score_Margin'].astype(int)
        return df


    def add_col_LOS(df):
        """Convert Point of Scrimmage to absolute Line of Scrimmage, in yards from target goal line (e.g. 1 = 1 yard from scoring, 67 = 67 yards from scoring)."""
        df['LOS_to_Goal'] = df['POS'].where(df['POS'] > 0, df['POS'] + 100)
        return df


    def add_col_net_gain(df):
        """Net Gain takes into account yards gained or lost by penalties as well as plays"""
        if 'Series' in df.columns:
            for s in df['Series'].unique():
                series_mask = df['Series'] == s
                dfs = df[series_mask]
                df.loc[series_mask, 'Net_Gain'] = df.loc[series_mask, 'LOS_to_Goal'] - df.loc[series_mask, 'LOS_to_Goal'].shift(-1)
                df.loc[dfs.index[-1], 'Net_Gain'] = df.loc[dfs.index[-1], 'Gain']
            df['Net_Gain'] = df['Net_Gain'].astype(int)
        else:
            pen_yards = df['Penalty'].str.extract('(\d+)$', expand=False).astype(float)
            pen_yards.fillna(0, inplace=True)
            df['Net_Gain'] = df['Gain'] + pen_yards
        return df


    def add_col_red_zone(df):
        rz_mask = df['LOS_to_Goal'] <= 20
        df.loc[rz_mask, 'Red_Zone'] = 1
        df.loc[~(rz_mask), 'Red_Zone'] = 0
        return df


    def add_cols_minute_and_second(df):
        """Split time col on the colon, take the numbers in front of it as the minutes, after it as seconds"""
        df['Minute'] = df['Time'].str.split(':', expand=True).loc[:, 0]
        df['Second'] = df['Time'].str.split(':', expand=True).loc[:, 1]
        return df


    def add_col_NumTE(df):
        one_TE_mask = (df['Personnel'].str.match('\d1')) | \
                        ((df['Formation'].str.lower().str.contains('closed')) & \
                            ~(df['Formation'].str.lower().str.contains('dual te')) & \
                            ~(df['Personnel'].str.match('\d2')))
        two_TE_mask = (df['Personnel'].str.match('\d2')) | (df['Formation'].str.lower().str.contains('dual te'))
        three_TE_mask = (df['Personnel'].str.match('\d3')) | (df['Formation'].str.lower().str.contains('triple te'))

        df.loc[one_TE_mask, 'Num_TE'] = 1
        df.loc[two_TE_mask, 'Num_TE'] = 2
        df.loc[three_TE_mask, 'Num_TE'] = 3
        return df


    def add_col_NumRB(df):
        one_RB_mask = (df['Personnel'].str.match('1\d')) | \
                        (df['Formation'].str.lower().str.match('singleback')) | \
                        ((df['Formation'].str.lower().str.contains('closed')) & \
                            ~(df['Formation'].str.lower().str.contains('dual rb')) & \
                            ~(df['Personnel'].str.match('2\d')))
        two_RB_mask = (df['Personnel'].str.match('2\d')) | (df['Formation'].str.contains('dual rb'))
        three_RB_mask = (df['Personnel'].str.match('3\d')) | (df['Formation'].str.contains('triple rb'))

        df.loc[one_RB_mask, 'Num_RB'] = 1
        df.loc[two_RB_mask, 'Num_RB'] = 2
        df.loc[three_RB_mask, 'Num_RB'] = 3
        return df


    def add_col_NumWR(df):
        df['Num_WR'] = 5 - df['Num_RB'] - df['Num_TE']
        return df


    def add_col_6OL(df):
        six_mask = df['Personnel'].str.lower().str.contains('6 ol')
        df.loc[six_mask, '6_OL'] = 1
        df.loc[~(six_mask), '6_OL'] = 0
        return df


    def add_col_formation_splits(df):
        df['Left_Split'] = df['Formation'].str.extract('^\"(\S)', expand=False)
        df['Right_Split'] = df['Formation'].str.extract('^\"\S{4}(\S)', expand=False)
        for col in ['Left_Split', 'Right_Split']:
            wide_mask = df[col] == '+'
            normal_mask = df[col] == '*'
            narrow_mask = df[col] == '-'

            df.loc[wide_mask, col] = 'Wide'
            df.loc[normal_mask, col] = 'Normal'
            df.loc[narrow_mask, col] = 'Narrow'
        return df


    def add_col_formation_shotgun(df):
        shotty_mask = df['Formation'].str.lower().str.contains('shotgun')
        df.loc[shotty_mask, 'Shotgun'] = 1
        df.loc[~(shotty_mask), 'Shotgun'] = 0
        return df


    def add_col_formation_shotgun_offset(df):
        R_mask = df['Formation'].str.lower().str.contains('shotgun offset r')
        L_mask = df['Formation'].str.lower().str.contains('shotgun offset l')
        df.loc[R_mask, 'Shotgun_Offset'] = 'Right'
        df.loc[L_mask, 'Shotgun_Offset'] = 'Left'
        return df


    def add_col_formation_IForm(df):
        IForm_mask = df['Formation'].str.lower().str.contains('i-form')
        df.loc[IForm_mask, 'I-Form'] = 1
        df.loc[~(IForm_mask), 'I-Form'] = 0
        return df


    def add_col_formation_IForm_offset(df):
        R_mask = df['Formation'].str.lower().str.contains('i-form offset r')
        L_mask = df['Formation'].str.lower().str.contains('i-form offset l')
        df.loc[R_mask, 'I-Form_Offset'] = 'Right'
        df.loc[L_mask, 'I-Form_Offset'] = 'Left'
        return df


    def add_col_motion_bool(df):
        df.loc[pd.notnull(df['Motion']), 'Motion_Bool'] = 1
        df.loc[pd.isnull(df['Motion']), 'Motion_Bool'] = 0
        return df


    def add_col_motion_pos(df):
        df['Motion_Pos'] = df['Motion'].str.extract('^(\S\S)', expand=False)
        return df


    def add_col_motion_direction(df):
        df['Motion_Dir'] = df['Motion'].str.extract('\s(\w*)$', expand=False)
        return df


    def add_col_target_position(df):
        pass_mask = ~(df['Target'].str.contains('N/A'))
        throwaway_mask = df['Target'].str.lower().str.contains('throwaway')
        RB_mask = df['Target'].str.lower().str.contains('rb|hb|fb')
        TE_mask = df['Target'].str.lower().str.contains('te')
        WR_mask = ~((TE_mask) | (RB_mask) | (throwaway_mask))

        df.loc[RB_mask, 'Target_Pos'] = 'RB'
        df.loc[TE_mask, 'Target_Pos'] = 'TE'
        df.loc[(pass_mask) & (WR_mask), 'Target_Pos'] = 'WR'
        return df


    def add_col_target_alignment(df):
        """ 1: Farthest from ball at snap
            2: Next farthest..
            3: ...
            4: Closest to ball"""
        df['Target_Align'] = df['Target'].str.extract('(\d)', expand=False)
        return df


    def add_col_pass_direction(df):
        R_mask = df['Target'].str.lower().str.contains('\(r')
        L_mask = df['Target'].str.lower().str.contains('\(l')

        df.loc[R_mask, 'Pass_Dir'] = 'Right'
        df.loc[L_mask, 'Pass_Dir'] = 'Left'
        return df


    def add_col_sack_TFL(df):
        kneel_mask = df['Play_Type'].str.lower().str.contains('kneel')
        sack_mask = df['Catch'].str.lower().str.contains('sack')
        tfl_mask = df['Net_Gain'] < 0 if 'Net_Gain' in df.columns else df['Gain'] < 0

        df.loc[((sack_mask) | (tfl_mask)) & ~(kneel_mask), 'Sack_TFL'] = 1
        df.loc[~((sack_mask) | (tfl_mask)) | (kneel_mask), 'Sack_TFL'] = 0
        return df


    def add_col_sack_TFL_yards(df):
        kneel_mask = df['Play_Type'].str.lower().str.contains('kneel')
        sack_mask = df['Catch'].str.lower().str.contains('sack')
        loss_mask = df['Net_Gain'] < 0 if 'Net_Gain' in df.columns else df['Gain'] < 0

        df.loc[((sack_mask) | (loss_mask)) & ~(kneel_mask), 'Sack_TFL_Yards'] = df.loc[((sack_mask) | (loss_mask)) & ~(kneel_mask), 'Gain']
        return df


    def add_col_penalty_team(df):
        pen_yards = df['Penalty'].str.extract('(\S*\d+)$', expand=False).astype(float)
        off_mask = pen_yards < 0
        def_mask = pen_yards > 0

        df.loc[off_mask, 'Penalty_Team'] = 'Offense'
        df.loc[def_mask, 'Penalty_Team'] = 'Defense'
        return df


    def add_col_penalty_type(df):
        df['Penalty_Type'] = df['Penalty'].str.split(',', expand=True).loc[:, 0]
        return df


    def add_col_penalty_yards(df):
        pen_yards = df['Penalty'].str.extract('(\S*\d+)$', expand=False).astype(float)
        pen_yards.fillna(0, inplace=True)
        df['Penalty_Yards'] = pen_yards
        return df


    def add_col_TD(df):
        """Whether a TD was scored on a play or not"""
        catch_mask = df['Catch'].str.contains('TD')
        rush_mask = df['Runner'].str.contains('TD')
        mask = ((catch_mask) | (rush_mask))

        df.loc[mask, 'TD'] = 1
        df.loc[~mask, 'TD'] = 0
        return df


    def add_cols_explosive_passes_and_yards(df):
        big_passes = (df['Play_Type'].str.lower().str.contains('pass')) & (df['Gain'] >= 16)
        df.loc[big_passes, 'Explosive_Pass'] = 1
        df.loc[~big_passes, 'Explosive_Pass'] = 0
        df.loc[big_passes, 'Explosive_Pass_Yd'] = df.loc[big_passes, 'Gain']
        return df


    def add_cols_explosive_runs_and_yards(df):
        big_runs = (df['Play_Type'].str.lower().str.contains('run')) & (df['Gain'] >= 12)
        df.loc[big_runs, 'Explosive_Run'] = 1
        df.loc[~big_runs, 'Explosive_Run'] = 0
        df.loc[big_runs, 'Explosive_Run_Yd'] = df.loc[big_runs, 'Gain']
        return df


    def add_col_explosive_play(df):
        play = (df['Explosive_Run'] == 1) | (df['Explosive_Pass'] == 1)
        df.loc[play, 'Explosive_Play'] = 1
        df.loc[~play, 'Explosive_Play'] = 0
        return df


    def add_col_successful_passes(df):
        """Using FootballOutsiders yardage values for 'successful plays'"""
        pass_mask = (df['Play_Type'].str.lower().str.contains('pass'))
        first_down = (df['Down'] == 1) & pass_mask
        second_down = (df['Down'] == 2) & pass_mask
        third_fourth_down = ((df['Down'] == 3) | (df['Down'] == 4)) & pass_mask

        success_pass_1st = df.loc[first_down, 'Gain'] >= (0.45 * df.loc[first_down, 'Distance'])
        success_pass_2nd = df.loc[second_down, 'Gain'] >= (0.6 * df.loc[second_down, 'Distance'])
        success_pass_3rd_4th = df.loc[third_fourth_down, 'Gain'] >= df.loc[third_fourth_down, 'Distance']

        success_1st_true = df.loc[first_down].loc[success_pass_1st]
        success_2nd_true = df.loc[second_down].loc[success_pass_2nd]
        success_3rd_4th_true = df.loc[third_fourth_down].loc[success_pass_3rd_4th]

        success_pass = \
            set(success_1st_true.index)\
            .union(set(success_2nd_true.index)\
            .union(set(success_3rd_4th_true.index)))

        df.loc[success_pass, 'Successful_Pass'] = 1

        pen_mask = df['Penalty_Team'] == 'Defense'
        df.loc[pen_mask, 'Successful_Pass'] = np.nan
        return df


    def add_col_successful_runs(df):
        """Using FootballOutsiders yardage values for 'successful plays'"""
        run_mask = (df['Play_Type'].str.lower().str.contains('run'))
        first_down = (df['Down'] == 1) & run_mask
        second_down = (df['Down'] == 2) & run_mask
        third_fourth_down = ((df['Down'] == 3) | (df['Down'] == 4)) & run_mask

        success_run_1st = df.loc[first_down, 'Gain'] >= (0.45 * df.loc[first_down, 'Distance'])
        success_run_2nd = df.loc[second_down, 'Gain'] >= (0.6 * df.loc[second_down, 'Distance'])
        success_run_3rd_4th = df.loc[third_fourth_down, 'Gain'] >= df.loc[third_fourth_down, 'Distance']

        success_1st_true = df.loc[first_down].loc[success_run_1st]
        success_2nd_true = df.loc[second_down].loc[success_run_2nd]
        success_3rd_4th_true = df.loc[third_fourth_down].loc[success_run_3rd_4th]

        success_run = \
            set(success_1st_true.index)\
            .union(set(success_2nd_true.index)\
            .union(set(success_3rd_4th_true.index)))

        df.loc[success_run, 'Successful_Run'] = 1

        ## Make Defensive Penalty a NaN, b/c not successful by O but not unsuccessful
        pen_mask = df['Penalty_Team'] == 'Defense'
        df.loc[pen_mask, 'Successful_Run'] = np.nan
        return df


    def add_col_successful_play(df):
        play = (df['Successful_Run'] == 1) | (df['Successful_Pass'] == 1)
        df.loc[play, 'Successful_Play'] = 1
        df.loc[~play, 'Successful_Play'] = 0

        ## Make Defensive Penalty a NaN, b/c not successful by O but not unsuccessful
        pen_mask = df['Penalty_Team'] == 'Defense'
        df.loc[pen_mask, 'Successful_Play'] = np.nan
        return df


    def void_kneeldown_yards(df):
        kneel_mask = df['Play_Type'].str.lower().str.contains('kneel')
        df.loc[kneel_mask, ['Gain']] = np.nan
        if 'Net_Gain' in df.columns:
            df.loc[kneel_mask, ['Net_Gain']] = np.nan
        return df


    def add_col_home_road(df):
        if 'Opponent' in df.columns:
            road_mask = df['Opponent'].str.lower().str.contains('at')
            df.loc[road_mask, 'Home/Road'] = 'Road'
            df.loc[~(road_mask), 'Home/Road'] = 'Home'
        return df


    def clean_col_opponent(df):
        if 'Opponent' in df.columns:
            df['Opponent'] = df['Opponent'].str.replace('at ', '')
            df.loc[df['Opponent'] == 'LA', 'Opponent'] = 'LAR'
        return df


    df = add_col_goalline(df)
    df = clean_col_score(df)
    df = clean_col_distance(df)
    df = add_col_LOS(df)
    df = add_col_red_zone(df)
    df = add_col_net_gain(df)
    df = add_cols_minute_and_second(df)
    df = add_col_NumRB(df)
    df = add_col_NumTE(df)
    df = add_col_NumWR(df)
    df = add_col_6OL(df)
    df = add_col_formation_splits(df)
    df = add_col_formation_shotgun(df)
    df = add_col_formation_shotgun_offset(df)
    df = add_col_formation_IForm(df)
    df = add_col_formation_IForm_offset(df)
    df = add_col_motion_bool(df)
    df = add_col_motion_pos(df)
    df = add_col_motion_direction(df)
    df = add_col_target_position(df)
    df = add_col_target_alignment(df)
    df = add_col_pass_direction(df)
    df = add_col_TD(df)
    df = add_cols_explosive_passes_and_yards(df)
    df = add_cols_explosive_runs_and_yards(df)
    df = add_col_explosive_play(df)
    df = add_col_penalty_team(df)
    df = add_col_penalty_type(df)
    df = add_col_penalty_yards(df)
    df = add_col_successful_passes(df)
    df = add_col_successful_runs(df)
    df = add_col_successful_play(df)
    df = add_col_sack_TFL(df)
    df = add_col_sack_TFL_yards(df)
    df = add_col_home_road(df)
    df = clean_col_opponent(df)
    df = void_kneeldown_yards(df)
    return df


def save_to_csv(df, fname, save=False):
    """Save defaults to False to prevent accidental overwrite"""
    if save:
        df.to_csv('../data/{f}.csv'.format(f=fname.replace('raw', 'cleaned')), index=False)
    return None



if __name__ == '__main__':
    files = [
        'film_charting_broncos_raiders_week_9_raw', \
        'film_charting_packers_bears_week_7_raw', \
        'film_charting_seahawks_3x1_sets_raw', \
        'film_charting_stafford_2016_raw'
        ]

    filename = files[0]
    for filename in files:
        df = load_data("../data/raw_data/{f}.csv".format(f=filename))
        df = parse_data_into_new_cols(df)
        save_to_csv(df, filename, save=True)


    df1 = pd.read_csv('../data/film_charting_broncos_raiders_week_9_cleaned.csv')
    df2 = pd.read_csv('../data/film_charting_packers_bears_week_7_cleaned.csv')
    df3 = df1.append(df2)
    df3.to_csv('../data/combined_game_charts_cleaned.csv', index=False)

    # dfg = df.groupby('Series')
