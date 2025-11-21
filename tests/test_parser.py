"""
Tests for Instruction Parser
============================
"""

import pytest
from bauto.core.parser import InstructionParser, ActionStep


class TestInstructionParser:
    """Test suite for InstructionParser."""
    
    def test_parse_simple_instructions(self, parser, sample_instructions):
        """Test parsing simple instructions."""
        actions = parser.parse(sample_instructions)
        
        assert len(actions) > 0
        assert any("Navigate" in action for action in actions)
        assert any("search" in action.lower() for action in actions)
    
    def test_parse_with_functions(self, parser, sample_function_instructions):
        """Test parsing instructions with function definitions."""
        actions = parser.parse(sample_function_instructions)
        
        # Should have function defined
        assert "login" in parser.functions
        assert len(parser.functions["login"]) > 0
        
        # Function should be expanded in action queue
        assert len(actions) > 0
    
    def test_function_definition_extraction(self, parser):
        """Test extraction of function definitions."""
        instructions = """
        DEFINE_FUNCTION search
        Find search box
        Type query
        Click search button
        END_FUNCTION
        """
        
        parser.parse(instructions)
        
        assert "search" in parser.functions
        assert len(parser.functions["search"]) == 3
        assert "Find search box" in parser.functions["search"]
    
    def test_function_call_expansion(self, parser):
        """Test function call expansion."""
        instructions = """
        DEFINE_FUNCTION setup
        Navigate to site
        Wait 2 seconds
        END_FUNCTION
        
        CALL setup
        Click button
        """
        
        actions = parser.parse(instructions)
        
        # Should include expanded function and regular action
        assert len(actions) == 3
        assert "Navigate to site" in actions
        assert "Click button" in actions
    
    def test_comment_filtering(self, parser):
        """Test that comments are filtered out."""
        instructions = """
        # This is a comment
        Navigate to site
        # Another comment
        Click button
        """
        
        actions = parser.parse(instructions)
        
        assert len(actions) == 2
        assert all("#" not in action for action in actions)
    
    def test_empty_lines_handling(self, parser):
        """Test handling of empty lines."""
        instructions = """
        Navigate to site
        
        
        Click button
        
        Type text
        """
        
        actions = parser.parse(instructions)
        
        assert len(actions) == 3
        assert all(action.strip() for action in actions)
    
    def test_parse_list_input(self, parser):
        """Test parsing from list of strings."""
        instructions = [
            "Navigate to https://example.com",
            "Wait 2 seconds",
            "Click button"
        ]
        
        actions = parser.parse(instructions)
        
        assert len(actions) == 3
        assert actions[0] == "Navigate to https://example.com"
    
    def test_undefined_function_call(self, parser):
        """Test calling undefined function."""
        instructions = """
        CALL undefined_function
        Navigate to site
        """
        
        actions = parser.parse(instructions)
        
        # Should continue with other actions
        assert "Navigate to site" in actions
    
    def test_nested_function_definitions(self, parser):
        """Test multiple function definitions."""
        instructions = """
        DEFINE_FUNCTION login
        Type username
        Type password
        END_FUNCTION
        
        DEFINE_FUNCTION logout
        Click profile
        Click logout
        END_FUNCTION
        
        CALL login
        Navigate to dashboard
        CALL logout
        """
        
        actions = parser.parse(instructions)
        
        assert "login" in parser.functions
        assert "logout" in parser.functions
        assert len(actions) > 0
    
    def test_clear_parser(self, parser):
        """Test clearing parser state."""
        parser.parse("DEFINE_FUNCTION test\nAction 1\nEND_FUNCTION")
        
        assert len(parser.functions) > 0
        
        parser.clear()
        
        assert len(parser.functions) == 0
        assert len(parser.action_queue) == 0
    
    def test_action_step_dataclass(self):
        """Test ActionStep dataclass."""
        step = ActionStep(
            instruction="Navigate to site",
            generated_code="env.navigate('https://example.com')",
            executed=True,
            error=None
        )
        
        assert step.instruction == "Navigate to site"
        assert step.executed is True
        assert step.error is None


class TestActionGrouping:
    """Test action grouping functionality."""
    
    def test_group_related_actions(self, parser):
        """Test grouping related actions."""
        actions = [
            "Navigate to site",
            "Then click button",
            "And type text",
            "Take screenshot"
        ]
        
        grouped = parser.group_related_actions(actions)
        
        # Actions with "then" and "and" should be grouped
        assert len(grouped) < len(actions)
    
    def test_group_independent_actions(self, parser):
        """Test that independent actions stay separate."""
        actions = [
            "Navigate to site",
            "Wait 2 seconds",
            "Click button"
        ]
        
        grouped = parser.group_related_actions(actions)
        
        assert len(grouped) == len(actions)
