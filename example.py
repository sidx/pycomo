from pycomo.factory import ResponseHandlerFactory, TokenUsageTracker, TokenUsage

# Implement your token tracker
class YourTokenTracker(TokenUsageTracker):
    def update_usage(self, usage: TokenUsage) -> None:
        # Your implementation
        pass

    def get_usage(self) -> TokenUsage:
        # Your implementation
        pass

# Create handler
token_tracker = YourTokenTracker()
handler = ResponseHandlerFactory.create_handler("gpt-4", token_tracker)

async def main():
    # Handle streaming response
    async for chunk in handler.handle_stream(stream):
        print(chunk)

# Handle simple response
result = handler.handle_simple(response)