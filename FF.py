import pandas as pd

# ppr = pd.read_csv(r'FantasyPros_2023_Overall_ADP_Rankings_PPR.csv')
# halfppr = pd.read_csv(r'FantasyPros_2023_Overall_ADP_Rankings_HalfPPR.csv')
# std = pd.read_csv(r'FantasyPros_2023_Overall_ADP_Rankings_STD.csv')

league_size = 10 #input("How many teams in the league?")
# draft_type = input("Standard snake draft? (Y/N)") #default Y
league_scoring = 'PPR' #input("What scoring method is used? (PPR, HalfPPR, STD)")
draft_number = 1 #input("What is your pick number?")

teams = {}

# OR: import league settings

filePath = 'FantasyPros_2023_Overall_ADP_Rankings_'+league_scoring+'.csv'
df = pd.read_csv(filePath)
for i in range(1, league_size):
    draft_number = i

    for j in range(10, 14): # Week number
        next_pick = draft_number

        current_df = df.loc[df['Bye'] == j]
        team = pd.DataFrame()
        score = 0

        for k in range(0, 3): # 8 Starters
            pick = current_df[current_df['Rank'] >= next_pick].iloc[:1]
            current_df = current_df[current_df['Rank'] >= next_pick].iloc[1:]

            team = pd.concat([team, pick])
            score += pick['Rank']

            next_draft_number = league_size - draft_number
            next_pick += 2 * (next_draft_number) + 1
            draft_number = next_draft_number
        
        teams[j] =  (score, team)

for team in teams:
    print('------------', team, '------------')
    print(teams[team][0])
    print(teams[team][1])


