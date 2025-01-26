import asyncio
from pycomo import (
    ModelRegistry, ModelConfig, AzureConfig,
    OpenAIModel, AnthropicModel, AzureOpenAIModel, DeepseekModel,
    OpenAIResponseHandler, AnthropicResponseHandler, TokenHandler
)

async def initialize_models():
    registry = ModelRegistry()
    token_handler = TokenHandler()
    openai_handler = OpenAIResponseHandler(token_handler)
    anthropic_handler = AnthropicResponseHandler(token_handler)

    # OpenAI GPT-4
    registry.register_model(
        config=ModelConfig(
            name="GPT-4",
            slug="gpt-4",
            engine="gpt-4",
            api_key="",
            rank=1,
            accept_image=True
        ),
        model_class=OpenAIModel,
        response_handler=openai_handler
    )

    # Claude 3 Opus
    registry.register_model(
        config=ModelConfig(
            name="Claude 3 Opus",
            slug="claude-3-opus",
            engine="",
            api_key="",
            rank=2,
            accept_image=True,
            max_tokens=4096
        ),
        model_class=AnthropicModel,
        response_handler=anthropic_handler
    )

    # Azure OpenAI GPT-4
    azure_config = AzureConfig(
        name="Azure GPT-4o",
        slug="azure-gpt4o",
        engine="gpt-4",
        api_key="",
        api_base="",
        deployment_name="gpt-4o",
        api_version="2024-08-01-preview",
        rank=3,
        accept_image=True,
    )
    
    registry.register_model(
        config=azure_config,  # Pass AzureConfig directly instead of ModelConfig
        model_class=AzureOpenAIModel,
        response_handler=openai_handler
    )

    # Deepseek Chat
    # registry.register_model(
    #     config=ModelConfig(
    #         name="Deepseek Chat",
    #         slug="deepseek-chat",
    #         engine="deepseek-chat",
    #         api_key="your-deepseek-key",
    #         base_url="https://api.deepseek.com",
    #         rank=4
    #     ),
    #     model_class=DeepseekModel,
    #     response_handler=openai_handler
    # )

    return registry

async def test_models():
    registry = await initialize_models()
    
    # Test messages
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Write a short poem about coding."}
    ]

    # Test each model
    # models = ["gpt-4", "claude-3-opus", "azure-gpt4", "deepseek-chat"]
    models = ["gpt-4", "azure-gpt4o", "claude-3-opus"]
    
    for model_slug in models:
        print(f"\n=== Testing {model_slug} ===")
        model = registry.get_model(model_slug)
        
        print("\nStreaming response:")
        async for chunk in await model.predict(messages, stream=True):
            print(chunk, end="")
            
        print("\n\nCompletion response:")
        response = await model.predict(messages, stream=False)
        print(response)
        
        # Get token usage
        token_handler = model.response_handler.token_handler
        usage = token_handler.get_usage()
        print(f"\nToken usage: {usage}")
        
        
if __name__ == "__main__":
    asyncio.run(test_models())

