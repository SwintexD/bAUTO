# Contributing to bAUTO

Thank you for your interest in contributing to bAUTO! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- A clear and descriptive title
- Detailed steps to reproduce the issue
- Expected vs. actual behavior
- Your environment (OS, Python version, bAUTO version)
- Relevant logs and error messages
- Instruction files that cause the issue

### Suggesting Features

Feature suggestions are welcome! Please:

- Use a clear and descriptive title
- Provide a detailed description of the proposed feature
- Explain why this feature would be useful
- Provide examples of how it would be used

### Pull Requests

1. **Fork the Repository**
   ```bash
   git clone https://github.com/SwintexD/bAUTO.git
   cd bauto
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Set Up Development Environment**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Make Your Changes**
   - Write clear, commented code
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

5. **Run Tests**
   ```bash
   # Run all tests
   pytest tests/ -v

   # Run with coverage
   pytest tests/ --cov=bauto --cov-report=html

   # Run specific test file
   pytest tests/test_parser.py -v
   ```

6. **Run Linting**
   ```bash
   # Format code
   black bauto/ tests/

   # Check linting
   ruff check bauto/ tests/

   # Type checking
   mypy bauto/
   ```

7. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature" # or "fix: resolve bug"
   ```

   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test additions/modifications
   - `refactor:` for code refactoring
   - `style:` for code style changes
   - `perf:` for performance improvements

8. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

## Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use type hints for function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Use meaningful variable names

### Testing

- Write tests for all new features
- Maintain or improve code coverage
- Test edge cases and error conditions
- Use mocks for external dependencies (AI API, browser)

### Documentation

- Update README.md if adding user-facing features
- Add docstrings to new functions and classes
- Include examples in docstrings
- Update CHANGELOG.md

### Project Structure

```
bauto/
├── core/              # Core automation logic
│   ├── automator.py   # Main orchestrator
│   ├── ai_interface.py # AI provider interface
│   ├── code_generator.py # Code generation
│   └── parser.py      # Instruction parser
├── engine/            # Execution engine
│   ├── browser.py     # Browser management
│   ├── action_engine.py # Action execution
│   └── memory.py      # Memory system
├── config/            # Configuration
│   └── settings.py    # Config dataclasses
└── utils/             # Utilities
    ├── logger.py      # Logging
    └── file_utils.py  # File operations

tests/                 # Test suite
├── conftest.py        # Pytest fixtures
├── test_parser.py     # Parser tests
├── test_code_generator.py
├── test_ai_interface.py
├── test_automator.py
└── test_config.py
```

## Setting Up Pre-commit Hooks

```bash
pre-commit install
```

This will run linting and formatting checks before each commit.

## Running the Full Test Suite

```bash
# Run all tests with coverage
pytest tests/ -v --cov=bauto --cov-report=html --cov-report=term

# Run specific test categories
pytest tests/test_parser.py -v
pytest tests/ -k "test_generate" -v

# Run with different Python versions (requires tox)
tox
```

## Building Documentation

```bash
cd docs/
make html
# Open docs/_build/html/index.html
```

## Release Process

1. Update version in `bauto/__init__.py`
2. Update CHANGELOG.md
3. Create a git tag
4. Push tag to GitHub
5. GitHub Actions will handle the rest

## Getting Help

- Check existing [documentation](README.md)
- Search [existing issues](https://github.com/SwintexD/bAUTO/issues)
- Join discussions in [Discussions](https://github.com/SwintexD/bAUTO/discussions)
- Ask questions by creating an issue with the `question` label

## Recognition

Contributors will be recognized in:
- README.md Contributors section
- Release notes
- CHANGELOG.md

Thank you for contributing to bAUTO! 🚀
