"""Tests for CLI safety features (v1.2.1)."""

import pytest
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch, Mock
from sourcescribe.cli import main, generate


def test_home_directory_warning(tmp_path):
    """Test warning when scanning from home directory."""
    runner = CliRunner()
    
    with patch('sourcescribe.cli.Path.home', return_value=tmp_path):
        with patch('sourcescribe.cli.Path.resolve', return_value=tmp_path):
            with patch('sourcescribe.cli.click.confirm', return_value=False) as mock_confirm:
                result = runner.invoke(generate, [str(tmp_path)])
                
                # Should ask for confirmation
                mock_confirm.assert_called_once()
                assert 'home directory' in mock_confirm.call_args[0][0].lower()
                
                # Should exit without running
                assert result.exit_code == 1
                assert 'Operation cancelled' in result.output


def test_home_directory_can_proceed_with_confirmation(tmp_path):
    """Test that user can proceed if they confirm."""
    runner = CliRunner()
    
    with patch('sourcescribe.cli.Path.home', return_value=tmp_path):
        with patch('sourcescribe.cli.Path.resolve', return_value=tmp_path):
            with patch('sourcescribe.cli.click.confirm', return_value=True):
                with patch('sourcescribe.config.loader.ConfigLoader.load_or_default') as mock_config:
                    with patch('sourcescribe.engine.generator.DocumentationGenerator'):
                        # Create minimal config
                        from sourcescribe.config.models import SourceScribeConfig
                        mock_config.return_value = SourceScribeConfig()
                        
                        result = runner.invoke(generate, [str(tmp_path)])
                        
                        # Should proceed (may fail later but should get past confirmation)
                        assert 'Operation cancelled' not in result.output


def test_system_directory_warning():
    """Test warning for system directories."""
    runner = CliRunner()
    library_path = Path("/Library")
    
    with patch('sourcescribe.cli.Path.resolve', return_value=library_path):
        with patch('sourcescribe.cli.click.confirm', return_value=False) as mock_confirm:
            result = runner.invoke(generate, [str(library_path)])
            
            # Should warn about system directory
            mock_confirm.assert_called_once()
            assert result.exit_code == 1


def test_normal_directory_no_warning(tmp_path):
    """Test that normal project directories don't trigger warnings."""
    runner = CliRunner()
    project_path = tmp_path / "my-project"
    project_path.mkdir()
    
    with patch('sourcescribe.config.loader.ConfigLoader.load_or_default') as mock_config:
        with patch('sourcescribe.engine.generator.DocumentationGenerator') as mock_gen:
            from sourcescribe.config.models import SourceScribeConfig
            mock_config.return_value = SourceScribeConfig()
            
            # Mock the generator to not actually run
            mock_instance = Mock()
            mock_gen.return_value = mock_instance
            
            result = runner.invoke(generate, [str(project_path)])
            
            # Should not ask for confirmation
            assert 'home directory' not in result.output.lower()
            assert 'system directory' not in result.output.lower()


def test_problematic_directory_names():
    """Test detection of problematic directory names."""
    problematic_dirs = ['Library', 'Applications', 'System', 'usr', 'opt']
    
    for dir_name in problematic_dirs:
        runner = CliRunner()
        test_path = Path(f"/{dir_name}")
        
        with patch('sourcescribe.cli.Path.resolve', return_value=test_path):
            with patch('sourcescribe.cli.click.confirm', return_value=False) as mock_confirm:
                result = runner.invoke(generate, [str(test_path)])
                
                # Should trigger warning
                mock_confirm.assert_called_once()
                assert result.exit_code == 1
