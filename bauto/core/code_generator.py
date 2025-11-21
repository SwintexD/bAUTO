"""
Action Code Generator for bAUTO
================================

Generates Selenium code from natural language using AI.
"""

import logging
from typing import Optional

from .ai_interface import AIModelInterface

logger = logging.getLogger(__name__)


class CodeGenerator:
    """Generates executable Selenium code from natural language."""
    
    # Base system prompt that defines the automation environment
    SYSTEM_PROMPT = """You are an expert Selenium automation code generator.

IMPORTANT: Generate code that EXECUTES IMMEDIATELY. Do not wrap code in functions or classes unless absolutely necessary.
If you must use functions, ALWAYS call them at the end.

You have access to an automation environment (env) with these methods:

Core Navigation:
- env.navigate(url) - Navigate to a URL
- env.wait(seconds) - Wait for specified seconds
- env.refresh() - Refresh the current page

Element Finding:
- env.find_element(by='xpath', value=None) - Find single element
- env.find_elements(by='xpath', value=None) - Find multiple elements
- env.find_visible_element(by='xpath', value=None) - Find first visible element
- env.find_element_by_text(text, tag='*') - Find element containing text

Element Interaction:
- env.click(element) - Click an element
- env.type_text(element, text) - Type text into element
- env.clear_and_type(element, text) - Clear then type
- env.select_option(element, value) - Select dropdown option
- env.check_checkbox(element, checked=True) - Check/uncheck

Page Interaction:
- env.scroll(direction) - Scroll page ('up', 'down', 'top', 'bottom')
- env.screenshot(filename) - Take screenshot
- env.get_page_text() - Get all visible text
- env.execute_script(script) - Run JavaScript

Element Properties:
- env.get_text(element) - Get element text
- env.get_attribute(element, attr) - Get element attribute
- env.is_visible(element) - Check if element is visible
- env.is_enabled(element) - Check if element is enabled

Guidelines:
1. Write DIRECT, EXECUTABLE code - no function definitions unless necessary
2. Use xpath with contains() for flexible matching: //button[contains(normalize-space(), 'Click')]
3. Always use env methods, never call element methods directly
4. Import Keys from selenium.webdriver.common.keys if needed
5. Write clean, minimal code without comments
6. Handle common cases like waiting for elements
7. If you define a function/class, ALWAYS call it immediately after

CRITICAL: Code must execute immediately. Do NOT leave functions uncalled.

Example (GOOD):
env.navigate("https://example.com")
element = env.find_element(by='xpath', value='//input')
env.type_text(element, "text")

Example (BAD - function not called):
def main():
    env.navigate("https://example.com")
# Missing: main() call

Generate ONLY executable Python code, no explanations.
"""

    def __init__(self, ai_interface: AIModelInterface, cache_enabled: bool = True):
        self.ai = ai_interface
        self.cache_enabled = cache_enabled
        self._code_cache = {}
    
    def generate(self, instruction: str, context: Optional[str] = None, 
                 retry_on_error: Optional[str] = None) -> str:
        """
        Generate Selenium code from natural language instruction.
        
        Args:
            instruction: Natural language instruction
            context: Additional context (e.g., previous actions)
            retry_on_error: Error message from previous attempt (for retry)
        
        Returns:
            Generated Python code
        """
        
        # Check cache
        cache_key = f"{instruction}:{context}:{retry_on_error}"
        if self.cache_enabled and cache_key in self._code_cache:
            logger.debug("Using cached code generation")
            return self._code_cache[cache_key]
        
        # Build prompt
        prompt = self._build_prompt(instruction, context, retry_on_error)
        
        # Generate code
        try:
            code = self.ai.generate_with_retry(
                prompt,
                temperature=0.0,
                max_tokens=1024
            )
            
            # Clean up code
            code = self._clean_code(code)
            
            # Cache result
            if self.cache_enabled:
                self._code_cache[cache_key] = code
            
            logger.debug(f"Generated code:\n{code}")
            return code
            
        except Exception as e:
            logger.error(f"Failed to generate code: {e}")
            raise
    
    def _build_prompt(self, instruction: str, context: Optional[str], 
                      error: Optional[str]) -> str:
        """Build the complete prompt for code generation."""
        
        prompt = f"{self.SYSTEM_PROMPT}\n\n"
        
        if context:
            prompt += f"Previous context:\n{context}\n\n"
        
        prompt += f"INSTRUCTION:\n{instruction}\n\n"
        
        if error:
            prompt += f"Previous attempt failed with error:\n{error}\n\n"
            prompt += "Fix the error and try again.\n\n"
        
        prompt += "OUTPUT (Python code only):\n```python\n"
        
        return prompt
    
    def _clean_code(self, code: str) -> str:
        """Clean up generated code and ensure it's executable."""
        # Remove markdown code blocks
        code = code.replace("```python", "").replace("```", "")
        
        # Remove common prefixes
        code = code.strip()
        
        # Remove excessive blank lines
        lines = code.split("\n")
        cleaned_lines = []
        prev_blank = False
        
        for line in lines:
            is_blank = not line.strip()
            if is_blank and prev_blank:
                continue
            cleaned_lines.append(line)
            prev_blank = is_blank
        
        code = "\n".join(cleaned_lines).strip()
        
        # Check if code defines functions/classes but doesn't call them
        has_def = 'def ' in code or 'class ' in code
        has_direct_calls = any(line.strip() and not line.strip().startswith(('def ', 'class ', 'import ', 'from ', '#'))
                               for line in code.split('\n'))
        
        # If code only has definitions but no direct execution, wrap and call
        if has_def and not has_direct_calls:
            # Find main callable (function or class method)
            if 'class ' in code:
                # Extract class name and add instantiation + call
                import re
                class_match = re.search(r'class\s+(\w+)', code)
                if class_match:
                    class_name = class_match.group(1)
                    code += f"\n\n# Execute\ninstance = {class_name}(env)\nif hasattr(instance, 'run'):\n    instance.run()\nelif hasattr(instance, '__call__'):\n    instance()"
            elif 'def main' in code or 'def automation' in code:
                # Call the main/automation function
                if 'def main' in code:
                    code += "\n\n# Execute\nmain(env)"
                elif 'def automation' in code:
                    code += "\n\n# Execute\nautomation()"
        
        return code
    
    def clear_cache(self):
        """Clear the code generation cache."""
        self._code_cache.clear()
        logger.info("Code generation cache cleared")

