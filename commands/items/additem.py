from commands.command import Command
from discord import Message
from dbhelper import *
import botutils
from unidecode import unidecode

GET_ITEM_TYPE_QUERY = botutils.QUERIES_FOLDER_PATH / 'get_item_type.sql'
CREATE_ITEM_QUERY_PATH = botutils.QUERIES_FOLDER_PATH / 'create_item.sql'
ITEM_EXISTS_QUERY = botutils.QUERIES_FOLDER_PATH / 'item_exists.sql'
GET_ITEM_TYPE_ID_QUERY = botutils.QUERIES_FOLDER_PATH / 'get_item_type_from_id.sql'

class AddItem(Command):
    async def run(self, msg: Message):
        msg_as_list = msg.content.split()
        
        #Pega o nome do item e checa se ele já existe na base de dados
        item_name = unidecode(get_item_name(msg_as_list)).capitalize().strip()
        if item_exists(item_name):
            await msg.reply(f'O item "{item_name}" já existe.')
            return
        
        item_price, index = self.get_item_price(msg_as_list)
        try:
            item_type, index2 = self.get_item_type(msg_as_list, index)
        except ItemTypeNotFoundError:
            await msg.reply(f'Não existe um tipo de item com esse nome/id.')
            return
    
        with Puller(botutils.DB_PATH, GET_ITEM_TYPE_QUERY) as puller:
            type_id = puller.pull((item_type,))[0][0]
        
        item_durability = self.get_item_durability(msg_as_list, index2)
        item_description = self.get_item_description(msg_as_list, index2 + 1)
        
        #Cria a tupla contendo os dados do item
        item = (item_name, type_id, item_description, item_price, item_durability)
        #Insere os dados        
        with Comitter(botutils.DB_PATH, CREATE_ITEM_QUERY_PATH) as comm:
            comm.commit(data=item)
        
        await msg.reply('Item criado com sucesso!')
    
    #Pega o preço do item, por ele ser o primeiro item numérico da lista, então fazemos um for simples
    #Retorna: Preço do item, Índice dele na lista
    @staticmethod
    def get_item_price(msg_as_list: list[str]):
        for word in msg_as_list:
            if word.isdigit():
                return word, msg_as_list.index(word)
        
        raise SyntaxError('Price not identified')
    
    def get_item_type(self, msg_as_list: list[str], starting_index: int):
        msg_as_list = msg_as_list[starting_index + 1:]
        if msg_as_list[0].isdigit():
            id = int(msg_as_list[0])
            item_type = self.retrieve_item_type_by_id(id)
            index = starting_index + 1
        else:
            item_type, index = self.retrieve_item_type_by_text(msg_as_list, starting_index)


        return item_type, index

    @staticmethod
    def get_item_durability(msg_as_list: list[str], starting_index: int):
        return int(msg_as_list[starting_index + 1])
    
    @staticmethod
    def get_item_description(msg_as_list: list[str], starting_index: int):
        msg_as_list = msg_as_list[starting_index + 1:]
        
        return " ".join(msg_as_list)
    
    
    @staticmethod
    def retrieve_item_type_by_id(item_id: int):
        with Puller(botutils.DB_PATH, GET_ITEM_TYPE_ID_QUERY) as puller:
            result = puller.pull((item_id,))
        if not result:
            raise ItemTypeNotFoundError(f'Item type with id = {item_id} does not exist')
        
        return result[0][0]
     
    def retrieve_item_type_by_text(self, msg_as_list, starting_index):
        item_type_list = list()
        for word in msg_as_list:
            if not word.isdigit():
                #Remove as aspas do tipo
                word.replace("'", '') if "'" in word else word
                word.replace('"', '') if '"' in word else word
                item_type_list.append(word)
                starting_index += 1
            else:
                break
        item_name = " ".join(item_type_list)
        item_name = item_name.capitalize()
        with Puller(botutils.DB_PATH, GET_ITEM_TYPE_QUERY) as puller:
            result = puller.pull((item_name,))
        if not result:
            raise ItemTypeNotFoundError(f'Item type with name = {item_name} does not exist')
        
        item_name = self.retrieve_item_type_by_id(result[0][0])
        
        return item_name, starting_index

def item_exists(item_name):
    with Puller(botutils.DB_PATH, ITEM_EXISTS_QUERY) as puller:
        exists = puller.pull((item_name,))
    return True if exists else False

#Pega o nome do item, através de pegar todas as primeiras palavras, dando um break quando ele chega no preço
def get_item_name(msg_as_list: list):
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
    return unidecode(item_name).capitalize().strip()
        

class ItemTypeNotFoundError(Exception): ...

class ItemExistsError(Exception): ...