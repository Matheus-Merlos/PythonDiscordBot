from dbhelper import Comitter
import botutils
from discord import Message

def update_player_stat(player_id, quantity, column, operation='+'):
    operations = ['+', '-']
    if operation not in operations:
        raise ValueError('This operation does not exist!')
    
    comm = Comitter(botutils.DB_PATH)
    query = f'UPDATE player SET {column} = {column} {operation} ? WHERE discordid = ?'
    comm.set_data_insertion_query(query)
    comm.commit((int(quantity), player_id))


def player_exists(discord_id):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT * FROM player WHERE discordid = ?')
    plr = pull.pull((discord_id,))
    
    return True if plr else False

def get_player_xp(discord_id):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT xp FROM player WHERE discordid = ?')
    xp = pull.pull((discord_id, ))
    return xp[0][0]

def get_rank(xp):
    xp = int(xp)
    if xp < 550:
        return '1'
    elif xp >= 550 and xp < 1500:
        return '2'
    elif xp >= 1500 and xp < 5000:
        return '3'
    elif xp >= 5000 and xp < 10000:
        return '4'
    elif xp >= 10000 and xp < 15000:
        return '5'
    elif xp >= 15000 and xp < 20000:
        return '6'
    else:
        return '7'

def check_player_rank(discord_id):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT ranks.id FROM ranks INNER JOIN player ON player.rank_id = ranks.id WHERE player.discordid = ?')
    rank = pull.pull((discord_id, ))
    return rank[0][0]

def change_rank(discord_id, new_rank):
    comm = Comitter(botutils.DB_PATH)
    query = 'UPDATE player SET rank_id = ? WHERE discordid = ?'
    comm.set_data_insertion_query(query)
    comm.commit((new_rank, discord_id))

async def alert_player(discord_id, new_rank_id, msg: Message):
    mention = f'<@{discord_id}>'
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT description, new_slots, new_atts FROM ranks WHERE id = ?')
    rank_name, new_slots, new_atts = pull.pull((new_rank_id, ))[0]
    
    await msg.channel.send(f'O player {mention} acabou de evoluir para **{rank_name.capitalize()}** e ganhou **{new_slots}** de habilidade e **{new_atts}** pontos de atributos, além de poder modificar uma habilidade antiga!')

async def check_update_and_alert_player(discord_id, xp_added, msg: Message):
    before = int(get_player_xp(discord_id))
    after = before + int(xp_added)
    
    rank_after_xp = get_rank(after)
    actual_rank = check_player_rank(discord_id)
    
    if int(actual_rank) != int(rank_after_xp):
        change_rank(discord_id, rank_after_xp)
        await alert_player(discord_id, rank_after_xp, msg)

        
def check_and_update_player(discord_id, xp_added):
    before = int(get_player_xp(discord_id))
    after = before - int(xp_added)
    
    rank_after_xp = get_rank(after)
    actual_rank = check_player_rank(discord_id)
    
    if int(actual_rank) != int(rank_after_xp):
        change_rank(discord_id, rank_after_xp) 
    