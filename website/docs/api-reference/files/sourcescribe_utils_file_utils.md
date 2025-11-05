# File Utility Functions

## Overview

The `file_utils.py` module provides a set of utility functions for working with files and directories in a Python project. These functions handle common file-related tasks such as reading, writing, and finding files, as well as detecting file types and creating directories.

## Main Components

The module defines the following functions:

1. `read_file(file_path: str, encoding: str = 'utf-8') -> str`
2. `write_file(file_path: str, content: str, encoding: str = 'utf-8') -> None`
3. `find_files(root_path: str, include_patterns: Optional[List[str]] = None, exclude_patterns: Optional[List[str]] = None, max_size: Optional[int] = None, follow_symlinks: bool = False) -> List[str]`
4. `get_file_language(file_path: str) -> str`
5. `is_text_file(file_path: str) -> bool`
6. `get_relative_path(file_path: str, root_path: str) -> str`
7. `create_directory(dir_path: str) -> None`

## Key Functionality

1. **Reading and Writing Files**: The `read_file()` and `write_file()` functions allow you to read the content of a file and write content to a file, respectively. These functions handle file encoding and automatically create directories if needed.

2. **Finding Files**: The `find_files()` function allows you to search for files within a given root directory, using include and exclude patterns, and filtering by maximum file size. This can be useful for tasks like indexing or processing a set of files.

3. **File Language Detection**: The `get_file_language()` function uses a predefined `LANGUAGE_MAP` to detect the programming language of a file based on its file extension.

4. **Text File Detection**: The `is_text_file()` function checks if a file is likely a text file by analyzing the first 8192 bytes of the file and looking for the presence of null bytes (common in binary files).

5. **Relative Path Retrieval**: The `get_relative_path()` function returns the relative path of a file with respect to a given root directory.

6. **Directory Creation**: The `create_directory()` function ensures that a directory and its parent directories are created if they don't already exist.

## Dependencies and Imports

The `file_utils.py` module imports the following Python standard library modules:

- `os`: For interacting with the operating system
- `pathlib`: For working with file paths
- `typing`: For type annotations
- `fnmatch`: For file pattern matching

## Usage Examples

Here are some examples of how to use the functions provided in the `file_utils.py` module:

```python
from sourcescribe.utils.file_utils import read_file, write_file, find_files, get_file_language, is_text_file, get_relative_path, create_directory

# Read file content
content = read_file('path/to/file.txt')

# Write content to a file
write_file('path/to/output.txt', 'Hello, World!')

# Find all Python files in a directory
python_files = find_files('path/to/directory', include_patterns=['*.py'])

# Get the programming language of a file
language = get_file_language('path/to/file.py')  # Output: 'python'

# Check if a file is a text file
is_text = is_text_file('path/to/file.txt')  # Output: True

# Get the relative path of a file
relative_path = get_relative_path('path/to/file.txt', 'path/to/directory')  # Output: 'file.txt'

# Create a directory if it doesn't exist
create_directory('path/to/new/directory')
```

## Implementation Details

1. The `LANGUAGE_MAP` dictionary is used to map file extensions to programming language names. This mapping can be extended as needed to support additional file types.

2. The `find_files()` function uses the `pathlib.Path.rglob()` method to recursively search for files in the specified root directory. It applies the provided include and exclude patterns to filter the results, and also checks the file size if a maximum size is specified.

3. The `is_text_file()` function reads the first 8192 bytes of the file and checks for the presence of null bytes, which are common in binary files. It then attempts to decode the bytes using UTF-8 and other common encodings to determine if the file is likely a text file.

4. The `get_relative_path()` function uses the `pathlib.Path.relative_to()` method to calculate the relative path of a file with respect to a given root directory. If the file path cannot be made relative, the original file path is returned.

5. The `create_directory()` function uses the `pathlib.Path.mkdir()` method to create a directory and its parent directories if they don't already exist.