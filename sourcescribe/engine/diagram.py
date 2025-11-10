"""Mermaid diagram generation."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class DiagramNode:
    """Represents a node in a diagram."""
    id: str
    label: str
    type: str  # class, function, module, etc.
    
@dataclass
class DiagramEdge:
    """Represents an edge in a diagram."""
    source: str
    target: str
    label: Optional[str] = None


class DiagramGenerator:
    """Generate Mermaid.js diagrams from code structure."""
    
    def generate_architecture_diagram(
        self,
        modules: List[Dict[str, Any]],
        title: str = "System Architecture"
    ) -> str:
        """
        Generate architecture diagram with smart filtering and grouping.
        
        Args:
            modules: List of module information
            title: Diagram title
            
        Returns:
            Mermaid diagram as string
        """
        # Group modules by directory/layer
        grouped_modules = self._group_modules_by_layer(modules)
        
        # Select most important modules to show (limit to avoid overwhelming diagram)
        important_modules = self._select_important_modules(modules, max_nodes=50)
        
        # Build module name to index map
        module_index = {m['name']: i for i, m in enumerate(important_modules)}
        
        lines = [
            "```mermaid",
            "graph TD",
            ""
        ]
        
        # Add grouped nodes with styling
        for layer, layer_modules in grouped_modules.items():
            # Only show modules that are in our important list
            layer_important = [m for m in layer_modules if m['name'] in module_index]
            if not layer_important:
                continue
                
            lines.append(f"    %% {layer} Layer")
            for module in layer_important:
                idx = module_index[module['name']]
                node_id = f"M{idx}"
                module_name = module.get('name', f'Module{idx}')
                
                # Add styling based on module characteristics
                style = self._get_node_style(module)
                lines.append(f"    {node_id}[{module_name}]{style}")
            lines.append("")
        
        # Add relationships (filtered to show only significant ones)
        edges_added = 0
        edges_by_importance = []
        unmatched_deps = set()  # Track dependencies that don't match any module
        
        for i, module in enumerate(important_modules):
            deps = module.get('dependencies', [])
            for dep in deps:
                if dep in module_index:
                    j = module_index[dep]
                    # Calculate importance (modules with more deps = more important edges)
                    importance = len(module.get('dependencies', []))
                    edges_by_importance.append((importance, i, j, module['name'], dep))
                else:
                    # Track unmatched for debugging
                    unmatched_deps.add(dep)
        
        # Sort by importance and limit
        edges_by_importance.sort(reverse=True)
        max_edges = min(100, len(edges_by_importance))  # Limit to 100 edges
        
        for _, i, j, from_name, to_name in edges_by_importance[:max_edges]:
            lines.append(f"    M{i} --> M{j}")
            edges_added += 1
        
        # Add styling for different layers
        lines.append("")
        lines.append("    %% Styling")
        for layer, color in [("Frontend", "#e1f5ff"), ("Backend", "#fff3e0"), 
                              ("Database", "#f3e5f5"), ("API", "#e8f5e9"),
                              ("Common", "#fce4ec")]:
            layer_modules = grouped_modules.get(layer, [])
            for module in layer_modules:
                if module['name'] in module_index:
                    idx = module_index[module['name']]
                    lines.append(f"    style M{idx} fill:{color}")
        
        # Add note about filtering if we limited nodes
        if len(modules) > len(important_modules):
            lines.append(f"    %% Showing {len(important_modules)} of {len(modules)} modules")
            lines.append(f"    %% ({edges_added} relationships)")
        elif edges_added == 0:
            lines.append("    %% Note: No internal dependencies detected")
            if unmatched_deps:
                # Show sample of unmatched deps for debugging
                sample_deps = list(unmatched_deps)[:5]
                lines.append(f"    %% Unmatched dependencies (sample): {', '.join(sample_deps)}")
        
        lines.append("```")
        return "\n".join(lines)
    
    def _group_modules_by_layer(self, modules: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group modules by their layer/directory."""
        from pathlib import Path
        
        groups = {
            "Frontend": [],
            "Backend": [],
            "Database": [],
            "API": [],
            "Common": [],
            "Tests": [],
            "Other": []
        }
        
        for module in modules:
            path = module.get('path', '')
            path_lower = path.lower()
            
            # Categorize based on path
            if any(x in path_lower for x in ['frontend', 'client', 'ui', 'components', 'pages', 'src/components']):
                groups["Frontend"].append(module)
            elif any(x in path_lower for x in ['backend', 'server', 'controllers', 'routes', 'middleware']):
                groups["Backend"].append(module)
            elif any(x in path_lower for x in ['models', 'migrations', 'database', 'db', 'schema']):
                groups["Database"].append(module)
            elif any(x in path_lower for x in ['api', 'services', 'providers']):
                groups["API"].append(module)
            elif any(x in path_lower for x in ['common', 'shared', 'utils', 'helpers', 'lib']):
                groups["Common"].append(module)
            elif any(x in path_lower for x in ['test', 'spec', '__tests__']):
                groups["Tests"].append(module)
            else:
                groups["Other"].append(module)
        
        # Remove empty groups
        return {k: v for k, v in groups.items() if v}
    
    def _select_important_modules(self, modules: List[Dict[str, Any]], max_nodes: int = 50) -> List[Dict[str, Any]]:
        """Select the most important modules to display."""
        # Score modules by:
        # 1. Number of dependencies (high = hub)
        # 2. Number of lines (complexity)
        # 3. Number of classes/functions
        
        scored_modules = []
        for module in modules:
            score = 0
            
            # Dependency count (both incoming and outgoing)
            deps = module.get('dependencies', [])
            score += len(deps) * 3  # Outgoing deps
            
            # Incoming dependencies (how many modules depend on this one)
            module_name = module.get('name', '')
            for other in modules:
                if module_name in other.get('dependencies', []):
                    score += 5  # Incoming deps are more important
            
            # Complexity indicators
            score += min(module.get('lines', 0) // 100, 10)  # Lines (capped)
            score += len(module.get('classes', [])) * 4
            score += len(module.get('functions', [])) * 2
            
            # Exclude test files from main diagram
            if 'test' not in module.get('path', '').lower():
                scored_modules.append((score, module))
        
        # Sort by score and take top N
        scored_modules.sort(reverse=True, key=lambda x: x[0])
        return [m for _, m in scored_modules[:max_nodes]]
    
    def _get_node_style(self, module: Dict[str, Any]) -> str:
        """Get visual style for a node based on its characteristics."""
        # Different shapes for different types
        classes = module.get('classes', [])
        functions = module.get('functions', [])
        
        if len(classes) > 3:
            return ":::classModule"
        elif len(functions) > 5:
            return ":::functionModule"
        else:
            return ""
    
    def generate_graph_diagram(
        self,
        modules: List[Dict[str, Any]],
        focus_module: Optional[str] = None,
        depth: int = 2
    ) -> str:
        """
        Generate a focused dependency graph around a specific module.
        
        Args:
            modules: List of module information
            focus_module: Name of module to focus on (shows its dependencies)
            depth: How many levels deep to traverse
            
        Returns:
            Mermaid diagram as string
        """
        if not modules:
            return "```mermaid\ngraph TD\n    Empty[No modules to display]\n```"
        
        # Build dependency graph
        module_map = {m['name']: m for m in modules}
        
        # If no focus module, pick the most connected one
        if not focus_module:
            focus_module = max(modules, 
                             key=lambda m: len(m.get('dependencies', [])))['name']
        
        # BFS to find connected modules within depth
        visited = {focus_module}
        to_visit = [(focus_module, 0)]
        selected_modules = []
        
        while to_visit:
            current, current_depth = to_visit.pop(0)
            if current not in module_map:
                continue
                
            selected_modules.append(module_map[current])
            
            if current_depth < depth:
                # Add dependencies
                deps = module_map[current].get('dependencies', [])
                for dep in deps:
                    if dep not in visited and dep in module_map:
                        visited.add(dep)
                        to_visit.append((dep, current_depth + 1))
        
        # Generate diagram
        lines = [
            "```mermaid",
            "graph TD",
            f"    %% Dependency graph focused on: {focus_module}",
            ""
        ]
        
        # Create index for selected modules
        module_index = {m['name']: i for i, m in enumerate(selected_modules)}
        
        # Add nodes
        for i, module in enumerate(selected_modules):
            node_id = f"M{i}"
            name = module['name']
            
            # Highlight the focus module
            if name == focus_module:
                lines.append(f"    {node_id}[{name}]:::focus")
            else:
                lines.append(f"    {node_id}[{name}]")
        
        lines.append("")
        
        # Add edges
        for i, module in enumerate(selected_modules):
            deps = module.get('dependencies', [])
            for dep in deps:
                if dep in module_index:
                    j = module_index[dep]
                    lines.append(f"    M{i} --> M{j}")
        
        # Add styling
        lines.append("")
        lines.append("    classDef focus fill:#ffeb3b,stroke:#f57c00,stroke-width:3px")
        
        lines.append("```")
        return "\n".join(lines)
    
    def generate_class_diagram(
        self,
        classes: List[Dict[str, Any]],
        title: str = "Class Diagram"
    ) -> str:
        """
        Generate class diagram.
        
        Args:
            classes: List of class information
            title: Diagram title
            
        Returns:
            Mermaid diagram as string
        """
        lines = [
            "```mermaid",
            "classDiagram",
            ""
        ]
        
        for cls in classes:
            class_name = cls.get('name', 'Unknown')
            lines.append(f"    class {class_name} {{")
            
            # Add attributes
            attributes = cls.get('attributes', [])
            for attr in attributes:
                lines.append(f"        {attr}")
            
            # Add methods
            methods = cls.get('methods', [])
            for method in methods:
                lines.append(f"        {method}()")
            
            lines.append("    }")
            lines.append("")
        
        # Add inheritance/relationships
        for cls in classes:
            class_name = cls.get('name', 'Unknown')
            
            # Inheritance
            parent = cls.get('parent')
            if parent:
                lines.append(f"    {parent} <|-- {class_name}")
            
            # Associations
            associations = cls.get('associations', [])
            for assoc in associations:
                lines.append(f"    {class_name} --> {assoc}")
        
        lines.append("```")
        return "\n".join(lines)
    
    def generate_flow_diagram(
        self,
        steps: List[Dict[str, Any]],
        title: str = "Process Flow"
    ) -> str:
        """
        Generate process flow diagram.
        
        Args:
            steps: List of process steps
            title: Diagram title
            
        Returns:
            Mermaid diagram as string
        """
        lines = [
            "```mermaid",
            "flowchart TD",
            f"    Start([Start])",
            ""
        ]
        
        # Add steps
        prev_id = "Start"
        for i, step in enumerate(steps):
            step_id = f"S{i}"
            step_text = step.get('text', f'Step {i+1}')
            step_type = step.get('type', 'process')
            
            # Different shapes for different step types
            if step_type == 'decision':
                lines.append(f"    {step_id}{{{step_text}}}")
            elif step_type == 'data':
                lines.append(f"    {step_id}[/{step_text}/]")
            else:
                lines.append(f"    {step_id}[{step_text}]")
            
            # Connect to previous
            lines.append(f"    {prev_id} --> {step_id}")
            prev_id = step_id
        
        # Add end
        lines.append(f"    {prev_id} --> End([End])")
        lines.append("```")
        return "\n".join(lines)
    
    def generate_sequence_diagram(
        self,
        interactions: List[Dict[str, Any]],
        title: str = "Sequence Diagram"
    ) -> str:
        """
        Generate sequence diagram.
        
        Args:
            interactions: List of interactions between components
            title: Diagram title
            
        Returns:
            Mermaid diagram as string
        """
        lines = [
            "```mermaid",
            "sequenceDiagram",
            ""
        ]
        
        # Extract participants
        participants = set()
        for interaction in interactions:
            participants.add(interaction.get('from', 'Unknown'))
            participants.add(interaction.get('to', 'Unknown'))
        
        # Declare participants
        for participant in sorted(participants):
            lines.append(f"    participant {participant}")
        
        lines.append("")
        
        # Add interactions
        for interaction in interactions:
            from_p = interaction.get('from', 'Unknown')
            to_p = interaction.get('to', 'Unknown')
            message = interaction.get('message', '')
            
            lines.append(f"    {from_p}->>+{to_p}: {message}")
            
            # Add response if available
            response = interaction.get('response')
            if response:
                lines.append(f"    {to_p}-->>-{from_p}: {response}")
        
        lines.append("```")
        return "\n".join(lines)
    
    def generate_entity_relationship_diagram(
        self,
        entities: List[Dict[str, Any]],
        relationships: List[Dict[str, Any]],
        title: str = "Entity Relationship Diagram"
    ) -> str:
        """
        Generate entity relationship diagram.
        
        Args:
            entities: List of entities
            relationships: List of relationships
            title: Diagram title
            
        Returns:
            Mermaid diagram as string
        """
        lines = [
            "```mermaid",
            "erDiagram",
            ""
        ]
        
        # Add entities with attributes
        for entity in entities:
            entity_name = entity.get('name', 'Unknown')
            attributes = entity.get('attributes', [])
            
            lines.append(f"    {entity_name} {{")
            for attr in attributes:
                attr_name = attr.get('name', 'field')
                attr_type = attr.get('type', 'string')
                lines.append(f"        {attr_type} {attr_name}")
            lines.append("    }")
            lines.append("")
        
        # Add relationships
        for rel in relationships:
            from_e = rel.get('from', 'Unknown')
            to_e = rel.get('to', 'Unknown')
            rel_type = rel.get('type', '||--||')  # one-to-one
            label = rel.get('label', '')
            
            lines.append(f"    {from_e} {rel_type} {to_e} : {label}")
        
        lines.append("```")
        return "\n".join(lines)
