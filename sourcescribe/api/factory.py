"""Factory for creating LLM providers."""

from typing import Optional
from sourcescribe.api.base import BaseLLMProvider
from sourcescribe.api.anthropic_provider import AnthropicProvider
from sourcescribe.api.openai_provider import OpenAIProvider
from sourcescribe.api.ollama_provider import OllamaProvider
from sourcescribe.config.models import LLMConfig, LLMProvider as LLMProviderEnum


class LLMProviderFactory:
    """Factory for creating LLM provider instances."""
    
    @staticmethod
    def create(config: LLMConfig) -> BaseLLMProvider:
        """
        Create an LLM provider based on configuration.
        
        Args:
            config: LLM configuration
            
        Returns:
            Instantiated provider
            
        Raises:
            ValueError: If provider is not supported
        """
        provider_map = {
            LLMProviderEnum.ANTHROPIC: AnthropicProvider,
            LLMProviderEnum.OPENAI: OpenAIProvider,
            LLMProviderEnum.OLLAMA: OllamaProvider,
        }
        
        provider_class = provider_map.get(config.provider)
        if not provider_class:
            raise ValueError(f"Unsupported LLM provider: {config.provider}")
        
        return provider_class(
            api_key=config.api_key,
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            timeout=config.timeout,
            base_url=config.base_url,
        )
    
    @staticmethod
    def create_from_name(
        provider_name: str,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> BaseLLMProvider:
        """
        Create an LLM provider by name.
        
        Args:
            provider_name: Name of the provider (anthropic, openai, ollama)
            api_key: Optional API key
            model: Optional model name
            **kwargs: Additional parameters
            
        Returns:
            Instantiated provider
        """
        provider_name = provider_name.lower()
        
        if provider_name == "anthropic":
            return AnthropicProvider(api_key=api_key, model=model or "", **kwargs)
        elif provider_name == "openai":
            return OpenAIProvider(api_key=api_key, model=model or "", **kwargs)
        elif provider_name == "ollama":
            return OllamaProvider(model=model or "llama2", **kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider_name}")
