from commands.command import Command
from discord import Message, Embed
import botutils
from dbhelper import *
from unidecode import unidecode

GET_OBJECTIVE_TYPES = botutils.DB_PATH / 'get_objective_types.sql'
INSERT_OBJECTIVE_TYPE = botutils.DB_PATH / 'create_objetive_type.sql'

class AddObjectiveType(Command):
    async def run(self, msg: Message):
        if not msg.author.guild_permissions.administrator:
            await msg.reply('Você não possui permissões de `administrador` para executar este comando.')
            return
        
        msg_as_list = msg.content.split()
        
        try:
            objective_type = unidecode(msg_as_list[1].strip().capitalize())
        except:
            await msg.reply('Você não forneceu todas as informações necessárias!')
            return
        
        with Comitter(botutils.DB_PATH, INSERT_OBJECTIVE_TYPE) as comm:
            comm.commit(data=(objective_type, ))
        comm = Comitter(botutils.DB_PATH)
        
        await msg.reply('Tipo de objetivo adicionado com sucesso.')

class ObjectiveType(Command):
    async def run(self, msg: Message):
        with Puller(botutils.DB_PATH, GET_OBJECTIVE_TYPES) as plr:
            types = plr.pull()
        
        embed = Embed(title='Tipos de Objetivos')
        for type in types:
            embed.add_field(name=f'{type[0]}  -  {type[1]}', value='', inline=False)
        
        await msg.reply(embed=embed)
            
        