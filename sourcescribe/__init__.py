"""
SourceScribe - Auto-documentation engine using LLMs.

An intelligent documentation generator that watches codebases and creates
comprehensive documentation with architecture diagrams using Claude, OpenAI, or Ollama.
"""

__version__ = "1.2.4"
__author__ = "SourceScribe Contributors"

from sourcescribe.engine.generator import DocumentationGenerator
from sourcescribe.config.models import SourceScribeConfig

__all__ = ["DocumentationGenerator", "SourceScribeConfig", "__version__"]
