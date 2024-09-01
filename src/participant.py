from src.database import Database

import sqlite3
import logging


class Participant:
    logger = logging.getLogger(__name__)

    def __init__(self, participant_data: dict, match_id: str, winning_team: int):
        self.database = Database()

        self._match_id = match_id
        self._winning_team = winning_team
        self._game_name = participant_data.get("riotIdGameName")
        self._tagline = participant_data.get("riotIdTagline")
        self._puuid = participant_data.get("puuid")
        self._team_id = participant_data.get("teamId")
        self._won_game = self._set_won_game()
        self._team_colour = None
        self._champion = participant_data.get("championName")
        self._kills = participant_data.get("kills")
        self._deaths = participant_data.get("deaths")
        self._assists = participant_data.get("assists")
        self._gold = participant_data.get("goldEarned")
        self._role = participant_data.get("teamPosition")

        self._set_team_colour()
        self.add_participant_to_db()

    def __str__(self):
        return (f"{self._game_name}#{self._tagline} | Champion: {self._champion} | "
                f"KDA: {self._kills}/{self._deaths}/{self._assists} | Gold: {self._gold}")

    def _set_team_colour(self):
        if self._team_id == 100:
            self._team_colour = "Blue"
        else:
            self._team_colour = "Red"

    def add_participant_to_db(self):
        Participant.logger.info("Adding new participant record")
        try:
            with sqlite3.connect("Database.db"):
                if not self.match_id_and_participant_already_in_db():
                    participant = self.get_participant_as_tuple()
                    self.database.insert_participant(participant)
                else:
                    Participant.logger.info("Participant already in table for this match")
        except sqlite3.Error as e:
            print(e)

    def get_participant_as_tuple(self) -> tuple:
        participant = (
            self._match_id, self._puuid, self._won_game, self._gold, self._kills, self._deaths, self._assists, self._champion)
        return participant

    def match_id_and_participant_already_in_db(self) -> bool:
        Participant.logger.info(f"Checking if participant already in match")
        try:
            with sqlite3.connect("Database.db") as conn:
                cur = conn.cursor()
                cur.execute(f"select * from participants")
                rows = cur.fetchall()
                for row in rows:
                    if row[0] == self._match_id and row[1] == self._puuid:
                        return True
                    else:
                        return False
        except sqlite3.Error as e:
            print(e)

    def _set_won_game(self) -> bool:
        if self._team_id == self._winning_team:
            return True
        else:
            return False

    def get_name(self):
        return self._game_name

    def get_tagline(self):
        return self._tagline

    def get_full_name(self):
        return f"{self._game_name}#{self._tagline}"

    def get_puuid(self):
        return self._puuid

    def get_team_id(self):
        return self._team_id

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
