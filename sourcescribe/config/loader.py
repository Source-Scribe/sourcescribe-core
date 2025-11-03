"""Configuration loading and management."""

import os
import yaml
from pathlib import Path
from typing import Optional, Dict, Any
from sourcescribe.config.models import SourceScribeConfig, LLMConfig


class ConfigLoader:
    """Load and manage SourceScribe configuration."""
    
    DEFAULT_CONFIG_NAMES = [".sourcescribe.yaml", ".sourcescribe.yml", "sourcescribe.yaml"]
    
    @staticmethod
    def load_from_file(config_path: str) -> SourceScribeConfig:
        """
        Load configuration from a YAML file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            SourceScribeConfig instance
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config is invalid
        """
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        if data is None:
            data = {}
        
        # Inject environment variables for API keys
        ConfigLoader._inject_env_vars(data)
        
        return SourceScribeConfig.from_dict(data)
    
    @staticmethod
    def find_config(start_path: Optional[str] = None) -> Optional[Path]:
        """
        Find configuration file by searching upwards from start_path.
        
        Args:
            start_path: Starting directory (defaults to cwd)
            
        Returns:
            Path to config file or None if not found
        """
        current = Path(start_path or os.getcwd()).resolve()
        
        # Search upwards through parent directories
        for parent in [current] + list(current.parents):
            for config_name in ConfigLoader.DEFAULT_CONFIG_NAMES:
                config_path = parent / config_name
                if config_path.exists():
                    return config_path
        
        return None
    
    @staticmethod
    def load_or_default(config_path: Optional[str] = None) -> SourceScribeConfig:
        """
        Load configuration from file or create default.
        
        Args:
            config_path: Optional path to config file
            
        Returns:
            SourceScribeConfig instance
        """
        if config_path:
            return ConfigLoader.load_from_file(config_path)
        
        # Try to find config file
        found_config = ConfigLoader.find_config()
        if found_config:
            return ConfigLoader.load_from_file(str(found_config))
        
        # Return default config with env vars injected
        config = SourceScribeConfig()
        ConfigLoader._inject_env_vars_to_config(config)
        return config
    
    @staticmethod
    def save_to_file(config: SourceScribeConfig, output_path: str) -> None:
        """
        Save configuration to a YAML file.
        
        Args:
            config: Configuration to save
            output_path: Path to output file
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        data = config.to_dict()
        
        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    
    @staticmethod
    def create_default_config(output_path: str) -> SourceScribeConfig:
        """
        Create and save a default configuration file.
        
        Args:
            output_path: Path to save config
            
        Returns:
            Default SourceScribeConfig instance
        """
        config = SourceScribeConfig()
        ConfigLoader.save_to_file(config, output_path)
        return config
    
    @staticmethod
    def _inject_env_vars(data: Dict[str, Any]) -> None:
        """Inject environment variables into config data."""
        if "llm" not in data:
            data["llm"] = {}
        
        llm_config = data["llm"]
        
        # Check for API keys in environment
        if "api_key" not in llm_config or not llm_config["api_key"]:
            provider = llm_config.get("provider", "anthropic")
            
            if provider == "anthropic":
                llm_config["api_key"] = os.getenv("ANTHROPIC_API_KEY")
            elif provider == "openai":
                llm_config["api_key"] = os.getenv("OPENAI_API_KEY")
        
        # Ollama base URL
        if llm_config.get("provider") == "ollama":
            if "base_url" not in llm_config or not llm_config["base_url"]:
                llm_config["base_url"] = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    @staticmethod
    def _inject_env_vars_to_config(config: SourceScribeConfig) -> None:
        """Inject environment variables directly into config object."""
        if not config.llm.api_key:
            if config.llm.provider == "anthropic":
                config.llm.api_key = os.getenv("ANTHROPIC_API_KEY")
            elif config.llm.provider == "openai":
                config.llm.api_key = os.getenv("OPENAI_API_KEY")
        
        if config.llm.provider == "ollama" and not config.llm.base_url:
            config.llm.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
