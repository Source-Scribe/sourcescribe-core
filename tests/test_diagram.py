"""Tests for diagram generation."""

import pytest
from sourcescribe.engine.diagram import DiagramGenerator


def test_architecture_diagram():
    """Test generating architecture diagram."""
    generator = DiagramGenerator()
    
    modules = [
        {'name': 'ModuleA', 'dependencies': ['ModuleB']},
        {'name': 'ModuleB', 'dependencies': []},
    ]
    
    diagram = generator.generate_architecture_diagram(modules, "Test Architecture")
    
    assert '```mermaid' in diagram
    assert 'graph TD' in diagram
    assert 'ModuleA' in diagram
    assert 'ModuleB' in diagram


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
