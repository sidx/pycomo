import openai
from typing import AsyncGenerator, Any, List, Dict
from pycomo.models.base import BaseModel
from pycomo.config.model_config import AzureConfig
from pycomo.handlers.response_handler import ResponseHandler

class AzureOpenAIModel(BaseModel):
    def __init__(self, config: AzureConfig, response_handler: ResponseHandler):
        self.azure_config = config
        super().__init__(config=config, response_handler=response_handler)

    def _initialize_client(self) -> None:
        # Azure OpenAI uses the same client as OpenAI
        pass

    async def predict(self, 
                     messages: List[Dict[str, Any]], 
                     stream: bool = False, 
                     **kwargs) -> AsyncGenerator[str, None] | str:
        response = await openai.ChatCompletion.acreate(
            api_key=self.azure_config.api_key,
            api_base=self.azure_config.api_base,
            api_type=self.azure_config.api_type,
            api_version=self.azure_config.api_version,
            engine=self.azure_config.deployment_name,
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
            api_key=self.azure_config.api_key,
            api_base=self.azure_config.api_base,
            api_type=self.azure_config.api_type,
            api_version=self.azure_config.api_version,
            engine=self.azure_config.deployment_name,
            messages=messages,
            temperature=self.config.temperature,
            **kwargs
        )
        return self.response_handler.handle_completion(response)