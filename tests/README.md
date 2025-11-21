# bAUTO Test Suite

Comprehensive test suite for the bAUTO framework.

## Running Tests

### All Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=bauto --cov-report=html

# Run in parallel
pytest tests/ -n auto
```

### Specific Tests

```bash
# Run specific test file
pytest tests/test_parser.py -v

# Run specific test class
pytest tests/test_parser.py::TestInstructionParser -v

# Run specific test method
pytest tests/test_parser.py::TestInstructionParser::test_parse_simple_instructions -v

# Run tests matching pattern
pytest tests/ -k "test_generate" -v
```

### Test Categories

```bash
# Run only unit tests
pytest tests/ -m unit

# Run only integration tests
pytest tests/ -m integration

# Skip slow tests
pytest tests/ -m "not slow"
```

## Test Structure

```
tests/
├── __init__.py              # Test package init
├── conftest.py              # Pytest fixtures
├── test_parser.py           # Instruction parser tests
├── test_code_generator.py   # Code generation tests
├── test_ai_interface.py     # AI provider tests
├── test_automator.py        # Main automator tests
└── test_config.py           # Configuration tests
```

## Fixtures

Common fixtures available in `conftest.py`:

- `mock_api_key` - Mock Google API key
- `test_config` - Test configuration object
- `mock_ai_interface` - Mock AI interface
- `mock_browser_env` - Mock browser environment
- `sample_instructions` - Sample instruction strings
- `parser` - Fresh parser instance

## Coverage

To generate coverage report:

```bash
# Terminal report
pytest tests/ --cov=bauto --cov-report=term-missing

# HTML report (opens in browser)
pytest tests/ --cov=bauto --cov-report=html
open htmlcov/index.html
```

## Writing Tests

### Test Naming

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Test

```python
def test_my_feature(mock_ai_interface):
    """Test description."""
    # Arrange
    generator = CodeGenerator(mock_ai_interface)
    
    # Act
    result = generator.generate("Navigate to site")
    
    # Assert
    assert "env.navigate" in result
```

### Using Mocks

```python
from unittest.mock import Mock, patch

@patch('bauto.core.automator.create_browser')
def test_with_mock(mock_create_browser):
    mock_create_browser.return_value = (Mock(), Mock())
    # Your test code
```

## Continuous Integration

Tests run automatically on:
- Push to main/develop branches
- Pull requests
- Multiple Python versions (3.8, 3.9, 3.10, 3.11)
- Multiple OS (Ubuntu, Windows, macOS)

## Test Requirements

```bash
pip install -r requirements-dev.txt
```

Includes:
- pytest
- pytest-cov (coverage)
- pytest-mock (mocking)
- pytest-timeout (timeout handling)
- pytest-xdist (parallel execution)

