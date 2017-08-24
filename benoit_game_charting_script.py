import pandas as pd
import numpy as np
import re
import datetime as dte


def load_data():
    def clean_col_names(df):
        if 'Gain' and 'Depth' not in df.columns:
            df.columns = df.loc[0].values
            df.drop(0, axis=0, inplace=True)

        df.rename(columns={'Series #': 'Series', 'Qtr': 'Quarter', 'Play #': 'Play', 'Play Description': 'Play_Type', 'Score': 'Score_Margin', 'Area': 'Pass_Area', 'Depth': 'Pass_Depth'}, inplace=True)
        df.columns = [col.replace(' ', '_') for col in df.columns]
        return df


    def fill_col_nans(df):
        """required to have a string instead of np.nan, which is a float, in order to do string parsing in later functions."""
        ## Change NaN into str='N/A' b/c can't index in with NaN (float)
        for col in ['Formation', 'Personnel', 'Target', 'Runner', 'Catch']:
            df[col].fillna('N/A', inplace=True)
        return df


    def fix_dtypes(df):
        for col in ['Series', 'Play', 'Quarter', 'Down', 'POS']:
            df[col] = df[col].astype(int)
        return df

    """There is extraneous data after column 25"""
    df = pd.read_csv('film_charting_seahawks_3x1_sets.csv', usecols=tuple([col for col in range(25)]))
    # df = pd.read_csv('film_charting_broncos_raiders_week_9.csv', usecols=tuple([col for col in range(25)]))
    df = clean_col_names(df)
    df = fill_col_nans(df)
    df = fix_dtypes(df)
    return df


def parse_data(df):
    def add_col_goalline(df):
        df['Goal_Line'] = [1 if 'G' in str(dist) else 0 for dist in df['Distance']]
        return df


    def clean_col_distance(df):
        df['Distance'] = df['Distance'].str.extract('(\d+)', expand=False)
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


    def add_col_off_team(df):
        """Static entry for this csv"""
        df['Off_Team'] = 'Raiders'
        return df


    def add_col_LOS(df):
        """Convert Point of Scrimmage to absolute Line of Scrimmage, in yards from target goal line (e.g. 1 = 1 yard from scoring, 67 = 67 yards from scoring)."""
        df['LOS_to_Goal'] = df['POS'].where(df['POS'] > 0, df['POS'] + 100)
        return df


    def add_col_net_gain(df):
        """Net Gain takes into account yards gained or lost by penalties as well as plays"""
        for s in df['Series'].unique():
            series_mask = df['Series'] == s
            dfs = df[series_mask]
            df.loc[series_mask, 'Net_Gain'] = df.loc[series_mask, 'LOS_to_Goal'] - df.loc[series_mask, 'LOS_to_Goal'].shift(-1)
            df.loc[dfs.index[-1], 'Net_Gain'] = df.loc[dfs.index[-1], 'Gain']
        df['Net_Gain'] = df['Net_Gain'].astype(int)
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
        R_mask = df['Formation'].str.lower().str.contains('shotgun offset R')
        L_mask = df['Formation'].str.lower().str.contains('shotgun offset L')
        df.loc[R_mask, 'Shotgun_Offset'] = 'Right'
        df.loc[L_mask, 'Shotgun_Offset'] = 'Left'
        return df


    def add_col_formation_IForm(df):
        IForm_mask = df['Formation'].str.lower().str.contains('i-form')
        df.loc[IForm_mask, 'I-Form'] = 1
        df.loc[~(IForm_mask), 'I-Form'] = 0
        return df


    def add_col_formation_IForm_offset(df):
        R_mask = df['Formation'].str.lower().str.contains('i-form offset R')
        L_mask = df['Formation'].str.lower().str.contains('i-form offset L')
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
        tfl_mask = df['Net_Gain'] < 0

        df.loc[((sack_mask) | (tfl_mask)) & ~(kneel_mask), 'Sack_TFL'] = 1
        df.loc[~((sack_mask) | (tfl_mask)) | (kneel_mask), 'Sack_TFL'] = 0
        return df


    def add_col_sack_TFL_yards(df):
        kneel_mask = df['Play_Type'].str.lower().str.contains('kneel')
        loss_mask = (df['Net_Gain'] < 0)
        sack_mask = df['Catch'].str.lower().str.contains('sack')

        df.loc[((sack_mask) | (loss_mask)) & ~(kneel_mask), 'Sack_TFL_Yards'] = df.loc[((sack_mask) | (loss_mask)) & ~(kneel_mask), 'Gain']
        return df


    def add_col_TD(df):
        """Whether a TD was scored on a play or not"""
        catch_mask = df['Catch'].str.contains('TD')
        rush_mask = df['Runner'].str.contains('TD')
        mask = ((catch_mask) | (rush_mask))

        df.loc[mask, 'TD'] = 1
        df.loc[~mask, 'TD'] = 0
        return df


    def void_kneeldown_yards(df):
        kneel_mask = df['Play_Type'].str.lower().str.contains('kneel')
        df.loc[kneel_mask, ['Gain', 'Net_Gain']] = np.nan
        return df



    df = add_col_off_team(df)
    df = add_col_goalline(df)
    df = clean_col_score(df)
    df = clean_col_distance(df)
    df = add_col_LOS(df)
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
    df = add_col_sack_TFL(df)
    df = add_col_sack_TFL_yards(df)
    df = void_kneeldown_yards(df)
    return df


if __name__ == '__main__':
    df = load_data()
    df = parse_data(df)
    dfg = df.groupby('Series')

    df.to_csv('~/Desktop/bronc2.csv', index=False)
