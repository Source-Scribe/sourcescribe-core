"""Anthropic Claude API provider."""

from typing import List, Optional, Any, Iterator
from sourcescribe.api.base import BaseLLMProvider, LLMMessage, LLMResponse

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class AnthropicProvider(BaseLLMProvider):
    """Claude API provider using Anthropic SDK."""
    
    def __init__(self, *args, **kwargs):
        """Initialize Anthropic provider."""
        if not ANTHROPIC_AVAILABLE:
            raise ImportError(
                "Anthropic SDK not installed. Install with: pip install anthropic"
            )
        super().__init__(*args, **kwargs)
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")
        
        self.client = anthropic.Anthropic(api_key=self.api_key, timeout=self.timeout)
        
        # Set default model if not provided
        if not self.model:
            self.model = "claude-3-haiku-20240307"
    
    def generate(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> LLMResponse:
        """
        Generate response using Claude.
        
        Args:
            messages: Conversation messages
            system_prompt: System prompt
            **kwargs: Additional parameters
            
        Returns:
            LLMResponse
        """
        self.validate_config()
        
        # Convert messages to Anthropic format
        anthropic_messages = [
            {"role": msg.role if msg.role != "system" else "user", "content": msg.content}
            for msg in messages
            if msg.role != "system"  # System messages handled separately
        ]
        
        # Prepare request parameters
        request_params = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            "messages": anthropic_messages,
        }
        
        if system_prompt:
            request_params["system"] = system_prompt
        
        # Make API call
        response = self.client.messages.create(**request_params)
        
        # Extract content
        content = ""
        for block in response.content:
            if hasattr(block, "text"):
                content += block.text
        
        return LLMResponse(
            content=content,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
            },
            finish_reason=response.stop_reason,
            raw_response=response,
        )
    
    def generate_streaming(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> Iterator[str]:
        """
        Generate streaming response using Claude.
        
        Args:
            messages: Conversation messages
            system_prompt: System prompt
            **kwargs: Additional parameters
            
        Yields:
            Response chunks
        """
        self.validate_config()
        
        # Convert messages to Anthropic format
        anthropic_messages = [
            {"role": msg.role if msg.role != "system" else "user", "content": msg.content}
            for msg in messages
            if msg.role != "system"
        ]
        
        # Prepare request parameters
        request_params = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            "messages": anthropic_messages,
        }
        
        if system_prompt:
            request_params["system"] = system_prompt
        
        # Stream response
        with self.client.messages.stream(**request_params) as stream:
            for text in stream.text_stream:
                yield text
