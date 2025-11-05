# Technology Stack

# Technology Stack

## Programming Languages

The project is primarily written in **Python**, which is the main programming language used throughout the codebase. Python was chosen for its readability, ease of use, and the availability of a vast ecosystem of libraries and frameworks that can be leveraged for this type of project.

## Frameworks & Libraries

The project utilizes the following key frameworks and libraries:

### API Providers
- **Anthropic Provider**: Provides an interface to interact with the Anthropic API for language model-based tasks.
- **Ollama Provider**: Provides an interface to interact with the Ollama API for language model-based tasks.
- **OpenAI Provider**: Provides an interface to interact with the OpenAI API for language model-based tasks.

These API providers abstract the complexity of interacting with the various language model APIs, allowing the project to easily integrate with different providers.

### Configuration Management
- **Pydantic**: Used for defining and validating configuration models, ensuring that the application is configured correctly.

### Logging
- **Loguru**: A modern and feature-rich logging library that provides a more user-friendly interface than the built-in `logging` module.

### Testing
- **pytest**: A popular testing framework for Python that provides a simple and extensible way to write and run tests.

## Development Tools

The project utilizes the following development tools:

- **Poetry**: A dependency management and packaging tool for Python that simplifies the process of managing project dependencies and creating distributable packages.
- **Black**: A code formatter that ensures consistent code style across the project.
- **Flake8**: A tool for checking Python code style and syntax.
- **mypy**: A static type checker for Python that helps catch type-related errors early in the development process.

## Infrastructure

The project does not include any specific infrastructure details, as it is likely a library or utility that can be deployed in various environments. However, the following considerations may be relevant:

- **Deployment**: The project can be packaged and distributed as a Python package, which can be installed using tools like `pip` or `poetry`.
- **Hosting**: As a Python-based project, it can be hosted on various cloud platforms or on-premises servers that support Python applications.
- **CI/CD**: The project can be integrated with continuous integration and continuous deployment (CI/CD) pipelines to automate the build, test, and deployment processes.

## Third-Party Integrations

The project integrates with the following third-party services and APIs:

- **Anthropic API**: Provides access to Anthropic's language models for various natural language processing tasks.
- **Ollama API**: Provides access to Ollama's language models for various natural language processing tasks.
- **OpenAI API**: Provides access to OpenAI's language models for various natural language processing tasks.

These integrations allow the project to leverage the capabilities of different language models and providers, offering flexibility and the ability to adapt to the user's needs.