from commands.command import Command
from commands.items.additem import get_item_name, item_exists
from commands.shop.shoputils import get_item_id_by_name
from discord import Message
from dbhelper import Comitter
import botutils

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
        
        comm = Comitter(botutils.DB_PATH)
        comm.set_data_insertion_query("""
                                        UPDATE inventarioitem
                                        SET current_durability = current_durability - 1
                                        WHERE item_id = ? AND player_id = ? AND current_durability > 0
                                        LIMIT 1;
                                      """)
        
        comm.commit((item_id, discord_id))
        
        await msg.reply(':thumbsup:')
        
def has_item_in_inventory(discord_id, item_id):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT id FROM inventarioitem WHERE player_id = ? AND item_id = ? AND current_durability > 0')
    
    return True if pull.pull((discord_id, item_id)) else False
