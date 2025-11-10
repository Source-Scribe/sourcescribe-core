"""Tests for diagram generation."""

import pytest
from sourcescribe.engine.diagram import DiagramGenerator


def test_architecture_diagram():
    """Test generating architecture diagram."""
    generator = DiagramGenerator()
    
    modules = [
        {
            'name': 'ModuleA', 
            'dependencies': ['ModuleB'],
            'path': '/project/src/ModuleA.js',
            'lines': 100,
            'classes': [],
            'functions': []
        },
        {
            'name': 'ModuleB', 
            'dependencies': [],
            'path': '/project/src/ModuleB.js',
            'lines': 50,
            'classes': [],
            'functions': []
        },
    ]
    
    diagram = generator.generate_architecture_diagram(modules, "Test Architecture")
    
    assert '```mermaid' in diagram
    assert 'graph TD' in diagram
    assert 'ModuleA' in diagram
    assert 'ModuleB' in diagram
    assert 'M0 --> M1' in diagram or 'M1 --> M0' in diagram  # Should have a relationship


def test_class_diagram():
    """Test generating class diagram."""
    generator = DiagramGenerator()
    
    classes = [
        {
            'name': 'MyClass',
            'attributes': ['x', 'y'],
            'methods': ['doSomething', 'doAnother'],
        }
    ]
    
    diagram = generator.generate_class_diagram(classes)
    
    assert '```mermaid' in diagram
    assert 'classDiagram' in diagram
    assert 'MyClass' in diagram
    assert 'doSomething' in diagram


def test_flow_diagram():
    """Test generating flow diagram."""
    generator = DiagramGenerator()
    
    steps = [
        {'text': 'Initialize', 'type': 'process'},
        {'text': 'Check condition', 'type': 'decision'},
        {'text': 'Process data', 'type': 'process'},
    ]
    
    diagram = generator.generate_flow_diagram(steps)
    
    assert '```mermaid' in diagram
    assert 'flowchart TD' in diagram
    assert 'Initialize' in diagram


def test_sequence_diagram():
    """Test generating sequence diagram."""
    generator = DiagramGenerator()
    
    interactions = [
        {'from': 'Client', 'to': 'Server', 'message': 'Request'},
        {'from': 'Server', 'to': 'Database', 'message': 'Query'},
    ]
    
    diagram = generator.generate_sequence_diagram(interactions)
    
    assert '```mermaid' in diagram
    assert 'sequenceDiagram' in diagram
    assert 'Client' in diagram
    assert 'Server' in diagram


def test_module_grouping():
    """Test that modules are grouped by layer correctly."""
    generator = DiagramGenerator()
    
    modules = [
        {'name': 'UserComponent', 'path': '/frontend/components/User.js', 'dependencies': [], 'lines': 100, 'classes': [], 'functions': []},
        {'name': 'UserController', 'path': '/backend/controllers/user.js', 'dependencies': [], 'lines': 100, 'classes': [], 'functions': []},
        {'name': 'UserModel', 'path': '/models/User.js', 'dependencies': [], 'lines': 100, 'classes': [], 'functions': []},
        {'name': 'apiHelper', 'path': '/api/helper.js', 'dependencies': [], 'lines': 100, 'classes': [], 'functions': []},
    ]
    
    grouped = generator._group_modules_by_layer(modules)
    
    assert 'Frontend' in grouped
    assert 'Backend' in grouped
    assert 'Database' in grouped
    assert 'API' in grouped
    assert len(grouped['Frontend']) == 1
    assert len(grouped['Backend']) == 1


def test_important_module_selection():
    """Test that most important modules are selected."""
    generator = DiagramGenerator()
    
    # Create 100 modules with varying importance
    modules = []
    for i in range(100):
        modules.append({
            'name': f'Module{i}',
            'path': f'/src/Module{i}.js',
            'dependencies': [f'Module{j}' for j in range(i % 5)],  # Varying deps
            'lines': (i + 1) * 10,
            'classes': [],
            'functions': []
        })
    
    important = generator._select_important_modules(modules, max_nodes=10)
    
    # Should select only 10
    assert len(important) == 10
    
    # Should include modules with more dependencies and lines
    assert any(len(m.get('dependencies', [])) > 0 for m in important)


def test_graph_diagram():
    """Test focused dependency graph generation."""
    generator = DiagramGenerator()
    
    modules = [
        {'name': 'App', 'dependencies': ['Router', 'Config'], 'path': '/src/App.js', 'lines': 100, 'classes': [], 'functions': []},
        {'name': 'Router', 'dependencies': ['Pages'], 'path': '/src/Router.js', 'lines': 50, 'classes': [], 'functions': []},
        {'name': 'Pages', 'dependencies': [], 'path': '/src/Pages.js', 'lines': 200, 'classes': [], 'functions': []},
        {'name': 'Config', 'dependencies': [], 'path': '/src/Config.js', 'lines': 30, 'classes': [], 'functions': []},
    ]
    
    # Generate focused graph
    diagram = generator.generate_graph_diagram(modules, focus_module='App', depth=2)
    
    assert '```mermaid' in diagram
    assert 'graph TD' in diagram
    assert 'App' in diagram
    assert 'Router' in diagram
    assert 'focus' in diagram  # Focus module should have special styling


def test_large_module_filtering():
    """Test that large numbers of modules are filtered appropriately."""
    generator = DiagramGenerator()
    
    # Create 500 modules (like the user's case)
    modules = []
    for i in range(500):
        modules.append({
            'name': f'M{i}',
            'path': f'/src/M{i}.js',
            'dependencies': [f'M{(i+1) % 500}'] if i % 3 == 0 else [],
            'lines': 50,
            'classes': [],
            'functions': []
        })
    
    diagram = generator.generate_architecture_diagram(modules)
    
    assert '```mermaid' in diagram
    # Should mention filtering
    assert 'Showing' in diagram or 'modules' in diagram
    # Should not have 500 nodes
    node_count = diagram.count('[M')
    assert node_count <= 50  # Should limit to max_nodes
