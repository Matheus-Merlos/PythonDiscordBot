from discord import Message
from commands.command import Command
from commands.items.additem import get_item_name, item_exists
from unidecode import unidecode
from commands.shop import shoputils

class Buy(Command):
    async def run(self, msg: Message):
        msg_as_list = msg.content.split()
        
        discord_id = msg.author.id
        item_name = unidecode(get_item_name(msg_as_list)).capitalize().strip()
        
        if not item_exists(item_name):
            await msg.reply(f'Não existe um item com o nome `{item_name}`')
            return
        
        player_gold = shoputils.get_player_gold(discord_id)
        