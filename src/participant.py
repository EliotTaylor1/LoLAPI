class Participant:
    def __init__(self, participant_data):
        self._game_name = participant_data.get("riotIdGameName")
        self._tagline = participant_data.get("riotIdTagline")
        self._puuid = participant_data.get("puuid")
        self._teamId = participant_data.get("teamId")
        self._team_colour = None
        self._champion = participant_data.get("championName")
        self._kills = participant_data.get("kills")
        self._deaths = participant_data.get("deaths")
        self._assists = participant_data.get("assists")
        self._gold = participant_data.get("goldEarned")
        self._role = participant_data.get("teamPosition")
        self._set_team_colour()

    def __str__(self):
        return (f"{self._game_name}#{self._tagline} | Champion: {self._champion} | "
                f"KDA: {self._kills}/{self._deaths}/{self._assists} | Gold: {self._gold}")

    def _set_team_colour(self):
        if self._teamId == 100:
            self._team_colour = "Blue"
        else:
            self._team_colour = "Red"

    def get_name(self):
        return self._game_name

    def get_tagline(self):
        return self._tagline

    def get_full_name(self):
        return f"{self._game_name}#{self._tagline}"

    def get_puuid(self):
        return self._puuid

    def get_teamId(self):
        return self._teamId

    def get_team_colour(self):
        return self._team_colour

    def get_champion(self):
        return self._champion

    def get_kills(self):
        return self._kills

    def get_deaths(self):
        return self._deaths

    def get_assists(self):
        return self._assists

    def get_gold(self):
        return self._gold

    def get_role(self):
        return self._role.title()
