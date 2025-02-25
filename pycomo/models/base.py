from abc import ABC, abstractmethod
from typing import AsyncGenerator, Any, List, Dict
from ..clients.base_client import BaseClientHandler
from ..handlers.response_handler import ResponseHandler
from ..config.model_config import ModelConfig

class BaseModel(ABC):
    def __init__(self, config: ModelConfig, response_handler: ResponseHandler):
        self.config = config
        self.response_handler = response_handler
        self._initialize_client()

    @abstractmethod
    def _initialize_client(self) -> None:
        """Initialize the model-specific client"""
        pass

    @abstractmethod
    async def predict(self, 
                     messages: List[Dict[str, Any]], 
                     stream: bool = False, 
                     **kwargs) -> AsyncGenerator[str, None] | str:
        """Make a prediction using the model"""
        pass

    @abstractmethod
    async def predict_completion(self, 
                               prompt: str, 
                               **kwargs) -> str:
        """Make a completion-style prediction"""
        pass