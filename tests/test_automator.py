"""
Tests for Browser Automator
============================
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from bauto.core.automator import BrowserAutomator
from bauto.config.settings import Config


class TestBrowserAutomator:
    """Test suite for BrowserAutomator."""
    
    def test_initialization_with_config(self, test_config):
        """Test automator initialization with config."""
        with patch('bauto.core.automator.AIModelInterface'):
            automator = BrowserAutomator(test_config)
            
            assert automator.config == test_config
            assert automator.ai is not None
            assert automator.parser is not None
            assert automator.code_generator is not None
    
    def test_initialization_without_config(self, mock_api_key):
        """Test automator initialization without config."""
        with patch('bauto.core.automator.AIModelInterface'):
            automator = BrowserAutomator()
            
            assert automator.config is not None
            assert isinstance(automator.config, Config)
    
    @patch('bauto.core.automator.create_browser')
    @patch('bauto.core.automator.ActionEngine')
    def test_initialize_browser(self, mock_engine, mock_create_browser, test_config):
        """Test browser initialization."""
        mock_driver = MagicMock()
        mock_env = MagicMock()
        mock_create_browser.return_value = (mock_driver, mock_env)
        
        with patch('bauto.core.automator.AIModelInterface'):
            automator = BrowserAutomator(test_config)
            automator._initialize_browser()
            
            assert automator.driver is not None
            assert automator.env is not None
            assert automator.engine is not None
            assert mock_create_browser.called
    
    def test_parse_instructions(self, test_config, sample_instructions):
        """Test instruction parsing."""
        with patch('bauto.core.automator.AIModelInterface'):
            automator = BrowserAutomator(test_config)
            actions = automator.parser.parse(sample_instructions)
            
            assert len(actions) > 0
            assert isinstance(actions, list)
    
    @patch('bauto.core.automator.create_browser')
    @patch('bauto.core.automator.ActionEngine')
    def test_execute_action_success(self, mock_engine_class, mock_create_browser, test_config):
        """Test successful action execution."""
        # Setup mocks
        mock_driver = MagicMock()
        mock_env = MagicMock()
        mock_create_browser.return_value = (mock_driver, mock_env)
        
        mock_engine = MagicMock()
        mock_engine.execute.return_value = (True, None)
        mock_engine_class.return_value = mock_engine
        
        with patch('bauto.core.automator.AIModelInterface'):
            automator = BrowserAutomator(test_config)
            automator._initialize_browser()
            
            success = automator._execute_action("Navigate to site")
            
            assert success is True
            assert mock_engine.execute.called
    
    @patch('bauto.core.automator.create_browser')
    @patch('bauto.core.automator.ActionEngine')
    def test_execute_action_failure(self, mock_engine_class, mock_create_browser, test_config):
        """Test failed action execution."""
        # Setup mocks
        mock_driver = MagicMock()
        mock_env = MagicMock()
        mock_create_browser.return_value = (mock_driver, mock_env)
        
        mock_engine = MagicMock()
        mock_engine.execute.return_value = (False, "Error occurred")
        mock_engine_class.return_value = mock_engine
        
        # Disable retries for this test
        test_config.automation.retry_attempts = 1
        
        with patch('bauto.core.automator.AIModelInterface'):
            automator = BrowserAutomator(test_config)
            automator._initialize_browser()
            
            success = automator._execute_action("Invalid action")
            
            assert success is False
    
    def test_cleanup(self, test_config):
        """Test cleanup of resources."""
        with patch('bauto.core.automator.AIModelInterface'):
            automator = BrowserAutomator(test_config)
            
            # Mock driver
            mock_driver = MagicMock()
            automator.driver = mock_driver
            
            automator._cleanup()
            
            assert mock_driver.quit.called
            assert automator.driver is None
    
    @patch('bauto.core.automator.create_browser')
    @patch('bauto.core.automator.ActionEngine')
    def test_get_page_text(self, mock_engine, mock_create_browser, test_config):
        """Test getting page text."""
        mock_driver = MagicMock()
        mock_env = MagicMock()
        mock_env.get_page_text.return_value = "Sample text"
        mock_create_browser.return_value = (mock_driver, mock_env)
        
        with patch('bauto.core.automator.AIModelInterface'):
            automator = BrowserAutomator(test_config)
            automator._initialize_browser()
            
            text = automator.get_page_text()
            
            assert text == "Sample text"
            assert mock_env.get_page_text.called
    
    @patch('bauto.core.automator.create_browser')
    @patch('bauto.core.automator.ActionEngine')
    def test_get_current_url(self, mock_engine, mock_create_browser, test_config):
        """Test getting current URL."""
        mock_driver = MagicMock()
        mock_env = MagicMock()
        mock_env.get_current_url.return_value = "https://example.com"
        mock_create_browser.return_value = (mock_driver, mock_env)
        
        with patch('bauto.core.automator.AIModelInterface'):
            automator = BrowserAutomator(test_config)
            automator._initialize_browser()
            
            url = automator.get_current_url()
            
            assert url == "https://example.com"
            assert mock_env.get_current_url.called
    
    @patch('bauto.core.automator.create_browser')
    @patch('bauto.core.automator.ActionEngine')
    def test_screenshot(self, mock_engine, mock_create_browser, test_config):
        """Test taking screenshot."""
        mock_driver = MagicMock()
        mock_env = MagicMock()
        mock_create_browser.return_value = (mock_driver, mock_env)
        
        with patch('bauto.core.automator.AIModelInterface'):
            automator = BrowserAutomator(test_config)
            automator._initialize_browser()
            
            automator.screenshot("test.png")
            
            assert mock_env.screenshot.called
            assert mock_env.screenshot.call_args[0][0] == "test.png"


class TestAutomatorIntegration:
    """Integration tests for automator."""
    
    @patch('bauto.core.automator.create_browser')
    @patch('bauto.core.automator.ActionEngine')
    def test_run_simple_instructions(self, mock_engine_class, mock_create_browser, test_config):
        """Test running simple instructions end-to-end."""
        # Setup mocks
        mock_driver = MagicMock()
        mock_env = MagicMock()
        mock_create_browser.return_value = (mock_driver, mock_env)
        
        mock_engine = MagicMock()
        mock_engine.execute.return_value = (True, None)
        mock_engine_class.return_value = mock_engine
        
        with patch('bauto.core.automator.AIModelInterface') as mock_ai_class:
            mock_ai = MagicMock()
            mock_ai.generate_with_retry.return_value = "env.navigate('https://example.com')"
            mock_ai_class.return_value = mock_ai
            
            automator = BrowserAutomator(test_config)
            
            instructions = "Navigate to https://example.com"
            success = automator.run(instructions, close_browser=True)
            
            assert success is True
            assert mock_driver.quit.called
    
    @patch('bauto.core.automator.read_instructions')
    @patch('bauto.core.automator.create_browser')
    @patch('bauto.core.automator.ActionEngine')
    def test_run_from_file(self, mock_engine_class, mock_create_browser, 
                          mock_read_instructions, test_config, tmp_path):
        """Test running from instruction file."""
        # Setup mocks
        mock_read_instructions.return_value = "Navigate to site"
        
        mock_driver = MagicMock()
        mock_env = MagicMock()
        mock_create_browser.return_value = (mock_driver, mock_env)
        
        mock_engine = MagicMock()
        mock_engine.execute.return_value = (True, None)
        mock_engine_class.return_value = mock_engine
        
        with patch('bauto.core.automator.AIModelInterface') as mock_ai_class:
            mock_ai = MagicMock()
            mock_ai.generate_with_retry.return_value = "env.navigate('https://example.com')"
            mock_ai_class.return_value = mock_ai
            
            automator = BrowserAutomator(test_config)
            
            test_file = str(tmp_path / "test.yaml")
            success = automator.run_from_file(test_file, close_browser=True)
            
            assert mock_read_instructions.called

