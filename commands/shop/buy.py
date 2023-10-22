from discord import Message
from commands.command import Command
from commands.items.additem import item_exists
from unidecode import unidecode
from commands.shop import shoputils
from commands.player import playerutils

class Buy(Command):
    async def run(self, msg: Message):
        msg_as_list = msg.content.split()
        
        discord_id = msg.author.id
        
        has_quantity = True if msg_as_list[-1].isdigit() else False
        quantity = int(msg_as_list[-1]) if has_quantity else 1
        
        item_name = unidecode(get_item_name(msg_as_list, has_quantity)).capitalize().strip()
        
        if not item_exists(item_name):
            await msg.reply(f'Não existe um item com o nome `{item_name}`')
            return
        
        player_gold = int(shoputils.get_player_gold(discord_id))
        total_price = int(shoputils.get_item_price(item_name)) * quantity
        
        if total_price > player_gold:
            await msg.reply(f'Você não possui gold suficiente para comprar {quantity}x `{item_name}`.')
            return
        
        playerutils.update_player_stat(discord_id, total_price, 'gold', '-')
        
        item_id = shoputils.get_item_id_by_name(item_name)
        if shoputils.can_buy(discord_id, item_id):
            for i in range(quantity):
                shoputils.add_into_inventory(discord_id, item_id)
                
            await msg.reply(f'Você comprou {quantity}x `{item_name}`.')
        else:
            await msg.reply(f'Você não pode comprar esse item, pois você já comprou ele antes.')

def get_item_name(msg_as_list, has_quantity=False):
    if not has_quantity:
        return " ".join(msg_as_list[1:])
    
    return " ".join(msg_as_list[1:len(msg_as_list)-1])


        