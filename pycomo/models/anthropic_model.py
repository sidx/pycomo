from anthropic import AsyncAnthropic
from typing import AsyncGenerator, Any, List, Dict
from pycomo.models.base import BaseModel

class AnthropicModel(BaseModel):
    def _initialize_client(self) -> None:
        self.client = AsyncAnthropic(api_key=self.config.api_key)

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

    async def predict(self, 
                     messages: List[Dict[str, Any]], 
                     stream: bool = False, 
                     **kwargs) -> AsyncGenerator[str, None] | str:
        system_message, consolidated_messages = self.process_messages(messages)
        
        if stream:
            response = await self.client.messages.stream(
                max_tokens=self.config.max_tokens,
                messages=consolidated_messages,
                model=self.config.engine,
                system=system_message,
                **kwargs
            ).__aenter__()
        else:
            response = await self.client.messages.create(
                max_tokens=self.config.max_tokens,
                messages=consolidated_messages,
                model=self.config.engine,
                system=system_message,
                **kwargs
            )

        return self.response_handler.handle_stream(response) if stream else \
               self.response_handler.handle_completion(response)

    async def predict_completion(self, prompt: str, **kwargs) -> str:
        messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
        response = await self.client.messages.create(
            max_tokens=self.config.max_tokens,
            messages=messages,
            model=self.config.engine,
            **kwargs
        )
        return self.response_handler.handle_completion(response)