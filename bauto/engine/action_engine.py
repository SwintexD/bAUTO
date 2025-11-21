"""
Action Execution Engine for bAUTO
==================================

Executes generated code in a safe, controlled environment.
"""

import logging
import traceback
from typing import Optional, Dict, Any

from .browser import BrowserEnvironment

logger = logging.getLogger(__name__)


class ActionEngine:
    """
    Executes generated automation code.
    Provides a safe execution environment with error handling.
    """
    
    def __init__(self, env: BrowserEnvironment, screenshot_on_error: bool = True,
                 screenshot_dir: str = "error_screenshots"):
        self.env = env
        self.screenshot_on_error = screenshot_on_error
        self.screenshot_dir = screenshot_dir
        self.execution_count = 0
    
    def execute(self, code: str, context: Optional[Dict[str, Any]] = None) -> tuple[bool, Optional[str]]:
        """
        Execute generated code.
        
        Args:
            code: Python code to execute
            context: Additional variables to inject into execution scope
        
        Returns:
            Tuple of (success, error_message)
        """
        self.execution_count += 1
        logger.info(f"Executing action #{self.execution_count}")
        
        # Always log the code being executed
        logger.info(f"Generated code:\n{code}")
        
        # Prepare execution scope
        scope = self._prepare_scope(context)
        
        try:
            # Execute code
            exec(code, scope)
            logger.info(f"Action #{self.execution_count} completed successfully")
            return True, None
            
        except Exception as e:
            error_msg = self._format_error(e)
            logger.error(f"Action #{self.execution_count} failed: {error_msg}")
            
            # Take screenshot if enabled
            if self.screenshot_on_error:
                self._save_error_screenshot()
            
            return False, error_msg
    
    def _prepare_scope(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Prepare execution scope with available objects."""
        import selenium.webdriver.common.keys as keys_module
        
        scope = {
            'env': self.env,
            'driver': self.env.driver,
            'Keys': keys_module.Keys,
            '__builtins__': __builtins__,
        }
        
        # Add custom context
        if context:
            scope.update(context)
        
        return scope
    
    def _format_error(self, exception: Exception) -> str:
        """Format exception for readability."""
        error_type = type(exception).__name__
        error_msg = str(exception)
        
        # Get traceback
        tb = traceback.format_exc()
        
        # Extract relevant lines
        lines = tb.split('\n')
        relevant_lines = []
        
        for i, line in enumerate(lines):
            if '<string>' in line or 'File' not in line:
                relevant_lines.append(line)
        
        formatted = f"{error_type}: {error_msg}"
        if relevant_lines:
            formatted += "\n" + "\n".join(relevant_lines[-5:])
        
        return formatted
    
    def _save_error_screenshot(self):
        """Save screenshot after error."""
        try:
            import os
            os.makedirs(self.screenshot_dir, exist_ok=True)
            
            filename = f"{self.screenshot_dir}/error_{self.execution_count}.png"
            self.env.screenshot(filename)
            logger.info(f"Error screenshot saved: {filename}")
        except Exception as e:
            logger.warning(f"Failed to save error screenshot: {e}")

