from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0

class TokenHandler:
    def __init__(self):
        self.reset_usage()

    def reset_usage(self):
        self.usage = TokenUsage()

    def update_usage(self, usage_data: Dict[str, Any]):
        if isinstance(usage_data, dict):
            self.usage.input_tokens += usage_data.get('prompt_tokens', 0)
            self.usage.output_tokens += usage_data.get('completion_tokens', 0)
            self.usage.total_tokens += usage_data.get('total_tokens', 0)
        else:
            # Handle Anthropic-style usage
            self.usage.input_tokens += getattr(usage_data, 'input_tokens', 0)
            self.usage.output_tokens += getattr(usage_data, 'output_tokens', 0)
            self.usage.cache_creation_input_tokens += getattr(usage_data, 'cache_creation_input_tokens', 0)
            self.usage.cache_read_input_tokens += getattr(usage_data, 'cache_read_input_tokens', 0)
            self.usage.total_tokens = (
                self.usage.input_tokens + 
                self.usage.output_tokens + 
                self.usage.cache_creation_input_tokens + 
                self.usage.cache_read_input_tokens
            )

    def get_usage(self) -> TokenUsage:
        return self.usage