from commands.command import Command
from discord import Message
import random
import botutils
from dbhelper import Puller

GET_CHAR_QUERY = botutils.QUERIES_FOLDER_PATH / 'get_char_name.sql'

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
                discord_id = botutils.get_id_from_mention(member)
                
                with Puller(botutils.DB_PATH, GET_CHAR_QUERY) as pull:
                    char_name = pull.pull((discord_id,))[0][0]
                first_char_name = char_name.split()[0]
                
                message += f"\n{first_char_name} - {roll}"
            
        await msg.channel.send(message)

