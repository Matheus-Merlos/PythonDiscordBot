from commands.command import Command
from discord import Message
import discord

class Help(Command):
    def __init__(self, name, prefix, syntax, description, command_list) -> None:
        super().__init__(name, prefix, syntax, description)
        self.command_list = command_list
    
    async def run(self, msg: Message):
        embed = discord.Embed(title='Comandos do Bot')
        for comm in self.command_list:
            embed.add_field(name=comm.name, value=f'`{comm.syntax}`\n{comm.description}', inline=False)
        
        await msg.channel.send(embed=embed)
        