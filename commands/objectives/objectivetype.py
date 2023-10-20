from commands.command import Command
from discord import Message, Embed
import botutils
from dbhelper import *
from unidecode import unidecode

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
        
        comm = Comitter(botutils.DB_PATH)
        comm.set_data_insertion_query('INSERT INTO objectivetypes (description) VALUES (?)')
        comm.commit((objective_type,))
        
        await msg.reply('Tipo de objetivo adicionado com sucesso.')

class ObjectiveType(Command):
    async def run(self, msg: Message):
        puller = Comitter(botutils.DB_PATH)
        puller.set_data_pull_query("SELECT id, description FROM objectivetypes;")
        types = puller.pull()
        
        embed = Embed(title='Tipos de Objetivos')
        for type in types:
            embed.add_field(name=f'{type[0]}  -  {type[1]}', value='', inline=False)
        
        await msg.reply(embed=embed)
            
        