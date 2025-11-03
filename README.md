# SourceScribe

An intelligent auto-documentation engine that watches your codebase and generates comprehensive documentation using LLMs (Claude, OpenAI, Ollama). Inspired by [CodeWiki](https://github.com/FSoft-AI4Code/CodeWiki) and [research](https://arxiv.org/html/2510.24428v2).

## Features

- 🤖 **Multi-LLM Support**: Integrates with Claude (Anthropic), OpenAI (GPT-4/5), and Ollama
- 👁️ **Real-time Watching**: Monitors code changes and updates documentation automatically
- 📊 **Architecture Diagrams**: Generates Mermaid.js diagrams for system architecture and processes
- 🌐 **Multi-language**: Supports all major programming languages
- ⚙️ **Configurable**: Flexible YAML-based configuration with Pydantic models
- 🔄 **Cross-platform**: Works on macOS, Linux, and Windows
- 🐍 **Python 3.7+**: Compatible with modern Python versions

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/sourcescribe.git
cd sourcescribe-core

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

## Quick Start

### 1. Configure API Keys

Set up your LLM API keys as environment variables:

```bash
export ANTHROPIC_API_KEY="your-anthropic-key"
export OPENAI_API_KEY="your-openai-key"
# Ollama runs locally, no key needed
```

### 2. Initialize a Project

```bash
sourcescribe init /path/to/your/project
```

This creates a `.sourcescribe.yaml` configuration file.

### 3. Generate Documentation

```bash
# One-time generation
sourcescribe generate /path/to/your/project

# Watch mode (auto-regenerate on changes)
sourcescribe watch /path/to/your/project
```

## Configuration

Example `.sourcescribe.yaml`:

```yaml
# LLM Provider Configuration
llm:
  provider: "anthropic"  # anthropic, openai, or ollama
  model: "claude-3-5-sonnet-20241022"
  temperature: 0.3
  max_tokens: 4000

# Repository Settings
repository:
  path: "."
  exclude_patterns:
    - "*.pyc"
    - "__pycache__"
    - "node_modules"
    - ".git"
  include_patterns:
    - "*.py"
    - "*.js"
    - "*.ts"
    - "*.java"
    - "*.go"

# Documentation Output
output:
  path: "./docs/generated"
  format: "markdown"
  include_diagrams: true
  diagram_format: "mermaid"

# Watch Mode Settings
watch:
  enabled: true
  debounce_seconds: 2.0
  batch_changes: true

# Documentation Style
style:
  include_examples: true
  include_architecture: true
  include_api_docs: true
  verbosity: "detailed"  # minimal, normal, detailed
```

## Usage Examples

### Generate Documentation for a Python Project

```bash
sourcescribe generate --provider anthropic --output ./docs
```

### Watch Mode with Custom Config

```bash
sourcescribe watch --config custom-config.yaml
```

### Generate Only Architecture Diagrams

```bash
sourcescribe generate --diagrams-only
```

## Architecture

SourceScribe consists of several key components:

- **Engine**: Core documentation generation logic with LLM orchestration
- **Watch**: File system monitoring and change detection
- **API**: LLM provider integrations (Anthropic, OpenAI, Ollama)
- **Config**: Pydantic-based configuration management
- **Utils**: Helper functions for parsing, formatting, and analysis

## How It Works

1. **Code Analysis**: Parses source files using tree-sitter for AST analysis
2. **Change Detection**: Monitors file system for modifications (in watch mode)
3. **Context Building**: Extracts relevant code context, dependencies, and structure
4. **LLM Processing**: Sends code context to LLM for intelligent documentation generation
5. **Diagram Generation**: Creates Mermaid.js architecture and flow diagrams
6. **Output**: Writes formatted markdown documentation with embedded diagrams

## Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black sourcescribe/

# Type checking
mypy sourcescribe/

# Linting
ruff check sourcescribe/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Inspired by [CodeWiki](https://github.com/FSoft-AI4Code/CodeWiki)
- Research paper: [arXiv:2510.24428v2](https://arxiv.org/html/2510.24428v2)
