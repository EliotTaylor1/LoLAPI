import requests
import json


class RiotAccount:
    region_url = "https://europe.api.riotgames.com"

    def __init__(self, game_name, tagline):
        with open("config.json") as f:
            config = json.load(f)
        self.game_name = game_name
        self.tagline = tagline
        self.api_key = config.get("api_key")
        self.puuid = None
        self.load_account_info()

    def __str__(self):
        return f"Name: {self.game_name}#{self.tagline} ID: {self.puuid}"

    def make_request(self, endpoint):
        url = f"{self.region_url}{endpoint}"
        headers = {
            "X-Riot-Token": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with {response.status_code}: {response.text}")

    def load_account_info(self):
        endpoint = f"/riot/account/v1/accounts/by-riot-id/{self.game_name}/{self.tagline}"
        account_info = self.make_request(endpoint)
        self.puuid = account_info.get("puuid")

    def get_match_history(self, num_of_matches):
        endpoint = f"/lol/match/v5/matches/by-puuid/{self.puuid}/ids?start=0&count={num_of_matches}"
        matches = self.make_request(endpoint)
        return matches
