# SourceScribe CLI Documentation

## File Purpose and Overview

The `cli.py` file in the `sourcescribe-core` project provides the command-line interface (CLI) for the SourceScribe auto-documentation engine. SourceScribe uses large language models (LLMs) to automatically generate documentation for software projects.

The CLI allows users to:

1. **Generate Documentation**: Analyze the source code of a project and generate comprehensive documentation using LLMs.
2. **Watch for Changes**: Continuously monitor a project for changes and automatically regenerate the documentation when files are modified.

The CLI supports multiple LLM providers (Anthropic, OpenAI, Ollama) and allows users to customize the configuration, output directory, and other settings.

## Main Components

The `cli.py` file defines the following main components:

1. **`main`** function: The entry point of the CLI, which sets up the logging configuration and provides the top-level command group.
2. **`generate`** command: Generates documentation for a project using the specified configuration and LLM provider.
3. **`watch`** command: Watches a project for changes and automatically regenerates the documentation when files are modified.

## Key Functionality

1. **Configuration Loading**: The CLI uses the `ConfigLoader` to load the SourceScribe configuration, either from a custom file or the default configuration.
2. **LLM Provider Selection**: Users can specify the LLM provider (Anthropic, OpenAI, or Ollama) and model to use for generating the documentation.
3. **Documentation Generation**: The `DocumentationGenerator` is used to analyze the project's source code and generate the documentation.
4. **File Watching**: The `FileWatcher` monitors the project directory for changes and triggers the regeneration of the documentation when files are modified.
5. **Error Handling**: The CLI gracefully handles various errors, such as missing API keys, connection issues, and unexpected exceptions.

## Dependencies and Imports

The `cli.py` file imports the following modules and dependencies:

- `sys`: Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.
- `click`: A Python package for creating beautiful command-line interfaces with as little code as possible.
- `pathlib`: Provides an object-oriented way of handling filesystem paths.
- `typing`: Provides support for type annotations.
- `sourcescribe`: Imports various modules and classes from the SourceScribe package, such as the version, configuration loader, models, generator, watcher, and logger.
- `logging`: Provides a flexible logging system for applications.

## Usage Examples

1. **Generate Documentation**:
   ```
   sourcescribe generate .
   sourcescribe generate --provider anthropic --model claude-3-haiku-20240307
   sourcescribe generate --provider openai --model gpt-4
   sourcescribe generate --provider ollama --model llama2
   sourcescribe generate --output ./custom-docs
   sourcescribe generate --config .sourcescribe.yaml
   ```

2. **Watch for Changes**:
   ```
   sourcescribe watch .
   sourcescribe watch --provider anthropic --model claude-3-haiku-20240307
   sourcescribe watch --provider openai --model gpt-4
   sourcescribe watch --provider ollama --model llama2
   sourcescribe watch --config .sourcescribe.yaml
   ```

## Implementation Details

1. **Configuration Loading**: The CLI uses the `ConfigLoader` to load the SourceScribe configuration, either from a custom file or the default configuration. The configuration includes settings for the LLM provider, model, output directory, and other options.

2. **Documentation Generation**: The `DocumentationGenerator` is responsible for analyzing the project's source code and generating the documentation. It uses the specified LLM provider and model to process the code and produce the documentation.

3. **File Watching**: The `FileWatcher` monitors the project directory for changes and triggers the regeneration of the documentation when files are modified. It uses the `on_changes` callback to handle the file changes and pass them to the `DocumentationGenerator` for processing.

4. **Error Handling**: The CLI uses a try-except block to handle various types of errors, such as missing API keys, connection issues, and unexpected exceptions. It provides user-friendly error messages and instructions to help the user resolve the issues.

5. **CLI Integration**: The CLI is built using the `click` library, which provides a simple and intuitive way to create command-line interfaces. The `main` function defines the top-level command group, and the `generate` and `watch` commands are defined as subcommands.

Overall, the `cli.py` file provides a powerful and user-friendly interface for the SourceScribe auto-documentation engine, allowing developers to easily generate and maintain documentation for their software projects.