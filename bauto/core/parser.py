"""
Instruction Parser for bAUTO
============================

Converts natural language instructions into structured action plans.
"""

import logging
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ActionStep:
    """Represents a single action step."""
    
    instruction: str
    generated_code: Optional[str] = None
    executed: bool = False
    error: Optional[str] = None


class InstructionParser:
    """Parses and manages instruction sequences."""
    
    # Instruction keywords
    FUNCTION_START = "DEFINE_FUNCTION"
    FUNCTION_END = "END_FUNCTION"
    CALL_FUNCTION = "CALL"
    
    def __init__(self):
        self.functions: Dict[str, List[str]] = {}
        self.action_queue: List[str] = []
        
    def parse(self, instructions: str | List[str]) -> List[str]:
        """
        Parse instructions into executable action queue.
        
        Supports:
        - Plain instructions
        - Function definitions
        - Function calls
        - Comments (lines starting with #)
        """
        
        if isinstance(instructions, str):
            lines = instructions.strip().split("\n")
        else:
            lines = instructions
        
        # First pass: Extract functions
        self._extract_functions(lines)
        
        # Second pass: Build action queue
        self._build_action_queue(lines)
        
        return self.action_queue
    
    def _extract_functions(self, lines: List[str]):
        """Extract function definitions."""
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip comments and empty lines
            if not line or line.startswith("#"):
                i += 1
                continue
            
            # Check for function definition
            if line.startswith(self.FUNCTION_START):
                func_name = line.split()[-1]
                func_body = []
                i += 1
                
                # Collect function body
                while i < len(lines):
                    line = lines[i].strip()
                    if line.startswith(self.FUNCTION_END):
                        break
                    if line and not line.startswith("#"):
                        func_body.append(line)
                    i += 1
                
                self.functions[func_name] = func_body
                logger.debug(f"Defined function '{func_name}' with {len(func_body)} steps")
            
            i += 1
    
    def _build_action_queue(self, lines: List[str]):
        """Build the action queue from instructions."""
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            
            # Skip function definitions
            if line.startswith(self.FUNCTION_START) or line.startswith(self.FUNCTION_END):
                continue
            
            # Handle function calls
            if line.startswith(self.CALL_FUNCTION):
                func_name = line.split()[-1]
                if func_name in self.functions:
                    self.action_queue.extend(self.functions[func_name])
                    logger.debug(f"Expanded function call '{func_name}'")
                else:
                    logger.warning(f"Function '{func_name}' not found")
                continue
            
            # Regular instruction
            self.action_queue.append(line)
        
        logger.info(f"Built action queue with {len(self.action_queue)} steps")
    
    def group_related_actions(self, actions: List[str]) -> List[str]:
        """
        Group related actions into logical blocks.
        Actions that should be executed together are combined.
        """
        grouped = []
        current_block = []
        
        for action in actions:
            action_lower = action.lower()
            
            # Check if this is a continuation of previous action
            is_continuation = any(
                keyword in action_lower 
                for keyword in ["then", "and", "after that", "next"]
            )
            
            if is_continuation and current_block:
                current_block.append(action)
            else:
                # Start new block
                if current_block:
                    grouped.append("\n".join(current_block))
                current_block = [action]
        
        # Add final block
        if current_block:
            grouped.append("\n".join(current_block))
        
        return grouped
    
    def clear(self):
        """Clear all parsed data."""
        self.functions.clear()
        self.action_queue.clear()

