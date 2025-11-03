"""Tests for file exclusion patterns."""

import os
import tempfile
from pathlib import Path
import pytest

from sourcescribe.utils.file_utils import find_files
from sourcescribe.config.models import RepositoryConfig


def test_venv_exclusion():
    """Test that venv directories are properly excluded."""
    config = RepositoryConfig()
    
    # venv should be in default exclude patterns
    assert "venv" in config.exclude_patterns
    assert "*/venv/*" in config.exclude_patterns
    
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test structure
        Path(tmpdir, "src", "main.py").parent.mkdir(parents=True, exist_ok=True)
        Path(tmpdir, "src", "main.py").write_text("print('hello')")
        
        Path(tmpdir, "venv", "lib", "python3.11", "site-packages").mkdir(parents=True, exist_ok=True)
        Path(tmpdir, "venv", "lib", "python3.11", "site-packages", "module.py").write_text("# venv module")
        
        Path(tmpdir, ".venv", "lib").mkdir(parents=True, exist_ok=True)
        Path(tmpdir, ".venv", "lib", "another.py").write_text("# .venv module")
        
        # Find files with default exclusions
        files = find_files(
            tmpdir,
            include_patterns=["*.py"],
            exclude_patterns=config.exclude_patterns,
        )
        
        # Convert to relative paths for easier checking
        tmpdir_resolved = Path(tmpdir).resolve()
        rel_files = [str(Path(f).resolve().relative_to(tmpdir_resolved)) for f in files]
        
        # Should find src/main.py
        assert any("src/main.py" in f or "src\\main.py" in f for f in rel_files)
        
        # Should NOT find anything in venv or .venv
        assert not any("venv" in f for f in rel_files)
        assert not any(".venv" in f for f in rel_files)


def test_site_packages_exclusion():
    """Test that site-packages directories are excluded."""
    config = RepositoryConfig()
    
    # site-packages should be in exclude patterns
    assert "site-packages" in config.exclude_patterns
    assert "*/site-packages/*" in config.exclude_patterns
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test structure
        Path(tmpdir, "myproject", "app.py").parent.mkdir(parents=True, exist_ok=True)
        Path(tmpdir, "myproject", "app.py").write_text("# app code")
        
        Path(tmpdir, "lib", "site-packages", "requests").mkdir(parents=True, exist_ok=True)
        Path(tmpdir, "lib", "site-packages", "requests", "api.py").write_text("# requests")
        
        # Find files
        files = find_files(
            tmpdir,
            include_patterns=["*.py"],
            exclude_patterns=config.exclude_patterns,
        )
        
        tmpdir_resolved = Path(tmpdir).resolve()
        rel_files = [str(Path(f).resolve().relative_to(tmpdir_resolved)) for f in files]
        
        # Should find project file
        assert any("myproject" in f and "app.py" in f for f in rel_files)
        
        # Should NOT find site-packages
        assert not any("site-packages" in f for f in rel_files)


def test_common_exclusions():
    """Test other common exclusion patterns."""
    config = RepositoryConfig()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create various files that should be excluded
        Path(tmpdir, "src", "module.py").parent.mkdir(parents=True, exist_ok=True)
        Path(tmpdir, "src", "module.py").write_text("# source")
        Path(tmpdir, "src", "module.pyc").write_text("bytecode")
        
        Path(tmpdir, "__pycache__").mkdir(exist_ok=True)
        Path(tmpdir, "__pycache__", "cache.pyc").write_text("cache")
        
        Path(tmpdir, "node_modules", "pkg").mkdir(parents=True, exist_ok=True)
        Path(tmpdir, "node_modules", "pkg", "index.js").write_text("// js")
        
        Path(tmpdir, "dist", "build.py").parent.mkdir(parents=True, exist_ok=True)
        Path(tmpdir, "dist", "build.py").write_text("# dist")
        
        Path(tmpdir, ".git", "config").parent.mkdir(parents=True, exist_ok=True)
        Path(tmpdir, ".git", "config").write_text("git config")
        
        # Find files
        files = find_files(
            tmpdir,
            include_patterns=["*.py", "*.js"],
            exclude_patterns=config.exclude_patterns,
        )
        
        tmpdir_resolved = Path(tmpdir).resolve()
        rel_files = [str(Path(f).resolve().relative_to(tmpdir_resolved)) for f in files]
        
        # Should only find src/module.py
        assert len(rel_files) == 1
        assert any("module.py" in f and "src" in f for f in rel_files)
        
        # Should NOT find excluded files
        assert not any(".pyc" in f for f in rel_files)
        assert not any("__pycache__" in f for f in rel_files)
        assert not any("node_modules" in f for f in rel_files)
        assert not any("dist" in f for f in rel_files)
        assert not any(".git" in f for f in rel_files)


def test_exclusion_priority():
    """Test that exclusions take priority over inclusions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a Python file in venv
        Path(tmpdir, "venv", "lib").mkdir(parents=True, exist_ok=True)
        Path(tmpdir, "venv", "lib", "test.py").write_text("# test")
        
        # Even though *.py is in include patterns, venv should exclude it
        files = find_files(
            tmpdir,
            include_patterns=["*.py"],
            exclude_patterns=["venv", "*/venv/*"],
        )
        
        # Should find nothing
        assert len(files) == 0
