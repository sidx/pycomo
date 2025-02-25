import asyncio
from pycomo import (
    ModelDelegator, ModelConfig, AzureConfig,
    OpenAIClientHandler, AnthropicClientHandler, AzureClientHandler,
    OpenAIResponseHandler, AnthropicResponseHandler, TokenHandler
)

async def initialize_delegator():
    delegator = ModelDelegator()
    token_handler = TokenHandler()
    openai_handler = OpenAIResponseHandler(token_handler)
    anthropic_handler = AnthropicResponseHandler(token_handler)

    # OpenAI GPT-4
    delegator.register_model(
        config=ModelConfig(
            name="DeepSeek",
            slug="deepseek-chat",
            engine="deepseek-chat",
            modbase_url="https://api.deepseek.com",
            api_key="sk-6507437889e74c158f6bf88c558a2c38",
            rank=1,
            accept_image=True
        ),
        client_handler=OpenAIClientHandler,
        response_handler=openai_handler
    )

    # Claude 3 Opus
    # delegator.register_model(
    #     config=ModelConfig(
    #         name="Claude 3 Opus",
    #         slug="claude-3-opus",
    #         engine="",
    #         api_key="",
    #         rank=2,
    #         accept_image=True,
    #         max_tokens=4096
    #     ),
    #     client_handler=AnthropicClientHandler,
    #     response_handler=anthropic_handler
    # )

    # # Azure OpenAI GPT-4
    # azure_config = AzureConfig(
    #     name="Azure GPT-4o",
    #     slug="azure-gpt4o",
    #     engine="gpt-4",
    #     api_key="",
    #     api_base="",
    #     deployment_name="gpt-4o",
    #     api_version="2024-08-01-preview",
    #     rank=3,
    #     accept_image=True,
    # )
    
    # delegator.register_model(
    #     config=azure_config,
    #     client_handler=AzureClientHandler,
    #     response_handler=openai_handler
    # )

    return delegator

async def test_models():
    delegator = await initialize_delegator()
    
    # Test messages
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Write a short poem about coding."}
    ]

    # Test each model
    models = ["gpt-4", "azure-gpt4o", "claude-3-opus"]
    
    for model_slug in models:
        print(f"\n=== Testing {model_slug} ===")
        
        print("\nStreaming response:")
        async for chunk in await delegator.predict(model_slug, messages, stream=True):
            print(chunk, end="")
            
        print("\n\nCompletion response:")
        response = await delegator.predict(model_slug, messages)
        print(response)
        
        # Get token usage
        usage = delegator.get_token_usage(model_slug)
        print(f"\nToken usage: {usage}")

if __name__ == "__main__":
    asyncio.run(test_models())

