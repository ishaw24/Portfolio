import pandas as pd
from nba_api.stats.endpoints import playerawards
from helperfunctions import wait_on_error, PLAYERSTATS_PERGAME_FILEPATH, PLAYERAWARDS_FILEPATH
from random import sample

def main():
    df_playerstats = pd.read_csv(PLAYERSTATS_PERGAME_FILEPATH)
    player_ids = pd.unique(df_playerstats['PLAYER_ID']).tolist()

    # player_ids = sample(player_ids, 10)

    check_csv = True # if we want to check what data is already in the written .csv and not rerequest it, only grab player ids not found in .csv
    if check_csv:
        df = pd.read_csv(PLAYERAWARDS_FILEPATH)
        player_ids = [pid for pid in player_ids if pid not in pd.unique(df['PERSON_ID'])]
    
    if len(player_ids) == 0:
        return 0
    print(f'Grabbing award data for {len(player_ids)} players')

    dfs = []
    for pid in player_ids:
        response = wait_on_error(playerawards.PlayerAwards, wait=False, player_id = pid)
        if response is None:
            print('Response timed out, breaking loop and saving.')
            break
        content = response.get_data_frames()[0]
        
        if len(content) == 0:
            content.loc[0,'PERSON_ID'] = pid
        dfs.append(content)


    if check_csv:
        dfs.append(df)

    df = pd.concat(dfs, axis='index')

    df.to_csv(PLAYERAWARDS_FILEPATH, index=False)
    print(f'Saved {len(df)} awards for {len(pd.unique(df['PERSON_ID']))} players')
    return 1

if __name__ == 'main':
    main()