from commands.command import Command
from discord import Message
from discord import Embed
from dbhelper import Puller
from unidecode import unidecode
import botutils

QUERY_PATH = botutils.QUERIES_FOLDER_PATH / 'get_item.sql'

class Item(Command):
    async def run(self, msg: Message):
        msg_as_list = msg.content.split()[1:]
        item_name = unidecode(" ".join(msg_as_list).capitalize().strip())
        
        with Puller(botutils.DB_PATH, QUERY_PATH) as puller:
            item = puller.pull((item_name,))[0]

        embed = Embed(title=item[0])
        embed.add_field(name='Preço', value=item[1], inline=True)
        embed.add_field(name='Tipo', value=item[2], inline=True)
        embed.add_field(name='Durabilidade', value=item[3], inline=True)
        embed.add_field(name='Descrição', value=item[4], inline=False)
        await msg.reply(embed=embed)
