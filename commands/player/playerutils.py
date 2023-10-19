from dbhelper import Comitter
import botutils

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