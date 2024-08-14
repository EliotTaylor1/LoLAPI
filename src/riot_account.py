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
        self._solo_tier = None
        self._solo_rank = None
        self._solo_lp = None
        self._solo_wins = None
        self._solo_losses = None
        self._solo_wr = 0.00
        self.load_account_info()
        self._matches = []

    def __str__(self):
        return (f"Name: {self._game_name}#{self._tagline}\n"
                f"PUUID: {self._puuid}\n"
                f"Summoner ID: {self._summoner_id}\n"
                f"Account ID: {self._account_id}\n"
                f"Level: {self._account_level}\n"
                f"Solo Q Rank: {self._solo_tier} {self._solo_rank} {self._solo_lp}LP\n"
                f"Solo Q W/L: {self._solo_wins}/{self._solo_losses} - {self._solo_wr:.2f}%\n")

    def load_account_info(self):
        self._set_account_puuid()
        self._set_account_level()
        self._set_account_id()
        self._set_summoner_id()
        self._set_solo_tier()
        self._set_solo_rank()
        self._set_solo_lp()
        self._set_solo_wins()
        self._set_solo_losses()
        self._set_solo_wr()

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

    def _set_solo_tier(self):
        endpoint = f"/lol/league/v4/entries/by-summoner/{self._summoner_id}"
        account_info = self.utils.make_request_server(endpoint)
        for queue in account_info:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                self._solo_tier = queue["tier"]
                break

    def _set_solo_rank(self):
        endpoint = f"/lol/league/v4/entries/by-summoner/{self._summoner_id}"
        account_info = self.utils.make_request_server(endpoint)
        for queue in account_info:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                self._solo_rank = queue["rank"]
                break

    def _set_solo_lp(self):
        endpoint = f"/lol/league/v4/entries/by-summoner/{self._summoner_id}"
        account_info = self.utils.make_request_server(endpoint)
        for queue in account_info:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                self._solo_lp = queue["leaguePoints"]
                break

    def _set_solo_wins(self):
        endpoint = f"/lol/league/v4/entries/by-summoner/{self._summoner_id}"
        account_info = self.utils.make_request_server(endpoint)
        for queue in account_info:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                self._solo_wins = queue["wins"]
                break

    def _set_solo_losses(self):
        endpoint = f"/lol/league/v4/entries/by-summoner/{self._summoner_id}"
        account_info = self.utils.make_request_server(endpoint)
        for queue in account_info:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                self._solo_losses = queue["losses"]
                break

    def _set_solo_wr(self):
        self._solo_wr = (self._solo_wins / (self._solo_wins + self._solo_losses)) * 100

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

    def get_solo_tier(self):
        return self._solo_tier

    def get_solo_rank(self):
        return self._solo_rank

    def get_solo_lp(self):
        return self._solo_lp

    def get_solo_wins(self):
        return self._solo_wins

    def get_solo_losses(self):
        return self._solo_losses

    def get_solo_wr(self):
        return self._solo_wr
