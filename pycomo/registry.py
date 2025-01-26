from typing import Dict, Optional
from .models.base import BaseModel
from .config.model_config import ModelConfig
from .handlers.response_handler import ResponseHandler

class ModelRegistry:
    _instance = None
    _models: Dict[str, BaseModel] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelRegistry, cls).__new__(cls)
        return cls._instance

    @classmethod
    def register_model(cls, 
                      config: ModelConfig, 
                      model_class: type[BaseModel],
                      response_handler: ResponseHandler) -> None:
        model = model_class(config=config, response_handler=response_handler)
        cls._models[config.slug] = model

    @classmethod
    def get_model(cls, slug: str) -> Optional[BaseModel]:
        return cls._models.get(slug)

    @classmethod
    def list_models(cls) -> list:
        return [
            {
                "name": model.config.name,
                "slug": model.config.slug,
                "enabled": model.config.enabled,
                "rank": model.config.rank,
                "accept_image": model.config.accept_image
            }
            for model in cls._models.values()
            if model.config.enabled
        ]