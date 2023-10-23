from commands.command import Command
from discord import Message, Embed
import discord
from commands.shop.shop import show_embeds

class Help(Command):
    def __init__(self, name, prefix, syntax, description, command_list, client) -> None:
        super().__init__(name, prefix, syntax, description)
        self.command_list = command_list
        self.client = client
    
    async def run(self, msg: Message):
        separated_lists = list()
        for i in range(0, len(self.command_list), 7):
            sublist = self.command_list[i:i + 7]
            separated_lists.append(sublist)
            
        embeds = list()
        
        #Cria uma embed separada para cada mini-lista que foi criada anteriormente
        for index, sublist in enumerate(separated_lists, start=1):
            embed = Embed(title='Comandos do Bot')
            embed.set_footer(text=f'Página {index}/{len(separated_lists)}')
            
            for item in sublist:
                description = f'`{item.syntax}`\n{item.description}'
                embed.add_field(name=item.name, value=description, inline=False)
            embeds.append(embed)
        
        await show_embeds(embeds, msg, self.client)
        