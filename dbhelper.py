import sqlite3
from pathlib import Path
import sqlparse

ROOT_DIR = Path(__file__).parent
DB_PATH = ROOT_DIR / 'database.sqlite3'

def create_tables():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS ranks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT,
                    required_exp INTEGER,
                    new_slots INTEGER,
                    new_atts INTEGER
                );
               """)

    cursor.execute(f"""
               CREATE TABLE IF NOT EXISTS player (
                   discordid BIGINT PRIMARY KEY,
                   charname TEXT,
                   xp INTEGER,
                   rank_id INTEGER,
                   gold INTEGER,
                   FOREIGN KEY (rank_id) REFERENCES ranks(id)
               );
               """)
    
    cursor.execute(f"""
                   CREATE TABLE IF NOT EXISTS itemtypes (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       description TEXT
                   );
                   """)
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS item (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT,
                       id_type INTEGER,
                       description TEXT,
                       price INTEGER,
                       durability INTEGER,
                       FOREIGN KEY (id_type) REFERENCES itemtypes(id)
                   );
                   """)
    
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS inventarioitem (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item_id INTEGER,
                        player_id INTEGER,
                        current_durability INTEGER,
                        FOREIGN KEY (item_id) REFERENCES item(id),
                        FOREIGN KEY (player_id) REFERENCES player(discordid)
                    );
            """)
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS objectivetypes (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       description TEXT
                   );
                   """)
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS objectives (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT,
                       type_id INTEGER,
                       xp_gain INTEGER,
                       gold_gain INTEGER,
                       description TEXT,
                       FOREIGN KEY (type_id) REFERENCES objectivetypes(id)
                   );
                   """)
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS completed_objectives (
                        discord_id BIGINT,
                        objective_id INTEGER,
                        FOREIGN KEY (discord_id) REFERENCES player(discordid),
                        FOREIGN KEY (objective_id) REFERENCES objectives(id),
                        PRIMARY KEY (discord_id, objective_id)
                   );
                   """)
    connection.commit()
    
    cursor.close()
    connection.close()

class ColumnEditor:
    def __init__(self, db_path) -> None:
        self.db_path = db_path
        self.update_query = None
    
    def set_data_update_query(self, query):
        self.update_query = query
        
    def commit(self, data):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        
        cursor.execute(self.update_query, data)
        connection.commit()
        
        cursor.close()
        connection.close()
if __name__ == '__main__':
    ...
    # create_tables()
    #add_player(475987459985734, 'teste', 'Koji')
    #create_rank()

class DBManager:
    def __init__(self, database_path, query_path) -> None:
        self.database_path = database_path
        self.query_path = query_path
        self.connection = None
        self.cursor = None
        self.query = None
    
    def __enter__(self):
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        
        with open(self.query_path, 'r', encoding='utf-8') as sqlfile:
            self.query = sqlfile.read()
        
        return self
    
    def __exit__(self, class_exception, exception_, traceback_):
        self.connection.commit()
        
        self.cursor.close()
        self.connection.close()
        return

class Comitter(DBManager):
    def commit(self, many=False, data=''):
        parsed = sqlparse.parse(self.query)
        if len(parsed) > 1 and not many:
            raise ValueError('You can only execute one statement at a time.')
        for statement in parsed:
            self.cursor.execute(str(statement), data)

class Puller(DBManager):
    def pull(self, data=()):
        parsed = sqlparse.parse(self.query)
        if len(parsed) > 1:
            raise ValueError('You can only execute one statement at a time.')
        self.cursor.execute(self.query, data)
        return self.cursor.fetchall()
