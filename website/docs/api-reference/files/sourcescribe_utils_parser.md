# SourceScribe Code Parser Documentation

## File Purpose and Overview

The `parser.py` file in the `sourcescribe/utils` directory of the SourceScribe project contains utilities for parsing source code and extracting its structure and elements. The main components are the `CodeElement` class and the `CodeParser` class.

The `CodeElement` class represents a code element, such as a function, class, or method, and contains information about its name, type, start and end lines, docstring, signature, parameters, and body.

The `CodeParser` class is responsible for parsing source code and extracting the code elements. It supports parsing for various programming languages, including Python, JavaScript/TypeScript, Java, and C/C++.

## Main Components

### `CodeElement` Class

The `CodeElement` class represents a code element and has the following attributes:

- `name`: The name of the code element (e.g., function name, class name).
- `type`: The type of the code element (e.g., 'function', 'class', 'method').
- `start_line`: The starting line number of the code element.
- `end_line`: The ending line number of the code element.
- `docstring`: The docstring of the code element (if available).
- `signature`: The signature of the code element (e.g., function signature).
- `params`: The parameters of the code element (for functions).
- `body`: The body of the code element (if available).

### `CodeParser` Class

The `CodeParser` class is responsible for parsing source code and extracting the code elements. It has the following main methods:

1. `__init__(self, language: str)`: Initializes the parser for a specific programming language.
2. `parse(self, code: str, file_path: Optional[str] = None) -> Dict[str, Any]`: Parses the given source code and returns a dictionary with the parsed information, including the language, imports, code elements, and the total number of lines.
3. `_parse_python(self, code: str) -> Dict[str, Any]`: Parses Python code and extracts imports, classes, and functions.
4. `_parse_javascript(self, code: str) -> Dict[str, Any]`: Parses JavaScript/TypeScript code and extracts imports, functions, and classes.
5. `_parse_java(self, code: str) -> Dict[str, Any]`: Parses Java code and extracts imports, classes, and methods.
6. `_parse_c_cpp(self, code: str) -> Dict[str, Any]`: Parses C/C++ code and extracts includes and functions.
7. `_parse_generic(self, code: str) -> Dict[str, Any]`: Provides a generic parsing implementation for unsupported languages.

## Key Functionality

The main functionality of this code is to parse source code and extract its structure and elements, such as imports, classes, functions, and methods. This information can be used for various purposes, such as code analysis, documentation generation, or code navigation.

The `CodeParser` class supports parsing for several popular programming languages, and it can be extended to support additional languages as needed.

## Dependencies and Imports

The `parser.py` file imports the following modules:

- `re`: Used for regular expression matching.
- `typing`: Provides type annotations for the function parameters and return values.
- `dataclasses`: Used to define the `CodeElement` class as a dataclass.
- `pathlib`: Provides the `Path` class for working with file paths.

## Usage Examples

Here's an example of how to use the `CodeParser` class to parse Python code:

```python
from sourcescribe.utils.parser import CodeParser

parser = CodeParser('python')
parsed_code = parser.parse("""
def my_function(a, b):
    """Adds two numbers."""
    return a + b
""")

print(parsed_code)
# Output:
# {
#     'language': 'python',
#     'imports': [],
#     'elements': [
#         CodeElement(
#             name='my_function',
#             type='function',
#             start_line=2,
#             end_line=4,
#             docstring='Adds two numbers.',
#             signature='def my_function(a, b):',
#             params=['a', 'b'],
#             body=None
#         )
#     ],
#     'total_lines': 4
# }
```

## Important Implementation Details

1. The `_parse_python` method uses regular expressions to extract imports, classes, and functions from the Python code. It also attempts to extract the docstring for each function.
2. The `_parse_javascript` method extracts imports, functions (both regular and arrow functions), and classes from JavaScript/TypeScript code.
3. The `_parse_java` method extracts imports, classes, and methods from Java code.
4. The `_parse_c_cpp` method extracts includes and functions from C/C++ code.
5. The `_parse_generic` method provides a fallback implementation for parsing code in unsupported languages.
6. The `_find_block_end` helper function is used to determine the end line of a code block (e.g., a function or class).
7. The `_extract_python_docstring` helper function is used to extract the docstring from Python code.

Overall, this code provides a flexible and extensible way to parse source code and extract its structure and elements, which can be useful for a variety of software engineering tasks.