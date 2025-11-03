"""Tests for file utilities."""

import pytest
import tempfile
from pathlib import Path
from sourcescribe.utils.file_utils import (
    read_file,
    write_file,
    find_files,
    get_file_language,
    is_text_file,
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
