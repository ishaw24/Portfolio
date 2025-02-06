import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats

data = leaguedashplayerstats.LeagueDashPlayerStats(
    league_id_nullable='00', 
    measure_type_detailed_defense = 'Base',
    per_mode_detailed='Per100Possessions',
    season='2023-24',
    season_type_all_star='Regular Season',
    rank='N'
    ).get_data_frames()[0]

data_filtered = data[['PLAYER_NAME','PTS', 'AST', 'REB', 'TOV', 'STL', 'BLK', 'FG3A', 'FGA', 'FTA', 'FG3_PCT']]

data_filtered.to_csv('per100_23-24.csv')
