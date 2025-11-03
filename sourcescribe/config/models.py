"""Pydantic models for SourceScribe configuration."""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, validator


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    OLLAMA = "ollama"


class Verbosity(str, Enum):
    """Documentation verbosity levels."""
    MINIMAL = "minimal"
    NORMAL = "normal"
    DETAILED = "detailed"


class OutputFormat(str, Enum):
    """Supported output formats."""
    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"


class DiagramFormat(str, Enum):
    """Supported diagram formats."""
    MERMAID = "mermaid"
    PLANTUML = "plantuml"


class LLMConfig(BaseModel):
    """LLM provider configuration."""
    provider: LLMProvider = Field(default=LLMProvider.ANTHROPIC, description="LLM provider to use")
    model: str = Field(default="claude-3-5-sonnet-20241022", description="Model identifier")
    api_key: Optional[str] = Field(default=None, description="API key (can be set via env var)")
    base_url: Optional[str] = Field(default=None, description="Custom API base URL (for Ollama)")
    temperature: float = Field(default=0.3, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: int = Field(default=4000, gt=0, description="Maximum tokens in response")
    timeout: int = Field(default=60, gt=0, description="Request timeout in seconds")
    
    class Config:
        use_enum_values = True


class RepositoryConfig(BaseModel):
    """Repository scanning configuration."""
    path: str = Field(default=".", description="Repository root path")
    exclude_patterns: List[str] = Field(
        default_factory=lambda: [
            "*.pyc", "__pycache__", "node_modules", ".git", 
            "*.egg-info", "dist", "build", ".venv", "venv"
        ],
        description="Patterns to exclude from scanning"
    )
    include_patterns: List[str] = Field(
        default_factory=lambda: [
            "*.py", "*.js", "*.ts", "*.jsx", "*.tsx", "*.java",
            "*.go", "*.rs", "*.cpp", "*.c", "*.h", "*.cs", "*.rb",
            "*.php", "*.swift", "*.kt", "*.scala", "*.r"
        ],
        description="Patterns to include in scanning"
    )
    max_file_size: int = Field(default=1048576, gt=0, description="Max file size in bytes (1MB)")
    follow_symlinks: bool = Field(default=False, description="Follow symbolic links")


class OutputConfig(BaseModel):
    """Documentation output configuration."""
    path: str = Field(default="./docs/generated", description="Output directory path")
    format: OutputFormat = Field(default=OutputFormat.MARKDOWN, description="Output format")
    include_diagrams: bool = Field(default=True, description="Include architecture diagrams")
    diagram_format: DiagramFormat = Field(default=DiagramFormat.MERMAID, description="Diagram format")
    overwrite: bool = Field(default=True, description="Overwrite existing documentation")
    create_index: bool = Field(default=True, description="Create index/README file")
    
    class Config:
        use_enum_values = True


class WatchConfig(BaseModel):
    """File watching configuration."""
    enabled: bool = Field(default=True, description="Enable watch mode")
    debounce_seconds: float = Field(default=2.0, ge=0.1, description="Debounce interval for changes")
    batch_changes: bool = Field(default=True, description="Batch multiple changes together")
    recursive: bool = Field(default=True, description="Watch subdirectories recursively")
    
    @validator("debounce_seconds")
    def validate_debounce(cls, v):
        """Validate debounce is reasonable."""
        if v > 60.0:
            raise ValueError("debounce_seconds should not exceed 60 seconds")
        return v


class StyleConfig(BaseModel):
    """Documentation style configuration."""
    include_examples: bool = Field(default=True, description="Include code examples")
    include_architecture: bool = Field(default=True, description="Include architecture overview")
    include_api_docs: bool = Field(default=True, description="Include API documentation")
    include_dependencies: bool = Field(default=True, description="Document dependencies")
    include_metrics: bool = Field(default=False, description="Include code metrics")
    verbosity: Verbosity = Field(default=Verbosity.DETAILED, description="Documentation detail level")
    language: str = Field(default="en", description="Documentation language")
    
    class Config:
        use_enum_values = True


class SourceScribeConfig(BaseModel):
    """Main SourceScribe configuration."""
    llm: LLMConfig = Field(default_factory=LLMConfig, description="LLM configuration")
    repository: RepositoryConfig = Field(default_factory=RepositoryConfig, description="Repository settings")
    output: OutputConfig = Field(default_factory=OutputConfig, description="Output configuration")
    watch: WatchConfig = Field(default_factory=WatchConfig, description="Watch mode settings")
    style: StyleConfig = Field(default_factory=StyleConfig, description="Documentation style")
    
    class Config:
        extra = "allow"  # Allow additional fields for extensibility
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return self.dict(exclude_none=True)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SourceScribeConfig":
        """Create config from dictionary."""
        return cls(**data)
