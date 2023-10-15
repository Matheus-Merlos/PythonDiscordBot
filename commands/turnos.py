from command import Command
from discord import Message
import random

class Turnos(Command):
    async def run(self, msg: Message):
        rolls = dict()
        msg = msg.content.split()[1:]
        for member in len(msg):
            rolls[member] = random.randint(1, 20)
        
        sorted_rolls = dict(sorted(rolls.items(), key=lambda item: item[1]))
        
        message = """--TURNOS--\n\n"""
        for member, roll in sorted_rolls.items():
            message += f"\n{member} - {roll}"
            
        await msg.channel.send(message)
        