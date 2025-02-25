from typing import Dict, Optional, Any
from .config.llm_config import LLMConfigurationManager, LLMProviderConfig
from .registry import ModelRegistry
from .handlers.response_handler import ResponseHandler
from .handlers.token_handler import TokenHandler

class ComoFacade:
    def __init__(self):
        self.config_manager = LLMConfigurationManager()
        self.model_registry = ModelRegistry()
        self.token_handler = TokenHandler()

    def configure_provider(self, 
                         provider: str, 
                         api_key: str, 
                         base_url: Optional[str] = None,
                         organization_id: Optional[str] = None) -> None:
        """
        Configure a provider with necessary credentials
        
        Args:
            provider: Provider name (e.g., 'openai', 'anthropic', 'azure')
            api_key: API key for the provider
            base_url: Optional base URL for API endpoint
            organization_id: Optional organization ID
        """
        config = LLMProviderConfig(
            api_key=api_key,
            base_url=base_url,
            organization_id=organization_id
        )
        self.config_manager.configure_provider(provider, config)

    async def get_completion(self, 
                           model_slug: str, 
                           prompt: str,
                           **kwargs) -> Dict[str, Any]:
        """
        Get completion from a specific model
        
        Args:
            model_slug: The slug/identifier for the model
            prompt: The prompt to send
            **kwargs: Additional model-specific parameters
            
        Returns:
            Dict containing response and usage statistics
        """
        model = self.model_registry.get_model(model_slug)
        if not model:
            raise ValueError(f"Model {model_slug} not found")
            
        response = await model.generate(prompt, **kwargs)
        usage = self.token_handler.get_usage(model_slug)
        
        return {
            "response": response,
            "usage": usage
        }

    def list_available_models(self) -> list:
        """List all available and configured models"""
        return self.model_registry.list_models()
