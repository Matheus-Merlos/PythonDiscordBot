from discord import Message
from commands.command import Command
import discord
from dbhelper import Comitter
import botutils
from commands.player.playerutils import player_exists
import asyncio
from pathlib import Path

QUERY_PATH = Path(__file__).parent.parent.parent / 'queries/novagen.sql'

class NovaGen(Command):
    def __init__(self, name, prefix, syntax, description, client) -> None:
        super().__init__(name, prefix, syntax, description)
        self.client = client
    
    async def run(self, msg: Message):
        if not msg.author.guild_permissions.administrator:
            await msg.reply('Você não possui permissões de `administrador` para executar este comando.')
            return
        
        message = await msg.reply('Atenção: isso irá apagar o inventário de tudo e todos, deixando apenas 1000 de gold para cada, você tem certeza disso?')
        await message.add_reaction('✅')
        await message.add_reaction('❌')
            
        def check(reaction, user):
                return user == msg.author and str(reaction.emoji) in ['✅', '❌']
            
            
        while True:
            try:
            #Fica verificando as reações, para saber se ele vai para frente ou para trás, isso dura por 60 segudos, após isso ele para de responder
                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=60.0)

                if str(reaction.emoji) == '✅' and user == msg.author:
                    with Comitter(botutils.DB_PATH, QUERY_PATH) as comm:
                        comm.commit(many=True)
                    
                    await msg.reply('INVENTÁRIO DE TODO MUNDO ZERADO!')
                    
                elif str(reaction.emoji) == '❌' and user == msg.author:
                    await message.delete()
                    break

            except asyncio.TimeoutError:
                break