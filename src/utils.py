import json
import logging
import os
import requests
from dotenv import load_dotenv


def load_champion_data():
    url = "https://ddragon.leagueoflegends.com/cdn/14.16.1/data/en_US/champion.json"
    response = requests.get(url)
    if response.status_code == 200:
        champion_data = response.json()
        return champion_data
    else:
        raise Exception(f"Failed to fetch champion data {response.status_code}: {response.text}")


class Utils:
    logger = logging.getLogger(__name__)

    def __init__(self, api_key=None, region=None, server=None):
        if api_key and region and server:
            self.api_key = api_key
            self.region = region
            self.server = server
        else:
            load_dotenv()
            self.api_key = os.getenv("API_KEY")
            self.server = os.getenv("SERVER")
            self.region = os.getenv("REGION")

    def make_request_region(self, endpoint: str):
        url = f"https://{self.region}.api.riotgames.com{endpoint}"
        Utils.logger.info(f"making request to: {url}")
        headers = {
            "X-Riot-Token": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with {response.status_code}: {response.text}")

    def make_request_server(self, endpoint: str):
        url = f"https://{self.server}.api.riotgames.com{endpoint}"
        Utils.logger.info(f"making request to: {url}")
        headers = {
            "X-Riot-Token": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with {response.status_code}: {response.text}")
