from commands.command import Command
from discord import Message
import botutils
from dbhelper import *
from commands.player.playerutils import player_exists, get_rank

class AddPlayer(Command):
    async def run(self, msg: Message):
        if not msg.author.guild_permissions.administrator:
            await msg.reply('Você não possui permissões de `administrador` para executar este comando.')
            return
        
        msg_as_list = msg.content.split()
        
        
        discord_id = botutils.get_id_from_mention(msg_as_list[1])
        char_name = get_char_name(msg_as_list).strip().title()
        xp, gold = get_xp_and_gold(msg_as_list)
        rank_id = get_rank(xp)
        
        if player_exists(discord_id):
            await msg.reply('Esse player já existe! Se você deseja alterar o nome do personagem, utilize o comando `;editchar`')
            return
        
        player = (discord_id, char_name, xp, rank_id, gold)
        
        comm = Comitter(DB_PATH)
        comm.set_data_insertion_query('INSERT INTO player (discordid, charname, xp, rank_id, gold) VALUES (?, ?, ?, ?, ?)')
        comm.commit(player)
        
        await msg.reply('Player adicionado com sucesso.')
        
    

def get_char_name(msg_as_list):
    char_name_list = list()
    for word in msg_as_list[2:]:
        if not word.isdigit():
            char_name_list.append(word)
        else:
            break
    
    return " ".join(char_name_list)

def get_xp_and_gold(msg_as_list):
    args = list()
    for word in msg_as_list[2:]:
        if word.isdigit():
            args.append(word)
        else:
            continue
        
    if len(args) == 0:
        args = [0, 0]
    
    return tuple(args)
    