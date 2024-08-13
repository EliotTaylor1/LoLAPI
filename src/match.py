from RiotAPI import RiotAPI


class Match(RiotAPI):
    def __init__(self, match_id, api_key=None):
        super().__init__(api_key)
        self.match_id = match_id
        self.gamemode = None
        self.uuids = []
        self.game_names = []
        self.bans = []
        self.picks = []
        self.duration = None
        self.get_match_details()

    def __str__(self):
        return f"ID: {self.match_id}, Duration: {self.duration}, Gamemode: {self.gamemode}, Players: {self.uuids}"

    def get_match_details(self):
        endpoint = f"/lol/match/v5/matches/{self.match_id}"
        match_info = self.make_request(endpoint)
        info = match_info.get("info", {})
        self.gamemode = info.get("gameMode")
        self.duration = info.get("gameDuration")
        self.uuids = [participant["puuid"] for participant in info.get("participants", [])]
