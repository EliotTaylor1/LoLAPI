import json
import requests


class RiotAPI:
    def __init__(self, api_key=None):
        if api_key:
            self.api_key = api_key
        else:
            with open("config.json") as f:
                config = json.load(f)
            self.api_key = config.get("api_key")

    def make_request(self, endpoint):
        url = f"https://europe.api.riotgames.com{endpoint}"
        headers = {
            "X-Riot-Token": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with {response.status_code}: {response.text}")