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
    
    def _generate_docusaurus_sidebar(self, analyses: List[Dict[str, Any]]) -> None:
        """Generate Docusaurus sidebar configuration automatically based on actual file structure."""
        self.logger.info("Generating Docusaurus sidebar configuration")
        
        output_path = Path(self.config.output.path)
        
        # Find website root
        website_root = None
        current = output_path
        for _ in range(5):  # Search up to 5 levels
            current = current.parent
            if (current / "package.json").exists() or (current / "docusaurus.config.ts").exists():
                website_root = current
                break
        
        if not website_root:
            self.logger.warning("Could not find Docusaurus website root, skipping sidebar generation")
            return
        
        # Determine the doc path prefix relative to website/docs
        # If output_path is /path/to/website/docs, prefix is empty
        # If output_path is /path/to/website/docs/api-reference, prefix is 'api-reference'
        docs_dir = website_root / "docs"
        try:
            relative_to_docs = output_path.relative_to(docs_dir)
            prefix = str(relative_to_docs) if str(relative_to_docs) != '.' else ''
        except ValueError:
            # output_path is not under website/docs
            prefix = ''
        
        # Scan the output directory to build sidebar structure
        sidebar_structure = self._scan_docs_structure(output_path, prefix)
        
        # Generate sidebar config
        sidebar_items = self._build_sidebar_items(sidebar_structure)
        
        sidebar_config = f"""/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 
 Auto-generated by SourceScribe
 */

import type {{SidebarsConfig}} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {{
  tutorialSidebar: {sidebar_items},
}};

export default sidebars;
"""
        
        sidebar_path = website_root / "sidebars.ts"
        write_file(str(sidebar_path), sidebar_config)
        self.logger.info(f"Generated Docusaurus sidebar at: {sidebar_path}")
    
    def _scan_docs_structure(self, docs_path: Path, prefix: str) -> Dict[str, Any]:
        """Scan documentation directory and build structure."""
        structure = {
            'readme': None,
            'categories': {}
        }
        
        # Check for README
        if (docs_path / "README.md").exists():
            doc_id = f"{prefix}/README" if prefix else "README"
            structure['readme'] = doc_id
        
        # Scan subdirectories
        for item in sorted(docs_path.iterdir()):
            if item.is_dir():
                category_name = item.name
                category_items = []
                
                # Scan files in this category
                for doc_file in sorted(item.glob("*.md")):
                    if doc_file.name == "README.md":
                        continue  # Skip README in subdirs
                    
                    # Build doc ID without .md extension
                    doc_name = doc_file.stem
                    if prefix:
                        doc_id = f"{prefix}/{category_name}/{doc_name}"
                    else:
                        doc_id = f"{category_name}/{doc_name}"
                    
                    category_items.append({
                        'id': doc_id,
                        'name': doc_name
                    })
                
                if category_items:
                    structure['categories'][category_name] = category_items
        
        return structure
    
    def _build_sidebar_items(self, structure: Dict[str, Any]) -> str:
        """Build sidebar items JSON string from structure."""
        items = []
        
        # Add README if exists
        if structure['readme']:
            items.append(f"""    {{
      type: 'doc',
      id: '{structure['readme']}',
      label: 'Documentation Home',
    }}""")
        
        # Define category order and labels
        category_order = {
            'overview': {'label': 'Overview', 'collapsed': False},
            'getting-started': {'label': 'Getting Started', 'collapsed': False},
            'features': {'label': 'Features', 'collapsed': False},
            'architecture': {'label': 'Architecture', 'collapsed': False},
            'api': {'label': 'API Reference', 'collapsed': True},
            'guides': {'label': 'Guides', 'collapsed': False},
        }
        
        # Build categories in order
        for category_name in category_order.keys():
            if category_name in structure['categories']:
                category_info = category_order[category_name]
                items.append(self._build_category_item(
                    category_name,
                    category_info['label'],
                    structure['categories'][category_name],
                    category_info['collapsed']
                ))
        
        # Add remaining categories not in the predefined order
        for category_name, category_items in structure['categories'].items():
            if category_name not in category_order:
                label = category_name.replace('-', ' ').replace('_', ' ').title()
                items.append(self._build_category_item(
                    category_name,
                    label,
                    category_items,
                    False
                ))
        
        return "[\n" + ",\n".join(items) + ",\n  ]"
    
    def _build_category_item(self, category_name: str, label: str, items: List[Dict[str, str]], collapsed: bool) -> str:
        """Build a single category item for sidebar."""
        # Define preferred order for common doc names
        doc_order = ['index', 'installation', 'quick-start', 'configuration', 'architecture', 'technology-stack', 'components']
        
        # Sort items by preferred order, then alphabetically
        def sort_key(item):
            name = item['name']
            if name in doc_order:
                return (0, doc_order.index(name))
            return (1, name)
        
        sorted_items = sorted(items, key=sort_key)
        
        # Build items list
        item_ids = [f"        '{item['id']}'" for item in sorted_items]
        items_str = ",\n".join(item_ids)
        
        return f"""    {{
      type: 'category',
      label: '{label}',
      collapsed: {str(collapsed).lower()},
      items: [
{items_str}
      ],
    }}"""
    
    def _update_docusaurus_config(self, analyses: List[Dict[str, Any]]) -> None:
        """Generate/update comprehensive Docusaurus configuration with AI-powered content."""
        from sourcescribe.utils.github_utils import get_github_url_from_git
        import re
        
        self.logger.info("Generating Docusaurus configuration")
        
        # Get GitHub URL
        github_url = self.config.repository.github_url
        if not github_url:
            github_url = get_github_url_from_git(self.config.repository.path)
        
        if not github_url:
            self.logger.warning("No GitHub URL found, using defaults for Docusaurus config")
            org_name = "your-org"
            repo_name = "your-repo"
        else:
            # Parse GitHub URL to get org and repo
            try:
                parts = github_url.rstrip('/').split('/')
                org_name = parts[-2]
                repo_name = parts[-1].replace('.git', '')
            except (IndexError, AttributeError):
                self.logger.warning(f"Could not parse GitHub URL: {github_url}")
                org_name = "your-org"
                repo_name = "your-repo"
        
        # Try to find docusaurus.config.ts
        output_path = Path(self.config.output.path)
        website_root = None
        current = output_path
        
        for _ in range(5):  # Search up to 5 levels
            current = current.parent
            config_file = current / "docusaurus.config.ts"
            if config_file.exists():
                website_root = current
                break
        
        if not website_root:
            self.logger.warning("Could not find docusaurus.config.ts, skipping config update")
            return
        
        config_path = website_root / "docusaurus.config.ts"
        
        # Infer project title from repo name or README
        title = self._infer_project_title(repo_name, analyses)
        
        # Generate tagline using AI
        tagline = self._generate_tagline(analyses)
        
        # Generate the complete Docusaurus config
        config_content = self._generate_docusaurus_config_content(
            title=title,
            tagline=tagline,
            github_url=github_url if github_url else f"https://github.com/{org_name}/{repo_name}",
            org_name=org_name,
            repo_name=repo_name
        )
        
        try:
            write_file(str(config_path), config_content)
            self.logger.info(f"Generated Docusaurus config at: {config_path}")
            self.logger.info(f"  - Title: {title}")
            self.logger.info(f"  - Tagline: {tagline}")
            self.logger.info(f"  - Organization: {org_name}")
            self.logger.info(f"  - Project: {repo_name}")
        except Exception as e:
            self.logger.error(f"Failed to update Docusaurus config: {e}")
    
    def _infer_project_title(self, repo_name: str, analyses: List[Dict[str, Any]]) -> str:
        """Infer project title from repo name and analysis."""
        # Check if there's a clear project name in README or package.json
        repo_path = Path(self.config.repository.path)
        
        # Try package.json first
        package_json = repo_path / "package.json"
        if package_json.exists():
            try:
                import json
                with open(package_json) as f:
                    data = json.load(f)
                    if 'name' in data and not data['name'].startswith('@'):
                        return data['name'].replace('-', ' ').title()
            except:
                pass
        
        # Try pyproject.toml
        pyproject = repo_path / "pyproject.toml"
        if pyproject.exists():
            try:
                import re
                with open(pyproject) as f:
                    content = f.read()
                    match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
                    if match:
                        return match.group(1).replace('-', ' ').title()
            except:
                pass
        
        # Fallback to formatted repo name
        return repo_name.replace('-', ' ').replace('_', ' ').title()
    
    def _generate_tagline(self, analyses: List[Dict[str, Any]]) -> str:
        """Generate a catchy tagline using AI."""
        self.logger.info("Generating project tagline with AI")
        
        # Build context from analyses
        context = self._build_project_context(analyses, max_files=5)
        
        prompt = f"""Based on this codebase analysis, generate a concise, catchy tagline (max 80 characters).

{context}

Requirements:
- Under 80 characters
- Clear and descriptive
- Professional but engaging
- No buzzwords or jargon
- Focus on what the project does and who it's for

Return ONLY the tagline text, nothing else."""

        try:
            messages = [
                LLMMessage(role="system", content=self._get_system_prompt()),
                LLMMessage(role="user", content=prompt)
            ]
            
            response = self.llm_provider.generate(messages)
            tagline = response.strip().strip('"').strip("'")
            
            # Validate length
            if len(tagline) > 100:
                tagline = tagline[:97] + "..."
            
            return tagline
        except Exception as e:
            self.logger.warning(f"Failed to generate tagline with AI: {e}")
            return "Auto-generated documentation for your project"
    
    def _generate_docusaurus_config_content(
        self,
        title: str,
        tagline: str,
        github_url: str,
        org_name: str,
        repo_name: str
    ) -> str:
        """Generate complete Docusaurus configuration content."""
        
        # Determine if we're outputting to a subdirectory
        output_path = Path(self.config.output.path)
        website_root = output_path.parent.parent if 'docs' in str(output_path) else output_path.parent
        
        # Try to find if docs are in a subdirectory
        docs_dir = website_root / "docs"
        
        config = f"""import {{themes as prismThemes}} from 'prism-react-renderer';
import type {{Config}} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {{
  title: '{title}',
  tagline: '{tagline}',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {{
    v4: true,
  }},

  // Set the production url of your site here
  url: 'https://{org_name}.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/{repo_name}/',

  // GitHub pages deployment config
  organizationName: '{org_name}',
  projectName: '{repo_name}',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {{
    defaultLocale: 'en',
    locales: ['en'],
  }},

  presets: [
    [
      'classic',
      {{
        docs: {{
          sidebarPath: './sidebars.ts',
          editUrl: '{github_url}/tree/main/website/',
        }},
        blog: false,
        theme: {{
          customCss: './src/css/custom.css',
        }},
      }} satisfies Preset.Options,
    ],
  ],

  markdown: {{
    mermaid: true,
  }},
  themes: ['@docusaurus/theme-mermaid'],

  themeConfig: {{
    mermaid: {{
      theme: {{light: 'neutral', dark: 'dark'}},
      options: {{
        fontSize: 16,
        nodeSpacing: 50,
        rankSpacing: 50,
        curve: 'basis',
        padding: 15,
      }},
    }},
    image: 'img/social-card.jpg',
    colorMode: {{
      respectPrefersColorScheme: true,
    }},
    navbar: {{
      title: '{title}',
      logo: {{
        alt: '{title} Logo',
        src: 'img/logo.svg',
      }},
      items: [
        {{
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Documentation',
        }},
        {{
          href: '{github_url}',
          label: 'GitHub',
          position: 'right',
        }},
      ],
    }},
    footer: {{
      style: 'dark',
      links: [
        {{
          title: 'Documentation',
          items: [
            {{
              label: 'Getting Started',
              to: '/docs/getting-started/installation',
            }},
            {{
              label: 'Overview',
              to: '/docs/overview/index',
            }},
          ],
        }},
        {{
          title: 'Community',
          items: [
            {{
              label: 'GitHub',
              href: '{github_url}',
            }},
            {{
              label: 'Issues',
              href: '{github_url}/issues',
            }},
          ],
        }},
        {{
          title: 'More',
          items: [
            {{
              label: 'Repository',
              href: '{github_url}',
            }},
          ],
        }},
      ],
      copyright: `Copyright © ${{new Date().getFullYear()}} {title}. Built with Docusaurus.`,
    }},
    prism: {{
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'json', 'python', 'typescript', 'javascript'],
    }},
  }} satisfies Preset.ThemeConfig,
}};

export default config;
"""
        return config
