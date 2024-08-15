from utils import Utils


class Match:
    def __init__(self, match_id):
        self.utils = Utils()
        self._match_id = match_id
        self._gamemode = None
        self._duration = None
        self._participant_puuids = []
        self._participant_names = []
        self._banned_champions = []
        self._picked_champions = []
        self._load_match_details()

    def __str__(self):
        return (f"Match ID: {self._match_id}\n"
                f"Duration: {self._duration}\n"
                f"Gamemode: {self._gamemode}\n"
                f"Players: {self._participant_names}\n"
                f"Picks: {self._picked_champions}\n"
                f"Bans: {self._banned_champions}")

    def _load_match_details(self):
        self._set_gamemode()
        self._set_duration()
        self._set_participant_puuids()
        self._set_participant_names()
        self._set_banned_champions()
        self._set_picked_champions()

    def _set_gamemode(self):
        endpoint = f"/lol/match/v5/matches/{self._match_id}"
        match_info = self.utils.make_request_region(endpoint)
        info = match_info.get("info", {})
        self._gamemode = info.get("gameMode")

    def _set_duration(self):
        endpoint = f"/lol/match/v5/matches/{self._match_id}"
        match_info = self.utils.make_request_region(endpoint)
        info = match_info.get("info", {})
        self._duration = info.get("gameDuration")

    def _set_participant_puuids(self):
        endpoint = f"/lol/match/v5/matches/{self._match_id}"
        match_info = self.utils.make_request_region(endpoint)
        info = match_info.get("metadata", {})
        self._participant_puuids = info.get("participants")

    def _set_participant_names(self):
        for participant in self._participant_puuids:
            game_name = self.utils.convert_puuid_to_game_name(participant)
            self._participant_names.append(game_name)

    def _set_picked_champions(self):
        endpoint = f"/lol/match/v5/matches/{self._match_id}"
        match_info = self.utils.make_request_region(endpoint)
        info = match_info.get("info", {})
        participants = info.get("participants", [])
        for participant in participants:
            pick = participant.get("championName")
            self._picked_champions.append(pick)

    def _set_banned_champions(self):
        endpoint = f"/lol/match/v5/matches/{self._match_id}"
        match_info = self.utils.make_request_region(endpoint)
        info = match_info.get("info", {})
        teams = info.get("teams", [])
        for team in teams:
            bans = team.get("bans")
            for ban in bans:
                self._banned_champions.append(ban.get("championId"))


