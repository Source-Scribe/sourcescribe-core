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
        Generate architecture diagram.
        
        Args:
            modules: List of module information
            title: Diagram title
            
        Returns:
            Mermaid diagram as string
        """
        lines = [
            "```mermaid",
            "graph TD",
            f"    title[{title}]",
            "    style title fill:#f9f,stroke:#333,stroke-width:2px",
            ""
        ]
        
        # Add modules as nodes with grouping by directory/package
        for i, module in enumerate(modules):
            node_id = f"M{i}"
            module_name = module.get('name', f'Module{i}')
            lines.append(f"    {node_id}[{module_name}]")
        
        lines.append("")  # Blank line for readability
        
        # Add relationships if available
        edges_added = 0
        for i, module in enumerate(modules):
            deps = module.get('dependencies', [])
            for dep in deps:
                # Find dependency module
                for j, other in enumerate(modules):
                    if other.get('name') == dep:
                        lines.append(f"    M{i} --> M{j}")
                        edges_added += 1
        
        # Add note if no relationships found
        if edges_added == 0:
            lines.append("    %% Note: No internal dependencies detected")
        
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
