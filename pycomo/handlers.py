from abc import ABC, abstractmethod
from typing import AsyncGenerator, Any, Dict, Optional

from .models import TokenUsage, TokenUsageTracker

class ResponseHandler(ABC):
    def __init__(self, token_tracker: TokenUsageTracker):
        self.token_tracker = token_tracker

    @abstractmethod
    async def handle_stream(self, stream: Any) -> AsyncGenerator[str, None]:
        pass

    @abstractmethod
    def handle_simple(self, response: Any) -> str:
        pass

    @abstractmethod
    def extract_token_usage(self, response: Any) -> TokenUsage:
        pass

class OpenAIResponseHandler(ResponseHandler):
    async def handle_stream(self, stream: Any) -> AsyncGenerator[str, None]:
        try:
            async for message in stream:
                if hasattr(message, "usage") and message.usage:
                    usage = TokenUsage(
                        input_tokens=message.usage['prompt_tokens'],
                        output_tokens=message.usage['completion_tokens'],
                        total_tokens=message.usage['total_tokens']
                    )
                    self.token_tracker.update_usage(usage)
                elif message.choices and message.choices[0].delta:
                    yield message.choices[0].delta.get('content', '')
        except Exception as e:
            # Handle error logging/reporting as needed
            yield ""

    def handle_simple(self, response: Any) -> str:
        try:
            usage = self.extract_token_usage(response)
            self.token_tracker.update_usage(usage)
            return response['choices'][0]["message"]["content"]
        except Exception as e:
            # Handle error logging/reporting as needed
            return ""

    def extract_token_usage(self, response: Any) -> TokenUsage:
        return TokenUsage(
            input_tokens=response.usage['prompt_tokens'],
            output_tokens=response.usage['completion_tokens'],
            total_tokens=response.usage['total_tokens']
        )

class ClaudeResponseHandler(ResponseHandler):
    async def handle_stream(self, stream: Any) -> AsyncGenerator[str, None]:
        try:
            async for event in stream:
                if event.type == "text":
                    yield event.text
                elif event.type == "message_stop":
                    usage = self.extract_token_usage(stream.current_message_snapshot)
                    self.token_tracker.update_usage(usage)
        except Exception as e:
            # Handle error logging/reporting as needed
            yield ""

    def handle_simple(self, response: Any) -> str:
        try:
            usage = self.extract_token_usage(response)
            self.token_tracker.update_usage(usage)
            return response.content[0].text
        except Exception as e:
            # Handle error logging/reporting as needed
            return ""

    def extract_token_usage(self, response: Any) -> TokenUsage:
        return TokenUsage(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            cache_creation_input_tokens=response.usage.cache_creation_input_tokens,
            cache_read_input_tokens=response.usage.cache_read_input_tokens,
            total_tokens=(
                response.usage.input_tokens + 
                response.usage.output_tokens + 
                response.usage.cache_creation_input_tokens + 
                response.usage.cache_read_input_tokens
            )
        )