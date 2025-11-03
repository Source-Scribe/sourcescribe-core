"""Ollama local LLM provider."""

import requests
from typing import List, Optional, Any, Iterator, Dict
from sourcescribe.api.base import BaseLLMProvider, LLMMessage, LLMResponse


class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider."""
    
    def __init__(self, *args, **kwargs):
        """Initialize Ollama provider."""
        super().__init__(*args, **kwargs)
        
        # Set default base URL if not provided
        if not self.base_url:
            self.base_url = "http://localhost:11434"
        
        # Set default model if not provided
        if not self.model:
            self.model = "llama2"
        
        self.api_url = f"{self.base_url}/api"
    
    def generate(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> LLMResponse:
        """
        Generate response using Ollama.
        
        Args:
            messages: Conversation messages
            system_prompt: System prompt
            **kwargs: Additional parameters
            
        Returns:
            LLMResponse
        """
        self.validate_config()
        
        # Build prompt from messages
        prompt = self._build_prompt(messages, system_prompt)
        
        # Prepare request
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.temperature),
                "num_predict": kwargs.get("max_tokens", self.max_tokens),
            }
        }
        
        # Make API call
        response = requests.post(
            f"{self.api_url}/generate",
            json=data,
            timeout=self.timeout,
        )
        response.raise_for_status()
        
        result = response.json()
        
        return LLMResponse(
            content=result.get("response", ""),
            model=self.model,
            usage={
                "prompt_tokens": result.get("prompt_eval_count", 0),
                "completion_tokens": result.get("eval_count", 0),
                "total_tokens": result.get("prompt_eval_count", 0) + result.get("eval_count", 0),
            },
            finish_reason=result.get("done_reason"),
            raw_response=result,
        )
    
    def generate_streaming(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> Iterator[str]:
        """
        Generate streaming response using Ollama.
        
        Args:
            messages: Conversation messages
            system_prompt: System prompt
            **kwargs: Additional parameters
            
        Yields:
            Response chunks
        """
        self.validate_config()
        
        # Build prompt from messages
        prompt = self._build_prompt(messages, system_prompt)
        
        # Prepare request
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": kwargs.get("temperature", self.temperature),
                "num_predict": kwargs.get("max_tokens", self.max_tokens),
            }
        }
        
        # Stream response
        response = requests.post(
            f"{self.api_url}/generate",
            json=data,
            timeout=self.timeout,
            stream=True,
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                import json
                result = json.loads(line)
                if "response" in result:
                    yield result["response"]
    
    def _build_prompt(self, messages: List[LLMMessage], system_prompt: Optional[str] = None) -> str:
        """Build a single prompt string from messages."""
        parts = []
        
        if system_prompt:
            parts.append(f"System: {system_prompt}\n")
        
        for msg in messages:
            role = msg.role.capitalize()
            parts.append(f"{role}: {msg.content}\n")
        
        parts.append("Assistant:")
        
        return "\n".join(parts)
    
    def list_models(self) -> List[Dict[str, Any]]:
        """
        List available Ollama models.
        
        Returns:
            List of model information dictionaries
        """
        response = requests.get(f"{self.api_url}/tags", timeout=10)
        response.raise_for_status()
        return response.json().get("models", [])
