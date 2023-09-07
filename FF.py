import pandas as pd
import random

# ppr = pd.read_csv(r'FantasyPros_2023_Overall_ADP_Rankings_PPR.csv')
# halfppr = pd.read_csv(r'FantasyPros_2023_Overall_ADP_Rankings_HalfPPR.csv')
# std = pd.read_csv(r'FantasyPros_2023_Overall_ADP_Rankings_STD.csv')

league_size = 10 #input("How many teams in the league?")
# draft_type = input("Standard snake draft? (Y/N)") #default Y
league_scoring = 'HalfPPR' #input("What scoring method is used? (PPR, HalfPPR, STD)")
draft_number = 6 #input("What is your pick number?")

teams = list()

# OR: import league settings

filePath = 'FantasyPros_2023_Overall_ADP_Rankings_'+league_scoring+'.csv'
df = pd.read_csv(filePath)
og_draft_number = draft_number

# ensures we are not picking too many of each position: 1QB, 4RB, 4WR, 4TE
def makeSelection(current_df, next_pick, posCount):
    pick = current_df[current_df['Rank'] >= next_pick].iloc[:1]
    current_df = current_df[current_df['Rank'] >= next_pick].iloc[1:]
    pick['PickDiff'] = pick['Rank'].values - next_pick
    (qb, rb, wr, te) = posCount
    posStr = pick['POS'].values[0][0:1]
    if ((qb > 0 and posStr == 'Q') or (rb > 2 and posStr == 'R') or (wr > 2 and posStr == 'W') or (te > 1 and posStr == 'T')):
        (pick, current_df) = makeSelection(current_df, next_pick, posCount)
    return (pick, current_df)

for i in range(0, 5): # 5 simulations
    for bye_week in range(1, 17): # Bye week number
        team = pd.DataFrame()
        #draft_number = i
        next_pick = draft_number

        current_df = df.loc[df['Bye'] == bye_week]
        if (current_df.empty):
            continue
        score = 0.0
        weekScore = 0.0
        diffScore = 0

        posCount = (0,0,0,0) # qb, rb, wr, te
        # Potential Scenarios:
        # 1: Everyone drafts at ADP (Expected)
        # 2: I can reach a few picks above ADP (Upper)
        # 3: I get sniped every time (Lower)
        # 4: Feed in mocks?

        for round_number in range(0, 8): # Starters ish
            (pick, current_df) = makeSelection(current_df, next_pick, posCount)
            if (random.randint(1, pick['PickDiff'].values + 4) == 1):
                (pick, current_df) = makeSelection(current_df, next_pick, posCount)
            (qb, rb, wr, te) = posCount
            posStr = pick['POS'].values[0][0:1]
            if (posStr == 'Q'):
                qb += 1
            elif (posStr == 'R'):
                rb += 1
            elif (posStr == 'W'):
                wr += 1
            elif (posStr == 'T'):
                te += 1
            posCount = (qb, rb, wr, te)
            pick['OverallPick'] = next_pick
            team = pd.concat([team, pick])
            score += pick['AVG'].values
            diffScore += pick['PickDiff'].values

            next_draft_number = league_size - draft_number + 1
            next_pick += (2 * next_draft_number) - 1
            draft_number = next_draft_number

        if len(score) != 0:
            teams.append((og_draft_number, bye_week, score[0], diffScore[0], team)) # i = original draft_number

teams.sort(key=lambda v : v[2])
best_per_draft_pos = [None]*17

for i in range(12):
    team = teams[i]
    print('------------------------')
    print('Draft Number:', team[0])
    print('Bye Week:', team[1])
    print('Score:', team[2])
    print('Diff Score:', team[3])
    print('Team:\n', team[4])


#     if (best_per_draft_pos[team[0]] == None):
#         best_per_draft_pos[team[0]] = (team[1], team[2], team[3])

# for i in range(1, 11):
#     print(i, best_per_draft_pos[i])
    
    




