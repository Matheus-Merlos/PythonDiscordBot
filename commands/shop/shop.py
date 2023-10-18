from commands.command import Command
from discord import Message, Embed
from dbhelper import Comitter
import botutils
import asyncio
from discord.ext import commands
from unidecode import unidecode

class Shop(Command):
    #Adiciona o parâmetro client para poder checar depois as reações
    def __init__(self, name, prefix, syntax, description, client) -> None:
        super().__init__(name, prefix, syntax, description)
        self.client = client
    
    async def run(self, msg: Message):
        #Pega todos os itens do banco de dados, em ordem ascendente de preço
        msg_as_list = msg.content.split()
        print(len(msg_as_list))
        if len(msg_as_list) == 1:
            items = get_items()
        else:
            if msg_as_list[1].isdigit():
                items = get_items(msg_as_list[1])
            else:
                word = unidecode(" ".join(msg_as_list[1:]).capitalize())
                puller = Comitter(botutils.DB_PATH)
                puller.set_data_pull_query("SELECT id FROM itemtypes WHERE description = ?")
                items = get_items(puller.pull((word, )))
        
        #Divide a lista em várias mini listas de 10 items cada
        separated_lists = list()
        for i in range(0, len(items), 10):
            sublist = items[i:i + 10]
            separated_lists.append(sublist)
            
        embeds = list()
        
        #Cria uma embed separada para cada mini-lista que foi criada anteriormente
        for index, sublist in enumerate(separated_lists, start=1):
            embed = Embed(title='Loja')
            embed.set_footer(text=f'Página {index}/{len(separated_lists)}')
            
            for item in sublist:
                description = f'{item[2][:128]}...' if len(item[2]) > 128 else item[2]
                embed.add_field(name=f'{item[0]} - R${item[1]}', value=description, inline=False)
            embeds.append(embed)
        
        await show_embeds(embeds, msg, self.client)
        
    

def get_items(item_type=None):
    if not item_type:
        puller = Comitter(botutils.DB_PATH)
        puller.set_data_pull_query("SELECT nome, price, description FROM item ORDER BY price ASC;")
        return puller.pull()
    else:
        puller = Comitter(botutils.DB_PATH)
        puller.set_data_pull_query("SELECT nome, price, description FROM item WHERE id_type = ? ORDER BY price ASC;")
        return puller.pull(item_type)

async def show_embeds(embeds: list, msg: Message, client):
    message = await msg.reply(embed=embeds[0])
    await message.add_reaction('⬅️')
    await message.add_reaction('➡️')
        
    def check(reaction, user):
            return user == msg.author and str(reaction.emoji) in ['⬅️', '➡️']
        
    current_embed = 0
        
    while True:
        try:
        #Fica verificando as reações, para saber se ele vai para frente ou para trás, isso dura por 60 segudos, após isso ele para de responder
            reaction, user = await client.wait_for('reaction_add', check=check, timeout=60.0)

            if str(reaction.emoji) == '⬅️':
                current_embed = max(current_embed - 1, 0)
            elif str(reaction.emoji) == '➡️':
                current_embed = min(current_embed + 1, len(embeds) - 1)

            await message.edit(embed=embeds[current_embed])
            await message.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            break
    