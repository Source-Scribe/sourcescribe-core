"""Tests for configuration module."""

import pytest
import tempfile
from pathlib import Path
from sourcescribe.config.models import (
    SourceScribeConfig,
    LLMConfig,
    LLMProvider,
    Verbosity,
)
from sourcescribe.config.loader import ConfigLoader


def test_default_config():
    """Test default configuration creation."""
    config = SourceScribeConfig()
    
    assert config.llm.provider == LLMProvider.ANTHROPIC
    assert config.llm.temperature == 0.3
    assert config.repository.path == "."
    assert config.output.include_diagrams is True
    assert config.style.verbosity == Verbosity.DETAILED


def test_config_from_dict():
    """Test creating config from dictionary."""
    data = {
        "llm": {
            "provider": "openai",
            "model": "gpt-4",
            "temperature": 0.5,
        },
        "output": {
            "path": "./custom-docs"
        }
    }
    
    config = SourceScribeConfig.from_dict(data)
    
    assert config.llm.provider == "openai"
    assert config.llm.model == "gpt-4"
    assert config.llm.temperature == 0.5
    assert config.output.path == "./custom-docs"


def test_config_validation():
    """Test configuration validation."""
    # Invalid temperature
    with pytest.raises(ValueError):
        LLMConfig(temperature=3.0)
    
    # Invalid debounce
    from sourcescribe.config.models import WatchConfig
    with pytest.raises(ValueError):
        WatchConfig(debounce_seconds=100.0)


def test_config_save_and_load():
    """Test saving and loading configuration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.yaml"
        
        # Create and save config
        config = SourceScribeConfig()
        config.llm.model = "test-model"
        ConfigLoader.save_to_file(config, str(config_path))
        
        # Load config
        loaded = ConfigLoader.load_from_file(str(config_path))
        
        assert loaded.llm.model == "test-model"


def test_config_find():
    """Test finding configuration file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / ".sourcescribe.yaml"
        
        # Create config
        ConfigLoader.create_default_config(str(config_path))
        
        # Find config
        found = ConfigLoader.find_config(tmpdir)
        
        assert found is not None
        assert found.name == ".sourcescribe.yaml"
