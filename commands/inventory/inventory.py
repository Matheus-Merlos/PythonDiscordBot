from commands.command import Command
from discord import Message, Embed
import botutils
from dbhelper import Puller

QUERY_PATH = botutils.QUERIES_FOLDER_PATH / 'inventory_pull.sql'
XP_QUERY = botutils.QUERIES_FOLDER_PATH / 'get_player_xp.sql'
GOLD_QUERY = botutils.QUERIES_FOLDER_PATH / 'get_player_gold.sql'

class Inventory(Command):
    def __init__(self, name, prefix, syntax, description, client) -> None:
        super().__init__(name, prefix, syntax, description)
        self.client = client
    
    async def run(self, msg: Message):
        msg_as_list = msg.content.split()
        if len(msg_as_list) == 1:
            player_id = msg.author.id
        else:
            player_id = botutils.get_id_from_mention(msg_as_list[1])
            
        with Puller(botutils.DB_PATH, XP_QUERY) as puller:
            xp = puller.pull((str(player_id),))[0][0]
        with Puller(botutils.DB_PATH, GOLD_QUERY) as puller:
            gold = puller.pull((str(player_id),))[0][0]
        
        embed = Embed(title=f'Inventário de {self.client.get_user(int(player_id)).display_name}')
        embed.add_field(name='XP Total', value=xp, inline=True)
        embed.add_field(name='Gold', value=f'R${gold},00', inline=True)
        
        with Puller(botutils.DB_PATH, QUERY_PATH) as puller:
            items = puller.pull((str(player_id),))
        if items:
            for item in items:
                embed.add_field(name=f'{item[1]} - {item[0]}', value='', inline=False)
        
        await msg.reply(embed=embed)