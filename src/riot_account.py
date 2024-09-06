import sqlite3
from datetime import datetime
import logging

from src.utils import Utils
from src.match import Match
from src.champion import Champion
from src.database import Database


class RiotAccount:
    logger = logging.getLogger(__name__)

    def __init__(self, game_name: str, tagline: str):
        self.utils = Utils()
        self.database = Database()

        self._match_history_length = 0
        self._game_name = game_name
        self._tagline = tagline
        self._puuid = None
        self._account_id = None
        self._summoner_id = None
        self._date_of_last_activity = None
        self._date_of_last_match = None
        self._account_level = None
        self._overall_champion_mastery = None
        self._champion_mastery_levels = {}
        self._champion_mastery_points = {}
        self._tiers = {}
        self._ranks = {}
        self._league_points = {}
        self._wins = {}
        self._losses = {}
        self._winrates = {}
        self._match_history = []
        self._champion_mastery_tuples = []
        self._ranked_stats_tuples = []
        self._match_tuples = []

        self._load_account_info()

        self.add_account_to_db()
        self.add_masteries_to_db()
        self.add_ranks_to_db()

    def __str__(self):
        return (f"Name: {self._game_name}#{self._tagline}\n"
                f"PUUID: {self._puuid}\n"
                f"Summoner ID: {self._summoner_id}\n"
                f"Account ID: {self._account_id}\n"
                f"Level: {self._account_level}\n"
                f"Mastery Level: {self._overall_champion_mastery}\n"
                f"Last profile activity: {self._date_of_last_activity}\n"
                f"Last match: {self._date_of_last_match}\n"
                f"{self.print_ranked_performance()}")

    def _load_account_info(self):
        print(f"Getting info for {self._game_name}#{self._tagline}...")
        RiotAccount.logger.info("Setting PUUID")
        self._set_account_puuid()
        RiotAccount.logger.info("Setting Account Info")
        self._set_account_info()
        RiotAccount.logger.info("Setting Ranked Info")
        self._set_ranked_info()
        RiotAccount.logger.info("Setting Overall Mastery")
        self._set_overall_champion_mastery()
        RiotAccount.logger.info("Setting Mastery Levels")
        self._set_mastery_levels()
        RiotAccount.logger.info("Setting Date of last match")
        self._set_date_of_last_match()

    def _set_account_puuid(self):
        endpoint = f"/riot/account/v1/accounts/by-riot-id/{self._game_name}/{self._tagline}"
        account_info = self.utils.make_request_region(endpoint)
        self._puuid = account_info.get("puuid")

    def _set_account_info(self):
        endpoint = f"/lol/summoner/v4/summoners/by-puuid/{self._puuid}"
        account_info = self.utils.make_request_server(endpoint)
        RiotAccount.logger.info("Setting Summoner level")
        self._account_level = account_info.get("summonerLevel")
        RiotAccount.logger.info("Setting Account ID")
        self._account_id = account_info.get("accountId")
        RiotAccount.logger.info("Setting Summoner ID")
        self._summoner_id = account_info.get("id")
        RiotAccount.logger.info("Setting Last revision date")
        revision_date = account_info.get("revisionDate") / 1000  # format posix date correctly
        self._date_of_last_activity = datetime.fromtimestamp(revision_date)

    def _set_ranked_info(self):
        endpoint = f"/lol/league/v4/entries/by-summoner/{self._summoner_id}"
        account_info = self.utils.make_request_server(endpoint)
        for queue in account_info:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                self._tiers["Solo"] = queue["tier"]
                self._ranks["Solo"] = queue["rank"]
                self._league_points["Solo"] = queue["leaguePoints"]
                self._wins["Solo"] = queue["wins"]
                self._losses["Solo"] = queue["losses"]
                solo_tuple = (self._puuid, queue["queueType"], self._tiers.get("Solo"), self._ranks.get("Solo"),
                              self._league_points.get("Solo"), self._wins.get("Solo"), self._losses.get("Solo"),
                              datetime.now())
                self._ranked_stats_tuples.append(solo_tuple)
            elif queue["queueType"] == "RANKED_FLEX_SR":
                self._tiers["Flex"] = queue["tier"]
                self._ranks["Flex"] = queue["rank"]
                self._league_points["Flex"] = queue["leaguePoints"]
                self._wins["Flex"] = queue["wins"]
                self._losses["Flex"] = queue["losses"]
                flex_tuple = (self._puuid, queue["queueType"], self._tiers.get("Flex"), self._ranks.get("Flex"),
                              self._league_points.get("Flex"), self._wins.get("Flex"), self._losses.get("Flex"),
                              datetime.now())
                self._ranked_stats_tuples.append(flex_tuple)
            elif queue["queueType"] == "CHERRY":
                self._league_points["Arena"] = queue["leaguePoints"]
                self._wins["Arena"] = queue["wins"]
                self._losses["Arena"] = queue["losses"]
        # check if the account has played a game of this queue type before we calculate the winrate.
        # then check if they have won a game in that queue type to avoid divide by 0.
        # if they haven't won a game just set winrate to 0.
        if "Solo" in self._wins and self._wins["Solo"] > 0:
            self._winrates["Solo"] = (self._wins.get('Solo') / (
                    self._wins.get('Solo') + self._losses.get('Solo'))) * 100
        else:
            self._winrates["Solo"] = 0
        if "Flex" in self._wins and self._wins["Flex"] > 0:
            self._winrates["Flex"] = (self._wins.get('Flex') / (
                    self._wins.get('Flex') + self._losses.get('Flex'))) * 100
        else:
            self._winrates["Flex"] = 0
        if "Arena" in self._wins and self._wins["Arena"] > 0:
            self._winrates["Arena"] = (self._wins.get('Arena') / (
                    self._wins.get('Arena') + self._losses.get('Arena'))) * 100
        else:
            self._winrates["Arena"] = 0

    def reset_match_history(self):
        self._match_history_length = 0
        self._match_history.clear()

    def set_match_history_length(self):
        if self._match_history_length > 0:
            print("Match history length already set")
            return
        num_of_games_valid = False
        while not num_of_games_valid:
            num_of_games_input = input("Enter number of games to get data for (1 - 100): ")
            num_of_games = int(num_of_games_input)
            if num_of_games < 1 or num_of_games > 100:
                print("Number of games must be between 1 - 100")
            else:
                self._match_history_length = num_of_games
                num_of_games_valid = True

    def _set_overall_champion_mastery(self):
        endpoint = f"/lol/champion-mastery/v4/scores/by-puuid/{self._puuid}"
        mastery = self.utils.make_request_server(endpoint)
        self._overall_champion_mastery = mastery

    def _set_mastery_levels(self):
        endpoint = f"/lol/champion-mastery/v4/champion-masteries/by-puuid/{self._puuid}/top?count=10"
        mastery_info = self.utils.make_request_server(endpoint)
        for entry in mastery_info:
            champion_id = entry["championId"]
            champion_name = Champion(champion_id)
            self._champion_mastery_levels[champion_name.get_name()] = entry["championLevel"]
            self._champion_mastery_points[champion_name.get_name()] = entry["championPoints"]
            champion_mastery_tuple = (
                self._puuid, champion_id, champion_name.get_name(), entry["championLevel"], entry["championPoints"],
                datetime.now())
            self._champion_mastery_tuples.append(champion_mastery_tuple)

    def retrieve_match_history(self, num_of_matches):
        print("Retrieving match history...")
        endpoint = f"/lol/match/v5/matches/by-puuid/{self._puuid}/ids?start=0&count={num_of_matches}"
        match_ids = self.utils.make_request_region(endpoint)
        existing_match_ids = {match.match_id for match in self._match_history}
        for match_id in match_ids:
            if match_id not in existing_match_ids:
                match = Match(match_id, self._puuid)
                self._match_history.append(match)

    def _set_date_of_last_match(self):
        endpoint = f"/lol/match/v5/matches/by-puuid/{self._puuid}/ids?start=0&count=1"
        match_ids = self.utils.make_request_region(endpoint)
        if not match_ids:
            raise Exception("No recent matches found")
        match_id = match_ids[0]
        match_info_endpoint = f"/lol/match/v5/matches/{match_id}"
        match_info = self.utils.make_request_region(match_info_endpoint)
        info = match_info.get("info")
        last_match = info.get("gameCreation") / 1000  # format POSIX date correctly
        self._date_of_last_match = datetime.fromtimestamp(last_match)

    def get_account_as_tuple(self) -> tuple:
        account = (self._puuid,
                   self._summoner_id,
                   self._account_id,
                   self._game_name,
                   self._tagline,
                   self._account_level,
                   self._date_of_last_activity,
                   self._date_of_last_match,
                   datetime.now())
        return account

    def add_account_to_db(self):
        try:
            with sqlite3.connect("Database.db"):
                if not self.puuid_already_in_db("accounts"):
                    RiotAccount.logger.info("Adding new account record")
                    account = self.get_account_as_tuple()
                    self.database.insert_account(account)
                else:
                    RiotAccount.logger.info("PUUID already in Accounts table, refreshing account record")
                    self.refresh_accounts_record()
        except sqlite3.Error as e:
            print(e)

    def add_masteries_to_db(self):
        try:
            with sqlite3.connect("Database.db"):
                if not self.puuid_already_in_db("masteries"):
                    RiotAccount.logger.info("Adding new mastery records")
                    RiotAccount.logger.info(f"Mastery tuple data: {self._champion_mastery_tuples}")
                    self.database.insert_masteries(self._champion_mastery_tuples)
                else:
                    RiotAccount.logger.info("PUUID already in Masteries table, refreshing mastery records")
                    self.refresh_masteries_record()
        except sqlite3.Error as e:
            print(e)

    def add_ranks_to_db(self):
        try:
            with sqlite3.connect("Database.db"):
                if not self.puuid_already_in_db("ranks"):
                    RiotAccount.logger.info("Adding new rank records")
                    RiotAccount.logger.info(f"Ranked tuple data: {self._ranked_stats_tuples}")
                    self.database.insert_ranks(self._ranked_stats_tuples)
                else:
                    RiotAccount.logger.info("PUUID already in Ranks table, refreshing ranked records")
                    self.refresh_ranked_record()
        except sqlite3.Error as e:
            print(e)

    def puuid_already_in_db(self, table: str) -> bool:
        RiotAccount.logger.info(f"Checking if puuid already in {table}")
        try:
            with sqlite3.connect("Database.db") as conn:
                cur = conn.cursor()
                cur.execute(f"select * from {table} where puuid=?", (self._puuid,))
                result = cur.fetchall()
                if result:
                    return True
                else:
                    return False
        except sqlite3.Error as e:
            print(e)

    def refresh_accounts_record(self):
        RiotAccount.logger.info("Refreshing account record")
        try:
            with sqlite3.connect("Database.db") as conn:
                cur = conn.cursor()
                sql = ("UPDATE accounts "
                       "SET game_name=?,"
                       "tag=?,"
                       "level=?,"
                       "last_activity=?,"
                       "last_match=?,"
                       "last_refresh=?"
                       "WHERE puuid=?")
                cur.execute(sql, (self._game_name, self._tagline, self._account_level, self._date_of_last_activity,
                                  self._date_of_last_activity, datetime.now(), self._puuid))
                conn.commit()
        except sqlite3.Error as e:
            print(e)

    def refresh_masteries_record(self):
        RiotAccount.logger.info("Refreshing mastery records")
        try:
            with sqlite3.connect("Database.db") as conn:
                cur = conn.cursor()
                sql = ("UPDATE masteries "
                       "SET level=?,"
                       "points=?,"
                       "last_refresh=?"
                       "WHERE puuid=?")
                for mastery_tuple in self._champion_mastery_tuples:
                    cur.execute(sql, (mastery_tuple[2], mastery_tuple[3], datetime.now(), self._puuid))
                conn.commit()
        except sqlite3.Error as e:
            print(e)

    def refresh_ranked_record(self):
        RiotAccount.logger.info("Refreshing ranked records")
        try:
            with sqlite3.connect("Database.db") as conn:
                cur = conn.cursor()
                sql = ("UPDATE ranks "
                       "SET queue_name=?,"
                       "tier=?,"
                       "rank=?,"
                       "league_points=?,"
                       "wins=?,"
                       "losses=?,"
                       "last_refresh=?"
                       "WHERE puuid=?")
                for rank_tuple in self._ranked_stats_tuples:
                    cur.execute(sql, (
                        rank_tuple[1], rank_tuple[2], rank_tuple[3], rank_tuple[4], rank_tuple[5], rank_tuple[6],
                        datetime.now(), self._puuid))
                conn.commit()
        except sqlite3.Error as e:
            print(e)

    def get_account_puuid(self):
        return self._puuid

    def get_account_level(self):
        return self._account_level

    def get_account_id(self):
        return self._account_id

    def get_summoner_id(self):
        return self._summoner_id

    def get_overall_mastery_level(self):
        return self._overall_champion_mastery

    def get_champion_mastery_levels(self):
        return self._champion_mastery_levels

    def get_champion_mastery_points(self):
        return self._champion_mastery_points

    def get_tiers(self):
        return self._tiers

    def get_ranks(self):
        return self._ranks

    def get_league_points(self):
        return self._league_points

    def get_wins(self):
        return self._wins

    def get_losses(self):
        return self._losses

    def get_winrates(self):
        return self._winrates

    def get_match_history(self):
        return self._match_history

    def get_match_history_length(self):
        return self._match_history_length

    def print_champion_mastery(self):
        print("====== Top 10 Champion Mastery ======")
        # Set the width of the columns
        index_width = 2
        champion_width = max(len(name) for name in self._champion_mastery_levels) + 3
        level_width = 3
        i = 0
        for champion_name in self._champion_mastery_levels:
            i += 1
            mastery_level = self._champion_mastery_levels[champion_name]
            mastery_points = self._champion_mastery_points[champion_name]
            print(
                f"{i:<{index_width}} {champion_name:<{champion_width}} || Mastery Level: {mastery_level:<{level_width}} || Mastery Points: {mastery_points}")

    def print_ranked_performance(self):
        message = ""
        if "Solo" in self._wins:
            message += f"Solo Q - Rank: {self._tiers.get('Solo')} {self._ranks.get('Solo')} {self._league_points.get('Solo')}LP || W/L: {self._wins.get('Solo')}W/{self._losses.get('Solo')}L - {self._winrates.get('Solo'):.2f}%\n"
        if "Flex" in self._wins:
            message += f"Flex Q - Rank: {self._tiers.get('Flex')} {self._ranks.get('Flex')} {self._league_points.get('Flex')}LP || W/L: {self._wins.get('Flex')}W/{self._losses.get('Flex')}L - {self._winrates.get('Flex'):.2f}%\n"
        if "Arena" in self._wins:
            message += f"Arena - W/L: {self._wins.get('Arena')}W/{self._losses.get('Arena')}L - {self._winrates.get('Arena'):.2f}%"
        return message

    def print_match_history(self):
        i = 1
        for match in self._match_history:
            print(f"====== Match {i}. ======")
            print(f"{match}")
            print("=========================\n")
            i += 1
