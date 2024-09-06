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
                      match_id TEXT PRIMARY KEY,
                      game_mode INTEGER,
                      duration INTEGER,
                      match_date TEXT
            );""",
            """ CREATE TABLE IF NOT EXISTS participants (
                      match_id TEXT,
                      puuid TEXT,
                      win INTEGER, 
                      gold INTEGER,
                      kills INTEGER,
                      deaths INTEGER ,
                      assists INTEGER,
                      picked_champion TEXT,
                      FOREIGN KEY (match_id)
                        REFERENCES matches (match_id)
            );""",
            """ CREATE TABLE IF NOT EXISTS ranks (
                      puuid TEXT,
                      queue_name TEXT,
                      tier TEXT,
                      rank INTEGER,
                      league_points INTEGER,
                      wins INTEGER,
                      losses INTEGER,
                      last_refresh TEXT,
                      FOREIGN KEY (puuid)   
                        REFERENCES accounts (puuid)
            );""",
            """ CREATE TABLE IF NOT EXISTS masteries (
                      puuid TEXT,
                      champion_id INTEGER,
                      champion_name TEXT,
                      level INTEGER,
                      points INTEGER,
                      last_refresh TEXT,
                      FOREIGN KEY (puuid)
                        REFERENCES accounts (puuid)
            );"""]
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                for statement in sql_statement:
                    cursor.execute(statement)
                conn.commit()
        except sqlite3.Error as e:
            print(e)

    def insert_account(self, account_data: tuple):
        sql = """ INSERT INTO accounts(puuid,summoner_id,account_id,game_name,tag,level,last_activity,last_match,last_refresh)
        VALUES(?,?,?,?,?,?,?,?,?)"""
        cur = self.conn.cursor()
        cur.execute(sql, account_data)
        self.conn.commit()
        return cur.lastrowid

    def insert_masteries(self, mastery_data: list):
        sql = """ INSERT INTO masteries(puuid,champion_id,champion_name,level,points,last_refresh)
        VALUES(?,?,?,?,?,?)"""
        cur = self.conn.cursor()
        cur.executemany(sql, mastery_data)
        self.conn.commit()
        return cur.lastrowid

    def insert_ranks(self, ranked_data: list):
        sql = """ INSERT INTO ranks(puuid,queue_name,tier,rank,league_points,wins,losses,last_refresh)
        VALUES(?,?,?,?,?,?,?,?)"""
        cur = self.conn.cursor()
        cur.executemany(sql, ranked_data)
        self.conn.commit()
        return cur.lastrowid

    def insert_match(self, match_data: tuple):
        sql = """ INSERT INTO matches(match_id,game_mode,duration,match_date)
        VALUES(?,?,?,?)"""
        cur = self.conn.cursor()
        cur.execute(sql, match_data)
        self.conn.commit()
        return cur.lastrowid

    def insert_participant(self, participant_data: tuple):
        sql = """ INSERT INTO participants(match_id,puuid,win,gold,kills,deaths,assists,picked_champion)
        VALUES(?,?,?,?,?,?,?,?)"""
        cur = self.conn.cursor()
        cur.execute(sql, participant_data)
        self.conn.commit()
        return cur.lastrowid
