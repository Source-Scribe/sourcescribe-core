# Anthropic Claude API Provider

## File Purpose and Overview
The `anthropic_provider.py` file contains the implementation of the `AnthropicProvider` class, which is a provider for the Anthropic Claude language model. This class is part of the `sourcescribe-core` project and is responsible for interacting with the Anthropic Claude API to generate responses for language model tasks.

## Main Components

### `AnthropicProvider` Class
The `AnthropicProvider` class is the main component of this file. It inherits from the `BaseLLMProvider` class and provides an implementation for generating responses using the Anthropic Claude API.

#### Methods
1. `__init__(self, *args, **kwargs)`: Initializes the `AnthropicProvider` instance by checking if the Anthropic SDK is available, validating the API key, and setting the default model if not provided.
2. `generate(self, messages: List[LLMMessage], system_prompt: Optional[str] = None, **kwargs: Any) -> LLMResponse`: Generates a response using the Anthropic Claude API. It converts the input messages to the Anthropic format, prepares the request parameters, makes the API call, and returns an `LLMResponse` object.
3. `generate_streaming(self, messages: List[LLMMessage], system_prompt: Optional[str] = None, **kwargs: Any) -> Iterator[str]`: Generates a streaming response using the Anthropic Claude API. It converts the input messages to the Anthropic format, prepares the request parameters, and yields the response chunks as they are received.

## Key Functionality
The `AnthropicProvider` class provides the following key functionality:

1. **Anthropic Claude API Integration**: The class encapsulates the interaction with the Anthropic Claude API, handling the necessary request parameters and response processing.
2. **Conversation Message Handling**: The `generate()` and `generate_streaming()` methods accept a list of `LLMMessage` objects, which represent the conversation context, and optionally a system prompt.
3. **Response Generation**: The class generates responses using the Anthropic Claude language model, either as a complete response or as a streaming response.
4. **Response Formatting**: The generated responses are formatted and returned as `LLMResponse` objects, which contain the response content, model information, usage statistics, and the raw response from the API.

## Dependencies and Imports
The `anthropic_provider.py` file has the following dependencies:

1. `typing`: Provides type annotations for the function parameters and return values.
2. `sourcescribe.api.base`: Imports the `BaseLLMProvider`, `LLMMessage`, and `LLMResponse` classes from the base API module.
3. `anthropic`: Imports the Anthropic SDK, which is used to interact with the Anthropic Claude API.

## Usage Examples
Here's an example of how to use the `AnthropicProvider` class:

```python
from sourcescribe.api.anthropic_provider import AnthropicProvider
from sourcescribe.api.base import LLMMessage

provider = AnthropicProvider(api_key="your_anthropic_api_key")

messages = [
    LLMMessage(role="user", content="What is the capital of France?"),
    LLMMessage(role="assistant", content="The capital of France is Paris."),
    LLMMessage(role="user", content="Can you tell me more about the Eiffel Tower?"),
]

response = provider.generate(messages)
print(response.content)

for chunk in provider.generate_streaming(messages):
    print(chunk, end="")
```

## Important Implementation Details
1. **Anthropic SDK Availability Check**: The `AnthropicProvider` class checks if the Anthropic SDK is installed and available before initializing the provider. If the SDK is not installed, an `ImportError` is raised.
2. **API Key Validation**: The class validates that the `ANTHROPIC_API_KEY` environment variable is set before initializing the provider. If the API key is not provided, a `ValueError` is raised.
3. **Default Model Selection**: If the `model` parameter is not provided during initialization, the class sets the default model to `"claude-3-haiku-20240307"`.
4. **Message Conversion**: The `generate()` and `generate_streaming()` methods convert the input `LLMMessage` objects to the format expected by the Anthropic API.
5. **Response Extraction**: The `generate()` method extracts the response content from the Anthropic API response, which may contain multiple text blocks, and returns an `LLMResponse` object.
6. **Streaming Response**: The `generate_streaming()` method uses the Anthropic API's streaming functionality to yield the response chunks as they are received, allowing for real-time response processing.
7. **Context Limiting**: The code includes a comment indicating that the content is limited to prevent context overflow, which is an important consideration when working with language models.