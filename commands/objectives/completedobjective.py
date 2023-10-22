from commands.command import Command
from discord import Message
import botutils
from commands.player.playerutils import *
from commands.objectives.addobjective import objective_exists
from dbhelper import Comitter

class CompletedObjective(Command):
    async def run(self, msg: Message):
        msg_as_list = msg.content.split()
        
        discord_id = botutils.get_id_from_mention(msg_as_list[1])
        objective_name = " ".join(msg_as_list[2:]).capitalize().strip()
        
        if not player_exists(discord_id):
            await msg.reply('Esse player não existe, ou não está cadastrado no sistema.')
            return
                
        if not objective_exists(objective_name):
            await msg.reply(f'Não existe objetivo com o nome `{objective_name}`')
            return
        
        xp, gold = get_objective_xp_and_gold(objective_name)
        
        await check_update_and_alert_player(discord_id, xp, msg)
        
        update_player_stat(discord_id, xp, 'xp', '+')
        update_player_stat(discord_id, gold, 'gold', '+')
        
        await msg.reply('Recompensas do objetivo adicionadas ao player com sucesso.')
        
def get_objective_xp_and_gold(objective_name):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT xp_gain, gold_gain FROM objectives WHERE name = ?')
    stats = pull.pull((objective_name, ))
    
    xp, gold = stats[0]
    return xp, gold
    