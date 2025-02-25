from typing import List, Dict, Any
from .base_client import BaseClientHandler
import openai

class OpenAIClientHandler(BaseClientHandler):
    def __init__(self, config):
        self.config = config

    def process_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return messages

    async def create_chat_completion(self, 
                                   messages: List[Dict[str, Any]], 
                                   stream: bool = False,
                                   **kwargs) -> Any:
        completion_kwargs = {
            "api_key": self.config.api_key,
            "model": self.config.engine,
            "messages": messages,
            "temperature": self.config.temperature,
            "stream": stream,
            **kwargs
        }
        return await openai.ChatCompletion.acreate(**completion_kwargs)
