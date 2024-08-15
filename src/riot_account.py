from utils import Utils


class RiotAccount:

    def __init__(self, game_name, tagline):
        self.utils = Utils()
        self._game_name = game_name
        self._tagline = tagline
        self._puuid = None
        self._account_id = None
        self._summoner_id = None
        self._account_level = None
        self._tiers = {}
        self._ranks = {}
        self._lps = {}
        self._wins = {}
        self._losses = {}
        self._wrs = {}
        self.load_account_info()
        self._matches = []

    def __str__(self):
        return (f"Name: {self._game_name}#{self._tagline}\n"
                f"PUUID: {self._puuid}\n"
                f"Summoner ID: {self._summoner_id}\n"
                f"Account ID: {self._account_id}\n"
                f"Level: {self._account_level}\n"
                f"Solo Q Rank: {self._tiers.get('Solo')} {self._ranks.get('Solo')} {self._lps.get('Solo')}LP\n"
                f"Solo Q W/L: {self._wins.get('Solo')}/{self._losses.get('Solo')} - {self._wrs.get('Solo'):.2f}%\n"
                f"Flex Q Rank: {self._tiers.get('Flex')} {self._ranks.get('Flex')} {self._lps.get('Flex')}LP\n"
                f"Flex Q W/L: {self._wins.get('Flex')}/{self._losses.get('Flex')} - {self._wrs.get('Flex'):.2f}%\n")

    def load_account_info(self):
        self._set_account_puuid()
        self._set_account_level()
        self._set_account_id()
        self._set_summoner_id()
        self._set_tiers()
        self._set_ranks()
        self._set_lps()
        self._set_wins()
        self._set_losses()
        self._set_wrs()

    def _set_account_puuid(self):
        endpoint = f"/riot/account/v1/accounts/by-riot-id/{self._game_name}/{self._tagline}"
        account_info = self.utils.make_request_region(endpoint)
        self._puuid = account_info.get("puuid")

    def _set_account_level(self):
        endpoint = f"/lol/summoner/v4/summoners/by-puuid/{self._puuid}"
        account_info = self.utils.make_request_server(endpoint)
        self._account_level = account_info.get("summonerLevel")

    def _set_account_id(self):
        endpoint = f"/lol/summoner/v4/summoners/by-puuid/{self._puuid}"
        account_info = self.utils.make_request_server(endpoint)
        self._account_id = account_info.get("accountId")

    def _set_summoner_id(self):
        endpoint = f"/lol/summoner/v4/summoners/by-puuid/{self._puuid}"
        account_info = self.utils.make_request_server(endpoint)
        self._summoner_id = account_info.get("id")

    def _set_tiers(self):
        endpoint = f"/lol/league/v4/entries/by-summoner/{self._summoner_id}"
        account_info = self.utils.make_request_server(endpoint)
        for queue in account_info:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                self._tiers["Solo"] = queue["tier"]
            elif queue["queueType"] == "RANKED_FLEX_SR":
                self._tiers["Flex"] = queue["tier"]

    def _set_ranks(self):
        endpoint = f"/lol/league/v4/entries/by-summoner/{self._summoner_id}"
        account_info = self.utils.make_request_server(endpoint)
        for queue in account_info:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                self._ranks["Solo"] = queue["rank"]
            elif queue["queueType"] == "RANKED_FLEX_SR":
                self._ranks["Flex"] = queue["rank"]

    def _set_lps(self):
        endpoint = f"/lol/league/v4/entries/by-summoner/{self._summoner_id}"
        account_info = self.utils.make_request_server(endpoint)
        for queue in account_info:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                self._lps["Solo"] = queue["leaguePoints"]
            elif queue["queueType"] == "RANKED_FLEX_SR":
                self._lps["Flex"] = queue["leaguePoints"]

    def _set_wins(self):
        endpoint = f"/lol/league/v4/entries/by-summoner/{self._summoner_id}"
        account_info = self.utils.make_request_server(endpoint)
        for queue in account_info:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                self._wins["Solo"] = queue["wins"]
            elif queue["queueType"] == "RANKED_FLEX_SR":
                self._wins["Flex"] = queue["wins"]

    def _set_losses(self):
        endpoint = f"/lol/league/v4/entries/by-summoner/{self._summoner_id}"
        account_info = self.utils.make_request_server(endpoint)
        for queue in account_info:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                self._losses["Solo"] = queue["losses"]
            elif queue["queueType"] == "RANKED_FLEX_SR":
                self._losses["Flex"] = queue["losses"]

    def _set_wrs(self):
        self._wrs["Solo"] = (self._wins.get('Solo') / (self._wins.get('Solo') + self._losses.get('Solo'))) * 100
        self._wrs["Flex"] = (self._wins.get('Flex') / (self._wins.get('Flex') + self._losses.get('Flex'))) * 100

    def _set_match_history(self, num_of_matches):
        endpoint = f"/lol/match/v5/matches/by-puuid/{self._puuid}/ids?start=0&count={num_of_matches}"
        self._matches = self.utils.make_request_region(endpoint)

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

    def get_lps(self):
        return self._lps

    def get_wins(self):
        return self._wins

    def get_losses(self):
        return self._losses

    def get_solo_wr(self):
        return self._wrs
