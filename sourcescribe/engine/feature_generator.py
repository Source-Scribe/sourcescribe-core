"""Feature-based documentation generation methods."""

from typing import List, Dict, Any
from pathlib import Path
from sourcescribe.api.base import LLMMessage
from sourcescribe.utils.file_utils import write_file, create_directory


class FeatureDocumentationMixin:
    """Mixin for feature-based documentation generation."""
    
    def _generate_overview_section(self, analyses: List[Dict[str, Any]]) -> None:
        """Generate Overview section with architecture and tech stack."""
        self.logger.info("Generating Overview section")
        
        # Create overview directory
        overview_dir = Path(self.config.output.path) / "overview"
        create_directory(str(overview_dir))
        
        context = self._build_project_context(analyses)
        system_prompt = self._get_system_prompt()
        
        # 1. Project Overview
        overview_prompt = f"""Analyze this codebase and provide a high-level project overview:

{context}

Generate a comprehensive overview covering:
1. **Project Purpose** - What problem does this solve?
2. **Target Users** - Who is this for?
3. **Key Value Propositions** - Why would someone use this?
4. **Core Capabilities** - What can it do?

Use clear, non-technical language. Format in Markdown with proper headings."""

        response = self.llm_provider.generate(
            messages=[LLMMessage(role="user", content=overview_prompt)],
            system_prompt=system_prompt
        )
        write_file(str(overview_dir / "index.md"), f"# Overview\n\n{response.content}")
        
        # 2. Architecture Overview with diagram
        module_map = self.analyzer.build_module_map(analyses)
        modules = list(module_map.values())
        arch_diagram = self.diagram_generator.generate_architecture_diagram(modules, "System Architecture")
        
        arch_prompt = f"""Analyze this system architecture and explain:

Modules: {len(modules)}
{self._format_modules_for_prompt(modules)}

Generate documentation covering:
1. **High-Level Architecture** - How components work together
2. **Key Components** - Main building blocks and their roles  
3. **Data Flow** - How information moves through the system
4. **Design Principles** - Architectural patterns used

Create a mermaid sequence diagram showing a typical user workflow.
Format in Markdown."""

        response = self.llm_provider.generate(
            messages=[LLMMessage(role="user", content=arch_prompt)],
            system_prompt=system_prompt
        )
        
        arch_content = f"""# Architecture Overview

{response.content}

## System Architecture Diagram

{arch_diagram}
"""
        write_file(str(overview_dir / "architecture.md"), arch_content)
        
        # 3. Technology Stack
        tech_prompt = f"""Based on this codebase analysis, document the technology stack:

{context}

Create a comprehensive technology stack document with:
1. **Programming Languages** - Primary and secondary languages
2. **Frameworks & Libraries** - Key dependencies and why they're used
3. **Development Tools** - Build tools, testing frameworks
4. **Infrastructure** - Deployment, hosting, CI/CD
5. **Third-Party Integrations** - External services and APIs

Format as a well-structured Markdown document."""

        response = self.llm_provider.generate(
            messages=[LLMMessage(role="user", content=tech_prompt)],
            system_prompt=system_prompt
        )
        write_file(str(overview_dir / "technology-stack.md"), f"# Technology Stack\n\n{response.content}")
        
        self.logger.info("Overview section completed")
    
    def _generate_getting_started_section(self, analyses: List[Dict[str, Any]]) -> None:
        """Generate Getting Started guides."""
        self.logger.info("Generating Getting Started section")
        
        getting_started_dir = Path(self.config.output.path) / "getting-started"
        create_directory(str(getting_started_dir))
        
        context = self._build_project_context(analyses)
        system_prompt = self._get_system_prompt()
        
        # 1. Installation Guide with flowchart
        install_prompt = f"""Create a comprehensive installation guide for this project:

{context}

Include:
1. **Prerequisites** - System requirements, dependencies
2. **Installation Steps** - Clear, numbered steps
3. **Environment Setup** - Configuration, environment variables
4. **Verification** - How to test the installation worked
5. **Troubleshooting** - Common installation issues

Create a mermaid flowchart showing the installation process.
Include code blocks and commands. Format in Markdown."""

        response = self.llm_provider.generate(
            messages=[LLMMessage(role="user", content=install_prompt)],
            system_prompt=system_prompt
        )
        write_file(str(getting_started_dir / "installation.md"), f"# Installation\n\n{response.content}")
        
        # 2. Quick Start Guide with sequence diagram
        quickstart_prompt = f"""Create a quick start guide with step-by-step tutorial:

{context}

Create:
1. **First Steps** - Minimal setup to get running
2. **Hello World Example** - Simple working example
3. **What Just Happened?** - Explain what the example did
4. **Next Steps** - Where to go from here

Include a mermaid sequence diagram showing what happens when running the example.
Use code examples. Format in Markdown."""

        response = self.llm_provider.generate(
            messages=[LLMMessage(role="user", content=quickstart_prompt)],
            system_prompt=system_prompt
        )
        write_file(str(getting_started_dir / "quick-start.md"), f"# Quick Start\n\n{response.content}")
        
        # 3. Configuration Guide
        config_prompt = f"""Document the configuration options for this project:

{context}

Cover:
1. **Configuration Files** - Location and format
2. **Configuration Options** - All available settings with descriptions
3. **Environment Variables** - Required and optional
4. **Examples** - Common configuration scenarios
5. **Best Practices** - Recommended settings

Format in Markdown with tables for options."""

        response = self.llm_provider.generate(
            messages=[LLMMessage(role="user", content=config_prompt)],
            system_prompt=system_prompt
        )
        write_file(str(getting_started_dir / "configuration.md"), f"# Configuration\n\n{response.content}")
        
        self.logger.info("Getting Started section completed")
    
    def _generate_feature_sections(self, analyses: List[Dict[str, Any]]) -> None:
        """Generate feature-based documentation sections."""
        self.logger.info("Generating feature sections")
        
        context = self._build_project_context(analyses)
        system_prompt = self._get_system_prompt()
        
        features_dir = Path(self.config.output.path) / "features"
        create_directory(str(features_dir))
        
        # Generate feature-oriented documentation
        feature_docs_prompt = f"""Analyze this codebase and create feature-based documentation:

{context}

Organize the documentation by FEATURES/CAPABILITIES, not files. For example:
- User Authentication & Authorization
- Data Management  
- API Integration
- File Processing
- Monitoring & Logging

For each major feature area, create:
1. **Feature Overview** - Purpose and capabilities
2. **How It Works** - Process flow with mermaid flowchart or sequence diagram
3. **Usage Examples** - Code examples showing how to use this feature
4. **Configuration** - Feature-specific settings
5. **Common Use Cases** - Real-world scenarios

Use mermaid diagrams extensively:
- Sequence diagrams for workflows
- Flowcharts for decision trees
- State diagrams for stateful features

Format as a comprehensive Markdown document with clear sections for each feature."""

        response = self.llm_provider.generate(
            messages=[LLMMessage(role="user", content=feature_docs_prompt)],
            system_prompt=system_prompt
        )
        
        write_file(str(features_dir / "index.md"), f"# Features\n\n{response.content}")
        
        self.logger.info("Feature sections completed")
    
    def _generate_architecture_section(self, analyses: List[Dict[str, Any]]) -> None:
        """Generate detailed architecture documentation."""
        self.logger.info("Generating Architecture section")
        
        arch_dir = Path(self.config.output.path) / "architecture"
        create_directory(str(arch_dir))
        
        module_map = self.analyzer.build_module_map(analyses)
        modules = list(module_map.values())
        arch_diagram = self.diagram_generator.generate_architecture_diagram(modules, "System Architecture")
        
        system_prompt = self._get_system_prompt()
        
        # Component architecture with detailed diagrams
        component_prompt = f"""Create detailed component architecture documentation:

Modules: {len(modules)}
{self._format_modules_for_prompt(modules)}

Document:
1. **Component Breakdown** - Each major component's responsibility
2. **Communication Patterns** - How components interact (with sequence diagrams)
3. **Data Models** - Key data structures (with class diagrams if applicable)
4. **Design Patterns** - Patterns used and why
5. **Extension Points** - How to extend the system

Include multiple mermaid diagrams:
- Component/module diagram
- Sequence diagrams for key workflows
- Class diagrams for important data models
- State diagrams if stateful behavior exists

Format in Markdown with extensive use of diagrams."""

        response = self.llm_provider.generate(
            messages=[LLMMessage(role="user", content=component_prompt)],
            system_prompt=system_prompt
        )
        
        arch_content = f"""# Component Architecture

{response.content}

## System Architecture Diagram

{arch_diagram}
"""
        write_file(str(arch_dir / "components.md"), arch_content)
        
        self.logger.info("Architecture section completed")
    
    def _generate_api_reference_section(self, analyses: List[Dict[str, Any]]) -> None:
        """Generate API reference if applicable."""
        self.logger.info("Generating API Reference section")
        
        endpoints = self.analyzer.extract_api_endpoints(analyses)
        if not endpoints:
            self.logger.info("No API endpoints found, skipping API reference")
            return
        
        api_dir = Path(self.config.output.path) / "api-reference"
        create_directory(str(api_dir))
        
        system_prompt = self._get_system_prompt()
        api_prompt = f"""Document these API endpoints:

{self._format_endpoints_for_prompt(endpoints)}

Create comprehensive API documentation with:
1. **Endpoint Overview** - Purpose and use cases
2. **Request Format** - Parameters, headers, body
3. **Response Format** - Success and error responses with examples
4. **Examples** - cURL and code examples in multiple languages
5. **Authentication** - Required auth mechanisms
6. **Rate Limiting** - If applicable
7. **Error Handling** - Common errors and how to handle them

Include mermaid sequence diagrams showing:
- Authentication flow
- Typical API call flow
- Error handling flow

Format in Markdown with clear sections for each endpoint."""

        response = self.llm_provider.generate(
            messages=[LLMMessage(role="user", content=api_prompt)],
            system_prompt=system_prompt
        )
        
        write_file(str(api_dir / "endpoints.md"), f"# API Reference\n\n{response.content}")
        
        self.logger.info("API Reference section completed")
    
    def _generate_feature_index(self, analyses: List[Dict[str, Any]]) -> None:
        """Generate main index for feature-based docs."""
        self.logger.info("Generating documentation index")
        
        index_content = """# Documentation

Welcome to the documentation! This documentation is organized by features and workflows rather than individual code files.

## 📚 Documentation Structure

### [Overview](./overview/index.md)
High-level understanding of the project
- **[Project Overview](./overview/index.md)** - What this project does and why
- **[Architecture Overview](./overview/architecture.md)** - How the system works
- **[Technology Stack](./overview/technology-stack.md)** - Technologies used

### [Getting Started](./getting-started/installation.md)
Everything you need to begin using the project
- **[Installation](./getting-started/installation.md)** - Set up the project
- **[Quick Start](./getting-started/quick-start.md)** - Get up and running in minutes
- **[Configuration](./getting-started/configuration.md)** - Configure for your needs

### [Features](./features/index.md)
Detailed documentation of each major feature and capability

### [Architecture](./architecture/components.md)
Deep dive into system design, components, and patterns

## 🚀 Quick Links

- **First time here?** Start with [Getting Started → Installation](./getting-started/installation.md)
- **Want to understand the system?** Read [Overview → Architecture](./overview/architecture.md)
- **Looking for specific functionality?** Browse [Features](./features/index.md)

## 💡 Documentation Philosophy

This documentation focuses on:
- **Use cases and workflows** rather than individual files
- **Visual diagrams** to explain complex concepts
- **Practical examples** you can copy and adapt
- **Progressive disclosure** from simple to advanced

"""
        
        output_path = Path(self.config.output.path) / "README.md"
        write_file(str(output_path), index_content)
        
        self.logger.info("Documentation index completed")
