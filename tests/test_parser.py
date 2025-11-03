"""Tests for code parser."""

import pytest
from sourcescribe.utils.parser import CodeParser


def test_parse_python():
    """Test parsing Python code."""
    code = '''
import os
from typing import List

class MyClass:
    def __init__(self):
        pass
    
    def my_method(self, arg1, arg2):
        """Docstring here."""
        return arg1 + arg2

def my_function(x, y):
    """Function docstring."""
    return x * y
'''
    
    parser = CodeParser('python')
    result = parser.parse(code)
    
    assert result['language'] == 'python'
    assert len(result['imports']) >= 2
    assert len(result['elements']) >= 2
    
    # Check for class and functions
    element_names = [e.name for e in result['elements']]
    assert 'MyClass' in element_names
    assert 'my_function' in element_names


def test_parse_javascript():
    """Test parsing JavaScript code."""
    code = '''
import React from 'react';

function myFunction(a, b) {
    return a + b;
}

const myArrowFunc = (x) => {
    return x * 2;
};

class MyComponent {
    render() {
        return null;
    }
}
'''
    
    parser = CodeParser('javascript')
    result = parser.parse(code)
    
    assert result['language'] == 'javascript'
    assert len(result['imports']) >= 1
    assert len(result['elements']) >= 2


def test_parse_java():
    """Test parsing Java code."""
    code = '''
import java.util.List;

public class MyClass {
    private int value;
    
    public void myMethod(String arg) {
        // method body
    }
}
'''
    
    parser = CodeParser('java')
    result = parser.parse(code)
    
    assert result['language'] == 'java'
    assert len(result['imports']) >= 1
    assert len(result['elements']) >= 1


def test_parse_generic():
    """Test parsing unknown language."""
    code = "some random code"
    
    parser = CodeParser('unknown')
    result = parser.parse(code)
    
    assert result['language'] == 'unknown'
    assert 'elements' in result
