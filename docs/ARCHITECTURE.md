# bAUTO Architecture

This document describes the architecture and design of the bAUTO framework.

## Overview

bAUTO is a modular browser automation framework that translates natural language instructions into executable Selenium code using AI models.

```
┌─────────────────────────────────────────────────────────┐
│                      User Interface                      │
│              (CLI / Python API / YAML Files)             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   BrowserAutomator                       │
│              (Main Orchestration Layer)                  │
└────────┬───────────────────────────────┬────────────────┘
         │                               │
         ▼                               ▼
┌──────────────────┐          ┌──────────────────────────┐
│  InstructionParser│          │    CodeGenerator         │
│  - Parse YAML    │          │  - AI Interface          │
│  - Extract funcs │          │  - Prompt building       │
│  - Build queue   │          │  - Code cleaning         │
└──────────────────┘          └──────────────────────────┘
         │                               │
         │                               ▼
         │                    ┌──────────────────────────┐
         │                    │    AIModelInterface      │
         │                    │  - Gemini Provider       │
         │                    │  - (Future: OpenAI)      │
         │                    └──────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                      ActionEngine                        │
│               (Code Execution Layer)                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  BrowserEnvironment                      │
│           (Selenium Abstraction Layer)                   │
│  - Browser control  - Element finding                    │
│  - Navigation       - Interactions                       │
│  - Screenshots      - JavaScript execution               │
└─────────────────────────────────────────────────────────┘
```

## Core Components

### 1. BrowserAutomator (`core/automator.py`)

**Purpose**: Main orchestrator that coordinates all components.

**Responsibilities**:
- Initialize all subsystems
- Manage browser lifecycle
- Execute automation pipeline
- Handle errors and retries
- Cleanup resources

**Key Methods**:
- `run()` - Execute instructions
- `run_from_file()` - Execute from file
- `_execute_action()` - Execute single action with retry

### 2. InstructionParser (`core/parser.py`)

**Purpose**: Parse and structure natural language instructions.

**Responsibilities**:
- Parse YAML/text instructions
- Extract function definitions
- Build action queue
- Handle function calls

**Features**:
- Function definition support (`DEFINE_FUNCTION` / `END_FUNCTION`)
- Function calls (`CALL function_name`)
- Comment filtering
- Action grouping

### 3. CodeGenerator (`core/code_generator.py`)

**Purpose**: Generate Selenium code from instructions using AI.

**Responsibilities**:
- Build AI prompts
- Generate executable code
- Clean and validate code
- Cache generated code

**System Prompt**:
- Defines available API methods
- Provides coding guidelines
- Ensures executable output

### 4. AIModelInterface (`core/ai_interface.py`)

**Purpose**: Unified interface for AI providers.

**Current Providers**:
- **GeminiProvider**: Google Gemini integration

**Future Providers**:
- OpenAI GPT
- Anthropic Claude
- Local models (Ollama)

**Features**:
- Provider abstraction
- Response caching
- Retry with backoff
- Configuration management

### 5. ActionEngine (`engine/action_engine.py`)

**Purpose**: Execute generated code safely.

**Responsibilities**:
- Prepare execution scope
- Execute Python code
- Handle exceptions
- Capture error screenshots
- Format error messages

**Safety Measures**:
- Controlled scope
- Error containment
- Screenshot on failure

### 6. BrowserEnvironment (`engine/browser.py`)

**Purpose**: Clean abstraction over Selenium.

**API Categories**:

**Navigation**:
- `navigate(url)`
- `refresh()`
- `wait(seconds)`

**Element Finding**:
- `find_element(by, value)`
- `find_elements(by, value)`
- `find_element_by_text(text)`
- `find_visible_element(by, value)`

**Interactions**:
- `click(element)`
- `type_text(element, text)`
- `clear_and_type(element, text)`
- `select_option(element, value)`

**Page Operations**:
- `scroll(direction)`
- `screenshot(filename)`
- `execute_script(script)`
- `get_page_text()`

### 7. Configuration System (`config/settings.py`)

**Purpose**: Centralized configuration management.

**Config Classes**:
- `ModelConfig` - AI model settings
- `BrowserConfig` - Browser options
- `AutomationConfig` - Automation behavior

**Features**:
- Environment variable loading
- YAML/JSON file support
- Validation
- Default values

## Data Flow

```
1. User Input (YAML/CLI/API)
   ↓
2. InstructionParser
   - Parse instructions
   - Extract functions
   - Build action queue
   ↓
3. For each action:
   a. CodeGenerator
      - Build prompt
      - Call AI (cached)
      - Clean code
   ↓
   b. ActionEngine
      - Prepare scope
      - Execute code
      - Handle errors
   ↓
   c. BrowserEnvironment
      - Perform Selenium actions
      - Return results
   ↓
4. Results & Cleanup
```

## Design Patterns

### 1. Strategy Pattern
- AI providers implement `AIProvider` interface
- Easy to add new AI providers

### 2. Factory Pattern
- `create_browser()` factory for browser creation
- Encapsulates complex setup

### 3. Facade Pattern
- `BrowserEnvironment` simplifies Selenium API
- `BrowserAutomator` provides simple public API

### 4. Template Method
- `_execute_action()` defines retry template
- Subclasses can customize behavior

## Error Handling

### Retry Strategy

```python
for attempt in range(retry_attempts):
    try:
        code = generate_code(action, last_error)
        success = execute(code)
        if success:
            return True
    except Exception as e:
        last_error = e
        if attempt < max_attempts:
            continue
    return False
```

### Error Screenshot

On failure:
1. Capture screenshot
2. Save to `error_screenshots/error_{N}.png`
3. Log screenshot location
4. Continue or fail based on config

## Caching Strategy

### Code Generation Cache
- Key: `(instruction, context, error)`
- Avoids redundant AI calls
- Significantly improves performance

### AI Response Cache
- Provider-level caching
- TTL not implemented (in-memory only)
- Can be cleared manually

## Security Considerations

### Code Execution
- `exec()` with controlled scope
- Limited builtins access
- No network operations in generated code
- Browser sandbox provides additional isolation

### API Keys
- Environment variables
- Never logged or exposed
- Validated on startup

### Browser Profiles
- Isolated per automation
- Can be cleared after use
- Contains session data

## Extension Points

### Adding AI Provider

```python
class NewProvider(AIProvider):
    def generate(self, prompt: str, **kwargs) -> str:
        # Implementation
        pass
    
    def generate_with_retry(self, prompt: str, **kwargs) -> str:
        # Implementation
        pass
```

### Adding Browser Action

```python
# In BrowserEnvironment
def new_action(self, param):
    """New action description."""
    # Implementation using self.driver
```

### Adding Configuration

```python
# In settings.py
@dataclass
class NewConfig:
    option1: str = "default"
    option2: int = 42
```

## Testing Strategy

### Unit Tests
- Each component tested independently
- Mock external dependencies
- Fast execution

### Integration Tests
- Test component interactions
- Mock browser and AI
- Verify data flow

### End-to-End Tests
- Full automation scenarios
- Real browser (optional)
- Mock AI for consistency

## Performance Considerations

### Bottlenecks
1. AI API calls (mitigated by caching)
2. Browser operations (inherently slow)
3. Network latency

### Optimizations
- Prompt caching
- Response caching
- Batch operations when possible
- Async operations (future)

## Future Architecture

### Planned Enhancements
1. Async/await support
2. Parallel execution
3. Distributed automation
4. Memory/context system
5. Multi-browser support
6. Plugin system

### Scalability
- Horizontal: Multiple browser instances
- Vertical: Faster models, caching
- Cloud: Selenium Grid integration

