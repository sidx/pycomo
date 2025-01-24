from typing import Dict, List, Optional
from dataclasses import dataclass
import json
from pathlib import Path
import os

@dataclass
class ModelConfigSchema:
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

    @classmethod
    def from_dict(cls, data: Dict) -> 'ModelConfigSchema':
        return cls(
            name=data.get('name', ''),
            slug=data.get('slug', ''),
            engine=data.get('engine', ''),
            api_key=data.get('api_key', ''),
            icon=data.get('icon', ''),
            enabled=data.get('enabled', False),
            rank=int(data.get('rank', 10000)),
            accept_image=data.get('accept_image', False),
            max_tokens=int(data.get('max_tokens', 4096)),
            temperature=float(data.get('temperature', 0.1))
        )

class ConfigManager:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.getenv('PYCOMO_CONFIG_PATH', 'config.json')
        self.models: Dict[str, ModelConfigSchema] = {}
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from file and environment variables"""
        # Load from file
        if Path(self.config_path).exists():
            with open(self.config_path) as f:
                config_data = json.load(f)
                if 'models' in config_data:
                    for model_data in config_data['models']:
                        model = ModelConfigSchema.from_dict(model_data)
                        self.models[model.slug] = model

        # Override with environment variables
        self._load_env_vars()

    def _load_env_vars(self) -> None:
        """Load configuration from environment variables"""
        env_prefix = 'PYCOMO_MODEL_'
        model_envs = {}

        # Group environment variables by model
        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                # Format: PYCOMO_MODEL_<slug>_<property>
                parts = key[len(env_prefix):].lower().split('_', 1)
                if len(parts) == 2:
                    model_slug, prop = parts
                    if model_slug not in model_envs:
                        model_envs[model_slug] = {}
                    model_envs[model_slug][prop] = value

        # Update or create models from environment variables
        for slug, props in model_envs.items():
            if slug in self.models:
                # Update existing model
                for prop, value in props.items():
                    setattr(self.models[slug], prop, value)
            else:
                # Create new model if all required fields are present
                required_fields = {'name', 'engine', 'api_key'}
                if all(field in props for field in required_fields):
                    self.models[slug] = ModelConfigSchema.from_dict(props)

    def get_model_config(self, slug: str) -> Optional[ModelConfigSchema]:
        """Get configuration for a specific model"""
        return self.models.get(slug)

    def get_all_models(self) -> List[ModelConfigSchema]:
        """Get all configured models"""
        return list(self.models.values()) 