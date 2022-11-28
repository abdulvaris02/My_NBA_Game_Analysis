import csv
import re 
def load_data(filename):
    result = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter="|")
        fields = next(csvreader)
        for row in csvreader:
            result.append(row)
    return result
def find_players(play_by_play_moves):
    ans = []
    result = []
    for play in play_by_play_moves:
        result.append(re.split(r"[\s+;\(\)]", play[7]))
    for i in range(len(result)):
        for a in range(len(result[i])):
            if(result[i][a].endswith(".") and (result[i][a]+ " " + result[i][a+1]) not in ans):
                    ans.append(result[i][a] + " " + result[i][a+1])
    # print(*ans, sep = '\n')
    return ans

def make_players_statistics(play_by_play_moves, lst_of_players):
    statics_of_all_players = []
    lst_fg = []
    lst_fga = []

    for player in lst_of_players:
        player_static = {"Players": '', "FG": 0, "FGA": 0, "FG%": 0, "3P": 0, "3PA": 0, "3P%": 0, "FT": 0, "FTA": 0, "FT%": 0, "ORB": 0, "DRB": 0, "TRB": 0, "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0}
        player_static['Players'] = player
        
        for play in play_by_play_moves:
            
            match_fg = re.search(r"(\w\. \w+) makes 2-pt", play[-1])
            if match_fg: 
                if(match_fg.group(1) == player):  
                    player_static['FG'] += 1
                    player_static['FGA'] += 1
            
            match_fga = re.search(r"(\w\. \w+) misses 2-pt", play[-1])
            if match_fga:
                if(match_fga.group(1) == player):
                    player_static['FGA'] += 1

            match_3p = re.search(r"(\w. \w+) makes 3-pt", play[-1])
            if match_3p:
                if(match_3p.group(1) == player):
                    player_static['3P'] += 1
                    player_static['3PA'] += 1
                    player_static['FG'] += 1
                    player_static['FGA'] += 1
            
            match_3pa = re.search(r"(\w. \w+) misses 3-pt", play[-1])
            if match_3pa:
                if(match_3pa.group(1) == player):
                    player_static['3PA'] += 1
                    player_static['FGA'] += 1
            
            match_ft = re.search(r"(\w\. \w+) makes free throw", play[-1])
            if(match_ft): 
                    if(match_ft.group(1) == player):
                        player_static['FT'] += 1
                        player_static['FTA'] += 1

            match_ft_a = re.search(r"(\w\. \w+) misses free throw", play[-1])
            if(match_ft_a):
                if(match_ft_a.group(1) == player):
                    player_static['FTA'] += 1 
                  
            match_orb = re.search(r"Offensive rebound by (\w\. \w+)", play[-1])
            if(match_orb):
                if(match_orb.group(1) == player):
                    player_static['ORB'] += 1
                    player_static['TRB'] += 1
            
            match_drb = re.search(r"Defensive rebound by (\w\. \w+)", play[-1])
            if(match_drb):
                if(match_drb.group(1) == player):
                    player_static['DRB'] += 1
                    player_static['TRB'] += 1
            
            match_ast = re.search(r"assist by (\w. \w+)", play[-1])
            if(match_ast):
                if(match_ast.group(1) == player): 
                    player_static['AST'] += 1
            
            match_stl = re.search(r"steal by (\w. \w+)", play[-1])            
            if(match_stl):
                if(match_stl.group(1) == player):
                    player_static['STL'] += 1
            
            match_blk = re.search(r"block by (\w. \w+)", play[-1])
            if(match_blk):
                if(match_blk.group(1) == player):
                    player_static['BLK'] += 1

            match_tov = re.search(r"Turnover by (\w. \w+)", play[-1])            
            if(match_tov):
                if(match_tov.group(1) == player):
                    player_static['TOV'] += 1        
            
            match_pf = re.search(r"foul by (\w\. \w+)", play[-1])
            if(match_pf):
                if(match_pf.group(1) == player):
                    player_static['PF'] += 1
        lst_fg.append(player_static['FG'])
        lst_fga.append(player_static['FGA'])
        if(player_static['FGA'] != 0):
            player_static['FG%'] = round((player_static['FG'] / player_static['FGA']), 3)
        else:
            player_static['FG%'] = 0
        
        if(player_static['3PA'] != 0):
            player_static['3P%'] = round((player_static['3P'] / player_static['3PA']), 3)
        else:
            player_static['3P%'] = 0 

        if(player_static['FTA'] != 0):
            player_static['FT%'] = round((player_static['FT'] / player_static['FTA']), 3)
        else:
            player_static['FT%'] = 0
        
        if player_static["FG"] != 0:
            player_static["PTS"] = 2*(player_static['FG'] - player_static['3P']) + 3*(player_static['3P']) + player_static['FT']
        else:
            player_static["PTS"] = 0   
       
        # print(player_static)
        statics_of_all_players.append(player_static)
    return statics_of_all_players

def team_matching(play_by_play_moves, lst_of_players, statics):
    team_1_name = play_by_play_moves[0][2]
    team_i = 1
    while team_i != len(play_by_play_moves):
        if(team_1_name != play_by_play_moves[team_i][2]):
            team_2_name = play_by_play_moves[team_i][2]
            break
        team_i += 1

    # print(team_1_name, "\n\n ", team_2_name)
    # print("\n\n\n\n\n\n\n\n")

    teams_of_players = {name: '' for name in lst_of_players}
    total1 = {"total1": 'Team Totals', "FG": 0, "FGA": 0, "FG%": 0, "3P": 0, "3PA": 0, "3P%": 0, "FT": 0, "FTA": 0, "FT%": 0, "ORB": 0, "DRB": 0, "TRB": 0, "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0}
    total2 = {"total2": 'Team Totals', "FG": 0, "FGA": 0, "FG%": 0, "3P": 0, "3PA": 0, "3P%": 0, "FT": 0, "FTA": 0, "FT%": 0, "ORB": 0, "DRB": 0, "TRB": 0, "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0}
    for play in play_by_play_moves:
        match1 = re.search(r"(\w\. \w+) makes \d-pt", play[-1])
        if(match1):
            name = match1.group(1)
            teams_of_players[name] = play[2]
        
        match_pf = re.search(r"(\w\. \w+) misses \d-pt", play[-1])
        if(match_pf):
          name = match_pf.group(1)
          teams_of_players[name] = play[2]
        
        match_enter = re.search(r"(\w\. \w+) enters the game", play[-1])
        if(match_enter):
            name = match_enter.group(1)
            teams_of_players[name] = play[2]

        match_df = re.search(r"Defensive rebound by (\w\. \w+)", play[-1])
        if(match_df):
            name = match_df.group(1)
            teams_of_players[name] = play[2]

        match_df = re.search(r"Defensive rebound by (\w\. \w+-\w+)", play[-1])
        if(match_df):
            name = match_df.group(1)
            teams_of_players[name] = play[2]
            
    team1 = []
    team2 = []
    print(*statics[0].keys(), sep = '\t')
    for k,v in teams_of_players.items():
        if(v == team_2_name):
            for event in statics:
                if(event['Players'] == k):
                    team1.append(event)
                    print(*event.values(), sep='\t')
                    break
    
    for event in team1:
        for k, v in event.items():
            for key, value in total1.items():
                if(key == k):
                    try:
                        total1[k] += v
                    except:
                        continue
            try:             
                total1["FG%"] = round((total1["FG"]/total1["FGA"]), 3)
            except:
                continue 
            try:
                total1["3P%"] = round((total1["3P"]/total1["3PA"]), 3)
            except:
                continue
            try:
                total1["FT%"] = round((total1["FT"]/total1["FTA"]), 3)                    
            except:
                continue

    print(*total1.values(), sep='\t')
    print("\n\n")
      
    print(*statics[0].keys(), sep = '\t')
    for k,v in teams_of_players.items():
        if(v == team_1_name):
            for event in statics:
                if(event['Players'] == k):
                    team2.append(event)
                    print(*event.values(), sep='\t')
                    break
    for event in team2:
        for k, v in event.items():
            for key, value in total1.items():
                if(key == k):
                    try:
                        total2[k] += v
                    except:
                        continue     

    print(*total2.values(), sep='\t')
    return teams_of_players        

def _main():
    play_by_play_moves = load_data("nba_game_warriors_thunder_20181016.txt")
    lst_of_players = find_players(play_by_play_moves)
    statics = make_players_statistics(play_by_play_moves, lst_of_players)
    teams = team_matching(play_by_play_moves, lst_of_players, statics)
_main()
