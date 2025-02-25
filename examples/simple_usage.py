import asyncio
from pycomo.facade import ComoFacade

async def main():
    # Initialize the facade
    como = ComoFacade()
    
    # Configure providers with API keys
    como.configure_provider(
        provider="openai",
        api_key="your-openai-key"
    )
    
    como.configure_provider(
        provider="anthropic",
        api_key="your-anthropic-key"
    )
    
    # Get completion from a specific model
    result = await como.get_completion(
        model_slug="gpt-4",
        prompt="Explain quantum computing in simple terms"
    )
    
    # Access response and usage statistics
    print("Response:", result["response"])
    print("Usage:", result["usage"])
    
    # List available models
    available_models = como.list_available_models()
    print("Available models:", available_models)

if __name__ == "__main__":
    asyncio.run(main())
