import json

from cachier import cachier
import os
from steam_web_api import Steam
from dotenv import load_dotenv
import requests
load_dotenv()

def check_key():
    return os.environ.get("STEAM_API_KEY") is not None


class SteamAPI:
    def __init__(self):
        if check_key() is False:
            raise KeyError("Steam Key env Missing")
        key = os.getenv("STEAM_KEY")
        self.steam = Steam(key)

    @cachier()
    def search_game(self, query):
        search = self.steam.apps.search_games(query)
        # print(search)
        return search

    @cachier()
    def game_details(self, game_id):
        user = self.steam.apps.get_app_details(game_id)
        if user is None:
            return None
        id=list(user.keys())[0]
        user['data'] = user[id]['data']
        del user[id]
        return user

    @cachier()
    def get_reviews(self, game_id):
        url = f"https://store.steampowered.com/appreviews/{game_id}?json=1"
        r = requests.get(url).text
        reviews = json.loads(r)
        reviews = reviews['query_summary'] # dump review text
        data = dict()
        data['review_score'] = reviews['review_score']
        data['review_score_desc'] = reviews['review_score_desc']
        data['total_positive'] = reviews['total_positive']
        data['total_negative'] = reviews['total_negative']
        data['total_reviews'] = reviews['total_reviews']
        return data

    def search_details(self, query):
        # search for game then get details
        data = self.search_game(query)
        if len(data['apps']) == 0:
            return None

        # print(data)
        game = dict()
        game['name'] = data['apps'][0]['name']
        game['id'] = data['apps'][0]['id'][0]

        game.update(self.game_details(game['id']))
        game.update(self.get_reviews(game['id']))
        return game

        # print(self.game_details(game['id']))
        # print(self.get_reviews(game['id']))




# Testing
if __name__ == "__main__":
    from pprint import pprint
    steam = SteamAPI()

    steam.get_reviews.clear_cache()
    steam.game_details.clear_cache()
    steam.get_reviews.clear_cache()

    pprint(steam.search_details("Batman"))
    # print(search_details())