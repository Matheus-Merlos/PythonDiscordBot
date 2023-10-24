from discord import Message
from commands.command import Command
import discord
from dbhelper import Comitter
import botutils
from commands.player.playerutils import player_exists

RESET_XP_GOLD = botutils.QUERIES_FOLDER_PATH / 'reset_xp_and_gold.sql'
RESET_OBJECTIVES = botutils.QUERIES_FOLDER_PATH / 'remove_objectives.sql'
RESET_INVENTORY = botutils.QUERIES_FOLDER_PATH / 'remove_items.sql'

class ResetPlayer(Command):
    async def run(self, msg: Message):
        if not msg.author.guild_permissions.administrator:
            await msg.reply('Você não possui permissões de `administrador` para executar este comando.')
            return
        
        msg_as_list = msg.content.split()
        
        player_id = botutils.get_id_from_mention(msg_as_list[1])
        
        if not player_exists(player_id):
            await msg.reply('Esse player não existe! Você precisa adicionar ele usando o comando `;addplayer`')
            return
        
        with Comitter(botutils.DB_PATH, RESET_XP_GOLD) as comm:
            comm.commit(player_id)
        
        with Comitter(botutils.DB_PATH, RESET_INVENTORY) as comm:
            comm.commit(player_id)
        
        with Comitter(botutils.DB_PATH, RESET_OBJECTIVES) as comm:
            comm.commit(player_id)
        
        await msg.reply('Player resetado com sucesso!')
        
        