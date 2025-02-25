from abc import ABC, abstractmethod
from typing import AsyncGenerator, Any, List, Dict

class BaseClientHandler(ABC):
    @abstractmethod
    async def create_chat_completion(self, 
                                   messages: List[Dict[str, Any]], 
                                   stream: bool = False,
                                   **kwargs) -> Any:
        pass

    @abstractmethod
    def process_messages(self, messages: List[Dict[str, Any]]) -> Any:
        pass
