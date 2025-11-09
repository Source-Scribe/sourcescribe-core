"""Main documentation generation engine."""

from typing import List, Dict, Any, Optional, Set
from pathlib import Path
from datetime import datetime
from sourcescribe.api.base import BaseLLMProvider, LLMMessage
from sourcescribe.api.factory import LLMProviderFactory
from sourcescribe.engine.analyzer import CodeAnalyzer
from sourcescribe.engine.diagram import DiagramGenerator
from sourcescribe.engine.feature_generator import FeatureDocumentationMixin
from sourcescribe.config.models import SourceScribeConfig
from sourcescribe.utils.file_utils import find_files, write_file, create_directory, get_relative_path
from sourcescribe.utils.logger import get_logger
from sourcescribe.utils.github_utils import get_github_url_from_git, format_github_link_markdown


class DocumentationGenerator(FeatureDocumentationMixin):
    """Main documentation generation engine."""
    
    def __init__(self, config: SourceScribeConfig):
        """
        Initialize documentation generator.
        
        Args:
            config: SourceScribe configuration
        """
        self.config = config
        self.llm_provider: BaseLLMProvider = LLMProviderFactory.create(config.llm)
        self.analyzer = CodeAnalyzer(config.repository)
        self.diagram_generator = DiagramGenerator()
        self.logger = get_logger(__name__)
        
        # Auto-detect GitHub URL if not configured
        self.github_url = config.repository.github_url
        if not self.github_url:
            self.github_url = get_github_url_from_git(config.repository.path)
            if self.github_url:
                self.logger.info(f"Auto-detected GitHub URL: {self.github_url}")
        
        self.github_branch = config.repository.default_branch
    
    def generate_documentation(
        self,
        files: Optional[List[str]] = None,
        incremental: bool = False
    ) -> None:
        """
        Generate feature-based documentation for the repository.
        
        Args:
            files: Optional list of specific files to document
            incremental: If True, only update changed files
        """
        self.logger.info("Starting feature-based documentation generation")
        
        # Find files to document
        if files is None:
            files = find_files(
                self.config.repository.path,
                include_patterns=self.config.repository.include_patterns,
                exclude_patterns=self.config.repository.exclude_patterns,
                max_size=self.config.repository.max_file_size,
                follow_symlinks=self.config.repository.follow_symlinks,
            )
        
        self.logger.info(f"Found {len(files)} file(s) to analyze")
        
        if not files:
            self.logger.warning("No files found to document")
            return
        
        # Analyze files
        analyses = self.analyzer.analyze_files(files)
        self.logger.info(f"Analyzed {len(analyses)} file(s)")
        
        # Generate process-oriented documentation structure
        self._generate_overview_section(analyses)
        self._generate_getting_started_section(analyses)
        self._generate_feature_sections(analyses)
        
        if self.config.style.include_architecture:
            self._generate_architecture_section(analyses)
        
        if self.config.style.include_api_docs:
            self._generate_api_reference_section(analyses)
        
        # Create index
        if self.config.output.create_index:
            self._generate_feature_index(analyses)
        
        # Generate Docusaurus sidebar if output path suggests Docusaurus structure
        self._generate_docusaurus_sidebar(analyses)
        
        # Update Docusaurus config with GitHub repository information
        self._update_docusaurus_config(analyses)
        
        self.logger.info("Feature-based documentation generation completed")
    
    def _generate_overview(self, analyses: List[Dict[str, Any]]) -> None:
        """Generate project overview documentation."""
        self.logger.info("Generating project overview")
        
        # Build context
        context = self._build_project_context(analyses)
        
        # Generate with LLM
        system_prompt = self._get_system_prompt()
        user_prompt = f"""Generate a comprehensive project overview documentation based on this codebase analysis:

{context}

Include:
1. Project purpose and main functionality
2. Key components and modules
3. Technology stack
4. Project structure overview
5. Getting started information (if applicable)

Format the output in clear Markdown."""
        
        response = self.llm_provider.generate(
            messages=[LLMMessage(role="user", content=user_prompt)],
            system_prompt=system_prompt,
        )
        
        # Save documentation
        output_path = Path(self.config.output.path) / "OVERVIEW.md"
        write_file(str(output_path), response.content)
        self.logger.info(f"Overview saved to: {output_path}")
    
    def _generate_file_docs(self, analyses: List[Dict[str, Any]]) -> None:
        """Generate documentation for individual files."""
        self.logger.info("Generating file documentation")
        
        for analysis in analyses:
            file_path = analysis.get('path', '')
            relative_path = get_relative_path(file_path, self.config.repository.path)
            
            self.logger.debug(f"Documenting: {relative_path}")
            
            # Generate documentation with LLM
            doc_content = self._generate_file_doc(analysis)
            
            # Save to output
            output_path = self._get_output_path_for_file(relative_path)
            write_file(output_path, doc_content)
    
    def _generate_file_doc(self, analysis: Dict[str, Any]) -> str:
        """Generate documentation for a single file."""
        file_path = analysis.get('path', '')
        language = analysis.get('language', 'unknown')
        content = analysis.get('content', '')
        elements = analysis.get('elements', [])
        
        # Build prompt
        elements_summary = "\n".join([
            f"- {e.type}: {e.name}" for e in elements[:20]  # Limit to prevent context overflow
        ])
        
        system_prompt = self._get_system_prompt()
        user_prompt = f"""Analyze and document this {language} code file:

File: {file_path}
Lines: {analysis.get('lines', 0)}

Key Elements:
{elements_summary}

Code:
```{language}
{content[:8000]}  # Limit content to prevent context overflow
```

Generate comprehensive documentation including:
1. File purpose and overview
2. Main components (classes, functions)
3. Key functionality
4. Dependencies and imports
5. Usage examples (if applicable)
6. Important implementation details

Format in Markdown."""
        
        response = self.llm_provider.generate(
            messages=[LLMMessage(role="user", content=user_prompt)],
            system_prompt=system_prompt,
        )
        
        return response.content
    
    def _generate_architecture_docs(self, analyses: List[Dict[str, Any]]) -> None:
        """Generate architecture documentation with diagrams."""
        self.logger.info("Generating architecture documentation")
        
        # Build module map
        module_map = self.analyzer.build_module_map(analyses)
        modules = list(module_map.values())
        
        # Generate architecture diagram
        arch_diagram = self.diagram_generator.generate_architecture_diagram(
            modules=modules,
            title="System Architecture"
        )
        
        # Generate documentation with LLM
        system_prompt = self._get_system_prompt()
        user_prompt = f"""Analyze this codebase architecture and provide comprehensive documentation:

Modules ({len(modules)}):
{self._format_modules_for_prompt(modules)}

Generate documentation covering:
1. Overall system architecture
2. Component organization
3. Module relationships and dependencies
4. Design patterns used
5. Key architectural decisions

Format in Markdown."""
        
        response = self.llm_provider.generate(
            messages=[LLMMessage(role="user", content=user_prompt)],
            system_prompt=system_prompt,
        )
        
        # Combine LLM output with diagram
        full_content = f"""# Architecture Documentation

{response.content}

## Architecture Diagram

{arch_diagram}
"""
        
        # Save
        output_path = Path(self.config.output.path) / "ARCHITECTURE.md"
        write_file(str(output_path), full_content)
        self.logger.info(f"Architecture docs saved to: {output_path}")
    
    def _generate_api_docs(self, analyses: List[Dict[str, Any]]) -> None:
        """Generate API documentation."""
        self.logger.info("Generating API documentation")
        
        # Extract API endpoints
        endpoints = self.analyzer.extract_api_endpoints(analyses)
        
        if not endpoints:
            self.logger.info("No API endpoints found")
            return
        
        # Generate documentation with LLM
        system_prompt = self._get_system_prompt()
        user_prompt = f"""Document these API endpoints:

{self._format_endpoints_for_prompt(endpoints)}

Generate comprehensive API documentation including:
1. Overview of the API
2. Endpoint descriptions
3. Request/response formats
4. Authentication requirements (if applicable)
5. Usage examples

Format in Markdown."""
        
        response = self.llm_provider.generate(
            messages=[LLMMessage(role="user", content=user_prompt)],
            system_prompt=system_prompt,
        )
        
        # Save
        output_path = Path(self.config.output.path) / "API.md"
        write_file(str(output_path), response.content)
        self.logger.info(f"API docs saved to: {output_path}")
    
    def _generate_index(self, analyses: List[Dict[str, Any]]) -> None:
        """Generate index/README file."""
        self.logger.info("Generating index")
        
        # Build index content
        content = f"""# Documentation Index

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Documents

- [Project Overview](OVERVIEW.md)
"""
        
        if self.config.style.include_architecture:
            content += "- [Architecture](ARCHITECTURE.md)\n"
        
        if self.config.style.include_api_docs:
            content += "- [API Documentation](API.md)\n"
        
        content += "\n## File Documentation\n\n"
        
        # List documented files
        for analysis in analyses[:50]:  # Limit to prevent huge index
            relative_path = get_relative_path(
                analysis.get('path', ''),
                self.config.repository.path
            )
            doc_path = self._get_output_path_for_file(relative_path, relative=True)
            content += f"- [{relative_path}]({doc_path})\n"
        
        # Save
        output_path = Path(self.config.output.path) / "README.md"
        write_file(str(output_path), content)
        self.logger.info(f"Index saved to: {output_path}")
    
    def _build_project_context(self, analyses: List[Dict[str, Any]]) -> str:
        """Build context summary for project."""
        total_files = len(analyses)
        total_lines = sum(a.get('lines', 0) for a in analyses)
        
        languages = {}
        for a in analyses:
            lang = a.get('language', 'unknown')
            languages[lang] = languages.get(lang, 0) + 1
        
        github_info = ""
        if self.github_url:
            github_info = f"\n- GitHub Repository: {self.github_url}\n- Branch: {self.github_branch}\n"
        
        context = f"""Project Statistics:
- Files: {total_files}
- Total Lines: {total_lines}
- Languages: {', '.join(f'{k} ({v})' for k, v in languages.items())}{github_info}

File Structure (with GitHub links):
"""
        
        for analysis in analyses[:30]:  # Limit for context
            path = analysis.get('path', '')
            relative = get_relative_path(path, self.config.repository.path)
            
            if self.github_url:
                github_link = format_github_link_markdown(
                    relative,
                    self.github_url,
                    self.github_branch,
                    link_text=relative
                )
                context += f"- {github_link} ({analysis.get('language', 'unknown')})\n"
            else:
                context += f"- {relative} ({analysis.get('language', 'unknown')})\n"
        
        return context
    
    def _format_modules_for_prompt(self, modules: List[Dict[str, Any]]) -> str:
        """Format modules for LLM prompt."""
        lines = []
        for mod in modules[:20]:  # Limit for context
            module_name = mod['name']
            module_path = mod.get('path', '')
            
            # Add GitHub link if available
            github_link = ""
            if self.github_url and module_path:
                relative_path = get_relative_path(module_path, self.config.repository.path)
                github_link = f"\n- GitHub: {self.github_url}/blob/{self.github_branch}/{relative_path}"
            
            lines.append(f"""
Module: {module_name}{github_link}
- Language: {mod['language']}
- Lines: {mod['lines']}
- Classes: {mod['num_classes']}
- Functions: {mod['num_functions']}
- Dependencies: {', '.join(mod['dependencies'][:5])}
""")
        return "\n".join(lines)
    
    def _format_endpoints_for_prompt(self, endpoints: List[Dict[str, Any]]) -> str:
        """Format endpoints for LLM prompt."""
        lines = []
        for ep in endpoints:
            lines.append(f"- {ep.get('method', 'GET')} {ep.get('path', '/')} ({ep.get('file', '')})")
        return "\n".join(lines)
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for LLM."""
        verbosity = self.config.style.verbosity
        
        github_instruction = ""
        if self.github_url:
            github_instruction = f"""
GitHub Links:
- **IMPORTANT**: When referencing specific code, configuration, or implementation details, always include GitHub permalinks
- Use this format: [description]({{github_permalink}})
- Example: "See the [configuration model]({self.github_url}/blob/{self.github_branch}/path/to/file.py#L10-L25)"
- Link to specific line ranges when referencing code blocks
- Link to files when discussing modules or components
- This makes documentation more useful and navigable
"""
        
        return f"""You are an expert technical documentation writer who specializes in creating 
user-centric, process-oriented documentation with extensive visual diagrams.

Documentation Style: {verbosity}

Key Principles:
- **Feature-Focused**: Organize by features/capabilities, not file structure
- **Visual First**: Use mermaid diagrams extensively (sequence, flowchart, class, state)
- **Process-Oriented**: Explain workflows and how things work together
- **User-Centric**: Write for developers who want to USE the system, not just understand the code
- **Progressive Disclosure**: Start high-level, then dive deeper
- **Link to Source**: Reference actual code with GitHub permalinks{github_instruction}

Formatting Guidelines:
- Use clear Markdown with proper heading hierarchy
- Include mermaid diagrams in every major section (minimum 1-2 per document)
- Provide practical code examples with GitHub links to the actual code
- Use tables for configuration options
- Include "How it Works" sections with sequence diagrams
- Add "Common Use Cases" with examples
- Link to source code files and specific lines when mentioning implementation details

Diagram Usage:
- Sequence diagrams for workflows and interactions
- Flowcharts for decision trees and processes
- Component/graph diagrams for architecture
- Class diagrams for data models (when applicable)
- State diagrams for stateful behavior

Write in a professional, clear, and accessible tone. Assume the reader wants to understand 
how to USE the system, not browse through individual source files."""
    
    def _get_output_path_for_file(self, relative_path: str, relative: bool = False) -> str:
        """Get output path for a documented file."""
        # Convert source path to doc path
        path = Path(relative_path)
        doc_name = str(path.with_suffix('.md')).replace('/', '_')
        
        if relative:
            return f"files/{doc_name}"
        
        output_dir = Path(self.config.output.path) / "files"
        create_directory(str(output_dir))
        return str(output_dir / doc_name)
    
    def process_changes(self, changed_files: Set[str]) -> None:
        """
        Process changed files and regenerate documentation.
        
        Args:
            changed_files: Set of changed file paths
        """
        self.logger.info(f"Processing {len(changed_files)} changed file(s)")
        
        # Filter to only included files
        files_to_process = [
            f for f in changed_files
            if self._should_document_file(f)
        ]
        
        if files_to_process:
            self.generate_documentation(files=files_to_process, incremental=True)
    
    def _should_document_file(self, file_path: str) -> bool:
        """Check if file should be documented."""
        from fnmatch import fnmatch
        
        path = Path(file_path)
        path_parts = path.parts
        
        # Check exclude patterns
        for pattern in self.config.repository.exclude_patterns:
            # Check full path
            if fnmatch(str(path), pattern):
                return False
            # Check filename
            if fnmatch(path.name, pattern):
                return False
            # Check if any directory in the path matches
            if not any(c in pattern for c in ['*', '?', '[']):
                if pattern in path_parts:
                    return False
        
        # Check include patterns
        for pattern in self.config.repository.include_patterns:
            if fnmatch(str(path), pattern) or fnmatch(path.name, pattern):
                return True
        
        return False
