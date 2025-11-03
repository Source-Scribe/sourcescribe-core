"""Base class for LLM providers."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class LLMMessage:
    """Represents a message in the conversation."""
    role: str  # "system", "user", or "assistant"
    content: str


@dataclass
class LLMResponse:
    """Response from LLM provider."""
    content: str
    model: str
    usage: Dict[str, int]  # tokens used
    finish_reason: Optional[str] = None
    raw_response: Optional[Any] = None


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "",
        temperature: float = 0.3,
        max_tokens: int = 4000,
        timeout: int = 60,
        base_url: Optional[str] = None,
    ):
        """
        Initialize LLM provider.
        
        Args:
            api_key: API key for authentication
            model: Model identifier
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            timeout: Request timeout in seconds
            base_url: Custom API base URL
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.base_url = base_url
    
    @abstractmethod
    def generate(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> LLMResponse:
        """
        Generate a response from the LLM.
        
        Args:
            messages: List of conversation messages
            system_prompt: Optional system prompt
            **kwargs: Additional provider-specific parameters
            
        Returns:
            LLMResponse object
        """
        pass
    
    @abstractmethod
    def generate_streaming(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ):
        """
        Generate a streaming response from the LLM.
        
        Args:
            messages: List of conversation messages
            system_prompt: Optional system prompt
            **kwargs: Additional provider-specific parameters
            
        Yields:
            Chunks of the response
        """
        pass
    
    def validate_config(self) -> bool:
        """
        Validate provider configuration.
        
        Returns:
            True if configuration is valid
        """
        if not self.model:
            raise ValueError("Model must be specified")
        return True
    
    @staticmethod
    def format_code_context(
        file_path: str,
        code: str,
        language: str,
        description: Optional[str] = None
    ) -> str:
        """
        Format code context for LLM.
        
        Args:
            file_path: Path to the file
            code: Code content
            language: Programming language
            description: Optional description
            
        Returns:
            Formatted code context
        """
        context = f"File: `{file_path}`\n"
        if description:
            context += f"Description: {description}\n"
        context += f"Language: {language}\n\n"
        context += f"```{language}\n{code}\n```"
        return context
