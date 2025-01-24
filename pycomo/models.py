from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any, AsyncGenerator, Union
from .config_schema import ModelConfigSchema, ConfigManager

@dataclass
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0

@dataclass
class ModelConfig:
    name: str
    slug: str
    engine: str
    api_key: str
    icon: str = ""
    enabled: bool = False
    rank: int = 10000
    accept_image: bool = False
    max_tokens: int = 4096
    temperature: float = 0.1

    @classmethod
    def from_config_schema(cls, schema: ModelConfigSchema) -> 'ModelConfig':
        return cls(
            name=schema.name,
            slug=schema.slug,
            engine=schema.engine,
            api_key=schema.api_key,
            icon=schema.icon,
            enabled=schema.enabled,
            rank=schema.rank,
            accept_image=schema.accept_image,
            max_tokens=schema.max_tokens,
            temperature=schema.temperature
        )

class TokenUsageTracker(ABC):
    @abstractmethod
    def update_usage(self, usage: TokenUsage) -> None:
        pass

    @abstractmethod
    def get_usage(self) -> TokenUsage:
        pass