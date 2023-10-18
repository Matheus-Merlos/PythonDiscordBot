from commands.command import Command
from discord import Message
import botutils
from dbhelper import *
from unidecode import unidecode

class EditItem(Command):
    async def run(self, msg: Message):
        options = {
            'nome': 'nome',
            'name': 'nome',
            'price': 'price',
            'preco': 'price',
            'durability': 'durability',
            'durabilidade': 'durability',
            'description': 'description',
            'descricao': 'descricao',
            'type': 'id_type',
            'itemtype': 'id_type',
            'tipo': 'id_type',
            'tipoitem': 'id_type'
        }
        
        msg_as_list = msg.content.split()
        if(msg_as_list[1] not in options):
            await msg.reply('O que você está tentando alterar não é uma informação válida.')
            return
        
        item_name, index = get_item_name(msg_as_list)
        print(item_name, index)

        column = options[msg_as_list[1]]
        editor = ColumnEditor(botutils.DB_PATH)
        editor.set_data_update_query('UPDATE item SET ?')
        
        
def get_item_name(msg_as_list: list):
    has = False
    texto = []

    for item in msg_as_list:
        if '"' in item:
            if not has:
                has = True
                texto.append(item.strip('"'))
            else:
                texto[-1] += ' ' + item.strip('"')
                has = False
        elif has:
            texto[-1] += ' ' + item

    return " ".join(texto), msg_as_list.index(texto[-1])