# SourceScribe Project Summary

## Overview

SourceScribe is a comprehensive auto-documentation engine written in Python that uses Large Language Models (LLMs) to automatically generate insightful documentation for software projects. It supports multiple LLM providers (Anthropic Claude, OpenAI GPT, and Ollama) and can watch for code changes in real-time to keep documentation up-to-date.

## Project Structure

```
sourcescribe-core/
├── sourcescribe/              # Main package
│   ├── __init__.py           # Package initialization
│   ├── cli.py                # Command-line interface
│   ├── engine/               # Core documentation engine
│   │   ├── __init__.py
│   │   ├── generator.py      # Main documentation generator
│   │   ├── analyzer.py       # Code analysis and structure extraction
│   │   └── diagram.py        # Mermaid diagram generation
│   ├── watch/                # File watching
│   │   ├── __init__.py
│   │   ├── watcher.py        # File system watcher
│   │   └── handler.py        # Change event handler
│   ├── config/               # Configuration management
│   │   ├── __init__.py
│   │   ├── models.py         # Pydantic configuration models
│   │   └── loader.py         # Configuration loading/saving
│   ├── utils/                # Utilities
│   │   ├── __init__.py
│   │   ├── file_utils.py     # File operations
│   │   ├── parser.py         # Code parsing
│   │   └── logger.py         # Logging setup
│   └── api/                  # LLM provider integrations
│       ├── __init__.py
│       ├── base.py           # Base provider class
│       ├── anthropic_provider.py
│       ├── openai_provider.py
│       ├── ollama_provider.py
│       └── factory.py        # Provider factory
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_parser.py
│   ├── test_file_utils.py
│   └── test_diagram.py
├── docs/                     # Documentation
│   ├── CONTRIBUTING.md
│   ├── EXAMPLES.md
│   └── QUICKSTART.md
├── pyproject.toml           # Project metadata (PEP 518)
├── setup.py                 # Setup script (backward compatibility)
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── README.md                # Main documentation
├── LICENSE                  # MIT License
├── CHANGELOG.md             # Version history
├── Makefile                 # Development commands
├── .gitignore              # Git ignore rules
├── .env.example            # Environment variables template
└── .sourcescribe.yaml.example  # Configuration template
```

## Key Features

### 1. Multi-LLM Support
- **Anthropic Claude**: claude-3-5-sonnet and other models
- **OpenAI GPT**: GPT-4, GPT-4-turbo, and other models
- **Ollama**: Local LLMs (Llama2, Mistral, etc.)

### 2. Real-time File Watching
- Monitors code changes using `watchdog`
- Configurable debouncing to batch changes
- Selective file watching with include/exclude patterns

### 3. Mermaid Diagram Generation
- Architecture diagrams
- Class diagrams
- Flow diagrams
- Sequence diagrams
- Entity-relationship diagrams

### 4. Multi-language Support
Supports parsing and documentation for:
- Python, JavaScript, TypeScript, Java, Go, Rust
- C, C++, C#, Ruby, PHP, Swift, Kotlin, Scala
- And many more...

### 5. Comprehensive Documentation
Generates:
- Project overview
- Individual file documentation
- Architecture documentation with diagrams
- API endpoint documentation
- Dependency analysis

### 6. Pydantic Configuration
- Type-safe configuration using Pydantic v1/v2
- YAML-based configuration files
- Environment variable support
- Validation and error handling

### 7. CLI Interface
Commands:
- `sourcescribe generate` - Generate documentation once
- `sourcescribe watch` - Watch mode with auto-regeneration
- `sourcescribe init` - Initialize configuration
- `sourcescribe validate` - Validate configuration
- `sourcescribe info` - Show information

## Technical Implementation

### Architecture

1. **Configuration Layer** (`sourcescribe/config/`)
   - Pydantic models for type-safe configuration
   - YAML loading/saving
   - Environment variable injection

2. **LLM Integration Layer** (`sourcescribe/api/`)
   - Abstract base class for providers
   - Provider-specific implementations
   - Factory pattern for provider creation
   - Support for streaming responses

3. **Analysis Layer** (`sourcescribe/engine/analyzer.py`)
   - Code parsing with regex patterns
   - AST-like structure extraction
   - Dependency analysis
   - API endpoint detection

4. **Generation Layer** (`sourcescribe/engine/generator.py`)
   - Main documentation orchestration
   - LLM prompt engineering
   - Context building for LLMs
   - Output formatting and file management

5. **Diagram Layer** (`sourcescribe/engine/diagram.py`)
   - Mermaid.js diagram generation
   - Multiple diagram types
   - Customizable formatting

6. **Watch Layer** (`sourcescribe/watch/`)
   - File system monitoring
   - Change event handling
   - Debouncing and batching

7. **CLI Layer** (`sourcescribe/cli.py`)
   - Click-based command interface
   - Rich console output
   - Error handling

### Design Patterns

- **Factory Pattern**: LLM provider creation
- **Strategy Pattern**: Different parsing strategies per language
- **Observer Pattern**: File watching and change detection
- **Template Method**: Base provider with customizable implementations
- **Dependency Injection**: Configuration passed to components

### Key Dependencies

- **pydantic**: Configuration models and validation
- **click**: CLI framework
- **rich**: Beautiful console output
- **watchdog**: File system monitoring
- **anthropic**: Anthropic API client
- **openai**: OpenAI API client
- **requests**: HTTP client for Ollama
- **gitpython**: Git integration
- **jinja2**: Template rendering
- **pyyaml**: YAML parsing

## Usage Examples

### Basic Usage
```bash
# Initialize and generate
sourcescribe init
sourcescribe generate

# Watch mode
sourcescribe watch
```

### Python API
```python
from sourcescribe import DocumentationGenerator, SourceScribeConfig

config = SourceScribeConfig()
config.repository.path = "./my-project"
generator = DocumentationGenerator(config)
generator.generate_documentation()
```

### Custom Configuration
```yaml
llm:
  provider: "anthropic"
  model: "claude-3-5-sonnet-20241022"
  
repository:
  path: "."
  include_patterns: ["*.py", "*.js"]
  
output:
  path: "./docs"
  include_diagrams: true
```

## Testing

Test suite includes:
- Configuration model tests
- Code parser tests
- File utility tests
- Diagram generation tests
- Integration tests (planned)

Run tests:
```bash
pytest tests/
pytest --cov=sourcescribe tests/
```

## Cross-platform Compatibility

- **Python 3.7+**: Compatible with Python 3.7 through 3.12
- **Operating Systems**: macOS, Linux, Windows
- **Path Handling**: Uses `pathlib.Path` for cross-platform paths
- **Line Endings**: Handles different line endings gracefully

## Extensibility

### Adding New LLM Providers
1. Create new provider class inheriting from `BaseLLMProvider`
2. Implement `generate()` and `generate_streaming()` methods
3. Add to `LLMProviderFactory`

### Adding New Languages
1. Update `LANGUAGE_MAP` in `file_utils.py`
2. Add parsing logic in `CodeParser`
3. Add tests

### Custom Diagrams
1. Add new method to `DiagramGenerator`
2. Follow Mermaid.js syntax

## Performance Considerations

- **File Filtering**: Exclude patterns to reduce files processed
- **Max File Size**: Configurable limit (default 1MB)
- **Context Limits**: Truncate large files for LLM context
- **Debouncing**: Batch file changes to reduce API calls
- **Incremental Updates**: Only regenerate changed files in watch mode

## Security

- **API Keys**: Environment variables, never hardcoded
- **File Access**: Respects gitignore patterns
- **Input Validation**: Pydantic validation for all config
- **Path Traversal**: Path validation to prevent security issues

## Future Enhancements

- Git integration for commit-based documentation
- More LLM providers (Gemini, Cohere)
- Enhanced tree-sitter for better parsing
- Interactive documentation browser
- VSCode extension
- Documentation versioning
- HTML output with search
- Custom templates

## Getting Started

See [QUICKSTART.md](docs/QUICKSTART.md) for detailed getting started guide.

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for contribution guidelines.

## License

MIT License - See [LICENSE](LICENSE) file.

---

**Version**: 0.1.0  
**Status**: Alpha  
**Python**: 3.7+  
**Platform**: Cross-platform (macOS, Linux, Windows)
