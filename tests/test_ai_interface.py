"""
Tests for AI Interface
======================
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from bauto.core.ai_interface import AIModelInterface, GeminiProvider


class TestGeminiProvider:
    """Test suite for GeminiProvider."""
    
    @patch('bauto.core.ai_interface.genai')
    def test_initialization(self, mock_genai, mock_api_key):
        """Test Gemini provider initialization."""
        provider = GeminiProvider(
            api_key=mock_api_key,
            model_name="models/gemini-2.0-flash"
        )
        
        assert provider.api_key == mock_api_key
        assert provider.model_name == "models/gemini-2.0-flash"
        assert mock_genai.configure.called
    
    @patch('bauto.core.ai_interface.genai')
    def test_generate_success(self, mock_genai, mock_api_key):
        """Test successful code generation."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.text = "env.navigate('https://example.com')"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        provider = GeminiProvider(api_key=mock_api_key)
        result = provider.generate("Navigate to example.com")
        
        assert "env.navigate" in result
        assert mock_model.generate_content.called
    
    @patch('bauto.core.ai_interface.genai')
    def test_generate_with_temperature(self, mock_genai, mock_api_key):
        """Test generation with custom temperature."""
        mock_response = MagicMock()
        mock_response.text = "code"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        provider = GeminiProvider(api_key=mock_api_key, temperature=0.5)
        provider.generate("Test", temperature=0.8)
        
        # Should use custom temperature
        assert mock_model.generate_content.called
    
    @patch('bauto.core.ai_interface.genai')
    def test_cache_functionality(self, mock_genai, mock_api_key):
        """Test response caching."""
        mock_response = MagicMock()
        mock_response.text = "cached_code"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        provider = GeminiProvider(api_key=mock_api_key)
        
        # First call
        result1 = provider.generate("Test prompt", use_cache=True)
        
        # Second call - should use cache
        result2 = provider.generate("Test prompt", use_cache=True)
        
        assert result1 == result2
        assert mock_model.generate_content.call_count == 1
    
    @patch('bauto.core.ai_interface.genai')
    def test_cache_disabled(self, mock_genai, mock_api_key):
        """Test with cache disabled."""
        mock_response = MagicMock()
        mock_response.text = "code"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        provider = GeminiProvider(api_key=mock_api_key)
        
        # Two calls without cache
        provider.generate("Test", use_cache=False)
        provider.generate("Test", use_cache=False)
        
        assert mock_model.generate_content.call_count == 2
    
    @patch('bauto.core.ai_interface.genai')
    def test_clear_cache(self, mock_genai, mock_api_key):
        """Test clearing cache."""
        mock_response = MagicMock()
        mock_response.text = "code"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        provider = GeminiProvider(api_key=mock_api_key)
        
        # Generate and cache
        provider.generate("Test", use_cache=True)
        assert len(provider._cache) > 0
        
        # Clear cache
        provider.clear_cache()
        assert len(provider._cache) == 0
    
    @patch('bauto.core.ai_interface.genai')
    def test_generate_with_retry_success(self, mock_genai, mock_api_key):
        """Test generate with retry on success."""
        mock_response = MagicMock()
        mock_response.text = "success_code"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        provider = GeminiProvider(api_key=mock_api_key)
        result = provider.generate_with_retry("Test prompt")
        
        assert result == "success_code"
        assert mock_model.generate_content.call_count == 1
    
    @patch('bauto.core.ai_interface.genai')
    @patch('bauto.core.ai_interface.time.sleep')
    def test_generate_with_retry_failure(self, mock_sleep, mock_genai, mock_api_key):
        """Test generate with retry on failure."""
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_genai.GenerativeModel.return_value = mock_model
        
        provider = GeminiProvider(api_key=mock_api_key)
        
        with pytest.raises(Exception):
            provider.generate_with_retry("Test prompt", max_retries=3)
        
        assert mock_model.generate_content.call_count == 3


class TestAIModelInterface:
    """Test suite for AIModelInterface."""
    
    @patch('bauto.core.ai_interface.genai')
    def test_gemini_provider_creation(self, mock_genai, mock_api_key):
        """Test creating Gemini provider."""
        interface = AIModelInterface(
            provider="gemini",
            api_key=mock_api_key,
            model_name="models/gemini-2.0-flash"
        )
        
        assert interface.provider_name == "gemini"
        assert isinstance(interface.provider, GeminiProvider)
    
    def test_unsupported_provider(self, mock_api_key):
        """Test error on unsupported provider."""
        with pytest.raises(ValueError, match="Unsupported AI provider"):
            AIModelInterface(
                provider="unsupported",
                api_key=mock_api_key
            )
    
    @patch('bauto.core.ai_interface.genai')
    def test_generate_method(self, mock_genai, mock_api_key):
        """Test generate method delegation."""
        mock_response = MagicMock()
        mock_response.text = "test_code"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        interface = AIModelInterface(provider="gemini", api_key=mock_api_key)
        result = interface.generate("Test prompt")
        
        assert "test_code" in result
    
    @patch('bauto.core.ai_interface.genai')
    def test_generate_with_retry_method(self, mock_genai, mock_api_key):
        """Test generate_with_retry method delegation."""
        mock_response = MagicMock()
        mock_response.text = "retry_code"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        interface = AIModelInterface(provider="gemini", api_key=mock_api_key)
        result = interface.generate_with_retry("Test prompt")
        
        assert "retry_code" in result
    
    @patch('bauto.core.ai_interface.genai')
    def test_clear_cache_method(self, mock_genai, mock_api_key):
        """Test clear_cache method delegation."""
        interface = AIModelInterface(provider="gemini", api_key=mock_api_key)
        
        # Should not raise error
        interface.clear_cache()
