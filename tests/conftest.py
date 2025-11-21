"""
Pytest Configuration and Fixtures for bAUTO Tests
=================================================
"""

import os
import sys
import pytest
from unittest.mock import Mock, MagicMock
from pathlib import Path

# Add bauto to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from bauto.config.settings import Config, ModelConfig, BrowserConfig, AutomationConfig
from bauto.core.ai_interface import AIModelInterface
from bauto.core.parser import InstructionParser
from bauto.engine.browser import BrowserEnvironment


@pytest.fixture
def mock_api_key():
    """Provide a mock API key for tests."""
    original_key = os.environ.get("GOOGLE_API_KEY")
    os.environ["GOOGLE_API_KEY"] = "test-api-key-12345"
    yield "test-api-key-12345"
    if original_key:
        os.environ["GOOGLE_API_KEY"] = original_key
    else:
        os.environ.pop("GOOGLE_API_KEY", None)


@pytest.fixture
def test_config(mock_api_key):
    """Provide a test configuration."""
    return Config(
        model=ModelConfig(
            provider="gemini",
            model_name="models/gemini-2.0-flash",
            api_key=mock_api_key
        ),
        browser=BrowserConfig(
            headless=True,
            profile_dir="test_profile"
        ),
        automation=AutomationConfig(
            retry_attempts=1,
            action_delay=0.1,
            enable_logging=False
        )
    )


@pytest.fixture
def mock_ai_interface():
    """Provide a mock AI interface."""
    mock = Mock(spec=AIModelInterface)
    mock.generate.return_value = "# Generated code\nprint('test')"
    mock.generate_with_retry.return_value = "# Generated code\nprint('test')"
    return mock


@pytest.fixture
def mock_browser_env():
    """Provide a mock browser environment."""
    env = Mock(spec=BrowserEnvironment)
    env.driver = MagicMock()
    env.navigate = Mock()
    env.wait = Mock()
    env.find_element = Mock()
    env.click = Mock()
    env.type_text = Mock()
    env.screenshot = Mock()
    env.get_page_text = Mock(return_value="Sample page text")
    env.get_current_url = Mock(return_value="https://example.com")
    return env


@pytest.fixture
def sample_instructions():
    """Provide sample instructions for testing."""
    return """
    # Navigate to website
    Navigate to https://example.com
    Wait 2 seconds
    
    # Search for something
    Find the search box
    Type "test query" in the search box
    Press Enter
    
    # Take screenshot
    Wait 3 seconds
    Take a screenshot and save as "result.png"
    """


@pytest.fixture
def sample_function_instructions():
    """Provide sample instructions with functions."""
    return """
    # Define login function
    DEFINE_FUNCTION login
    Navigate to https://example.com/login
    Type username in username field
    Type password in password field
    Click login button
    END_FUNCTION
    
    # Use the function
    CALL login
    Wait 2 seconds
    Navigate to dashboard
    """


@pytest.fixture
def parser():
    """Provide a fresh parser instance."""
    return InstructionParser()


@pytest.fixture
def temp_test_dir(tmp_path):
    """Provide a temporary directory for test files."""
    test_dir = tmp_path / "bauto_test"
    test_dir.mkdir()
    return test_dir


@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Clean up test files after each test."""
    yield
    # Cleanup code here if needed
    test_files = ["test_screenshot.png", "test.png", "result.png"]
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
            except:
                pass
