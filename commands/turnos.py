from commands.command import Command
from discord import Message
import random
import botutils

class Turnos(Command):
    async def run(self, msg: Message):
        #Rola um dado d20 para cada membro no mensagem
        rolls = dict()
        msg_as_list = msg.content.split()[1:]
        for member in msg_as_list:
            rolls[member] = random.randint(1, 20)
        
        #Organiza o dicionário em ordem decrescente
        sorted_rolls = dict(sorted(rolls.items(), key=lambda item: item[1], reverse=True))
        
        #Cria uma mensagem para enviar
        #Se for aliado: normal
        #Se for inimigo: negrito
        message = """--TURNOS--\n\n"""
        for member, roll in sorted_rolls.items():
            if not '@' in member:
                message += f"\n**{member} - {roll}**"
            else:
                message += f"\n{member} - {roll}"
                print(botutils.get_id_from_mention(member))
            
        await msg.channel.send(message)
        