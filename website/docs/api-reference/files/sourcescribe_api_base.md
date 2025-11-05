# SourceScribe Core API: Base LLM Provider

## File Purpose and Overview

The `base.py` file in the `sourcescribe/api` directory of the SourceScribe Core project defines the base classes and functionality for interacting with Large Language Models (LLMs) in the SourceScribe application. This file establishes the foundation for integrating different LLM providers, such as OpenAI, Anthropic, or Hugging Face, into the SourceScribe system.

## Main Components

The key components defined in this file are:

1. `LLMMessage` dataclass
2. `LLMResponse` dataclass
3. `BaseLLMProvider` abstract base class

### `LLMMessage` Dataclass

The `LLMMessage` dataclass represents a single message in the conversation with an LLM. It has the following fields:

- `role`: The role of the message, which can be "system", "user", or "assistant".
- `content`: The content of the message.

### `LLMResponse` Dataclass

The `LLMResponse` dataclass represents the response from an LLM provider. It has the following fields:

- `content`: The generated content from the LLM.
- `model`: The name of the LLM model used.
- `usage`: A dictionary containing the number of tokens used in the response.
- `finish_reason`: An optional string indicating the reason the generation finished.
- `raw_response`: An optional field to store the raw response from the LLM provider.

### `BaseLLMProvider` Abstract Base Class

The `BaseLLMProvider` abstract base class defines the common interface and functionality for interacting with LLM providers. It has the following methods:

- `__init__`: Initializes the LLM provider with the necessary configuration, such as API key, model, temperature, max tokens, timeout, and base URL.
- `generate`: Generates a response from the LLM based on the provided messages and an optional system prompt.
- `generate_streaming`: Generates a streaming response from the LLM, yielding chunks of the response.
- `validate_config`: Validates the provider configuration, ensuring that the model is specified.
- `format_code_context`: Formats the code context for the LLM, including the file path, code content, language, and an optional description.

## Key Functionality

The main functionality provided by this file is the foundation for integrating different LLM providers into the SourceScribe application. The `BaseLLMProvider` abstract base class defines the common interface and methods that all LLM providers must implement, ensuring a consistent and extensible way of interacting with various LLM models.

The `LLMMessage` and `LLMResponse` dataclasses provide a standardized way of representing the input messages and the generated responses, respectively, across different LLM providers.

The `format_code_context` method is a utility function that helps format the code context in a way that can be easily consumed by the LLM during the generation process.

## Dependencies and Imports

The file imports the following modules and classes:

- `abc` module: Provides the `ABC` and `abstractmethod` classes for defining abstract base classes.
- `typing` module: Provides type annotations for the function parameters and return values.
- `dataclasses` module: Provides the `dataclass` decorator for creating data classes.

## Usage Examples

While this file does not provide any direct usage examples, it serves as the foundation for integrating LLM providers into the SourceScribe application. Concrete implementations of the `BaseLLMProvider` abstract base class would be responsible for handling the specific details of interacting with each LLM provider's API.

## Important Implementation Details

1. **Abstract Base Class**: The `BaseLLMProvider` class is defined as an abstract base class, which means that it cannot be instantiated directly. Instead, concrete subclasses must be created to implement the `generate` and `generate_streaming` methods.

2. **Configuration Parameters**: The `__init__` method of the `BaseLLMProvider` class accepts several configuration parameters, such as the API key, model, temperature, max tokens, timeout, and base URL. These parameters are used to configure the LLM provider's behavior.

3. **Validation**: The `validate_config` method ensures that the model is specified, as it is a required parameter for the LLM provider to function correctly.

4. **Code Formatting**: The `format_code_context` method provides a way to format the code context in a standardized manner, including the file path, code content, language, and an optional description. This formatted context can be used when interacting with the LLM during the generation process.

5. **Dataclasses**: The `LLMMessage` and `LLMResponse` dataclasses are used to represent the input messages and the generated responses, respectively. Dataclasses provide a convenient way to define and work with structured data in Python.