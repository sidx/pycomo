"""
PyComo - Python LLM Client Library

A simple and efficient Python library for interacting with various Large Language Models (LLMs)
including OpenAI, Anthropic, and Azure OpenAI.
"""

from .facade import ComoFacade
from .config.llm_config import LLMProviderConfig
from .registry import ModelRegistry

__version__ = "0.1.0"
__author__ = "Sidharth Nair"
__email__ = "sidharth.xtb@gmail.com"

__all__ = [
    "ComoFacade",
    "LLMProviderConfig",
    "ModelRegistry",
]