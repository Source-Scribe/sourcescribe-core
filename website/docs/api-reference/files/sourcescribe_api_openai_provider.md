# OpenAI GPT API Provider

## File Purpose and Overview

The `openai_provider.py` file contains the implementation of the `OpenAIProvider` class, which is a provider for the OpenAI GPT API. This class is part of the `sourcescribe-core` project and is used to interact with the OpenAI GPT language model for generating text responses.

## Main Components

### Class: `OpenAIProvider`

The `OpenAIProvider` class is the main component of this file. It inherits from the `BaseLLMProvider` class and provides an implementation for generating responses using the OpenAI GPT API.

#### Key Functionality

1. **Initialization**: The `__init__` method initializes the OpenAI provider by checking if the OpenAI SDK is installed and setting the API key, timeout, and base URL.
2. **Response Generation**: The `generate` method takes a list of `LLMMessage` objects, an optional system prompt, and additional parameters, and generates a response using the OpenAI GPT API. It converts the input messages to the OpenAI format, makes the API call, and returns an `LLMResponse` object.
3. **Streaming Response Generation**: The `generate_streaming` method is similar to `generate`, but it generates the response in a streaming fashion, yielding response chunks as they become available.

## Dependencies and Imports

The file imports the following modules and types:

- `typing`: For type annotations
- `sourcescribe.api.base`: For the `BaseLLMProvider`, `LLMMessage`, and `LLMResponse` classes
- `openai`: The OpenAI SDK, which is imported conditionally based on its availability

## Usage Examples

Here's an example of how to use the `OpenAIProvider` class:

```python
from sourcescribe.api.openai_provider import OpenAIProvider
from sourcescribe.api.base import LLMMessage

provider = OpenAIProvider(api_key="your_openai_api_key")

messages = [
    LLMMessage(role="user", content="What is the capital of France?"),
    LLMMessage(role="assistant", content="The capital of France is Paris."),
]

response = provider.generate(messages)
print(response.content)  # Output: "The capital of France is Paris."
```

## Important Implementation Details

1. **API Key Validation**: The `OpenAIProvider` class checks if the `OPENAI_API_KEY` environment variable is set and raises a `ValueError` if it is not.
2. **Default Model**: If the `model` parameter is not provided, the class sets the default model to `"gpt-4-turbo-preview"`.
3. **Message Conversion**: The `generate` and `generate_streaming` methods convert the input `LLMMessage` objects to the format expected by the OpenAI API.
4. **API Call**: The methods make the API call to the OpenAI GPT API using the `openai.chat.completions.create` method, passing in the appropriate parameters.
5. **Response Handling**: The methods return an `LLMResponse` object, which contains the generated text, model information, usage statistics, and the raw API response.
6. **Streaming Response**: The `generate_streaming` method uses the `stream=True` parameter to generate the response in a streaming fashion, yielding response chunks as they become available.
7. **Context Overflow Prevention**: The code includes a comment indicating that the content is limited to prevent context overflow, but the implementation details are not provided in the given code snippet.