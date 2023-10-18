import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).parent
DB_PATH = ROOT_DIR / 'database.sqlite3'

def create_tables():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS ranks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT
                );
               """)

    cursor.execute(f"""
               CREATE TABLE IF NOT EXISTS player (
                   discordid BIGINT PRIMARY KEY,
                   name TEXT,
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
                       nome TEXT,
                       id_type INTEGER,
                       description TEXT,
                       price INTEGER,
                       durability INTEGER,
                       FOREIGN KEY (id_type) REFERENCES itemtypes(id)
                   );
                   """)
    
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS inventarioitem (
                        item_id INTEGER,
                        player_id INTEGER,
                        current_durability INTEGER,
                        FOREIGN KEY (item_id) REFERENCES item(id),
                        FOREIGN KEY (player_id) REFERENCES player(discordid),
                        PRIMARY KEY (item_id, player_id)
                    );
            """)
    connection.commit()
    
    cursor.close()
    connection.close()
    
class Comitter:
    def __init__(self, database_path):
        self.database_path = database_path
        self.query = None
        self.pull_query = None
    
    def set_data_insertion_query(self, query):
        self.query = query
    
    def set_data_pull_query(self, query):
        self.pull_query = query
    
    def commit(self, data):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        
        cursor.execute(self.query, data)
        connection.commit()
        
        cursor.close()
        connection.close()
        
    def pull(self, args=()):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        
        cursor.execute(self.pull_query, args)
        
        content = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return content

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
    create_tables()
    #add_player(475987459985734, 'teste', 'Koji')
    #create_rank()
