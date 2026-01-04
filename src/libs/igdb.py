import http.client
import json
import os
from loguru import logger as log
from cachier import cachier
from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry



class TwitchOAuth:
    def __init__(self):
        log.info("Initializing Twitch OAuth")
        load_dotenv()
        self.conn = http.client.HTTPSConnection("api.igdb.com")
        self.headers = {"User-Agent": "insomnia/12.2.0"}
        self.access_token = self.get_access_token()
        log.info("Done initializing Twitch OAuth")

    @cachier()
    def get_access_token(self):
        log.info("Fetching access token")
        conn = http.client.HTTPSConnection("id.twitch.tv")
        conn.request(
            "POST",
            f"/oauth2/token?client_id={os.getenv('client_id')}&client_secret={os.getenv('client_secret')}&grant_type=client_credentials",
            "",
            self.headers,
        )

        res = conn.getresponse()
        data = res.read()
        log.info("Fetched access token")
        return json.loads(data.decode("utf-8"))['access_token']

class Game:
    def __init__(self, id, name, rating, rating_count):
        log.debug("Initializing Game")
        self.id = id
        self.name = name
        self.rating = rating
        self.rating_count = rating_count

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Rating: {self.rating}, Rating Count: {self.rating_count}"

class IGDB(TwitchOAuth):
    def __init__(self):
        super().__init__()
        log.info("Initializing IGDB")

    @cachier()
    @sleep_and_retry
    @limits(calls=4, period=1)
    def get_game_data(self, body="fields id,name,rating,category,rating_count"):
        self.headers["Authorization"] = f"Bearer {self.access_token}"
        self.headers["Client-ID"] = os.getenv('client_id')#
        # print(self.headers)
        self.conn.request(
            "POST",
            url=f"/v4/games?",
            body=body,
            headers=self.headers,
        )

        res = self.conn.getresponse()
        data = res.read()
        # json


        try:
            js = json.loads(data.decode("utf-8"))[0]
            if {'id','name','rating','rating_count'}.issubset(js):
                return Game(js["id"], js["name"], js["rating"], js["rating_count"])
            else:
                log.error("Missing Tags: %s" % js)
                return None
        except IndexError as e:
            log.error(f"IndexError: {e}")
            return None

