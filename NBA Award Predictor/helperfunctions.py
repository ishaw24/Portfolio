from time import sleep
from requests.exceptions import ReadTimeout
PLAYERSTATS_PERGAME_FILEPATH = './Portfolio/NBA Award Predictor/Data/playerstats_pergame.csv'
PLAYERAWARDS_FILEPATH = './Portfolio/NBA Award Predictor/Data/playerawards.csv'

def year_formatter(year: str | int) -> str:
    # i.e. '2000' -> '2000-01'
    return f"{year}-{str(int(year) + 1)[-2:]}"

def year_range(start: str, end: str) -> list[str]:
    start_int, end_int = int(start[0:4]), int(end[0:4])
    return [year_formatter(i) for i in range(start_int, end_int + 1)]

def wait_on_error(func, wait: float | bool= 5.0, **kwargs): # nba.com's API can timeout with repeated calls, this is a "wait and try again" incase
    try:
        return func(**kwargs)
    except ReadTimeout:
        if wait is not False:
            sleep(wait)
            return func(**kwargs)
        else:
            return None
