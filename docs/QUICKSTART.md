# Quick Start Guide

Get up and running with SourceScribe in minutes!

## Installation

### From Source

```bash
git clone https://github.com/yourusername/sourcescribe.git
cd sourcescribe-core
pip install -e .
```

### Using pip (when published)

```bash
pip install sourcescribe
```

## Setup

### 1. Set API Keys

Choose your LLM provider and set the appropriate API key:

**For Anthropic Claude:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**For OpenAI:**
```bash
export OPENAI_API_KEY="sk-..."
```

**For Ollama (local):**
```bash
# No API key needed - just ensure Ollama is running
ollama serve
```

### 2. Initialize Configuration

Navigate to your project and initialize SourceScribe:

```bash
cd /path/to/your/project
sourcescribe init
```

This creates a `.sourcescribe.yaml` configuration file.

### 3. Generate Documentation

```bash
sourcescribe generate
```

Your documentation will be generated in `./docs/generated/` by default.

## Basic Usage

### Generate Once

```bash
# Generate for current directory
sourcescribe generate

# Generate for specific directory
sourcescribe generate /path/to/project

# Use specific output directory
sourcescribe generate --output ./my-docs
```

### Watch Mode (Auto-regenerate)

```bash
# Watch current directory
sourcescribe watch

# Watch specific directory
sourcescribe watch /path/to/project
```

Press `Ctrl+C` to stop watching.

### Using Different Providers

```bash
# Use OpenAI instead of default Anthropic
sourcescribe generate --provider openai --model gpt-4

# Use Ollama (local)
sourcescribe generate --provider ollama --model llama2
```

## Configuration

Edit `.sourcescribe.yaml` to customize:

```yaml
llm:
  provider: "anthropic"
  model: "claude-3-5-sonnet-20241022"
  temperature: 0.3

repository:
  path: "."
  include_patterns:
    - "*.py"
    - "*.js"
    - "*.ts"

output:
  path: "./docs/generated"
  include_diagrams: true

style:
  verbosity: "detailed"
```

## Examples

### Document a Python Project

```bash
cd my-python-project
sourcescribe init
sourcescribe generate
```

### Document a JavaScript Project

```bash
cd my-js-project
sourcescribe init
# Edit .sourcescribe.yaml to include *.js, *.jsx, *.ts, *.tsx
sourcescribe generate
```

### Watch Mode with Custom Config

```bash
sourcescribe watch --config custom-config.yaml
```

## Output Structure

After generation, you'll find:

```
docs/generated/
├── README.md              # Index of all documentation
├── OVERVIEW.md            # Project overview
├── ARCHITECTURE.md        # Architecture with diagrams
├── API.md                 # API documentation (if applicable)
└── files/                 # Individual file documentation
    ├── module1.py.md
    ├── module2.py.md
    └── ...
```

## Tips

1. **Start with defaults** - The default configuration works for most projects
2. **Use watch mode** - Automatically updates docs as you code
3. **Review generated docs** - The LLM does its best, but review for accuracy
4. **Customize verbosity** - Use `minimal`, `normal`, or `detailed` based on needs
5. **Exclude test files** - Add test directories to `exclude_patterns`

## Troubleshooting

### "No API key" Error

```bash
# Make sure you've exported your API key
echo $ANTHROPIC_API_KEY  # Should show your key

# Or set it in your shell profile (~/.bashrc, ~/.zshrc)
export ANTHROPIC_API_KEY="your-key"
```

### "No configuration found" Error

```bash
# Initialize configuration first
sourcescribe init
```

### Rate Limiting

If you hit API rate limits:
- Reduce the number of files (use `include_patterns`)
- Use a local LLM with Ollama
- Wait and retry

## Next Steps

- Read the [Examples](EXAMPLES.md) for advanced usage
- Check [Contributing](CONTRIBUTING.md) to help improve SourceScribe
- See the main [README](../README.md) for full documentation

## Getting Help

- Check existing [issues](https://github.com/yourusername/sourcescribe/issues)
- Open a new issue for bugs
- Start a discussion for questions

Happy documenting! 📝
