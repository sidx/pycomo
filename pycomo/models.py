from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any, AsyncGenerator, Union

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

class TokenUsageTracker(ABC):
    @abstractmethod
    def update_usage(self, usage: TokenUsage) -> None:
        pass

    @abstractmethod
    def get_usage(self) -> TokenUsage:
        pass