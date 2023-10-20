from commands.command import Command
from discord import Message, Embed
import botutils
from dbhelper import Comitter

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
        
        xp = get(player_id, 'xp')
        gold = get(player_id, 'gold')
        
        embed = Embed(title=f'Inventário de {self.client.get_user(int(player_id)).display_name}')
        embed.add_field(name='XP Total', value=xp, inline=True)
        embed.add_field(name='Gold', value=f'R${gold},00', inline=True)
        
        await msg.reply(embed=embed)


def get(player_id, column):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query(f'SELECT {column} FROM player WHERE discordid = ?')
    plr = pull.pull((player_id,))
    return plr[0][0]