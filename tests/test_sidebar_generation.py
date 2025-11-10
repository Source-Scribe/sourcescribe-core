"""Tests for dynamic sidebar generation (v1.2.1)."""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from sourcescribe.engine.feature_generator import FeatureDocumentationMixin
from sourcescribe.config.models import SourceScribeConfig


class MockGenerator(FeatureDocumentationMixin):
    """Mock generator for testing mixin methods."""
    
    def __init__(self):
        self.config = SourceScribeConfig()
        self.logger = Mock()


def test_scan_docs_structure_basic(tmp_path):
    """Test scanning basic documentation structure."""
    generator = MockGenerator()
    
    # Create test structure
    docs_path = tmp_path / "docs"
    docs_path.mkdir()
    
    # Create README
    (docs_path / "README.md").write_text("# Documentation")
    
    # Create categories
    overview_dir = docs_path / "overview"
    overview_dir.mkdir()
    (overview_dir / "index.md").write_text("# Overview")
    (overview_dir / "architecture.md").write_text("# Architecture")
    
    features_dir = docs_path / "features"
    features_dir.mkdir()
    (features_dir / "index.md").write_text("# Features")
    
    # Scan structure
    structure = generator._scan_docs_structure(docs_path, "")
    
    # Assertions
    assert structure['readme'] == "README"
    assert 'overview' in structure['categories']
    assert 'features' in structure['categories']
    assert len(structure['categories']['overview']) == 2
    assert len(structure['categories']['features']) == 1


def test_scan_docs_structure_with_prefix(tmp_path):
    """Test scanning docs with path prefix."""
    generator = MockGenerator()
    
    docs_path = tmp_path / "docs"
    docs_path.mkdir()
    (docs_path / "README.md").write_text("# Docs")
    
    overview_dir = docs_path / "overview"
    overview_dir.mkdir()
    (overview_dir / "index.md").write_text("# Overview")
    
    structure = generator._scan_docs_structure(docs_path, "api-reference")
    
    assert structure['readme'] == "api-reference/README"
    assert 'overview' in structure['categories']
    assert structure['categories']['overview'][0]['id'] == "api-reference/overview/index"


def test_build_sidebar_items_ordering():
    """Test that sidebar items are ordered correctly."""
    generator = MockGenerator()
    
    structure = {
        'readme': 'README',
        'categories': {
            'features': [
                {'id': 'features/index', 'name': 'index'},
            ],
            'overview': [
                {'id': 'overview/technology-stack', 'name': 'technology-stack'},
                {'id': 'overview/index', 'name': 'index'},
                {'id': 'overview/architecture', 'name': 'architecture'},
            ],
            'getting-started': [
                {'id': 'getting-started/configuration', 'name': 'configuration'},
                {'id': 'getting-started/installation', 'name': 'installation'},
                {'id': 'getting-started/quick-start', 'name': 'quick-start'},
            ],
            'custom': [
                {'id': 'custom/doc', 'name': 'doc'},
            ]
        }
    }
    
    sidebar_items = generator._build_sidebar_items(structure)
    
    # Check that it's valid TypeScript array
    assert sidebar_items.startswith('[')
    assert sidebar_items.endswith(']')
    
    # Check README comes first
    assert "'README'" in sidebar_items or '"README"' in sidebar_items
    
    # Check predefined categories appear before custom ones
    assert sidebar_items.index('Overview') < sidebar_items.index('Custom')
    assert sidebar_items.index('Getting Started') < sidebar_items.index('Custom')


def test_build_category_item():
    """Test building individual category items."""
    generator = MockGenerator()
    
    items = [
        {'id': 'overview/architecture', 'name': 'architecture'},
        {'id': 'overview/index', 'name': 'index'},
        {'id': 'overview/technology-stack', 'name': 'technology-stack'},
    ]
    
    result = generator._build_category_item('overview', 'Overview', items, False)
    
    # Check structure
    assert "type: 'category'" in result
    assert "label: 'Overview'" in result
    assert "collapsed: false" in result
    assert 'items: [' in result
    
    # Check ordering: index should come first
    lines = result.split('\n')
    item_lines = [l for l in lines if 'overview/' in l]
    assert 'overview/index' in item_lines[0]


def test_generate_docusaurus_sidebar(tmp_path):
    """Test full sidebar generation."""
    generator = MockGenerator()
    generator.config.output.path = str(tmp_path / "website" / "docs")
    
    # Create website structure
    website_root = tmp_path / "website"
    website_root.mkdir()
    (website_root / "package.json").write_text('{}')
    
    docs_path = Path(generator.config.output.path)
    docs_path.mkdir(parents=True)
    
    # Create test docs
    (docs_path / "README.md").write_text("# Docs")
    overview_dir = docs_path / "overview"
    overview_dir.mkdir()
    (overview_dir / "index.md").write_text("# Overview")
    
    # Mock analyses
    analyses = [{'path': str(docs_path / 'README.md')}]
    
    # Generate sidebar
    generator._generate_docusaurus_sidebar(analyses)
    
    # Check sidebar was created
    sidebar_path = website_root / "sidebars.ts"
    assert sidebar_path.exists()
    
    content = sidebar_path.read_text()
    assert 'SidebarsConfig' in content
    assert 'tutorialSidebar' in content
    assert 'Auto-generated by SourceScribe' in content


def test_scan_docs_ignores_readme_in_subdirs(tmp_path):
    """Test that README files in subdirectories are ignored."""
    generator = MockGenerator()
    
    docs_path = tmp_path / "docs"
    docs_path.mkdir()
    
    overview_dir = docs_path / "overview"
    overview_dir.mkdir()
    (overview_dir / "README.md").write_text("# Should be ignored")
    (overview_dir / "index.md").write_text("# Should be included")
    
    structure = generator._scan_docs_structure(docs_path, "")
    
    # Should only have index.md, not README.md
    assert len(structure['categories']['overview']) == 1
    assert structure['categories']['overview'][0]['name'] == 'index'
