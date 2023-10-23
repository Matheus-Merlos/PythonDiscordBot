from discord import Message
from commands.command import Command
from commands.items.additem import item_exists
from unidecode import unidecode
from commands.shop import shoputils
import botutils

class Give(Command):
    def __init__(self, name, prefix, syntax, description, client) -> None:
        super().__init__(name, prefix, syntax, description)
        self.client = client
    
    async def run(self, msg: Message):
        msg_as_list = msg.content.split()
        
        if not '@' in msg_as_list[1]:
            await msg.reply(f'`{msg_as_list[1]}` não é um player válido.')
            return
        
        discord_id = botutils.get_id_from_mention(msg_as_list[1])
        
        has_quantity = True if msg_as_list[-1].isdigit() else False
        quantity = int(msg_as_list[-1]) if has_quantity else 1
        
        item_name = unidecode(get_item_name(msg_as_list, has_quantity)).capitalize().strip()
        
        if not item_exists(item_name):
            await msg.reply(f'Não existe um item com o nome `{item_name}`')
            return
        
        item_id = shoputils.get_item_id_by_name(item_name)
        if shoputils.can_buy(discord_id, item_id):
            for i in range(quantity):
                shoputils.add_into_inventory(discord_id, item_id)
                
            await msg.reply(f'Você deu {quantity}x `{item_name}` para {self.client.get_user(int(discord_id)).display_name}.')
        else:
            await msg.reply(f'Você não pode dar esse item a este player, pois ele já o teve antes.')

def get_item_name(msg_as_list, has_quantity=False):
    if not has_quantity:
        return " ".join(msg_as_list[2:])
    
    return " ".join(msg_as_list[2:len(msg_as_list)-1])
        