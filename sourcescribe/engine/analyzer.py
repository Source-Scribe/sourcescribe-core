"""Code analysis and structure extraction."""

from typing import List, Dict, Any, Optional
from pathlib import Path
from sourcescribe.utils.file_utils import read_file, get_file_language
from sourcescribe.utils.parser import CodeParser
from sourcescribe.config.models import RepositoryConfig
from sourcescribe.utils.logger import get_logger


class CodeAnalyzer:
    """Analyzes code structure and extracts information."""
    
    def __init__(self, repo_config: Optional[RepositoryConfig] = None):
        """
        Initialize code analyzer.
        
        Args:
            repo_config: Repository configuration
        """
        self.repo_config = repo_config or RepositoryConfig()
        self.logger = get_logger(__name__)
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a single file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Dictionary with file analysis
        """
        try:
            # Read file content
            content = read_file(file_path)
            
            # Detect language
            language = get_file_language(file_path)
            
            # Parse code
            parser = CodeParser(language)
            parsed = parser.parse(content, file_path)
            
            # Extract basic info
            path_obj = Path(file_path)
            
            return {
                'path': file_path,
                'name': path_obj.name,
                'language': language,
                'size': len(content),
                'lines': parsed.get('total_lines', 0),
                'elements': parsed.get('elements', []),
                'imports': parsed.get('imports', []),
                'includes': parsed.get('includes', []),
                'content': content,
            }
        
        except Exception as e:
            self.logger.error(f"Error analyzing file {file_path}: {e}")
            return {
                'path': file_path,
                'error': str(e),
            }
    
    def analyze_files(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze multiple files.
        
        Args:
            file_paths: List of file paths
            
        Returns:
            List of file analyses
        """
        analyses = []
        
        for file_path in file_paths:
            analysis = self.analyze_file(file_path)
            if 'error' not in analysis:
                analyses.append(analysis)
        
        return analyses
    
    def extract_dependencies(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Extract dependencies from file analysis.
        
        Args:
            analysis: File analysis dictionary
            
        Returns:
            List of dependency names
        """
        dependencies = []
        language = analysis.get('language', 'unknown')
        
        if language == 'python':
            # Extract from imports
            imports = analysis.get('imports', [])
            for imp in imports:
                # Parse "import x" or "from x import y"
                if imp.startswith('from '):
                    parts = imp.split()
                    if len(parts) >= 2:
                        dependencies.append(parts[1])
                elif imp.startswith('import '):
                    parts = imp.replace('import ', '').split(',')
                    dependencies.extend([p.strip().split('.')[0] for p in parts])
        
        elif language in ['javascript', 'typescript']:
            # Extract from imports/requires
            imports = analysis.get('imports', [])
            for imp in imports:
                # Parse "import ... from 'x'" or "require('x')"
                if 'from' in imp:
                    parts = imp.split('from')
                    if len(parts) >= 2:
                        dep = parts[1].strip().strip('"').strip("'")
                        dependencies.append(dep)
                elif 'require' in imp:
                    import re
                    match = re.search(r'require\(["\'](.+?)["\']\)', imp)
                    if match:
                        dependencies.append(match.group(1))
        
        elif language == 'java':
            # Extract from imports
            imports = analysis.get('imports', [])
            for imp in imports:
                if imp.startswith('import '):
                    dep = imp.replace('import ', '').replace(';', '').strip()
                    # Get package name
                    parts = dep.split('.')
                    if len(parts) >= 2:
                        dependencies.append('.'.join(parts[:-1]))
        
        return list(set(dependencies))  # Remove duplicates
    
    def build_module_map(self, analyses: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Build a map of modules and their relationships.
        
        Args:
            analyses: List of file analyses
            
        Returns:
            Dictionary mapping module names to their info
        """
        module_map = {}
        
        for analysis in analyses:
            path = analysis.get('path', '')
            name = analysis.get('name', '')
            
            # Extract module name from path
            path_obj = Path(path)
            module_name = path_obj.stem
            
            # Get dependencies
            dependencies = self.extract_dependencies(analysis)
            
            # Count elements
            elements = analysis.get('elements', [])
            classes = [e for e in elements if e.type == 'class']
            functions = [e for e in elements if e.type in ['function', 'method']]
            
            module_map[module_name] = {
                'name': module_name,
                'path': path,
                'language': analysis.get('language', 'unknown'),
                'lines': analysis.get('lines', 0),
                'dependencies': dependencies,
                'classes': classes,
                'functions': functions,
                'num_classes': len(classes),
                'num_functions': len(functions),
            }
        
        return module_map
    
    def extract_api_endpoints(self, analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract API endpoints from analyses.
        
        Args:
            analyses: List of file analyses
            
        Returns:
            List of API endpoint information
        """
        endpoints = []
        
        for analysis in analyses:
            language = analysis.get('language', '')
            content = analysis.get('content', '')
            
            # Look for common API patterns
            if language == 'python':
                # Flask/FastAPI routes
                import re
                route_patterns = [
                    r'@app\.route\(["\']([^"\']+)["\']\)',
                    r'@router\.(get|post|put|delete)\(["\']([^"\']+)["\']\)',
                ]
                
                for pattern in route_patterns:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        endpoints.append({
                            'file': analysis.get('path', ''),
                            'path': match.group(1) if match.lastindex == 1 else match.group(2),
                            'method': match.group(1) if match.lastindex == 2 else 'GET',
                        })
            
            elif language in ['javascript', 'typescript']:
                # Express routes
                import re
                route_pattern = r'router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']\)'
                matches = re.finditer(route_pattern, content)
                for match in matches:
                    endpoints.append({
                        'file': analysis.get('path', ''),
                        'method': match.group(1).upper(),
                        'path': match.group(2),
                    })
        
        return endpoints
