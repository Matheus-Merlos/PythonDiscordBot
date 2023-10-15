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

client.run(os.getenv('TOKEN'))
