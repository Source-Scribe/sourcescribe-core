# Project Overview: SourceScribe

## 1. Project Purpose and Main Functionality

SourceScribe is a powerful documentation generation tool that automatically creates comprehensive documentation for software projects. It analyzes the codebase and generates detailed documentation, including API references, diagrams, and other relevant information. The primary goal of SourceScribe is to streamline the documentation process, making it easier for developers to maintain up-to-date and accurate documentation for their projects.

## 2. Key Components and Modules

The SourceScribe project is organized into the following key components and modules:

### 2.1. API Providers
- `sourcescribe/api/`: This directory contains the implementation of various API providers, such as Anthropic, Ollama, and OpenAI, which are used to generate documentation content.
- `sourcescribe/api/base.py`: Defines the base class for API providers, providing a common interface for interacting with different AI-powered documentation generation services.
- `sourcescribe/api/factory.py`: Handles the creation and management of API provider instances.

### 2.2. Configuration
- `sourcescribe/config/`: This directory houses the configuration-related modules, including the configuration loader and models.
- `sourcescribe/config/loader.py`: Responsible for loading and parsing the project configuration.
- `sourcescribe/config/models.py`: Defines the data models for the configuration settings.

### 2.3. Documentation Engine
- `sourcescribe/engine/`: This directory contains the core functionality for analyzing the codebase, generating diagrams, and producing the final documentation.
- `sourcescribe/engine/analyzer.py`: Analyzes the codebase and extracts relevant information for documentation generation.
- `sourcescribe/engine/diagram.py`: Generates diagrams and visualizations based on the codebase analysis.
- `sourcescribe/engine/generator.py`: Responsible for the overall documentation generation process.

### 2.4. Utilities
- `sourcescribe/utils/`: This directory houses various utility modules, such as file handling, logging, and parsing.
- `sourcescribe/utils/file_utils.py`: Provides file-related utility functions.
- `sourcescribe/utils/logger.py`: Handles logging functionality.
- `sourcescribe/utils/parser.py`: Implements parsing logic for various file formats.

### 2.5. Monitoring and Automation
- `sourcescribe/watch/`: This directory contains modules related to monitoring the codebase and automating the documentation generation process.
- `sourcescribe/watch/handler.py`: Handles file change events and triggers the documentation generation process.
- `sourcescribe/watch/watcher.py`: Monitors the codebase for changes and notifies the handler.

### 2.6. Command-Line Interface
- `sourcescribe/cli.py`: Provides a command-line interface for interacting with the SourceScribe tool.

## 3. Technology Stack

SourceScribe is primarily built using the following technologies:

- **Python**: The core of the project is written in Python, leveraging various Python libraries and frameworks.
- **JavaScript**: The website component of the project, located in the `website/` directory, is built using JavaScript.
- **TypeScript**: Some of the website components are written in TypeScript to provide better type safety and tooling.

## 4. Project Structure Overview

The SourceScribe project has the following file structure:

```
sourcescribe/
├── setup.py
├── __init__.py
├── api/
│   ├── __init__.py
│   ├── anthropic_provider.py
│   ├── base.py
│   ├── factory.py
│   ├── ollama_provider.py
│   └── openai_provider.py
├── cli.py
├── config/
│   ├── __init__.py
│   ├── loader.py
│   └── models.py
├── engine/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── diagram.py
│   └── generator.py
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   ├── logger.py
│   └── parser.py
└── watch/
    ├── __init__.py
    ├── handler.py
    └── watcher.py
```

The project is organized into several directories, each containing modules that handle specific functionalities, such as API providers, configuration management, the documentation engine, utility functions, and monitoring/automation.

## 5. Getting Started

To get started with SourceScribe, follow these steps:

1. **Install the dependencies**: Ensure that you have Python installed on your system. Then, install the required dependencies by running `pip install -r requirements.txt` in the project directory.

2. **Configure the project**: Create a configuration file (e.g., `config.yml`) in the project root directory. This file should contain the necessary settings for your project, such as the API provider credentials, exclusions, and other preferences.

3. **Run the CLI**: Use the provided command-line interface to generate the documentation. From the project root, run `python sourcescribe/cli.py generate` to initiate the documentation generation process.

4. **Explore the generated documentation**: The generated documentation will be saved in the project's `docs/` directory. You can open the HTML files in a web browser to view the comprehensive documentation for your project.

For more detailed information, please refer to the project's README file and the documentation available in the `docs/` directory.