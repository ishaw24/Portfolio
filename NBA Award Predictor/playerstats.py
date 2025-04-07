import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats
from helperfunctions import year_range, wait_on_error, PLAYERSTATS_PERGAME_FILEPATH


years = year_range('1998-99', '2023-24')

check_csv = True # if we want to check what data is already in the written .csv and not rerequest it, only grab years not found in .csv
if check_csv:
    df = pd.read_csv(PLAYERSTATS_PERGAME_FILEPATH)
    years = [year for year in years if year not in pd.unique(df['YEAR'])]
    
print(f'Grabbing data for the following seasons:\n{years}')

dfs = [
    wait_on_error(leaguedashplayerstats.LeagueDashPlayerStats, wait = 5.0,
    per_mode_detailed='PerGame',
    season_type_all_star='Regular Season',
    season=year,
    league_id_nullable='00'
    ).get_data_frames()[0].assign(YEAR=year)
    for year in years
]

if check_csv:
    dfs.append(df)

df = pd.concat(dfs, axis='index')

df.to_csv(PLAYERSTATS_PERGAME_FILEPATH, index=False)
print(f'Saved {len(df)} player-seasons for {len(pd.unique(df['PLAYER_ID']))} unique players')