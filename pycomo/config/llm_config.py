from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class LLMProviderConfig:
    api_key: str
    base_url: Optional[str] = None
    organization_id: Optional[str] = None

class LLMConfigurationManager:
    _instance = None
    _provider_configs: Dict[str, LLMProviderConfig] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMConfigurationManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def configure_provider(cls, provider: str, config: LLMProviderConfig) -> None:
        """Configure a provider with its API keys and settings"""
        cls._provider_configs[provider] = config

    @classmethod
    def get_provider_config(cls, provider: str) -> Optional[LLMProviderConfig]:
        """Get configuration for a specific provider"""
        return cls._provider_configs.get(provider)

    @classmethod
    def is_provider_configured(cls, provider: str) -> bool:
        """Check if a provider is configured"""
        return provider in cls._provider_configs
