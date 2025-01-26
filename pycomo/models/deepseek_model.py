import openai
from typing import AsyncGenerator, Any, List, Dict
from .base import BaseModel

class DeepseekModel(BaseModel):
    def _initialize_client(self) -> None:
        # Deepseek uses OpenAI-compatible API
        pass

    async def predict(self, 
                     messages: List[Dict[str, Any]], 
                     stream: bool = False, 
                     **kwargs) -> AsyncGenerator[str, None] | str:
        response = await openai.ChatCompletion.acreate(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            model=self.config.engine,
            messages=messages,
            temperature=self.config.temperature,
            stream=stream,
            **kwargs
        )

        return self.response_handler.handle_stream(response) if stream else \
               self.response_handler.handle_completion(response)

    async def predict_completion(self, prompt: str, **kwargs) -> str:
        messages = [{"role": "user", "content": prompt}]
        response = await openai.ChatCompletion.acreate(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            model=self.config.engine,
            messages=messages,
            temperature=self.config.temperature,
            **kwargs
        )
        return self.response_handler.handle_completion(response)