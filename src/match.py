from participant import Participant
from utils import Utils


class Match:
    def __init__(self, match_id):
        self.utils = Utils()
        self._match_id = match_id
        self._match_info = None
        self._gamemode = None
        self._duration = None
        self._winning_team = None
        self._participants = []
        self._team_gold = {}
        self._banned_champions = []
        self._picked_champions = []
        self._load_match_summary()

    def __str__(self):
        return (f"Match ID: {self._match_id}\n"
                f"Winning team: {self.get_winning_team()} | "
                f"Duration: {self.print_duration()}\n"
                f"Gamemode: {self._gamemode}\n"
                f"Players: {self.print_players()}\n"
                f"Picks: {', '.join(self._picked_champions)}\n"
                f"Bans: {', '.join(map(str, self._banned_champions))}")

    def _load_match_summary(self):
        self._match_info = self._retrieve_match_info()
        print("Setting match info")
        self._set_match_info()
        print("Setting participants")
        self._set_participants()
        print("Setting banned champs")
        self._set_banned_champions()
        print("Setting picked champs")
        self._set_picked_champions()
        print("Setting winning team")
        self._set_winning_team()
        print("Setting team gold")
        self._set_team_gold()
        print("Match info set")

    def _retrieve_match_info(self):
        endpoint = f"/lol/match/v5/matches/{self._match_id}"
        return self.utils.make_request_region(endpoint)

    def _set_match_info(self):
        info = self._match_info.get("info")
        self._gamemode = info.get("gameMode")
        self._duration = info.get("gameDuration")

    def _set_participants(self):
        info = self._match_info.get("info")
        participants = info.get("participants")
        for participant_data in participants:
            participant = Participant(participant_data)
            self._participants.append(participant)

    def _set_picked_champions(self):
        info = self._match_info.get("info")
        participants = info.get("participants")
        for participant in participants:
            pick = participant.get("championName")
            self._picked_champions.append(pick)

    def _set_banned_champions(self):
        info = self._match_info.get("info")
        teams = info.get("teams")
        for team in teams:
            bans = team.get("bans")
            for ban in bans:
                self._banned_champions.append(ban.get("championId"))

    def _set_winning_team(self):
        info = self._match_info.get("info")
        teams = info.get("teams")
        for team in teams:
            team_id = team.get("teamId")
            if team.get("win") and team_id == 100:
                self._winning_team = "Blue"
                break
            else:
                self._winning_team = "Red"
                break

    def _set_team_gold(self):
        for participant in self._participants:
            team_id = participant.get_teamId()
            player_gold = participant.get_gold()
            if team_id in self._team_gold:
                self._team_gold[team_id] += player_gold
            else:
                self._team_gold[team_id] = player_gold

    def get_team_gold(self):
        return self._team_gold

    def get_winning_team(self):
        return self._winning_team

    def get_duration(self):
        return self._duration

    def get_match_info(self):
        return self._match_info

    def print_players(self):
        players = []
        for participant in self._participants:
            players.append(participant.get_full_name())
        return ', '.join(players)

    def print_duration(self):
        total_seconds = self._duration
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes}M {seconds}S"

    def print_detailed_match_stats(self):
        print(f"Winning team: {self.get_winning_team()} | "
              f"Game length: {self.print_duration()}\n"
              f"Blue team gold: {self.get_team_gold().get(100)}\n"
              f"Red team gold: {self.get_team_gold().get(200)}\n"
              f"================")
        sorted_participants = sorted(self._participants, key=lambda p: p.get_teamId())
        for participant in sorted_participants:
            print(f"Player: {participant.get_full_name()}\n"
                  f"Team: {participant.get_team_colour()}\n"
                  f"Champion: {participant.get_champion()} - "
                  f"KDA: {participant.get_kills()}/{participant.get_deaths()}/{participant.get_assists()}\n"
                  f"Role: {participant.get_role()}\n"
                  f"Gold: {participant.get_gold()}")
            print("================")
