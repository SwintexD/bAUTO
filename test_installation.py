"""
Simple test to verify bAUTO installation
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    
    print("Testing bAUTO installation...")
    print("-" * 50)
    
    errors = []
    
    # Test Python version
    print(f"[OK] Python {sys.version.split()[0]}")
    
    # Test core dependencies
    try:
        import selenium
        print(f"[OK] Selenium {selenium.__version__}")
    except ImportError as e:
        errors.append(f"[ERROR] Selenium: {e}")
    
    try:
        import google.generativeai
        print("[OK] Google Generative AI")
    except ImportError as e:
        errors.append(f"[ERROR] Google Generative AI: {e}")
    
    try:
        import webdriver_manager
        print("[OK] WebDriver Manager")
    except ImportError as e:
        errors.append(f"[ERROR] WebDriver Manager: {e}")
    
    try:
        import dotenv
        print("[OK] python-dotenv")
    except ImportError as e:
        errors.append(f"[ERROR] python-dotenv: {e}")
    
    try:
        import click
        print("[OK] Click")
    except ImportError as e:
        errors.append(f"[ERROR] Click: {e}")
    
    try:
        import yaml
        print("[OK] PyYAML")
    except ImportError as e:
        errors.append(f"[ERROR] PyYAML: {e}")
    
    # Test bAUTO modules
    print("\nTesting bAUTO modules...")
    
    try:
        from bauto.config.settings import Config
        print("[OK] bauto.config")
    except ImportError as e:
        errors.append(f"[ERROR] bauto.config: {e}")
    
    try:
        from bauto.core.automator import BrowserAutomator
        print("[OK] bauto.core")
    except ImportError as e:
        errors.append(f"[ERROR] bauto.core: {e}")
    
    try:
        from bauto.engine.browser import BrowserEnvironment
        print("[OK] bauto.engine")
    except ImportError as e:
        errors.append(f"[ERROR] bauto.engine: {e}")
    
    # Check API key
    print("\nChecking API keys...")
    if os.getenv("GOOGLE_API_KEY"):
        print("[OK] GOOGLE_API_KEY found")
    elif os.getenv("OPENAI_API_KEY"):
        print("[OK] OPENAI_API_KEY found")
    else:
        print("[WARN] No API key found (GOOGLE_API_KEY or OPENAI_API_KEY)")
        print("  Run: python -m bauto.cli setup")
    
    # Summary
    print("-" * 50)
    if errors:
        print("\n[FAILED] Installation has issues:")
        for error in errors:
            print(f"  {error}")
        print("\nInstall missing dependencies with:")
        print("  pip install -r requirements.txt")
        return False
    else:
        print("\n[SUCCESS] All checks passed! bAUTO is ready to use.")
        print("\nQuick start:")
        print("  python quick_start.py")
        return True


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)

