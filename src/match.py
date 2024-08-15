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
                f"Players: {', '.join(self._participant_names)}\n"
                f"Picks: {', '.join(self._picked_champions)}\n"
                f"Bans: {', '.join(map(str, self._banned_champions))}")

    def _load_match_details(self):
        match_info = self._retrieve_match_info()
        self._set_match_info(match_info)
        self._set_participant_puuids(match_info)
        self._set_participant_names(match_info)
        self._set_banned_champions(match_info)
        self._set_picked_champions(match_info)

    def _retrieve_match_info(self):
        endpoint = f"/lol/match/v5/matches/{self._match_id}"
        return self.utils.make_request_region(endpoint)

    def _set_match_info(self, match_info):
        info = match_info.get("info", {})
        self._gamemode = info.get("gameMode")
        self._duration = info.get("gameDuration")

    def _set_participant_puuids(self, match_info):
        info = match_info.get("metadata", {})
        self._participant_puuids = info.get("participants")

    def _set_participant_names(self, match_info):
        info = match_info.get("info", {})
        participants = info.get("participants", [])
        for participant in participants:
            name = participant.get("riotIdGameName")
            tag = participant.get("riotIdTagline")
            final = f"{name}#{tag}"
            self._participant_names.append(final)

    def _set_picked_champions(self, match_info):
        info = match_info.get("info", {})
        participants = info.get("participants", [])
        for participant in participants:
            pick = participant.get("championName")
            self._picked_champions.append(pick)

    def _set_banned_champions(self, match_info):
        info = match_info.get("info", {})
        teams = info.get("teams", [])
        for team in teams:
            bans = team.get("bans")
            for ban in bans:
                self._banned_champions.append(ban.get("championId"))
