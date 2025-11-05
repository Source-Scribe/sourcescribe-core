# Code Analyzer Documentation

## File Purpose and Overview

The `analyzer.py` file is part of the `sourcescribe-core` project and is responsible for analyzing code files and extracting relevant information. The `CodeAnalyzer` class provides the main functionality for this task, including:

- Analyzing a single file to extract metadata, code structure, and dependencies
- Analyzing a list of files and aggregating the results
- Building a module map that captures the relationships between different modules in the codebase
- Extracting API endpoints from the analyzed code

The code analysis and structure extraction performed by this module are crucial for the SourceScribe project, which aims to provide comprehensive documentation for software projects.

## Main Components

### `CodeAnalyzer` Class

The `CodeAnalyzer` class is the main component of this module. It provides the following key functionality:

#### `__init__(self, repo_config: Optional[RepositoryConfig] = None)`
Initializes the `CodeAnalyzer` instance with an optional `RepositoryConfig` object, which can be used to configure the analysis process.

#### `analyze_file(self, file_path: str) -> Dict[str, Any]`
Analyzes a single file at the given `file_path` and returns a dictionary containing the analysis results, including the file path, name, language, size, line count, code elements, imports, and includes.

#### `analyze_files(self, file_paths: List[str]) -> List[Dict[str, Any]]`
Analyzes a list of files specified by `file_paths` and returns a list of analysis results for each file.

#### `extract_dependencies(self, analysis: Dict[str, Any]) -> List[str]`
Extracts the dependencies from the file analysis dictionary, handling different programming language-specific patterns for imports and requires.

#### `build_module_map(self, analyses: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]`
Builds a map of modules and their relationships based on the provided file analyses. The module map includes information such as the module name, path, language, line count, dependencies, classes, and functions.

#### `extract_api_endpoints(self, analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]`
Extracts API endpoints from the file analyses, currently supporting patterns for Flask and FastAPI routes in Python.

## Key Functionality

The `CodeAnalyzer` class provides the following key functionality:

1. **File Analysis**: The `analyze_file` and `analyze_files` methods allow for the analysis of individual files or a list of files, respectively. The analysis includes extracting metadata, code structure, and dependencies.

2. **Module Mapping**: The `build_module_map` method aggregates the file analyses and constructs a comprehensive module map, capturing the relationships between different modules in the codebase.

3. **API Endpoint Extraction**: The `extract_api_endpoints` method scans the file analyses and extracts information about API endpoints, such as the HTTP method and the endpoint path.

These key functionalities are essential for the SourceScribe project, as they provide the necessary data for generating comprehensive documentation for software projects.

## Dependencies and Imports

The `analyzer.py` file depends on the following modules and classes:

- `typing`: For type annotations
- `pathlib.Path`: For working with file paths
- `sourcescribe.utils.file_utils`: For file-related utility functions
- `sourcescribe.utils.parser`: For parsing code content
- `sourcescribe.config.models`: For accessing repository configuration
- `sourcescribe.utils.logger`: For logging

## Usage Examples

The `CodeAnalyzer` class can be used as follows:

```python
from sourcescribe.engine.analyzer import CodeAnalyzer

# Analyze a single file
analyzer = CodeAnalyzer()
file_analysis = analyzer.analyze_file('/path/to/file.py')
print(file_analysis)

# Analyze multiple files
file_paths = ['/path/to/file1.py', '/path/to/file2.py', '/path/to/file3.py']
analyses = analyzer.analyze_files(file_paths)
for analysis in analyses:
    print(analysis)

# Build a module map
module_map = analyzer.build_module_map(analyses)
for module_name, module_info in module_map.items():
    print(f"Module: {module_name}")
    print(module_info)

# Extract API endpoints
api_endpoints = analyzer.extract_api_endpoints(analyses)
for endpoint in api_endpoints:
    print(endpoint)
```

## Important Implementation Details

1. **Language-specific Dependency Extraction**: The `extract_dependencies` method handles different programming language-specific patterns for imports and requires, such as `import x`, `from x import y`, and `require('x')`.

2. **Module Name Normalization**: When building the module map, the method normalizes dependencies to module names for internal imports, converting paths like `sourcescribe.engine.analyzer` to just `analyzer`.

3. **API Endpoint Extraction**: The `extract_api_endpoints` method currently supports the extraction of Flask and FastAPI routes in Python. It uses regular expressions to identify the HTTP method and the endpoint path.

4. **Error Handling**: The `analyze_file` method includes a try-except block to handle any exceptions that may occur during the analysis process, returning a dictionary with an error message in case of a failure.

5. **Logging**: The `CodeAnalyzer` class uses the `sourcescribe.utils.logger` module to log any errors that occur during the analysis process.