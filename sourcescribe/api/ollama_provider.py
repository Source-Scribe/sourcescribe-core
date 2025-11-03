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
        
        # Check if Ollama is running
        self._check_connection()
    
    def _check_connection(self) -> None:
        """Check if Ollama server is accessible."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.base_url}\n"
                "Make sure Ollama is installed and running:\n"
                "  1. Install: https://ollama.ai/download\n"
                "  2. Start: ollama serve\n"
                "  3. Pull a model: ollama pull llama2"
            )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ConnectionError(
                    f"Ollama server at {self.base_url} is not responding correctly.\n"
                    "Make sure you're running a compatible version of Ollama."
                )
            raise
    
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
        try:
            response = requests.post(
                f"{self.api_url}/generate",
                json=data,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                # Try to get list of available models
                try:
                    tags_response = requests.get(f"{self.api_url}/tags", timeout=5)
                    if tags_response.ok:
                        models_data = tags_response.json()
                        available_models = [m.get('name', '') for m in models_data.get('models', [])]
                        if available_models:
                            raise ValueError(
                                f"Model '{self.model}' not found. Available models: {', '.join(available_models)}\n"
                                f"Pull the model with: ollama pull {self.model}"
                            )
                except:
                    pass
                raise ConnectionError(
                    f"Ollama API endpoint not found.\n"
                    f"Make sure:\n"
                    f"  1. Ollama is running: ollama serve\n"
                    f"  2. Model '{self.model}' is pulled: ollama pull {self.model}\n"
                    f"  3. You're using a compatible Ollama version"
                )
            raise
        
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
