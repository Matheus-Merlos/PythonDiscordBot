from commands.command import Command
from discord import Message

class Teste(Command):
    async def run(self, msg: Message):
        await msg.channel.send('Olá, mundo!')