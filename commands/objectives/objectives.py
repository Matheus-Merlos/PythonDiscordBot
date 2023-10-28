from commands.command import Command
from discord import Message, Embed
from dbhelper import Puller
import botutils
from commands.shop.shop import show_embeds

GET_OBJECTIVES = botutils.QUERIES_FOLDER_PATH / 'get_objectives.sql'

class Objectives(Command):
    def __init__(self, name, prefix, syntax, description, client) -> None:
        super().__init__(name, prefix, syntax, description)
        self.client = client

    async def run(self, msg: Message):
        with Puller(botutils.DB_PATH, GET_OBJECTIVES) as plr:
            objectives = plr.pull()
        
        pequenos = [objective for objective in objectives if objective[1] == 'Pequeno']
        medios = [objective for objective in objectives if objective[1] == 'Medio']
        grandes = [objective for objective in objectives if objective[1] == 'Grande']
        insanos =  [objective for objective in objectives if objective[1] == 'Insano']
        
        embed_list = list()
        embed_list.append(generate_embed('Objetivos Pequenos', pequenos))
        embed_list.append(generate_embed('Objetivos Médios', medios))
        embed_list.append(generate_embed('Objetivos Grandes', grandes))
        embed_list.append(generate_embed('Objetivos Insanos', insanos))
        
        await show_embeds(embed_list, msg, self.client)

def generate_embed(embed_title, list):
    embed = Embed(title=embed_title)
    for index, element in enumerate(list, start=1):
        embed.add_field(name=f'{index} - {element[0]}',
                        value=f'XP Ganho = {element[2]}\nGold Ganho = {element[3]}\n{element[4]}',
                        inline=False)
    
    return embed