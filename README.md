# 🐳bAUTO🐬

**Browser Automation with AI** - Transform natural language instructions into browser actions seamlessly.


[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---
<img src="https://github.com/user-attachments/assets/07830728-9d1e-4fcb-b327-410c777925f5" alt="developer illustration" width="512px" align="center"/>

For better quality media(open image for see video): https://i.imgur.com/hf9XgAi.mp4
## 🌀 Features

- 🐝 **AI-Powered**: Uses Google Gemini or OpenAI to understand natural language instructions
- 🐝 **Simple Syntax**: Write automation in plain English
- 🐝 **Smart Retry**: Automatic retry with error context for robust execution
- 📦 **Function System**: Define and reuse instruction blocks
- 🐝 **Clean API**: Both CLI and Python API available
- 🐝 **Stealth Mode**: Advanced anti-detection for realistic browsing
- 🐝 **Error Screenshots**: Automatic screenshots on failure
- 👉 **Caching**: Smart prompt caching for faster execution

---

## 🚤 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/SwintexD/bAUTO.git
cd bauto

# Install dependencies
pip install -r requirements.txt

# Or install from PyPI (coming soon)
pip install bauto
```

### Setup API Key

Get a free Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

```bash
# Interactive setup
python -m bauto.cli setup

# Or create .env file manually
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### Run Demo

```bash
python quick_start.py
```

---

## 📖 Usage

### Command Line Interface

```bash
# Run automation from file
python -m bauto.cli run instructions.yaml

# Quick automation without file
python -m bauto.cli quick "https://google.com" "Search for AI automation"

# Check system info
python -m bauto.cli info
```

### Python API

```python
from bauto import BrowserAutomator, Config, ModelConfig

# Simple usage
automator = BrowserAutomator()
automator.run("Go to google.com and search for Python")

# With custom configuration
config = Config(
    model=ModelConfig(model_name="models/gemini-2.0-flash"),
    browser=BrowserConfig(headless=True),
    automation=AutomationConfig(retry_attempts=3)
)
automator = BrowserAutomator(config)
automator.run("Navigate to https://example.com")
```

### Instruction Files

Create a YAML file with your instructions:

```yaml
# my_task.yaml
instructions: |
  # Simple task
  Navigate to https://google.com
  Wait 2 seconds
  Find the search box
  Type "AI automation" in the search box
  Press Enter
  Wait 3 seconds
  Take a screenshot and save as "result.png"
```

Run it:

```bash
python -m bauto.cli run my_task.yaml
```

### Function System

Define reusable functions:

```yaml
instructions: |
  # Define a login function
  DEFINE_FUNCTION login
  Navigate to https://example.com/login
  Type "username" in username field
  Type "password" in password field
  Click login button
  Wait 2 seconds
  END_FUNCTION
  
  # Use the function
  CALL login
  Navigate to dashboard
  Take screenshot
```

---

## 📂 Project Structure

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
├── config/            # Configuration system
│   └── settings.py    # Config dataclasses
├── utils/             # Utilities
│   ├── logger.py      # Logging
│   └── file_utils.py  # File operations
└── examples/          # Example instruction files

tests/                 # Comprehensive test suite
quick_start.py         # Quick demo script
```

---

## ✅ Examples

Check out the `bauto/examples/` directory for complete examples:

- **wikipedia_example.yaml** - Simple Wikipedia search
- **shopping_example.yaml** - E-commerce workflow
- **social_media_example.yaml** - Social media automation with functions
- **advanced_example.yaml** - Complex GitHub workflow
- **form_filling_example.yaml** - Form automation

---

## ⚙️ Configuration

### Environment Variables

```bash
GOOGLE_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key  # Alternative
```

### Configuration File

Create `config.yaml`:

```yaml
model:
  provider: gemini
  model_name: models/gemini-2.0-flash
  temperature: 0.0

browser:
  headless: false
  stealth_mode: true
  profile_dir: browser_profile

automation:
  retry_attempts: 3
  action_delay: 0.5
  screenshot_on_error: true
  log_level: INFO
```

---

## 🧪 Testing

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=bauto --cov-report=html

# Run specific tests
pytest tests/test_parser.py -v

# Run linting
black bauto/ tests/
ruff check bauto/ tests/
```

---

## 📚 Documentation

### Browser Environment API

The framework provides a clean interface over Selenium:

```python
env.navigate(url)                    # Navigate to URL
env.find_element_by_text("text")     # Find element by text
env.click(element)                   # Click element
env.type_text(element, "text")       # Type text
env.screenshot("filename.png")       # Take screenshot
env.scroll("down")                   # Scroll page
env.wait(seconds)                    # Wait
```

### Available Actions

- **Navigation**: Navigate, go to, visit
- **Interaction**: Click, type, press enter, scroll
- **Waiting**: Wait X seconds, pause
- **Screenshots**: Take screenshot, capture page
- **Forms**: Fill form, select option, check checkbox

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🐛 Troubleshooting

### Common Issues

**Blank Screenshots**
- Solution: Add `Wait 3 seconds` after navigation before taking screenshots

**Element Not Found**
- Solution: Add wait times and use more specific descriptions

**Browser Crashes**
- Solution: Try disabling headless mode or clearing browser profile

For more help, check [Issues](https://github.com/SwintexD/bAUTO/issues) or create a new one.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Selenium](https://www.selenium.dev/)
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Inspired by the need for simpler browser automation

---

## 📊 Project Stats

- **8 main modules** with clean architecture
- **15+ classes** well documented
- **50+ methods** with type hints
- **Comprehensive test suite** with pytest
- **5 complete examples** included

---

## 💬 Community

- [Discussions](https://github.com/SwintexD/bAUTO/discussions) - Ask questions, share ideas
- [Issues](https://github.com/SwintexD/bAUTO/issues) - Report bugs, request features
- [Contributing](CONTRIBUTING.md) - Contribute to the project

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ by the bAUTO community**

**Version:** 1.0.0 | **Python:** 3.8+  | **License:** MIT

