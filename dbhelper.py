import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).parent
DB_PATH = ROOT_DIR / 'database.sqlite3'

def create_table():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS ranks (
                    id INT PRIMARY KEY,
                    description TEXT
                );
               """)

    cursor.execute(f"""
               CREATE TABLE IF NOT EXISTS player (
                   discordid BIGINT PRIMARY KEY,
                   name TEXT,
                   charname TEXT,
                   xp INTEGER,
                   rank_id INT,
                   gold INTEGER,
                   FOREIGN KEY (rank_id) REFERENCES ranks(id)
               );
               """)
    connection.commit()
    
    cursor.close()
    connection.close()
