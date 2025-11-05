# SourceScribe API Factory

## File Purpose and Overview
The `factory.py` file in the `sourcescribe/api/` directory of the SourceScribe project contains the implementation of the `LLMProviderFactory` class. This factory class is responsible for creating instances of `BaseLLMProvider` subclasses, which represent different Large Language Model (LLM) providers such as Anthropic, OpenAI, and Ollama.

The purpose of this factory is to provide a centralized and consistent way of instantiating LLM providers based on the configuration settings specified in the `LLMConfig` model.

## Main Components

### `LLMProviderFactory` Class
The `LLMProviderFactory` class is the main component of this file. It provides two static methods for creating LLM provider instances:

1. `create(config: LLMConfig) -> BaseLLMProvider`:
   - This method takes an `LLMConfig` object as input and returns an instance of the appropriate `BaseLLMProvider` subclass based on the configuration.
   - It uses a `provider_map` dictionary to map the `LLMProvider` enum values to the corresponding provider classes.
   - If the provider is not supported, it raises a `ValueError`.

2. `create_from_name(provider_name: str, api_key: Optional[str] = None, model: Optional[str] = None, **kwargs) -> BaseLLMProvider`:
   - This method allows you to create an LLM provider instance by specifying the provider name as a string (e.g., "anthropic", "openai", "ollama").
   - It takes an optional `api_key` and `model` parameter, as well as any additional keyword arguments.
   - It uses conditional logic to instantiate the appropriate `BaseLLMProvider` subclass based on the provider name.
   - If the provider name is not supported, it raises a `ValueError`.

## Key Functionality
The main functionality of this file is to provide a centralized and consistent way of creating LLM provider instances based on configuration settings or provider name. This helps to decouple the LLM provider implementation details from the rest of the SourceScribe codebase, making it easier to add, remove, or change LLM providers as needed.

## Dependencies and Imports
The `factory.py` file imports the following modules and classes:

- `typing.Optional`: For optional type annotations.
- `sourcescribe.api.base.BaseLLMProvider`: The base class for all LLM providers.
- `sourcescribe.api.anthropic_provider.AnthropicProvider`: The Anthropic LLM provider implementation.
- `sourcescribe.api.openai_provider.OpenAIProvider`: The OpenAI LLM provider implementation.
- `sourcescribe.api.ollama_provider.OllamaProvider`: The Ollama LLM provider implementation.
- `sourcescribe.config.models.LLMConfig`: The configuration model for LLM providers.
- `sourcescribe.config.models.LLMProvider`: The enum representing the available LLM providers.

## Usage Examples
Here are some examples of how to use the `LLMProviderFactory` class:

```python
from sourcescribe.config.models import LLMConfig, LLMProvider
from sourcescribe.api.factory import LLMProviderFactory

# Create an LLM provider from configuration
config = LLMConfig(
    provider=LLMProvider.ANTHROPIC,
    api_key="your_anthropic_api_key",
    model="claude-v1",
    temperature=0.7,
    max_tokens=2048,
    timeout=60,
)
provider = LLMProviderFactory.create(config)

# Create an LLM provider by name
provider = LLMProviderFactory.create_from_name(
    "openai",
    api_key="your_openai_api_key",
    model="text-davinci-003",
    temperature=0.5,
)
```

## Important Implementation Details
- The `LLMProviderFactory` class uses a `provider_map` dictionary to map the `LLMProvider` enum values to the corresponding provider classes. This allows for easy addition or removal of LLM providers in the future.
- The `create_from_name()` method provides a more flexible way of creating LLM provider instances, allowing you to specify the provider name as a string instead of relying on the `LLMProvider` enum.
- The factory methods handle the instantiation of the appropriate `BaseLLMProvider` subclass, encapsulating the provider-specific configuration and initialization logic.