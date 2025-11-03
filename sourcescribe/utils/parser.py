"""Code parsing utilities."""

import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CodeElement:
    """Represents a code element (function, class, etc.)."""
    name: str
    type: str  # function, class, method, etc.
    start_line: int
    end_line: int
    docstring: Optional[str] = None
    signature: Optional[str] = None
    params: Optional[List[str]] = None
    body: Optional[str] = None


class CodeParser:
    """Parse source code to extract structure and elements."""
    
    def __init__(self, language: str):
        """
        Initialize parser for a specific language.
        
        Args:
            language: Programming language
        """
        self.language = language.lower()
    
    def parse(self, code: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse code and extract structure.
        
        Args:
            code: Source code
            file_path: Optional file path
            
        Returns:
            Dictionary with parsed information
        """
        if self.language == 'python':
            return self._parse_python(code)
        elif self.language in ['javascript', 'typescript']:
            return self._parse_javascript(code)
        elif self.language == 'java':
            return self._parse_java(code)
        elif self.language in ['c', 'cpp']:
            return self._parse_c_cpp(code)
        else:
            return self._parse_generic(code)
    
    def _parse_python(self, code: str) -> Dict[str, Any]:
        """Parse Python code."""
        elements = []
        imports = []
        
        lines = code.split('\n')
        
        # Extract imports
        import_pattern = r'^(?:from\s+[\w.]+\s+)?import\s+[\w., ]+'
        for i, line in enumerate(lines):
            if re.match(import_pattern, line.strip()):
                imports.append(line.strip())
        
        # Extract classes
        class_pattern = r'^class\s+(\w+).*:'
        for i, line in enumerate(lines):
            match = re.match(class_pattern, line)
            if match:
                class_name = match.group(1)
                elements.append(CodeElement(
                    name=class_name,
                    type='class',
                    start_line=i + 1,
                    end_line=self._find_block_end(lines, i),
                    signature=line.strip(),
                ))
        
        # Extract functions
        func_pattern = r'^(?:async\s+)?def\s+(\w+)\s*\((.*?)\).*:'
        for i, line in enumerate(lines):
            match = re.match(func_pattern, line)
            if match:
                func_name = match.group(1)
                params = [p.strip() for p in match.group(2).split(',') if p.strip()]
                
                # Extract docstring
                docstring = None
                if i + 1 < len(lines):
                    next_lines = lines[i + 1:min(i + 10, len(lines))]
                    docstring = self._extract_python_docstring(next_lines)
                
                elements.append(CodeElement(
                    name=func_name,
                    type='function',
                    start_line=i + 1,
                    end_line=self._find_block_end(lines, i),
                    signature=line.strip(),
                    params=params,
                    docstring=docstring,
                ))
        
        return {
            'language': 'python',
            'imports': imports,
            'elements': elements,
            'total_lines': len(lines),
        }
    
    def _parse_javascript(self, code: str) -> Dict[str, Any]:
        """Parse JavaScript/TypeScript code."""
        elements = []
        imports = []
        
        lines = code.split('\n')
        
        # Extract imports
        import_pattern = r'^(?:import|export).*from\s+'
        for i, line in enumerate(lines):
            if re.match(import_pattern, line.strip()):
                imports.append(line.strip())
        
        # Extract functions
        func_pattern = r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\((.*?)\)'
        arrow_func_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\((.*?)\)\s*=>'
        
        for i, line in enumerate(lines):
            # Regular function
            match = re.search(func_pattern, line)
            if match:
                elements.append(CodeElement(
                    name=match.group(1),
                    type='function',
                    start_line=i + 1,
                    end_line=i + 1,
                    signature=line.strip(),
                ))
            
            # Arrow function
            match = re.search(arrow_func_pattern, line)
            if match:
                elements.append(CodeElement(
                    name=match.group(1),
                    type='function',
                    start_line=i + 1,
                    end_line=i + 1,
                    signature=line.strip(),
                ))
        
        # Extract classes
        class_pattern = r'class\s+(\w+)'
        for i, line in enumerate(lines):
            match = re.search(class_pattern, line)
            if match:
                elements.append(CodeElement(
                    name=match.group(1),
                    type='class',
                    start_line=i + 1,
                    end_line=i + 1,
                    signature=line.strip(),
                ))
        
        return {
            'language': self.language,
            'imports': imports,
            'elements': elements,
            'total_lines': len(lines),
        }
    
    def _parse_java(self, code: str) -> Dict[str, Any]:
        """Parse Java code."""
        elements = []
        imports = []
        
        lines = code.split('\n')
        
        # Extract imports
        for i, line in enumerate(lines):
            if line.strip().startswith('import '):
                imports.append(line.strip())
        
        # Extract classes
        class_pattern = r'(?:public\s+)?(?:abstract\s+)?class\s+(\w+)'
        for i, line in enumerate(lines):
            match = re.search(class_pattern, line)
            if match:
                elements.append(CodeElement(
                    name=match.group(1),
                    type='class',
                    start_line=i + 1,
                    end_line=i + 1,
                    signature=line.strip(),
                ))
        
        # Extract methods
        method_pattern = r'(?:public|private|protected)\s+(?:static\s+)?(?:\w+)\s+(\w+)\s*\((.*?)\)'
        for i, line in enumerate(lines):
            match = re.search(method_pattern, line)
            if match:
                elements.append(CodeElement(
                    name=match.group(1),
                    type='method',
                    start_line=i + 1,
                    end_line=i + 1,
                    signature=line.strip(),
                ))
        
        return {
            'language': 'java',
            'imports': imports,
            'elements': elements,
            'total_lines': len(lines),
        }
    
    def _parse_c_cpp(self, code: str) -> Dict[str, Any]:
        """Parse C/C++ code."""
        elements = []
        includes = []
        
        lines = code.split('\n')
        
        # Extract includes
        for i, line in enumerate(lines):
            if line.strip().startswith('#include'):
                includes.append(line.strip())
        
        # Extract functions
        func_pattern = r'(?:\w+\s+)+(\w+)\s*\([^)]*\)\s*\{'
        for i, line in enumerate(lines):
            match = re.search(func_pattern, line)
            if match:
                elements.append(CodeElement(
                    name=match.group(1),
                    type='function',
                    start_line=i + 1,
                    end_line=i + 1,
                    signature=line.strip(),
                ))
        
        return {
            'language': self.language,
            'includes': includes,
            'elements': elements,
            'total_lines': len(lines),
        }
    
    def _parse_generic(self, code: str) -> Dict[str, Any]:
        """Generic parsing for unsupported languages."""
        lines = code.split('\n')
        
        return {
            'language': self.language,
            'total_lines': len(lines),
            'elements': [],
        }
    
    def _find_block_end(self, lines: List[str], start: int) -> int:
        """Find the end of a code block (Python indentation-based)."""
        if start >= len(lines):
            return start
        
        start_indent = len(lines[start]) - len(lines[start].lstrip())
        
        for i in range(start + 1, len(lines)):
            line = lines[i]
            if line.strip():  # Non-empty line
                indent = len(line) - len(line.lstrip())
                if indent <= start_indent:
                    return i
        
        return len(lines)
    
    def _extract_python_docstring(self, lines: List[str]) -> Optional[str]:
        """Extract Python docstring."""
        if not lines:
            return None
        
        first_line = lines[0].strip()
        if first_line.startswith('"""') or first_line.startswith("'''"):
            quote = first_line[:3]
            docstring_lines = []
            
            # Single-line docstring
            if first_line.endswith(quote) and len(first_line) > 6:
                return first_line[3:-3].strip()
            
            # Multi-line docstring
            docstring_lines.append(first_line[3:])
            for line in lines[1:]:
                if quote in line:
                    docstring_lines.append(line[:line.index(quote)])
                    break
                docstring_lines.append(line)
            
            return '\n'.join(docstring_lines).strip()
        
        return None
