from RiotAPI import RiotAPI


class RiotAccount(RiotAPI):

    def __init__(self, game_name, tagline, api_key=None):
        super().__init__(api_key)
        self.game_name = game_name
        self.tagline = tagline
        self.puuid = None
        self.load_account_info()
        self.matches = []

    def __str__(self):
        return f"Name: {self.game_name}#{self.tagline} ID: {self.puuid}"

    def load_account_info(self):
        endpoint = f"/riot/account/v1/accounts/by-riot-id/{self.game_name}/{self.tagline}"
        account_info = self.make_request(endpoint)
        self.puuid = account_info.get("puuid")

    def get_match_history(self, num_of_matches):
        endpoint = f"/lol/match/v5/matches/by-puuid/{self.puuid}/ids?start=0&count={num_of_matches}"
        self.matches = self.make_request(endpoint)

