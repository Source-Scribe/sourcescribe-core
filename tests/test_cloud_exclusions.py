"""Tests for cloud storage and system directory exclusions (v1.2.1)."""

import pytest
from pathlib import Path
from sourcescribe.config.models import RepositoryConfig
from sourcescribe.utils.file_utils import find_files


def test_cloud_storage_exclusions(tmp_path):
    """Test that cloud storage directories are excluded by default."""
    config = RepositoryConfig()
    
    # Create test structure
    project = tmp_path / "project"
    project.mkdir()
    
    # Create normal files
    src = project / "src"
    src.mkdir()
    (src / "app.py").write_text("# normal file")
    
    # Create cloud storage paths
    cloud = project / "Library" / "CloudStorage" / "GoogleDrive-user@gmail.com"
    cloud.mkdir(parents=True)
    (cloud / "bad.py").write_text("# should be excluded")
    
    dropbox = project / "Dropbox"
    dropbox.mkdir()
    (dropbox / "bad.js").write_text("// should be excluded")
    
    # Find files
    files = find_files(
        str(project),
        include_patterns=["*.py", "*.js"],
        exclude_patterns=config.exclude_patterns
    )
    
    # Should only find normal files
    assert len(files) == 1
    assert "app.py" in files[0]


def test_system_directory_exclusions(tmp_path):
    """Test that system directories are excluded."""
    config = RepositoryConfig()
    
    project = tmp_path / "project"
    project.mkdir()
    
    # Normal file
    (project / "app.py").write_text("# normal")
    
    # System paths
    library = project / "Library" / "Caches"
    library.mkdir(parents=True)
    (library / "bad.py").write_text("# excluded")
    
    trash = project / ".Trash"
    trash.mkdir()
    (trash / "bad.js").write_text("// excluded")
    
    files = find_files(
        str(project),
        include_patterns=["*.py", "*.js"],
        exclude_patterns=config.exclude_patterns
    )
    
    assert len(files) == 1
    assert "app.py" in files[0]


def test_standard_exclusions_still_work(tmp_path):
    """Test that standard exclusions (node_modules, .git, etc.) still work."""
    config = RepositoryConfig()
    
    project = tmp_path / "project"
    project.mkdir()
    
    # Normal files
    (project / "index.js").write_text("// normal")
    
    # Excluded dirs
    node_modules = project / "node_modules" / "package"
    node_modules.mkdir(parents=True)
    (node_modules / "index.js").write_text("// excluded")
    
    git = project / ".git"
    git.mkdir()
    (git / "config").write_text("excluded")
    
    pycache = project / "__pycache__"
    pycache.mkdir()
    (pycache / "module.pyc").write_text("excluded")
    
    files = find_files(
        str(project),
        include_patterns=["*.js"],
        exclude_patterns=config.exclude_patterns
    )
    
    assert len(files) == 1
    assert "index.js" in files[0]


def test_docs_and_website_exclusions(tmp_path):
    """Test that docs and website directories are excluded from scanning."""
    config = RepositoryConfig()
    
    project = tmp_path / "project"
    project.mkdir()
    
    # Normal file
    (project / "main.js").write_text("// normal")
    
    # Excluded paths
    website = project / "website" / "src"
    website.mkdir(parents=True)
    (website / "index.js").write_text("// excluded")
    
    docs = project / "docs"
    docs.mkdir()
    (docs / "README.md").write_text("excluded")
    
    files = find_files(
        str(project),
        include_patterns=["*.js", "*.md"],
        exclude_patterns=config.exclude_patterns
    )
    
    assert len(files) == 1
    assert "main.js" in files[0]


def test_default_exclusions_count():
    """Test that we have a reasonable number of exclusion patterns."""
    config = RepositoryConfig()
    
    # Should have standard patterns plus cloud/system patterns
    assert len(config.exclude_patterns) > 15
    
    # Check specific important patterns are included
    assert any('CloudStorage' in p for p in config.exclude_patterns)
    assert any('Dropbox' in p for p in config.exclude_patterns)
    assert any('node_modules' in p for p in config.exclude_patterns)
    assert any('.git' in p for p in config.exclude_patterns)
