from commands.command import Command
from discord import Message
from dbhelper import Comitter

class AddItem(Command):
    async def run(self, msg: Message):
        print(self.get_item_name(msg.content.split()))
    
    @staticmethod
    def get_item_name(msg_as_list: list):
        del msg_as_list[0]
        item_name_list = list()
        for word in msg_as_list:
            wrd = str(word)
            if not wrd.isdigit():
                item_name_list.append(wrd)
            else:
                break
        
        item_name = " ".join(item_name_list)
        return item_name

        