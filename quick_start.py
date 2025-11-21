"""
Quick Start Script for bAUTO
=============================

Run this to quickly test bAUTO.
"""

import os
import sys
from getpass import getpass
from dotenv import load_dotenv

# Add bauto to path
sys.path.insert(0, os.path.dirname(__file__))

from bauto.config.settings import Config, ModelConfig
from bauto.core.automator import BrowserAutomator


def main():
    """Run a quick demo automation."""
    
    print("=" * 60)
    print("  bAUTO - Browser Automation with AI")
    print("=" * 60)
    print()
    
    # Load environment
    load_dotenv()
    
    # Check for API key
    if not os.environ.get("GOOGLE_API_KEY") and not os.environ.get("OPENAI_API_KEY"):
        print("[WARN] API Key Required")
        print()
        print("You need a Google Gemini API key to use bAUTO.")
        print("Get one free at: https://makersuite.google.com/app/apikey")
        print()
        
        api_key = getpass("Enter your Google API Key: ").strip()
        if not api_key:
            print("[ERROR] API key is required. Exiting.")
            return
        
        os.environ["GOOGLE_API_KEY"] = api_key
        
        # Save to .env
        with open(".env", "w") as f:
            f.write(f"GOOGLE_API_KEY={api_key}\n")
        
        print("[SUCCESS] API key saved to .env file")
        print()
    
    # Create configuration
    print("Configuring bAUTO...")
    config = Config(
        model=ModelConfig(
            provider="gemini",
            model_name="models/gemini-2.0-flash"  # Using stable 2.0 flash model
        )
    )
    
    # Create automator
    automator = BrowserAutomator(config)
    
    # Demo instructions
    instructions = """
    # Step 1: Go directly to Wikipedia
    Navigate to https://www.wikipedia.org
    Wait 3 seconds for the Wikipedia homepage to fully load
    
    # Step 2: Search inside Wikipedia for Artificial Intelligence
    Find the Wikipedia search box on the page Type "Artificial Intelligence" in the search box Press Enter to search
    
    # Step 3: Wait for article to load
    Wait 4 seconds for the Artificial Intelligence article page to fully load
    
    # Step 4: Scroll down to see more content
    Scroll down the page slowly
    Wait 2 seconds
    
    # Step 5: Take a screenshot of the article
    Take a screenshot and save as "wikipedia_ai.png"
    """
    
    print("Starting automation...")
    print()
    print("Task: Search Wikipedia for 'Artificial Intelligence'")
    print()
    
    # Run automation
    try:
        success = automator.run(instructions, close_browser=True)
        
        print()
        if success:
            print("[SUCCESS] Automation completed successfully!")
            print("Screenshot saved as 'wikipedia_ai.png'")
        else:
            print("[FAILED] Automation encountered errors")
        
    except KeyboardInterrupt:
        print("\n[WARN] Automation interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
    
    print()
    print("=" * 60)
    print("Next steps:")
    print("  1. Check the examples in bauto/examples/")
    print("  2. Create your own instruction files")
    print("  3. Run: python -m bauto.cli run <instruction_file>")
    print("=" * 60)


if __name__ == "__main__":
    main()

