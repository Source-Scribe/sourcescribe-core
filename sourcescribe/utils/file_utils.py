"""File utility functions."""

import os
from pathlib import Path
from typing import List, Optional, Set
import fnmatch


# Map file extensions to programming languages
LANGUAGE_MAP = {
    '.py': 'python',
    '.js': 'javascript',
    '.jsx': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.java': 'java',
    '.go': 'go',
    '.rs': 'rust',
    '.c': 'c',
    '.cpp': 'cpp',
    '.cc': 'cpp',
    '.cxx': 'cpp',
    '.h': 'c',
    '.hpp': 'cpp',
    '.cs': 'csharp',
    '.rb': 'ruby',
    '.php': 'php',
    '.swift': 'swift',
    '.kt': 'kotlin',
    '.kts': 'kotlin',
    '.scala': 'scala',
    '.r': 'r',
    '.R': 'r',
    '.m': 'objective-c',
    '.mm': 'objective-c',
    '.pl': 'perl',
    '.lua': 'lua',
    '.sh': 'bash',
    '.bash': 'bash',
    '.zsh': 'zsh',
    '.fish': 'fish',
    '.sql': 'sql',
    '.html': 'html',
    '.css': 'css',
    '.scss': 'scss',
    '.sass': 'sass',
    '.vue': 'vue',
    '.md': 'markdown',
    '.json': 'json',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.toml': 'toml',
    '.xml': 'xml',
}


def read_file(file_path: str, encoding: str = 'utf-8') -> str:
    """
    Read file content.
    
    Args:
        file_path: Path to file
        encoding: File encoding
        
    Returns:
        File content as string
    """
    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        return f.read()


def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> None:
    """
    Write content to file.
    
    Args:
        file_path: Path to file
        content: Content to write
        encoding: File encoding
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding=encoding) as f:
        f.write(content)


def find_files(
    root_path: str,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    max_size: Optional[int] = None,
    follow_symlinks: bool = False
) -> List[str]:
    """
    Find files matching patterns.
    
    Args:
        root_path: Root directory to search
        include_patterns: Glob patterns to include
        exclude_patterns: Glob patterns to exclude
        max_size: Maximum file size in bytes
        follow_symlinks: Follow symbolic links
        
    Returns:
        List of matching file paths
    """
    root = Path(root_path).resolve()
    found_files = []
    
    # Default patterns
    if include_patterns is None:
        include_patterns = ['*']
    if exclude_patterns is None:
        exclude_patterns = []
    
    for path in root.rglob('*'):
        # Skip if symlink and not following
        if path.is_symlink() and not follow_symlinks:
            continue
        
        # Only process files
        if not path.is_file():
            continue
        
        # Get relative path for pattern matching
        try:
            rel_path = path.relative_to(root)
        except ValueError:
            continue
        
        rel_path_str = str(rel_path)
        
        # Check exclude patterns
        if any(fnmatch.fnmatch(rel_path_str, pattern) or
               fnmatch.fnmatch(path.name, pattern)
               for pattern in exclude_patterns):
            continue
        
        # Check include patterns
        if not any(fnmatch.fnmatch(rel_path_str, pattern) or
                   fnmatch.fnmatch(path.name, pattern)
                   for pattern in include_patterns):
            continue
        
        # Check file size
        if max_size and path.stat().st_size > max_size:
            continue
        
        found_files.append(str(path))
    
    return sorted(found_files)


def get_file_language(file_path: str) -> str:
    """
    Detect programming language from file extension.
    
    Args:
        file_path: Path to file
        
    Returns:
        Language name or 'unknown'
    """
    ext = Path(file_path).suffix.lower()
    return LANGUAGE_MAP.get(ext, 'unknown')


def is_text_file(file_path: str) -> bool:
    """
    Check if file is likely a text file.
    
    Args:
        file_path: Path to file
        
    Returns:
        True if text file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(1024)
        return True
    except (UnicodeDecodeError, PermissionError):
        return False


def get_relative_path(file_path: str, root_path: str) -> str:
    """
    Get relative path from root.
    
    Args:
        file_path: Full file path
        root_path: Root directory
        
    Returns:
        Relative path
    """
    try:
        return str(Path(file_path).relative_to(Path(root_path)))
    except ValueError:
        return file_path


def create_directory(dir_path: str) -> None:
    """
    Create directory if it doesn't exist.
    
    Args:
        dir_path: Directory path
    """
    Path(dir_path).mkdir(parents=True, exist_ok=True)
