"""
Main Automator Class for bAUTO
===============================

The core automation orchestrator.
"""

import logging
from typing import Optional, List

from ..config.settings import Config
from ..utils.logger import setup_logging
from ..utils.file_utils import read_instructions, save_output
from ..core.ai_interface import AIModelInterface
from ..core.parser import InstructionParser
from ..core.code_generator import CodeGenerator
from ..engine.browser import create_browser, BrowserEnvironment
from ..engine.action_engine import ActionEngine

logger = logging.getLogger(__name__)


class BrowserAutomator:
    """
    Main automation orchestrator for bAUTO.
    
    Coordinates all components to execute natural language automation.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the automator.
        
        Args:
            config: Configuration object. If None, uses defaults.
        """
        
        self.config = config or Config()
        self.config.validate()
        
        # Setup logging
        if self.config.automation.enable_logging:
            setup_logging(level=self.config.automation.log_level)
        
        logger.info("Initializing bAUTO Browser Automator")
        
        # Initialize components
        self.ai = AIModelInterface(
            provider=self.config.model.provider,
            api_key=self.config.model.api_key,
            model_name=self.config.model.model_name,
            temperature=self.config.model.temperature,
            max_tokens=self.config.model.max_tokens
        )
        
        self.parser = InstructionParser()
        self.code_generator = CodeGenerator(
            self.ai, 
            cache_enabled=self.config.automation.cache_prompts
        )
        
        # Browser components (initialized on run)
        self.driver = None
        self.env = None
        self.engine = None
        
        logger.info("bAUTO initialized successfully")
    
    def run(self, instructions: str | List[str], close_browser: bool = True) -> bool:
        """
        Execute automation from instructions.
        
        Args:
            instructions: Natural language instructions (string or list)
            close_browser: Whether to close browser when done
        
        Returns:
            True if all actions succeeded
        """
        
        try:
            # Create browser
            self._initialize_browser()
            
            # Parse instructions
            logger.info("Parsing instructions")
            action_queue = self.parser.parse(instructions)
            logger.info(f"Parsed {len(action_queue)} actions")
            
            # Execute actions
            all_success = True
            for i, action in enumerate(action_queue, 1):
                logger.info(f"[{i}/{len(action_queue)}] Processing: {action[:80]}...")
                
                success = self._execute_action(action)
                if not success:
                    all_success = False
                    if self.config.automation.retry_attempts <= 1:
                        logger.error("Action failed, stopping execution")
                        break
                
                # Delay between actions
                if i < len(action_queue):
                    import time
                    time.sleep(self.config.automation.action_delay)
            
            if all_success:
                logger.info("All actions completed successfully!")
            else:
                logger.warning("Some actions failed")
            
            return all_success
            
        except Exception as e:
            logger.error(f"Automation failed: {e}", exc_info=True)
            return False
            
        finally:
            if close_browser and self.driver:
                self._cleanup()
    
    def run_from_file(self, filepath: str, output_file: Optional[str] = None,
                     close_browser: bool = True) -> bool:
        """
        Execute automation from instruction file.
        
        Args:
            filepath: Path to instruction file
            output_file: Optional path to save results
            close_browser: Whether to close browser when done
        
        Returns:
            True if successful
        """
        
        logger.info(f"Loading instructions from: {filepath}")
        instructions = read_instructions(filepath)
        
        result = self.run(instructions, close_browser)
        
        if output_file:
            save_output(output_file, {
                "success": result,
                "instructions_file": filepath
            })
        
        return result
    
    def _initialize_browser(self):
        """Initialize browser and engine."""
        if self.driver is None:
            logger.info("Creating browser instance")
            self.driver, self.env = create_browser(self.config)
            self.engine = ActionEngine(
                self.env,
                screenshot_on_error=self.config.automation.screenshot_on_error,
                screenshot_dir=self.config.automation.error_screenshot_dir
            )
    
    def _execute_action(self, action: str) -> bool:
        """Execute a single action with retry logic."""
        
        last_error = None
        
        for attempt in range(self.config.automation.retry_attempts):
            if attempt > 0:
                logger.info(f"Retry attempt {attempt + 1}/{self.config.automation.retry_attempts}")
            
            # Generate code
            try:
                code = self.code_generator.generate(
                    action,
                    retry_on_error=last_error
                )
            except Exception as e:
                logger.error(f"Code generation failed: {e}")
                return False
            
            # Execute code
            success, error = self.engine.execute(code)
            
            if success:
                # Add small delay after successful action to ensure stability
                import time
                time.sleep(0.5)
                return True
            
            last_error = error
            
            # Don't retry if no retries configured
            if self.config.automation.retry_attempts <= 1:
                break
        
        return False
    
    def _cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up")
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
            self.env = None
            self.engine = None
    
    def get_page_text(self) -> str:
        """Get current page text."""
        if self.env:
            return self.env.get_page_text()
        return ""
    
    def get_current_url(self) -> str:
        """Get current URL."""
        if self.env:
            return self.env.get_current_url()
        return ""
    
    def screenshot(self, filename: str):
        """Take screenshot."""
        if self.env:
            self.env.screenshot(filename)

