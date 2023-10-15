from abc import ABC, abstractmethod
from discord import Message

class Command(ABC):
    def __init__(self, name, prefix, syntax, description) -> None:
        super().__init__()
        self.name = name
        self.prefix = prefix
        self.syntax = syntax
        self.description = description
    
    @abstractmethod
    async def run(self, msg: Message): ...