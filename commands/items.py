from commands.command import Command
from discord import Message
from dbhelper import *
from commands.itemtypes import ItemTypes
import botutils

class AddItem(Command):
    async def run(self, msg: Message):
        msg_as_list = msg.content.split()
        item_name = self.get_item_name(msg_as_list)
        item_price, index = self.get_item_price(msg_as_list)
        item_type, index2 = self.get_item_type(msg_as_list, index)
        item_durability = self.get_item_durability(msg_as_list, index2)
        item_description = self.get_item_description(msg_as_list, index2 + 1)
        print(item_name, item_price, item_type, item_durability, item_description)
        
        
    
    #Pega o nome do item, através de pegar todas as primeiras palavras, dando um break quando ele chega no preço
    @staticmethod
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
        return item_name
    
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
        puller = Comitter(botutils.DB_PATH)
        puller.set_data_pull_query("SELECT description FROM itemtypes WHERE id = ?")
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
        puller = Comitter(botutils.DB_PATH)
        puller.set_data_pull_query("SELECT id FROM itemtypes WHERE description COLLATE NOCASE = ? COLLATE UNICODE")
        result = puller.pull((item_name,))
        if not result:
            raise ItemTypeNotFoundError(f'Item type with name = {item_name} does not exist')
        
        item_name = self.retrieve_item_type_by_id(result[0][0])
        
        return item_name, starting_index


class ItemTypeNotFoundError(Exception): ...