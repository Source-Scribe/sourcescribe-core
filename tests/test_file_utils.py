"""Tests for file utility functions."""

import pytest
import tempfile
from pathlib import Path
from sourcescribe.utils.file_utils import (
    find_files,
    get_file_language,
    is_text_file,
    get_relative_path,
    sanitize_mdx_content,
    write_file,
    read_file,
)


def test_read_write_file():
    """Test reading and writing files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test.txt"
        content = "Hello, World!"
        
        # Write file
        write_file(str(file_path), content)
        
        # Read file
        read_content = read_file(str(file_path))
        
        assert read_content == content


def test_find_files():
    """Test finding files with patterns."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        (Path(tmpdir) / "test.py").touch()
        (Path(tmpdir) / "test.js").touch()
        (Path(tmpdir) / "test.txt").touch()
        (Path(tmpdir) / "ignore.pyc").touch()
        
        # Find Python files
        files = find_files(
            tmpdir,
            include_patterns=["*.py"],
            exclude_patterns=["*.pyc"]
        )
        
        assert len(files) == 1
        assert files[0].endswith("test.py")


def test_get_file_language():
    """Test detecting file language."""
    assert get_file_language("test.py") == "python"
    assert get_file_language("test.js") == "javascript"
    assert get_file_language("test.java") == "java"
    assert get_file_language("test.go") == "go"
    assert get_file_language("test.unknown") == "unknown"


def test_is_text_file():
    """Test checking if file is text."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create text file
        text_file = Path(tmpdir) / "text.txt"
        text_file.write_text("Hello")
        
        # Create binary file
        bin_file = Path(tmpdir) / "binary.bin"
        bin_file.write_bytes(b'\x00\x01\x02\x03')
        
        assert is_text_file(str(text_file)) is True
        assert is_text_file(str(bin_file)) is False


def test_sanitize_mdx_invalid_jsx():
    """Test sanitizing invalid JSX patterns."""
    # Self-closing tags with dots (file references)
    content = "Use the <config.js/> file"
    sanitized = sanitize_mdx_content(content)
    assert "`<config.js/>`" in sanitized
    
    # Self-closing tags with dashes
    content = "Component <my-component/> is used"
    sanitized = sanitize_mdx_content(content)
    assert "`<my-component/>`" in sanitized
    
    # Lowercase tags (invalid React components)
    content = "Use <button/> here"
    sanitized = sanitize_mdx_content(content)
    assert "`<button/>`" in sanitized


def test_sanitize_mdx_valid_jsx():
    """Test that valid JSX is preserved."""
    # Valid React component names (PascalCase)
    content = "Use <MyComponent/> here"
    sanitized = sanitize_mdx_content(content)
    # Should NOT be escaped
    assert "<MyComponent/>" in sanitized


def test_sanitize_mdx_file_paths():
    """Test escaping file paths with slashes."""
    content = "Edit <src/components/App.js> to get started"
    sanitized = sanitize_mdx_content(content)
    assert "`<src/components/App.js>`" in sanitized


def test_sanitize_mdx_code_blocks():
    """Test that code blocks are not modified."""
    content = """
Here's an example:

```javascript
const Component = () => <div/>;
const file = <config.js/>;
```

Use the `<file.js/>` inline code.
"""
    sanitized = sanitize_mdx_content(content)
    
    # Code blocks should be preserved
    assert "<div/>" in sanitized
    assert "<config.js/>" in sanitized  # Inside code block
    
    # But inline code should also be preserved
    assert "`<file.js/>`" in sanitized


def test_sanitize_mdx_write_file():
    """Test writing with MDX sanitization enabled."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test.md"
        content = "Use <config.js/> and <app/> components"
        
        # Write with sanitization
        write_file(str(file_path), content, sanitize_mdx=True)
        
        # Read back
        result = read_file(str(file_path))
        
        # Should be sanitized
        assert "`<config.js/>`" in result
        assert "`<app/>`" in result


def test_sanitize_mdx_complex_example():
    """Test real-world example from user's error."""
    content = """# Configuration

To configure the app, edit <config/database.js/> and set:

1. Database URL in <.env/>
2. API keys in <config/api.js/>

Example code:
```javascript
import config from '<config/database.js/>';
```

Use the <Button/> component for actions.
"""
    
    sanitized = sanitize_mdx_content(content)
    
    # Invalid JSX should be escaped
    assert "`<config/database.js/>`" in sanitized
    assert "`<.env/>`" in sanitized
    assert "`<config/api.js/>`" in sanitized
    
    # Code block should be preserved
    assert "import config from '<config/database.js/>'" in sanitized
    
    # Valid React component should NOT be escaped
    assert "<Button/>" in sanitized


def test_sanitize_mdx_unclosed_br_tags():
    """Test fixing unclosed <br> tags (user's actual error)."""
    # Unclosed <br> in table
    content = """| Column 1 | Column 2 |
|----------|----------|
| Value 1<br>Line 2 | Value 2 |"""
    
    sanitized = sanitize_mdx_content(content)
    
    # Should be self-closing
    assert "<br />" in sanitized
    assert "<br>" not in sanitized


def test_sanitize_mdx_unclosed_html_tags():
    """Test fixing various unclosed HTML tags."""
    content = """
Use a line break<br>here.
Add a horizontal rule<hr>below.
Show an image<img src="test.png">
"""
    
    sanitized = sanitize_mdx_content(content)
    
    # All should be self-closing
    assert "<br />" in sanitized
    assert "<hr />" in sanitized
    assert '<img src="test.png" />' in sanitized


def test_sanitize_mdx_urls_in_angle_brackets():
    """Test escaping URLs in angle brackets."""
    content = "Visit <https://example.com> for more info"
    sanitized = sanitize_mdx_content(content)
    
    # URLs should be escaped
    assert "`<https://example.com>`" in sanitized
