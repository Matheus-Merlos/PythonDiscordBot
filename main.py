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
from commands.player.stackeditstats import *
from commands.inventory.inventory import Inventory
from commands.objectives.objectivetype import *
from commands.objectives.addobjective import AddObjective
from commands.objectives.objectives import Objectives
from commands.objectives.completedobjective import CompletedObjective
from commands.shop.buy import Buy
from commands.items.use import Use
from commands.shop.give import Give
from commands.adm.resetplayer import ResetPlayer
from commands.adm.novagen import NovaGen
from commands.adm.roles import Teste

PATH = Path(__file__).parent

class Client(discord.Client):
    def __init__(self, *, intents: Intents, **options: Any) -> None:
        super().__init__(intents=intents, **options)
        self.commands = dict[str, Command]()
    
    async def on_ready(self):
        print('Conectado ao servidor com sucesso!')
    
    async def on_message(self, message: Message):
        for prefix, command in self.commands.items():
            if message.content.lower().startswith(prefix):
                await command.run(message)
                return
            
        if message.content.startswith(';'):
            await message.reply('Desculpa, mas esse comando não existe!')
    
    def add_command(self, command: Command):
        self.commands[command.prefix] = command
        
    
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

dotenv.load_dotenv(PATH / '.env')

client = Client(intents=intents)

client.add_command(Turnos('Turnos', ';turnos', ';turnos <@ de quem vai participar>', 'Gera uma mensagem contendo os turnos do rpg.'))
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

client.add_command(StackAddExp('Stack Adicionar XP', ';stackaddexp', ';stackaddexp <quantidade> <@menções>', 'Adiciona uma quantidade x de xp para todos os players que forem mencionados', client))
client.add_command(StackRemoveExp('Stack Remover XP', ';stackremoveexp', ';stackremoveexp <quantidade> <@menções>', 'Remove uma quantidade x de xp para todos os players que forem mencionados', client))
client.add_command(StackAddGold('Stack Adicionar Gold', ';stackaddgold', ';stackaddgold <quantidade> <@menções>', 'Adiciona uma quantidade x de gold para todos os players que forem mencionados', client))
client.add_command(StackRemoveGold('Stack Remover Gold', ';stackremovegold', ';stackremovegold <quantidade> <@menções>', 'Remove uma quantidade x de gold para todos os players que forem mencionados', client))

client.add_command(Inventory('Inventário', ';inv', ';inv <@player(opcional)>', 'Mostra o inventário seu, ou do player que você marcar', client))

client.add_command(AddObjectiveType('Adicionar tipo de objetivo', ';addobjectivetype', ';addobjectivetype <Nome do tipo>', 'Comando para adicionar tipos de objetivos, podendo ser utilizado apenas por administradores.'))
client.add_command(ObjectiveType('Tipos de Objetivos', ';objectivetypes', ';objectivetypes', 'Mostra os tipos de objetivos que tem no servidor'))

client.add_command(AddObjective('Adicionar Objetivo', ';addobjective', ';addobjective <nome do objetivo> <xp ganho> <tipo(id ou nome)> <gold> <descrição>', 'Adiciona um novo objetivo.'))
client.add_command(Objectives('Objetivos', ';objectives', ';objectives', 'Mostra todos os objetivos cadastrados no servidor.', client))

client.add_command(CompletedObjective('Completou Objetivo', ';completedobjective', ';completedobjective <@menção> <nome objetivo>', 'adiciona o xp e o gold do objetivo que a pessoa concluiu.'))

client.add_command(Buy('Comprar', ';buy', ';buy <Nome do Item> <quantidade(opcional)>', 'Compra um item da loja e adiciona a seu inventário!'))
client.add_command(Use('Usar Item', ';use', ';use <nome do item>', 'Usa o item específicado 1 vez'))
client.add_command(Give('Dar item', ';give', ';give <@menção> <nome do item> <quantidade(opcional)>', 'Dá o item especificado ao player', client))

client.add_command(ResetPlayer('Resetar Player', ';resetplayer', ';resetplayer <@menção>', 'Tira TUDO de um player, ele deixa-o só com 1000 de gold (comando apenas para administradores)'))
client.add_command(NovaGen('Nova gen', ';novagen', ';novagen', '`NOW I AM BECOME DEATH, DESTROYER OF WORLDS`', client))

client.add_command(Help('Ajuda', ';help', ';help', 'Comando de ajuda do bot, mostra toda a documentação e como utilizar', list(client.commands.values()), client))

client.run(os.getenv('TOKEN'))