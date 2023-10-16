from commands.command import Command
from discord import Message
from dbhelper import Comitter
import discord
import botutils

class AddItemType(Command):
    async def run(self, msg: Message):
        msg_as_list = msg.content.split()
        del msg_as_list[0]
        
        item_type_name = " ".join(msg_as_list)
        
        content = tuple([item_type_name])
        
        comm = Comitter(botutils.DB_PATH)
        comm.set_data_insertion_query("""
                                      INSERT INTO itemtypes (description)
                                      VALUES (?);
                                      """)
        comm.commit(content)
        
        await msg.reply('Tipo de item adicionado com sucesso!')

class ItemTypes(Command):
    async def run(self, msg: Message):
        comm = Comitter(botutils.DB_PATH)
        comm.set_data_pull_query("""
                                 SELECT (description) FROM itemtypes;
                                 """)
        
        itemtypes = comm.pull()
        
        embed = discord.Embed(title='Tipos de Item')
        for index, type in enumerate(itemtypes, start=1):
            embed.add_field(name=f'{index}-{type[0]}', value='', inline=False)
        
        await msg.channel.send(embed=embed)
