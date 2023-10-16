from pathlib import Path

ROOT_DIR = Path(__file__).parent
DB_PATH = ROOT_DIR / 'database.sqlite3'

def get_id_from_mention(mention):
    mention = mention[2:] [:-1]
    return mention