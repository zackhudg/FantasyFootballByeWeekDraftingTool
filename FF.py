import pandas as pd
import operator

# ppr = pd.read_csv(r'FantasyPros_2023_Overall_ADP_Rankings_PPR.csv')
# halfppr = pd.read_csv(r'FantasyPros_2023_Overall_ADP_Rankings_HalfPPR.csv')
# std = pd.read_csv(r'FantasyPros_2023_Overall_ADP_Rankings_STD.csv')

league_size = 10 #input("How many teams in the league?")
# draft_type = input("Standard snake draft? (Y/N)") #default Y
league_scoring = 'PPR' #input("What scoring method is used? (PPR, HalfPPR, STD)")
draft_number = 1 #input("What is your pick number?")

teams = list()

# OR: import league settings

filePath = 'FantasyPros_2023_Overall_ADP_Rankings_'+league_scoring+'.csv'
df = pd.read_csv(filePath)
for i in range(1, league_size+1):
    for bye_week in range(1, 17): # Week number

        team = pd.DataFrame()
        draft_number = i
        next_pick = draft_number

        current_df = df.loc[df['Bye'] == bye_week]
        score = 0.0

        # Potential Scenarios:
        # 1: Everyone drafts at ADP (Expected)
        # 2: I can reach a few picks above ADP (Upper)
        # 3: I get sniped every time (Lower)
        # 4: Feed in mocks?

        for round_number in range(0, 10): # 8 Starters
            pick = current_df[current_df['Rank'] >= next_pick].iloc[:1]
            pick['OverallPick'] = next_pick
            current_df = current_df[current_df['Rank'] >= next_pick].iloc[1:]

            team = pd.concat([team, pick])
            score += pick['AVG'].values

            next_draft_number = league_size - draft_number + 1
            next_pick += (2 * next_draft_number) - 1
            draft_number = next_draft_number

        if len(score) != 0:
            teams.append((i, bye_week, score[0], team)) # i = original draft_number

teams.sort(key=lambda v : v[2])
for i in range(0, len(teams)):
    team = teams[i]
    print('------------------------')
    print('Draft Number:', team[0])
    print('Bye Week:', team[1])
    print('Score:', team[2])
    if i < 10:
        print('Team:\n', team[3])



