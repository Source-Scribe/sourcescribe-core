"""OpenAI GPT API provider."""

from typing import List, Optional, Any, Iterator
from sourcescribe.api.base import BaseLLMProvider, LLMMessage, LLMResponse

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider."""
    
    def __init__(self, *args, **kwargs):
        """Initialize OpenAI provider."""
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI SDK not installed. Install with: pip install openai"
            )
        super().__init__(*args, **kwargs)
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")
        
        self.client = openai.OpenAI(
            api_key=self.api_key,
            timeout=self.timeout,
            base_url=self.base_url,
        )
        
        # Set default model if not provided
        if not self.model:
            self.model = "gpt-4-turbo-preview"
    
    def generate(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> LLMResponse:
        """
        Generate response using GPT.
        
        Args:
            messages: Conversation messages
            system_prompt: System prompt
            **kwargs: Additional parameters
            
        Returns:
            LLMResponse
        """
        self.validate_config()
        
        # Convert messages to OpenAI format
        openai_messages = []
        
        if system_prompt:
            openai_messages.append({"role": "system", "content": system_prompt})
        
        for msg in messages:
            openai_messages.append({"role": msg.role, "content": msg.content})
        
        # Make API call
        response = self.client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
        )
        
        choice = response.choices[0]
        
        return LLMResponse(
            content=choice.message.content or "",
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            finish_reason=choice.finish_reason,
            raw_response=response,
        )
    
    def generate_streaming(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> Iterator[str]:
        """
        Generate streaming response using GPT.
        
        Args:
            messages: Conversation messages
            system_prompt: System prompt
            **kwargs: Additional parameters
            
        Yields:
            Response chunks
        """
        self.validate_config()
        
        # Convert messages to OpenAI format
        openai_messages = []
        
        if system_prompt:
            openai_messages.append({"role": "system", "content": system_prompt})
        
        for msg in messages:
            openai_messages.append({"role": msg.role, "content": msg.content})
        
        # Stream response
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            stream=True,
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
