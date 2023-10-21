from commands.command import Command
from discord import Message, Embed
from dbhelper import Comitter
import botutils
from commands.shop.shop import show_embeds

class Objectives(Command):
    def __init__(self, name, prefix, syntax, description, client) -> None:
        super().__init__(name, prefix, syntax, description)
        self.client = client

    async def run(self, msg: Message):
        pull = Comitter(botutils.DB_PATH)
        pull.set_data_pull_query("""
                                 SELECT objectives.name, objectivetypes.description, objectives.xp_gain, objectives.gold_gain, objectives.description 
                                 FROM objectives 
                                 INNER JOIN objectivetypes ON objectives.type_id = objectivetypes.id
                                 ORDER BY objectives.type_id, objectives.xp_gain ASC
                                 """)
        
        objectives = pull.pull()
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