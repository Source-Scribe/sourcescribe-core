# Architecture Overview

# System Architecture Documentation

## High-Level Architecture

The system is composed of several key modules that work together to provide a comprehensive solution. The high-level architecture can be visualized as follows:

```mermaid
graph LR
    cli --> factory
    factory --> providers[Providers]
    providers --> models
    models --> analyzer
    analyzer --> diagram
    analyzer --> generator
    generator --> file_utils
    watcher --> handler
    handler --> logger
```

The main components and their roles are:

- **CLI**: Provides the command-line interface for users to interact with the system.
- **Factory**: Responsible for creating and managing the different provider instances (Anthropic, OpenAI, OLLama).
- **Providers**: Implement the logic to communicate with the various AI language models (Anthropic, OpenAI, OLLama).
- **Models**: Define the data structures and schemas used throughout the system.
- **Analyzer**: Analyzes the input files and extracts relevant information.
- **Diagram**: Generates visual diagrams (e.g., sequence diagrams, flowcharts) based on the analyzed data.
- **Generator**: Generates the final output files based on the analyzed data.
- **File Utils**: Provides utility functions for file and directory operations.
- **Watcher**: Monitors the file system for changes and triggers the appropriate actions.
- **Handler**: Handles file-related events and coordinates the processing of changes.
- **Logger**: Provides logging functionality for the system.

## Data Flow

The typical data flow in the system is as follows:

1. The user interacts with the CLI, providing input files or commands.
2. The CLI module passes the user's input to the Factory, which creates the appropriate provider instances.
3. The provider instances communicate with the external AI language models to obtain the necessary information.
4. The provider responses are then passed to the Models module, which handles the data structures.
5. The Analyzer module processes the input files and extracts relevant information, such as code structure, dependencies, and documentation.
6. The extracted data is then used by the Diagram and Generator modules to generate the final output, which may include visual diagrams and documentation.
7. The Watcher and Handler modules monitor the file system for changes and trigger the appropriate processing steps.

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Factory
    participant Providers
    participant Models
    participant Analyzer
    participant Diagram
    participant Generator
    participant FileUtils

    User->>CLI: Provide input files/commands
    CLI->>Factory: Pass user input
    Factory->>Providers: Create provider instances
    Providers->>Models: Provide data
    Analyzer->>Models: Process input files
    Analyzer->>Diagram: Generate diagrams
    Analyzer->>Generator: Generate documentation
    Generator->>FileUtils: Write output files
    Watcher->>Handler: Monitor file changes
    Handler->>Analyzer: Trigger re-analysis
```

## Design Principles

The system architecture follows several key design principles:

1. **Modularity**: The system is divided into well-defined, loosely coupled modules, each with a specific responsibility. This promotes maintainability, testability, and flexibility.
2. **Abstraction**: The use of abstract base classes and interfaces in the `base` module allows for easy substitution of different provider implementations, following the Dependency Inversion Principle.
3. **Separation of Concerns**: The clear separation of concerns, such as data modeling, file processing, and output generation, helps to keep the codebase organized and easier to understand.
4. **Extensibility**: The system is designed to be easily extensible, allowing for the addition of new providers, data models, and processing capabilities without requiring significant changes to the existing codebase.
5. **Configuration-Driven**: The use of configuration files and the `loader` module allows for easy customization of the system's behavior, making it more adaptable to different use cases.

These design principles contribute to the overall robustness, maintainability, and scalability of the system architecture.

## System Architecture Diagram

```mermaid
graph TD
    title[System Architecture]
    style title fill:#f9f,stroke:#333,stroke-width:2px

    M0[setup]
    M1[__init__]
    M2[anthropic_provider]
    M3[base]
    M4[factory]
    M5[ollama_provider]
    M6[openai_provider]
    M7[cli]
    M8[loader]
    M9[models]
    M10[analyzer]
    M11[diagram]
    M12[feature_generator]
    M13[generator]
    M14[file_utils]
    M15[logger]
    M16[parser]
    M17[handler]
    M18[watcher]
    M19[test_config]
    M20[test_diagram]
    M21[test_exclusions]
    M22[test_file_utils]
    M23[test_parser]

    M2 --> M3
    M4 --> M2
    M4 --> M9
    M4 --> M6
    M4 --> M3
    M4 --> M5
    M5 --> M3
    M6 --> M3
    M7 --> M13
    M7 --> M18
    M7 --> M9
    M7 --> M15
    M7 --> M8
    M8 --> M9
    M10 --> M9
    M10 --> M16
    M10 --> M15
    M10 --> M14
    M12 --> M3
    M12 --> M14
    M13 --> M9
    M13 --> M4
    M13 --> M3
    M13 --> M14
    M13 --> M15
    M13 --> M10
    M13 --> M11
    M13 --> M12
    M17 --> M15
    M18 --> M17
    M18 --> M9
    M18 --> M15
    M19 --> M9
    M19 --> M8
    M20 --> M11
    M21 --> M9
    M21 --> M14
    M23 --> M16
```
