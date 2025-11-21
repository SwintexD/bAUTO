"""
Tests for Action Engine
========================

Tests code execution in the action engine.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from bauto.engine.action_engine import ActionEngine


class TestActionEngine:
    """Test ActionEngine functionality."""
    
    def test_execute_simple_code(self, mock_browser_env):
        """Test executing simple valid code."""
        engine = ActionEngine(mock_browser_env, screenshot_on_error=False)
        
        code = "result = 1 + 1"
        success, error = engine.execute(code)
        
        assert success is True
        assert error is None
    
    def test_execute_with_env_access(self, mock_browser_env):
        """Test code execution with env object access."""
        engine = ActionEngine(mock_browser_env, screenshot_on_error=False)
        
        code = "url = env.get_current_url()"
        success, error = engine.execute(code)
        
        assert success is True
        assert error is None
        mock_browser_env.get_current_url.assert_called_once()
    
    def test_execute_invalid_code(self, mock_browser_env):
        """Test executing invalid code."""
        engine = ActionEngine(mock_browser_env, screenshot_on_error=False)
        
        code = "invalid syntax here !!!"
        success, error = engine.execute(code)
        
        assert success is False
        assert error is not None
        assert "SyntaxError" in error
    
    def test_execute_runtime_error(self, mock_browser_env):
        """Test code that raises runtime error."""
        engine = ActionEngine(mock_browser_env, screenshot_on_error=False)
        
        code = "raise ValueError('Test error')"
        success, error = engine.execute(code)
        
        assert success is False
        assert error is not None
        assert "ValueError" in error
        assert "Test error" in error
    
    def test_execution_count_increments(self, mock_browser_env):
        """Test execution count increments correctly."""
        engine = ActionEngine(mock_browser_env, screenshot_on_error=False)
        
        assert engine.execution_count == 0
        
        engine.execute("x = 1")
        assert engine.execution_count == 1
        
        engine.execute("y = 2")
        assert engine.execution_count == 2
    
    def test_screenshot_on_error(self, mock_browser_env):
        """Test screenshot is taken on error when enabled."""
        engine = ActionEngine(
            mock_browser_env,
            screenshot_on_error=True,
            screenshot_dir="test_screenshots"
        )
        
        code = "raise Exception('Test error')"
        success, error = engine.execute(code)
        
        assert success is False
        mock_browser_env.screenshot.assert_called_once()
    
    def test_no_screenshot_when_disabled(self, mock_browser_env):
        """Test no screenshot is taken when disabled."""
        engine = ActionEngine(mock_browser_env, screenshot_on_error=False)
        
        code = "raise Exception('Test error')"
        success, error = engine.execute(code)
        
        assert success is False
        mock_browser_env.screenshot.assert_not_called()
    
    def test_execute_with_custom_context(self, mock_browser_env):
        """Test execution with custom context variables."""
        engine = ActionEngine(mock_browser_env, screenshot_on_error=False)
        
        custom_context = {"custom_var": 42}
        code = "result = custom_var * 2"
        
        success, error = engine.execute(code, context=custom_context)
        
        assert success is True
        assert error is None
    
    def test_driver_available_in_scope(self, mock_browser_env, mock_driver):
        """Test that driver is available in execution scope."""
        engine = ActionEngine(mock_browser_env, screenshot_on_error=False)
        
        code = "current_url = driver.current_url"
        success, error = engine.execute(code)
        
        assert success is True
        assert error is None
    
    def test_keys_available_in_scope(self, mock_browser_env):
        """Test that Selenium Keys are available in scope."""
        engine = ActionEngine(mock_browser_env, screenshot_on_error=False)
        
        code = "enter_key = Keys.ENTER"
        success, error = engine.execute(code)
        
        assert success is True
        assert error is None

