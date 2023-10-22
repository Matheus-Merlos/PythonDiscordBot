import botutils
from dbhelper import Comitter

def get_player_gold(discord_id):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT gold FROM player WHERE discordid = ?')
    
    return pull.pull((discord_id,))[0][0]

def get_item_price(item_name):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT price FROM item WHERE name = ?')
    
    return pull.pull((item_name,))[0][0]

def get_item_id_by_name(item_name):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT id FROM item WHERE name = ?')
    
    return pull.pull((item_name,))[0][0]

def get_item_type(item_id):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT id_type FROM item WHERE id = ?')
    
    return pull.pull((item_id,))[0][0]

def has_item_in_inventory(discord_id, item_id):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT id FROM inventarioitem WHERE player_id = ? AND item_id = ?')
    
    return True if pull.pull((discord_id, item_id)) else False

def can_buy(discord_id, item_id, quantity=1):
    permitted_types = (2, 3, 8, 5, 4)
    item_type = get_item_type(item_id)
     
    if has_item_in_inventory(discord_id, item_id):
        return True if item_type in permitted_types else False
    return True
    

def add_into_inventory(discord_id, item_id):
    durability = get_item_durability(item_id)
    
    comm = Comitter(botutils.DB_PATH)
    comm.set_data_insertion_query('INSERT INTO inventarioitem (player_id, item_id, current_durability) VALUES (?, ?, ?)')
    comm.commit((discord_id, item_id, durability))

def get_item_durability(item_id):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT durability FROM item WHERE id = ?')
    
    return pull.pull((item_id,))[0][0]