# Ollama Provider Documentation

## File Purpose and Overview
The `ollama_provider.py` file contains the implementation of the `OllamaProvider` class, which is a provider for the Ollama local Large Language Model (LLM). This provider allows users to interact with the Ollama LLM service, generating responses based on provided messages and system prompts.

## Main Components

### `OllamaProvider` Class
The `OllamaProvider` class is the main component of this file. It inherits from the `BaseLLMProvider` class and provides the following functionality:

1. **Initialization**: The `__init__` method sets up the Ollama provider by configuring the base URL and default model, and checking the connection to the Ollama server.
2. **Connection Checking**: The `_check_connection` method verifies that the Ollama server is accessible and running the correct version.
3. **Response Generation**: The `generate` method generates a response from the Ollama LLM based on the provided messages and system prompt. It constructs the prompt, sends a request to the Ollama API, and returns the response.
4. **Streaming Response Generation**: The `generate_streaming` method generates a response from the Ollama LLM in a streaming fashion, yielding response chunks as they become available.
5. **Prompt Building**: The `_build_prompt` method constructs a single prompt string from the provided messages and system prompt.
6. **Model Listing**: The `list_models` method retrieves a list of available Ollama models.

## Key Functionality
The `OllamaProvider` class provides the following key functionality:

1. **Connecting to Ollama**: The class ensures that the Ollama server is running and accessible, and that the specified model is available.
2. **Generating Responses**: The `generate` and `generate_streaming` methods allow users to generate responses from the Ollama LLM based on provided messages and system prompts.
3. **Handling Errors**: The class handles various types of errors that may occur during the interaction with the Ollama server, providing informative error messages to the user.
4. **Listing Available Models**: The `list_models` method allows users to retrieve a list of available Ollama models.

## Dependencies and Imports
The `ollama_provider.py` file imports the following dependencies:

- `requests`: Used for making HTTP requests to the Ollama API.
- `typing`: Used for type annotations.
- `sourcescribe.api.base`: Imports the `BaseLLMProvider`, `LLMMessage`, and `LLMResponse` classes from the base module.

## Usage Examples
Here's an example of how to use the `OllamaProvider` class:

```python
from sourcescribe.api.ollama_provider import OllamaProvider
from sourcescribe.api.base import LLMMessage

provider = OllamaProvider()

messages = [
    LLMMessage(role="user", content="What is the capital of France?"),
    LLMMessage(role="assistant", content="The capital of France is Paris.")
]

response = provider.generate(messages)
print(response.content)  # Output: The capital of France is Paris.
```

In this example, we create an instance of the `OllamaProvider` class, then use the `generate` method to generate a response based on the provided messages.

## Important Implementation Details
1. **Ollama Server Configuration**: The `OllamaProvider` class automatically sets the base URL and default model if they are not provided during initialization. It also checks the connection to the Ollama server and raises appropriate errors if the server is not accessible or the specified model is not available.
2. **Prompt Building**: The `_build_prompt` method constructs a single prompt string from the provided messages and system prompt, which is then used for the API request.
3. **Response Handling**: The `generate` and `generate_streaming` methods handle the API response, extracting the relevant information (content, usage, finish reason, and raw response) and returning an `LLMResponse` object.
4. **Error Handling**: The class provides detailed error messages to help users troubleshoot issues, such as when the Ollama server is not running or the specified model is not available.