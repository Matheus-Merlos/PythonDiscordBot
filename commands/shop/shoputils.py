import botutils
from dbhelper import Comitter

def get_player_gold(discord_id):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT gold FROM player WHERE id = ?')
    
    return pull.pull((discord_id,))[0][0]

def get_item_price(item_name):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT gold FROM player WHERE id = ?')
    
    return pull.pull((item_name,))[0][0]