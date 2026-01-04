from cachier import cachier

from libs.igdb import IGDB
import libs.epiclibrary as ep

from loguru import logger as log

# IGDB = IGDB()
# game_title = "Sea of thieves"
# body = f"""search "{game_title}";\nfields id,name,rating,category;"""
# print(IGDB.get_game_data(body=body))

games = ep.EpicLibrary().fetch_games()
igdb = IGDB()

CLEAR_CACHE = False

# @cachier()
def get_game(title):
    body = f"""search "{title}";\nfields id,name,rating,category,rating_count;""".encode("utf-8")
    return igdb.get_game_data(body=body)


@cachier()
def scan_library():
    log.info(f"Scanning {len(games)} games")
    game_data = []
    for game in games:
        title = game['title']
        log.info(f"Title: {title}")
        game_data.append(get_game(title=title))
    return game_data

def sort_games(game_data):
    if game_data == None:
        return 9999
    return game_data.rating_count

if CLEAR_CACHE:
    scan_library.clear_cache()
    log.info("Cleared Cache")

games = scan_library()
games.sort(key=sort_games, reverse=True)

# sort games

log.info(f"Found {len(games)-games.count(None)}/{len(games)}. Errors: {games.count(None)}")
import csv
with open('games.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Rating", "Rating_Count"])
    for game in games:
        if game == None:
            continue
        writer.writerow([game.name, round(float(game.rating)), game.rating_count])
