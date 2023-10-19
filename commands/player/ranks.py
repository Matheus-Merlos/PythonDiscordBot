from commands.command import Command
from discord import Message
import botutils
from dbhelper import *
from unidecode import unidecode

class AddRank(Command):
    async def run(self, msg: Message):
        if not msg.author.guild_permissions.administrator:
            await msg.reply('Você não possui permissões de `administrador` para executar este comando.')
            return
        
        msg_as_list = msg.content.split()
        
        try:
            rank_description = unidecode(msg_as_list[1].strip().capitalize())
            required_exp = msg_as_list[2]
            new_slots = msg_as_list[3]
            new_atts = msg_as_list[4]
        except:
            await msg.reply('Você não forneceu todas as informações necessárias!')
            return
        
        rank = (rank_description, required_exp, new_slots, new_atts)
        
        comm = Comitter(botutils.DB_PATH)
        comm.set_data_insertion_query('INSERT INTO ranks (description, required_exp, new_slots, new_atts) VALUES (?, ?, ?, ?)')
        comm.commit(rank)
        
        await msg.reply('Rank adicionado com sucesso.')