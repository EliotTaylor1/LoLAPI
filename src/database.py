import sqlite3


class Database:
    def __init__(self):
        self.db_name = "Database.db"
        self.conn = None

        try:
            self.conn = sqlite3.connect(self.db_name)
            print(sqlite3.sqlite_version)
        except sqlite3.Error as e:
            print(e)
        # finally:
        #     if self.conn:
        #         self.conn.close()

    def close_connection(self):
        if self.conn:
            self.conn.close()

    def create_tables(self):
        sql_statement = [
            """CREATE TABLE IF NOT EXISTS accounts (
                      puuid TEXT PRIMARY KEY,
                      summoner_id TEXT,
                      account_id TEXT,
                      game_name TEXT,
                      tag TEXT,
                      level INTEGER,
                      last_activity TEXT,
                      last_match TEXT,
                      last_refresh TEXT
            );""",
            """ CREATE TABLE IF NOT EXISTS matches (
                      match_id INTEGER PRIMARY KEY,
                      puuid TEXT,
                      queue_id INTEGER,
                      duration REAL,
                      winning_team INTEGER,
                      gold INTEGER,
                      kills INTEGER,
                      deaths INTEGER,
                      assists INTEGER,
                      picked_champion INTEGER,
                      banned_champion INTEGER,
                      match_date TEXT
            );""",
            """ CREATE TABLE IF NOT EXISTS ranks (
                      puuid TEXT PRIMARY KEY,
                      queue_type INTEGER,
                      tier TEXT,
                      rank INTEGER,
                      league_points INTEGER,
                      wins INTEGER,
                      losses INTEGER,
                      last_refresh TEXT
            );""",
            """ CREATE TABLE IF NOT EXISTS masteries (
                      puuid TEXT PRIMARY KEY,
                      champion_id INTEGER,
                      level INTEGER,
                      points INTEGER,
                      last_refresh TEXT
            );"""]
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                for statement in sql_statement:
                    cursor.execute(statement)
                conn.commit()
        except sqlite3.Error as e:
            print(e)

    def insert_account(self, account_data: list):
        sql = """ INSERT INTO accounts(puuid,summoner_id,account_id,game_name,tag,level,last_activity,last_match,last_refresh)
        VALUES(?,?,?,?,?,?,?,?,?)"""
        cur = self.conn.cursor()
        cur.execute(sql, account_data)
        self.conn.commit()
        return cur.lastrowid
