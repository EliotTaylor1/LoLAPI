from Utils import Utils


class Match:
    def __init__(self, match_id):
        self.utils = Utils()
        self.match_id = match_id
        self.gamemode = None
        self.puuids = []
        self.game_names = []
        self.bans = []
        self.picks = []
        self.duration = None
        self.get_match_details()

    def __str__(self):
        return f"ID: {self.match_id}, Duration: {self.duration}, Gamemode: {self.gamemode}, Players: {self.game_names}"

    def get_match_details(self):
        endpoint = f"/lol/match/v5/matches/{self.match_id}"
        match_info = self.utils.make_request(endpoint)
        info = match_info.get("info", {})
        self.gamemode = info.get("gameMode")
        self.duration = info.get("gameDuration")
        self.puuids = [participant["puuid"] for participant in info.get("participants", [])]
        for puuid in self.puuids:
            name = self.utils.convert_puuid_to_game_name(puuid)
            self.game_names.append(name)

