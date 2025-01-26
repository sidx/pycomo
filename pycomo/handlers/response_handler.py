from abc import ABC, abstractmethod
from typing import AsyncGenerator, Any, Dict
from .token_handler import TokenHandler


class ResponseHandler(ABC):
    def __init__(self, token_handler: TokenHandler):
        self.token_handler = token_handler

    @abstractmethod
    async def handle_stream(self, stream: Any) -> AsyncGenerator[str, None]:
        """Handle streaming responses"""
        pass

    @abstractmethod
    def handle_completion(self, response: Any) -> str:
        """Handle completion-style responses"""
        pass


class OpenAIResponseHandler(ResponseHandler):
    async def handle_stream(self, stream: Any) -> AsyncGenerator[str, None]:
        async for message in stream:
            if hasattr(message, "usage"):
                self.token_handler.update_usage(message.usage)
            if message.choices and message.choices[0].delta:
                yield message.choices[0].delta.get('content', '')

    def handle_completion(self, response: Any) -> str:
        if hasattr(response, "usage"):
            self.token_handler.update_usage(response.usage)
        return response['choices'][0]["message"]["content"]


class AnthropicResponseHandler(ResponseHandler):
    async def handle_stream(self, stream: Any) -> AsyncGenerator[str, None]:
        async for event in stream:
            if event.type == "text":
                yield event.text
            elif event.type == "message_stop":
                self.token_handler.update_usage(stream.current_message_snapshot.usage)
    
    def handle_completion(self, response: Any) -> str:
        if hasattr(response, "usage"):
            self.token_handler.update_usage(response.usage)
        return response.content[0].text