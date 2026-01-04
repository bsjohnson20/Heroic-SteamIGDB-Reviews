import ftfy
import tqdm
from cachier import cachier

from libs.igdb import IGDB
import libs.epiclibrary as ep
from libs.steam import SteamAPI

from loguru import logger as log

# Set logger level
import sys
log.remove()
log.add(sys.stderr, level="INFO")

# IGDB = IGDB()
# game_title = "Sea of thieves"
# body = f"""search "{game_title}";\nfields id,name,rating,category;"""
# print(IGDB.get_game_data(body=body))

games = ep.EpicLibrary().fetch_games()

# games = games[5:10]

igdb = IGDB()
steam = SteamAPI()


# @cachier()
def igdb_get_game(title):
    body = f"""search "{title}";\nfields id,name,rating,category,rating_count;""".encode("utf-8")
    return igdb.get_game_data(body=body)

def steam_get_game(title):
    return steam.search_details(title)

def get_game_data(title):
    # grabs from IGDB AND steam
    igdb = igdb_get_game(title)
    steam_response = steam.search_details(title)
    game = dict()
    try:
        game.update(igdb)
    except TypeError as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # log.error(f"Could not get game data for {title}. Full traceback: {exc_traceback, exc_value}")
    try:
        game.update(steam_response)
    except TypeError as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        log.error(f"STEAM could not get game data for {title}. Full traceback: {exc_traceback, exc_value}")
    if "name" not in game:
        game["name"] = title
    return game


@cachier()
def scan_library():
    log.info(f"ppScanning {len(games)} games")
    game_data = []
    for game in tqdm.tqdm(games):
        title = game['title']
        log.debug(f"Title: {title}")
        game_data.append(get_game_data(title))
        # game_data.append(igdb_get_game(title=title))
    return game_data

def sort_games(game_data):
    if game_data == None:
        return 9999
    if "rating_count" in game_data:
        return game_data['rating_count']
    elif "total_reviews" in game_data:
        return game_data['total_reviews']
    else:
        return 9999

CLEAR_CACHE = False
if CLEAR_CACHE:
    scan_library.clear_cache()
    steam.search_game.clear_cache()
    steam.game_details.clear_cache()
    steam.get_reviews.clear_cache()
    log.info("Cleared Cache")

games = scan_library()
games.sort(key=sort_games, reverse=True)

# sort games
# reorder data to be at the end
keys = list(games[0].keys())
keys.pop(keys.index("data"))
# keys.append("data")


log.info(f"Found {len(games)-games.count(None)}/{len(games)}. Errors: {games.count(None)}")
import csv
with open('games.csv', 'w', newline='\n', errors='replace') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(keys)
    # writer.writerow(["Title", "Rating", "Rating_Count"])
    for game in games:
        if game == None:
            continue
        cleaned = game
        if "id" not in cleaned:
            cleaned["id"]= ""
        row = [
            cleaned.get("name", ""),
            cleaned.get("id", ""),
            cleaned.get("review_score", ""),
            cleaned.get("review_score_desc", ""),
            cleaned.get("total_positive", ""),
            cleaned.get("total_negative", ""),
            cleaned.get("total_reviews", ""),
        ]

        writer.writerow(row)
