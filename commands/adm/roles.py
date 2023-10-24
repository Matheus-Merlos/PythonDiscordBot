from discord import Message
from commands.command import Command

class Teste(Command):
    async def run(self, msg: Message):
        print(msg.content.split())