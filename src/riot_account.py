from utils import Utils
from match import Match


class RiotAccount:

    def __init__(self, game_name, tagline, num_of_matches):
        self.utils = Utils()
        self.match_history_length = num_of_matches
        self._game_name = game_name
        self._tagline = tagline
        self._puuid = None
        self._account_id = None
        self._summoner_id = None
        self._account_level = None
        self._tiers = {}
        self._ranks = {}
        self._league_points = {}
        self._wins = {}
        self._losses = {}
        self._winrates = {}
        self._matches = []
        self._load_account_info()

    def __str__(self):
        return (f"Name: {self._game_name}#{self._tagline}\n"
                f"PUUID: {self._puuid}\n"
                f"Summoner ID: {self._summoner_id}\n"
                f"Account ID: {self._account_id}\n"
                f"Level: {self._account_level}\n"
                f"Solo Q Rank: {self._tiers.get('Solo')} {self._ranks.get('Solo')} {self._league_points.get('Solo')}LP\n"
                f"Solo Q W/L: {self._wins.get('Solo')}W/{self._losses.get('Solo')}L - {self._winrates.get('Solo'):.2f}%\n"
                f"Flex Q Rank: {self._tiers.get('Flex')} {self._ranks.get('Flex')} {self._league_points.get('Flex')}LP\n"
                f"Flex Q W/L: {self._wins.get('Flex')}W/{self._losses.get('Flex')}L - {self._winrates.get('Flex'):.2f}%\n")

    def _load_account_info(self):
        self._set_account_puuid()
        self._set_account_info()
        self._set_ranked_info()
        self._set_match_history(self.match_history_length)

    def _set_account_puuid(self):
        endpoint = f"/riot/account/v1/accounts/by-riot-id/{self._game_name}/{self._tagline}"
        account_info = self.utils.make_request_region(endpoint)
        self._puuid = account_info.get("puuid")

    def _set_account_info(self):
        endpoint = f"/lol/summoner/v4/summoners/by-puuid/{self._puuid}"
        account_info = self.utils.make_request_server(endpoint)
        self._account_level = account_info.get("summonerLevel")
        self._account_id = account_info.get("accountId")
        self._summoner_id = account_info.get("id")

    def _set_ranked_info(self):
        endpoint = f"/lol/league/v4/entries/by-summoner/{self._summoner_id}"
        account_info = self.utils.make_request_server(endpoint)
        for queue in account_info:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                self._tiers["Solo"] = queue["tier"]
                self._ranks["Solo"] = queue["rank"]
                self._league_points["Solo"] = queue["leaguePoints"]
                self._wins["Solo"] = queue["wins"]
                self._losses["Solo"] = queue["losses"]
            elif queue["queueType"] == "RANKED_FLEX_SR":
                self._tiers["Flex"] = queue["tier"]
                self._ranks["Flex"] = queue["rank"]
                self._league_points["Flex"] = queue["leaguePoints"]
                self._wins["Flex"] = queue["wins"]
                self._losses["Flex"] = queue["losses"]
        self._winrates["Solo"] = (self._wins.get('Solo') / (self._wins.get('Solo') + self._losses.get('Solo'))) * 100
        self._winrates["Flex"] = (self._wins.get('Flex') / (self._wins.get('Flex') + self._losses.get('Flex'))) * 100

    def _set_match_history(self, num_of_matches):
        endpoint = f"/lol/match/v5/matches/by-puuid/{self._puuid}/ids?start=0&count={num_of_matches}"
        match_ids = self.utils.make_request_region(endpoint)
        for match_id in match_ids:
            match = Match(match_id)
            self._matches.append(match)

    def get_account_puuid(self):
        return self._puuid

    def get_account_level(self):
        return self._account_level

    def get_account_id(self):
        return self._account_id

    def get_summoner_id(self):
        return self._summoner_id

    def get_tiers(self):
        return self._tiers

    def get_ranks(self):
        return self._ranks

    def get_league_points(self):
        return self._league_points

    def get_wins(self):
        return self._wins

    def get_losses(self):
        return self._losses

    def get_winrates(self):
        return self._winrates

    def get_matches(self):
        return self._matches
