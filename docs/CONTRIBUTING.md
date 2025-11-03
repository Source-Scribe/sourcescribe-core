# Contributing to SourceScribe

Thank you for your interest in contributing to SourceScribe! This document provides guidelines for contributing to the project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sourcescribe.git
   cd sourcescribe-core
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements-dev.txt
   pip install -e .
   ```

4. **Set up API keys**
   ```bash
   export ANTHROPIC_API_KEY="your-key"
   export OPENAI_API_KEY="your-key"
   ```

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=sourcescribe tests/

# Run specific test file
pytest tests/test_config.py
```

## Code Style

We use the following tools for code quality:

- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

```bash
# Format code
black sourcescribe/

# Lint code
ruff check sourcescribe/

# Type check
mypy sourcescribe/
```

## Project Structure

```
sourcescribe-core/
├── sourcescribe/
│   ├── engine/       # Core documentation generation
│   ├── watch/        # File watching
│   ├── config/       # Configuration management
│   ├── utils/        # Utilities
│   └── api/          # LLM provider integrations
├── tests/            # Test files
└── docs/             # Documentation
```

## Adding a New Feature

1. **Create a feature branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Write tests first** (TDD approach)
   - Add tests in `tests/`
   - Ensure tests fail initially

3. **Implement the feature**
   - Follow existing code style
   - Add docstrings to functions/classes
   - Keep functions focused and small

4. **Update documentation**
   - Update README.md if needed
   - Add docstrings and comments
   - Update CHANGELOG.md

5. **Run tests and checks**
   ```bash
   pytest tests/
   black sourcescribe/
   ruff check sourcescribe/
   mypy sourcescribe/
   ```

6. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   git push origin feat/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide clear description
   - Reference any related issues
   - Ensure CI passes

## Adding a New LLM Provider

To add support for a new LLM provider:

1. Create a new provider class in `sourcescribe/api/`
2. Inherit from `BaseLLMProvider`
3. Implement `generate()` and `generate_streaming()` methods
4. Update `LLMProviderFactory` in `factory.py`
5. Add tests in `tests/`

Example:
```python
from sourcescribe.api.base import BaseLLMProvider, LLMMessage, LLMResponse

class NewProvider(BaseLLMProvider):
    def generate(self, messages, system_prompt=None, **kwargs):
        # Implementation
        pass
    
    def generate_streaming(self, messages, system_prompt=None, **kwargs):
        # Implementation
        pass
```

## Adding Language Support

To improve parsing for a new language:

1. Update `LANGUAGE_MAP` in `sourcescribe/utils/file_utils.py`
2. Add parsing logic in `CodeParser._parse_<language>()` in `sourcescribe/utils/parser.py`
3. Add tests for the new language

## Commit Message Format

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `style:` Code style changes
- `chore:` Maintenance tasks

Example: `feat: add support for Gemini API`

## Pull Request Guidelines

- Keep PRs focused on a single feature/fix
- Write clear PR descriptions
- Update tests
- Ensure all CI checks pass
- Request review from maintainers

## Reporting Issues

When reporting issues, include:

- SourceScribe version
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

## Code Review Process

1. Maintainer reviews PR
2. Feedback provided via comments
3. Author makes requested changes
4. Maintainer approves and merges

## Questions?

- Open an issue for bugs/features
- Start a discussion for questions
- Check existing issues first

Thank you for contributing! 🎉
