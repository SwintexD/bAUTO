# bAUTO 🤖

**Browser Automation with AI** - Transform natural language into browser actions using Google Gemini.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Features

- **Natural Language Control**: Write automation instructions in plain English
- **AI-Powered**: Uses Google Gemini (or OpenAI GPT) to generate Selenium code
- **Simple & Clean**: Intuitive API and CLI interface
- **Function Support**: Define reusable instruction blocks
- **Smart Retry**: Automatic retry with error recovery
- **Anti-Detection**: Stealth mode for bypassing bot detection
- **Flexible**: Supports YAML, JSON, and plain text instructions

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/SwintexD/bAUTO.git
cd bauto

# Install dependencies
pip install -r requirements.txt
```

### Setup

Run the interactive setup wizard:

```bash
python -m bauto.cli setup
```

Or manually create a `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### Your First Automation

Create a file `my_task.yaml`:

```yaml
instructions: |
  Go to https://www.google.com
  Search for "AI automation"
  Click on the first result
  Take a screenshot named "result.png"
```

Run it:

```bash
python -m bauto.cli run my_task.yaml
```

---

## 📖 Usage

### CLI Commands

#### Run automation from file

```bash
python -m bauto.cli run <instruction_file> [OPTIONS]

Options:
  --model TEXT           AI model to use (default: gemini-2.0-flash-exp)
  --headless            Run browser in headless mode
  --output PATH         Output file for results
  --profile-dir TEXT    Browser profile directory
  --retry INTEGER       Number of retry attempts (default: 3)
  --delay FLOAT         Delay between actions in seconds (default: 0.5)
  --log-level TEXT      Logging level (DEBUG/INFO/WARNING/ERROR)
  --no-cache           Disable prompt caching
```

#### Quick automation

```bash
python -m bauto.cli quick <url> <task> [OPTIONS]

Example:
  python -m bauto.cli quick "https://wikipedia.org" "Search for Python programming"
```

#### System info

```bash
python -m bauto.cli info
```

### Python API

```python
from bauto import BrowserAutomator, Config

# Create configuration
config = Config()

# Create automator
automator = BrowserAutomator(config)

# Run from instructions
instructions = """
Go to https://example.com
Find the search box and type "automation"
Click the search button
"""

automator.run(instructions)
```

---

## 📝 Instruction Format

### Simple Instructions

```yaml
instructions: |
  Navigate to https://example.com
  Click on "Sign Up"
  Fill in email with "user@example.com"
  Click Submit
```

### Using Functions

```yaml
instructions: |
  # Define reusable login function
  DEFINE_FUNCTION login
  Type "username" into the username field
  Type "password" into the password field
  Click the login button
  Wait 2 seconds
  END_FUNCTION
  
  # Use the function
  Go to https://mysite.com
  CALL login
  Navigate to dashboard
```

### Comments

Lines starting with `#` are treated as comments:

```yaml
instructions: |
  # This is a comment
  Go to https://example.com  # This works too
```

---

## 🏗️ Project Structure

```
bauto/
├── core/
│   ├── ai_interface.py      # AI provider interface
│   ├── automator.py          # Main orchestrator
│   ├── code_generator.py     # Code generation
│   └── parser.py             # Instruction parser
├── engine/
│   ├── action_engine.py      # Code execution
│   └── browser.py            # Browser management
├── config/
│   └── settings.py           # Configuration
├── utils/
│   ├── file_utils.py         # File I/O
│   └── logger.py             # Logging setup
├── examples/                 # Example instructions
└── cli.py                    # Command-line interface
```

---

## ⚙️ Configuration

### Using Config Object

```python
from bauto.config.settings import Config, ModelConfig, BrowserConfig

config = Config(
    model=ModelConfig(
        provider="gemini",
        model_name="gemini-2.0-flash-exp",
        temperature=0.0
    ),
    browser=BrowserConfig(
        headless=True,
        stealth_mode=True
    )
)
```

### From Config File

```python
config = Config.load_from_file("config.yaml")
```

`config.yaml`:

```yaml
model:
  provider: gemini
  model_name: gemini-2.0-flash-exp
  temperature: 0.0

browser:
  headless: false
  stealth_mode: true
  window_size: [1920, 1080]

automation:
  retry_attempts: 3
  action_delay: 0.5
  screenshot_on_error: true
```

---

## 🎯 Examples

Check out the `bauto/examples/` directory for more examples:

- `wikipedia_example.yaml` - Simple Wikipedia navigation
- `shopping_example.yaml` - Amazon product search
- `social_media_example.yaml` - Social media posting with functions

---

## 🔧 Advanced Features

### Custom Browser Options

```python
from bauto.config.settings import BrowserConfig

browser_config = BrowserConfig(
    headless=True,
    proxy="http://proxy.example.com:8080",
    user_agent="Custom User Agent",
    stealth_mode=True
)
```

### Error Screenshots

Automatically captures screenshots on errors:

```python
from bauto.config.settings import AutomationConfig

automation_config = AutomationConfig(
    screenshot_on_error=True,
    error_screenshot_dir="error_screenshots"
)
```

### Retry Logic

```python
automation_config = AutomationConfig(
    retry_attempts=5,
    action_delay=1.0
)
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Built with [Selenium](https://www.selenium.dev/)
- Inspired by the need for simple, AI-powered automation

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ by the bAUTO Team**

