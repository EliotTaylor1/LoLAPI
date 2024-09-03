import logging
from datetime import datetime
import sqlite3

from src.database import Database
from src.participant import Participant
from src.champion import Champion
from src.utils import Utils


class Match:
    logger = logging.getLogger(__name__)

    def __init__(self, match_id: str, account_puuid: str):
        self.utils = Utils()
        self.database = Database()

        self._account_puuid = account_puuid
        self._result_for_account = None
        self.match_id = match_id
        self._match_info = None
        self._match_date = None
        self._game_mode = None
        self._duration = None
        self._winning_team = None
        self._participants = []
        self._team_gold = {}
        self._banned_champions = []
        self._picked_champions = []

        self._load_match_summary()
        self.add_match_to_db()

    def __str__(self):
        return (f"{self._result_for_account}\n"
                f"Match ID: {self.match_id}\n"
                f"Match Date: {self._match_date}\n"
                f"Gamemode: {self.print_game_mode()}\n"
                f"Winning team: {self.print_winning_team()} in {self.print_duration()}\n"
                f"Players: {self.print_players()}\n"
                f"Picks: {', '.join(self._picked_champions)}\n"
                f"Bans: {', '.join(map(str, self._banned_champions))}")

    def _load_match_summary(self):
        self._match_info = self._retrieve_match_info()
        Match.logger.info("Setting match game mode")
        self._set_game_mode()
        Match.logger.info("Setting match duration")
        self._set_duration()
        Match.logger.info("Setting match date")
        self._set_date()
        Match.logger.info("Setting winning team")
        self._set_winning_team()
        Match.logger.info("Setting participants")
        self._set_participants()
        Match.logger.info("Setting banned champs")
        self._set_banned_champions()
        Match.logger.info("Setting picked champs")
        self._set_picked_champions()
        Match.logger.info("Setting team gold")
        self._set_team_gold()
        Match.logger.info("Setting if account won or not")
        self._set_result_for_account()
        Match.logger.info("Match info set")

    def add_match_to_db(self):
        try:
            with sqlite3.connect("Database.db"):
                if not self.match_id_already_in_db():
                    Match.logger.info("Adding new Match record")
                    match_tuple = self.set_match_tuple()
                    Match.logger.info(f"Match tuple data: {match_tuple}")
                    self.database.insert_match(match_tuple)
                else:
                    Match.logger.info("Match ID already in Matches table")
        except sqlite3.Error as e:
            print(e)

    def match_id_already_in_db(self) -> bool:
        Match.logger.info(f"Checking if Match ID already in table")
        try:
            with sqlite3.connect("Database.db") as conn:
                cur = conn.cursor()
                cur.execute(f"select * from matches where match_id=?", (self.match_id,))
                result = cur.fetchall()
                if result:
                    return True
                else:
                    return False
        except sqlite3.Error as e:
            print(e)

    def _retrieve_match_info(self):
        endpoint = f"/lol/match/v5/matches/{self.match_id}"
        return self.utils.make_request_region(endpoint)

    def set_match_tuple(self) -> tuple:
        return self.match_id, self._duration, self._match_date

    def _set_game_mode(self):
        info = self._match_info.get("info")
        self._game_mode = info.get("queueId")

    def _set_duration(self):
        info = self._match_info.get("info")
        self._duration = info.get("gameDuration")

    def _set_participants(self):
        info = self._match_info.get("info")
        participants = info.get("participants")
        metadata = self._match_info.get("metadata")
        match_id = metadata.get("matchId")
        for participant_data in participants:
            participant = Participant(participant_data, match_id, self._winning_team)
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
                champion_id = ban.get("championId")
                champion = Champion(champion_id)
                self._banned_champions.append(champion.get_name())

    def _set_winning_team(self):
        info = self._match_info.get("info")
        teams = info.get("teams")
        for team in teams:
            team_id = team.get("teamId")
            if team.get("win") and team_id == 100:
                self._winning_team = 100
                break
            else:
                self._winning_team = 200
                break

    def _set_result_for_account(self):
        account_team_id = None
        for participant in self._participants:
            if participant.get_puuid() == self._account_puuid:
                account_team_id = participant.get_team_id()
        if account_team_id == self.get_winning_team():
            self._result_for_account = "WIN"
        else:
            self._result_for_account = "LOSS"

    def _set_date(self):
        info = self._match_info.get("info")
        time = info.get("gameCreation") / 1000  # format posix date correctly
        self._match_date = datetime.fromtimestamp(time)

    def _set_team_gold(self):
        for participant in self._participants:
            team_id = participant.get_team_id()
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

    def get_game_mode(self):
        return self._game_mode

    def get_match_date(self):
        return self._match_date

    def get_match_info(self):
        return self._match_info

    def print_winning_team(self):
        if self._winning_team == 100:
            return "Blue"
        else:
            return "Red"

    def print_players(self):
        players = []
        for participant in self._participants:
            players.append(participant.get_full_name())
        return ', '.join(players)

    def print_duration(self):
        total_seconds = self._duration
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes}M {seconds}S"

    def print_game_mode(self):
        if self._game_mode == 420:
            return "Ranked Solo"
        elif self._game_mode == 430:
            return "Blind pick"
        elif self._game_mode == 440:
            return "Ranked Flex"
        elif self._game_mode == 450:
            return "ARAM"
        elif self._game_mode == 490:
            return "Quick play"
        elif self._game_mode == 700:
            return "Clash"
        elif self._game_mode == 720:
            return "ARAM Clash"
        elif self._game_mode == 870:
            return "Co-op vs AI - Intro"
        elif self._game_mode == 880:
            return "Co-op vs AI - Beginner"
        elif self._game_mode == 890:
            return "Co-op vs AI - Intermediate"
        elif self._game_mode == 1700:
            return "Arena"
        elif self._game_mode == 1710:
            return "Arena"

    def print_detailed_match_stats(self):
        name_width = 30
        team_width = 8
        champ_width = 15
        kda_width = 8
        role_width = 10
        gold_width = 10

        print(f"Match Date: {self._match_date}\n"
              f"Winning Team: {self.print_winning_team()} || Game Length: {self.print_duration()}\n"
              f"Blue Team Gold: {self.get_team_gold().get(100)}\n"
              f"Red Team Gold: {self.get_team_gold().get(200)}\n")
        print("=" * (name_width + team_width + champ_width + kda_width + role_width + gold_width + 15))

        sorted_participants = sorted(self._participants, key=lambda p: p.get_team_id())

        # Print header for participant stats
        print(f"{'Player':<{name_width}} | {'Team':<{team_width}} | {'Champion':<{champ_width}} | "
              f"{'KDA':<{kda_width}} | {'Role':<{role_width}} | {'Gold':<{gold_width}}")
        print("=" * (name_width + team_width + champ_width + kda_width + role_width + gold_width + 15))

        for participant in sorted_participants:
            #  'kda' string needed to fix formatting alignment issues... (an hour wasted)
            kda = f"{participant.get_kills()}/{participant.get_deaths()}/{participant.get_assists()}"
            print(f"{participant.get_full_name():<{name_width}} | "
                  f"{participant.get_team_colour():<{team_width}} | "
                  f"{participant.get_champion():<{champ_width}} | "
                  f"{kda:<{kda_width}} | "
                  f"{participant.get_role():<{role_width}} | "
                  f"{participant.get_gold():<{gold_width}}")
            print("-" * (name_width + team_width + champ_width + kda_width + role_width + gold_width + 15))
