from dataclasses import dataclass
from typing import Optional

@dataclass
class ModelConfig:
    name: str
    slug: str
    engine: str
    api_key: str
    base_url: Optional[str] = None
    icon: str = ""
    enabled: bool = True
    rank: int = 10000
    accept_image: bool = False
    max_tokens: int = 4096
    temperature: float = 0.1

@dataclass
class AzureConfig:
    api_key: str
    api_base: str
    deployment_name: str
    api_version: str
    name: str
    slug: str
    engine: str
    api_type: str = 'azure'
    rank: int = 10000
    accept_image: bool = True
    temperature: float = 0.1
    max_tokens: int = 4096