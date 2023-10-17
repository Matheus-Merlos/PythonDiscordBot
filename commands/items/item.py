from commands.command import Command
from discord import Message
from discord import Embed
from dbhelper import Comitter
from unidecode import unidecode
import botutils

class Item(Command):
    async def run(self, msg: Message):
        msg_as_list = msg.content.split()[1:]
        item_name = unidecode(" ".join(msg_as_list).capitalize())
        
        puller = Comitter(botutils.DB_PATH)
        puller.set_data_pull_query("""SELECT item.nome, item.price, itemtypes.description, item.durability, item.description 
                                   FROM item 
                                   INNER JOIN itemtypes ON item.id_type = itemtypes.id WHERE item.nome = ?""")
        item = puller.pull((item_name,))[0]

        embed = Embed(title=item[0])
        embed.add_field(name='Preço', value=item[1], inline=True)
        embed.add_field(name='Tipo', value=item[2], inline=True)
        embed.add_field(name='Durabilidade', value=item[3], inline=True)
        embed.add_field(name='Descrição', value=item[4], inline=False)
        await msg.reply(embed=embed)
