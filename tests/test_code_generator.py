"""
Tests for Code Generator
=========================
"""

import pytest
from unittest.mock import Mock, patch
from bauto.core.code_generator import CodeGenerator


class TestCodeGenerator:
    """Test suite for CodeGenerator."""
    
    def test_initialization(self, mock_ai_interface):
        """Test generator initialization."""
        generator = CodeGenerator(mock_ai_interface)
        
        assert generator.ai is mock_ai_interface
        assert generator.cache_enabled is True
        assert len(generator._code_cache) == 0
    
    def test_generate_simple_instruction(self, mock_ai_interface):
        """Test generating code from simple instruction."""
        mock_ai_interface.generate_with_retry.return_value = """
        env.navigate("https://example.com")
        """
        
        generator = CodeGenerator(mock_ai_interface)
        code = generator.generate("Navigate to example.com")
        
        assert "env.navigate" in code
        assert mock_ai_interface.generate_with_retry.called
    
    def test_code_caching(self, mock_ai_interface):
        """Test that code generation is cached."""
        generator = CodeGenerator(mock_ai_interface, cache_enabled=True)
        
        instruction = "Click button"
        
        # First call
        code1 = generator.generate(instruction)
        
        # Second call - should use cache
        code2 = generator.generate(instruction)
        
        assert code1 == code2
        assert mock_ai_interface.generate_with_retry.call_count == 1
    
    def test_cache_disabled(self, mock_ai_interface):
        """Test with cache disabled."""
        generator = CodeGenerator(mock_ai_interface, cache_enabled=False)
        
        instruction = "Click button"
        
        # Two calls should both hit the AI
        code1 = generator.generate(instruction)
        code2 = generator.generate(instruction)
        
        assert mock_ai_interface.generate_with_retry.call_count == 2
    
    def test_retry_on_error(self, mock_ai_interface):
        """Test code generation with retry on error."""
        generator = CodeGenerator(mock_ai_interface)
        
        error_msg = "Element not found"
        code = generator.generate(
            "Click button",
            retry_on_error=error_msg
        )
        
        # Should pass error to AI for better retry
        assert mock_ai_interface.generate_with_retry.called
        call_args = mock_ai_interface.generate_with_retry.call_args
        assert error_msg in call_args[0][0]
    
    def test_clean_code_markdown_removal(self, mock_ai_interface):
        """Test removal of markdown code blocks."""
        mock_ai_interface.generate_with_retry.return_value = """
        ```python
        env.navigate("https://example.com")
        ```
        """
        
        generator = CodeGenerator(mock_ai_interface)
        code = generator.generate("Navigate to site")
        
        assert "```" not in code
        assert "python" not in code
        assert "env.navigate" in code
    
    def test_clean_code_blank_lines(self, mock_ai_interface):
        """Test removal of excessive blank lines."""
        mock_ai_interface.generate_with_retry.return_value = """
        env.navigate("https://example.com")
        
        
        
        env.wait(2)
        """
        
        generator = CodeGenerator(mock_ai_interface)
        code = generator.generate("Navigate and wait")
        
        # Should have at most single blank lines
        assert "\n\n\n" not in code
    
    def test_function_execution_addition(self, mock_ai_interface):
        """Test that function definitions get called."""
        mock_ai_interface.generate_with_retry.return_value = """
        def main(env):
            env.navigate("https://example.com")
        """
        
        generator = CodeGenerator(mock_ai_interface)
        code = generator.generate("Navigate to site")
        
        # Should add function call
        assert "main(env)" in code or "main" in code.split('\n')[-1]
    
    def test_clear_cache(self, mock_ai_interface):
        """Test clearing the code cache."""
        generator = CodeGenerator(mock_ai_interface)
        
        # Generate and cache
        generator.generate("Test instruction")
        assert len(generator._code_cache) > 0
        
        # Clear cache
        generator.clear_cache()
        assert len(generator._code_cache) == 0
    
    def test_context_passing(self, mock_ai_interface):
        """Test passing context to generation."""
        generator = CodeGenerator(mock_ai_interface)
        
        context = "Previously navigated to homepage"
        code = generator.generate(
            "Click login button",
            context=context
        )
        
        # Context should be in prompt
        call_args = mock_ai_interface.generate_with_retry.call_args
        assert context in call_args[0][0]
    
    def test_system_prompt_present(self, mock_ai_interface):
        """Test that system prompt is included."""
        generator = CodeGenerator(mock_ai_interface)
        
        generator.generate("Test instruction")
        
        call_args = mock_ai_interface.generate_with_retry.call_args
        prompt = call_args[0][0]
        
        assert "Selenium" in prompt
        assert "env.navigate" in prompt
        assert "env.click" in prompt


class TestPromptBuilding:
    """Test prompt building functionality."""
    
    def test_build_basic_prompt(self, mock_ai_interface):
        """Test building basic prompt."""
        generator = CodeGenerator(mock_ai_interface)
        
        prompt = generator._build_prompt(
            "Navigate to site",
            context=None,
            error=None
        )
        
        assert "Navigate to site" in prompt
        assert "INSTRUCTION" in prompt
    
    def test_build_prompt_with_context(self, mock_ai_interface):
        """Test building prompt with context."""
        generator = CodeGenerator(mock_ai_interface)
        
        prompt = generator._build_prompt(
            "Click button",
            context="User is logged in",
            error=None
        )
        
        assert "Click button" in prompt
        assert "User is logged in" in prompt
    
    def test_build_prompt_with_error(self, mock_ai_interface):
        """Test building prompt with error."""
        generator = CodeGenerator(mock_ai_interface)
        
        prompt = generator._build_prompt(
            "Click button",
            context=None,
            error="Element not found"
        )
        
        assert "Element not found" in prompt
        assert "Fix the error" in prompt
