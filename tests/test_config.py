"""
Tests for Configuration System
===============================
"""

import pytest
import os
from bauto.config.settings import Config, ModelConfig, BrowserConfig, AutomationConfig


class TestModelConfig:
    """Test suite for ModelConfig."""
    
    def test_default_config(self, mock_api_key):
        """Test default model configuration."""
        config = ModelConfig()
        
        assert config.provider == "gemini"
        assert "gemini" in config.model_name.lower()
        assert config.temperature == 0.0
        assert config.max_tokens == 2048
    
    def test_custom_config(self, mock_api_key):
        """Test custom model configuration."""
        config = ModelConfig(
            provider="gemini",
            model_name="models/gemini-2.0-flash-exp",
            temperature=0.5,
            max_tokens=4096
        )
        
        assert config.provider == "gemini"
        assert config.model_name == "models/gemini-2.0-flash-exp"
        assert config.temperature == 0.5
        assert config.max_tokens == 4096
    
    def test_api_key_from_env(self, mock_api_key):
        """Test API key detection from environment."""
        config = ModelConfig(provider="gemini")
        
        assert config.api_key == mock_api_key


class TestBrowserConfig:
    """Test suite for BrowserConfig."""
    
    def test_default_config(self):
        """Test default browser configuration."""
        config = BrowserConfig()
        
        assert config.headless is False
        assert config.stealth_mode is True
        assert config.window_size == (1920, 1080)
    
    def test_custom_config(self):
        """Test custom browser configuration."""
        config = BrowserConfig(
            headless=True,
            window_size=(1280, 720),
            user_agent="CustomAgent/1.0"
        )
        
        assert config.headless is True
        assert config.window_size == (1280, 720)
        assert config.user_agent == "CustomAgent/1.0"
    
    def test_chrome_options_generation(self):
        """Test Chrome options generation."""
        config = BrowserConfig(
            headless=True,
            stealth_mode=True,
            profile_dir="custom_profile"
        )
        
        options = config.get_chrome_options()
        
        assert "--headless" in options
        assert "--disable-blink-features" in options
        assert "--user-data-dir" in options


class TestAutomationConfig:
    """Test suite for AutomationConfig."""
    
    def test_default_config(self):
        """Test default automation configuration."""
        config = AutomationConfig()
        
        assert config.retry_attempts == 3
        assert config.action_delay == 0.5
        assert config.screenshot_on_error is True
        assert config.enable_logging is True
    
    def test_custom_config(self):
        """Test custom automation configuration."""
        config = AutomationConfig(
            retry_attempts=5,
            action_delay=1.0,
            screenshot_on_error=False,
            log_level="DEBUG"
        )
        
        assert config.retry_attempts == 5
        assert config.action_delay == 1.0
        assert config.screenshot_on_error is False
        assert config.log_level == "DEBUG"


class TestConfig:
    """Test suite for main Config class."""
    
    def test_default_config(self, mock_api_key):
        """Test default configuration."""
        config = Config()
        
        assert isinstance(config.model, ModelConfig)
        assert isinstance(config.browser, BrowserConfig)
        assert isinstance(config.automation, AutomationConfig)
    
    def test_custom_config(self, mock_api_key):
        """Test custom configuration."""
        config = Config(
            model=ModelConfig(provider="gemini"),
            browser=BrowserConfig(headless=True),
            automation=AutomationConfig(retry_attempts=5)
        )
        
        assert config.model.provider == "gemini"
        assert config.browser.headless is True
        assert config.automation.retry_attempts == 5
    
    def test_from_dict(self, mock_api_key):
        """Test creating config from dictionary."""
        config_dict = {
            "model": {
                "provider": "gemini",
                "model_name": "models/gemini-2.0-flash"
            },
            "browser": {
                "headless": True
            },
            "automation": {
                "retry_attempts": 2
            }
        }
        
        config = Config.from_dict(config_dict)
        
        assert config.model.provider == "gemini"
        assert config.browser.headless is True
        assert config.automation.retry_attempts == 2
    
    def test_validation_success(self, mock_api_key):
        """Test successful configuration validation."""
        config = Config()
        
        assert config.validate() is True
    
    def test_validation_failure(self):
        """Test configuration validation failure."""
        # Remove API key from environment
        original_key = os.environ.pop("GOOGLE_API_KEY", None)
        
        try:
            config = Config(model=ModelConfig(api_key=None))
            
            with pytest.raises(ValueError, match="API key not found"):
                config.validate()
        finally:
            # Restore API key
            if original_key:
                os.environ["GOOGLE_API_KEY"] = original_key
