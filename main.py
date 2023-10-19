from typing import Any
import discord
from discord.flags import Intents
import dotenv
import os
from pathlib import Path
from discord import Message
from commands.command import Command
from commands.turnos import Turnos
from commands.help import Help
from commands.rolls import Roll
from commands.items.itemtypes import *
from commands.items.additem import *
from commands.items.item import Item
from commands.shop.shop import Shop
from commands.items.edititem import EditItem
from commands.player.ranks import *
from commands.player.addplayer import AddPlayer
from commands.player.editstats import *


PATH = Path(__file__).parent

class Client(discord.Client):
    def __init__(self, *, intents: Intents, **options: Any) -> None:
        super().__init__(intents=intents, **options)
        self.commands = dict[str, Command]()
    
    async def on_ready(self):
        print('Conectado ao servidor com sucesso!')
    
    async def on_message(self, message: Message):
        for prefix, command in self.commands.items():
            if message.content.startswith(prefix):
                await command.run(message)
                return
            
        if message.content.startswith(';'):
            await message.channel.send('Desculpa, mas esse comando não existe!')
    
    def add_command(self, command: Command):
        self.commands[command.prefix] = command
        
    
intents = discord.Intents.default()
intents.message_content = True

dotenv.load_dotenv(PATH / '.env')

client = Client(intents=intents)

client.add_command(Turnos('Turnos', ';turnos', ';turnos <@ de quem vai participar>', 'Gera uma mensagem contendo os turnos do rpg.'))
client.add_command(Help('Ajuda', ';help', ';help', 'Comando de ajuda do bot, mostra toda a documentação e como utilizar', client.commands.values()))
client.add_command(Roll('Roll', ';roll', ';roll <dado(opcional)> <modificador(opcional)>', 'Rola um, ou vários dados para você, e mostra o resultado, sendo o principal comando do RPG'))

client.add_command(AddItemType('Adicionar Tipo de Item', ';additemtype', ';additemtype <Nome>', 'Comando para adicionar novos tipos de item, requer permissão de "administrador"'))
client.add_command(ItemTypes('Tipos de Item', ';itemtypes', ';itemtypes', 'Mostra os tipos de itens que foram registrados'))

client.add_command(AddItem('Adicionar Item', ';additem', ';additem <nome do item> <preço> <tipo> <durabilidade> <descrição>', 'Cria um novo item para ser usado, o tipo do item pode ser especificado tanto em nome, quanto em ID, para mais informações sobre isso apenas digite ";itemtypes"'))
client.add_command(Item('Item', ';item', ';item <nome do item>', 'Ver os detalhes de um item, como nome, preço, durabilidade, tipo e descrição'))

#TODO
#client.add_command(EditItem('Editar item', ';edititem', ';edititem <campo> <nome do item(Entre aspas)> <informação nova>', 'Alt
# era a informação de um item.'))

client.add_command(Shop('Shop', ';shop', ';shop <tipo de item(opcional)>', 'Mostra todos os itens criados e seus respectivos preços', client))

client.add_command(AddRank('Adicionar Rank', ';addrank', ';addrank <nome> <XP necessário> <n° de Habilidades ganhas> <n° de Atributos Ganhos>', 'Cria um novo rank, podendo ser utilizado apenas por administradores'))
client.add_command(Ranks('Ranks', ';ranks', ';ranks', 'Mostra todos os ranks adicionados no servidor'))

client.add_command(AddPlayer('Adicionar Jogador', ';addplayer', ';addplayer <@Menção> <Nome do personagem> <XP (opcional)> <Gold (opcional>)', 'Adiciona um jogador para o server, comando restrito apenas para administradores'))
client.add_command(AddExp('Adicionar XP', ';addexp', ';addexp <@menção do player> <quantidade>', 'Adiciona a quantidade de xp descrita do inventário do player'))
client.add_command(RemoveExp('Remover XP', ';removeexp', ';removeexp <@menção do player> <quantidade>', 'Remove a quantidade de xp descrita do inventário do player'))
client.add_command(AddGold('Adicionar Gold', ';addgold', ';addgold <@menção do player> <quantidade>', 'Adiciona a quantidade de gold descrita do inventário do player'))
client.add_command(RemoveGold('Remover Gold', ';removegold', ';removegold <@menção do player> <quantidade>', 'Remove a quantidade de gold descrita do inventário do player'))


client.run(os.getenv('TOKEN'))