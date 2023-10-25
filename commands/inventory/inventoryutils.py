import botutils
from dbhelper import Puller

XP_QUERY = botutils.QUERIES_FOLDER_PATH / 'get_player_xp.sql'
GOLD_QUERY = botutils.QUERIES_FOLDER_PATH / 'get_player_gold.sql'

def get_player_xp(player_id):
    with Puller(botutils.DB_PATH, XP_QUERY) as puller:
        xp = puller.pull((str(player_id),))[0][0]
    return xp

def get_player_gold(player_id):
    with Puller(botutils.DB_PATH, GOLD_QUERY) as puller:
        gold = puller.pull((str(player_id),))[0][0]
    return gold