from utils import Utils


class Match:
    def __init__(self, match_id):
        self.utils = Utils()
        self.match_id = match_id
        self.gamemode = None
        self.duration = None
        self.puuids = []
        self.game_names = []
        self.bans = []
        self.picks = []
        self.set_match_details()  # populate match details
        self.get_bans()

    def __str__(self):
        return f"Match ID: {self.match_id}\n Duration: {self.duration}\n Gamemode: {self.gamemode}\n Players: {self.game_names} \n Picks: {self.picks}"

    def set_match_details(self):
        endpoint = f"/lol/match/v5/matches/{self.match_id}"
        match_info = self.utils.make_request(endpoint)
        info = match_info.get("info", {})
        self.gamemode = info.get("gameMode")
        self.duration = info.get("gameDuration")
        self.puuids = [participant["puuid"] for participant in info.get("participants", [])]
        for puuid in self.puuids:
            name = self.utils.convert_puuid_to_game_name(puuid)
            self.game_names.append(name)
        self.picks = [participant["championName"] for participant in info.get("participants")]

    def get_bans(self):
        endpoint = f"/lol/match/v5/matches/{self.match_id}"
        match_info = self.utils.make_request(endpoint)
        info = match_info.get("info", {})
        team = info.get("teams", {})
        self.bans = [ban["championId"] for ban in team.get("bans")]

