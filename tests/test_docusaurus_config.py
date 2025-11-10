"""Tests for AI-powered Docusaurus config generation (v1.2.2)."""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from sourcescribe.engine.feature_generator import FeatureDocumentationMixin
from sourcescribe.config.models import SourceScribeConfig
from sourcescribe.api.base import LLMResponse


class MockGenerator(FeatureDocumentationMixin):
    """Mock generator for testing mixin methods."""
    
    def __init__(self):
        self.config = SourceScribeConfig()
        self.logger = Mock()
        self.llm_provider = Mock()
    
    def _get_system_prompt(self):
        return "You are a helpful assistant."
    
    def _build_project_context(self, analyses, max_files=30):
        return "Mock project context"


def test_infer_project_title_from_package_json(tmp_path):
    """Test inferring title from package.json."""
    generator = MockGenerator()
    generator.config.repository.path = str(tmp_path)
    
    # Create package.json
    package_json = tmp_path / "package.json"
    package_json.write_text(json.dumps({"name": "my-awesome-project"}))
    
    title = generator._infer_project_title("my-awesome-project", [])
    
    assert title == "My Awesome Project"


def test_infer_project_title_from_pyproject_toml(tmp_path):
    """Test inferring title from pyproject.toml."""
    generator = MockGenerator()
    generator.config.repository.path = str(tmp_path)
    
    # Create pyproject.toml
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nname = "cool-python-lib"\n')
    
    title = generator._infer_project_title("fallback", [])
    
    assert title == "Cool Python Lib"


def test_infer_project_title_fallback():
    """Test fallback to formatted repo name."""
    generator = MockGenerator()
    generator.config.repository.path = "/nonexistent"
    
    title = generator._infer_project_title("my_repo-name", [])
    
    assert title == "My Repo Name"


def test_generate_tagline_success():
    """Test successful AI tagline generation."""
    from sourcescribe.engine.generator import DocumentationGenerator
    from sourcescribe.api.base import LLMMessage
    
    generator = DocumentationGenerator(SourceScribeConfig())
    
    # Mock LLM response
    mock_response = LLMResponse(
        content='"A powerful tool for developers"',
        model="test-model",
        usage={"total_tokens": 10}
    )
    generator.llm_provider.generate.return_value = mock_response
    
    tagline = generator._generate_tagline([])
    
    assert tagline == "A powerful tool for developers"
    assert len(tagline) <= 100


def test_generate_tagline_strips_quotes():
    """Test that tagline generation strips quotes properly."""
    from sourcescribe.engine.generator import DocumentationGenerator
    
    generator = DocumentationGenerator(SourceScribeConfig())
    
    mock_response = LLMResponse(
        content="'Single quoted tagline'",
        model="test-model",
        usage={"total_tokens": 10}
    )
    generator.llm_provider.generate.return_value = mock_response
    
    tagline = generator._generate_tagline([])
    
    assert tagline == "Single quoted tagline"


def test_generate_tagline_truncates_long_output():
    """Test that overly long taglines are truncated."""
    from sourcescribe.engine.generator import DocumentationGenerator
    
    generator = DocumentationGenerator(SourceScribeConfig())
    
    long_text = "A" * 150
    mock_response = LLMResponse(
        content=long_text,
        model="test-model",
        usage={"total_tokens": 10}
    )
    generator.llm_provider.generate.return_value = mock_response
    
    tagline = generator._generate_tagline([])
    
    assert len(tagline) <= 100
    assert tagline.endswith("...")


def test_generate_tagline_fallback_on_error():
    """Test fallback when AI generation fails."""
    from sourcescribe.engine.generator import DocumentationGenerator
    
    generator = DocumentationGenerator(SourceScribeConfig())
    generator.llm_provider.generate.side_effect = Exception("API Error")
    
    tagline = generator._generate_tagline([])
    
    assert tagline == "Auto-generated documentation for your project"


def test_generate_docusaurus_config_content():
    """Test Docusaurus config content generation."""
    generator = MockGenerator()
    
    config_content = generator._generate_docusaurus_config_content(
        title="Test Project",
        tagline="An awesome test project",
        github_url="https://github.com/testorg/test-repo",
        org_name="testorg",
        repo_name="test-repo"
    )
    
    # Check essential components
    assert "title: 'Test Project'" in config_content
    assert "tagline: 'An awesome test project'" in config_content
    assert "organizationName: 'testorg'" in config_content
    assert "projectName: 'test-repo'" in config_content
    
    # Check Mermaid configuration
    assert "markdown: {" in config_content
    assert "mermaid: true" in config_content
    assert "themes: ['@docusaurus/theme-mermaid']" in config_content
    
    # Check mermaid theme config
    assert "mermaid: {" in config_content
    assert "theme: {light: 'neutral', dark: 'dark'}" in config_content
    
    # Check no Tutorial references
    assert "Tutorial" not in config_content
    assert "/docs/intro" not in config_content
    
    # Check proper footer links
    assert "Getting Started" in config_content
    assert "/docs/getting-started/installation" in config_content
    assert "Overview" in config_content
    assert "/docs/overview/index" in config_content
    
    # Check blog is disabled
    assert "blog: false" in config_content


def test_generate_docusaurus_config_github_url_parsing():
    """Test GitHub URL is parsed correctly for deployment."""
    from sourcescribe.engine.generator import DocumentationGenerator
    
    generator = DocumentationGenerator(SourceScribeConfig())
    
    config_content = generator._generate_docusaurus_config_content(
        title="Test",
        tagline="Test",
        github_url="https://github.com/myorg/myrepo",
        org_name="myorg",
        repo_name="myrepo"
    )
    
    # Check deployment URLs - the URL generation creates github pages URL
    assert "myorg.github.io" in config_content
    assert "baseUrl: '/myrepo/'" in config_content


def test_update_docusaurus_config_creates_file(tmp_path):
    """Test that config file is created."""
    from sourcescribe.engine.generator import DocumentationGenerator
    
    config = SourceScribeConfig()
    config.output.path = str(tmp_path / "website" / "docs")
    config.repository.github_url = "https://github.com/test/test"
    
    generator = DocumentationGenerator(config)
    
    # Create website structure
    website_root = tmp_path / "website"
    website_root.mkdir()
    docs_path = Path(generator.config.output.path)
    docs_path.mkdir(parents=True)
    
    # Mock AI response
    mock_response = LLMResponse(
        content="A test tagline",
        model="test-model",
        usage={"total_tokens": 10}
    )
    generator.llm_provider.generate.return_value = mock_response
    
    # Generate config
    generator._update_docusaurus_config([])
    
    # Check file was created
    config_path = website_root / "docusaurus.config.ts"
    assert config_path.exists()
    
    content = config_path.read_text()
    assert "import {themes as prismThemes}" in content
    assert "export default config" in content


def test_update_docusaurus_config_handles_missing_github_url(tmp_path):
    """Test graceful handling when GitHub URL is not available."""
    from sourcescribe.engine.generator import DocumentationGenerator
    
    config = SourceScribeConfig()
    config.output.path = str(tmp_path / "website" / "docs")
    config.repository.github_url = None
    
    generator = DocumentationGenerator(config)
    
    website_root = tmp_path / "website"
    website_root.mkdir()
    docs_path = Path(generator.config.output.path)
    docs_path.mkdir(parents=True)
    
    mock_response = LLMResponse(
        content="A test tagline",
        model="test-model",
        usage={"total_tokens": 10}
    )
    generator.llm_provider.generate.return_value = mock_response
    
    with patch('sourcescribe.utils.github_utils.get_github_url_from_git', return_value=None):
        generator._update_docusaurus_config([])
    
    config_path = website_root / "docusaurus.config.ts"
    assert config_path.exists()
    
    content = config_path.read_text()
    # Should use defaults
    assert "organizationName: 'your-org'" in content
    assert "projectName: 'your-repo'" in content


def test_build_project_context_with_max_files():
    """Test that max_files parameter limits context."""
    from sourcescribe.engine.generator import DocumentationGenerator
    
    config = SourceScribeConfig()
    config.repository.path = "/test"
    generator = DocumentationGenerator(config)
    
    # Create 10 analyses
    analyses = [
        {'path': f'/test/file{i}.py', 'language': 'python', 'lines': 100}
        for i in range(10)
    ]
    
    # Test with max_files=5
    context = generator._build_project_context(analyses, max_files=5)
    
    # Count file references in context (each file adds a line)
    # Should only include 5 files
    file_lines = [line for line in context.split('\n') if 'file' in line and '.py' in line]
    assert len(file_lines) <= 6  # 5 files + potential header
