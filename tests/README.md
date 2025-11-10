# SourceScribe Test Suite

This directory contains comprehensive unit and integration tests for SourceScribe.

## Test Structure

### Core Tests
- `test_config.py` - Configuration model tests
- `test_diagram.py` - Mermaid diagram generation tests
- `test_exclusions.py` - File exclusion pattern tests
- `test_file_utils.py` - File utility function tests
- `test_parser.py` - Code parsing tests

### v1.2.x Feature Tests

#### `test_sidebar_generation.py`
Tests for dynamic Docusaurus sidebar generation (v1.2.1):
- Scans actual documentation structure
- Builds sidebar items with correct ordering
- Handles path prefixes for subdirectories
- Ignores README files in subdirectories
- Generates valid TypeScript sidebar configuration

#### `test_docusaurus_config.py`
Tests for AI-powered Docusaurus configuration (v1.2.2):
- Infers project titles from `package.json` and `pyproject.toml`
- Generates AI-powered taglines with fallback
- Creates complete Docusaurus config with Mermaid.js support
- Removes all "Tutorial" and `/docs/intro` references
- Handles missing GitHub URLs gracefully
- Validates GitHub Pages URL generation

#### `test_cloud_exclusions.py`
Tests for cloud storage and system directory exclusions (v1.2.1):
- Excludes cloud storage (Google Drive, Dropbox, OneDrive, iCloud Drive)
- Excludes system directories (Library, .Trash, Applications, .cache)
- Preserves standard exclusions (node_modules, .git, __pycache__)
- Excludes docs and website directories from scanning

#### `test_cli_safety.py`
Tests for CLI safety features (v1.2.1):
- Warns users when scanning from home directory
- Warns about scanning system directories
- Allows users to confirm and proceed if needed
- No warnings for normal project directories

#### `test_v1_2_integration.py`
End-to-end integration tests:
- Complete documentation generation workflow
- Sidebar generation reflects actual file structure
- Cloud storage protection in action
- Tagline generation with AI fallback
- Mermaid configuration validation
- No Tutorial references in final output

## Running Tests

### Run all tests:
```bash
pytest tests/
```

### Run specific test file:
```bash
pytest tests/test_sidebar_generation.py -v
```

### Run with coverage:
```bash
pytest tests/ --cov=sourcescribe --cov-report=html
```

### Run only v1.2.x tests:
```bash
pytest tests/test_sidebar_generation.py tests/test_docusaurus_config.py tests/test_cloud_exclusions.py tests/test_cli_safety.py tests/test_v1_2_integration.py -v
```

## Test Coverage

Current test status:
- **17/23 tests passing** (6 tests require API key mocking for full pass)
- Sidebar generation: ✅ 6/6 passing
- Cloud exclusions: ✅ 5/5 passing  
- CLI safety: ⚠️ Requires runner environment
- Docusaurus config: ⚠️ Some tests need API key mock
- Integration: ⚠️ Some tests need API key mock

## Notes

- Some tests require environment setup (API keys, git configuration)
- Integration tests use temporary directories for isolation
- Mock LLM providers are used where possible
- Tests validate both success and error handling paths
