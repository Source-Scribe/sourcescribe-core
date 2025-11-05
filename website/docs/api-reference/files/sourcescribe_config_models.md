# SourceScribe Configuration Models

## File Purpose and Overview

This Python file, `models.py`, defines the Pydantic models for the configuration of the SourceScribe tool. SourceScribe is a documentation generation tool that can automatically generate comprehensive documentation for software projects based on the source code.

The configuration models defined in this file cover various aspects of the SourceScribe tool, including:

- LLM (Large Language Model) provider and settings
- Repository scanning configuration
- Documentation output settings
- File watching and change detection
- Documentation style and content

These models provide a structured and extensible way to configure the behavior of the SourceScribe tool, allowing users to customize the documentation generation process to their specific needs.

## Main Components

The main components in this file are the following Pydantic models:

1. `LLMProvider`: An enumeration of the supported LLM providers, including Anthropic, OpenAI, and Ollama.
2. `Verbosity`: An enumeration of the supported documentation verbosity levels, including minimal, normal, and detailed.
3. `OutputFormat`: An enumeration of the supported output formats for the generated documentation, including Markdown, HTML, and JSON.
4. `DiagramFormat`: An enumeration of the supported diagram formats, including Mermaid and PlantUML.
5. `LLMConfig`: A model that holds the configuration for the LLM provider, including the model, API key, temperature, and maximum tokens.
6. `RepositoryConfig`: A model that holds the configuration for scanning the repository, including the root path, exclusion and inclusion patterns, maximum file size, and whether to follow symbolic links.
7. `OutputConfig`: A model that holds the configuration for the documentation output, including the output directory, format, diagram inclusion, diagram format, overwriting, and index file creation.
8. `WatchConfig`: A model that holds the configuration for the file watching feature, including whether it's enabled, the debounce interval, batch changes, and recursive watching.
9. `StyleConfig`: A model that holds the configuration for the documentation style, including the inclusion of examples, architecture overview, API documentation, dependencies, metrics, verbosity level, and language.
10. `SourceScribeConfig`: The main configuration model that aggregates all the other configuration models and provides additional utility methods for converting the configuration to and from a dictionary.

## Key Functionality

The main functionality provided by this file is the definition of the configuration models for the SourceScribe tool. These models allow users to customize the behavior of the tool to their specific needs, such as:

- Selecting the LLM provider and configuring its settings
- Defining the repository scanning rules, including which files to include and exclude
- Specifying the output format and location for the generated documentation
- Configuring the file watching and change detection behavior
- Controlling the style and content of the generated documentation

The `SourceScribeConfig` model serves as the main entry point for the configuration, allowing users to easily access and modify all the relevant settings.

## Dependencies and Imports

This file imports the following dependencies:

- `typing`: For type annotations, including `List`, `Optional`, `Dict`, and `Any`.
- `enum`: For creating enumeration types, such as `LLMProvider`, `Verbosity`, `OutputFormat`, and `DiagramFormat`.
- `pydantic`: For defining the base model and various field types and validators.

## Usage Examples

While this file does not contain any direct usage examples, it can be used as follows:

```python
from sourcescribe.config.models import SourceScribeConfig

# Create a SourceScribeConfig instance with custom settings
config = SourceScribeConfig(
    llm=LLMConfig(
        provider=LLMProvider.OPENAI,
        model="text-davinci-003",
        api_key="your_openai_api_key"
    ),
    repository=RepositoryConfig(
        path="/path/to/your/repository",
        exclude_patterns=["*.pyc", "__pycache__"]
    ),
    output=OutputConfig(
        path="./docs/generated",
        format=OutputFormat.HTML
    ),
    style=StyleConfig(
        verbosity=Verbosity.DETAILED
    )
)

# Use the config to generate documentation
# (the actual usage would be in another part of the codebase)
```

## Important Implementation Details

1. The `model_config = ConfigDict(use_enum_values=True)` lines in the models allow the use of enum values directly in the configuration, rather than having to use the enum member names as strings.
2. The `field_validator` decorator is used in the `WatchConfig` model to validate the `debounce_seconds` field, ensuring that it does not exceed 60 seconds.
3. The `to_dict()` and `from_dict()` methods in the `SourceScribeConfig` model provide a convenient way to convert the configuration to and from a dictionary, which can be useful for serialization and deserialization purposes.
4. The `SourceScribeConfig` model uses the `ConfigDict(extra="allow")` setting, which allows for additional fields to be added to the configuration in the future, ensuring extensibility.

Overall, this file provides a well-structured and extensible way to configure the SourceScribe tool, making it easier for users to customize the documentation generation process to their specific needs.