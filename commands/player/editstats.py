from commands.command import Command
from discord import Message
import botutils
from commands.player.playerutils import *

class EditStat(Command):
    async def run(self, msg: Message, column, operation):
        msg_as_list = msg.content.split()
        
        player_id = botutils.get_id_from_mention(msg_as_list[1])
        if not player_id.isdigit():
            await msg.reply('Você não forneceu um player válido.')
            return
        
        if not player_exists(player_id):
            await msg.reply('Esse player não existe. Para cadastrá-lo, use o comando `;addplayer`')
            return
        
        quantity = msg_as_list[2]
        if column == 'xp':
                if operation == '+':
                    await check_update_and_alert_player(id, quantity, msg)
                elif operation == '-':
                    check_and_update_player(id, quantity)
        update_player_stat(player_id, quantity, column, operation)
        
        if operation == '+':
            operation_message = 'adicionado'
        else:
            operation_message = 'removido'
        
        await msg.reply(f'{column.upper()} {operation_message} com sucesso!')

class AddExp(EditStat):
    async def run(self, msg: Message):
        await super().run(msg, 'xp', '+')

class RemoveExp(EditStat):
    async def run(self, msg: Message):
        await super().run(msg, 'xp', '-')

class AddGold(EditStat):
    async def run(self, msg: Message):
        await super().run(msg, 'gold', '+')

class RemoveGold(EditStat):
    async def run(self, msg: Message):
        await super().run(msg, 'gold', '-')
