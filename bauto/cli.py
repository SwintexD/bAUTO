"""
bAUTO - Browser Automation with AI
===================================

Command-line interface for bAUTO.
"""

import os
import sys
import click
from dotenv import load_dotenv

from bauto.config.settings import Config, ModelConfig, BrowserConfig, AutomationConfig
from bauto.core.automator import BrowserAutomator
from bauto.utils.logger import setup_logging

# Load environment variables
load_dotenv()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    bAUTO - Intelligent Browser Automation with AI
    
    Transform natural language into browser actions.
    """
    pass


@cli.command()
@click.argument('instruction_file', type=click.Path(exists=True))
@click.option('--model', default='models/gemini-2.0-flash', help='AI model to use')
@click.option('--headless', is_flag=True, help='Run browser in headless mode')
@click.option('--output', type=click.Path(), help='Output file for results')
@click.option('--profile-dir', default='browser_profile', help='Browser profile directory')
@click.option('--retry', default=3, type=int, help='Number of retry attempts')
@click.option('--delay', default=0.5, type=float, help='Delay between actions (seconds)')
@click.option('--log-level', default='INFO', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']))
@click.option('--no-cache', is_flag=True, help='Disable prompt caching')
def run(instruction_file, model, headless, output, profile_dir, retry, delay, log_level, no_cache):
    """
    Run automation from instruction file.
    
    Example:
        bauto run instructions.yaml --model gemini-2.0-flash-exp
    """
    
    # Check API key
    if "GOOGLE_API_KEY" not in os.environ and "OPENAI_API_KEY" not in os.environ:
        click.echo("❌ API key not found!", err=True)
        click.echo("Please set GOOGLE_API_KEY or OPENAI_API_KEY environment variable.", err=True)
        sys.exit(1)
    
    # Setup logging
    setup_logging(level=log_level)
    
    # Determine provider from model name
    provider = "gemini" if "gemini" in model.lower() else "openai"
    
    # Create configuration
    config = Config(
        model=ModelConfig(
            provider=provider,
            model_name=model
        ),
        browser=BrowserConfig(
            headless=headless,
            profile_dir=profile_dir
        ),
        automation=AutomationConfig(
            retry_attempts=retry,
            action_delay=delay,
            log_level=log_level,
            cache_prompts=not no_cache
        )
    )
    
    # Create automator
    automator = BrowserAutomator(config)
    
    # Run automation
    click.echo(f"Starting bAUTO automation...")
    click.echo(f"Instructions: {instruction_file}")
    click.echo(f"Model: {model}")
    
    success = automator.run_from_file(instruction_file, output_file=output)
    
    if success:
        click.echo("[SUCCESS] Automation completed successfully!")
    else:
        click.echo("[FAILED] Automation failed.", err=True)
        sys.exit(1)


@cli.command()
@click.argument('url')
@click.argument('task')
@click.option('--model', default='models/gemini-2.0-flash', help='AI model to use')
@click.option('--headless', is_flag=True, help='Run browser in headless mode')
def quick(url, task, model, headless):
    """
    Quick automation task.
    
    Example:
        bauto quick "https://google.com" "Search for AI automation"
    """
    
    # Check API key
    if "GOOGLE_API_KEY" not in os.environ and "OPENAI_API_KEY" not in os.environ:
        click.echo("[ERROR] API key not found!", err=True)
        click.echo("Please set GOOGLE_API_KEY or OPENAI_API_KEY environment variable.", err=True)
        sys.exit(1)
    
    # Setup logging
    setup_logging(level="INFO")
    
    # Determine provider
    provider = "gemini" if "gemini" in model.lower() else "openai"
    
    # Create configuration
    config = Config(
        model=ModelConfig(provider=provider, model_name=model),
        browser=BrowserConfig(headless=headless)
    )
    
    # Create automator
    automator = BrowserAutomator(config)
    
    # Build instructions
    instructions = [
        f"Navigate to {url}",
        task
    ]
    
    click.echo(f"Quick automation...")
    click.echo(f"URL: {url}")
    click.echo(f"Task: {task}")
    
    success = automator.run(instructions)
    
    if success:
        click.echo("[SUCCESS] Task completed!")
    else:
        click.echo("[FAILED] Task failed.", err=True)
        sys.exit(1)


@cli.command()
def setup():
    """
    Interactive setup wizard.
    """
    
    click.echo("bAUTO Setup Wizard")
    click.echo("=" * 50)
    
    # Check for existing .env
    env_exists = os.path.exists(".env")
    
    if env_exists:
        if not click.confirm(".env file already exists. Overwrite?"):
            click.echo("Setup cancelled.")
            return
    
    # Get API key
    click.echo("\nAPI Key Configuration")
    click.echo("Choose your AI provider:")
    click.echo("1. Google Gemini (Recommended)")
    click.echo("2. OpenAI GPT")
    
    choice = click.prompt("Enter choice", type=int, default=1)
    
    if choice == 1:
        api_key = click.prompt("Enter your Google API Key", hide_input=True)
        with open(".env", "w") as f:
            f.write(f"GOOGLE_API_KEY={api_key}\n")
        click.echo("[SUCCESS] Gemini API key configured!")
    else:
        api_key = click.prompt("Enter your OpenAI API Key", hide_input=True)
        with open(".env", "w") as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        click.echo("[SUCCESS] OpenAI API key configured!")
    
    click.echo("\nSetup complete! You can now run:")
    click.echo("   python -m bauto.cli run <instruction_file>")


@cli.command()
def info():
    """
    Show system information.
    """
    
    click.echo("bAUTO - Browser Automation with AI")
    click.echo("=" * 50)
    click.echo(f"Version: 1.0.0")
    click.echo(f"Python: {sys.version.split()[0]}")
    
    # Check API keys
    click.echo("\nAPI Keys:")
    if os.getenv("GOOGLE_API_KEY"):
        click.echo("  [OK] Google API Key: Configured")
    else:
        click.echo("  [NOT FOUND] Google API Key: Not found")
    
    if os.getenv("OPENAI_API_KEY"):
        click.echo("  [OK] OpenAI API Key: Configured")
    else:
        click.echo("  [NOT FOUND] OpenAI API Key: Not found")
    
    # Check dependencies
    click.echo("\nDependencies:")
    try:
        import selenium
        click.echo(f"  [OK] Selenium: {selenium.__version__}")
    except:
        click.echo("  [ERROR] Selenium: Not installed")
    
    try:
        import google.generativeai
        click.echo("  [OK] Google Generative AI: Installed")
    except:
        click.echo("  [ERROR] Google Generative AI: Not installed")


if __name__ == '__main__':
    cli()

