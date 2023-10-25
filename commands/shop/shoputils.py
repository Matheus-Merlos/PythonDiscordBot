import botutils
from dbhelper import Comitter, Puller

GET_ITEM_PRICE_QUERY = botutils.QUERIES_FOLDER_PATH / 'get_item_price.sql'
GET_ITEM_ID_BY_NAME_QUERY = botutils.QUERIES_FOLDER_PATH / 'get_item_id_by_name.sql'
GET_ITEM_ITEMTYPE = botutils.QUERIES_FOLDER_PATH / 'get_item_itemtype.sql'
HAS_ITEM = botutils.QUERIES_FOLDER_PATH / 'has_item_no_durability.sql'
ADD_INTO_INVENTORY = botutils.QUERIES_FOLDER_PATH / 'add_into_inventory.sql'
GET_ITEM_DURABILITY = botutils.QUERIES_FOLDER_PATH / 'get_item_durability.sql'

def get_item_price(item_name):
    with Puller(botutils.DB_PATH, GET_ITEM_PRICE_QUERY) as puller:
        return puller.pull((item_name,))[0][0]

def get_item_id_by_name(item_name):
    with Puller(botutils.DB_PATH, GET_ITEM_ID_BY_NAME_QUERY) as puller:
        return puller.pull((item_name,))[0][0]

def get_item_type(item_id):
    with Puller(botutils.DB_PATH, GET_ITEM_ITEMTYPE) as pull:
        return pull.pull((item_id,))[0][0]

def has_item_in_inventory(discord_id, item_id):
    with Puller(botutils.DB_PATH, HAS_ITEM) as pull:
        return True if pull.pull((discord_id, item_id)) else False

def can_buy(discord_id, item_id, quantity=1):
    permitted_types = (2, 3, 8, 5, 4)
    item_type = get_item_type(item_id)
     
    if has_item_in_inventory(discord_id, item_id):
        return True if item_type in permitted_types else False
    return True

def get_item_durability(item_id):
    with Puller(botutils.DB_PATH, GET_ITEM_DURABILITY) as pull:
        return pull.pull((item_id,))[0][0]

def add_into_inventory(discord_id, item_id):
    durability = get_item_durability(item_id)
    
    with Comitter(botutils.DB_PATH, ADD_INTO_INVENTORY) as comm:
        comm.commit(data=(discord_id, item_id, durability))