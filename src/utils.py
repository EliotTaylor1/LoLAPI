import json

import requests


class Utils:
    def __init__(self, api_key=None, region=None, server=None):
        if api_key and region and server:
            self.api_key = api_key
            self.region = region
            self.server = server
        else:
            with open("../config.json") as f:
                config = json.load(f)
            self.api_key = config.get("api_key")
            self.region = config.get("region")
            self.server = config.get("server")

    def make_request_region(self, endpoint):
        url = f"https://{self.region}.api.riotgames.com{endpoint}"
        print(f"making request to: {url}")
        headers = {
            "X-Riot-Token": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with {response.status_code}: {response.text}")

    def make_request_server(self, endpoint):
        url = f"https://{self.server}.api.riotgames.com{endpoint}"
        print(f"making request to: {url}")
        headers = {
            "X-Riot-Token": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with {response.status_code}: {response.text}")

    def convert_puuid_to_game_name(self, puuid):
        endpoint = f"/riot/account/v1/accounts/by-puuid/{puuid}"
        account_info = self.make_request_region(endpoint)
        game_name = f"{account_info.get('gameName')}#{account_info.get('tagLine')}"
        return game_name
