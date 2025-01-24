from typing import Optional
from .handlers import ResponseHandler, OpenAIResponseHandler, ClaudeResponseHandler
from .models import TokenUsageTracker

class ResponseHandlerFactory:
    @staticmethod
    def create_handler(model_name: str, token_tracker: TokenUsageTracker) -> ResponseHandler:
        if any(name in model_name.lower() for name in ["openai", "gpt", "o1", "deepseek"]):
            return OpenAIResponseHandler(token_tracker)
        elif "claude" in model_name.lower():
            return ClaudeResponseHandler(token_tracker)
        else:
            raise ValueError(f"Unsupported model: {model_name}")