from commands.command import Command
from discord import Message
from dbhelper import Comitter
import discord
import botutils
from unidecode import unidecode

class AddItemType(Command):
    async def run(self, msg: Message):
        if not msg.author.guild_permissions.administrator:
            await msg.reply('Você não possui permissões de `administrador` para executar este comando.')
            return
            
        msg_as_list = msg.content.split()
        del msg_as_list[0]
        
        item_type_name = " ".join(msg_as_list)
        
        content = tuple([item_type_name])
        
        comm = Comitter(botutils.DB_PATH)
        comm.set_data_insertion_query("INSERT INTO itemtypes (description) VALUES (?);")
        comm.commit(unidecode(content))
        
        await msg.reply('Tipo de item adicionado com sucesso!')

class ItemTypes(Command):
    async def run(self, msg: Message):
        comm = Comitter(botutils.DB_PATH)
        comm.set_data_pull_query("SELECT (description) FROM itemtypes;")
        
        itemtypes = comm.pull()
        
        embed = discord.Embed(title='Tipos de Item')
        for index, type in enumerate(itemtypes, start=1):
            embed.add_field(name=f'{index}-{type[0]}', value='', inline=False)
        
        await msg.reply(embed=embed)
