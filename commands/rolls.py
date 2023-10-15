from commands.command import Command
from discord import Message
import random

class Roll(Command):
    async def run(self, msg: Message):
        msg_as_list = msg.content.split()[1:]
        if len(msg_as_list) == 0:
            result = simpleroll(6)
            await RollMessage(6, result).send_message(msg)
        elif len(msg_as_list) == 1:
            result = simpleroll(int(msg_as_list[0]))
            await RollMessage(msg_as_list[0], result).send_message(msg)
        else:
            dice = int(msg_as_list[0])
            result = simpleroll(dice)

            modifier = msg_as_list[1]
            modifier_value = eval(modifier[1:])
            modifier_sign = '+' if modifier.startswith('+') else '-'
            final_result = eval(f'{result} {modifier_sign} {modifier_value}')
            
            await RollMessage(dice, result, True, modifier, final_result).send_message(msg)
            
                
class RollMessage:
    def __init__(self, dice:int, result:int, has_modifier: bool=False, modifier: str=0, final_result: int=0) -> None:
        self.dice = dice
        self.result = result
        self.has_modifier = has_modifier
        self.modifier = modifier
        self.final_result = final_result
        
    async def send_message(self, msg: Message):
        if not self.has_modifier:
            message = f':game_die: d{self.dice} = **{self.result}**'
        else:
            message = f':game_die: d{self.dice} = `{self.result}` **{self.modifier}** = `{self.final_result}`'
        
        await msg.reply(message)

def simpleroll(dice):
    return random.randint(1,dice)