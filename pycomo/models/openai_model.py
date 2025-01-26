import openai
from typing import AsyncGenerator, Any, List, Dict
from .base import BaseModel

class OpenAIModel(BaseModel):
    def _initialize_client(self) -> None:
        # OpenAI doesn't need explicit client initialization
        pass

    async def predict(self, 
                     messages: List[Dict[str, Any]], 
                     stream: bool = False, 
                     **kwargs) -> AsyncGenerator[str, None] | str:
        response = await openai.ChatCompletion.acreate(
            api_key=self.config.api_key,
            model=self.config.engine,
            messages=messages,
            temperature=self.config.temperature,
            stream=stream,
            **kwargs
        )
        
        if stream:
            return self.response_handler.handle_stream(response)
        return self.response_handler.handle_completion(response)

    async def predict_completion(self, prompt: str, **kwargs) -> str:
        messages = [{"role": "user", "content": prompt}]
        response = await openai.ChatCompletion.acreate(
            api_key=self.config.api_key,
            model=self.config.engine,
            messages=messages,
            temperature=self.config.temperature,
            **kwargs
        )
        return self.response_handler.handle_completion(response)