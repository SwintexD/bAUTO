"""
AI Language Model Interface for bAUTO
=====================================

Unified interface for different AI providers (Gemini, OpenAI, etc.)
"""

import os
import time
import logging
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod

import google.generativeai as genai

logger = logging.getLogger(__name__)


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate completion from prompt."""
        pass
    
    @abstractmethod
    def generate_with_retry(self, prompt: str, max_retries: int = 3, **kwargs) -> str:
        """Generate with automatic retry on failure."""
        pass


class GeminiProvider(AIProvider):
    """Google Gemini AI provider."""
    
    def __init__(self, api_key: str, model_name: str = "models/gemini-2.0-flash", 
                 temperature: float = 0.0, max_tokens: int = 2048):
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._cache: Dict[str, str] = {}
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
        logger.info(f"Initialized Gemini provider with model: {self.model_name}")
    
    def generate(self, prompt: str, temperature: Optional[float] = None, 
                 max_tokens: Optional[int] = None, stop_sequences: Optional[List[str]] = None,
                 use_cache: bool = True) -> str:
        """Generate completion from Gemini."""
        
        # Check cache first
        if use_cache and prompt in self._cache:
            logger.debug("Using cached response")
            return self._cache[prompt]
        
        # Prepare generation config
        gen_config = genai.types.GenerationConfig(
            candidate_count=1,
            max_output_tokens=max_tokens or self.max_tokens,
            temperature=temperature if temperature is not None else self.temperature,
            stop_sequences=stop_sequences or []
        )
        
        try:
            response = self.model.generate_content(prompt, generation_config=gen_config)
            text = response.text.strip()
            
            # Clean up code blocks
            text = text.replace("```python", "").replace("```", "").strip()
            
            # Cache the response
            if use_cache:
                self._cache[prompt] = text
            
            return text
            
        except Exception as e:
            logger.error(f"Error generating from Gemini: {e}")
            raise
    
    def generate_with_retry(self, prompt: str, max_retries: int = 3, 
                           retry_delay: float = 2.0, **kwargs) -> str:
        """Generate with automatic retry on failure."""
        
        for attempt in range(max_retries):
            try:
                return self.generate(prompt, **kwargs)
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                else:
                    logger.error(f"All {max_retries} attempts failed")
                    raise
    
    def clear_cache(self):
        """Clear the response cache."""
        self._cache.clear()
        logger.info("Response cache cleared")


class AIModelInterface:
    """Unified interface for all AI providers."""
    
    def __init__(self, provider: str = "gemini", **config):
        self.provider_name = provider
        
        if provider == "gemini":
            self.provider = GeminiProvider(**config)
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate completion."""
        return self.provider.generate(prompt, **kwargs)
    
    def generate_with_retry(self, prompt: str, **kwargs) -> str:
        """Generate with retry."""
        return self.provider.generate_with_retry(prompt, **kwargs)
    
    def clear_cache(self):
        """Clear cache."""
        self.provider.clear_cache()

