# Configuration

# SourceScribe Configuration

SourceScribe is a powerful documentation generation tool that allows you to create comprehensive, user-centric technical documentation from your source code. This guide covers the various configuration options available to customize the behavior and output of SourceScribe.

## Configuration Files

SourceScribe supports configuration via YAML files. By default, it looks for a `sourcescribe.yml` file in the current working directory. You can also specify a custom configuration file path using the `--config` CLI option.

The configuration file follows a simple structure with top-level keys for the different settings categories.

## Configuration Options

The following table outlines the available configuration options for SourceScribe:

| Option | Description | Default |
| --- | --- | --- |
| `output_dir` | The directory where the generated documentation will be saved. | `./docs` |
| `source_dir` | The directory containing the source code to be documented. | `./` |
| `exclude_dirs` | A list of directories to exclude from the documentation generation. | `[]` |
| `exclude_files` | A list of files to exclude from the documentation generation. | `[]` |
| `api_providers` | A list of API providers to use for feature extraction. Supported providers: `anthropic`, `openai`, `ollama`. | `['openai']` |
| `api_keys` | A dictionary of API keys for the configured providers. | `{}` |
| `max_tokens` | The maximum number of tokens to use for feature extraction. | `2048` |
| `temperature` | The temperature to use for feature extraction. Higher values result in more creative output. | `0.7` |
| `top_p` | The top-p value to use for feature extraction. Controls the diversity of the output. | `0.9` |
| `diagrams` | A dictionary of settings for the various diagram types: <br> - `sequence`: Sequence diagrams <br> - `flowchart`: Flowcharts <br> - `class`: Class diagrams <br> - `state`: State diagrams | `{}` |
| `watch` | Settings for the file watcher feature: <br> - `enabled`: Whether to enable the file watcher <br> - `interval`: The interval (in seconds) to check for file changes | `{"enabled": false, "interval": 5}` |

## Environment Variables

SourceScribe supports the following environment variables:

| Variable | Description | Required |
| --- | --- | --- |
| `SOURCESCRIBE_CONFIG_FILE` | The path to the SourceScribe configuration file. | No |
| `ANTHROPIC_API_KEY` | The API key for the Anthropic API provider. | Yes, if using the Anthropic provider |
| `OPENAI_API_KEY` | The API key for the OpenAI API provider. | Yes, if using the OpenAI provider |
| `OLLAMA_API_KEY` | The API key for the Ollama API provider. | Yes, if using the Ollama provider |

## Examples

### Minimal Configuration

```yaml
output_dir: ./docs
source_dir: ./
api_providers:
  - openai
api_keys:
  openai: YOUR_OPENAI_API_KEY
```

### Advanced Configuration

```yaml
output_dir: ./generated-docs
source_dir: ./src
exclude_dirs:
  - tests
  - examples
exclude_files:
  - setup.py
api_providers:
  - openai
  - anthropic
api_keys:
  openai: YOUR_OPENAI_API_KEY
  anthropic: YOUR_ANTHROPIC_API_KEY
max_tokens: 4096
temperature: 0.5
top_p: 0.8
diagrams:
  sequence:
    theme: dark
  flowchart:
    theme: forest
watch:
  enabled: true
  interval: 10
```

## Best Practices

- Use environment variables for sensitive information like API keys to avoid committing them to version control.
- Experiment with the `max_tokens`, `temperature`, and `top_p` settings to find the optimal balance between conciseness and creativity in the generated documentation.
- Customize the diagram settings to match the visual style of your project's documentation.
- Enable the file watcher to automatically regenerate the documentation when source files change.
- Regularly review the generated documentation to ensure it accurately reflects the current state of your project.