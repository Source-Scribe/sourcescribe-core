# Technology Stack

# Technology Stack

## Programming Languages

The primary programming language used in this project is **Python**. Python was chosen for its readability, extensive ecosystem of libraries, and suitability for tasks such as text processing, data analysis, and rapid prototyping.

## Frameworks & Libraries

The project utilizes the following key frameworks and libraries:

### API Providers
- **Anthropic Provider**: Provides integration with the Anthropic language model API for generating text-based content.
- **Ollama Provider**: Integrates with the Ollama language model API for additional text generation capabilities.
- **OpenAI Provider**: Allows the use of OpenAI's language models, such as GPT-3, for text generation.

These API providers abstract the complexity of interacting with the various language model services, making it easier to integrate and switch between different providers as needed.

### Configuration Management
- **Pydantic**: Used for defining and validating configuration models, ensuring the integrity of the application's settings.

### Utilities
- **Mermaid.js**: A JavaScript library for generating diagrams (sequence, flowchart, class, state) that are embedded in the documentation.
- **Loguru**: A modern logging library that provides more advanced logging features compared to the built-in `logging` module.

### Testing
- **pytest**: The primary testing framework used for writing and running unit tests.

## Development Tools

The project utilizes the following development tools:

- **Poetry**: A dependency management and packaging tool for Python, used to manage project dependencies and create distributable packages.
- **Black**: A code formatter that ensures consistent code style throughout the project.
- **Flake8**: A tool for checking code style and syntax, helping to maintain code quality.
- **mypy**: A static type checker that helps catch type-related errors during development.

## Infrastructure

The project does not include any specific information about the infrastructure or deployment setup. It appears to be a standalone Python package that can be installed and used locally or integrated into other applications.

## Third-Party Integrations

The project integrates with the following third-party services:

- **Anthropic**: Provides a language model API for generating text-based content.
- **Ollama**: Offers another language model API for text generation.
- **OpenAI**: Allows the use of OpenAI's language models, such as GPT-3, for text generation.

These integrations are facilitated through the API provider classes, which abstract the complexity of interacting with the various language model services.