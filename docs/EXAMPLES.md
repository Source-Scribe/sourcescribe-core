# SourceScribe Examples

This document provides practical examples of using SourceScribe.

## Basic Usage

### Generate Documentation Once

```bash
# Generate documentation for current directory
sourcescribe generate

# Generate for specific directory
sourcescribe generate /path/to/project

# Use specific provider
sourcescribe generate --provider openai --model gpt-4

# Custom output directory
sourcescribe generate --output ./my-docs
```

### Watch Mode

```bash
# Watch current directory
sourcescribe watch

# Watch specific directory
sourcescribe watch /path/to/project

# With custom config
sourcescribe watch --config my-config.yaml
```

## Configuration Examples

### Minimal Configuration

```yaml
llm:
  provider: "anthropic"
  model: "claude-3-5-sonnet-20241022"

repository:
  path: "."
  
output:
  path: "./docs"
```

### Python Project Configuration

```yaml
llm:
  provider: "anthropic"
  model: "claude-3-5-sonnet-20241022"
  temperature: 0.2

repository:
  path: "."
  include_patterns:
    - "*.py"
  exclude_patterns:
    - "*.pyc"
    - "__pycache__"
    - "venv"
    - ".venv"
    - "tests"

output:
  path: "./docs/generated"
  include_diagrams: true

style:
  include_examples: true
  include_api_docs: true
  verbosity: "detailed"
```

### JavaScript/Node.js Project

```yaml
llm:
  provider: "openai"
  model: "gpt-4-turbo-preview"

repository:
  path: "./src"
  include_patterns:
    - "*.js"
    - "*.jsx"
    - "*.ts"
    - "*.tsx"
  exclude_patterns:
    - "node_modules"
    - "dist"
    - "build"

output:
  path: "./docs/api"
  include_diagrams: true

style:
  include_architecture: true
  include_api_docs: true
```

### Using Ollama (Local LLM)

```yaml
llm:
  provider: "ollama"
  model: "llama2"
  base_url: "http://localhost:11434"
  temperature: 0.3

repository:
  path: "."

output:
  path: "./docs"
```

## Python API Examples

### Basic Generation

```python
from sourcescribe import DocumentationGenerator, SourceScribeConfig

# Create config
config = SourceScribeConfig()
config.repository.path = "./my-project"
config.output.path = "./docs"

# Generate documentation
generator = DocumentationGenerator(config)
generator.generate_documentation()
```

### Custom Configuration

```python
from sourcescribe.config.models import (
    SourceScribeConfig,
    LLMConfig,
    RepositoryConfig,
    OutputConfig,
)

# Create custom config
config = SourceScribeConfig(
    llm=LLMConfig(
        provider="anthropic",
        model="claude-3-5-sonnet-20241022",
        temperature=0.3,
    ),
    repository=RepositoryConfig(
        path="./src",
        include_patterns=["*.py", "*.js"],
    ),
    output=OutputConfig(
        path="./docs",
        include_diagrams=True,
    ),
)

# Generate
generator = DocumentationGenerator(config)
generator.generate_documentation()
```

### Watch Mode in Code

```python
from sourcescribe import DocumentationGenerator
from sourcescribe.watch import FileWatcher
from sourcescribe.config.loader import ConfigLoader

# Load config
config = ConfigLoader.load_or_default()

# Create generator
generator = DocumentationGenerator(config)

# Define callback
def on_changes(files):
    print(f"Processing {len(files)} changed files...")
    generator.process_changes(files)

# Start watcher
watcher = FileWatcher(
    root_path=config.repository.path,
    callback=on_changes,
    watch_config=config.watch,
    repo_config=config.repository,
)

# Run in watch mode
watcher.run()
```

### Generate Specific Diagrams

```python
from sourcescribe.engine.diagram import DiagramGenerator

generator = DiagramGenerator()

# Architecture diagram
modules = [
    {'name': 'Frontend', 'dependencies': ['API']},
    {'name': 'API', 'dependencies': ['Database']},
    {'name': 'Database', 'dependencies': []},
]
arch_diagram = generator.generate_architecture_diagram(modules)

# Flow diagram
steps = [
    {'text': 'User Request', 'type': 'process'},
    {'text': 'Authenticate?', 'type': 'decision'},
    {'text': 'Process Request', 'type': 'process'},
    {'text': 'Return Response', 'type': 'process'},
]
flow_diagram = generator.generate_flow_diagram(steps)

# Save to file
with open('architecture.md', 'w') as f:
    f.write(arch_diagram)
```

### Analyze Code Structure

```python
from sourcescribe.engine.analyzer import CodeAnalyzer

analyzer = CodeAnalyzer()

# Analyze single file
analysis = analyzer.analyze_file('myfile.py')
print(f"Found {len(analysis['elements'])} code elements")

# Analyze multiple files
files = ['file1.py', 'file2.py', 'file3.py']
analyses = analyzer.analyze_files(files)

# Build module map
module_map = analyzer.build_module_map(analyses)
for name, info in module_map.items():
    print(f"{name}: {info['num_classes']} classes, {info['num_functions']} functions")
```

## Integration Examples

### GitHub Actions

```yaml
# .github/workflows/docs.yml
name: Generate Documentation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  docs:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install SourceScribe
      run: |
        pip install sourcescribe
    
    - name: Generate Documentation
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      run: |
        sourcescribe generate --output ./docs
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Regenerate documentation on commit
sourcescribe generate --output ./docs

# Add generated docs to commit
git add docs/
```

### CI/CD Pipeline

```bash
# In your CI script
pip install sourcescribe

# Validate config
sourcescribe validate

# Generate docs
sourcescribe generate

# Check if docs were generated
if [ -d "docs/generated" ]; then
  echo "Documentation generated successfully"
else
  echo "Documentation generation failed"
  exit 1
fi
```

## Advanced Examples

### Custom LLM Provider

```python
from sourcescribe.api.base import BaseLLMProvider, LLMMessage, LLMResponse

class CustomProvider(BaseLLMProvider):
    def generate(self, messages, system_prompt=None, **kwargs):
        # Your custom implementation
        # Call your LLM API here
        response_text = self._call_custom_api(messages)
        
        return LLMResponse(
            content=response_text,
            model=self.model,
            usage={'total_tokens': 100},
        )
    
    def generate_streaming(self, messages, system_prompt=None, **kwargs):
        # Streaming implementation
        for chunk in self._call_custom_api_streaming(messages):
            yield chunk

# Use custom provider
config = SourceScribeConfig()
generator = DocumentationGenerator(config)
generator.llm_provider = CustomProvider(model="custom-model")
generator.generate_documentation()
```

### Multi-Repository Documentation

```python
import os
from sourcescribe import DocumentationGenerator, SourceScribeConfig

repos = [
    '/path/to/repo1',
    '/path/to/repo2',
    '/path/to/repo3',
]

for repo_path in repos:
    print(f"Documenting {repo_path}...")
    
    config = SourceScribeConfig()
    config.repository.path = repo_path
    config.output.path = f"./docs/{os.path.basename(repo_path)}"
    
    generator = DocumentationGenerator(config)
    generator.generate_documentation()

print("All repositories documented!")
```

These examples should help you get started with SourceScribe. For more information, see the main [README.md](../README.md).
