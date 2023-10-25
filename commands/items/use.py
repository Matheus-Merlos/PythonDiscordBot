from commands.command import Command
from commands.items.additem import get_item_name, item_exists
from commands.shop.shoputils import get_item_id_by_name
from discord import Message
from dbhelper import Comitter, Puller
import botutils

USE_ITEM_QUERY = botutils.QUERIES_FOLDER_PATH / 'create_item_type.sql'
HAS_ITEM_QUERY = botutils.QUERIES_FOLDER_PATH / 'has_item.sql'

class Use(Command):
    async def run(self, msg: Message):
        msg_as_list = msg.content.split()
        
        item_name = get_item_name(msg_as_list)
        
        if not item_exists(item_name):
            await msg.reply(f'Não existe um item com o nome {item_name}')
            return
        
        discord_id = msg.author.id
        item_id = get_item_id_by_name(item_name)
        
        if not has_item_in_inventory(discord_id, item_id):
            await msg.reply('Você não possui esse item em seu inventário.')
            return
        
        with Comitter(botutils.DB_PATH, USE_ITEM_QUERY) as comm:
            comm.commit(data=(item_id, discord_id))
        
        await msg.reply(':thumbsup:')
        
def has_item_in_inventory(discord_id, item_id):
    with Puller(botutils.DB_PATH, HAS_ITEM_QUERY) as pull:
        return True if pull.pull((discord_id, item_id)) else False
