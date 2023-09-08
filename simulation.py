import pandas as pd
import random
import numpy as np

class Team:
    def __init__(self, draft_number, bye_week, score, diff_score, team_data):
        self.draft_number = draft_number
        self.bye_week = bye_week
        self.score = score
        self.diff_score = diff_score
        self.team_data = team_data

    def __hash__(self):
        # Convert relevant attributes to a tuple and hash it
        return hash((self.draft_number, self.bye_week, self.score, self.diff_score, tuple(self.team_data['Player'].values.tolist())))
    
    def __str__(self):
        # Format the object as a string
        team_data_str = self.team_data[['Player', 'POS', 'PickDiff', 'MyPick']].to_html()
        return f"Draft Number: {self.draft_number}\nBye Week: {self.bye_week}\nScore: {self.score}\nDiff Score: {self.diff_score}\nTeam:\n{team_data_str}"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.draft_number, self.bye_week, self.score, tuple(self.team_data['Player'].values.tolist())) == (other.draft_number, other.bye_week, other.score, tuple(other.team_data['Player'].values.tolist()))
        else:
            return False

def make_selection(current_df, next_pick, pos_count, round_number, adp_std):
    adp_values = current_df['AVG'].values + np.random.normal(0, adp_std, len(current_df))
    current_df.loc[:, 'PerturbedADP'] = adp_values
    pick = current_df[current_df['PerturbedADP'] >= next_pick].iloc[:1]
    current_df = current_df[current_df['PerturbedADP'] >= next_pick].iloc[1:]
    pick['PickDiff'] = pick['AVG'].values - next_pick

    (qb, rb, wr, te) = pos_count
    pos_str = pick['POS'].values[0][0:1]

    if round_number <= 8:
        if ((qb > 0 and pos_str == 'Q') or 
            (rb > 4 and pos_str == 'R') or 
            (wr > 4 and pos_str == 'W') or 
            (te > 1 and pos_str == 'T') or 
            (pos_str == "K") or 
            (pos_str == "D")):
            (pick, current_df) = make_selection(current_df, next_pick, pos_count, round_number, adp_std)
    else:
        if ((qb > 1 and pos_str == 'Q') or 
            (rb > 8 and pos_str == 'R') or 
            (wr > 8 and pos_str == 'W') or 
            (te > 2 and pos_str == 'T') or 
            (pos_str == "K") or 
            (pos_str == "D")):
            (pick, current_df) = make_selection(current_df, next_pick, pos_count, round_number, adp_std)

    return (pick, current_df)

def simulate_draft(league_size, league_scoring, draft_number, num_rounds, adp_std, number_of_sims):
    teams = {}

    file_path = f'FantasyPros_2023_Overall_ADP_Rankings_{league_scoring}.csv'
    df = pd.read_csv(file_path)
    df = df[['Player', 'Bye', 'AVG', 'POS']]
    original_draft_number = draft_number

    for i in range(number_of_sims):  # 5 simulations
        for bye_week in range(1, 17):  # Bye week number
            team = pd.DataFrame()
            next_pick = draft_number

            current_df = df.loc[df['Bye'] == bye_week]
            if current_df.empty:
                continue

            score = 0.0
            diff_score = 0
            pos_count = (0, 0, 0, 0)  # qb, rb, wr, te

            for round_number in range(1, num_rounds + 1):
                (pick, current_df) = make_selection(current_df, next_pick, pos_count, round_number, adp_std)

                (qb, rb, wr, te) = pos_count
                pos_str = pick['POS'].values[0][0:1]

                if pos_str == 'Q':
                    qb += 1
                elif pos_str == 'R':
                    rb += 1
                elif pos_str == 'W':
                    wr += 1
                elif pos_str == 'T':
                    te += 1

                pos_count = (qb, rb, wr, te)
                pick['MyPick'] = next_pick
                team = pd.concat([team, pick])
                score += pick['AVG'].values
                diff_score += pick['PickDiff'].values

                next_draft_number = league_size - draft_number + 1
                next_pick += (2 * next_draft_number) - 1
                draft_number = next_draft_number

            if len(score) != 0:
                # Create a Team instance
                team_instance = Team(original_draft_number, bye_week, score[0], diff_score[0], team)
                if team_instance in teams.keys():
                    teams[team_instance] += 1
                else:
                    teams[team_instance] = 1

    # teams.sort(key=lambda v: v.score)
    return teams
