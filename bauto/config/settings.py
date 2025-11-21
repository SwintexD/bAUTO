"""
Configuration Management for bAUTO
==================================

Centralized configuration system for the bAUTO framework.
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class ModelConfig:
    """Configuration for AI models."""
    
    provider: str = "gemini"  # gemini or openai
    model_name: str = "models/gemini-2.0-flash"  # Stable Gemini 2.0 Flash model
    api_key: Optional[str] = None
    temperature: float = 0.0
    max_tokens: int = 2048
    
    def __post_init__(self):
        """Auto-detect API key from environment if not provided."""
        if not self.api_key:
            if self.provider == "gemini":
                self.api_key = os.getenv("GOOGLE_API_KEY")
            elif self.provider == "openai":
                self.api_key = os.getenv("OPENAI_API_KEY")


@dataclass
class BrowserConfig:
    """Configuration for browser automation."""
    
    headless: bool = False
    disable_gpu: bool = True
    no_sandbox: bool = True
    window_size: tuple = (1920, 1080)
    user_agent: Optional[str] = None
    proxy: Optional[str] = None
    profile_dir: str = "bauto_browser_profile"  # Use unique profile
    auto_download_driver: bool = True
    
    # Anti-detection settings
    stealth_mode: bool = True
    disable_automation_flags: bool = True
    
    def get_chrome_options(self) -> Dict[str, Any]:
        """Generate Chrome options dict."""
        options = {}
        
        if self.headless:
            options["--headless"] = None
        if self.disable_gpu:
            options["--disable-gpu"] = None
        if self.no_sandbox:
            options["--no-sandbox"] = None
            options["--disable-dev-shm-usage"] = None
        if self.window_size:
            options[f"--window-size"] = f"{self.window_size[0]},{self.window_size[1]}"
        if self.user_agent:
            options["--user-agent"] = self.user_agent
        if self.proxy:
            options["--proxy-server"] = self.proxy
        if self.profile_dir:
            options["--user-data-dir"] = os.path.abspath(self.profile_dir)
            
        # Anti-detection
        if self.stealth_mode:
            options["--disable-blink-features"] = "AutomationControlled"
            
        return options


@dataclass
class AutomationConfig:
    """Configuration for automation behavior."""
    
    retry_attempts: int = 3
    action_delay: float = 0.5  # seconds between actions
    implicit_wait: float = 10.0  # seconds
    page_load_timeout: float = 30.0  # seconds
    enable_memory: bool = False
    memory_dir: str = "automation_memory"
    screenshot_on_error: bool = True
    error_screenshot_dir: str = "error_screenshots"
    enable_logging: bool = True
    log_level: str = "INFO"
    cache_prompts: bool = True
    
    
@dataclass
class Config:
    """Main configuration class for bAUTO."""
    
    model: ModelConfig = field(default_factory=ModelConfig)
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    automation: AutomationConfig = field(default_factory=AutomationConfig)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "Config":
        """Create Config from dictionary."""
        return cls(
            model=ModelConfig(**config_dict.get("model", {})),
            browser=BrowserConfig(**config_dict.get("browser", {})),
            automation=AutomationConfig(**config_dict.get("automation", {}))
        )
    
    @classmethod
    def load_from_file(cls, filepath: str) -> "Config":
        """Load configuration from YAML or JSON file."""
        import yaml
        import json
        
        with open(filepath, "r") as f:
            if filepath.endswith(".yaml") or filepath.endswith(".yml"):
                config_dict = yaml.safe_load(f)
            elif filepath.endswith(".json"):
                config_dict = json.load(f)
            else:
                raise ValueError("Config file must be .yaml, .yml, or .json")
        
        return cls.from_dict(config_dict)
    
    def validate(self) -> bool:
        """Validate configuration."""
        if not self.model.api_key:
            raise ValueError(f"{self.model.provider.upper()} API key not found in environment")
        return True

