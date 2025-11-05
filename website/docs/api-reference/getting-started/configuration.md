# Configuration

# SourceScribe Configuration

SourceScribe is a powerful documentation generation tool that uses AI-powered analysis to create user-friendly technical documentation. This guide covers the various configuration options available to customize the behavior and output of SourceScribe.

## Configuration Files

SourceScribe supports configuration via YAML files. By default, it looks for a `sourcescribe.yml` file in the current working directory. You can also specify a custom configuration file using the `--config` CLI option.

The configuration file follows this structure:

```yaml
# sourcescribe.yml
providers:
  openai:
    api_key: YOUR_OPENAI_API_KEY
  anthropic:
    api_key: YOUR_ANTHROPIC_API_KEY
  ollama:
    api_key: YOUR_OLLAMA_API_KEY
  
output:
  directory: docs
  format: markdown

analysis:
  max_tokens: 4096
  temperature: 0.7

exclusions:
  - "tests/**"
  - "venv/**"
  - "*.pyc"
```

## Configuration Options

The following configuration options are available:

| Option | Description | Default |
| --- | --- | --- |
| `providers.openai.api_key` | Your OpenAI API key | `None` |
| `providers.anthropic.api_key` | Your Anthropic API key | `None` |
| `providers.ollama.api_key` | Your Ollama API key | `None` |
| `output.directory` | The directory to output the generated documentation | `"docs"` |
| `output.format` | The output format (currently only supports `"markdown"`) | `"markdown"` |
| `analysis.max_tokens` | The maximum number of tokens to use for the AI analysis | `4096` |
| `analysis.temperature` | The temperature parameter for the AI model (controls creativity/randomness) | `0.7` |
| `exclusions` | A list of file/directory patterns to exclude from the analysis | `["tests/**", "venv/**", "*.pyc"]` |

### Environment Variables

SourceScribe also supports the following environment variables:

| Variable | Description |
| --- | --- |
| `SOURCESCRIBE_OPENAI_API_KEY` | Your OpenAI API key |
| `SOURCESCRIBE_ANTHROPIC_API_KEY` | Your Anthropic API key |
| `SOURCESCRIBE_OLLAMA_API_KEY` | Your Ollama API key |
| `SOURCESCRIBE_CONFIG_FILE` | Path to a custom configuration file |

## Configuration Examples

### Basic Configuration

```yaml
providers:
  openai:
    api_key: sk-ABC123DEF456GHI789JKL
output:
  directory: docs
  format: markdown
```

This configuration uses the OpenAI provider with the specified API key, and outputs the generated documentation in Markdown format to the `docs` directory.

### Advanced Configuration

```yaml
providers:
  openai:
    api_key: sk-ABC123DEF456GHI789JKL
  anthropic:
    api_key: ANTHROPIC_API_KEY_HERE
  ollama:
    api_key: OLLAMA_API_KEY_HERE

output:
  directory: documentation
  format: markdown

analysis:
  max_tokens: 8192
  temperature: 0.5

exclusions:
  - "tests/**"
  - "venv/**"
  - "*.pyc"
  - "*.md"
```

This configuration uses all three available providers (OpenAI, Anthropic, and Ollama), with the specified API keys. The generated documentation is output in Markdown format to the `documentation` directory. The analysis settings have been adjusted to use a higher maximum token count and a lower temperature. Additionally, the configuration excludes several directories and file types from the analysis.

## Best Practices

- **Use Environment Variables**: Store sensitive API keys in environment variables rather than in the configuration file.
- **Adjust Analysis Settings**: Experiment with the `max_tokens` and `temperature` settings to find the optimal balance between detail and conciseness.
- **Customize Exclusions**: Ensure that you exclude any files or directories that are not relevant to the generated documentation, such as tests, build artifacts, and documentation sources.
- **Review Output Regularly**: Periodically review the generated documentation to ensure it meets your requirements and make adjustments to the configuration as needed.

By following these best practices, you can ensure that SourceScribe generates high-quality, user-friendly documentation that meets the specific needs of your project.