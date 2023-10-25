from commands.command import Command
from discord import Message
from dbhelper import Puller, Comitter
import discord
import botutils
from unidecode import unidecode

GET_ITEM_TYPE_QUERY = botutils.QUERIES_FOLDER_PATH / 'get_item_types.sql'
CREATE_ITEM_TYPE_QUERY = botutils.QUERIES_FOLDER_PATH / 'create_item_type.sql'

class AddItemType(Command):
    async def run(self, msg: Message):
        if not msg.author.guild_permissions.administrator:
            await msg.reply('Você não possui permissões de `administrador` para executar este comando.')
            return
            
        msg_as_list = msg.content.split()
        del msg_as_list[0]
        
        item_type_name = unidecode(" ".join(msg_as_list))
        
        content = tuple([item_type_name])
        
        with Comitter(botutils.DB_PATH, CREATE_ITEM_TYPE_QUERY) as commiter:
            commiter.commit(data=content)
        
        await msg.reply('Tipo de item adicionado com sucesso!')

class ItemTypes(Command):
    async def run(self, msg: Message):
        with Puller(botutils.DB_PATH, GET_ITEM_TYPE_QUERY) as puller:
            itemtypes = puller.pull()
        embed = discord.Embed(title='Tipos de Item')
        for index, type in enumerate(itemtypes, start=1):
            embed.add_field(name=f'{index}-{type[0]}', value='', inline=False)
        
        await msg.reply(embed=embed)
