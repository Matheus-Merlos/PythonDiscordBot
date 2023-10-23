from discord import Message
from commands.command import Command
import discord
from dbhelper import Comitter
import botutils
from commands.player.playerutils import player_exists

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
        
        reset_xp_and_gold(player_id)
        remove_items(player_id)
        remove_objectives(player_id)
        
        await msg.reply('Player resetado com sucesso!')
        
def reset_xp_and_gold(player_id):
    comm = Comitter(botutils.DB_PATH)
    comm.set_data_insertion_query("""
                                  UPDATE player SET xp = 0, gold = 1000, rank_id = 1 WHERE discordid = ?
                                  """)
    comm.commit((player_id, ))
    
def remove_items(player_id):
    comm = Comitter(botutils.DB_PATH)
    comm.set_data_insertion_query("DELETE FROM inventarioitem WHERE player_id = ?")
    comm.commit((player_id, ))
    
def remove_objectives(player_id):
    comm = Comitter(botutils.DB_PATH)
    comm.set_data_insertion_query("DELETE FROM completed_objectives WHERE discord_id = ?")
    comm.commit((player_id, ))
        
        