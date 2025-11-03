"""Logging configuration for SourceScribe."""

import logging
import sys
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console


def setup_logger(
    name: str = "sourcescribe",
    level: int = logging.INFO,
    use_rich: bool = True
) -> logging.Logger:
    """
    Set up logger with optional Rich formatting.
    
    Args:
        name: Logger name
        level: Logging level
        use_rich: Use Rich handler for pretty output
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    if use_rich:
        # Use Rich handler for beautiful output
        handler = RichHandler(
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            console=Console(stderr=True),
        )
        handler.setFormatter(logging.Formatter("%(message)s"))
    else:
        # Standard handler
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (defaults to sourcescribe)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name or "sourcescribe")
