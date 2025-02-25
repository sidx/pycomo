from typing import List, Dict, Any
from .base_client import BaseClientHandler
from anthropic import AsyncAnthropic

class AnthropicClientHandler(BaseClientHandler):
    def __init__(self, config):
        self.config = config
        self.client = AsyncAnthropic(api_key=config.api_key)

    def process_messages(self, messages: List[Dict[str, Any]]) -> tuple[str, list]:
        system_message = ""
        filtered_messages = []

        # Extract system message and filter messages
        for msg in messages:
            if msg['role'] == 'system':
                system_message += msg['content'][0]['text'] if isinstance(msg['content'], list) else msg['content']
            else:
                filtered_messages.append({'role': msg['role'], 'content': msg['content']})

        # Consolidate consecutive user messages
        consolidated_messages = []
        current_user_message = []

        for msg in filtered_messages:
            if msg['role'] == 'user':
                if isinstance(msg['content'], list):
                    current_user_message.extend(msg['content'])
                else:
                    current_user_message.extend([{"type": "text", "text": msg['content']}])
            else:
                if current_user_message:
                    consolidated_messages.append({'role': 'user', 'content': current_user_message})
                    current_user_message = []
                consolidated_messages.append(msg)

        # Add any remaining user message
        if current_user_message:
            consolidated_messages.append({'role': 'user', 'content': current_user_message})

        return system_message, consolidated_messages


    async def create_chat_completion(self, 
                                   messages: List[Dict[str, Any]], 
                                   stream: bool = False,
                                   **kwargs) -> Any:
        system_message, consolidated_messages = self.process_messages(messages)
        
        if stream:
            return await self.client.messages.stream(
                max_tokens=self.config.max_tokens,
                messages=consolidated_messages,
                model=self.config.engine,
                system=system_message,
                **kwargs
            ).__aenter__()
        
        return await self.client.messages.create(
            max_tokens=self.config.max_tokens,
            messages=consolidated_messages,
            model=self.config.engine,
            system=system_message,
            **kwargs
        )
