from discord import Message
from commands.command import Command
import botutils
from dbhelper import Comitter
from unidecode import unidecode

class AddObjective(Command):
    async def run(self, msg: Message):
        msg_as_list = msg.content.split()
        
        name = unidecode(get_objective_name(msg_as_list).capitalize().strip())
        if objective_exists(name):
            await msg.reply('Esse objetivo já existe!')
            return
                    
        xp_gain, index = get_objective_exp(msg_as_list)
        
        try:
            type = get_objective_type(msg_as_list, index)
        except:
            await msg.reply(f'Não existe um tipo objetivo com o nome/id `{msg_as_list[index+1]}`')
            return
        
        gold_gain = msg_as_list[index+2].strip()
        
        description = get_objective_description(msg_as_list, index)
        
        objective = (name, type, xp_gain, gold_gain, description)
        
        comm = Comitter(botutils.DB_PATH)
        comm.set_data_insertion_query('INSERT INTO objectives (name, type_id, xp_gain, gold_gain, description) VALUES (?, ?, ?, ?, ?)')
        comm.commit(objective)
        
        await msg.reply('Objetivo adicionado com sucesso.')
        

#Pega o nome do item, através de pegar todas as primeiras palavras, dando um break quando ele chega no preço
def get_objective_name(msg_as_list: list):
    del msg_as_list[0]
    item_name_list = list()
    for word in msg_as_list:
        if not word.isdigit():
            #Remove as aspas do nome
            word.replace("'", '') if "'" in word else word
            word.replace('"', '') if '"' in word else word
            item_name_list.append(word)
        else:
            break
        
    item_name = " ".join(item_name_list)
    return item_name

def get_objective_exp(msg_as_list: list):
    for index, word in enumerate(msg_as_list):
        if word.isdigit():
            return word, index
    return None

def get_objective_type(msg_as_list: list, index):
    type = msg_as_list[index+1].capitalize()
    if type.strip().isdigit():
        if int(type) > 4:
            raise ValueError('This objective id does not exist!')
        return type
    else:
        return get_objective_type_from_name(type)

def get_objective_type_from_name(objective_type):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT id FROM objectivetypes WHERE description = ?')
    objective_type_id = pull.pull((objective_type, ))
    
    if not objective_type_id:
        raise ValueError('This objective does not exist!')
    
    return objective_type_id[0][0]

def get_objective_description(msg_as_list: list, index: int):
    item_name_list = msg_as_list[index+3:]
        
    objective_description = " ".join(item_name_list)
    return objective_description

def objective_exists(objective_name):
    pull = Comitter(botutils.DB_PATH)
    pull.set_data_pull_query('SELECT id FROM objectives WHERE name = ?')
    objective = pull.pull((objective_name, ))
    
    if objective:
        return True
    
    return False
