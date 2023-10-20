from commands.command import Command
from discord import Message
import botutils
from commands.player.playerutils import *
import discord

class StackEditStat(Command):
    def __init__(self, name, prefix, syntax, description, client) -> None:
        super().__init__(name, prefix, syntax, description)
        self.client = client
    
    async def run(self, msg: Message, column, operation):
        msg_as_list = msg.content.split()
        
        #Checa se a quantidade é valida
        quantity = msg_as_list[1]
        if not quantity.isdigit():
            await msg.reply('Você não forneceu uma quantidade válida. Lembre-se que é primeiro a quantidade e depois os players.')
            return
        
        #Pega todos os ids mencionados
        ids = [botutils.get_id_from_mention(id) for id in msg_as_list[2:]]
        
        #Adiciona os itens para cada id
        for id in ids:
            if column == 'xp':
                if operation == '+':
                    await check_update_and_alert_player(id, quantity, msg)
                elif operation == '-':
                    check_and_update_player(id, quantity)
            
            update_player_stat(id, quantity, column, operation)
            
            if operation == '+':
                operation_message = 'adicionado'
            else:
                operation_message = 'removido'
            
            player_name = self.client.get_user(int(id)).display_name
            
            await msg.reply(f'{column.upper()} {operation_message} com sucesso para **{player_name}**')

class StackAddExp(StackEditStat):
    async def run(self, msg: Message):
        return await super().run(msg, 'xp', '+')

class StackRemoveExp(StackEditStat):
    async def run(self, msg: Message):
        return await super().run(msg, 'xp', '-')

class StackAddGold(StackEditStat):
    async def run(self, msg: Message):
        return await super().run(msg, 'gold', '+')

class StackRemoveGold(StackEditStat):
    async def run(self, msg: Message):
        return await super().run(msg, 'gold', '-')