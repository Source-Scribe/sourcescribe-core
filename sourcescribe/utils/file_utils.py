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


def sanitize_mdx_content(content: str) -> str:
    """
    Sanitize markdown content to be MDX-compatible.
    
    Escapes patterns that MDX might interpret as JSX but aren't valid.
    
    Args:
        content: Markdown content to sanitize
        
    Returns:
        Sanitized content safe for MDX
    """
    import re
    
    # Split content by code blocks to avoid modifying code
    parts = re.split(r'(```[\s\S]*?```|`[^`]+`)', content)
    
    # Process each non-code part
    for i in range(len(parts)):
        if not (parts[i].startswith('```') or parts[i].startswith('`')):
            # 1. Fix unclosed HTML tags (br, hr, img, etc.) -> self-closing
            # Match: <br>, <hr>, <img ...>, etc. (not already self-closing)
            parts[i] = re.sub(
                r'<(br|hr|img|input|meta|link)(\s+[^>]*?)?>(?!\s*/)',
                r'<\1\2 />',
                parts[i],
                flags=re.IGNORECASE
            )
            
            # 2. Escape invalid self-closing tags (with dots, dashes, lowercase)
            def escape_invalid_jsx(match):
                tag = match.group(0)
                tag_name = tag[1:-2].strip()  # Remove < and />
                
                # If it has dots, dashes, starts with lowercase, or has slashes, escape it
                if ('.' in tag_name or '-' in tag_name or 
                    (tag_name and tag_name[0].islower()) or
                    '/' in tag_name):
                    return f'`{tag}`'
                return tag
            
            # Match self-closing tags: <anything/>
            pattern = r'(?<!`)(?<!```)<([a-zA-Z.][\w._/\-]*)\s*/>'
            parts[i] = re.sub(pattern, escape_invalid_jsx, parts[i])
            
            # 3. Escape angle brackets around file paths like <path/to/file>
            parts[i] = re.sub(
                r'<([a-zA-Z0-9_\-./]+/[a-zA-Z0-9_\-./]+)>',
                r'`<\1>`',
                parts[i]
            )
            
            # 4. Escape URLs in angle brackets like <http://example.com>
            parts[i] = re.sub(
                r'<(https?://[^>]+)>',
                r'`<\1>`',
                parts[i]
            )
            
            # 5. Escape curly braces that look like JSX expressions but aren't valid
            # Match {word}, {snake_case}, {github_permalink} etc.
            # These cause "ReferenceError: variable is not defined" in MDX
            # Don't match: markdown links [...](url), inline code, or actual JSX props
            def escape_invalid_jsx_expression(match):
                full_match = match.group(0)
                var_name = match.group(1)
                
                # If it looks like a placeholder variable (letters, numbers, underscores, dots)
                # and not a complex JSX expression (no spaces, operators, etc.)
                if re.match(r'^[a-zA-Z_][a-zA-Z0-9_\.]*$', var_name):
                    # Escape it with backticks
                    return f'`{full_match}`'
                return full_match
            
            # Match {variable_name} patterns (not inside links or complex expressions)
            # Negative lookbehind to avoid matching inside markdown links
            parts[i] = re.sub(
                r'(?<!\])\{([a-zA-Z_][a-zA-Z0-9_\.]*)\}',
                escape_invalid_jsx_expression,
                parts[i]
            )
    
    return ''.join(parts)


def write_file(file_path: str, content: str, encoding: str = 'utf-8', sanitize_mdx: bool = False) -> None:
    """
    Write content to file.
    
    Args:
        file_path: Path to file
        content: Content to write
        encoding: File encoding (default: utf-8)
        sanitize_mdx: Whether to sanitize content for MDX compatibility (default: False)
    """
    file_obj = Path(file_path)
    file_obj.parent.mkdir(parents=True, exist_ok=True)
    
    # Sanitize MDX if requested and file is markdown
    if sanitize_mdx and (file_path.endswith('.md') or file_path.endswith('.mdx')):
        content = sanitize_mdx_content(content)
    
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
        # Check against full path, filename, and individual path components
        path_parts = rel_path.parts
        excluded = False
        for pattern in exclude_patterns:
            # Check full relative path
            if fnmatch.fnmatch(rel_path_str, pattern):
                excluded = True
                break
            # Check filename
            if fnmatch.fnmatch(path.name, pattern):
                excluded = True
                break
            # Check if any directory in the path matches (for patterns like "venv", "site-packages")
            if not any(c in pattern for c in ['*', '?', '[']):  # Simple pattern without wildcards
                if pattern in path_parts:
                    excluded = True
                    break
        
        if excluded:
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
        # Read first 8192 bytes as binary
        with open(file_path, 'rb') as f:
            chunk = f.read(8192)
        
        # Check for null bytes (common in binary files)
        if b'\x00' in chunk:
            return False
        
        # Try to decode as UTF-8
        try:
            chunk.decode('utf-8')
            return True
        except UnicodeDecodeError:
            # Try other common encodings
            for encoding in ['latin-1', 'cp1252']:
                try:
                    chunk.decode(encoding)
                    return True
                except UnicodeDecodeError:
                    continue
            return False
    except (IOError, PermissionError):
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
